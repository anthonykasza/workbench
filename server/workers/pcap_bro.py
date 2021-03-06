''' PcapBro worker '''
import os
import datetime
import tempfile
import contextlib
import shutil
import gevent.subprocess
import glob
import zerorpc

class PcapBro(object):
    ''' This worker runs Bro scripts on a pcap file '''
    dependencies = ['sample']

    def __init__(self):
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")
        self.orig_dir = os.getcwd()

    def get_bro_script_path(self):
        # Just run all the scripts in the bro directory
        if os.path.exists('bro'):
            return os.path.abspath('bro')
        elif os.path.exists('workers/bro'):
            return os.path.abspath('workers/bro')
        else:
            raise Exception('pcap_bro could not find bro directory under: %s' % os.getcwd())

    def setup_pcap_inputs(self, input_data):
        ''' Write the PCAPs to disk for Bro to process and return the pcap filenames '''

        # Setup the pcap in the input data for processing by Bro. The input
        # may be either an individual sample or a sample set.
        file_list = []
        if 'sample' in input_data:
            raw_bytes = input_data['sample']['raw_bytes']
            filename = os.path.basename(input_data['sample']['filename'])
            file_list.append({'filename':filename, 'bytes':raw_bytes})
        else:
            for md5 in input_data['sample_set']['md5_list']:
                sample = self.c.get_sample(md5)['sample']
                raw_bytes = sample['raw_bytes']
                filename = os.path.basename(sample['filename'])
                file_list.append({'filename':filename, 'bytes':raw_bytes})

        # Write the pcaps to disk and keep the filenames for Bro to process
        for file_info in file_list:
            with open(file_info['filename'],'wb') as pcap_file:
                pcap_file.write(file_info['bytes'])

        # Return filenames
        return [file_info['filename'] for file_info in file_list]


    def execute(self, input_data):
        ''' Execute '''

        # Get the bro script path (workers/bro/__load__.bro)
        script_path = self.get_bro_script_path()

        # Create a temporary directory
        with self.make_temp_directory() as temp_dir:
            os.chdir(temp_dir)

            # Get the pcap inputs (filenames)
            print 'pcap_bro: Setting up PCAP inputs...'
            filenames = self.setup_pcap_inputs(input_data)
            command_line = ['bro']
            for filename in filenames:
                command_line += ['-C', '-r', filename]
            if script_path:
                command_line.append(script_path)

            # Execute command line as a subprocess
            print 'pcap_bro: Executing subprocess...'
            self.subprocess_manager(command_line)

            # Scrape up all the output log files
            print 'pcap_bro: Scraping output logs...'
            my_output = {}
            for output_log in glob.glob('*.log'):

                # Store the output into workbench, put the name:md5 in my output
                output_name = os.path.splitext(output_log)[0] + '_log'
                with open(output_log, 'rb') as bro_file:
                    raw_bytes = bro_file.read()
                    my_output[output_name] = self.c.store_sample(output_name, raw_bytes, 'bro')

            # Scrape any extracted files
            print 'pcap_bro: Scraping extracted files...'
            my_output['extracted_files'] = []
            for output_file in glob.glob('extract_files/*'):

                # Store the output into workbench, put md5s in the 'extracted_files' field
                output_name = os.path.basename(output_file)
                with open(output_file, 'rb') as extracted_file:
                    if output_name.endswith('exe'):
                        type_tag = 'pe'
                    else:
                        type_tag = output_name[-3:]
                    raw_bytes = extracted_file.read()
                    my_output['extracted_files'].append(self.c.store_sample(output_name, raw_bytes, type_tag))

        # Construct back-pointers to the PCAPs
        if 'sample' in input_data:
            my_output['pcaps'] = [input_data['sample']['md5']]
        else:
            my_output['pcaps'] = input_data['sample_set']['md5_list']

        # Return my output
        return my_output

    def subprocess_manager(self, exec_args):
        try:
            sp = gevent.subprocess.Popen(exec_args, stdout=gevent.subprocess.PIPE, stderr=gevent.subprocess.PIPE)
        except OSError:
            raise Exception('Could not run bro executable (either not installed or not in path): %s' % (exec_args))
        out, err = sp.communicate()
        if out:
            print 'standard output of subprocess: %s' % out
        if err:
            raise Exception('%s\npcap_bro had output on stderr: %s' % (exec_args, err))
        if sp.returncode:
            raise Exception('%s\npcap_bro had returncode: %d' % (exec_args, sp.returncode))

    @contextlib.contextmanager
    def make_temp_directory(self):
        temp_dir = tempfile.mkdtemp()
        try:
            yield temp_dir
        finally:
            # Remove the directory/files
            shutil.rmtree(temp_dir)
            # Change back to original directory
            os.chdir(self.orig_dir)

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.c.close()


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' pcap_bro.py: Unit test'''

    # This worker test requires a local server running
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Generate the input data for this worker
    md5 = c.store_sample('http.pcap', open('../../data/pcap/http.pcap', 'rb').read(), 'pcap')
    input_data = c.get_sample(md5)

    # Execute the worker (unit test)
    worker = PcapBro()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    import pprint
    pprint.pprint(output)

    # Execute the worker (server test)
    output = c.work_request('pcap_bro', md5)
    print '\n<<< Server Test >>>'
    import pprint
    pprint.pprint(output)

    # Open a bunch of pcaps
    data_dir = '../../data/pcap'
    file_list = [os.path.join(data_dir, child) for child in os.listdir(data_dir)]
    pcap_md5s = []
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as f:
            pcap_md5s.append(c.store_sample(filename, f.read(), 'pcap'))

    # Now store the sample set
    set_md5 = c.store_sample_set(pcap_md5s)
    print set_md5

    # Execute the worker (unit test)
    output = worker.execute({'sample_set':{'md5_list':pcap_md5s}})
    print '\n<<< Unit Test >>>'
    import pprint
    pprint.pprint(output)

    # Execute the worker (server test)
    output = c.work_request('pcap_bro', set_md5)
    print '\n<<< Server Test >>>'
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()

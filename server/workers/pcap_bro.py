''' PcapBro worker '''
import os
import datetime
import tempfile
import contextlib
import shutil
import gevent.subprocess
import glob
import zerorpc

def plugin_info():
    return {'name':'pcap_bro', 'class':'PcapBro', 'dependencies': ['sample'],
            'description': 'This worker runs Bro scripts on a pcap file. Output keys: [log_name:md5...]'}

class PcapBro(object):

    def __init__(self):
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")
        self.orig_dir = os.getcwd()

    def get_bro_scripts(self):
        # Just run all the scripts in the bro directory
        if os.path.exists('bro'):
            os.chdir('bro')
        elif os.path.exists('workers/bro'):
            os.chdir('workers/bro')
        else:
            raise Exception('pcap_bro could not find bro directory under: %s' % os.getcwd())

        # Construct absolute paths to bro scripts
        script_paths = [os.path.abspath(bro_script) for bro_script in glob.glob('*.bro')]
        return script_paths

    def pcap_inputs(self, input_data):
        # Setup handles to the input data
        raw_bytes = input_data['sample']['raw_bytes']
        filename = os.path.basename(input_data['sample']['filename'])
        with open(filename,'wb') as bro_file:
            bro_file.write(raw_bytes)
        return [filename]

    def execute(self, input_data):

        # Get all bro scripts (workers/bro/*.bro)
        script_paths = self.get_bro_scripts()

        # Create a temporary directory
        with self.make_temp_directory() as temp_dir:
            os.chdir(temp_dir)

            # Get the pcap inputs (filenames)
            filenames = self.pcap_inputs(input_data)
            command_line = ['bro']
            for filename in filenames:
                command_line += ['-C', '-r', filename]
            if script_paths:
                command_line += script_paths

            # Execute command line as a subprocess
            self.subprocess_manager(command_line)

            # Scrape up all the output log files
            my_output = {}
            for output_log in glob.glob('*.log'):

                # Store the output into workbench, put the name:md5 in my output
                output_name = os.path.splitext(output_log)[0] + '_log'
                with open(output_log, 'rb') as bro_file:
                    raw_bytes = bro_file.read()
                    my_output[output_name] = self.c.store_sample(output_name, raw_bytes, 'bro')

            # Scrape any extracted files
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
            shutil.rmtree(temp_dir)

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.c.close()

        # Change back to original directory
        os.chdir(self.orig_dir)


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' pcap_bro.py: Unit test'''
    worker = PcapBro()
    print worker.execute({'sample':{'raw_bytes':open('../../data/pcap/http.pcap', 'rb').read(),
                'filename':'http.pcap', 'import_time':datetime.datetime.now()}})

if __name__ == "__main__":
    test()

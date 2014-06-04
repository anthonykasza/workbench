## Additional Information on Workbench
* Detailed Project Description
* Configuration File Information
* Optional Tools
* Making your own Worker
* Making your own Client
* Running the IPython Notebooks
* Workbench Conventions
* Test Coverage
* Bounties (Rewards for contributing to Workbench)
* Dependency Installation Errors
* Deprecated Stuff

### Detailed Project Description
The workbench project takes the workbench metaphore seriously. It's a platform that allows you to do work; it provides a flat work surface that supports your ability to combine tools (python modules) together. In general a workbench never constrains you (oh no! you can't use those 3 tools together!) on the flip side it doesn't hold your hand either. Using the workbench software is a bit like using a Lego set, you can put the pieces together however you want AND adding your own pieces is super easy!.

* **Loosely coupled**
  * No inheritance relationships
  * No knowledge of data structures
  * Just take some input and barf some output (no format requirements)
* **Flat**
  * Workers (that's it... everything is a worker)
  * Server dynamically loads workers from a directory called 'workers'
* **Robust**
  * Worker fails to load (that's fine)
  * Worker crashes (no sweat, that request fails but system chugs on)
* **Transparency**
  * All worker output is reflected in the data store (currently Mongo)
  * Use RoboMongo (see below) to inspect exactly what workers are outputting.
* **Small Granularity:**
  * The system works by passing references from one worker to another so there is NO benefit to large granularity workers.
  * It's super easy to have a worker that aggregates information from a set of workers, the opposite (breaking apart a large code chunk into smaller units) is almost never easy.
  * Pull just what you want, workers and views (which are just workers) can be selectve about exactly which fields get pulled from which workers.

### Configuration File Information
When you first run workbench it copies default.ini to config.ini within the workbench/server directory, you can make local changes to this file without worrying about it getting overwritten on the next 'git pull'. Also you can store API keys in it because it never gets pushed back to the repository.

```
# Example/default configuration for the workbench server
[workbench]

# Server URI (server machine ip or name)
# Example: mybigserver or 12.34.56.789
server_uri = localhost

# DataStore URI (datastore machine ip or name)
# Example: mybigserver or 12.34.56.789
datastore_uri = localhost

# Neo4j URI (Neo4j Graph DB machine ip or name)
# Example: mybigserver or 12.34.56.789
neo4j_uri = localhost

# ElasticSearch URI (ELS machine ip or name)
# Example: mybigserver or 12.34.56.789
els_uri = localhost

# DataStore Database
# Example: customer123, ml_talk, pdf_deep
database = workbench

# Storage Limits (in MegaBytes, 0 for no limit)
worker_cap = 10
samples_cap = 200

# VT API Key
# Example: 93748163412341234v123947
vt_apikey = 123
```


### Optional Tools
**Robomongo**

Robomongo is a shell-centric cross-platform MongoDB management tool. Simply, it is a handy GUI to inspect your mongodb.

- http://robomongo.org/
- download and follow install instructions
- create a new connection to localhost (default settings fine). Name it as you wish.

### Making your own Worker
Fill in info

### Making your own Client
Although the Workbench repository has dozens of clients (see workbench/clients)there is NO official client to workbench. Clients are examples of how YOU can just use ZeroRPC from the Python, Node.js, or CLI interfaces. See [ZeroRPC](http://zerorpc.dotcloud.com/).

```python
import zerorpc
c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
with open('evil.pcap','rb') as f:
    md5 = c.store_sample('evil.pcap', f.read())
print c.work_request('pcap_meta', md5)
```

**Output from above 'client':**
```python
{'pcap_meta': {'encoding': 'binary',
  'file_size': 54339570,
  'file_type': 'tcpdump (little-endian) - version 2.4 (Ethernet, 65535)',
  'filename': 'evil.pcap',
  'import_time': '2014-02-08T22:15:50.282000Z',
  'md5': 'bba97e16d7f92240196dc0caef9c457a',
  'mime_type': 'application/vnd.tcpdump.pcap'}}
```
### Running the IPython Notebooks
* brew install freetype
* brew install gfortran
* pip install -r requirements_notebooks.txt
* Go to Starbucks..

### Workbench Conventions
Workers should adhere to the following naming conventions (not enforced)

- If you work on a specific type of sample than start the name with that
  - Examples: pcap_bro.py, pe_features.py, log_meta.py
- A worker that is new/experimental should start with 'x_' (x_pcap_razor.py)
- A 'view'(worker that handles 'presentation') should start with 'view_'
  - Examples: view_log_meta.py, view_pdf.py, view_pe.py

### Test Coverage
If you want to run the test code coverage properly you'll need to create a ~/.noserc file with these options:

    [nosetests]
    with-coverage=1
    cover-erase=1
    cover-inclusive=1
    cover-min-percentage=90
    cover-package=.

### Bounties (Rewards for contributing to Workbench)

**Top Bounties**

- [Bro Scripts for OWASP Top 10 (1000 Cow Points)](/../../issues/27)
- [Python based SWF Decompiler/Decompression (500 Cow Points)](/../../issues/28)
- [Deep PDF Static Analysis (500 Cow Points)](/../../issues/29)
- [Worker for Cab File extraction (100 Cow Points)](/../../issues/30)

**FAQ about Cow Points**

- Are Cow Points worth anything? : No
- Will Cow Points ever be worth anything? : Maybe
- Are Cow Points officially tracked? : Yes
- Will I receive good Karma for Cow Points? : Yes

### Dependency Installation Errors
**Python Modules**

Note: If you get a bunch of clang errors about unknown arguments or 'cannot link a simple C program' add the following FLAGs:
    
    ```
    $ export CFLAGS=-Qunused-arguments
    $ export CPPFLAGS=-Qunused-arguments
    ```

**Errors when running Tests**

If when running the worker tests you get some errors like 'MagicError: regexec error 17, (illegal byte sequence)' it's an issue with libmagic 5.17, revert to libmagic 5.16. Using brew on Mac:

    $ cd /usr/local
    $ brew versions libmagic # Copy the line for version 5.16, then paste (for me it looked like the following line)
    $ git checkout bfb6589 Library/Formula/libmagic.rb
    $ brew uninstall libmagic
    $ brew install libmagic
### Deprecated Stuff

**Scapy Install**

- brew tap Homebrew/python
- brew install scapy
- brew install pypcap
  - If you get error about pyrex.distutils:
    - pip install pyrex (or if this doesn't work do easy_install pyrex)
    - and then retry the 'brew install pypcap' 
  - Still not working try pyrex from scatch [pyrex](http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/)
<br><br>

  (2-5-14): For scapy python binding you have to manually install the latest release from
[secdev.org](http://www.secdev.org/projects/scapy/doc/installation.html#latest-release) and follow the instructions (like first 5 lines)
  <pre>
$ wget http://www.secdev.org/projects/scapy/files/scapy-latest.zip
$ unzip scapy-latest.zip
$ cd scapy-2.*
$ sudo python setup.py install
</pre>

### Deprecated Instructions for Ubuntu 12.04
#### Ubuntu (tested on 12.04)
- Mongo: Go through the steps given at [MongoDB Installation Tutorial](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/)
- Bro IDS: Check out the Installation tutorial [here](https://www.digitalocean.com/community/articles/how-to-install-bro-ids-2-2-on-ubuntu-12-04)
- Yara: Read the installation instructions [here](https://github.com/plusvic/yara/releases/latest)
- sudo apt-get install libmagic-dev
- sudo apt-get install libxml2-dev
- sudo apt-get install libxslt-dev
- sudo apt-get install libevent-dev

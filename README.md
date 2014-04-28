<p align="center"><img src="http://raw.github.com/supercowpowers/workbench/master/images/workbench.jpg"></p>

[![Coverage Status](https://coveralls.io/repos/SuperCowPowers/workbench/badge.png)](https://coveralls.io/r/SuperCowPowers/workbench)
workbench
=========
A light-weight and flexible approach to task management, execution and pipelining.

<pre>
git clone https://github.com/supercowpowers/workbench.git
</pre>

### Why should I give a rat's pitootie about workbench?
* **<a href="http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/Workbench_Demo.ipynb">Workbench Demo</a>**
* **<a href="http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/PCAP_DriveBy.ipynb">WIP: PCAP DriveBy Analysis</a>**
* **<a href="http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/PE_SimGraph.ipynb">Using Neo4j for PE File Sim Graph</a>**
* **<a href="http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/Generator_Pipelines.ipynb">Generator Pipelines Notebook</a>**

### Project Description
The workbench project takes the workbench metaphore seriously. It's a platform that allows you to do work; it provides a flat work surface that supports your ability to combine tools (python modules) together. In general a workbench never constrains you (oh no! you can't use those 3 tools together!) on the flip side it doesn't hold your hand either. Using the workbench software is a bit like using a Lego set, you can put the pieces together however you want AND adding your own pieces is super easy!.

If Workbench had political leanings they would be **'libertarian minarchist'**.

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
  * We cannot emphasize enough how AMAZINGLY useful small granularity is, if you don't agree you are stupid and ugly.


### Workbench Dependencies:
If the dependencies below are 'scary' than workbench probably isn't for you..
Most of the dependencies are for the server.
  
#### MongoDB
- brew install mongodb (or port or aptget or aptitude..)
- Note: Follow instructions posted at the end of install to start mongodb at login. (Recommended)

** Bro IDS: ** brew install bro (or port or aptget or aptitude..)

** LibMagic: ** brew install libmagic (or port or aptget or aptitude..)

** Yara: ** brew install yara (or port or aptget or aptitude..)

#### Python Dependencies:
Install pip, it's significantly better than easy_install.

* easy_install pip

Also setting up a python virtualenv is the way to go.. if you don't do that than you'll have to add 'sudo' in front of these commands

* cd workbench
* pip install -r requirements.txt
* Go have a large cup of coffee..

    Note: If you get a bunch of clang errors about unknown arguments or 'cannot link a simple C program' add the following FLAGs:
    
    ```
    $ export CFLAGS=-Qunused-arguments
    $ export CPPFLAGS=-Qunused-arguments
    ```

#### IPython Notebooks (optional):
* brew install freetype
* brew install gfortran
* pip install -r requirements_notebooks.txt


### Running It:
#### Server (localhost or server machine)
<pre>
$ cd workbench/server
$ python -O workbench.py
</pre>
#### Your Client (empowerment)
Note: there is NO specific client to workbench just use ZeroRPC from the Python, Node.js, or CLI interfaces. See [ZeroRPC](http://zerorpc.dotcloud.com/).
<pre>
import zerorpc
c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
with open('evil.pcap','rb') as f:
    md5 = c.store_sample('evil.pcap', f.read())
print c.work_request('pcap_meta', md5)
</pre>
**Output from above 'client':**
<pre>
{'pcap_meta': {'encoding': 'binary',
  'file_size': 54339570,
  'file_type': 'tcpdump (little-endian) - version 2.4 (Ethernet, 65535)',
  'filename': 'evil.pcap',
  'import_time': '2014-02-08T22:15:50.282000Z',
  'md5': 'bba97e16d7f92240196dc0caef9c457a',
  'mime_type': 'application/vnd.tcpdump.pcap'}}
</pre>
#### Example Clients (use -s for remote server)
There are about a dozen example clients showing how to use workbench on pcaps, PEfiles, pdfs, and log files. We even has a simple nodes.js client (looking for node devs to pop some pull requests :).
<pre>
$ cd workbench/clients
$ python simple_workbench_client.py [-s tcp://mega.server.com]
</pre>

### Testing:
Unit testing and sub-pipeline tests
<pre>
$ cd workbench/server/workers
$ ./runtests
</pre>
**Note 1:** If you look at the test() method of the workers they are setup in a way so that most of the code executes locally. This is so the test can be stepped through with a debugger and 'coverage' gets a proper line count. You should not emulate the test code for general usage of workbench (see clients for better examples of general usage).

**Note 2:** If when running the worker tests you get some errors like 'MagicError: regexec error 17, (illegal byte sequence)' it's an issue with libmagic 5.17, revert to libmagic 5.16. Using brew on Mac:

    $ cd /usr/local
    $ brew versions libmagic # Copy the line for version 5.16, then paste (for me it looked like the following line)
    $ git checkout bfb6589 Library/Formula/libmagic.rb
    $ brew uninstall libmagic
    $ brew install libmagic
      
Full pipeline tests (clients exercise a larger set of components)
<pre>
$ cd workbench/clients
$ ./runtests
</pre>
#### Coverage:
If you want to run the test code coverage properly you'll need to create a ~/.noserc file with these options:

    [nosetests]
    with-coverage=1
    cover-erase=1
    cover-inclusive=1
    cover-min-percentage=90
    cover-package=.

### Conventions:
Workers should adhere to the following naming conventions (not enforced)

- If you work on a specific type of sample than start the name with that
  - Examples: pcap_bro.py, pe_features.py, log_meta.py
- A worker that is new/experimental should start with 'x_' (x_pcap_razor.py)
- A 'view'(worker that handles 'presentation') should start with 'view_'
  - Examples: view_log_meta.py, view_pdf.py, view_pe.py
  


### Open Issues:
* Dorsey's Mom

### Tools/Optional:
#### Robomongo
Robomongo is a shell-centric cross-platform MongoDB management tool. Simply, it is a handy GUI to inspect your mongodb.
- http://robomongo.org/
- download and follow install instructions
- create a new connection to localhost (default settings fine). Name it as you wish.

### Advanced/Optional: 
#### Neo4j Install
If you'd like to play with the alpha graph database functionality you can install Neo4j and look at the clients with _graph in the name.

- brew install neo4j (or port or aptget or aptitude..)
- Note: Follow instructions posted at the end of install to start Neo4j at login. (Recommended)
- You may need to install Java JDK 1.7 [Oracle JDK 1.7 DMG](http://download.oracle.com/otn-pub/java/jdk/7u51-b13/jdk-7u51-macosx-x64.dmg) for macs. For other platforms you'll have to google (fixme: put better info here)
- pip install -U py2neo
- open http://localhost:7474/browser/
- Run one of the Neo4j indexing clients and behold the awesome

#### ElasticSearch Install
If you'd like to play with the alpha indexing functionality you can install elasticsearch and look at the clients with _indexer in the name.

- brew install elasticsearch (or port or aptget or aptitude..)
- Note: Follow instructions posted at the end of install to start elasticsearch at login. (Recommended)
- pip install -U elasticsearch

### Thanks
- Mike Sconzo for general awesomeness.
- David Dorsey for lots of great discussions and insights.
- Eric Chavez for helping with installation challenges and docs.
- Click Security: Super hugs to all specially Kit :).


<br><br><br>
### Deprecated Stuff
#### Scapy Install
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

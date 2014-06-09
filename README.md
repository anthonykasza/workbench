<p align="center"><img src="http://raw.github.com/supercowpowers/workbench/master/images/workbench.jpg"></p>

[![Build Status](https://travis-ci.org/SuperCowPowers/workbench.svg?branch=master)](https://travis-ci.org/SuperCowPowers/workbench)
[![Coverage Status](https://coveralls.io/repos/SuperCowPowers/workbench/badge.png)](https://coveralls.io/r/SuperCowPowers/workbench)
[![Code Health](https://landscape.io/github/SuperCowPowers/workbench/master/landscape.png)](https://landscape.io/github/SuperCowPowers/workbench/master)
[![Project Stats](https://www.ohloh.net/p/workbench/widgets/project_thin_badge.gif)](https://www.ohloh.net/p/workbench)
workbench
=========
The Workbench framework focuses on simplicity, transparency, and easy on-site customization.
As an open source python framework it provides light-weight task management, execution and pipelining for a loosely-coupled set of python classes. Adding your own code to Workbench is amazingly simple, please see our set of IPython notebooks below for examples.

### Why should I give a rat's pitootie about workbench?
* **<a href="http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/PCAP_to_Graph.ipynb">PCAP to Graph</a>** (A short teaser)
* **<a href="http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/Workbench_Demo.ipynb">Workbench Demo</a>**
* **<a href="http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/PCAP_to_Dataframe.ipynb">PCAP to Dataframe</a>**
* **<a href="http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/PCAP_DriveBy.ipynb">PCAP DriveBy Analysis</a>**
* **<a href="http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/PE_SimGraph.ipynb">Using Neo4j for PE File Sim Graph</a>**
* **<a href="http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/Generator_Pipelines.ipynb">Generator Pipelines Notebook</a>**
* WIP Notebooks
	* **<a href="http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/Network_Stream.ipynb">Network Stream Analysis Notebook</a>**

### Email lists (anyone can join)
- Users Email List: [workbench-users](https://groups.google.com/forum/#!forum/workbench-users)
- Developers Email List: [workbench-devs](https://groups.google.com/forum/#!forum/workbench-devs)

<br>
<img src="http://raw.github.com/supercowpowers/workbench/master/images/warning.jpg" width=90 align="left">
### Pull the repository
<pre>
git clone https://github.com/supercowpowers/workbench.git
</pre>
**Warning!: The repository contains malcious data samples, be careful, exclude the workbench directory from AV, etc...**
<br><br>

### Installing Workbench:
Please note the indexers 'Neo4j' and 'ElasticSearch' are optional. We strongly suggest you install both of them but we also appreciate that there are cases where that's not possible or feasible.

#### Mac/OSX
- brew install mongodb
- brew install yara
- brew install libmagic
- brew install bro
   - Put the bro executable in your PATH (/usr/local/bin or wherever bro is)

#### Ubuntu (14.04 and 12.04)
- sudo apt-get install mongodb
- sudo apt-get install python-dev
- sudo apt-get install g++
- sudo apt-get install libssl0.9.8
- Bro IDS: 
   - Put the bro executable in your PATH (/opt/bro/bin or wherever bro is)

    In general the Bro debian package files are WAY too locked down with dependencies on exact versions of libc6 and python2.6. We have a more 'flexible' version [Bro-2.2-Linux-x86_64_flex.deb](https://drive.google.com/uc?export=download&id=0B1QHlgNhJmssNzZ4cDdTdktPNlU). 
    - sudo dpkg -i Bro-2.2-Linux-x86_64_flex.deb
 
   If using the Debian package above doesn't work out:
   - Check out the Installation tutorial [here](https://www.digitalocean.com/community/articles/how-to-install-bro-ids-2-2-on-ubuntu-12-04)
   - or this one [here](http://www.justbeck.com/getting-started-with-bro-ids/)
   - or go to offical Bro Downloads [www.bro.org/download/](http://www.bro.org/download)

    
###Install Indexers:

#### Mac/OSX
- brew install elasticsearch
- pip install -U elasticsearch
- brew install neo4j
    - Note: You may need to install Java JDK 1.7 [Oracle JDK 1.7 DMG](http://download.oracle.com/otn-pub/java/jdk/7u51-b13/jdk-7u51-macosx-x64.dmg) for macs.

#### Ubuntu (14.04 and 12.04)
- Neo4j: See official instructions for Neo4j [here](http://www.neo4j.org/download/linux)
- ElasticSearch:
    - wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.2.1.deb
    - sudo dpkg -i elasticsearch-1.2.1.deb

#### Python Modules:
Note: Workbench has only been tested with python 2.7. If you'd like to volunteer to add support for other versions please do so. :)

* cd workbench
* pip install -r requirements.txt
* Go have a large cup of coffee...


### Running It:
#### Server (localhost or server machine)
<pre>
$ cd workbench/server
$ python -O workbench.py
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
      
Full pipeline tests (clients exercise a larger set of components)
<pre>
$ cd workbench/clients
$ ./runtests
</pre>

### Benign Error
We have no idea why occasionaly you see this pop up in the server output. To our knowledge it literally has no impact on any functionality or robustness. If you know anything about this please help us out by opening an issue and pull request. :)
<pre>
ERROR:zerorpc.channel:zerorpc.ChannelMultiplexer, unable to route event:
_zpc_more {'response_to': '67d7df3f-1f3e-45f4-b2e6-352260fa1507', 'zmqid':
['\x00\x82*\x01\xea'], 'message_id': '67d7df42-1f3e-45f4-b2e6-352260fa1507',
'v': 3} [...]
</pre>
### VirusTotal Error
If you get an error on the vt_query.py test that is completely expected. You'll have to put your own VirusTotal API key in the workbench/server/config.ini file.
<br>

### Contributions/Support/Getting Involved
Workbench is committed to providing open source security software. If you're a developer looking to chip-in or want to support the project please contact us at <support@supercowpowers.com> or visit one of the links below:

- Users email list: [workbench-users](https://groups.google.com/forum/#!forum/workbench-users)
- Developer email list: [workbench-devs](https://groups.google.com/forum/#!forum/workbench-devs)
- Feature requests: [issue tracker](https://github.com/SuperCowPowers/workbench/issues)
- **Buy a T-Shirt!**: [SuperCowPowers](http://www.supercowpowers.com/#about)
- Donate: [SuperCowPowers](http://www.supercowpowers.com/#about)

#### Pull Requests
If you going to make a pull request on the workbench repository:

- You're awesome
- Use the 'develop' branch for small changes
- Use the 'future' branch for big changes
- Make sure all tests pass
    - Workers: server/workers/runtests
    - Clients: clients/runtests
- New code must have a test and greater than 94% test coverage


### Additional Information
For additional information on the following subjects:
 
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

Please see [README_more.md](README_more.md)

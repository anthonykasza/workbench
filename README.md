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

<br>
<img src="http://raw.github.com/supercowpowers/workbench/master/images/warning.jpg" width=90 align="left">
### Pull the repository
<pre>
git clone https://github.com/supercowpowers/workbench.git
</pre>
**Warning!: The repository contains malcious data samples, be careful, exclude the workbench directory from AV, etc...**
<br><br>

### Installing Workbench:
This install gets you most of the workbench functionality, the only missing functionality are the 'indexers' Neo4j Graph DB and ElasticSearch. If you want those as well please see [Install Indexers](README_more.md####Install Indexers):

#### Mac/OSX
- brew install mongodb
- brew http://www.neo4j.org/download/linux yara
- brew install libmagic
- brew install bro

#### Ubuntu (tested on 14.04)
- sudo apt-get install mongodb
- sudo apt-get install python-dev
- sudo apt-get install g++
- Bro IDS
    - Check out the Installation tutorial [here](https://www.digitalocean.com/community/articles/how-to-install-bro-ids-2-2-on-ubuntu-12-04)
    - or this one [here](http://www.justbeck.com/getting-started-with-bro-ids/)
    - Editorial: In general the Bro debian package files are WAY too locked down with dependencies on exact versions of libc6 and python2.6. You can hack the package control file and remove those and it will work just fine.


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

### Additional Information
For additional information on the following subjects:
 
* Detailed Project Description
* Configuration File Information
* Install Indexers
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

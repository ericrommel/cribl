# Get Log Events
###### source: Cribl

## Take Home Project
### Setup
#### Hosts:
1. Agent - 1 host tagged as _`Agent`_
2. Splitter - 1 host tagged as _`Splitter`_
3. Target - 2 hosts with one tagged as _`Target-1`_ & the other as _`Target-2`_


#### Application Modes:
1. Agent - Reads from a specified file and forwards the contents to a _`Splitter`_
2. Splitter - Receives data from an _`Agent`_ and randomly splits the data
between the two configured _`Target`_ hosts
3. Target - Receives data from a _`Splitter`_ and writes it to a file on disk

#### Objectives
Automate the following tasks using language of your choice:
1. Download and install the provided application on each of the 4 hosts mentioned
in the _`Setup`_ section
- *Note:* The link to the application can be found in the “Resources” section below
2. For each _`Application Mode`_, there is a corresponding configuration directory in
the provided package; please examine these files before proceeding. You will
need to start the applications in the exact order: Targets, Splitter, Agent.
Otherwise, the deployment may not function as expected.
To start each application, run:
   
   $ node app.js <conf_directory>

3. Automate test cases for the deployment that:
- Validates all data received on the ‘Target’ nodes are correct

4. Capture all output and artifacts generated from each application/host


## Technical Requirements

These are the main tech requirement. The complete list is in requirements.txt.
- [Python 3](http://python.org/)
- [Pip](https://pip.pypa.io/)
- [Docker](https://docker-py.readthedocs.io/)


### Installing

The default Git version is the master branch.

    # clone the repository
    $ cd desired/path/
    $ git clone git@github.com:ericrommel/cribl.git

The next step is install the project's Python dependencies. Just like _Git_ if you still don't have it go to the [official site](http://python.org/) and get it done. You'll also need [Pip](https://pip.pypa.io/), same rules applies here. Another interesting tool that is not required but strongly recommended is [Pipenv](http://pipenv.readthedocs.io), it helps to manage dependencies and virtual environments.

Installing with **Pip**:

    # Go to root repository folder 
    $ cd path/to/cribl
    $ pip install -r requirements.txt

### Start Container

Docker and docker-compose should be installed first. [Tutorial here](https://docs.docker.com/install/).
At the repo root run:

    $ docker-compose up --build


### Run Tests
From Python code tests (unit tests)::

    $ pytest


## About

This project is part of [Cribl](https://cribl.io/jobs/) challenge for their QA Engineer hire process sent in April 2021.


## Author

- [Eric Dantas](https://github.com/ericrommel)

## License

This project is licensed under the GNU License - see the [License](./LICENSE) file for details.

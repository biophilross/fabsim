## fabsim README

### Personal Fabricator Diffusion Simulation

This it the protoype of a simulation package being used to study the socio-economics effects of the widespread adoption and diffusion of personal fabricators.

### Install

1. If you have git installed:
    1. Opening your command line tool of choice
    2. Changing to the directory you'd like to download the files to
    3. Using `git clone https://github.com/thephilross/fabsim.git`
2. If you just want to download the source code:
    1. Download the zip file
3. Open up your favorite command line tool and change to the fabsim project directory

4. Run `python setup.py` to install any module dependencies (assuming you have python installed)

5. Run `cd src` and then run `simulation.py test.json` to make sure the simulation runs properly

Wanna see a quick description of each *.py file? Run `pydoc simulation` (assuming yo have pydoc installed and note the lack of .py at the end). Same thing applies to all source code files replacing 'simulation' with the desired file name.


### Quick Start

If everything in the 'Install' section worked properly then you should have already been able to run your first simulation! If not…well I have some work to do.

Essentially you have two files within the _src_ directory you can run from the command line. You can either run `validate.py inputfile` or `simulation.py inputFile`

_validate.py_ is used to validate the model being used to run our simulation while _simulation.py_ is a more scalable version of _validate.py_ that should be used once the simulation results of _validate.py_ are properly understood.

### Inputs

The input files are formatted in JSON which follows a key-value data structure similar to a dictionary in python. You'll find the simulation file inputs within the inputs directory.

The inputs for _simulation.py_ are:

* **SIMLENGTH** - number of time steps per simulation
* **NUMGOODS** - number of TOTAL goods in the simulation
* **NUMCONSUMERS** - number of consumers 
* **NUMPRODUCERS** - number of produers
* **PERCENTFACTORY** - decimal value dictating the percentage of NUMGOODS that a factory can hold within its inventory. 1 - PERCENTFACTORY is the percentage of goods that a fabricator can hold within its inventorys
* **numTrials** - number of simulations to run
* **scenario** - the distribution of producers you would like to see within your simulation; currently can only choose from all factories, all fabricators or half factories and half fabricators
* **monitor** - True or False depending on whether you want to see the results of each invidual simulation in the console output

The inputs for _validate.py_ are all the same except for the following addition:

* **testCase** - see __sim_overview.md__ to understand what I mean by this

Additionally there is no option to choose how many producers are present. There are always just two.


### Outputs

Resulting data from each simulation on each producer is output to a file with the same name as the input file within the results directory in JSON format.

### Additional Documentation

Additional documentation exists in the doc directory.



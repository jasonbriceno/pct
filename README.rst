Pictionary Telephone Tool
=========================

This library defines a useful NLP/Knowledge-Retreival Engine. This documentation is for you, Gambino.
  
Installation
------------

This library is meant to be managed by anaconda (https://conda.io), which you will need to install. You'll also need to make sure that **conda-forge** is one of your channels::

  conda config --add channels conda-forge
  
You should then clone the repo, navigate to the base directory, and run::

  conda create --name <environment_name> --file requirements.txt
  
This will install the python environment and libraries, which you can activate by running::

  source activate <environment_name>
  
You should now have a fully installed pct library.

Simple Start
------------

The library comes with a simple interactor CLI, which you can run thusly::

  python -m pct.interactor.interactor
  
This interactor can be used to load directories containing all of the images for a given pictionary telephone comic. You can then modify picture order, rotation, and cropping, and finnaly compose a comic. The interactor help function should explain everything.
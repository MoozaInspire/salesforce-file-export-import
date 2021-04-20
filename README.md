*********************************************
Salesforce File/Enhanced Notes Data Migration
*********************************************

Salesforce File/Enhanced Notes Data Migration is a bunch of scripts developed in Python 3.8.7. Their goal is to help with Salesforce Files and Attachments data migration from one Salesforce org to another.

# Prerequisites
If you don't have Python on your computer we recommend to install it using [PyEnv](https://github.com/pyenv/pyenv).

On Mac you can use [brew](https://github.com/rbenv/rbenv) to install it:

    brew install pyenv
    
If you don't have brew on your machine, you can run:

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Apart from other python libraries it uses Simple Salesforce (Salesforce REST API Python library) and Future (compatibility layer between Python 2 and Python 3) which are not available by default and need to be installed extra. In order to do that you can run:

    pip install simple-salesforce
    pip install future

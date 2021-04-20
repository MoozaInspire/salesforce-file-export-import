*********************************************
# Salesforce File/Enhanced Notes Data Migration
*********************************************

Salesforce File/Enhanced Notes Data Migration is a bunch of scripts developed in Python 3.8.7. Their goal is to help with Salesforce Files and Attachments data migration from one Salesforce org to another.

## Prerequisites
If you are going to use python scripts for the first time on your Mac you might find the following commands useful.

We are going to use [brew](https://github.com/rbenv/rbenv) to install [PyEnv](https://github.com/pyenv/pyenv) and PyEnv to install Python 3.8.7.

If you don't have Homebrew on your laptop you can use the following commands to install it:

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

After you have Homebrew installed, you can run the following command in order to install PyEnv:

    brew install pyenv

If you don't have Python on your computer we recommend to install it using [PyEnv](https://github.com/pyenv/pyenv):
    
    pyenv install 3.8.7
    
We recommend to run the following command to make the version 3.8.7 global:

    pyenv global 3.8.7
    
After PyEnv is installed you will need to define environment variable PYENV_ROOT to point to the path where pyenv repo is cloned. Depending on which shell you are using on your laptop (given by OSX version). If you are not sure what shell you are using, run the following command:

    echo $0

For **-bash** value run:
    
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile

For **-zsh** value run:

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    
After 

Apart from other python libraries scripts use Simple Salesforce (Salesforce REST API Python library) and Future (compatibility layer between Python 2 and Python 3) which are not available by default and need to be installed extra. In order to do that you can run:

    pip install simple-salesforce
    pip install future

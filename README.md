*********************************************
# Salesforce File/Enhanced Notes Data Migration
*********************************************

Salesforce File/Enhanced Notes Data Migration is a bunch of scripts developed in Python 3.8.7. Their goal is to help with Salesforce Files and Attachments data migration from one Salesforce org to another.

## Prerequisites
If you are going to use python scripts for the first time on your Mac you might find the following commands useful.

### PyEnv Installation
#### Mac Users
On Mac consider using [brew](https://github.com/rbenv/rbenv) to install [PyEnv](https://github.com/pyenv/pyenv) and PyEnv to install Python 3.8.7.

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
    
#### Windows Users
If you're on Windows, consider using @kirankotari's pyenv-win fork. (pyenv does not work on windows outside the Windows Subsystem for Linux)

### Additional Python Libraries
Apart from other python libraries scripts use Simple Salesforce (Salesforce REST API Python library) and Future (compatibility layer between Python 2 and Python 3) which are not available by default and need to be installed extra. In order to do that you can run:

    pip install simple-salesforce
    pip install future
    
## Installation

    git clone https://github.com/MoozaInspire/salesforce-file-export-import.git
    
### For Mac users - you can add the repository to your PATH variable so that you can run it from anywhere
Please make sure you replace <PATH_TO_BIN_FOLDER_OF_THIS_REPOSITORY> before you run these commands

For **-bash** value run:
    
    echo 'export SFDC_FILE_MIGRATION_ROOT="$HOME/<PATH_TO_BIN_FOLDER_OF_THIS_REPOSITORY>"' >> ~/.bash_profile
    echo 'export PATH="$SFDC_FILE_MIGRATION_ROOT/bin:$PATH"' >> ~/.bash_profile
    
    e.g.
    echo 'export SFDC_FILE_MIGRATION_ROOT="$HOME/Workspace/salesforce-file-export-import/bin"' >> ~/.bash_profile
    echo 'export PATH="$SFDC_FILE_MIGRATION_ROOT/bin:$PATH"' >> ~/.bash_profile
    
    # reinitialize the shell
    source ~/.bash_profile

For **-zsh** value run:
    
    echo 'export SFDC_FILE_MIGRATION_ROOT="$HOME/<PATH_TO_BIN_FOLDER_OF_THIS_REPOSITORY>"' >> ~/.zshrc
    echo 'export PATH="$SFDC_FILE_MIGRATION_ROOT/bin:$PATH"' >> ~/.zshrc

    e.g.
    echo 'export SFDC_FILE_MIGRATION_ROOT="$HOME/Workspace/salesforce-file-export-import/bin"' >> ~/.zshrc
    echo 'export PATH="$SFDC_FILE_MIGRATION_ROOT/bin:$PATH"' >> ~/.zshrc
    
    # reinitialize the shell
    source ~/.zshrc

## Configuration

### Salesforce Credentials
All scripts require connection to Salesforce.

To be able to easily switch between environments there is a dedicated configuration file for Salesforce credentials. One configuration file represents one SF org.

For details you can have a look at the template file.

    <YOUR_LOCAL_REPOSITORY>/etc/sf_credentials_default_sandbox_template.ini
    
In the configuration file you will find the following:

    username = <USERNAME>
    password = <PASSWORD>
    security_token = <SECURITY_TOKEN>

    connect_to_sandbox = True
    domain =
    
You will need to replace values with your credentials. If you connect to sandbox make sure connect_to_sandbox is set to **True** or change it to **False** otherwise. This setting affects the login URL. Populate **domain** only if you are using custom domain.

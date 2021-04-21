*********************************************
# Salesforce File/Enhanced Notes Data Migration
*********************************************

Salesforce File/Enhanced Notes Data Migration is a bunch of scripts developed in Python 3.8.7. Their goal is to help with Salesforce Files and Attachments data migration from one Salesforce org to another.

----


## Table of Contents

* **[Prerequisites](#Prerequisites)**
  * [ Prerequisites](# Prerequisites)
* **[Installation](#installation)**
  * [PyEnv Installation](#PyEnv Installation)
    * [Mac Users](#Mac Users)
* **[Command Reference](#command-reference)**


## Prerequisites
If you are going to use python scripts for the first time on your Mac you might find the following commands useful.

### PyEnv Installation
#### Mac Users
On Mac consider using [Homebrew](https://github.com/rbenv/rbenv) to install [PyEnv](https://github.com/pyenv/pyenv) and PyEnv to install Python 3.8.7.

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
    echo 'export SFDC_FILE_MIGRATION_ROOT="$HOME/Workspace/salesforce-file-export-import"' >> ~/.bash_profile
    echo 'export PATH="$SFDC_FILE_MIGRATION_ROOT/bin:$PATH"' >> ~/.bash_profile
    
    # reinitialize the shell
    source ~/.bash_profile

For **-zsh** value run:
    
    echo 'export SFDC_FILE_MIGRATION_ROOT="$HOME/<PATH_TO_BIN_FOLDER_OF_THIS_REPOSITORY>"' >> ~/.zshrc
    echo 'export PATH="$SFDC_FILE_MIGRATION_ROOT/bin:$PATH"' >> ~/.zshrc

    e.g.
    echo 'export SFDC_FILE_MIGRATION_ROOT="$HOME/Workspace/salesforce-file-export-import"' >> ~/.zshrc
    echo 'export PATH="$SFDC_FILE_MIGRATION_ROOT/bin:$PATH"' >> ~/.zshrc
    
    # reinitialize the shell
    source ~/.zshrc

## Configuration
The following configuration is shared by all the scripts. The dedicated configuration will be described in each script section.

### Salesforce Credentials
To be able to easily switch between environments there is a dedicated configuration file for Salesforce credentials. One configuration file represents one SF org.

For details you can have a look at the template file.

    etc/sf_credentials_default_sandbox_template.ini
    
In the configuration file you will find the following:

    username = <USERNAME>
    password = <PASSWORD>
    security_token = <SECURITY_TOKEN>

    connect_to_sandbox = True
    domain =
    
You will need to replace values with your credentials. If you connect to sandbox make sure connect_to_sandbox is set to **True** or change it to **False** otherwise. This setting affects the login URL.

Populate **domain** only if you are using custom domain.

## Command Reference
* [`export_attachment.py`](#export_attachment.py)
* [`upload_attachment.py`](#upload_attachment.py)
* [`export_content_version.py`](#export_content_version.py)
* [`upload_content_version.py`](#upload_content_version.py)

### export_attachment.py

```
Export ContentDocumentLink and Attachment (Files) related to parent records (e.g. Account) from Salesforce

optional arguments:
  -h, --help            show this help message and exit
  -q query, --query query
                        SOQL to limit the valid ContentDocumentIds. Must return the Ids of parent objects.
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        Output folder
  -s SALESFORCE_CONFIG_FILE, --salesforce-config-file SALESFORCE_CONFIG_FILE
                        Salesforce config file with login info
  -c BASIC_CONFIG_FILE, --basic-config-file BASIC_CONFIG_FILE
                        Optional parameter to override default basic configuration of the script
```
 
### upload_attachment.py

```
Example:
	upload_attachments.py

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        Input CSV file with Attachment info
  -s SALESFORCE_CONFIG_FILE, --salesforce-config-file SALESFORCE_CONFIG_FILE
                        Salesforce config file with login info
  -f INPUT_FOLDER, --input-folder INPUT_FOLDER
                        Input folder with binary data - file referenced by original attachment ID
  -u USER_MAPPING, --user-mapping USER_MAPPING
                        User ID mapping in CSV format
  -p PARENT_MAPPING, --parent-mapping PARENT_MAPPING
                        Parent ID mapping in CSV format
  -v, --verbose         Verbose
```

### export_content_version.py

```
Example:
	upload_content_versions.py upload_content_versions.py -u Source_Original_Id__c -s ~/Workspace/salesforce-file-export-import/etc/sf_credentials_myproject_dev.ini -i content_version_account_dev/content_version.csv -f content_version_account_dev/ContentVersion

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        Input CSV file with ContentVersion info
  -f INPUT_FOLDER, --input-folder INPUT_FOLDER
                        Input folder with binary data - file referenced by original content version ID
  -v, --verbose         Verbose
  -s SALESFORCE_CONFIG_FILE, --salesforce-config-file SALESFORCE_CONFIG_FILE
                        Salesforce config file with login info
  -u UPSERT_KEY, --upsert-key UPSERT_KEY
                        Upsert key
```

### upload_content_version.py

```
Example:
	export_content_version.py -q "SELECT Id FROM Account" -s ~/Workspace/salesforce-file-export-import/etc/sf_credentials_myproject_uat.ini -o content_version_account_dev --include-notes True
	
optional arguments:
  -h, --help            show this help message and exit
  -q query, --query query
                        SOQL to limit the valid ContentDocumentIds. Must return the Ids of parent objects.
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        Output folder
  -s SALESFORCE_CONFIG_FILE, --salesforce-config-file SALESFORCE_CONFIG_FILE
                        Salesforce config file with login info
  -c BASIC_CONFIG_FILE, --basic-config-file BASIC_CONFIG_FILE
                        Optional parameter to override default basic configuration of the script
  --include-notes INCLUDE_NOTES
                        By default notes are included in the export - set this flag to False if you want to exclude them
```

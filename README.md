*********************************************
Salesforce File/Enhanced Notes Data Migration
*********************************************

Salesforce File/Enhanced Notes Data Migration is a bunch of scripts developed in Python 3.8.7. Their goal is to help with Salesforce Files and Attachments data migration from one Salesforce org to another.

If you don't have Python on your computer we recommend to install it using .. _PyEnv: https://github.com/pyenv/pyenv. In order to install PyEnv on Mac you can use .. _brew: https://brew.sh to install it:

.. code-block:: python

    brew install pyenv

Apart from other python libraries it uses Simple Salesforce (Salesforce REST API Python library) and Future (compatibility layer between Python 2 and Python 3) which are not available by default and need to be installed extra. In order to do that you can run:

.. code-block:: python

    pip install simple-salesforce
    pip install future

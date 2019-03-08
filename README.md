# Selenium test: send an e-mail

This repository contains a simple test using Selenium to send an e-mail using Outlook.

## Installation guide

### Selenium: Chrome
First, we will set up Selenium. The installation guide has been tested on Ubuntu.

1. Navigate to the chrome driver installation page: `http://chromedriver.chromium.org/downloads`
2. Select the relevant chrome driver. The installation has been tested with [version 2.46](https://chromedriver.storage.googleapis.com/index.html?path=2.46/)
3. Download and unzip the package anywhere on your computer (ideally in the root folder of this repository to keep track of it).
4. Add the unzipped folder to your file path. For the linux64 version, the command to append it to your file path can be found below. If you have downloaded a different version, simply replace `chromedriver_linux64` with the folder name for the version you have downloaded. 

Adding the unzipped folder to your file path:
```
export PATH=$PATH:$PWD/chromedriver_linux64
```
**Note**: When executing this command, you should have a terminal in the folder where you've unzipped the driver. Executing `ls` should display the folder `chromedriver_linux64` (or other similar distribution).
You can double check that your PATH has been successfuly updated by running:
```
echo $PATH
```
The output should include, among other things, the full path to your chrome driver folder.

### Python script

1. Navigate to the folder `python-version`
2. `python -m venv venv`: Create a virtual environment
3. `source venv/bin/activate`: Activate your environment
4. `pip install -r requirements.txt`: Install the requirements
5. The tests require you to set environment variables. See below the shell commands you need to run to set these up. Without these environment variables, the script will notify you to set them.
6. `python selenium-tests.py`: Run the tests :tada:

Environment variables:
```
export email_username="yourname@mail.mcgill.ca"
export email_password="yourpassword"
export email_recipient="recipient@mail.mcgill.ca"
```

## Demo
![demo](full_selenium_run.gif "Selenium Test Demo")

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
**Note 1**: When executing this command, you should have a terminal in the folder where you've unzipped the driver. Executing `ls` should display the folder `chromedriver_linux64` (or other similar distribution).
**Note 2**: If the file `chromedriver` (contained within `chromedriver_linux64`) is instead extracted at the root of a directory, not inside a folder named `chromedriver_<distribution>`, simply make the `PATH` variable point to the director containing `chromedriver`. In other words, go inside the directory with `chromedriver` and run:
```
export PATH=$PATH:$PWD
```

You can double check that your PATH has been successfuly updated by running:
```
echo $PATH
```
The output should include, among other things, the full path to your chrome driver folder.

### Python script

1. Navigate to the root of this repository
2. `python -m venv venv`: Create a virtual environment
3. `source venv/bin/activate`: Activate your environment
4. `pip install -r requirements.txt`: Install the requirements (namely `Selenium` and `Behave`)
5. The tests require you to set environment variables. See below the shell commands you need to run to set these up. Without these environment variables, the script will not be able to perform its "background" operation for the tests (logging in to Outlook).
6. `behave`: Run this command from the root of this repository. Tests should run as in the demo gif below ! :tada:

Environment variables:
```
export email_username="yourname@mail.mcgill.ca"
export email_password="yourpassword"
```
**Note**: This has been tested using Python 3.6.7, but any version of Python above 3.6 should be sufficient. For installing Python, [please visit the official page](https://www.python.org/downloads/). Run `python --version` to ensure you are running the correct version. If you have installed Python 3.6 or above, but the version command returns `2.7`, try running `python3 --version`. If this gives the newer version, simply run: `alias python=python3` as well as `alias pip=pip3` (the `pip` version should also match Python 3.6).

## Demo
![demo](full_selenium_run.gif "Selenium Test Demo")

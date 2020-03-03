# Night Owls Detector

This script can show you all devman users, who sent his task to check at midnight (from 00 to 1 AM).

# How to Install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

# Quickstart

For start script you need to run the script in console/terminal.

```bash
$ python seek_dev_nighters.py
```

There are two input parameters hour_from(default value 0) and hour_to(default value 6). 
You can use them to set 'night' timedelta.

Also you can find full list of parameters by running:
```bash
$ python seek_dev_nighters.py -h
```


# Output example:
```
User with name User1 sent task to check at:
	2020-02-20 00:10:35
	2020-02-15 02:08:10
------------------------------
User with name User2 sent task to check at:
	2020-01-29 00:12:26
------------------------------
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

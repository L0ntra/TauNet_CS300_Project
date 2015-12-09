# TauNet v1.0
----------------
Copyright (C) 2015 Gregory Gaston

TauNet is a secure messaging system developed for operaton on Raspberry Pi Devices running the Raspbian Operating System.

*** While this program will run on other devices and operating systems, this progam has only been tested on Raspberry Pi Devices running Raspbian Operating System.

*** As with any encryption methods it is possible that messages sent using TauNet could be intercepted and decrypted by outside sources. This program uses arcfour encryption, which is speculated to have been broken by some State Encryption Agencies [(wikipedia)](https://en.wikipedia.org/wiki/RC4).


### Setup
----------------
 * An ecnryption key that will be used by all users on TauNet neededs to be chosen. It can be any ASCII string of 1 more more characters, but a key of at least 10 characters is recommended.
 * Each user on the network will need to choose a unique user name, that they shall provide to other users along with their IP address
 * The encryption key and user information will be shared amongst all TauNet users before running TauNet for the first time.
 * To run TauNet Execute main.py using Python v3.5
```$ python3 main.py```
 * The Follow the system prompts to set up the new TauNet network
 * Once the Network setup is complete type '?' to get a list of available commands

### Future Updates
----------------
 * Store and Display sent messages
 * Display messages to/from a particular user
 * Detailed user information
 * Onion Routing
 * Redesigned interface that allows for messages to be displayed seporatly from the command line.
 * User ip updates and add user requests
 * Group Messaging
 * Track Online users
 * Encrypted user file
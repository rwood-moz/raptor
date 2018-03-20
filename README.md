[![Build Status](https://api.travis-ci.org/rwood-moz/raptor.svg?branch=master)](https://travis-ci.org/rwood-moz/raptor)

# raptor
Desktop browser performance framework prototype

## Installation
Create a python virtualenv:

    virtualenv .raptor-venv
    source .raptor-venv/bin/activate

Then run setup:

    python setup.py develop

## Running
Currently the name of the test to run is just hardcoded in the web extension (for now) until I add a command line arg for that.

To run the prototype in it's current form:

    git clone https://github.com/tarekziade/heroes

To get the 'heros' test page (this page has multiple hero timing elements). Then locally in the root dir of that cloned repo:

    python -m SimpleHTTPServer 8081

To share out the test page on localhost.

Then to run the test on Firefox, use this command line (but use your own binary location):

    raptor -b firefox -e "/Users/rwood/mozilla-unified/obj-x86_64-apple-darwin17.4.0/dist/Nightly.app/Contents/MacOS/firefox"

To run the test on Google Chrome, just use '-b chrome' and provide the location of the chrome binary.

Note: Currenlty the prototype doesn't shutdown Google Chrome automatically; so once you see the control server has received and dumped out the results, just manually close Chrome at that point.

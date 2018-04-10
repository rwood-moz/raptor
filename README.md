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
To run the prototype in it's current form:

    git clone https://github.com/tarekziade/heroes

To get the 'heros' test page (this page has multiple hero timing elements). Then locally in the root dir of that cloned repo:

    python -m SimpleHTTPServer 8081

To share out the test page on localhost.

Then to run the test on Firefox, use this command line (but use your own binary location):

    raptor -t raptor-firefox-tp7 -b "/Users/rwood/mozilla-unified/obj-x86_64-apple-darwin17.4.0/dist/Nightly.app/Contents/MacOS/firefox"

To run the test on Google Chrome, use this command line (but use your own binary location):

    raptor -t raptor-chrome-tp7 --app chrome -b "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

Note: Currently the prototype doesn't shutdown Google Chrome automatically; so once you see the control server has received the results, just manually close Chrome at that point.

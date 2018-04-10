import os
import sys
here = os.path.abspath(os.path.dirname(__file__))

# TODO Remove once this lands in mozilla-central
vendor_dir = os.path.join(os.path.dirname(here), 'vendor')
sys.path.insert(0, vendor_dir)

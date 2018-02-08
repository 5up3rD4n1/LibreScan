#!/bin/bash
# Install chdkptp for python3.6 from tar.gz
git clone --recursive https://github.com/5up3rD4n1/chdkptp.py.git
cd chdkptp.py
python setup.py sdist
python setup.py install
#!/bin/bash
cd ./pelican_planet/tests/data  # Python 3.6 does not support --directory option for http.server module
set -x
python -m http.server --bind 0.0.0.0 8088

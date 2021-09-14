#!/bin/bash
python -m http.server --directory $(pwd)/pelican_planet/tests/data --bind 0.0.0.0 8088

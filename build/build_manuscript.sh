#!/bin/bash

# Use pandoc to convert the manuscript markdown file to a pdf file using tectonic
# and place it in the output folder.

# Requires pandoc to be installed

# Install pandoc

# https://pandoc.org/installing.html

# Run this script from the root of the repository

# Usage: ./build/build_manuscript.sh

pandoc manuscript.md -o output/manuscript.pdf --pdf-engine=tectonic
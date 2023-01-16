#!/bin/bash

# Use CairoSVG to convert all SVG files in the figures folder to png
# and place them in the figures folder.

# Requires CairoSVG to be installed

# Install CairoSVG

# pip install cairosvg

# Run this script from the root of the repository

# Usage: ./build/build_figures.sh

# Path to the figures folder

FIGURES_FOLDER=figures

# Path to the output folder

OUTPUT_FOLDER=figures

# Loop through all SVG files in the figures folder

for file in $FIGURES_FOLDER/*.svg; do
    cairosvg $file -b white -o $OUTPUT_FOLDER/$(basename $file .svg).png
done
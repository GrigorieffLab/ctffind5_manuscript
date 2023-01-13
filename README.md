# CTFFIND5 provides improved insight into quality and geometry of cellular cryo-EM samples

## Johannes Elferich, Lingli Kong, Ximena Zotttig, Nikolaus Grigorieff

This repository contains the raw text, figures, and scripts used to generate a manuscript describing improvements 
to the CTFFIND program targeted at cryo-EM imaging of cellular samples.

## Get started

Clone this repository

```
git clone https://github.com/GrigorieffLab/ctffind5_manuscript.git ./
```

Make sure Git LFS is setup 

```
git lfs install
```

Setup the conda environment
```
conda env create -f build/environment.yml
```

Activate the environment:
```
source activate ctffind5_manuscript
```

Build the manuscript:

```
./build/build.sh
```

## Tools

The following tools are used for this purpose:

- [**pandoc**](https://pandoc.org/) to convert the markdown files into Word or PDF files
- [**manubot-cite-pandoc**](https://manubot.github.io/manubot/reference/manubot/pandoc/cite_filter/) to manage citations
- [**miniconda**](https://docs.conda.io/en/latest/miniconda.html) to maintain a virtual environment for the required tools
- [**inkscape**](https://inkscape.org/) to assemble panels into figures
- [**python**](https://python.org) and [**matplotlib**](https://matplotlib.org/) to generate plots
- [**tikz**](https://tikz.net/) to generate flowcharts
- [**git-lfs**](https://git-lfs.com/) to maintain image files

## Files and directories

- [**manuscript.md**](manuscript.md) the manuscript file
- [**output/**](output/) contains rendered figures and manuscript. The contents will not be indexed by git
- [**figures/**](figures/) contains the inkscape .svg files
- [**panels/scripts**](panels/scripts) contains python scripts that create plots
- [**panels/images**](panels/images) contains the image files resulting from the scripts


## TODO items

- Choose pixel size for fitting better
- Square FFT over whol;e image

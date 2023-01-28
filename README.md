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

- [**manuscript.md**](manuscript.md) the manuscript file.
- [**output/**](output/) contains the rendered manuscript. 
- [**figures/**](figures/) contains the inkscape .svg files and .png files created from them.
- [**panels/scripts**](panels/scripts) contains python scripts that create plots.
- [**panels/images**](panels/images) contains the image files resulting from the scripts. IMages could be placed directly in there, but the preference is to have them generated by code.
- [**scripts/**](scripts) contains scripts that do data processing, but do not directly result in a panel.


## TODO items

- [x] Choose pixel size for fitting better
- [ ] Find datasets for tomo vs thickness verification
- [ ] Fix OverlayCTF
- [ ] Just change FRC threshold?
- [ ] Find out why it fails for certain images atm
- [ ] Options for 
    - [ ] McMullan vs CTFFIND style model
    - [ ] Reduce weight of node area in fitting

## Dataset for tomo thickness verification

- Johanes_20210614/undiff_red1

## Figures

#### Figure 1: How does tilt estimation work?

#### Figure 2: How does thickness estimation work?

#### Figure 3: CTF correction of low magnification maps

#### Figure 4: Verification and error estimate of tilt 

#### Figure 5: Verification and error estimate of thickness 



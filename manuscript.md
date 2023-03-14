---
title: CTFFIND5 provides improved insight into quality and geometry of cellular cryo-EM samples
author:
- "Johannes Elferich"
- "Lingli Kong"
- "Ximena Zottig" 
- "Nikolaus Grigorieff"
---

## Abstract

Images taken by transmission electron microscopes (TEM) are distorted by the spherical aberration of the lens system and by the sample not being within the focal plane of the instrument, among other factors. These distortions can be modeled in reciprocal space using the contrast-transfer function (CTF). Accurate estimation and correction of the CTF has been one of the key aspects of the "resolution-revolution" in cryo-EM microscopy. While estimation of the CTF is mainly done to restore as much of the image as possible, many important sample characteristics are encoded in the CTF, such as sample thickness and sample tilt. These characteristics are of high interest for the microscopist, especially when imaging cellular samples. Currently, a substantial bottleneck for high-resolution cryo-EM of cellular samples is the preparation of samples with suitable thickness and the identification of areas within a given sample that are amenable for data collection. Real-time measurement of sample thickness and geometry, derived from accurate modeling of the CTF would therefore a tool towards minimizing this bottleneck. In this paper we describe the program CTFFIND5, the newest iteration of the commonly used software CTFFIND, which has been improved by implementing procedures for the before mentioned measurements. We describe how these procedures have been implemented and validate their accuracy using samples of eucaryotic cells thinned by cryo-focused ion beam (cryo-FIB) milling. We find that CTFFIND5 can estimate the tilt of the sample with an accuracy of X and the thickness of the sample with an accuracy of X nm. 

## Introduction

Transmission electron microscopy of biological spcimens at cryogenic
temperatures (cryo-EM) is a powerful tool to image biomolecules at high
resolution, both in solution and within the cell. Interpretation of cryo-EM
images depends on understanding the 

## Methods

### Tilt estimation algorithm

### Verification of tilt estimation using tilt-series

### Verification of tilt estimation using tilted samples of aquaporin crystals

### Sample thickness estimation algorithm

In CTFFIND5 we implemented a new $CTF_{t}$ model function, based on the $CTF$
function implemented in CTFFIND4 [@doi:10.1016/j.jsb.2015.08.008] adjusted by
the formula described by [@pmid:26103047]

$$
CTF_{t}(\lambda,\textbf{g},\Delta f,C_{s},\Delta\varphi, \omega_{2},t) = \frac{1}{2}(1-{\rm sinc}(\xi(\lambda,\textbf{g},t))\cos(2\chi(\lambda,|\textbf{g}|,\Delta f,C_{s},\Delta\varphi,\omega_{2})))
$$ {#eq:ctft}

where $\chi$ denotes the phase-shift as a function of the electron wavelength
$\lambda$, the spatial frequency vector $|\textbf{g}|$, the objective defocus
$\Delta f$, the spherical aberration $C_{s}$, the additional phase shift
$\Delta\varphi$, and the fraction of amplitude contrast $\omega_{2}$. The
modulation of the CTF due to sample thickness $t$ is described by the function
$\xi$:

$$
\xi(\lambda,\textbf{g},t) = \pi\lambda\textbf{g}^{2}t
$$ {#eq:xi}

If the user request sample thickness estimation, the program will first fit the
$CTF$ model function as implemented in CTFFIND 4 and the "goodness of fit"
resolution  will be used as an estimate of the location of the first node of the
$CTF_{t}$ function, with $t$ given by:

$$
t = /frac{1}{\lambda\textbf{g}^{2}}
$$ {#eq:t}

If the option "Brute-force 1D fit" is selected, CTFFIND5 will further refine $t$ and $\Delta f$ by calculating the normalized cross-correlation between the radial average of the powerspectrum (corrected for astigmatism, as described in ) and $CTF_t$, searching systematically for the best combination of $t$ in the range of 50-400 nm at 10 nm steps and $\Delta f$ in 10 nm steps from the previously fitted value +- 200 nm. 

Finally, if the option "2D-refinement" is selected CTFFIND5 will optimize $t$, $\Delta f_{1}$, $\Delta f_{2}$, and $\omega$ using teh conjugate gradient algorithm descibed in and the normalized cross correlation between $CTF_{t}$ and the 2D powespectrum as a scoring function.

After the optimal values for $t$ and $\Delta f$ have been obtained the "goodness of fit" crosscorrelation is recalculated using $CTF_{t}$, with the a frequency window that is 1.5 time larger, to avoid the drop-off in the node regions of $CTF_{t}$.


### Verification of sample thickness estimation using Lambert-Beers law

We used 1000 micrographs collected on one lamella of ER-HoxB8 cells (dataset Lamella$_EUC1$ from [@doi:]). For each micrograph we calculated $ln(\frac{I}{I_0})$, where $I$ was the sum of all pixels in the center quadrant of the micrograph and $I_0$ was the average of this sum for 45 micrographs collected over vacuum, with the same energy filter settings. We then used CTFFIND5 to estimate the thickness $t$ of each micrograph using the "Brute-force 1D fit" and "2D-refinement" setting. We used a "RANSAC" algorithm as implemented in [@doi] to fit a linear model to the relationship of $ln(\frac{I}{I_0})$ and $t$, while rejecting outliers. We then manually inspected every outlier of the model fit and categorized the reason for the discrepance into "wrong fitting", "ice contamination", "partial vacuum".

### Verification of sample thickness estimation using tomography

### CTF correction of medium magnification lamella images

The CTF of the representative mmm image was estimated using CTFFIND4 using the parameters: ...,...,.... We then used the program apply_ctf fo the cisTEM suite to flip the phases according to the ctf fit. We furthermore implemented the Wiener like filter described in [@doi:] in apply_ctf to produce the image shown in ... . The parameters for the Wiener like filter were chosen manually as ... to produce the subjectively most natural looking image.



## Results

### CTF estimation and correction assists biological interpretation of intermediate-magnification lamella images

### Tilt estimation by CTF

### Sample Thickness estimation by CTF

After correction for the incoherence of the CTF due to sample tilt we set out to
also account for the sample thickness. As evident in Figure [] there are
thon-ring like modulation in the powerspectrum at higher resolution than the
goodness of fit estimate. These modulations are as described by [] and []
phase-shifted to the normal CTF. [] suggested that the goodness of fit estimate
could be used as an estimation of the location of the first node and the sample
estimated according to equation []. We implemented this in CTFFIND5 and found
that indeed when we replaced the CTFFIND4 model function with the function
described by [] and used the goodness of fit estimate as the location of the
first node the resulting model CTF had a better agreement with the experimental
powerspectrum (Figure). We then implemented a procedure to refine the CTF
parameters together with the sample thickness and found that this procedure
improved the agreement between the model and experimental CTF even further, even
though the adjustemnt to the parameters was rather small. 

While using the goodness of fit resolution estimation was good enough for many
images, we also found that in images with defocus under 1 um and with a sample
wthickness over 200 nm the goodness CTFFIND would fit the CTF before and after
the first node using the old model function. FIgure [] shows an example of such
a case. The reader might appreciate that at lowe resolution (>7A) The
experimental peaks are at lower resolution than in the model CTF while at
resolution abover 7A the experimental peaks are at higher resolution than in the
model CTF. That th

### Verification using tomography

### Verification using Lamber-Beer laws on DeCo-LACE data

## Discussion

## Figures

![Tilt estimation (A) Variance score as a function of tilt axis orientation and sample tilt](figures/tilt_figure.png){#fig:tilt}

![CTF correction of medium magnification overviews](figures/mmm_figure.png){#fig:mmm}

![Validation of sample thickness estimation](figures/node_figure.png){#fig:node}

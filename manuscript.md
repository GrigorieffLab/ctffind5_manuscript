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
During the milling process and the sample loading to the microscope, the real orientation of the lamella sample can be slightly off the milling angles set by users and the direction of the TEM tilting axis. Thus, the quality of the CTF correction simply based on the microscope’s axis and tilt settings can be less satisfactory. Furthermore, this error can influence the tomography alignment. 
In ctffind5, we extended the implementation of the tilt estimate to cryo-EM lamella samples. On one hand, our algorithm enabled the direct measurements of the tilt angle and axis direction for a single tilt image. On the other hand, the real lamella orientation can be further calculated by combining the axis and tilt angles from ctffind5 and the microscope tilt settings. Considering that the results obtained by ctffind5 represent the real tilts of the sample, if we use a rotation matrix R0 to represent the real lamella loading orientation and a rotation matrix Rtem to represent the tilt and axis information of the microscope, the ctffind5 rotation matrix can be expressed as follows:  
Rctf = R0 X Rtem
where R0 is a fixed term. We encode the tilt angle and axis to a rotation matrix by embedding the tilt angle  and axis  to a ‘zxz’ rotation system in a sequence of ‘(,,-)’. 
By fitting the above equation to the ctffind5 result, the lamella loading orientation R0 can be obtained. 
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

We used 655  micrographs collected on one lamella of ER-HoxB8 cells (dataset
Lamella$_EUC1$ from [@doi:]). For each micrograph we calculated
$ln(\frac{I}{I_0})$, where $I$ was the sum of all pixels in the illuminated
area of the movie and $I_0$ was the average of this sum for 45 micrographs collected
over vacuum, with the same energy filter settings. This value should have a
linear relationship to the thickness of the sample, consistent with Lambert-Berrs
law [@doi:10.1016/j.jsb.2015.09.019;@doi:10.1016/j.jsb.2018.06.007]:

$$
ln(\frac{I}{I_0}) = \frac{1}{\kappa} t
$$ {#eq:lb}

where $\kappa$ is the apparent mean free path for inelastic scattering.

We then used CTFFIND5 to
estimate the thickness $t$ of each micrograph using the "Brute-force 1D fit" and
"2D-refinement" setting (Min. Resolution 30A, Max. Resolution 5A, Low Defocus
for search 500nm, High Defocus 5000nm, Min. Resolution for thickness estimate
10A, Max. Resolution for thickness estimate 3A). 
We used a "RANSAC" algorithm as implemented in [@doi]
to fit a linear model to the relationship of $ln(\frac{I}{I_0})$ and $t$, while
rejecting outliers. We then manually inspected every outlier of the model fit
and categorized the reason for the discrepance into "wrong fitting",
"contamination", "partially occluded beam", and "partially vacuum".

### Verification of sample thickness estimation using tomography

### CTF correction of medium magnification lamella images

The CTF of the representative mmm image was estimated using CTFFIND4 using the parameters: ...,...,.... We then used the program apply_ctf fo the cisTEM suite to flip the phases according to the ctf fit. We furthermore implemented the Wiener like filter described in [@doi:] in apply_ctf to produce the image shown in ... . The parameters for the Wiener like filter were chosen manually as ... to produce the subjectively most natural looking image.



## Results

### CTF estimation and correction assists biological interpretation of intermediate-magnification lamella images

### Tilt estimation by CTF
Fig 1. Presents the fitted result and the orientation measurement obtained by CTFFIND5. The sample in Fig 1(a) is milled by 20 and the TEM axis direction is 178.4.  The fitting result (𝜃, 𝜑) is (19.5, 171.9). If we remove the outliers based on the 3 sigma criteria, the fitting result can be updated to (20.5, 172.9). As we can see from the result, the fitted milling angle only has 0.5 difference. However, the axis direction has up to a 6 difference, which means that the loaded grid is not well aligned to the orientation of the tilting axis of the microscope. The sample in Fig1(b) is milled by 20 and the TEM axis direction is 176.3. The fitting result is (22.1, 172.6). By removing the outliers, the fitting result is (22.6, 174.31). Although CTFFIND5 has some noticeable errors at the lower tilt angles, the fitting result is still within a reasonable range. More examples are provided in the supplementary material. 

![Comparison o ctffind5 result and the crystal information](figures/Table.png){#fig:tilt}

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

We a dataset of 7 exposures collected on lamellae of ER-HoxB8 cells together
with tilt-series sollected afterwards in the same location to verify the
accuracy of the thickness estimate in CTFFIND5. We used CTFFIND5 to estimate $t$
for every exposures and compared it with the thickness estimated from tomograms
reconstructed from the tilt-series. We mesures the thickness in the tomograms by
manually estimating the distance between the surfaces of the lamella in X
different spots. 

For tomography reconstruction, tilt movie frames were aligned using SerialEM
plugin, then, tilt series were aligned using IMOD (version 4.11 ) software
package. For coarse alignment, a high-frequency cutoff radius of 0.15 was used.
The fiducial model was generated using patch tracking with patches of 450x450
and a fractional overlap of patches of 0.33x0.33. High-tilt frames were omitted
while generating the fiducial model. Robust fitting with a tuning factor of 1
was used for fine alignment. After computing the alignment, the fiducial model
was edited and re-computed. The edited models with the lowest residual error
mean and sd were used for fine alignment. Tomogram positioning was used to
correct the tilt angle offset. Full-aligned stacks were generated with a binning
of 2 or 4 (tomogram pixel size of 8.349). Tomograms were reconstructed using a
SIRT-like filtering option in IMOD and manually inspected. The tomograms were
back-projected along the Y axis using a homemade script, generating a small set
of XZ stacks. Thickness measurements on the projected central slides were
performed using tdisp (display tool included in cisTEM software package).

### Verification using Lamber-Beer laws on DeCo-LACE data

Cryo-EM is frequently performed using an energy filter to remove inelastically
scatteres electrons. The fraction of inelatically scattered electrons can be
described by the Lambert-Beer law, which states that the fraction of extingished
electrons is proportional to the thickness of the sample. The extinction
coefficent has been experimentally determined for common cryo-EM condistions
[@doi:]. To test whether thickness estimation in CTFFIND5 is consistent with
this methods we used a dataset of 655 exposures of a lamella of ER-HoxB8 cells
collected using the DeCo-LACE approach [@doi:]. We used CTFFIND5 to estimate the
thickness $t$ of every exposures and plotted $-ln(\frac{I}{I_0})$ against $t$.
Fitting the data to a linear model we found that that 568 out of 655 exposures
could be well explained by a linear relationship where $\kappa$ was 323 nm. This
value is consistent the value found by [@doi:10.1016/j.jsb.2018.06.007], even
though our dataset was collected without an objective aperture. The X-intercept 
of the linear model was -12.2 nm, meaning that the node position systemnatically
predicts a smaller thickness than the extintion of electrons. Possible
explanations are discussed below. The standard deviation of the residuals was
5.7 nm.

## Discussion

## Figures

![Tilt estimation (A) Variance score as a function of tilt axis orientation and sample tilt](figures/tilt_figure.png){#fig:tilt}

![CTF correction of medium magnification overviews](figures/mmm_figure.png){#fig:mmm}

![Validation of sample thickness estimation](figures/node_figure.png){#fig:node}

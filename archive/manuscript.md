---
title: CTFFIND5 provides improved insight into quality and geometry of cellular cryo-EM samples
author:
- "Johannes Elferich"
- "Lingli Kong"
- "Ximena Zottig" 
- "Nikolaus Grigorieff"
---

## Abstract

Images taken by transmission electron microscopes (TEM) are distorted by the
spherical aberration of the lens system and by the sample not being within the
focal plane of the instrument, among other factors. These distortions can be
modeled in reciprocal space using the contrast-transfer function (CTF). Accurate
estimation and correction of the CTF has been one of the key aspects of the
"resolution-revolution" in cryo-EM microscopy. While estimation of the CTF is
mainly done to restore as much of the image as possible, many important sample
characteristics are encoded in the CTF, such as sample thickness and sample
tilt. These characteristics are of high interest for the microscopist,
especially when imaging cellular samples. Currently, a substantial bottleneck
for high-resolution cryo-EM of cellular samples is the preparation of samples
with suitable thickness and the identification of areas within a given sample
that are amenable for data collection. Real-time measurement of sample thickness
and geometry, derived from accurate modeling of the CTF would therefore a tool
towards minimizing this bottleneck. In this paper we describe the program
CTFFIND5, the newest iteration of the commonly used software CTFFIND, which has
been improved by implementing procedures for the before mentioned measurements.
We describe how these procedures have been implemented and validate their
accuracy using samples of eucaryotic cells thinned by cryo-focused ion beam
(cryo-FIB) milling. We find that CTFFIND5 can estimate the tilt of the sample
with an accuracy of X and the thickness of the sample with an accuracy of X nm. 

## Introduction

Transmission electron microscopy of biological spcimens at cryogenic
temperatures (cryo-EM) is a powerful tool to image biomolecules at high
resolution, both in solution and within the cell. Interpretation of cryo-EM
images depends on understanding the image formation process of the TEM, which is
described by the CTF. The CTF is commonly modeled using an astigmatic defocus,
the spherical aberration, and if appropriate a phase shift introduced by a phase
plate as parameters. 

## Methods

### Tilt estimation algorithm

### Verification of tilt estimation using tilted samples of aquaporin crystals

We used aquaporin 2D crystal samples [@doi:org/10.1038/35036519] to verify the
reliability of the tilt and axis angle estimation of CTFFIND5, the real angle
and axis direction of which are regarded to be accurately given. Since the
default CTF estimation setting in cisTEM disabled the tilt search, select yes
for tilt search under expert options to conduct the tilt estimation operation.
The other initial parameters are kept the same as the default cisTEM settings,
i.e., defocus search ranges from 5000 $\Angstrom$ to 50000 $\Angstrom$ with step
of 100 $\Angstrom$, resolution fitting ranges from 30 $\Angstrom$ to 5
$\Angstrom$, and the box size is 512 pixels. 

### Verification of tilt estimation using tilt-series
When the lamella sample is loaded to the microscope, the real orientation of the
lamella sample can be slightly off from the direction of the TEM tilting axis
and the milling angles set by users. This error can influence the tomography
alignment. The quality of the CTF correction simply based on the microscope’s
axis and tilt settings can also be less satisfactory. In CTFFIND5, we extended
the implementation of the tilt estimation to cryo-EM lamella samples. Since our
algorithm enabled the direct measurements of the tilt angle and axis direction
for each tilt image, the lamella initial loading orientation, i.e., the
orientation of the lamella when it is loaded to the microscope before tilting,
can be calculated by combining the axis and tilt angles from CTFFIND5 and the
microscope tilt settings. If we use a rotation matrix $R_{0}$ to represent the
real lamella initial loading orientation and a rotation matrix $R_{tem}$ to
represent the tilt and axis information of the microscope, the rotation matrix
of the sample’s real orientation can be expressed as follows:  
$$
R = R_{0} \times R_{tem}
$${#eq:t}
where $R_0$ is a fixed term. The tilt and axis angles are encoded to a rotation
matrix $R$ by embedding the tilt angle $\theta$ and axis direction $\phi$ to a
‘zxz’ rotation system in a sequence of ‘($\phi$, $\theta$, $-\phi$)’. In
CTFFIND5, both the axis direction and the tilt angle are clockwise angles. The
axis direction is the angle formed between the tilt axis and x-axis. They can be
converted to the angle system of the microscope ($\theta_{tem}$, $\phi_{tem}$)
by: 
$$
\begin{aligned}
\phi_{tem} &=270^{\circ} - \phi_{ctffind5} \\
\theta_{tem} &=-\theta_{ctffind5}
\end{aligned}
$$ {#eq:t}

Considering that the results obtained by CTFFIND5 represent the real orientation
of the sample, by fitting equation (1) to the CTFFIND5 result $R_{ctf}$, the
lamella loading orientation $R_{0}$ can be obtained. Furthermore, since the
sample is a plane, we can use the normal vector of the lamella to represent the
orientation. Thus, the overall effect of tilt angle or axis direction can be
considered simultaneously. By calculating the normal vector difference between
the fitted initial orientation and the one calculated directly by $R_{ctf}
\times R_{tem}^{-1}$ at each tilt, the root mean squared error (RMSE) can be
obtained to find the outliers to further improve the fitting result. To generate
better defocus and tilt estimation, the defocus search range and resolution
fitting range should be adjusted according to the dataset. For our cryo-EM
samples, the resolution fitting range is from 50 $\Angstrom$ to 10 $\Angstrom$
and the defocus search range is $\pm$ 10000 to 20000 $\Angstrom$ from the data
collection defocus.



### Sample thickness estimation algorithm

In CTFFIND5 we implemented a new $CTF_{t}$ model function, based on the $CTF$
function implemented in CTFFIND4 [@doi:10.1016/j.jsb.2015.08.008] adjusted by
the formula described by [@pmid:26103047]

$$
CTF_{t}(\lambda,\textbf{g},\Delta f,C_{s},\Delta\varphi, \omega_{2},t) = \frac{1}{2}(1-{\mathrm{sinc}}(\xi(\lambda,\textbf{g},t))\cos(2\chi(\lambda,|\textbf{g}|,\Delta f,C_{s},\Delta\varphi,\omega_{2})))
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

If the option "Brute-force 1D fit" is selected, CTFFIND5 will further refine $t$
and $\Delta f$ by calculating the normalized cross-correlation between the
radial average of the powerspectrum (corrected for astigmatism, as described in
) and $CTF_t$, searching systematically for the best combination of $t$ in the
range of 50-400 nm at 10 nm steps and $\Delta f$ in 10 nm steps from the
previously fitted value +- 200 nm. 

Finally, if the option "2D-refinement" is selected CTFFIND5 will optimize $t$,
$\Delta f_{1}$, $\Delta f_{2}$, and $\omega$ using teh conjugate gradient
algorithm descibed in and the normalized cross correlation between $CTF_{t}$ and
the 2D powespectrum as a scoring function.

After the optimal values for $t$ and $\Delta f$ have been obtained the "goodness
of fit" crosscorrelation is recalculated using $CTF_{t}$, with the a frequency
window that is 1.5 time larger, to avoid the drop-off in the node regions of
$CTF_{t}$.


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

The CTF of the representative mmm image was estimated using CTFFIND4 using the
parameters: ...,...,.... We then used the program apply_ctf fo the cisTEM suite
to flip the phases according to the ctf fit. We furthermore implemented the
Wiener like filter described in [@doi:] in apply_ctf to produce the image shown
in ... . The parameters for the Wiener like filter were chosen manually as ...
to produce the subjectively most natural looking image.



## Results


### Tilt estimation by CTF

\begin{table}[]
\centering
\caption{Comparison of CTFFIND5 Result and the Crystal Information}\label{tbl:tiltcrystal}
\ra{1.3}
\begin{tabular}{@{}rcrrrcrrr@{}}
\toprule
Image  & \phantom{abc} &\multicolumn{3}{c}{Tilt axis $\phi$}    & \phantom{abc}                              & \multicolumn{3}{c}{Tilt angle $\theta$}                                    \\ \cmidrule{3-5}  \cmidrule{7-9}
       && crys  & ctffind5 & $\Delta\phi$   && crys   & ctffind5 & $\Delta\theta$     \\ \midrule
530394 && 93.28  & 94.98    & -1.7  && 19.6   & 20.69    & -1.09   \\ 
530419 && 109.78 & 106.51   & 3.27  && 18.66  & 16.04    & 2.62    \\ 
530430 && 104.38 & 101.13   & 3.25  && -21.32 & 20.37    & -41.69  \\ 
530444 && 98.39  & 97.62    & 0.77  && 20.72  & 20.88    & -0.16   \\ 
660027 && 99.68  & 102.34   & -2.66 && 19.4   & 22.39    & -2.99   \\ 
540149 && 94.45  & 85.84    & 8.61  && 43.08  & 44.59    & -1.51   \\ 
540291 && 96.16  & 98.1     & -1.94 && 45.11  & 40.68    & 4.43    \\ 
540302 && 93.98  & 93.39    & 0.59  && 44.7   & 44.21    & 0.49    \\ 
540313 && 95.34  & 95.13    & 0.21  && 44.03  & 46.49    & -2.46   \\ 
660183 && 97.69  & 97.27    & 0.42  && 48.13  & 48.99    & -0.86   \\ 
550069 && 90.08  & 92.55    & -2.47 && 60.46  & 60.83    & -0.37   \\ 
550089 && 91.48  & 92.04    & -0.56 && 60.5   & 60.72    & -0.22   \\ 
660291 && 93.23  & 92.19    & 1.04  && -57.59 & 59.19    & -116.78 \\ 
660421 && 89.32 & 89.06    & 0.26  && 61.36  & 60.01    & 1.35    \\ 
680341 && 89.67 & 90.02    & -0.35 && 58.68  & 59.62    & -0.94   \\ 
530345 && N/A    & 108.6    &       && 0      & 0.84     & -0.84   \\ 
530356 && N/A    & 231.17   &       && 0      & 1.93     & -1.93   \\ 
530358 && N/A    & 56.58    &       && 0      & 1.29     & -1.29   \\ 
530375 && N/A    & 3.21     &       && 0      & 0.79     & -0.79   \\ 
530378 && N/A   & 67.6     &       && 0      & 2.17     & -2.17   \\ 
\bottomrule
\end{tabular}
\end{table}

To verify that CTFFIND5 can reliably estimate the tilt of the sample, we used a
dataset of tilted aquaporin crystals, that was use to benchmark the original
CTFTILT implementation. Table [@tbl:tiltcrystal] compares the tilt information
of the samples obtained from crystallographic analysis and the estimation
results of CTFFIND5. As shown in Table [@tbl:tiltcrystal], the results of CTFFIND5 agree well
with the aquaporin crystals information. For crystals with 0$^{\circ}$ tilt,
CTFFIND5 still gives an angle estimation. This is because CTFFIND5 estimates the
tilt based on the defocus difference among the tiles and the sample cannot be
perfectly flat to have the same defocus throughout the image. Therefore,
CTFFIND5 estimation results tend to reflect the angle and axis of the uneven
sample surface in this case. 

Fig 1. Presents the fitted result and the orientation measurement obtained by
CTFFIND5. The sample in Fig 1(a) is milled by 20$^{\circ}$ and the TEM axis
direction is 178.4$^{\circ}$.  The fitting result $(\theta, \phi)$ is
(19.5$^{\circ}$, 171.9$^{\circ}$). If we remove the outliers, the fitting result
can be updated to (20.6$^{\circ}$, 172.9$^{\circ}$). As we can see from the
result, the fitted milling angle only has 0.6$^{\circ}$ difference. However, the
axis direction has up to a 6$^{\circ}$ difference, which means that the loaded
grid is not well aligned with the orientation of the tilting axis of the
microscope. The sample in Fig1(b) is milled by 20$^{\circ}$ and the TEM axis
direction is 176.3$^{\circ}$. The fitting result is (-22.1$^{\circ}$,
187.41$^{\circ}$). By removing the outliers, the fitting result is
(-22.9$^{\circ}$, 185.3$^{\circ}$). Although CTFFIND5 has some noticeable errors
at the lower tilt angles, the fitting result is still within a reasonable range.
The value of tilt angles are all adjusted to be negative values for a better
display of the fitted curve. When a tilt angle is converted to a positive value,
the corresponding axis direction should be adjusted by 180$^{\circ}$. More
examples are provided in the supplementary material. 


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

### CTF estimation and correction assists biological interpretation of intermediate-magnification lamella images

During data collection of Cryo-EM data in cells, the operator frequently relies
on images taken at a low magnification to select areas of interest and establish
biological context of taken micrographs. These images are usually taken at
pixelsize of approximately 40 angstroms and a defocus of around 200 um. This
produces strong contrast of biological membranes, but can sometimes lead to
substantial fringes of biological membranes [@fig:mmm]A. In order to correct for
these we found that CTFFind produces accurate CTF estimation of such overview
images [@fig:mmm]B. In order to correct for these the program apply_ctf of the
cisTEM suite can be used to flip the phases of the resolution ranges with
negative contrast [@fig:mmm]C. However, we found that using the wiener filter
based phase correction describe by Tegunov et.al. produces a natrually looking
image that might be best suited to judge the biological context [@fig:mmm]D. The
estimation of the CTF as well as the phase correction can be perfomed within a
few seconds [TODO: actual measure runtime], making it feasible to usew this
approach during data collection.

## Discussion

## Figures

![Tilt estimation and correction in CTFFIND5 (a) Powespectra are calculated in
128x128 pixel patches as indicated on this representative micrographs. Each dots
represents the location of a patch and a box indicates the size of a patch. (b)
A model of the expected powerspectrum in each patch given an average defocus
$\Delta f$, tilt angle $\theta$, and axis direction $\phi$ is compared to the
actual powerspectra of tiles. After an optimal set of $\theta$ and $\phi$ has
been found a corrected powerspectrum is calculated by summing the tile
powerspectra after scaling them to correct for the defocus difference. (c)
Comparison of the original powespectrum (solid line, blue) to the tilt-corrected
powerspectrum (solid line, black). The tilt-corrected powerspectrum exhibits
clear peaks at higher spatial resolution than the overall powespectrum as
evident by the "goodness-of-fit" scores (dashed lines). The estimated CTF
parameters are $\Delta f_{1}=10603\text{\AA},\Delta f_{2}=10193\text{\AA},\alpha
=85.9°$ for the overall powerspectrum and $\Delta f_{1}=10492\text{\AA},\Delta
f_{2}=10342\text{\AA},\alpha =81.2°,\theta =12.3°,\phi=261.6°$ for the tilt
corrected powerspectrum. The fit resolution is 5.9Å for the overall
powerspectrum (dashed line, blue) and 4.6Å for the tilt-corrected spectrum
(dashed line, black).](figures/tilt_figure.png){#fig:tilt width=50%}

![Validation of tilt estimation using tilt-series data. (a) Estimated tilt angle
and tilt axis direction of 40 micrographs of a tilt-series taken on a FIB-milled
biological specimen. For each image the tilt angle (dot, upper plot) and tilt
axis direction (cross, middle plot) are plotted as a function of the nominal
stage angle. The data has been fitted to a model of the specimen tilt before
tilting the stage. The estimated tilt-angle is -20.6° and axis direction is
172.1°, which is consistent with the FIB-milling angle of 20° and manual
alignment of the milling direction to the tilt-axis at 178.4°. In the lower plot
the absolute fit residuals for tilt angle and axis direction are plotted.
Residuals for tilt-axis direction in images where the tilt-angle was lower than
10 degrees have been omitted, since the tilt axis direction is poorly defined in
these cases. (b) Estimated tilt angle and tilt axis direction of 30 micrographs
of a tilt-series taken on a FIB-milled biological specimen. For each image the
tilt angle (dot, upper plot) and tilt axis direction (cross, middle plot) are
plotted as a function of the nominal stage angle. The data has been fitted to a
model of the specimen tilt before tilting the stage. The estimated tilt-angle is
22.9° and axis direction is 185.08°, which is consistent with the FIB-milling
angle of 20° and manual alignment of the milling direction to the tilt-axis at
178.4°. In the lower plot the absolute fit residuals for tilt angle and axis
direction are plotted. Residuals for tilt-axis direction in images where the
tilt-angle was lower than 10 degrees have been omitted, since the tilt axis
direction is poorly defined in these
cases.](figures/TiltFitting.png){#fig:tilt_fitting width=50%}

![Sample thickness estimation by fitting CTF modulation. (a) Comparison of the
CTF model used sample thickness estimation in CTFFIND4 and after applying the
modulation function (right) described by McMullan et.al. (b) Representative
example of CTF fitting in a lamella without (top) and with (bottom) thickness
estimation. The tilt of the specimen was estimated to be $12.3°$. When fitting
without thickness estimation the estimated parameters were $\Delta
f_{1}=10492\text{\AA},\Delta f_{2}=10342\text{\AA},\alpha =81.2°$. When taking
smaple thickness into account the estimated parameters were $\Delta
f_{1}=10481\text{\AA},\Delta f_{2}=10286\text{\AA},\alpha =69.6°,
t=969\text{\AA}$. The estimated fit resolution was $4.6\text{\AA}$ and
$3.4\text{\AA}$ without and with sample estimation, respectively. (c)
Representative example of CTF fitting in a lamella without (top) and with
(bottom) thickness estimation. The tilt of the specimen was estimated to be
$6.7°$. When fitting without thickness estimation the estimated parameters were
$\Delta f_{1}=8002\text{\AA},\Delta f_{2}=7717\text{\AA},\alpha =73.4°$. When
taking smaple thickness into account the estimated parameters were $\Delta
f_{1}=8549\text{\AA},\Delta f_{2}=8343\text{\AA},\alpha =63.3°,
t=2017\text{\AA}$. The estimated fit resolution was $4.3\text{\AA}$ and
$4.2\text{\AA}$ without and with sample estimation, respectively.
](figures/node_figure.png){#fig:node width=50%}

![Validation of sample thickness
estimation](figures/node_validation_figure.png){#fig:nodevalidationthickness width=50%}

![Validation of sample thickness estimation by
tomography](figures/node_validation_figure_tomo.png){#fig:nodevalidationtomo width=50%}


![CTF correction of medium magnification
overviews](figures/mmm_figure.png){#fig:mmm width=50%}



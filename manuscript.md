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

## Methods

### Tilt estimation by CTF

### Sample Thickness estimation by CTF

## Results

### CTF estimation and correction assists biological interpretation of intermediate-magnification lamella images

### Tilt estimation by CTF

### Sample Thickness estimation by CTF

### Verification using tomography

### Verification using Lamber-Beer laws on DeCo-LACE data

## Discussion

## Figures

![Tilt estimation (A) Variance score as a function of tilt axis orientation and sample tilt](figures/tilt_figure.png)

![CTF correction of medium magnification overviews](figures/mmm_figure.png)

![Validation of sample thickness estimation](figures/node_figure.png)
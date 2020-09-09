# Capstone Project: MbientLab Real-time Step Counter

## Introduction

> **Here I present a novel real-time step counting algorithm for the [Mbientlab MMR inertial measurement unit](https://mbientlab.com/metamotionr/).**
> The algorithm uses fourier transformed accelerometer signal for frequency-based walk detection, similar to the protocol found in [Kang 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5796454/).
> It also relies on SPRING dynamic time warping, as per [Sakurai et al 2007](https://www.dm.sanken.osaka-u.ac.jp/~yasushi/publications/spring-slides.pdf), to count steps.

## Repository Summary

|File|Description|
|---|---|
|walking_data|Repository of walking accelerometer data from [Harle, R., & Brajdic, A. (2017)](https://www.repository.cam.ac.uk/handle/1810/266947) |
|[DTW_graph.ipynb](DTW_graph.ipynb)|Script to generate dynamic time warping visualizations for presentation|
|[DTW_testing.ipynb](DTW_testing.ipynb)|Testing DTW spring algorithm accuray on walking data|
|[WD_testing_and_EDA.ipynb](WD_testing_and_EDA.ipynb)|Testing frequency-based walk detection accuracy on walking data|
|[bluetooth_setup_notes.md](bluetooth_setup_notes.md)|Notes on setting up a bluetooth connection with your MMR through a Linux Virtual machine running on top of OSX|
|[capstone_presentation](capstone_presentation)|Presentation slide deck|
|[final_script.py](final_script.py)|Final real-time step counting script|
|[generate_step_template.ipynb](generate_step_template.ipynb)|Script to create average step template from walking data|
|[parseTraces.py](parseTraces.py)|Script to parse walking data|
|[step_template.csv](step_template.csv)|average normalized accelerometer and gyroscope time-series for a single step|

## Algorithm

![](algo_pic.png =250x)


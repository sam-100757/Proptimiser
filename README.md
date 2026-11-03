# Proptimiser
**tl;dr:** A python based propeller calculator (optimising tool: work in progress).

## Introduction
Proptimiser is an ongoing computational project aimed at developing a framework for rotor aerodynamic analysis, performance estimation, and, (hopefully soon) optimisation.

The project focuses on implementing established rotorcraft aerodynamic theories into a modular computational tool, with due importance to understanding the underlying physical models, and their engineering applications.

## 1. Current Capabilities

The framework currently incorporates the following modules:

### Atmospheric Modelling
* Implementation of the International Standard Atmosphere (ISA) model.
* Estimation of atmospheric properties such as temperature, pressure, density, and speed of sound at altitudes upto 80km.

### Momentum Theory
* Implementation of basic rotor momentum theory.
* Calculation of:
        - induced velocity
        - ideal induced power
        - wake velocity
        - cT
        - actual Power (if FOM given)
* The idea is, based on whatever the parameters have been given by the user to the programme, the programme can calculate whatever is possible for it to calculate using Momentum Theory.

### Blade Element Theory (BET)
* Spanwise calculations via integration for the rotor blade.
* Modelling of blade geometry and pitch distribution.
* Numerical integration of sectional forces to obtain rotor thrust and torque coefficients.
* Attempts to take into account empirical corrections due to real life factors such as tip loss estimation and torque due to rotation of wake.
-> Performance Analysis
The framework currently evaluates below parameters (BEMT based on Prouty):
* Thrust coefficient and Thrust
* Torque coefficient
* Power coefficient and Power
* Induced velocity
* Disk loading
* Figure of Merit (FoM)

-> -> Limitations
* BEMT model works only for NACA 0012 propellers as of now. The empirical corrections have been taken from whirl tower tests for those propellers as per reference.
* Limited accuracy
* Only functional for Hover. Climb/Descent and fwd flight yet to be added.

## Theoretical Foundation

The current implementation is based on classical rotorcraft aerodynamic formulations, with particular reference to:

* *Helicopter Performance, Stability, and Control* — Raymond W. Prouty.
* https://ntrs.nasa.gov/api/citations/19930085275/downloads/19930085275.pdf

-> Development and Validation: All implemented (finished) models are validated by some existing examples under the validation segment. Most of the examples have been taken from the Appendix A/B of the reference itself.

## 4. Technology Stack

* **Language:** Python
* **Numerical Computing:** NumPy
* **Data Handling:** Pandas
* **Visualisation:** Matplotlib

## 5. Project Status & Exciting New Prospects

<em>Work in Progress</em>

Proptimiser is under active development. The current focus is on improving the aerodynamic model, validating its outputs, and expanding its capabilities.

Potential future developments include:
* More comprehensive Blade Element Momentum Theory (BEMT) implementation.
* Integration of airfoil aerodynamic data (support for different airfoils)
* Support for applying different types of taper and twist along the blade (in a singular blade).
* Design optimisation based on user given criteria and priorities.
* Extended analysis of rotor operating conditions.

## 6. Repository Structure

The repository is being organised into modular components to the code and the validation files.

-> File Descriptions:-

# Environment 
* isa.py: Implements the International Standard Atmosphere (ISA) model for estimating atmospheric properties.
bemt_custom.py

# Momentum Theory
* mt.py: Implements fundamental rotor momentum theory for estimating induced velocity and ideal rotor performance parameters.

* ex1_AS350BatMtEverest.py: Validation exercise comparing momentum theory predictions for an AS350B rotor operating at the apex of Mount Everest.

* ex1_AppendixAHeli.py: Validation exercise reproducing momentum theory based rotor performance calculations for the helicopter described in Prouty's Appendix A.

# BEMT stuff

* Experimental implementation of a custom Blade Element Momentum Theory (BEMT) model: currently under development.

* bemt_prouty.py: Implements blade-element-based rotor performance calculations following the methodology presented in Prouty.

* ex2_proutyexampleheliAppendixB.py: Reproduces a helicopter performance example from Appendix B of Prouty for comparison with reference calculations.

* booksRadialDistrGraph.jpeg: Reference radial distribution plots extracted from the literature for comparison.

* generatedGraphoverlayWithBook.jpeg: Overlay of computationally generated radial distribution plots with published reference graphs for visual validation.

# docs

* glossary.txt: Glossary of terminology.

* README.md: hey, this is where you are right now.

## 7. Acknowledgements

Thanks to Dr Omkar Halbe for his guidance and advice on the subject.
Thanks to JustMe1236499 for the brainstorming sessions and CSE advice.

---

thanks for reading! cheers and celebrations.
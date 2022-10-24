Using SyFoS
===========

After starting SyFoS a GUI is provided as shown in figure 1. In the GUI’s upper third all parameters needed for creating synthetic force spectroscopy data are listed, grouped in three vertical sections, **Probe**, **Sample**, **Force spectroscopy Experiment** and **Artefacts**. 

All parameters can be altered and adjusted independently by the user. However, since parameters have between them a range of magnitude from 10-21 to 109 it is not advisable to start with completely arbitrary values in order to get meaningful results. For a quick start literature values for materials, which are commonly used in force spectroscopy experiments can be chosen from a dropdown menu. Parameters concerned with the experimental set-up start with a recommended value but can be adjusted as the user sees fit. 

The definition and recommended range of all values and parameters are given in :ref:`input parameters and values`.

With a complete set of values SyFoS can be executed with **Create Force Volume** in the GUI’s control section. Creation of the synthetic force spectroscopy data involves several steps (see 2.2), as calculating auxiliary parameters (2.2.1, 2.2.2 and 2.2.3), creating an ideal data set (!!) and simulating a force volume (!!), which is group of data sets. 

Upon successful execution auxiliary parameters and synthetic data are shown in the GUI’s presentation field. Synthetic force spectroscopy data is plotted as force curves, i. e. deflection δ as a function of the piezo displacement Z, mirroring real force spectroscopy results as those two data sets would be the raw data acquired in such measurements. Two types of curves are plotted: one ideal synthetic curve and a group of curves (number equals the number of curves given in the input mask, see also 2.1.9 ) which have additional artefacts, being shifted out of the origin (see 2.1.10, 2.1.11) and have noise (see 2.1.12). These artefacts reflect inaccuracies which cannot be avoided during real force volumes and therefore are also present in test data, for which SyFoS is primarily used. 

Additional sets of synthetic data can now be added for comparison. If for example the influence of the probes spring constant :math:`k_c` (2.1.1) is of interest this parameter can be changed and SyFos again executed by Create Force Volume. The according auxiliar parameters are shown and curves are now plotted on top of the first force volume. 

Choosing the according buttons, the plot area can be adjusted by zooming and panning. Adjustments to the plot area can be undone by, reset or back and redone by forward. 

By using the options in the GUI’s control penal, one can navigate through a stack of synthetic data: choosing the active force volume, deleting, and exporting data sets. 


.. _input parameters and values:

Input parameters and values
---------------------------

Definition and physical meaningful range of all values are given below.


.. _creating synthetic force spectroscopy data:

Creating synthetic force spectroscopy data
------------------------------------------

Creation of the synthetic force spectroscopy data involves several steps, which are listed and explained below. Starting with calculating auxiliary parameters reduced modulus Etot (2.2.1), jump to contact JTC (2.2.2) and combined Hamaker constant Atot (2.2.3) all needed parameters are available. 


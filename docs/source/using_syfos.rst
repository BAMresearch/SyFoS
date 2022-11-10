After starting SyFoS a GUI is provided as shown in figure 1. In the GUI’s upper third all parameters needed for creating synthetic force spectroscopy data are listed, grouped in four vertical sections, **Probe**, **Sample**, **Force Spectroscopy Experiment** and **Artefacts**. 

+--------------------------------------+--------------------------------------+-------------------------------------------------+------------------------------------+
| Probe                                | Sample                               | Force Spectroscopy Experiment                   | Artefacts                          |
+-----------------+--------------+-----+--------------------+------------+----+----------------------------+----------------+---+--------------------+-----------+---+
| :math:`E_{tip}` | 1e6 - 300e9  | Pa  | :math:`E_{sample}` | 1e6 - 300e9| Pa | Start Distance :math:`Z_0` | -10e-6 - 0     | m | Virtual Deflection | 0 – 3e-6  | m |
+-----------------+--------------+-----+--------------------+------------+----+----------------------------+----------------+---+--------------------+-----------+---+
| :math:`ν_{tip}` | 0 - 0.5      |     | :math:`ν_{sample}` | 0 - 0.5    |    | Step Size :math:`dZ`       | 0.01e-9 - 1e-9 | m | Topography Offset  | 0 - 10e-6 | m |
+-----------------+--------------+-----+--------------------+------------+----+----------------------------+----------------+---+--------------------+-----------+---+
| :math:`A_{tip}` | 1 - 450      | zJ  | :math:`A_{sample}` | 1 - 450    | zJ | Maximum :math:`Z_{max}`    | 0 - 1e-6       | m | Noise              | 0 - 1e-9  |   |
+-----------------+--------------+-----+--------------------+------------+----+----------------------------+----------------+---+--------------------+-----------+---+
| :math:`k_c`     | 0.001 - 100  | N/m |                    |            |    |                            |                |   |                    |           |   |
+-----------------+--------------+-----+--------------------+------------+----+----------------------------+----------------+---+--------------------+-----------+---+
| :math:`R`       | 1e-9 - 10e-6 | m   |                    |            |    |                            |                |   |                    |           |   |
+-----------------+--------------+-----+--------------------+------------+----+----------------------------+----------------+---+--------------------+-----------+---+

All parameters can be altered and adjusted within their value range. For a quick start literature values for materials, which are commonly used in force spectroscopy experiments can be chosen from a dropdown menu. Parameters concerned with the experimental set-up start with a recommended value but can be adjusted as the user sees fit. 

The definition and recommended range of all values and parameters are given in :ref:`material parameters`.

With a complete set of values SyFoS can be executed with :guilabel:`Create Force Volume` in the GUI’s control section. Creation of the synthetic force spectroscopy data involves several steps (see 2.2), as calculating auxiliary parameters (2.2.1, 2.2.2 and 2.2.3), creating an ideal data set (!!) and simulating a force volume (!!), which is group of data sets. 

Upon successful execution auxiliary parameters and synthetic data are shown in the GUI’s presentation field. Synthetic force spectroscopy data is plotted as force curves, i. e. deflection δ as a function of the piezo displacement Z, mirroring real force spectroscopy results as those two data sets would be the raw data acquired in such measurements. Two types of curves are plotted: one ideal synthetic curve and a group of curves (number equals the number of curves given in the input mask, see also 2.1.9 ) which have additional artefacts, being shifted out of the origin (see 2.1.10, 2.1.11) and have noise (see 2.1.12). These artefacts reflect inaccuracies which cannot be avoided during real force volumes and therefore are also present in test data, for which SyFoS is primarily used. 

Additional sets of synthetic data can now be added for comparison. If for example the influence of the probes spring constant :math:`k_c` (2.1.1) is of interest this parameter can be changed and SyFos again executed by Create Force Volume. The according auxiliar parameters are shown and curves are now plotted on top of the first force volume. 

Choosing the according buttons, the plot area can be adjusted by zooming and panning. Adjustments to the plot area can be undone by, reset or back and redone by forward. 

By using the options in the GUI’s control penal, one can navigate through a stack of synthetic data: choosing the active force volume, deleting, and exporting data sets. 

Parameter selection
===================

Text

Create a synthetic force volume
===============================

Text

Data presentation
=================

Text

Export Data
===========

Text
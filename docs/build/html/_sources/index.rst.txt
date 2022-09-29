About SyFoS
===========

With SyFoS (**Sy**\nthetic **Fo**\rce **S**\pectroscopy) data can be created. Force spectroscopy data is usually acquired experimentally by atomic force microscopy (AFM) and has its challenges when an automated analysis of the data is attempted, f. e. with SOFA (**SO**\ftware for **F**\orce **A**\nalysis). For one it is unique to this spectroscopic data, that the shift of the abscissa is not inherently known from the measurement. An additional challenge is, that the spectrum is not monotonous. The change of regimes of attractive and repulsive forces results in a singularity JTC (jump to contact). Data in the attractive respectively repulsive regime can be described by general theories, such as van der Waals attraction and Hertz contact, but one single expression which describes the full spectroscopic range does not exist. 

With SOFA we develop a software aiming for a robust algorithm which will be able to handle all varieties of force spectroscopy data. In order to test this capability reliable synthetic test data is required for which SyFoS was written. SyFoS mirrors the experimental acquisition of data and successively builds force spectroscopy data, taking material parameter and experimental parameter into account. All parameters can be specified by the user via a GUI (Figure 1). To achieve realistic challenges in the test data sets a noise level and data offsets are added. The software is stored in Git Hub, and published in $doi 

Using SyFoS
===========
.. toctree::
   :maxdepth: 1

   Using SyFoS <using_syfos>

Reference
=========
.. toctree::
   :maxdepth: 1

   Reference <reference>

Glossary
========
.. toctree::
   :maxdepth: 1

   Glossary <glossary>
==========
Parameters
==========

.. _material parameters:

Material parameters 
===================

Definition and physical meaningful range of all material parameters. 

.. _spring constant:

Probe's spring constant :math:`k_c`
-------------------------------------

The AFM probe’s cantilever spring constant :math:`k_c` describes the force :math:`F` needed to bend the cantilever by a deflection :math:`δ`. Since this is considered an elastic deflection, it is described by Hooke’s law :eq:`hookes law`. Commercially available AFM Probes have an :math:`k_c` range of 0.01 - 100 N/m. 

.. _radius:

Probe's tip radius :math:`R`
----------------------------

The AFM probe’s tip radius :math:`R` describes the curvature at the very end of the tip. In cases of a sharp tip (:math:`R` << 100nm) the tip has a height of up to 20µm and is rather a paraboloid or a pyramid. However, for the mechanical contact :eq:`hertz contact` only the tip’s shape at the very end is of consequence. For the calculation of attractive forces this radius is usually underestimated which is accepted in SyFoS for the time being. Das et al. suggested the use of an effective radius :math:`R_{eff}` >> :math:`R` which represents the influence of the tip size more realistically in respect to the attractive forces, which might be an option in the future for SyFoS. In the case of colloidal probes (100nm < :math:`R` < 20µm) the whole tip is of spherical shape and :math:`R` represents the radius for both cases, attractive and repulsive forces, correctly. 

.. _modulus:

Modulus :math:`E`
-----------------

The Young’s modulus :math:`E` is a characteristic property of every material, which describes the elastic responds to applied Force :math:`F`. Since the mechanical contact of an AFM measurement involves two different materials, the Young’s modulus of the tip material :math:`E_{tip}` and the Young’s modulus of the sample’s material :math:`E_{sample}` are required parameters. 

.. _poisson ratio:

Poisson ratio :math:`ν`
-----------------------

The Poisson ratio :math:`ν` describes the deformation perpendicular to the direction of applied force :math:`F`. It is the negative ratio of :math:`ν=-\frac{e_\perp}{e_\parallel}`, with :math:`e_\perp` being the relative change of dimension perpendicular to the applied force :math:`F` and :math:`e_\parallel` being the relative change of dimension in direction of applied force :math:`F`. Poisson ratios of common materials are expected to be between 0 and 0.5, which are accepted values in SyFoS. There is a class of materials which exhibits negative Poisson ratios (basically getting thicker when stretched), but those are not considered in SyFoS. 

.. _hamaker:

Hamaker constant :math:`A`
--------------------------

Van der Waals described the force needed to bring single neutral molecules from infinte to finite separation, now well known as van der Waals force :math:`F_{vdW}`. Hamaker transferred this concept to bulk materials by using pairwise summation approximation. This way the interactions and attractive forces of bodies can be described for different geometries, such as sphere/plane as appropriate for AFM measurements (tip/sample), by means of the Hamaker constant, which ranges from 1 to 450 zJ. 

.. _parameters experiment:

Force spectroscopy experimental set-up
======================================

For creating synthetic force spectroscopy data parameters which concern the experimental acquisition of data need to be defined. 

.. _start distance:

Start Distance :math:`Z_0`
----------------------------

The start distance :math:`Z_0` is the initial distance between the AFM probe and the sample surface. It also defines the beginning of the Z-scale and hence the lowest value in the abscisse of the force-distance curve. The start distance should exceed by far the distance at which attractive forces are relevant. Very common values are between -1µm and -100nm. 

.. _step size:

Step Size :math:`dZ`
--------------------

The step size :math:`dZ` is the inverse of the point rate (:math:`nm^{-1}`) of the data. 

.. _maximum piezo:

Maximum piezo displacement :math:`Z_{max}`
------------------------------------------

The maximum piezo displacement :math:`Z_{max}` marks the end of the Z-scale and hence the highest value on the abscisse of a force-distance curve. As the maximum piezo displacement :math:`Z_{max}` a positive value should be chosen, so contact between tip and sample is established.

.. _number of curves:

Size of Force Volume – number of curves
---------------------------------------

It is very common to record force distance curves in a x-y grid (mapping, also called force volume) rather than having single force-distance curves at arbitrary points. When recorded in a grid, the force spectroscopy data has an additional spatial information which is important for inhomogeneous samples. It is also useful for homogeneous samples because one acquires an array of curves which can be averaged and statistically treated for errors. In order to achieve a reasonable signal to noise ratio between 30 and 100 curves are averaged. 

.. _artefact parameters:

Artefact parameters
===================

Experimentally acquired force curves show typically artefacts, which are not present in ideal synthetic curves. These Artefacts can be added to the ideal curves in SyFoS and their magnitude can be controlled by the following parameters. 

.. _virtual deflection:

Virtual Deflection
------------------

Text in progress.

.. _topography offset:

Topography offset
-----------------

Text in progress.

.. _noise:

Noise
-----

Text in progress. 

Auxiliary Parameters
====================

From all parameters given by the user auxiliary parameters as :ref:`tip-sample distance <tip sample distance>` ζ, :ref:`reduced modulus <reduced modulus>` :math:`E_{tot}`, :ref:`jump to contact <jump to contact>` :math:`JTC` and :ref:`combined Hamaker <combined hamaker>` constant :math:`A_{tot}` can be calculated for creating a synthetic force curve. The auxiliary parameters are also given as output in the gui. 

.. _tip sample distance:

Tip-Sample distance
-------------------

For all theories, describing the different regimes of a force distance curve the true tip sample distance needs to be known. During the regime of attractive forces, the cantilever deflects towards the sample surface by :math:`δ`, thereby decreasing the tip sample distance :math:`ζ` additionally to the z-pizo displacement :math:`Z:ζ=δ−Z`. During the contact or the repulsive regime, the tip sample distance :math:`ζ` should be 0, but it is actually increased by the deformation :math:`D` that is caused by the contact between tip and sample: :math:`D=Z−δ`.

In SyFoS :math:`ζ` and :math:`D` are calculated continuously for each iterative step. Only between :math:`JTC` and contact the tip sample distance is assumed to be zero. This is a simplification but since this part of the data is not relevant for any automated analysis the effect of this simplification is neglectable. 

.. _reduced modulus:

Reduced modulus :math:`E_{tot}`
-------------------------------

The reduced Young’s modulus :math:`E_{tot}` is the resulting Young’s modulus of two materials - tip and sample - in contact. It is calculated from the :ref:`Young’s moduli <modulus>` of tip and sample and the :ref:`Poisson ratio <poisson ratio>` of tip and sample with the given equation :eq:`etot`. 

.. _jump to contact:

Jump to contact :math:`JTC`
---------------------------

The attractive forces :math:`F_{attr}` are dependent on the tip-sample distance (Eqn ). At a certain tip-sample distance the attractive forces :math:`F_{attr}` between sample and tip increase up to a point when their gradient exceeds the spring constant kc. Figure 1(ii) jump to contact (JTC): a discontinuity where the system is not in equilibrium and the tip snaps onto the sample. 

.. _combined hamaker:

Combined Hamaker constant :math:`A_{tot}`
-----------------------------------------

Text in progress.
Creating synthetic force spectroscopy data
==========================================

Under the umbrella term of force spectroscopy usually force curves, such as force distance curves (FDC) are understood. The process of generating an ideal curve is explained in :ref:`creation of ideal force curves`. In :ref:`creating force curves with artefacts` the most common sources of deviation of real force curves from an ideal force curve are shown, which can be added to the ideal curve in SyFoS. Since it is very common in an experiment to record more than one force curve, for example in a series or in an array (also called force volume) this option is also given in SyFoS (:ref:`creating force curve arrays`). 

.. _creation of ideal force curves:

Creation of ideal force curves
------------------------------

SyFoS is designed to mirror force spectroscopy measurements, more precisely the acquisition of force-distance curves (FDC). Below the FDC experiment is described.

.. _figure 1:

.. figure:: images/tip_sample_interaction.jpg
	:alt: Image describing a FDC experiment

	**Figure 1:** a) representation of tip-sample interactions b) schematic drawing of a FDC with (I) zero-line, (II) regime of attractive forces, (ii) JTC, (iii) contact and (III) contact line. 

During the acquisition of a FDC the AFM probe, a paraboloid shaped tip with :ref:`radius <radius>` :math:`R` is hold at a fixed x,y position while it approaches the sample surface by use of a :math:`Z-piezo` (3.1.6, 3.1.7 and 3.1.8). The tip is attached at a cantilever which can be described as an elastic spring following Hooke’s law:

:math:`F=k_{c}δ` (eq 1) 

with force :math:`F`, spring constant of the cantilever :math:`k_c` (3.1.1) and cantilever deflection :math:`δ`. In this way the forces acting on the tip are measured by recording the deflection :math:`δ` of the cantilever. While decreasing the distance between tip and sample, the cantilever deflects toward the sample (attractive forces) or away (repulsive forces), depending on which interacting forces are dominant. 

Due to the sum of all interacting forces, a FDC shows three typical regimes upon approach as depicted in Figure 1. 

Figure 1(I) **zero line**: when tip and sample are far away from each other and interacting forces are not detectable, the deflection signal :math:`δ` is zero which equals the free equilibrium position of the cantilever. 
Figure 1(II) **regime of attractive forces** :math:`F_{attr}`: upon further approach of sample and tip, attractive forces start to govern, and the cantilever is bend towards the sample. The attractive forces between sample and tip increase up to a point when their gradient exceeds the spring constant :math:`k_c`. Figure 1(ii) **jump to contact (JTC)**: a discontinuity where the system is not in equilibrium and the tip snaps onto the sample. Figure 1(iii) **contact**: attractive and repulsive forces are in balance and the cantilever has reached its equilibrium position again. Figure 1(III) contact line: upon further approach the repulsive forces are dominant, and the cantilever is pushed away from the sample. The deflection :math:`δ` corresponds to the applied force :math:`F` by Equation (1). At a maximum deflection :math:`δ_{max}`, (Fmax) the approach is stopped, and the sample is withdrawn until the contact is lost at jump off contact (JOC) and the zero line is reached again (only shown in Figure 1b, blue dashed line). In SyFoS, only the approach part of acquired curves is considered. 

This experiment is mirrored in SyFoS, by assigning the according cantilever deflection :math:`δ_i` to a given piezo displacement :math:`Z_i` for a range of :math:`Z` values starting from :math:`Z_0` and increasing by :math:`dZ` until :math:`Z_{max}` is reached (see 3.2). Due to the discontinuity of the JTC SyFoS creates the synthetic data by a case-by-case analysis, starting in the zero line and attractive regime. 

For every given piezo displacement at point :math:`i` :math:`Z_i` (:math:`Z_0 ≤ Z_i << Z=0`) the actual tip-sample distance :math:`ζ_i` is calculated: 

:math:`ζ=δ−Z` (eq2).

For the given tip-sample distance :math:`ζ_i` the van der Waals interaction :math:`F_{vdW,i}` and is calculated by: 


:math:`F_{vdW}=-\frac{A}{6}\frac{R}{δ-Z^2}=-\frac{A}{6}\frac{R}{ζ^2}` (eq3)

with Hamaker constant :math:`A` (3.1.5), tip radius :math:`R` (3.1.2), deflection :math:`δ`, piezo displacement :math:`Z` and tip-sample distance :math:`ζ`.

From the acting van der Waals force :math:`F_{vdW,i}` the resulting deflection :math:`δ_{(i+1)}` is determined by Equ 1. From this deflection :math:`δ_{(i+1)}` and :math:`Z_{(i+1)}=Z_i+dZ` the true tip-sample distance :math:`ζ_{(i+1)}` is calculated and the :math:`F_{vdW,i+1}` is calculated.

This continues until the condition for JTC is met, which is the case when the gradient (first derivative) of the attractive Forces (Equ. 2) equals or exceeds :math:`k_c`:

:math:`\frac{𝜕}{𝜕ζ}-\frac{A}{6}\frac{R}{ζ^2}=\frac{AR}{3ζ^3}\equiv k_c \to ζJTC=\sqrt[3]{\frac{AR}{3k_c}}` (eq4).

In this case SyFoS sets the tip-sample distance to :math:`ζ≡0` and assigns the according :math:`δ_{JTC}` to the piezo displacement :math:`Z_i` with :math:`δ_{JTC}<0`. 

This is continued for :math:`Z_i` until :math:`Z_i=0` and :math:`δ(Z_i)=0`. 

We want to point out, that in this region (from JTC to contact line, ii to iii in Figure 1), a mixture of attractive and repulsive forces acts on the tip-sample system, which cannot be correctly described without taking time-dependent parameters into account. Since this part of the force curve is not subject to any subsequent use as test data, there is no attempt to implement the necessary theory on the cost of over-complicating the acquisition of synthetic force curves. For this we refer to [nanohub link]. 

For all :math:`Z_i (Z=0 ≤ Zi ≤ Zmax)` the dominance of repulsive forces (contact line, Figure 1(III)) is assumed. Here, instead of a tip-sample distance :math:`ζ` the deformation :math:`D` has to be considered, which is calculated by:

:math:`D=Z-δ` with deflection :math:`δ` and piezo displacement :math:`Z` (eq5).

In order to calculate the correct deformation :math:`D` a theory of continuums mechanics has to be applied, in case of SyFoS we chose to use Hertz contact of a sphere versus a plane is used:

:math:`D=\frac{F}{\sqrt{r}E_{tot}}^{\frac{2}{3}}` (eq6)

With applied force :math:`F`, tip Radius :math:`R` (3.1.2) and the reduced Young’s modulus :math:`E_{tot}`.

:math:`\frac{1}{E_{tot}}=\frac{3}{4}\frac{1-ν^{2}_{tip}}{E_{tip}}+\frac{1-ν^2}{E}` (eq7)

with the Young’s modulus of the two materials :math:`E_{tip}` and :math:`E` (3.1.3) and their poisson ratios :math:`ν_{tip}` and :math:`ν` (3.1.4). 

SyFoS is creating the deflection :math:`δ` in dependence of the z piezo displacement :math:`δ(Z)` for any given :math:`Z_i`, with :math:`Z=0 ≤ Z_i ≤ Z_{max}`. To accommodate this in the Hertz theory (6) deformation :math:`D` and force :math:`F` have to by expressed through deflection :math:`δ` and z piezo displacement :math:`Z` by using Eqns 1 and 5. 

:math:`(Z-δ)=\frac{k_{c}δ}{\sqrt{R}E_{tot}}^\frac{2}{3}` (eq8)

With spring constant :math:`k_c` (3.1.1), tip radius :math:`R` (3.1.2) and reduced Young’s modulus :math:`E_{tot}` (3.2). 

For solving the equation, the constant parameters :math:`k_c`, :math:`R` and :math:`E_{tot}` are substituted by :math:`a=\frac{k_c}{\sqrt{r}E_{tot}}` leading to one real solution: 

:math:`δZ=\frac{1}{3}(3Z-a^2)+\frac{cubic root}{3 \sqrt[3]{2}}-\frac{\sqrt[3]{2}(6a^2Z-a^4)}{3*cubic root}` (eq9)

:math:`cubic root = \sqrt[3]{-2a^6+18a^4Z-27a^2Z^2+3 \sqrt{3}*inner root}`

:math:`inner root = \sqrt{27a^4Z^4-4a^6Z^3}`

The imaginary solutions are not taken into consideration for SyFoS since :math:`Z`, :math:`δ` and a have always positive values (>0). 

.. _creating force curves with artefacts:

Creating force curves with artefacts
------------------------------------

Experimentally acquired force curves differ in three respects from ideal force curves. First experimental curves usually experience a virtual deflection, which causes the deflection δ¹0 for the equilibrium position of the cantilever. This can be simply an offset or also a linear or sinusoidal function δ(Z). Second in FDC experiments the tip-sample distance is actually not known exactly. Since the topography of the sample is usually not perfectly smooth the point of JTC can be expected for a certain range of piezo displacements Z, but the exact point of contact (Z≡0) has to be established later during analysis. Thirdly, as all experimental data, also FDC suffer from noise. All three disturbance values can be added in SyFoS to the ideal curves, as explained in 3.3, in order to make the synthetic force spectroscopy data more realistic. 

.. _creating force curve arrays:

Creating force curve arrays 
---------------------------

It is very common to record force distance curves in a x-y grid (mapping, also called force volume) rather than having single force-distance curves at arbitrary points. When recorded in a grid, the force spectroscopy data has an additional spatial information which is important for inhomogeneous samples. It is also useful for homogeneous samples because one acquires an array of curves which can be averaged and statistically treated for errors. To mirror this in SyFoS arrays can also be created, consisting of single curves which exhibit artefacts as described in 2.2 and 3.3.
DF (``galpy.df``)
==================

``galpy.df`` contains tools for dealing with distribution functions of
stars in galaxies. It mainly contains a number of classes that define
different types of distribution function, but ``galpy.df.jeans`` also
has some tools for solving the Jeans equations for equilibrium
systems.

Jeans modeling tools (``galpy.df.jeans``)
-----------------------------------------

.. toctree::
   :maxdepth: 2

   sigmar <dfjeanssigmar.rst>
   sigmalos <dfjeanssigmalos.rst>

General instance routines for all df classes
--------------------------------------------


.. toctree::
   :maxdepth: 2

   turn_physical_off <dfturnphysicaloff.rst>
   turn_physical_on <dfturnphysicalon.rst>

.. _api_sphericaldfs:

Spherical distribution functions
---------------------------------

Isotropic and anisotropic distribution functions for spherical
systems. Documentation of these is limited at this point, but
generally, one can use them as::

  from galpy import potential
  from galpy.df import isotropicNFWdf
  np= potential.NFWPotential(amp=1.2,a=2.3)
  ndf= isotropicNFWdf(pot=np)
  # sample
  sam= ndf.sample(n=int(1e6))
  print(numpy.std(sam[numpy.fabs(sam.r()-1.2) < 0.1].vr()))
  # 0.2156787374302913
  # Compute vel. dispersion
  print(ndf.sigmar(1.2))
  # 0.21985277878647172

or::

  from galpy.df import kingdf
  kdf= kingdf(M=2.3,rt=1.4,W0=3.)
  sam= kdf.sample(n=int(1e6))
  print(numpy.amax(sam.r()))
  # 1.3883460662897116
  print(numpy.std(sam[numpy.fabs(sam.r()-0.2) < 0.01].vr()))
  # 1.081298923132113
  print(kdf.sigmar(0.2))
  # 1.0939934290993467

Various spherical DFs are explicitly implemented (e.g., Hernquist, NFW
using a new approximation, King, Plummer) in isotropic and various
anisotropic forms. General methods for computing isotropic,
constant-beta anisotropic, and Osipkov-Merritt anisotropic for any
potential/density pair are also included. Use of interpolated spherical 
potentials (``galpy.potential.interpSphericalPotential``) is also supported 
with DFs, however numerical issues can arise during sampling or calculation 
of moments of the DF, and so caution is recommended when using these potentials. 
It is adviseable to use a very finely spaced radial grid, and ensure that it 
spans a range of radii much larger than the radii of interest for the DF.

General instance routines
+++++++++++++++++++++++++


.. toctree::
   :maxdepth: 2

   __call__ <sphericaldfcall.rst>
   beta <sphericaldfbeta.rst>
   sigmar <sphericaldfsigmar.rst>
   sigmar <sphericaldfsigmat.rst>
   vmomentdensity <sphericaldfvmomentdensity.rst>

Sampling routines
^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   sample <sphericaldfsample.rst>

Specific distribution functions
+++++++++++++++++++++++++++++++

The following are isotropic distribution functions

.. toctree::
   :maxdepth: 2

   Arbitrary Eddington-inversion DF <dfeddington.rst>
   Hernquist DF <dfhernquist.rst>
   King DF <dfking.rst>
   NFW DF <dfnfw.rst>
   Plummer DF <dfplummer.rst>

Anisotropic versions also exist:

.. toctree::
   :maxdepth: 2

   Arbitrary constant-anisotropy DF <dfconstantbeta.rst>
   Arbitrary Osipkov-Merritt DF <dfosipkovmerritt.rst>
   Hernquist DF with constant anisotropy beta <dfhernquistconstantbeta.rst>
   Hernquist DF with Osipkov-Merritt anisotropy <dfhernquistosipkov.rst>
   NFW DF with Osipkov-Merritt anisotropy <dfnfwosipkov.rst>

Two-dimensional, axisymmetric disk distribution functions
----------------------------------------------------------

Distribution function for orbits in the plane of a galactic
disk.

General instance routines
+++++++++++++++++++++++++


.. toctree::
   :maxdepth: 2

   __call__ <diskdfcall.rst>
   asymmetricdrift <diskdfasymmetricdrift.rst>
   kurtosisvR <diskdfkurtosisvR.rst>
   kurtosisvT <diskdfkurtosisvT.rst>
   meanvR <diskdfmeanvR.rst>
   meanvT <diskdfmeanvT.rst>
   oortA <diskdfoortA.rst>
   oortB <diskdfoortB.rst>
   oortC <diskdfoortC.rst>
   oortK <diskdfoortK.rst>
   sigma2surfacemass <diskdfsigma2surfacemass.rst>
   sigma2 <diskdfsigma2.rst>
   sigmaR2 <diskdfsigmaR2.rst>
   sigmaT2 <diskdfsigmaT2.rst>
   skewvR <diskdfskewvR.rst>
   skewvT <diskdfskewvT.rst>
   surfacemass <diskdfsurfacemass.rst>
   surfacemassLOS <diskdfsurfacemassLOS.rst>
   targetSigma2 <diskdftargetSigma2.rst>
   targetSurfacemass <diskdftargetSurfacemass.rst>
   targetSurfacemassLOS <diskdftargetSurfacemassLOS.rst>
   vmomentsurfacemass <diskdfvmomentsurfacemass.rst>

Sampling routines
^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   sample <diskdfsample.rst>
   sampledSurfacemassLOS <diskdfsampledSurfacemassLOS.rst>
   sampleLOS <diskdfsampleLOS.rst>
   sampleVRVT <diskdfsampleVRVT.rst>


Specific distribution functions
+++++++++++++++++++++++++++++++

.. toctree::
   :maxdepth: 2

   Dehnen DF <dfdehnen.rst>
   Schwarzschild DF <dfschwarzschild.rst>
   Shu DF <dfshu.rst>


Two-dimensional, non-axisymmetric disk distribution functions
--------------------------------------------------------------

Distribution function for orbits in the plane of a galactic disk in
non-axisymmetric potentials. These are calculated using the technique
of `Dehnen 2000 <http://adsabs.harvard.edu/abs/2000AJ....119..800D>`_,
where the DF at the current time is obtained as the evolution of an
initially-axisymmetric DF at time ``to`` in the non-axisymmetric
potential until the current time.

General instance routines
+++++++++++++++++++++++++


.. toctree::
   :maxdepth: 2

   __call__ <edfcall.rst>
   __init__ <edf.rst>
   meanvR <edfmeanvr.rst>
   meanvT <edfmeanvt.rst>
   oortA <edfoorta.rst>
   oortB <edfoortb.rst>
   oortC <edfoortc.rst>
   oortK <edfoortk.rst>
   sigmaR2 <edfsigmar2.rst>
   sigmaRT <edfsigmart.rst>
   sigmaT2 <edfsigmat2.rst>
   vertexdev <edfvertexdev.rst>
   vmomentsurfacemass <edfvmomentsurfacemass.rst>

Three-dimensional disk distribution functions
----------------------------------------------

Distribution functions for orbits in galactic disks, including the
vertical motion for stars reaching large heights above the
plane. Currently only the *quasi-isothermal DF*.

General instance routines
+++++++++++++++++++++++++


.. toctree::
   :maxdepth: 2

   __call__ <quasidfcall.rst>
   density <quasidfdensity.rst>
   estimate_hr <quasidfestimatehr.rst>
   estimate_hsr <quasidfestimatehsr.rst>
   estimate_hsz <quasidfestimatehsz.rst>
   estimate_hz <quasidfestimatehz.rst>
   jmomentdensity <quasidfjmomentdensity.rst>
   meanjr <quasidfmeanjr.rst>
   meanjz <quasidfmeanjz.rst>
   meanlz <quasidfmeanlz.rst>
   meanvR <quasidfmeanvr.rst>
   meanvT <quasidfmeanvt.rst>
   meanvz <quasidfmeanvz.rst>
   pvR <quasidfpvr.rst>
   pvRvT <quasidfpvrvt.rst>
   pvRvz <quasidfpvrvz.rst>
   pvT <quasidfpvt.rst>
   pvTvz <quasidfpvtvz.rst>
   pvz <quasidfpvz.rst>
   sampleV <quasidfsamplev.rst>
   sampleV_interpolate <quasidfsamplevinterpolate.rst>
   sigmaR2 <quasidfsigmar2.rst>
   sigmaRz <quasidfsigmarz.rst>
   sigmaT2 <quasidfsigmat2.rst>
   sigmaz2 <quasidfsigmaz2.rst>
   surfacemass_z <quasidfsurfacemass_z.rst>
   tilt <quasidftilt.rst>
   vmomentdensity <quasidfvmomentdensity.rst>


Specific distribution functions
+++++++++++++++++++++++++++++++

.. toctree::
   :maxdepth: 2

   quasiisothermal DF <dfquasiisothermal.rst>


The distribution function of a tidal stream in action-angle coordinates
------------------------------------------------------------------------

From `Bovy 2014 <http://arxiv.org/abs/1401.2985>`_;
see :ref:`stream-tutorial`.

General instance routines
+++++++++++++++++++++++++

.. toctree::
   :maxdepth: 2

   __call__ <streamdfcall.rst>
   __init__ <streamdf.rst>
   calc_stream_lb <streamdfcalcstreamlb.rst>
   callMarg <streamdfcallmarg.rst>
   density_par <streamdfdenspar.rst>
   estimateTdisrupt <streamdfestimatetdisrupt.rst>
   find_closest_trackpoint <streamdffindclosesttrackpoint.rst>
   find_closest_trackpointLB <streamdffindclosesttrackpointlb.rst>
   freqEigvalRatio <streamdffreqeigvalratio.rst>
   gaussApprox <streamdfgaussapprox.rst>
   length <streamdflength.rst>
   meanangledAngle <streamdfmeanangledangle.rst>
   meanOmega <streamdfmeanomega.rst>
   meantdAngle <streamdfmeantdangle.rst>
   misalignment <streamdfmisalignment.rst>
   pangledAngle <streamdfpangledangle.rst>
   plotCompareTrackAAModel <streamdfplotcomparetrackaamodel.rst>
   plotProgenitor <streamdfplotprogenitor.rst>
   plotTrack <streamdfplottrack.rst>
   pOparapar <streamdfpoparapar.rst>
   ptdAngle <streamdfptdangle.rst>
   sample <streamdfsample.rst>
   sigangledAngle <streamdfsigangledangle.rst>
   sigOmega <streamdfsigomega.rst>
   sigtdAngle <streamdfsigtdangle.rst>
   subhalo_encounters <streamdfsubhaloencounters.rst>

The distribution function of a gap in a tidal stream
----------------------------------------------------

From `Sanders, Bovy, & Erkal 2015 <http://arxiv.org/abs/1510.03426>`_;
see :ref:`streamgap-tutorial`. Implemented as a subclass of
``streamdf``. No full implementation is available currently, but the
model can be set up and sampled as in the above paper.

General instance routines
+++++++++++++++++++++++++

.. toctree::
   :maxdepth: 2

   __init__ <streamgapdf.rst>
   sample <streamdfsample.rst>

Helper routines to compute kicks
+++++++++++++++++++++++++++++++++

.. toctree::
   :maxdepth: 2

   impulse_deltav_plummer <impulse_deltav_plummer.rst>
   impulse_deltav_plummer_curvedstream <impulse_deltav_plummer_curvedstream.rst>
   impulse_deltav_hernquist <impulse_deltav_hernquist.rst>
   impulse_deltav_hernquist_curvedstream <impulse_deltav_hernquist_curvedstream.rst>
   impulse_deltav_general <impulse_deltav_general.rst>
   impulse_deltav_general_curvedstream <impulse_deltav_general_curvedstream.rst>
   impulse_deltav_general_orbitintegration <impulse_deltav_general_orbitintegration.rst>
   impulse_deltav_general_fullplummerintegration <impulse_deltav_general_fullplummerintegration.rst>

The distribution function of a tidal stream using a particle-spray technique
----------------------------------------------------------------------------

Model from `Fardal et al. (2015)
<https://ui.adsabs.harvard.edu/abs/2015MNRAS.452..301F/abstract>`__ with full
details of the ``galpy`` implementation given in `Qian et al. (2022)
<https://ui.adsabs.harvard.edu/abs/2022MNRAS.511.2339Q/abstract>`__;
see :ref:`streamspray-tutorial`.

General instance routines
+++++++++++++++++++++++++

.. toctree::
   :maxdepth: 2

   __init__ <streamspraydf.rst>
   sample <streamspraydfsample.rst>

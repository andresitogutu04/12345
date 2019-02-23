##########################TESTS ON MULTIPLE ORBITS#############################
import sys
import numpy
import astropy.units as u
import astropy.coordinates as apycoords
import pytest
from galpy import potential
import astropy
_APY3= astropy.__version__ > '3'

# Test that initializing an Orbit (not an Orbits) with an array of SkyCoords
# processes the input correctly into the Orbit._orb.vxvv attribute;
# The Orbits class depends on this to process arrays SkyCoords itself quickly
def test_orbit_initialization_SkyCoordarray():
    # Only run this for astropy>3
    if not _APY3: return None
    from galpy.orbit import Orbit
    numpy.random.seed(1)
    nrand= 30
    ras= numpy.random.uniform(size=nrand)*360.*u.deg
    decs= 90.*(2.*numpy.random.uniform(size=nrand)-1.)*u.deg
    dists= numpy.random.uniform(size=nrand)*10.*u.kpc
    pmras= 20.*(2.*numpy.random.uniform(size=nrand)-1.)*20.*u.mas/u.yr
    pmdecs= 20.*(2.*numpy.random.uniform(size=nrand)-1.)*20.*u.mas/u.yr
    vloss= 200.*(2.*numpy.random.uniform(size=nrand)-1.)*u.km/u.s
    # Without any custom coordinate-transformation parameters
    co= apycoords.SkyCoord(ra=ras,dec=decs,distance=dists, 
                           pm_ra_cosdec=pmras,pm_dec=pmdecs,
                           radial_velocity=vloss,
                           frame='icrs')
    os= Orbit(co)
    vxvv= numpy.array(os._orb.vxvv).T
    for ii in range(nrand):
        to= Orbit(co[ii])
        assert numpy.all(numpy.fabs(numpy.array(to._orb.vxvv)-vxvv[ii]) < 1e-10), 'Orbit initialization with an array of SkyCoords does not give the same result as processing each SkyCoord individually'
    # With custom coordinate-transformation parameters
    v_sun= apycoords.CartesianDifferential([-11.1,215.,3.25]*u.km/u.s)
    co= apycoords.SkyCoord(ra=ras,dec=decs,distance=dists, 
                           pm_ra_cosdec=pmras,pm_dec=pmdecs,
                           radial_velocity=vloss,
                           frame='icrs',
                           galcen_distance=10.*u.kpc,z_sun=1.*u.kpc,
                           galcen_v_sun=v_sun)
    os= Orbit(co)
    vxvv= numpy.array(os._orb.vxvv).T
    for ii in range(nrand):
        to= Orbit(co[ii])
        assert numpy.all(numpy.fabs(numpy.array(to._orb.vxvv)-vxvv[ii]) < 1e-10), 'Orbit initialization with an array of SkyCoords does not give the same result as processing each SkyCoord individually'
    return None

# Test Orbits initialization
def test_initialization_vxvv():
    from galpy.orbit import Orbit, Orbits
    # 1D
    vxvvs= [[1.,0.1],[0.1,3.]]
    orbits= Orbits(vxvvs)
    assert orbits.dim() == 1, 'Orbits initialization with vxvv in 1D does not work as expected'
    assert orbits.phasedim() == 2, 'Orbits initialization with vxvv in 1D does not work as expected'
    assert numpy.fabs(orbits.x()[0]-1.) < 1e-10, 'Orbits initialization with vxvv in 1D does not work as expected'
    assert numpy.fabs(orbits.x()[1]-0.1) < 1e-10, 'Orbits initialization with vxvv in 1D does not work as expected'
    assert numpy.fabs(orbits.vx()[0]-0.1) < 1e-10, 'Orbits initialization with vxvv in 1D does not work as expected'
    assert numpy.fabs(orbits.vx()[1]-3.) < 1e-10, 'Orbits initialization with vxvv in 1D does not work as expected'
    # 2D, 3 phase-D
    vxvvs= [[1.,0.1,1.],[0.1,3.,1.1]]
    orbits= Orbits(vxvvs)
    assert orbits.dim() == 2, 'Orbits initialization with vxvv in 2D, 3 phase-D does not work as expected'
    assert orbits.phasedim() == 3, 'Orbits initialization with vxvv in 2D, 3 phase-D does not work as expected'
    assert numpy.fabs(orbits.R()[0]-1.) < 1e-10, 'Orbits initialization with vxvv in 2D, 3 phase-D does not work as expected'
    assert numpy.fabs(orbits.R()[1]-0.1) < 1e-10, 'Orbits initialization with vxvv in 2D, 3 phase-D does not work as expected'
    assert numpy.fabs(orbits.vR()[0]-0.1) < 1e-10, 'Orbits initialization with vxvv in 2D, 3 phase-D does not work as expected'
    assert numpy.fabs(orbits.vR()[1]-3.) < 1e-10, 'Orbits initialization with vxvv in 2D, 3 phase-D does not work as expected'
    assert numpy.fabs(orbits.vT()[0]-1.) < 1e-10, 'Orbits initialization with vxvv in 2D, 3 phase-D does not work as expected'
    assert numpy.fabs(orbits.vT()[1]-1.1) < 1e-10, 'Orbits initialization with vxvv in 2D, 3 phase-D does not work as expected'
    # 2D, 4 phase-D
    vxvvs= [[1.,0.1,1.,1.5],[0.1,3.,1.1,2.]]
    orbits= Orbits(vxvvs)
    assert orbits.dim() == 2, 'Orbits initialization with vxvv 2D, 4 phase-D does not work as expected'
    assert orbits.phasedim() == 4, 'Orbits initialization with vxvv 2D, 4 phase-D does not work as expected'
    assert numpy.fabs(orbits.R()[0]-1.) < 1e-10, 'Orbits initialization with vxvv 2D, 4 phase-D does not work as expected'
    assert numpy.fabs(orbits.R()[1]-0.1) < 1e-10, 'Orbits initialization with vxvv 2D, 4 phase-D does not work as expected'
    assert numpy.fabs(orbits.vR()[0]-0.1) < 1e-10, 'Orbits initialization with vxvv 2D, 4 phase-D does not work as expected'
    assert numpy.fabs(orbits.vR()[1]-3.) < 1e-10, 'Orbits initialization with vxvv 2D, 4 phase-D does not work as expected'
    assert numpy.fabs(orbits.vT()[0]-1.) < 1e-10, 'Orbits initialization with vxvv 2D, 4 phase-D does not work as expected'
    assert numpy.fabs(orbits.vT()[1]-1.1) < 1e-10, 'Orbits initialization with vxvv 2D, 4 phase-D does not work as expected'
    assert numpy.fabs(orbits.phi()[0]-1.5) < 1e-10, 'Orbits initialization with vxvv 2D, 4 phase-D does not work as expected'
    assert numpy.fabs(orbits.phi()[1]-2.) < 1e-10, 'Orbits initialization with vxvv 2D, 4 phase-D does not work as expected'
    # 3D, 5 phase-D
    vxvvs= [[1.,0.1,1.,0.1,-0.2],[0.1,3.,1.1,-0.3,0.4]]
    orbits= Orbits(vxvvs)
    assert orbits.dim() == 3, 'Orbits initialization with vxvv 3D, 5 phase-D does not work as expected'
    assert orbits.phasedim() == 5, 'Orbits initialization with vxvv 3D, 5 phase-D does not work as expected'
    assert numpy.fabs(orbits.R()[0]-1.) < 1e-10, 'Orbits initialization with vxvv 3D, 5 phase-D does not work as expected'
    assert numpy.fabs(orbits.R()[1]-0.1) < 1e-10, 'Orbits initialization with vxvv 3D, 5 phase-D does not work as expected'
    assert numpy.fabs(orbits.vR()[0]-0.1) < 1e-10, 'Orbits initialization with vxvv 3D, 5 phase-D does not work as expected'
    assert numpy.fabs(orbits.vR()[1]-3.) < 1e-10, 'Orbits initialization with vxvv 3D, 5 phase-D does not work as expected'
    assert numpy.fabs(orbits.vT()[0]-1.) < 1e-10, 'Orbits initialization with vxvv 3D, 5 phase-D does not work as expected'
    assert numpy.fabs(orbits.vT()[1]-1.1) < 1e-10, 'Orbits initialization with vxvv 3D, 5 phase-D does not work as expected'
    assert numpy.fabs(orbits.z()[0]-0.1) < 1e-10, 'Orbits initialization with vxvv 3D, 5 phase-D does not work as expected'
    assert numpy.fabs(orbits.z()[1]+0.3) < 1e-10, 'Orbits initialization with vxvv 3D, 5 phase-D does not work as expected'
    assert numpy.fabs(orbits.vz()[0]+0.2) < 1e-10, 'Orbits initialization with vxvv 3D, 5 phase-D does not work as expected'
    assert numpy.fabs(orbits.vz()[1]-0.4) < 1e-10, 'Orbits initialization with vxvv 3D, 5 phase-D does not work as expected'
    # 3D, 6 phase-D
    vxvvs= [[1.,0.1,1.,0.1,-0.2,1.5],[0.1,3.,1.1,-0.3,0.4,2.]]
    orbits= Orbits(vxvvs)
    assert orbits.dim() == 3, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert orbits.phasedim() == 6, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert numpy.fabs(orbits.R()[0]-1.) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert numpy.fabs(orbits.R()[1]-0.1) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert numpy.fabs(orbits.vR()[0]-0.1) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert numpy.fabs(orbits.vR()[1]-3.) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert numpy.fabs(orbits.vT()[0]-1.) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert numpy.fabs(orbits.vT()[1]-1.1) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert numpy.fabs(orbits.z()[0]-0.1) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert numpy.fabs(orbits.z()[1]+0.3) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert numpy.fabs(orbits.vz()[0]+0.2) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert numpy.fabs(orbits.vz()[1]-0.4) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert numpy.fabs(orbits.phi()[0]-1.5) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert numpy.fabs(orbits.phi()[1]-2.) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    return None

def test_initialization_SkyCoord():
    # Only run this for astropy>3
    if not _APY3: return None
    from galpy.orbit import Orbit, Orbits
    numpy.random.seed(1)
    nrand= 30
    ras= numpy.random.uniform(size=nrand)*360.*u.deg
    decs= 90.*(2.*numpy.random.uniform(size=nrand)-1.)*u.deg
    dists= numpy.random.uniform(size=nrand)*10.*u.kpc
    pmras= 20.*(2.*numpy.random.uniform(size=nrand)-1.)*20.*u.mas/u.yr
    pmdecs= 20.*(2.*numpy.random.uniform(size=nrand)-1.)*20.*u.mas/u.yr
    vloss= 200.*(2.*numpy.random.uniform(size=nrand)-1.)*u.km/u.s
    # Without any custom coordinate-transformation parameters
    co= apycoords.SkyCoord(ra=ras,dec=decs,distance=dists, 
                           pm_ra_cosdec=pmras,pm_dec=pmdecs,
                           radial_velocity=vloss,
                           frame='icrs')
    orbits= Orbits(co)
    assert orbits.dim() == 3, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert orbits.phasedim() == 6, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    for ii in range(nrand):
        to= Orbit(co[ii])
        assert numpy.fabs(orbits.R()[ii]-to.R()) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
        assert numpy.fabs(orbits.vR()[ii]-to.vR()) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
        assert numpy.fabs(orbits.vT()[ii]-to.vT()) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
        assert numpy.fabs(orbits.z()[ii]-to.z()) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
        assert numpy.fabs(orbits.vz()[ii]-to.vz()) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
        assert numpy.fabs(orbits.phi()[ii]-to.phi()) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    # With custom coordinate-transformation parameters
    v_sun= apycoords.CartesianDifferential([-11.1,215.,3.25]*u.km/u.s)
    co= apycoords.SkyCoord(ra=ras,dec=decs,distance=dists, 
                           pm_ra_cosdec=pmras,pm_dec=pmdecs,
                           radial_velocity=vloss,
                           frame='icrs',
                           galcen_distance=10.*u.kpc,z_sun=1.*u.kpc,
                           galcen_v_sun=v_sun)
    orbits= Orbits(co)
    assert orbits.dim() == 3, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    assert orbits.phasedim() == 6, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    for ii in range(nrand):
        to= Orbit(co[ii])
        assert numpy.fabs(orbits.R()[ii]-to.R()) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
        assert numpy.fabs(orbits.vR()[ii]-to.vR()) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
        assert numpy.fabs(orbits.vT()[ii]-to.vT()) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
        assert numpy.fabs(orbits.z()[ii]-to.z()) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
        assert numpy.fabs(orbits.vz()[ii]-to.vz()) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
        assert numpy.fabs(orbits.phi()[ii]-to.phi()) < 1e-10, 'Orbits initialization with vxvv in 3D, 6 phase-D does not work as expected'
    return None

# Test that attempting to initialize Orbits with radec, lb, or uvw gives 
# an error
def test_initialization_radecetc_error():
    from galpy.orbit import Orbits
    with pytest.raises(NotImplementedError) as excinfo:
        Orbits([[0.,0.,0.,0.,0.,0.,]],radec=True)
    with pytest.raises(NotImplementedError) as excinfo:
        Orbits([[0.,0.,0.,0.,0.,0.,]],lb=True)
    with pytest.raises(NotImplementedError) as excinfo:
        Orbits([[0.,0.,0.,0.,0.,0.,]],radec=True,uvw=True)
    return None

# Tests that integrating Orbits agrees with integrating multiple Orbit 
# instances
def test_integration_1d():
    from galpy.orbit import Orbit, Orbits
    times= numpy.linspace(0.,10.,1001)
    orbits_list= [Orbit([1.,0.1]),Orbit([0.1,1.]),Orbit([-0.2,0.3])]
    orbits= Orbits(orbits_list)
    # Integrate as Orbits, twice to make sure initial cond. isn't changed
    orbits.integrate(times,
                     potential.toVerticalPotential(potential.MWPotential2014,1.))
    orbits.integrate(times,
                     potential.toVerticalPotential(potential.MWPotential2014,1.))
    # Integrate as multiple Orbits
    for o in orbits_list:
        o.integrate(times,
                    potential.toVerticalPotential(potential.MWPotential2014,1.))
    # Compare
    for ii in range(len(orbits)):
        assert numpy.amax(numpy.fabs(orbits_list[ii].x(times)-orbits.x(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vx(times)-orbits.vx(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    return None
    
def test_integration_2d():
    from galpy.orbit import Orbit, Orbits
    times= numpy.linspace(0.,10.,1001)
    orbits_list= [Orbit([1.,0.1,1.,0.]),Orbit([.9,0.3,1.,-0.3]),
                  Orbit([1.2,-0.3,0.7,5.])]
    orbits= Orbits(orbits_list)
    # Integrate as Orbits, twice to make sure initial cond. isn't changed
    orbits.integrate(times,potential.MWPotential)
    orbits.integrate(times,potential.MWPotential)
    # Integrate as multiple Orbits
    for o in orbits_list:
        o.integrate(times,potential.MWPotential)
    # Compare
    for ii in range(len(orbits)):
        assert numpy.amax(numpy.fabs(orbits_list[ii].x(times)-orbits.x(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vx(times)-orbits.vx(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].y(times)-orbits.y(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vy(times)-orbits.vy(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].R(times)-orbits.R(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vR(times)-orbits.vR(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vT(times)-orbits.vT(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(((orbits_list[ii].phi(times)-orbits.phi(times)[ii]+numpy.pi) % (2.*numpy.pi)) - numpy.pi)) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    return None
    
def test_integration_p3d():
    # 3D phase-space integration
    from galpy.orbit import Orbit, Orbits
    times= numpy.linspace(0.,10.,1001)
    orbits_list= [Orbit([1.,0.1,1.]),Orbit([.9,0.3,1.]),
                  Orbit([1.2,-0.3,0.7])]
    orbits= Orbits(orbits_list)
    # Integrate as Orbits, twice to make sure initial cond. isn't changed
    orbits.integrate(times,potential.MWPotential2014)
    orbits.integrate(times,potential.MWPotential2014)
    # Integrate as multiple Orbits
    for o in orbits_list:
        o.integrate(times,potential.MWPotential2014)
    # Compare
    for ii in range(len(orbits)):
        assert numpy.amax(numpy.fabs(orbits_list[ii].R(times)-orbits.R(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vR(times)-orbits.vR(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vT(times)-orbits.vT(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    return None
    
def test_integration_3d():
    from galpy.orbit import Orbit, Orbits
    times= numpy.linspace(0.,10.,1001)
    orbits_list= [Orbit([1.,0.1,1.,0.,0.1,0.]),Orbit([.9,0.3,1.,-0.3,0.4,3.]),
                  Orbit([1.2,-0.3,0.7,.5,-0.5,6.])]
    orbits= Orbits(orbits_list)
    # Integrate as Orbits, twice to make sure initial cond. isn't changed
    orbits.integrate(times,potential.MWPotential2014)
    orbits.integrate(times,potential.MWPotential2014)
    # Integrate as multiple Orbits
    for o in orbits_list:
        o.integrate(times,potential.MWPotential2014)
    # Compare
    for ii in range(len(orbits)):
        assert numpy.amax(numpy.fabs(orbits_list[ii].x(times)-orbits.x(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vx(times)-orbits.vx(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].y(times)-orbits.y(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vy(times)-orbits.vy(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].z(times)-orbits.z(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vz(times)-orbits.vz(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].R(times)-orbits.R(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vR(times)-orbits.vR(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vT(times)-orbits.vT(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs((((orbits_list[ii].phi(times)-orbits.phi(times)[ii])+numpy.pi) % (2.*numpy.pi)) - numpy.pi)) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    return None
    
def test_integration_p5d():
    # 5D phase-space integration
    from galpy.orbit import Orbit, Orbits
    times= numpy.linspace(0.,10.,1001)
    orbits_list= [Orbit([1.,0.1,1.,0.,0.1]),Orbit([.9,0.3,1.,-0.3,0.4]),
                  Orbit([1.2,-0.3,0.7,.5,-0.5])]
    orbits= Orbits(orbits_list)
    # Integrate as Orbits, twice to make sure initial cond. isn't changed
    orbits.integrate(times,potential.MWPotential2014)
    orbits.integrate(times,potential.MWPotential2014)
    # Integrate as multiple Orbits
    for o in orbits_list:
        o.integrate(times,potential.MWPotential2014)
    # Compare
    for ii in range(len(orbits)):
        assert numpy.amax(numpy.fabs(orbits_list[ii].z(times)-orbits.z(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vz(times)-orbits.vz(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].R(times)-orbits.R(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vR(times)-orbits.vR(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vT(times)-orbits.vT(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    return None
    
# Tests that integrating Orbits agrees with integrating multiple Orbit 
# instances when using parallel_map Python paralleliization
def test_integration_forcemap_1d():
    from galpy.orbit import Orbit, Orbits
    times= numpy.linspace(0.,10.,1001)
    orbits_list= [Orbit([1.,0.1]),Orbit([0.1,1.]),Orbit([-0.2,0.3])]
    orbits= Orbits(orbits_list)
    # Integrate as Orbits
    orbits.integrate(times,
                     potential.toVerticalPotential(potential.MWPotential2014,1.),
                     force_map=True)
    # Integrate as multiple Orbits
    for o in orbits_list:
        o.integrate(times,
                    potential.toVerticalPotential(potential.MWPotential2014,1.))
    # Compare
    for ii in range(len(orbits)):
        assert numpy.amax(numpy.fabs(orbits_list[ii].x(times)-orbits.x(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vx(times)-orbits.vx(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    return None
    
def test_integration_forcemap_2d():
    from galpy.orbit import Orbit, Orbits
    times= numpy.linspace(0.,10.,1001)
    orbits_list= [Orbit([1.,0.1,1.,0.]),Orbit([.9,0.3,1.,-0.3]),
                  Orbit([1.2,-0.3,0.7,5.])]
    orbits= Orbits(orbits_list)
    # Integrate as Orbits
    orbits.integrate(times,potential.MWPotential2014,force_map=True)
    # Integrate as multiple Orbits
    for o in orbits_list:
        o.integrate(times,potential.MWPotential2014)
    # Compare
    for ii in range(len(orbits)):
        assert numpy.amax(numpy.fabs(orbits_list[ii].x(times)-orbits.x(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vx(times)-orbits.vx(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].y(times)-orbits.y(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vy(times)-orbits.vy(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].R(times)-orbits.R(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vR(times)-orbits.vR(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vT(times)-orbits.vT(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs((((orbits_list[ii].phi(times)-orbits.phi(times)[ii])+numpy.pi) % (2.*numpy.pi)) - numpy.pi)) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    return None
    
def test_integration_forcemap_3d():
    from galpy.orbit import Orbit, Orbits
    times= numpy.linspace(0.,10.,1001)
    orbits_list= [Orbit([1.,0.1,1.,0.,0.1,0.]),Orbit([.9,0.3,1.,-0.3,0.4,3.]),
                  Orbit([1.2,-0.3,0.7,.5,-0.5,6.])]
    orbits= Orbits(orbits_list)
    # Integrate as Orbits
    orbits.integrate(times,potential.MWPotential2014,force_map=True)
    # Integrate as multiple Orbits
    for o in orbits_list:
        o.integrate(times,potential.MWPotential2014)
    # Compare
    for ii in range(len(orbits)):
        assert numpy.amax(numpy.fabs(orbits_list[ii].x(times)-orbits.x(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vx(times)-orbits.vx(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].y(times)-orbits.y(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vy(times)-orbits.vy(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].z(times)-orbits.z(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vz(times)-orbits.vz(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].R(times)-orbits.R(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vR(times)-orbits.vR(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vT(times)-orbits.vT(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs((((orbits_list[ii].phi(times)-orbits.phi(times)[ii])+numpy.pi) % (2.*numpy.pi)) - numpy.pi)) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    return None

# Test slicing of orbits
def test_slice_singleobject():
    from galpy.orbit import Orbit, Orbits
    times= numpy.linspace(0.,10.,1001)
    orbits_list= [Orbit([1.,0.1,1.,0.,0.1,0.]),Orbit([.9,0.3,1.,-0.3,0.4,3.]),
                  Orbit([1.2,-0.3,0.7,.5,-0.5,6.])]
    orbits= Orbits(orbits_list)
    orbits.integrate(times,potential.MWPotential2014)
    indices= [0,1,-1]
    for ii in indices:
        assert numpy.amax(numpy.fabs(orbits[ii].x(times)-orbits.x(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits[ii].vx(times)-orbits.vx(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits[ii].y(times)-orbits.y(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits[ii].vy(times)-orbits.vy(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits[ii].z(times)-orbits.z(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits[ii].vz(times)-orbits.vz(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits[ii].R(times)-orbits.R(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits[ii].vR(times)-orbits.vR(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits[ii].vT(times)-orbits.vT(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs((((orbits[ii].phi(times)-orbits.phi(times)[ii])+numpy.pi) % (2.*numpy.pi)) - numpy.pi)) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    return None
    
# Test slicing of orbits
def test_slice_multipleobjects():
    from galpy.orbit import Orbit, Orbits
    times= numpy.linspace(0.,10.,1001)
    orbits_list= [Orbit([1.,0.1,1.,0.,0.1,0.]),
                  Orbit([.9,0.3,1.,-0.3,0.4,3.]),
                  Orbit([1.2,-0.3,0.7,.5,-0.5,6.]),
                  Orbit([0.6,-0.4,0.4,.25,-0.5,6.]),
                  Orbit([1.1,-0.13,0.17,.35,-0.5,2.])]
    orbits= Orbits(orbits_list)
    # Pre-integration
    orbits_slice= orbits[1:4]
    for ii in range(3):
        assert numpy.amax(numpy.fabs(orbits_slice.x()[ii]-orbits.x()[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.vx()[ii]-orbits.vx()[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.y()[ii]-orbits.y()[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.vy()[ii]-orbits.vy()[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.z()[ii]-orbits.z()[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.vz()[ii]-orbits.vz()[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.R()[ii]-orbits.R()[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.vR()[ii]-orbits.vR()[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.vT()[ii]-orbits.vT()[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.phi()[ii]-orbits.phi()[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    # After integration
    orbits.integrate(times,potential.MWPotential2014)
    orbits_slice= orbits[1:4]
    for ii in range(3):
        assert numpy.amax(numpy.fabs(orbits_slice.x(times)[ii]-orbits.x(times)[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.vx(times)[ii]-orbits.vx(times)[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.y(times)[ii]-orbits.y(times)[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.vy(times)[ii]-orbits.vy(times)[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.z(times)[ii]-orbits.z(times)[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.vz(times)[ii]-orbits.vz(times)[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.R(times)[ii]-orbits.R(times)[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.vR(times)[ii]-orbits.vR(times)[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.vT(times)[ii]-orbits.vT(times)[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_slice.phi(times)[ii]-orbits.phi(times)[ii+1])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    return None

def test_slice_integratedorbit_wrapperpot_367():
    # Test related to issue 367: slicing orbits with a potential that includes 
    # a wrapper potential (from Ted Mackereth)
    from galpy.orbit import Orbit, Orbits
    from galpy.potential import DehnenSmoothWrapperPotential, \
        DehnenBarPotential, LogarithmicHaloPotential
    #initialise a wrapper potential
    tform= -10.
    tsteady= 5. 
    omega= 1.85 
    angle=25./180.*numpy.pi 
    dp= DehnenBarPotential(omegab=omega,rb=3.5/8.,Af=(1./75.),
                           tform=tform,tsteady=tsteady,barphi=angle)
    lhp=LogarithmicHaloPotential(normalize=1.)
    dswp= DehnenSmoothWrapperPotential(pot=dp,tform=-4.*2.*numpy.pi/dp.OmegaP(),
                                       tsteady=2.*2.*numpy.pi/dp.OmegaP())
    pot= [lhp,dswp]
    #initialise 2 random orbits
    r = numpy.random.randn(2)*0.01+1.
    z = numpy.random.randn(2)*0.01+0.2
    phi = numpy.random.randn(2)*0.01+0.
    vR = numpy.random.randn(2)*0.01+0.
    vT = numpy.random.randn(2)*0.01+1.
    vz = numpy.random.randn(2)*0.01+0.02
    vxvv = numpy.dstack([r,vR,vT,z,vz,phi])[0]
    os = Orbits(vxvv)
    times = numpy.linspace(0.,100.,3000)
    os.integrate(times,pot)
    # This failed in #367
    assert not os[0] is None, 'Slicing an integrated Orbits instance with a WrapperPotential does not work'
    return None
 
# Test that initializing Orbits with orbits with different phase-space
# dimensions raises an error
def test_initialize_diffphasedim_error():
    from galpy.orbit import Orbits
    # 2D with 3D
    with pytest.raises(RuntimeError) as excinfo:
        Orbits([[1.,0.1],[1.,0.1,1.]])
    # 2D with 4D
    with pytest.raises(RuntimeError) as excinfo:
        Orbits([[1.,0.1],[1.,0.1,1.,0.1]])
    # 2D with 5D
    with pytest.raises(RuntimeError) as excinfo:
        Orbits([[1.,0.1],[1.,0.1,1.,0.1,0.2]])
    # 2D with 6D
    with pytest.raises(RuntimeError) as excinfo:
        Orbits([[1.,0.1],[1.,0.1,1.,0.1,0.2,3.]])
    # 3D with 4D
    with pytest.raises(RuntimeError) as excinfo:
        Orbits([[1.,0.1,1.],[1.,0.1,1.,0.1]])
    # 3D with 5D
    with pytest.raises(RuntimeError) as excinfo:
        Orbits([[1.,0.1,1.],[1.,0.1,1.,0.1,0.2]])
    # 3D with 6D
    with pytest.raises(RuntimeError) as excinfo:
        Orbits([[1.,0.1,1.],[1.,0.1,1.,0.1,0.2,6.]])
    # 4D with 5D
    with pytest.raises(RuntimeError) as excinfo:
        Orbits([[1.,0.1,1.,2.],[1.,0.1,1.,0.1,0.2]])
    # 4D with 6D
    with pytest.raises(RuntimeError) as excinfo:
        Orbits([[1.,0.1,1.,2.],[1.,0.1,1.,0.1,0.2,6.]])
    # 5D with 6D
    with pytest.raises(RuntimeError) as excinfo:
        Orbits([[1.,0.1,1.,0.2,-0.2],[1.,0.1,1.,0.1,0.2,6.]])
    return None

def test_orbits_consistentro():
    from galpy.orbit import Orbit, Orbits
    ro= 7.
    # Initialize Orbits from list of Orbit instances
    orbits_list= [Orbit([1.,0.1,1.,0.1,0.2,-3.],ro=ro),
                  Orbit([1.,0.1,1.,0.1,0.2,-4.],ro=ro)]
    orbits= Orbits(orbits_list)
    # Check that ro is taken correctly
    assert numpy.fabs(orbits._ro-orbits_list[0]._ro) < 1e-10, "Orbits' ro not correctly taken from input list of Orbit instances"
    assert orbits._roSet, "Orbits' ro not correctly taken from input list of Orbit instances"
    # Check that consistency of ros is enforced
    with pytest.raises(RuntimeError) as excinfo:
        orbits= Orbits(orbits_list,ro=6.)
    orbits_list= [Orbit([1.,0.1,1.,0.1,0.2,-3.],ro=ro),
                  Orbit([1.,0.1,1.,0.1,0.2,-4.],ro=ro*1.2)]
    with pytest.raises(RuntimeError) as excinfo:
        orbits= Orbits(orbits_list,ro=ro)
    return None

def test_orbits_consistentvo():
    from galpy.orbit import Orbit, Orbits
    vo= 230.
    # Initialize Orbits from list of Orbit instances
    orbits_list= [Orbit([1.,0.1,1.,0.1,0.2,-3.],vo=vo),
                  Orbit([1.,0.1,1.,0.1,0.2,-4.],vo=vo)]
    orbits= Orbits(orbits_list)
    # Check that vo is taken correctly
    assert numpy.fabs(orbits._vo-orbits_list[0]._vo) < 1e-10, "Orbits' vo not correctly taken from input list of Orbit instances"
    assert orbits._voSet, "Orbits' vo not correctly taken from input list of Orbit instances"
    # Check that consistency of vos is enforced
    with pytest.raises(RuntimeError) as excinfo:
        orbits= Orbits(orbits_list,vo=210.)
    orbits_list= [Orbit([1.,0.1,1.,0.1,0.2,-3.],vo=vo),
                  Orbit([1.,0.1,1.,0.1,0.2,-4.],vo=vo*1.2)]
    with pytest.raises(RuntimeError) as excinfo:
        orbits= Orbits(orbits_list,vo=vo)
    return None

def test_orbits_consistentzo():
    from galpy.orbit import Orbit, Orbits
    zo= 0.015
    # Initialize Orbits from list of Orbit instances
    orbits_list= [Orbit([1.,0.1,1.,0.1,0.2,-3.],zo=zo),
                  Orbit([1.,0.1,1.,0.1,0.2,-4.],zo=zo)]
    orbits= Orbits(orbits_list)
    # Check that zo is taken correctly
    assert numpy.fabs(orbits._zo-orbits_list[0]._orb._zo) < 1e-10, "Orbits' zo not correctly taken from input list of Orbit instances"
    # Check that consistency of zos is enforced
    with pytest.raises(RuntimeError) as excinfo:
        orbits= Orbits(orbits_list,zo=0.045)
    orbits_list= [Orbit([1.,0.1,1.,0.1,0.2,-3.],zo=zo),
                  Orbit([1.,0.1,1.,0.1,0.2,-4.],zo=zo*1.2)]
    with pytest.raises(RuntimeError) as excinfo:
        orbits= Orbits(orbits_list,zo=zo)
    return None

def test_orbits_consistentsolarmotion():
    from galpy.orbit import Orbit, Orbits
    solarmotion= numpy.array([-10.,20.,30.])
    # Initialize Orbits from list of Orbit instances
    orbits_list= [Orbit([1.,0.1,1.,0.1,0.2,-3.],solarmotion=solarmotion),
                  Orbit([1.,0.1,1.,0.1,0.2,-4.],solarmotion=solarmotion)]
    orbits= Orbits(orbits_list)
    # Check that solarmotion is taken correctly
    assert numpy.all(numpy.fabs(orbits._solarmotion-orbits_list[0]._orb._solarmotion) < 1e-10), "Orbits' solarmotion not correctly taken from input list of Orbit instances"
    # Check that consistency of solarmotions is enforced
    with pytest.raises(RuntimeError) as excinfo:
        orbits= Orbits(orbits_list,solarmotion=numpy.array([15.,20.,30]))
    with pytest.raises(RuntimeError) as excinfo:
        orbits= Orbits(orbits_list,solarmotion=numpy.array([-10.,25.,30]))
    with pytest.raises(RuntimeError) as excinfo:
        orbits= Orbits(orbits_list,solarmotion=numpy.array([-10.,20.,-30]))
    orbits_list= [Orbit([1.,0.1,1.,0.1,0.2,-3.],solarmotion=solarmotion),
                  Orbit([1.,0.1,1.,0.1,0.2,-4.],solarmotion=solarmotion*1.2)]
    with pytest.raises(RuntimeError) as excinfo:
        orbits= Orbits(orbits_list,solarmotion=solarmotion)
    return None

def test_orbits_stringsolarmotion():
    from galpy.orbit import Orbit, Orbits
    solarmotion= 'hogg'
    orbits_list= [Orbit([1.,0.1,1.,0.1,0.2,-3.],solarmotion=solarmotion),
                  Orbit([1.,0.1,1.,0.1,0.2,-4.],solarmotion=solarmotion)]
    orbits= Orbits(orbits_list,solarmotion='hogg')
    assert numpy.all(numpy.fabs(orbits._solarmotion-numpy.array([-10.1,4.0,6.7])) < 1e-10), 'String solarmotion not parsed correcty'
    return None
                     
def test_orbits_dim_2dPot_3dOrb():
    # Test that orbit integration throws an error when using a potential that
    # is lower dimensional than the orbit (using ~Plevne's example)
    from galpy.util import bovy_conversion
    from galpy.orbit import Orbit, Orbits
    b_p= potential.PowerSphericalPotentialwCutoff(\
        alpha=1.8,rc=1.9/8.,normalize=0.05)
    ell_p= potential.EllipticalDiskPotential()
    pota=[b_p,ell_p]
    o= Orbits([Orbit(vxvv=[20.,10.,2.,3.2,3.4,-100.],
                     radec=True,ro=8.0,vo=220.0),
               Orbit(vxvv=[20.,10.,2.,3.2,3.4,-100.],
                     radec=True,ro=8.0,vo=220.0)])
    ts= numpy.linspace(0.,3.5/bovy_conversion.time_in_Gyr(vo=220.0,ro=8.0),
                       1000,endpoint=True)
    with pytest.raises(AssertionError) as excinfo:
        o.integrate(ts,pota,method="odeint")
    return None

def test_orbit_dim_1dPot_3dOrb():
    # Test that orbit integration throws an error when using a potential that
    # is lower dimensional than the orbit, for a 1D potential
    from galpy.util import bovy_conversion
    from galpy.orbit import Orbit, Orbits
    b_p= potential.PowerSphericalPotentialwCutoff(\
        alpha=1.8,rc=1.9/8.,normalize=0.05)
    pota= potential.RZToverticalPotential(b_p,1.1)
    o= Orbits([Orbit(vxvv=[20.,10.,2.,3.2,3.4,-100.],
                     radec=True,ro=8.0,vo=220.0),
               Orbit(vxvv=[20.,10.,2.,3.2,3.4,-100.],
                     radec=True,ro=8.0,vo=220.0)])
    ts= numpy.linspace(0.,3.5/bovy_conversion.time_in_Gyr(vo=220.0,ro=8.0),
                       1000,endpoint=True)
    with pytest.raises(AssertionError) as excinfo:
        o.integrate(ts,pota,method="odeint")
    return None

def test_orbit_dim_1dPot_2dOrb():
    # Test that orbit integration throws an error when using a potential that
    # is lower dimensional than the orbit, for a 1D potential
    from galpy.orbit import Orbit, Orbits
    b_p= potential.PowerSphericalPotentialwCutoff(\
        alpha=1.8,rc=1.9/8.,normalize=0.05)
    pota= [b_p.toVertical(1.1)]
    o= Orbits([Orbit(vxvv=[1.1,0.1,1.1,0.1]),Orbit(vxvv=[1.1,0.1,1.1,0.1])])
    ts= numpy.linspace(0.,10.,1001)
    with pytest.raises(AssertionError) as excinfo:
        o.integrate(ts,pota,method="leapfrog")
    with pytest.raises(AssertionError) as excinfo:
        o.integrate(ts,pota,method="dop853")
    return None

# Test the error for when explicit stepsize does not divide the output stepsize
def test_check_integrate_dt():
    from galpy.orbit import Orbit, Orbits
    from galpy.potential import LogarithmicHaloPotential
    lp= LogarithmicHaloPotential(normalize=1.,q=0.9)
    o= Orbits([Orbit([1.,0.1,1.2,0.3,0.2,2.]),
               Orbit([1.,0.1,1.2,0.3,0.2,2.])])
    times= numpy.linspace(0.,7.,251)
    # This shouldn't work
    try:
        o.integrate(times,lp,dt=(times[1]-times[0])/4.*1.1)
    except ValueError: pass
    else: raise AssertionError('dt that is not an integer divisor of the output step size does not raise a ValueError')
    # This should
    try:
        o.integrate(times,lp,dt=(times[1]-times[0])/4.)
    except ValueError:
        raise AssertionError('dt that is an integer divisor of the output step size raises a ValueError')
    return None

# Test that evaluating coordinate functions for integrated orbits works
def test_coordinate_interpolation():
    from galpy.orbit import Orbit, Orbits
    from galpy.potential import MWPotential2014
    numpy.random.seed(1)
    nrand= 10
    Rs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)+1.
    vRs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)
    vTs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)+1.
    zs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)
    vzs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)
    phis= 2.*numpy.pi*(2.*numpy.random.uniform(size=nrand)-1.)
    os= Orbits(list(zip(Rs,vRs,vTs,zs,vzs,phis)))
    list_os= [Orbit([R,vR,vT,z,vz,phi])
              for R,vR,vT,z,vz,phi in zip(Rs,vRs,vTs,zs,vzs,phis)]
    # Before integration
    for ii in range(nrand):
        assert numpy.all(numpy.fabs(os.R()[ii]-list_os[ii].R()) < 1e-10), 'Evaluating Orbits R does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.r()[ii]-list_os[ii].r()) < 1e-10), 'Evaluating Orbits r does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vR()[ii]-list_os[ii].vR()) < 1e-10), 'Evaluating Orbits vR does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vT()[ii]-list_os[ii].vT()) < 1e-10), 'Evaluating Orbits vT does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.z()[ii]-list_os[ii].z()) < 1e-10), 'Evaluating Orbits z does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vz()[ii]-list_os[ii].vz()) < 1e-10), 'Evaluating Orbits vz does not agree with Orbit'
        assert numpy.all(numpy.fabs(((os.phi()[ii]-list_os[ii].phi()+numpy.pi) % (2.*numpy.pi)) - numpy.pi) < 1e-10), 'Evaluating Orbits phi does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.x()[ii]-list_os[ii].x()) < 1e-10), 'Evaluating Orbits x does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.y()[ii]-list_os[ii].y()) < 1e-10), 'Evaluating Orbits y does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vx()[ii]-list_os[ii].vx()) < 1e-10), 'Evaluating Orbits vx does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vy()[ii]-list_os[ii].vy()) < 1e-10), 'Evaluating Orbits vy does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vphi()[ii]-list_os[ii].vphi()) < 1e-10), 'Evaluating Orbits vphi does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.ra()[ii]-list_os[ii].ra()) < 1e-10), 'Evaluating Orbits ra  does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.dec()[ii]-list_os[ii].dec()) < 1e-10), 'Evaluating Orbits dec does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.dist()[ii]-list_os[ii].dist()) < 1e-10), 'Evaluating Orbits dist does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.ll()[ii]-list_os[ii].ll()) < 1e-10), 'Evaluating Orbits ll does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.bb()[ii]-list_os[ii].bb()) < 1e-10), 'Evaluating Orbits bb  does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmra()[ii]-list_os[ii].pmra()) < 1e-10), 'Evaluating Orbits pmra does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmdec()[ii]-list_os[ii].pmdec()) < 1e-10), 'Evaluating Orbits pmdec does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmll()[ii]-list_os[ii].pmll()) < 1e-10), 'Evaluating Orbits ll does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmbb()[ii]-list_os[ii].pmbb()) < 1e-10), 'Evaluating Orbits pmbb does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vlos()[ii]-list_os[ii].vlos()) < 1e-10), 'Evaluating Orbits vlos does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioX()[ii]-list_os[ii].helioX()) < 1e-10), 'Evaluating Orbits helioX does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioY()[ii]-list_os[ii].helioY()) < 1e-10), 'Evaluating Orbits helioY does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioZ()[ii]-list_os[ii].helioZ()) < 1e-10), 'Evaluating Orbits helioZ does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.U()[ii]-list_os[ii].U()) < 1e-10), 'Evaluating Orbits U does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.V()[ii]-list_os[ii].V()) < 1e-10), 'Evaluating Orbits V does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.W()[ii]-list_os[ii].W()) < 1e-10), 'Evaluating Orbits W does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord().ra[ii]-list_os[ii].SkyCoord().ra).to(u.deg).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord().dec[ii]-list_os[ii].SkyCoord().dec).to(u.deg).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord().distance[ii]-list_os[ii].SkyCoord().distance).to(u.kpc).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        if _APY3:
            assert numpy.all(numpy.fabs(os.SkyCoord().pm_ra_cosdec[ii]-list_os[ii].SkyCoord().pm_ra_cosdec).to(u.mas/u.yr).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
            assert numpy.all(numpy.fabs(os.SkyCoord().pm_dec[ii]-list_os[ii].SkyCoord().pm_dec).to(u.mas/u.yr).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
            assert numpy.all(numpy.fabs(os.SkyCoord().radial_velocity[ii]-list_os[ii].SkyCoord().radial_velocity).to(u.km/u.s).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
    # Integrate all
    times= numpy.linspace(0.,10.,1001)
    os.integrate(times,MWPotential2014)
    [o.integrate(times,MWPotential2014) for o in list_os]
    # Test exact times of integration
    for ii in range(nrand):
        assert numpy.all(numpy.fabs(os.R(times)[ii]-list_os[ii].R(times)) < 1e-10), 'Evaluating Orbits R does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.r(times)[ii]-list_os[ii].r(times)) < 1e-10), 'Evaluating Orbits r does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vR(times)[ii]-list_os[ii].vR(times)) < 1e-10), 'Evaluating Orbits vR does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vT(times)[ii]-list_os[ii].vT(times)) < 1e-10), 'Evaluating Orbits vT does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.z(times)[ii]-list_os[ii].z(times)) < 1e-10), 'Evaluating Orbits z does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vz(times)[ii]-list_os[ii].vz(times)) < 1e-10), 'Evaluating Orbits vz does not agree with Orbit'
        assert numpy.all(numpy.fabs(((os.phi(times)[ii]-list_os[ii].phi(times)+numpy.pi) % (2.*numpy.pi)) - numpy.pi) < 1e-10), 'Evaluating Orbits phi does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.x(times)[ii]-list_os[ii].x(times)) < 1e-10), 'Evaluating Orbits x does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.y(times)[ii]-list_os[ii].y(times)) < 1e-10), 'Evaluating Orbits y does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vx(times)[ii]-list_os[ii].vx(times)) < 1e-10), 'Evaluating Orbits vx does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vy(times)[ii]-list_os[ii].vy(times)) < 1e-10), 'Evaluating Orbits vy does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vphi(times)[ii]-list_os[ii].vphi(times)) < 1e-10), 'Evaluating Orbits vphi does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.ra(times)[ii]-list_os[ii].ra(times)) < 1e-10), 'Evaluating Orbits ra  does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.dec(times)[ii]-list_os[ii].dec(times)) < 1e-10), 'Evaluating Orbits dec does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.dist(times)[ii]-list_os[ii].dist(times)) < 1e-10), 'Evaluating Orbits dist does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.ll(times)[ii]-list_os[ii].ll(times)) < 1e-10), 'Evaluating Orbits ll does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.bb(times)[ii]-list_os[ii].bb(times)) < 1e-10), 'Evaluating Orbits bb  does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmra(times)[ii]-list_os[ii].pmra(times)) < 1e-10), 'Evaluating Orbits pmra does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmdec(times)[ii]-list_os[ii].pmdec(times)) < 1e-10), 'Evaluating Orbits pmdec does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmll(times)[ii]-list_os[ii].pmll(times)) < 1e-10), 'Evaluating Orbits ll does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmbb(times)[ii]-list_os[ii].pmbb(times)) < 1e-10), 'Evaluating Orbits pmbb does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vlos(times)[ii]-list_os[ii].vlos(times)) < 1e-9), 'Evaluating Orbits vlos does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioX(times)[ii]-list_os[ii].helioX(times)) < 1e-10), 'Evaluating Orbits helioX does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioY(times)[ii]-list_os[ii].helioY(times)) < 1e-10), 'Evaluating Orbits helioY does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioZ(times)[ii]-list_os[ii].helioZ(times)) < 1e-10), 'Evaluating Orbits helioZ does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.U(times)[ii]-list_os[ii].U(times)) < 1e-10), 'Evaluating Orbits U does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.V(times)[ii]-list_os[ii].V(times)) < 1e-10), 'Evaluating Orbits V does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.W(times)[ii]-list_os[ii].W(times)) < 1e-10), 'Evaluating Orbits W does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord(times).ra[ii]-list_os[ii].SkyCoord(times).ra).to(u.deg).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord(times).dec[ii]-list_os[ii].SkyCoord(times).dec).to(u.deg).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord(times).distance[ii]-list_os[ii].SkyCoord(times).distance).to(u.kpc).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        if _APY3:
            assert numpy.all(numpy.fabs(os.SkyCoord(times).pm_ra_cosdec[ii]-list_os[ii].SkyCoord(times).pm_ra_cosdec).to(u.mas/u.yr).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
            assert numpy.all(numpy.fabs(os.SkyCoord(times).pm_dec[ii]-list_os[ii].SkyCoord(times).pm_dec).to(u.mas/u.yr).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
            assert numpy.all(numpy.fabs(os.SkyCoord(times).radial_velocity[ii]-list_os[ii].SkyCoord(times).radial_velocity).to(u.km/u.s).value < 1e-9), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        # Also a single time in the array ...
        assert numpy.all(numpy.fabs(os.R(times[1])[ii]-list_os[ii].R(times[1])) < 1e-10), 'Evaluating Orbits R does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.r(times[1])[ii]-list_os[ii].r(times[1])) < 1e-10), 'Evaluating Orbits r does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vR(times[1])[ii]-list_os[ii].vR(times[1])) < 1e-10), 'Evaluating Orbits vR does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vT(times[1])[ii]-list_os[ii].vT(times[1])) < 1e-10), 'Evaluating Orbits vT does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.z(times[1])[ii]-list_os[ii].z(times[1])) < 1e-10), 'Evaluating Orbits z does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vz(times[1])[ii]-list_os[ii].vz(times[1])) < 1e-10), 'Evaluating Orbits vz does not agree with Orbit'
        assert numpy.all(numpy.fabs(((os.phi(times[1])[ii]-list_os[ii].phi(times[1])+numpy.pi) % (2.*numpy.pi)) - numpy.pi) < 1e-10), 'Evaluating Orbits phi does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.x(times[1])[ii]-list_os[ii].x(times[1])) < 1e-10), 'Evaluating Orbits x does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.y(times[1])[ii]-list_os[ii].y(times[1])) < 1e-10), 'Evaluating Orbits y does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vx(times[1])[ii]-list_os[ii].vx(times[1])) < 1e-10), 'Evaluating Orbits vx does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vy(times[1])[ii]-list_os[ii].vy(times[1])) < 1e-10), 'Evaluating Orbits vy does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vphi(times[1])[ii]-list_os[ii].vphi(times[1])) < 1e-10), 'Evaluating Orbits vphi does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.ra(times[1])[ii]-list_os[ii].ra(times[1])) < 1e-10), 'Evaluating Orbits ra  does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.dec(times[1])[ii]-list_os[ii].dec(times[1])) < 1e-10), 'Evaluating Orbits dec does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.dist(times[1])[ii]-list_os[ii].dist(times[1])) < 1e-10), 'Evaluating Orbits dist does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.ll(times[1])[ii]-list_os[ii].ll(times[1])) < 1e-10), 'Evaluating Orbits ll does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.bb(times[1])[ii]-list_os[ii].bb(times[1])) < 1e-10), 'Evaluating Orbits bb  does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmra(times[1])[ii]-list_os[ii].pmra(times[1])) < 1e-10), 'Evaluating Orbits pmra does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmdec(times[1])[ii]-list_os[ii].pmdec(times[1])) < 1e-10), 'Evaluating Orbits pmdec does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmll(times[1])[ii]-list_os[ii].pmll(times[1])) < 1e-10), 'Evaluating Orbits ll does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmbb(times[1])[ii]-list_os[ii].pmbb(times[1])) < 1e-10), 'Evaluating Orbits pmbb does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vlos(times[1])[ii]-list_os[ii].vlos(times[1])) < 1e-10), 'Evaluating Orbits vlos does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioX(times[1])[ii]-list_os[ii].helioX(times[1])) < 1e-10), 'Evaluating Orbits helioX does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioY(times[1])[ii]-list_os[ii].helioY(times[1])) < 1e-10), 'Evaluating Orbits helioY does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioZ(times[1])[ii]-list_os[ii].helioZ(times[1])) < 1e-10), 'Evaluating Orbits helioZ does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.U(times[1])[ii]-list_os[ii].U(times[1])) < 1e-10), 'Evaluating Orbits U does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.V(times[1])[ii]-list_os[ii].V(times[1])) < 1e-10), 'Evaluating Orbits V does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.W(times[1])[ii]-list_os[ii].W(times[1])) < 1e-10), 'Evaluating Orbits W does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord(times[1]).ra[ii]-list_os[ii].SkyCoord(times[1]).ra).to(u.deg).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord(times[1]).dec[ii]-list_os[ii].SkyCoord(times[1]).dec).to(u.deg).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord(times[1]).distance[ii]-list_os[ii].SkyCoord(times[1]).distance).to(u.kpc).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        if _APY3:
            assert numpy.all(numpy.fabs(os.SkyCoord(times[1]).pm_ra_cosdec[ii]-list_os[ii].SkyCoord(times[1]).pm_ra_cosdec).to(u.mas/u.yr).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
            assert numpy.all(numpy.fabs(os.SkyCoord(times[1]).pm_dec[ii]-list_os[ii].SkyCoord(times[1]).pm_dec).to(u.mas/u.yr).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
            assert numpy.all(numpy.fabs(os.SkyCoord(times[1]).radial_velocity[ii]-list_os[ii].SkyCoord(times[1]).radial_velocity).to(u.km/u.s).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
    # Test actual interpolated
    itimes= times[:-2]+(times[1]-times[0])/2.
    for ii in range(nrand):
        assert numpy.all(numpy.fabs(os.R(itimes)[ii]-list_os[ii].R(itimes)) < 1e-10), 'Evaluating Orbits R does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.r(itimes)[ii]-list_os[ii].r(itimes)) < 1e-10), 'Evaluating Orbits r does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vR(itimes)[ii]-list_os[ii].vR(itimes)) < 1e-10), 'Evaluating Orbits vR does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vT(itimes)[ii]-list_os[ii].vT(itimes)) < 1e-10), 'Evaluating Orbits vT does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.z(itimes)[ii]-list_os[ii].z(itimes)) < 1e-10), 'Evaluating Orbits z does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vz(itimes)[ii]-list_os[ii].vz(itimes)) < 1e-10), 'Evaluating Orbits vz does not agree with Orbit'
        assert numpy.all(numpy.fabs(((os.phi(itimes)[ii]-list_os[ii].phi(itimes)+numpy.pi) % (2.*numpy.pi)) - numpy.pi) < 1e-10), 'Evaluating Orbits phi does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.x(itimes)[ii]-list_os[ii].x(itimes)) < 1e-10), 'Evaluating Orbits x does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.y(itimes)[ii]-list_os[ii].y(itimes)) < 1e-10), 'Evaluating Orbits y does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vx(itimes)[ii]-list_os[ii].vx(itimes)) < 1e-10), 'Evaluating Orbits vx does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vy(itimes)[ii]-list_os[ii].vy(itimes)) < 1e-10), 'Evaluating Orbits vy does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vphi(itimes)[ii]-list_os[ii].vphi(itimes)) < 1e-10), 'Evaluating Orbits vphidoes not agree with Orbit'
        assert numpy.all(numpy.fabs(os.ra(itimes)[ii]-list_os[ii].ra(itimes)) < 1e-10), 'Evaluating Orbits ra  does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.dec(itimes)[ii]-list_os[ii].dec(itimes)) < 1e-10), 'Evaluating Orbits dec does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.dist(itimes)[ii]-list_os[ii].dist(itimes)) < 1e-10), 'Evaluating Orbits dist does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.ll(itimes)[ii]-list_os[ii].ll(itimes)) < 1e-10), 'Evaluating Orbits ll does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.bb(itimes)[ii]-list_os[ii].bb(itimes)) < 1e-10), 'Evaluating Orbits bb  does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmra(itimes)[ii]-list_os[ii].pmra(itimes)) < 1e-10), 'Evaluating Orbits pmra does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmdec(itimes)[ii]-list_os[ii].pmdec(itimes)) < 1e-10), 'Evaluating Orbits pmdec does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmll(itimes)[ii]-list_os[ii].pmll(itimes)) < 1e-10), 'Evaluating Orbits ll does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmbb(itimes)[ii]-list_os[ii].pmbb(itimes)) < 1e-10), 'Evaluating Orbits pmbb does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vlos(itimes)[ii]-list_os[ii].vlos(itimes)) < 1e-10), 'Evaluating Orbits vlos does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioX(itimes)[ii]-list_os[ii].helioX(itimes)) < 1e-10), 'Evaluating Orbits helioX does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioY(itimes)[ii]-list_os[ii].helioY(itimes)) < 1e-10), 'Evaluating Orbits helioY does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioZ(itimes)[ii]-list_os[ii].helioZ(itimes)) < 1e-10), 'Evaluating Orbits helioZ does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.U(itimes)[ii]-list_os[ii].U(itimes)) < 1e-10), 'Evaluating Orbits U does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.V(itimes)[ii]-list_os[ii].V(itimes)) < 1e-10), 'Evaluating Orbits V does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.W(itimes)[ii]-list_os[ii].W(itimes)) < 1e-10), 'Evaluating Orbits W does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord(itimes).ra[ii]-list_os[ii].SkyCoord(itimes).ra).to(u.deg).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord(itimes).dec[ii]-list_os[ii].SkyCoord(itimes).dec).to(u.deg).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord(itimes).distance[ii]-list_os[ii].SkyCoord(itimes).distance).to(u.kpc).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        if _APY3:
            assert numpy.all(numpy.fabs(os.SkyCoord(itimes).pm_ra_cosdec[ii]-list_os[ii].SkyCoord(itimes).pm_ra_cosdec).to(u.mas/u.yr).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
            assert numpy.all(numpy.fabs(os.SkyCoord(itimes).pm_dec[ii]-list_os[ii].SkyCoord(itimes).pm_dec).to(u.mas/u.yr).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
            assert numpy.all(numpy.fabs(os.SkyCoord(itimes).radial_velocity[ii]-list_os[ii].SkyCoord(itimes).radial_velocity).to(u.km/u.s).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        # Also a single time in the array ...
        assert numpy.all(numpy.fabs(os.R(itimes[1])[ii]-list_os[ii].R(itimes[1])) < 1e-10), 'Evaluating Orbits R does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.r(itimes[1])[ii]-list_os[ii].r(itimes[1])) < 1e-10), 'Evaluating Orbits r does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vR(itimes[1])[ii]-list_os[ii].vR(itimes[1])) < 1e-10), 'Evaluating Orbits vR does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vT(itimes[1])[ii]-list_os[ii].vT(itimes[1])) < 1e-10), 'Evaluating Orbits vT does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.z(itimes[1])[ii]-list_os[ii].z(itimes[1])) < 1e-10), 'Evaluating Orbits z does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vz(itimes[1])[ii]-list_os[ii].vz(itimes[1])) < 1e-10), 'Evaluating Orbits vz does not agree with Orbit'
        assert numpy.all(numpy.fabs(((os.phi(itimes[1])[ii]-list_os[ii].phi(itimes[1])+numpy.pi) % (2.*numpy.pi)) - numpy.pi) < 1e-10), 'Evaluating Orbits phi does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.ra(itimes[1])[ii]-list_os[ii].ra(itimes[1])) < 1e-10), 'Evaluating Orbits ra  does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.dec(itimes[1])[ii]-list_os[ii].dec(itimes[1])) < 1e-10), 'Evaluating Orbits dec does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.dist(itimes[1])[ii]-list_os[ii].dist(itimes[1])) < 1e-10), 'Evaluating Orbits dist does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.ll(itimes[1])[ii]-list_os[ii].ll(itimes[1])) < 1e-10), 'Evaluating Orbits ll does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.bb(itimes[1])[ii]-list_os[ii].bb(itimes[1])) < 1e-10), 'Evaluating Orbits bb  does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmra(itimes[1])[ii]-list_os[ii].pmra(itimes[1])) < 1e-10), 'Evaluating Orbits pmra does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmdec(itimes[1])[ii]-list_os[ii].pmdec(itimes[1])) < 1e-10), 'Evaluating Orbits pmdec does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmll(itimes[1])[ii]-list_os[ii].pmll(itimes[1])) < 1e-10), 'Evaluating Orbits ll does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.pmbb(itimes[1])[ii]-list_os[ii].pmbb(itimes[1])) < 1e-10), 'Evaluating Orbits pmbb does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vlos(itimes[1])[ii]-list_os[ii].vlos(itimes[1])) < 1e-10), 'Evaluating Orbits vlos does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioX(itimes[1])[ii]-list_os[ii].helioX(itimes[1])) < 1e-10), 'Evaluating Orbits helioX does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioY(itimes[1])[ii]-list_os[ii].helioY(itimes[1])) < 1e-10), 'Evaluating Orbits helioY does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.helioZ(itimes[1])[ii]-list_os[ii].helioZ(itimes[1])) < 1e-10), 'Evaluating Orbits helioZ does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.U(itimes[1])[ii]-list_os[ii].U(itimes[1])) < 1e-10), 'Evaluating Orbits U does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.V(itimes[1])[ii]-list_os[ii].V(itimes[1])) < 1e-10), 'Evaluating Orbits V does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.W(itimes[1])[ii]-list_os[ii].W(itimes[1])) < 1e-10), 'Evaluating Orbits W does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord(itimes[1]).ra[ii]-list_os[ii].SkyCoord(itimes[1]).ra).to(u.deg).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord(itimes[1]).dec[ii]-list_os[ii].SkyCoord(itimes[1]).dec).to(u.deg).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.SkyCoord(itimes[1]).distance[ii]-list_os[ii].SkyCoord(itimes[1]).distance).to(u.kpc).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
        if _APY3:
            assert numpy.all(numpy.fabs(os.SkyCoord(itimes[1]).pm_ra_cosdec[ii]-list_os[ii].SkyCoord(itimes[1]).pm_ra_cosdec).to(u.mas/u.yr).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
            assert numpy.all(numpy.fabs(os.SkyCoord(itimes[1]).pm_dec[ii]-list_os[ii].SkyCoord(itimes[1]).pm_dec).to(u.mas/u.yr).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
            assert numpy.all(numpy.fabs(os.SkyCoord(itimes[1]).radial_velocity[ii]-list_os[ii].SkyCoord(itimes[1]).radial_velocity).to(u.km/u.s).value < 1e-10), 'Evaluating Orbits SkyCoord does not agree with Orbit'
    return None

# Test that evaluating coordinate functions for integrated orbits works, 
# for 5D orbits
def test_coordinate_interpolation_5d():
    from galpy.orbit import Orbit, Orbits
    from galpy.potential import MWPotential2014
    numpy.random.seed(1)
    nrand= 20
    Rs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)+1.
    vRs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)
    vTs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)+1.
    zs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)
    vzs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)
    os= Orbits(list(zip(Rs,vRs,vTs,zs,vzs)))
    list_os= [Orbit([R,vR,vT,z,vz])
              for R,vR,vT,z,vz in zip(Rs,vRs,vTs,zs,vzs)]
    # Before integration
    for ii in range(nrand):
        assert numpy.all(numpy.fabs(os.R()[ii]-list_os[ii].R()) < 1e-10), 'Evaluating Orbits R does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.r()[ii]-list_os[ii].r()) < 1e-10), 'Evaluating Orbits r does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vR()[ii]-list_os[ii].vR()) < 1e-10), 'Evaluating Orbits vR does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vT()[ii]-list_os[ii].vT()) < 1e-10), 'Evaluating Orbits vT does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.z()[ii]-list_os[ii].z()) < 1e-10), 'Evaluating Orbits z does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vz()[ii]-list_os[ii].vz()) < 1e-10), 'Evaluating Orbits vz does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vphi()[ii]-list_os[ii].vphi()) < 1e-10), 'Evaluating Orbits vphi does not agree with Orbit'
    # Integrate all
    times= numpy.linspace(0.,10.,1001)
    os.integrate(times,MWPotential2014)
    [o.integrate(times,MWPotential2014) for o in list_os]
    # Test exact times of integration
    for ii in range(nrand):
        assert numpy.all(numpy.fabs(os.R(times)[ii]-list_os[ii].R(times)) < 1e-10), 'Evaluating Orbits R does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.r(times)[ii]-list_os[ii].r(times)) < 1e-10), 'Evaluating Orbits r does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vR(times)[ii]-list_os[ii].vR(times)) < 1e-10), 'Evaluating Orbits vR does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vT(times)[ii]-list_os[ii].vT(times)) < 1e-10), 'Evaluating Orbits vT does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.z(times)[ii]-list_os[ii].z(times)) < 1e-10), 'Evaluating Orbits z does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vz(times)[ii]-list_os[ii].vz(times)) < 1e-10), 'Evaluating Orbits vz does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vphi(times)[ii]-list_os[ii].vphi(times)) < 1e-10), 'Evaluating Orbits vphi does not agree with Orbit'
        # Also a single time in the array ...
        assert numpy.all(numpy.fabs(os.R(times[1])[ii]-list_os[ii].R(times[1])) < 1e-10), 'Evaluating Orbits R does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.r(times[1])[ii]-list_os[ii].r(times[1])) < 1e-10), 'Evaluating Orbits r does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vR(times[1])[ii]-list_os[ii].vR(times[1])) < 1e-10), 'Evaluating Orbits vR does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vT(times[1])[ii]-list_os[ii].vT(times[1])) < 1e-10), 'Evaluating Orbits vT does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.z(times[1])[ii]-list_os[ii].z(times[1])) < 1e-10), 'Evaluating Orbits z does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vz(times[1])[ii]-list_os[ii].vz(times[1])) < 1e-10), 'Evaluating Orbits vz does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vphi(times[1])[ii]-list_os[ii].vphi(times[1])) < 1e-10), 'Evaluating Orbits vphi does not agree with Orbit'
    # Test actual interpolated
    itimes= times[:-2]+(times[1]-times[0])/2.
    for ii in range(nrand):
        assert numpy.all(numpy.fabs(os.R(itimes)[ii]-list_os[ii].R(itimes)) < 1e-10), 'Evaluating Orbits R does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.r(itimes)[ii]-list_os[ii].r(itimes)) < 1e-10), 'Evaluating Orbits r does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vR(itimes)[ii]-list_os[ii].vR(itimes)) < 1e-10), 'Evaluating Orbits vR does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vT(itimes)[ii]-list_os[ii].vT(itimes)) < 1e-10), 'Evaluating Orbits vT does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.z(itimes)[ii]-list_os[ii].z(itimes)) < 1e-10), 'Evaluating Orbits z does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vz(itimes)[ii]-list_os[ii].vz(itimes)) < 1e-10), 'Evaluating Orbits vz does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vphi(itimes)[ii]-list_os[ii].vphi(itimes)) < 1e-10), 'Evaluating Orbits vphi does not agree with Orbit'
        # Also a single time in the array ...
        assert numpy.all(numpy.fabs(os.R(itimes[1])[ii]-list_os[ii].R(itimes[1])) < 1e-10), 'Evaluating Orbits R does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.r(itimes[1])[ii]-list_os[ii].r(itimes[1])) < 1e-10), 'Evaluating Orbits r does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vR(itimes[1])[ii]-list_os[ii].vR(itimes[1])) < 1e-10), 'Evaluating Orbits vR does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vT(itimes[1])[ii]-list_os[ii].vT(itimes[1])) < 1e-10), 'Evaluating Orbits vT does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.z(itimes[1])[ii]-list_os[ii].z(itimes[1])) < 1e-10), 'Evaluating Orbits z does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vz(itimes[1])[ii]-list_os[ii].vz(itimes[1])) < 1e-10), 'Evaluating Orbits vz does not agree with Orbit'
        assert numpy.all(numpy.fabs(os.vphi(itimes[1])[ii]-list_os[ii].vphi(itimes[1])) < 1e-10), 'Evaluating Orbits vphi does not agree with Orbit'
    return None

# Test interpolation with backwards orbit integration
def test_backinterpolation():
    from galpy.orbit import Orbit, Orbits
    from galpy.potential import MWPotential2014
    numpy.random.seed(1)
    nrand= 20
    Rs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)+1.
    vRs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)
    vTs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)+1.
    zs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)
    vzs= 0.2*(2.*numpy.random.uniform(size=nrand)-1.)
    phis= 2.*numpy.pi*(2.*numpy.random.uniform(size=nrand)-1.)
    os= Orbits(list(zip(Rs,vRs,vTs,zs,vzs,phis)))
    list_os= [Orbit([R,vR,vT,z,vz,phi])
              for R,vR,vT,z,vz,phi in zip(Rs,vRs,vTs,zs,vzs,phis)]
    # Integrate all
    times= numpy.linspace(0.,-10.,1001)
    os.integrate(times,MWPotential2014)
    [o.integrate(times,MWPotential2014) for o in list_os]
    # Test actual interpolated
    itimes= times[:-2]+(times[1]-times[0])/2.
    for ii in range(nrand):
        assert numpy.all(numpy.fabs(os.R(itimes)[ii]-list_os[ii].R(itimes)) < 1e-10), 'Evaluating Orbits R does not agree with Orbit'
        # Also a single time in the array ...
        assert numpy.all(numpy.fabs(os.R(itimes[1])[ii]-list_os[ii].R(itimes[1])) < 1e-10), 'Evaluating Orbits R does not agree with Orbit'
    return None

def test_call_issue256():
    # Same as for Orbit instances: non-integrated orbit with t=/=0 should return eror
    from galpy.orbit import Orbits
    o = Orbits(vxvv=[[5.,-1.,0.8, 3, -0.1, 0]])
    # no integration of the orbit
    with pytest.raises(ValueError) as excinfo:
        o.R(30)
    return None

# Test that we can still get outputs when there aren't enough points for an actual interpolation
# Test whether Orbits evaluation methods sound warning when called with
# unitless time when orbit is integrated with unitfull times
def test_orbits_method_integrate_t_asQuantity_warning():
    from galpy.potential import MWPotential2014
    from galpy.orbit import Orbits
    from astropy import units
    from test_orbit import check_integrate_t_asQuantity_warning
    # Setup and integrate orbit
    ts= numpy.linspace(0.,10.,1001)*units.Gyr
    o= Orbits([[1.1,0.1,1.1,0.1,0.1,0.2],
               [1.1,0.1,1.1,0.1,0.1,0.2]])
    o.integrate(ts,MWPotential2014)
    # Now check
    check_integrate_t_asQuantity_warning(o,'R')
    return None

# Check plotting routines
def test_plotting():
    from galpy.orbit import Orbit, Orbits
    from galpy.potential import LogarithmicHaloPotential
    o= Orbits([Orbit([1.,0.1,1.1,0.1,0.2,2.]),Orbit([1.,0.1,1.1,0.1,0.2,2.])])
    times= numpy.linspace(0.,7.,251)
    lp= LogarithmicHaloPotential(normalize=1.,q=0.8)
    # Integrate
    o.integrate(times,lp)
    # Some plots
    o.plotE()
    # Plot the orbit itself
    o.plot() #defaults
    o.plot(d1='vR')
    o.plotR()
    o.plotvR(d1='vT')
    o.plotvT(d1='z')
    o.plotz(d1='vz')
    return None

def test_integrate_method_warning():
    """ Test Orbits.integrate raises an error if method is unvalid """
    from galpy.potential import MWPotential2014
    from galpy.orbit import Orbit, Orbits
    o = Orbits([Orbit(vxvv=[1.0, 0.1, 0.1, 0.5, 0.1, 0.0]),
                Orbit(vxvv=[1.0, 0.1, 0.1, 0.5, 0.1, 0.0])])
    t = numpy.arange(0.0, 10.0, 0.001)
    with pytest.raises(ValueError):
        o.integrate(t, MWPotential2014, method='rk4')

# Test that fallback onto Python integrators works for Orbits
def test_integrate_Cfallback_symplec():
    from test_potential import BurkertPotentialNoC
    from galpy.orbit import Orbit, Orbits
    times= numpy.linspace(0.,10.,1001)
    orbits_list= [Orbit([1.,0.1,1.]),Orbit([.9,0.3,1.]),
                  Orbit([1.2,-0.3,0.7])]
    orbits= Orbits(orbits_list)
    # Integrate as Orbits
    pot= BurkertPotentialNoC()
    pot.normalize(1.)
    orbits.integrate(times,pot,method='symplec4_c')
    # Integrate as multiple Orbits
    for o in orbits_list:
        o.integrate(times,pot,method='symplec4_c')
    # Compare
    for ii in range(len(orbits)):
        assert numpy.amax(numpy.fabs(orbits_list[ii].R(times)-orbits.R(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vR(times)-orbits.vR(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vT(times)-orbits.vT(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    return None
    
def test_integrate_Cfallback_nonsymplec():
    from test_potential import BurkertPotentialNoC
    from galpy.orbit import Orbit, Orbits
    times= numpy.linspace(0.,10.,1001)
    orbits_list= [Orbit([1.,0.1,1.]),Orbit([.9,0.3,1.]),
                  Orbit([1.2,-0.3,0.7])]
    orbits= Orbits(orbits_list)
    # Integrate as Orbits
    pot= BurkertPotentialNoC()
    pot.normalize(1.)
    orbits.integrate(times,pot,method='dop853_c')
    # Integrate as multiple Orbits
    for o in orbits_list:
        o.integrate(times,pot,method='dop853_c')
    # Compare
    for ii in range(len(orbits)):
        assert numpy.amax(numpy.fabs(orbits_list[ii].R(times)-orbits.R(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vR(times)-orbits.vR(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
        assert numpy.amax(numpy.fabs(orbits_list[ii].vT(times)-orbits.vT(times)[ii])) < 1e-10, 'Integration of multiple orbits as Orbits does not agree with integrating multiple orbits'
    return None
    
@pytest.mark.xfail(sys.platform != 'win32',strict=True,raises=ValueError,
                   reason="Does not fail on Windows...")
def test_ChandrasekharDynamicalFrictionForce_constLambda():
    # Test from test_potential for Orbits now! Currently fails because Chandra
    # can't be pickled for parallel_map...
    #
    # Test that the ChandrasekharDynamicalFrictionForce with constant Lambda
    # agrees with analytical solutions for circular orbits:
    # assuming that a mass remains on a circular orbit in an isothermal halo 
    # with velocity dispersion sigma and for constant Lambda:
    # r_final^2 - r_initial^2 = -0.604 ln(Lambda) GM/sigma t 
    # (e.g., B&T08, p. 648)
    from galpy.util import bovy_conversion
    from galpy.orbit import Orbit, Orbits
    ro,vo= 8.,220.
    # Parameters
    GMs= 10.**9./bovy_conversion.mass_in_msol(vo,ro)
    const_lnLambda= 7.
    r_inits= [2.,2.5]
    dt= 2./bovy_conversion.time_in_Gyr(vo,ro)
    # Compute
    lp= potential.LogarithmicHaloPotential(normalize=1.,q=1.)
    cdfc= potential.ChandrasekharDynamicalFrictionForce(\
        GMs=GMs,const_lnLambda=const_lnLambda,
        dens=lp) # don't provide sigmar, so it gets computed using galpy.df.jeans
    o= Orbits([Orbit([r_inits[0],0.,1.,0.,0.,0.]),
               Orbit([r_inits[1],0.,1.,0.,0.,0.])])
    ts= numpy.linspace(0.,dt,1001)
    o.integrate(ts,[lp,cdfc],method='odeint')
    r_pred= numpy.sqrt(numpy.array(o.r())**2.
                       -0.604*const_lnLambda*GMs*numpy.sqrt(2.)*dt)
    assert numpy.all(numpy.fabs(r_pred-numpy.array(o.r(ts[-1]))) < 0.015), 'ChandrasekharDynamicalFrictionForce with constant lnLambda for circular orbits does not agree with analytical prediction'
    return None

def test_error_handling():
    # Only run this for astropy>3
    if not _APY3: return None
    from galpy.orbit import Orbits
    ras = numpy.array([1., 2., 3.]) * u.deg
    decs = numpy.array([1., 2., 3.]) * u.deg
    dists = numpy.array([1., 2., 3.]) * u.kpc
    pmras = numpy.array([1., 2000., 3.]) * u.mas / u.yr  # second one high velocity unbound orbit
    pmdecs = numpy.array([1., 2000., 3.]) * u.mas / u.yr  # second one high velocity unbound orbit
    vloss = numpy.array([1., 2., 3.]) * u.km / u.s
    # Without any custom coordinate-transformation parameters
    co = apycoords.SkyCoord(ra=ras, dec=decs, distance=dists,
                            pm_ra_cosdec=pmras, pm_dec=pmdecs,
                            radial_velocity=vloss,
                            frame='icrs')
    os = Orbits(co)

    e = os.e(analytic=True, type='staeckel', pot=potential.MWPotential2014)
    # assert all orbits e estimation are finished and the second high velocity one is NaN
    assert numpy.isnan(e[1])

###############################################################################
#   TriaxialGaussianPotential.py: Potential of a triaxial Gaussian stratified
#                                 on similar ellipsoids
#
#                                 \rho(x,y,z) ~ exp(-m^2/[2\sigma^2])
#
#                                 with m^2 = x^2+y^2/b^2+z^2/c^2
#
###############################################################################
import numpy
from .Potential import _APY_LOADED
from .EllipsoidalPotential import EllipsoidalPotential
if _APY_LOADED:
    from astropy import units
class TriaxialGaussianPotential(EllipsoidalPotential):
    """Potential of a triaxial Gaussian (`Emsellem et al. 1994 <https://ui.adsabs.harvard.edu/abs/1994A%26A...285..723E/abstract>`__):

    .. math::

        \\rho(x,y,z) = \\frac{\\mathrm{amp}}{(2\\pi\\,\\sigma)^{3/2}\\,b\\,c}\,e^{-\\frac{m^2}{2\\sigma^2}}

    where :math:`\\mathrm{amp} = GM` is the total mass and :math:`m^2 = x^2+y^2/b^2+z^2/c^2`.
    """
    def __init__(self,amp=1.,sigma=5.,b=1.,c=1.,
                 zvec=None,pa=None,glorder=50,
                 normalize=False,ro=None,vo=None):
        """
        NAME:

           __init__

        PURPOSE:

           initialize a Gaussian potential

        INPUT:

           amp - amplitude to be applied to the potential (default: 1); can be a Quantity with units of mass or Gxmass

           sigma - Gaussian dispersion scale (can be Quantity)

           b - y-to-x axis ratio of the density

           c - z-to-x axis ratio of the density

           zvec= (None) If set, a unit vector that corresponds to the z axis

           pa= (None) If set, the position angle of the x axis (rad or Quantity)

           glorder= (50) if set, compute the relevant force and potential integrals with Gaussian quadrature of this order

           ro=, vo= distance and velocity scales for translation into internal units (default from configuration file)

        OUTPUT:

           (none)

        HISTORY:

           2020-08-18 - Started - Bovy (UofT)

        """
        EllipsoidalPotential.__init__(self,amp=amp,b=b,c=c,
                                      zvec=zvec,pa=pa,glorder=glorder,
                                      ro=ro,vo=vo,amp_units='mass')
        if _APY_LOADED and isinstance(sigma,units.Quantity):
            sigma= sigma.to_value(units.kpc)/self._ro
        self._sigma= sigma
        self._twosigma2= 2.*self._sigma**2
        self._scale= self._sigma
        # Adjust amp
        self._amp/= (2.*numpy.pi)**1.5*self._sigma**3.*self._b*self._c
        if normalize or \
                (isinstance(normalize,(int,float)) \
                     and not isinstance(normalize,bool)): #pragma: no cover
            self.normalize(normalize)
        self.hasC= not self._glorder is None
        self.hasC_dxdv= False
        self.hasC_dens= self.hasC # works if mdens is defined, necessary for hasC
        return None

    def _psi(self,m):
        """\psi(m) = -\int_m^\infty d m^2 \rho(m^2)"""
        return -self._twosigma2*numpy.exp(-m**2./self._twosigma2)

    def _mdens(self,m):
        """Density as a function of m"""
        return numpy.exp(-m**2/self._twosigma2)

    def _mdens_deriv(self,m):
        """Derivative of the density as a function of m"""
        return -2.*m*numpy.exp(-m**2/self._twosigma2)/self._twosigma2

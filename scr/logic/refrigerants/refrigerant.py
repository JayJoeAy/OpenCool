# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Abstraction layer for CoolProp library
"""

import CoolProp as Cp
import logging as log
from scr.logic.errors import RefrigerantLibraryError


class Refrigerant:
    DENSITY = Cp.iDmass
    ENTROPY = Cp.iSmass
    QUALITY = Cp.iQ
    ENTHALPY = Cp.iHmass
    PRESSURE = Cp.iP
    TEMPERATURE = Cp.iT

    # If is not specify, all units in SI.
    def __init__(self, backend: str, refrigerant: str) -> None:
        self._ref = Cp.AbstractState(backend, refrigerant)

    @staticmethod
    def build(backend: str, refrigerant: str) -> 'Refrigerant':
        # FIXME: Need use the coolprop information and the refrigerants plugins register the supported library.
        if backend == 'CoolPropHeos':
            return Refrigerant('HEOS', refrigerant)
        else:
            msg = f"Error loading refrigerant library. {backend} is not found"
            log.error(msg)
            raise RefrigerantLibraryError(msg)

    def _update(self, property_type_1, property_1, property_type_2, property_2):
        input_keys = Cp.CoolProp.generate_update_pair(property_type_1, property_1, property_type_2, property_2)
        self._ref.update(input_keys[0], input_keys[1], input_keys[2])

    def T(self, property_type_1: int, property_1: float, property_type_2: int, property_2: float) -> float:
        """Temperature in Kelvin."""
        self._update(property_type_1, property_1, property_type_2, property_2)
        return self._ref.T()

    def p(self, property_type_1: int, property_1: float, property_type_2: int, property_2: float) -> float:
        """Absolute pressure un Pascals."""
        self._update(property_type_1, property_1, property_type_2, property_2)
        return self._ref.p()

    def h(self, property_type_1: int, property_1: float, property_type_2: int, property_2: float) -> float:
        """Enthalpy in J/kg."""
        self._update(property_type_1, property_1, property_type_2, property_2)
        return self._ref.hmass()

    def d(self, property_type_1: int, property_1: float, property_type_2: int, property_2: float) -> float:
        """Density in kg/m3."""
        self._update(property_type_1, property_1, property_type_2, property_2)
        return self._ref.rhomass()

    def s(self, property_type_1: int, property_1: float, property_type_2: int, property_2: float) -> float:
        """Return entropy in J/kg·K."""
        self._update(property_type_1, property_1, property_type_2, property_2)
        return self._ref.smass()

    def Q(self, property_type_1: int, property_1: float, property_type_2: int, property_2: float) -> float:
        """Vapor quality; 0 = saturated liquid, 1 = saturated vapour, <0 if one phase."""
        self._update(property_type_1, property_1, property_type_2, property_2)
        return self._ref.Q()

    def T_crit(self) -> float:
        """Critical temperature in Kelvin."""
        return self._ref.T_critical()

    def p_crit(self) -> float:
        """Critical pressure in Pascals."""
        return self._ref.p_critical()

    def T_sat(self, pressure: float, Q: float=1.0) -> float:
        """Saturation temperature in Kelvin."""
        self._ref.update(Cp.PQ_INPUTS, pressure, Q)
        return self._ref.T()

    def p_sat(self, temperature: float, Q: float=1.0) -> float:
        """Saturation pressure in Pascals."""
        self._ref.update(Cp.QT_INPUTS, Q, temperature)
        return self._ref.p()

    def name(self) -> str:
        return self._ref.name()

    # Refrigerant property limits. If there are no limit, return None.
    # FIXME Coolprop 6.1.0 doesn't support check all limits. All not supported, are harcorded
    def Tmin(self) -> float:
        """Minimum temperature in Kelvin allowed by the library."""
        return self._ref.Tmin()

    def Tmax(self) -> float:
        """Maximum temperature in Kelvin allowed by the library."""
        return self._ref.Tmax()

    def pmin(self) -> float:
        """Minimum pressure in Pascals allowed by the library."""
        return 0.0

    def pmax(self) -> float:
        """Maximum pressure in Pascals allowed by the library."""
        return self._ref.pmax()

    def dmin(self) -> float:
        """Minimum density in kg/m3 allowed by the library."""
        return 0.0

    def dmax(self) -> None:
        """Maximum density in kg/m3 allowed by the library."""
        return None

    def hmin(self) -> float:
        """Minimum enthalpy in J/kg allowed by the library."""
        return 0.0

    def hmax(self) -> None:
        """Maximum enthalpy in J/kg allowed by the library."""
        return None

    def smin(self) -> float:
        """Minimum entropy in J/kg·K allowed by the library."""
        return 0.0

    def smax(self) -> None:
        """Maximum entropy in J/kg·K allowed by the library."""
        return None

    def Qmin(self) -> float:
        """Minimum vapor quality allowed by the library."""
        return 0.0

    def Qmax(self) -> float:
        """Maximum vapor quality by the library."""
        return 1.0

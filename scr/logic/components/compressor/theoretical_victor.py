# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Define the Compressor component.
"""
from math import inf

from scr.logic.components.component import Component as Cmp
from scr.logic.components.component import ComponentInfo as CmpInfo
from scr.logic.components.component import component, basic_property, auxiliary_property
from scr.logic.refrigerants.refrigerant import Refrigerant

from scr.helpers.properties import NumericProperty


def update_saved_data_to_last_version(orig_data, orig_version):
    # Here will be the code to update to update saved data to current format
    return orig_data


@component('theoretical_compressor', CmpInfo.COMPRESSOR, 1, update_saved_data_to_last_version)
class Theoretical_victor(Cmp):

    def __init__(self, id_, inlet_nodes_id, outlet_nodes_id, component_data):
        super().__init__(id_, inlet_nodes_id, outlet_nodes_id, component_data)

    """ Fundamental properties equations """

    """ Basic properties equations """
    # @basic_property(name of basic property = value type)
    # Name must be only one word
    @basic_property(isentropic_efficiency=NumericProperty(0, 1))
    def _eval_eq_isentropic_effiency(self):
        id_inlet_node = list(self.get_id_inlet_nodes())[0]
        inlet_node = self.get_inlet_node(id_inlet_node)
        id_outlet_node = list(self.get_id_outlet_nodes())[0]
        outlet_node = self.get_outlet_node(id_outlet_node)

        h_in = inlet_node.enthalpy()
        s_in = inlet_node.entropy()
        h_out = outlet_node.enthalpy()
        p_out = outlet_node.pressure()
        ref = outlet_node.get_refrigerant()
        h_is = ref.h(Refrigerant.PRESSURE, p_out, Refrigerant.ENTROPY, s_in)
        return (h_is - h_in) / (h_out - h_in)

    @basic_property(power_consumption=NumericProperty(0, 1))
    def _eval_eq_power_consumption(self):
        id_inlet_node = list(self.get_id_inlet_nodes())[0]
        inlet_node = self.get_inlet_node(id_inlet_node)
        id_outlet_node = list(self.get_id_outlet_nodes())[0]
        outlet_node = self.get_outlet_node(id_outlet_node)

        h_in = inlet_node.enthalpy()
        h_out = outlet_node.enthalpy()
        mass_flow = h_out.mass_flow()
        return mass_flow * (h_out - h_in) / 1000.0

    ### Auxiliary properties equations ###
    @auxiliary_property(displacement_volume=NumericProperty(0, inf))
    def _eval_eq_displacement_volume(self):
        id_inlet_node = list(self.get_id_inlet_nodes())[0]
        inlet_node = self.get_inlet_node(id_inlet_node)
        id_outlet_node = list(self.get_id_outlet_nodes())[0]
        outlet_node = self.get_outlet_node(id_outlet_node)

        mass_flow = inlet_node.mass_flow()
        density = inlet_node.density()
        # Remember, magics has happpened and all static
        # attributes have been transformed to instance attributes
        # and primitive types ;)
        return mass_flow * density / self.displacement_volume

    @auxiliary_property(volumetric_efficiency=NumericProperty(0, 1))
    def _eval_eq_volumetric_efficiency(self):
        id_inlet_node = list(self.get_id_inlet_nodes())[0]
        inlet_node = self.get_inlet_node(id_inlet_node)
        id_outlet_node = list(self.get_id_outlet_nodes())[0]
        outlet_node = self.get_outlet_node(id_outlet_node)

        mass_flow = inlet_node.mass_flow()
        density = inlet_node.density()
        # Remember, magics has happpened and all static
        # attributes have been transformed to instance attributes
        # and primitive types ;)
        return mass_flow * density / self.volumetric_efficiency

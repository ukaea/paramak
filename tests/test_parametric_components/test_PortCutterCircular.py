
import unittest

import paramak


class test_component(unittest.TestCase):

    def setUp(self):
        self.test_shape = paramak.PortCutterCircular(
            distance=300, radius=20
        )

    def test_default_parameters(self):
        """Checks that the default parameters of a PortCutterCircular are correct."""

        assert self.center_point == (0, 0)
        assert self.workplane == "ZY"
        assert self.rotation_axis == "Z"
        assert self.extrusion_start_offset == 1
        assert self.stp_filename == "PortCutterCircular.stp"
        assert self.stl_filename == "PortCutterCircular.stl"
        assert self.name == "circular_port_cutter"
        assert self.material_tag == "circular_port_cutter_mat"

    def test_creation(self):
        """Creates a circular port cutter using the PortCutterCircular parametric
        component and checks that a cadquery solid is created."""

        assert self.test_shape.solid is not None
        assert self.test_shape.volume > 1000 

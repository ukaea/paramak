
import unittest

import paramak


class TestPortCutterRectangular(unittest.TestCase):

    def setUp(self):
        self.test_shape = paramak.PortCutterRectangular(
            width=40, height=40, distance=300
        )

    def test_default_parameters(self):
        """Checks that the default parameters of a PortCutterRectangular are correct."""

        assert self.center_point = (0, 0)
        assert self.workplane = "ZY"
        assert self.rotation_axis == "Z"
        assert self.extrusion_start_offset == 1
        assert self.stp_filename == "PortCutterRectangular.stp"
        assert self.stl_filename == "PortCutterRectangular.stl"
        assert self.name == "rectangular_port_cutter"
        assert self.material_tag == "rectangular_port_cutter_mat"

    def test_creation(self):
        """Creates a rectangular port cutter using the PortCutterRectangular parametric
        component and checks that a cadquery solid is created."""

        assert self.test_shape.solid is not None
        assert self.test_shape.volume > 1000

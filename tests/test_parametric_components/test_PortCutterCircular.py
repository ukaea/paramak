
import unittest

import paramak


class test_component(unittest.TestCase):

    def test_creation(self):
        """Checks a PortCutterCircular creation."""

        test_component = paramak.PortCutterCircular(
            center_point=(0, 0),
            distance=3,
            radius=0.1,
            extrusion_start_offset=1,
            azimuth_placement_angle=[0, 45, 90, 180]
        )

        assert test_component.solid is not None

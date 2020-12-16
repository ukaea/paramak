
import unittest

import pytest
from paramak import ExtrudeSplineShape


class TestExtrudeSplineShape(unittest.TestCase):

    def setUp(self):
        self.test_shape = ExtrudeSplineShape(
            points=[(50, 0), (50, 20), (70, 80), (90, 50), (70, 0), (90, -50),
                    (70, -80), (50, -20)], distance=30
        )

    def test_default_parameters(self):
        """Checks that the default parameters of an ExtrudeSplineShape are correct."""

        assert self.test_shape.rotation_angle == 360
        assert self.test_shape.stp_filename == "ExtrudeSplineShape.stp"
        assert self.test_shape.stl_filename == "ExtrudeSplineShape.stl"
        assert self.test_shape.extrude_both

    def test_absolute_shape_volume(self):
        """Creates an ExtrudeSplineShape and checks that the volume is correct."""

        assert self.test_shape.solid is not None
        assert self.test_shape.volume > 20 * 20 * 30

    def test_shape_face_areas(self):
        """Creates an ExtrudeSplineShape and checks that the face areas are expected."""

        self.test_shape.extrude_both = False
        assert len(self.test_shape.areas) == 3
        assert len(set([round(i) for i in self.test_shape.areas])) == 2

    def test_relative_shape_volume(self):
        """Creates two ExtrudeSplineShapes and checks that their relative volumes
        are correct."""

        test_volume = self.test_shape.volume
        self.test_shape.azimuth_placement_angle = [0, 180]

        assert self.test_shape.volume == pytest.approx(
            test_volume * 2, rel=0.01)

    def test_cut_volume(self):
        """Creates an ExtrudeSplineShape with another ExtrudeSplineShape cut out
        and checks that the volume is correct."""

        inner_shape = ExtrudeSplineShape(
            points=[(5, 5), (5, 10), (10, 10), (10, 5)], distance=30
        )

        outer_shape = ExtrudeSplineShape(
            points=[(3, 3), (3, 12), (12, 12), (12, 3)], distance=30
        )

        outer_shape_with_cut = ExtrudeSplineShape(
            points=[(3, 3), (3, 12), (12, 12), (12, 3)], cut=inner_shape,
            distance=30,
        )

        assert inner_shape.volume == pytest.approx(1165, abs=2)
        assert outer_shape.volume == pytest.approx(3775, abs=2)
        assert outer_shape_with_cut.volume == pytest.approx(3775 - 1165, abs=2)

    def test_rotation_angle(self):
        """Creates an ExtrudeStraightShape with a rotation_angle < 360 and checks that
        the correct cut is performed and the volume is correct."""

        self.test_shape.azimuth_placement_angle = [45, 135, 225, 315]
        test_volume = self.test_shape.volume
        self.test_shape.rotation_angle = 180
        assert self.test_shape.volume == pytest.approx(
            test_volume * 0.5, rel=0.01)

    def test_extrude_both(self):
        """Creates an ExtrudeSplineShape with extrude_both = True and False and checks
        that the volumes are correct."""

        test_volume_extrude_both = self.test_shape.volume
        self.test_shape.extrude_both = False
        assert self.test_shape.volume == pytest.approx(
            test_volume_extrude_both)


if __name__ == "__main__":
    unittest.main()

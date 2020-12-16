
import math
import os
import unittest
from pathlib import Path

import pytest
from paramak import RotateStraightShape


class TestRotateStraightShape(unittest.TestCase):

    def setUp(self):
        self.test_shape = RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20), (20, 0)]
        )

    def test_largest_dimension(self):
        """Checks that the largest_dimension is correct."""

        assert self.test_shape.largest_dimension == 20

    def test_default_parameters(self):
        """Checks that the default parameters of a RotateStraightShape are correct."""

        assert self.test_shape.rotation_angle == 360
        assert self.test_shape.stp_filename == "RotateStraightShape.stp"
        assert self.test_shape.stl_filename == "RotateStraightShape.stl"
        assert self.test_shape.azimuth_placement_angle == 0

    def test_rotation_angle_getting_setting(self):
        """Checks that the rotation_angle of a RotateStraightShape can be changed."""

        assert self.test_shape.rotation_angle == 360
        self.test_shape.rotation_angle = 180
        assert self.test_shape.rotation_angle == 180

    def test_absolute_shape_volume(self):
        """Creates a RotateStraightShape and checks that its volume is correct."""

        assert self.test_shape.solid is not None
        assert self.test_shape.volume == pytest.approx(math.pi * (20**2) * 20)

    def test_relative_shape_volume(self):
        """Creates two RotateStraightShapes and checks that their relative volumes
        are correct."""

        test_volume = self.test_shape.volume
        self.test_shape.rotation_angle = 180
        assert test_volume == pytest.approx(self.test_shape.volume * 2)

    def test_union_volume_addition(self):
        """Fuses two RotateStraightShapes and checks that their fused volume is
        correct."""

        inner_box = RotateStraightShape(
            points=[(100, 100), (100, 200), (200, 200), (200, 100)],
        )

        outer_box = RotateStraightShape(
            points=[(200, 100), (200, 200), (500, 200), (500, 100)],
        )

        outer_box_and_inner_box = RotateStraightShape(
            points=[(200, 100), (200, 200), (500, 200), (500, 100)],
            union=inner_box,
        )

        assert inner_box.volume + outer_box.volume == pytest.approx(
            outer_box_and_inner_box.volume, rel=0.01
        )

    def test_absolute_shape_areas(self):
        """Creates RotateStraightShapes and checks that the areas of each face
        are correct."""

        assert self.test_shape.area == pytest.approx(
            (math.pi * (20**2) * 2) + (math.pi * (20 * 2) * 20))
        assert len(self.test_shape.areas) == 3
        assert self.test_shape.areas.count(
            pytest.approx(math.pi * (20**2))) == 2
        assert self.test_shape.areas.count(
            pytest.approx(math.pi * (20 * 2) * 20)) == 1

        self.test_shape.rotation_angle = 180
        assert self.test_shape.area == pytest.approx(
            ((math.pi * (20**2) / 2) * 2) + (20 * 40) + (math.pi * (20 * 2) * 20 / 2))
        assert len(self.test_shape.areas) == 4
        assert self.test_shape.areas.count(
            pytest.approx(math.pi * (20**2) / 2)) == 2
        assert self.test_shape.areas.count(pytest.approx(20 * 40)) == 1
        assert self.test_shape.areas.count(
            pytest.approx((math.pi * (20 * 2) * 20) / 2)) == 1

        test_shape = RotateStraightShape(
            points=[(50, 0), (50, 50), (70, 50), (70, 0)],
        )

        assert test_shape.area == pytest.approx(
            (((math.pi * (70**2)) - (math.pi * (50**2))) * 2) + (math.pi * (50 * 2) * 50) + (math.pi * (70 * 2) * 50))
        assert len(test_shape.areas) == 4
        assert test_shape.areas.count(pytest.approx(
            (math.pi * (70**2)) - (math.pi * (50**2)))) == 2
        assert test_shape.areas.count(
            pytest.approx(math.pi * (50 * 2) * 50)) == 1
        assert test_shape.areas.count(
            pytest.approx(math.pi * (70 * 2) * 50)) == 1

        test_shape.rotation_angle = 180
        assert test_shape.area == pytest.approx((20 * 50 * 2) + ((((math.pi * (70**2)) / 2) - (
            (math.pi * (50**2)) / 2)) * 2) + ((math.pi * (50 * 2) * 50) / 2) + ((math.pi * (70 * 2) * 50) / 2))
        assert len(test_shape.areas) == 6
        assert test_shape.areas.count(pytest.approx(20 * 50)) == 2
        assert test_shape.areas.count(pytest.approx(
            ((math.pi * (70**2)) / 2) - ((math.pi * (50**2)) / 2))) == 2
        assert test_shape.areas.count(
            pytest.approx(math.pi * (50 * 2) * 50 / 2)) == 1
        assert test_shape.areas.count(
            pytest.approx(math.pi * (70 * 2) * 50 / 2)) == 1

    def test_export_stp(self):
        """Creates a RotateStraightShape and checks that a stp file of the
        shape can be exported with the correct suffix using the export_stp
        method."""

        os.system("rm filename.stp filename.step")
        self.test_shape.export_stp("filename.stp")
        self.test_shape.export_stp("filename.step")
        assert Path("filename.stp").exists() is True
        assert Path("filename.step").exists() is True
        os.system("rm filename.stp filename.step")
        self.test_shape.export_stp("filename")
        assert Path("filename.stp").exists() is True
        os.system("rm filename.stp")
        self.test_shape.export_stp()
        assert Path("RotateStraightShape.stp").exists() is True
        os.system("rm RotateStraightShape.stp")

    def test_export_stl(self):
        """Creates a RotateStraightShape and checks that a stl file of the
        shape can be exported with the correct suffix using the export_stl
        method."""

        os.system("rm filename.stl")
        self.test_shape.export_stl("filename.stl")
        assert Path("filename.stl").exists() is True
        os.system("rm filename.stl")
        self.test_shape.export_stl("filename")
        assert Path("filename.stl").exists() is True
        os.system("rm filename.stl")

    def test_export_svg(self):
        """Creates a RotateStraightShape and checks that a svg file of the
        shape can be exported with the correct suffix using the export_svg
        method."""

        os.system("rm filename.svg")
        self.test_shape.export_svg("filename.svg")
        assert Path("filename.svg").exists() is True
        os.system("rm filename.svg")
        self.test_shape.export_svg("filename")
        assert Path("filename.svg").exists() is True
        os.system("rm filename.svg")

    def test_cut_volume(self):
        """Creates a RotateStraightShape with another RotateStraightShape
        cut out and checks that the volume is correct."""

        shape_with_cut = RotateStraightShape(
            points=[(0, -5), (0, 25), (25, 25), (25, -5)],
            cut=self.test_shape
        )

        assert shape_with_cut.volume == pytest.approx(
            (math.pi * (25**2) * 30) - (math.pi * (20**2) * 20)
        )

    def test_multiple_cut_volume(self):
        """Creates a RotateStraightShape with multiple RotateStraightShapes
        cut out and checks that the volume is correct."""

        main_shape = RotateStraightShape(
            points=[(0, 0), (0, 200), (200, 200), (200, 0)],
        )

        shape_to_cut_1 = RotateStraightShape(
            points=[(20, 0), (20, 200), (40, 200), (40, 0)],
        )

        shape_to_cut_2 = RotateStraightShape(
            points=[(120, 0), (120, 200), (140, 200), (140, 0)],
        )

        main_shape_with_cuts = RotateStraightShape(
            points=[(0, 0), (0, 200), (200, 200), (200, 0)],
            cut=[shape_to_cut_1, shape_to_cut_2]
        )

        assert main_shape_with_cuts.volume == pytest.approx(
            (math.pi * (200**2) * 200) -
            ((math.pi * (40**2) * 200) - (math.pi * (20**2) * 200)) -
            ((math.pi * (140**2) * 200) - (math.pi * (120**2) * 200))
        )

    def test_hash_value(self):
        """Creates a RotateStraightShape and checks that a cadquery solid with
        a unique has value is created when .solid is called. Checks that the same
        solid is returned when .solid is called again after no changes have been
        made to the shape. Checks that a new solid with a new unique has is
        constructed when .solid is called after changes to the shape have been
        made. Checks that the hash_value of the shape is not updated until a new
        solid has been constructed."""

        assert self.test_shape.hash_value is None
        assert self.test_shape.solid is not None
        assert self.test_shape.hash_value is not None
        initial_hash_value = self.test_shape.hash_value
        assert self.test_shape.solid is not None
        assert initial_hash_value == self.test_shape.hash_value
        self.test_shape.rotation_angle = 180
        assert initial_hash_value == self.test_shape.hash_value
        assert self.test_shape.solid is not None
        assert initial_hash_value != self.test_shape.hash_value


if __name__ == "__main__":
    unittest.main()

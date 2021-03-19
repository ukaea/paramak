
import json
import os
import unittest
from pathlib import Path

import cadquery as cq
import paramak
import pytest


class TestReactor(unittest.TestCase):

    def setUp(self):
        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])

        self.test_reactor = paramak.Reactor([test_shape])

    def test_incorrect_merge_tolerance_too_small(self):

        def incorrect_merge_tolerance_too_small():
            """Set merge_tolerance as a negative number which should raise an error"""

            self.test_reactor.merge_tolerance = -3

        self.assertRaises(
            ValueError,
            incorrect_merge_tolerance_too_small
        )

    def test_incorrect_faceting_tolerance_too_small(self):

        def incorrect_faceting_tolerance_too_small():
            """Set faceting_tolerance as a negative int which should raise an error"""

            self.test_reactor.faceting_tolerance = -3

        self.assertRaises(
            ValueError,
            incorrect_faceting_tolerance_too_small
        )

    def test_merge_tolerance_setting_and_getting(self):
        """Makes a neutronics model and checks the default merge_tolerance"""

        assert self.test_reactor.merge_tolerance == 1e-4

        self.test_reactor.merge_tolerance = 1e-6
        assert self.test_reactor.merge_tolerance == 1e-6

    def test_incorrect_methods_settings(self):
        """Creates NeutronicsModel objects and checks errors are
        raised correctly when arguments are incorrect."""

        def test_incorrect_method():
            """Tries to make a h5m with an inccorect method which should return
            a ValueError"""

            self.test_reactor.export_h5m(
                method='incorrect')

        self.assertRaises(ValueError, test_incorrect_method)

    def test_adding_shape_with_material_tag_to_reactor(self):
        """Checks that a shape object can be added to a Reactor object with
        the correct material tag property."""

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)], material_tag="mat1"
        )
        test_shape.rotation_angle = 360
        test_shape.create_solid()
        test_reactor = paramak.Reactor([test_shape])
        assert len(test_reactor.material_tags()) == 1
        assert test_reactor.material_tags()[0] == "mat1"

    def test_adding_multiple_shapes_with_material_tag_to_reactor(self):
        """Checks that multiple shape objects can be added to a Reactor object
        with the correct material tag properties."""

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)], material_tag="mat1"
        )
        test_shape2 = paramak.RotateSplineShape(
            points=[(0, 0), (0, 20), (20, 20)], material_tag="mat2"
        )
        test_shape.rotation_angle = 360
        test_shape.create_solid()
        test_reactor = paramak.Reactor([test_shape, test_shape2])
        assert len(test_reactor.material_tags()) == 2
        assert "mat1" in test_reactor.material_tags()
        assert "mat2" in test_reactor.material_tags()

    def test_adding_shape_with_stp_filename_to_reactor(self):
        """Checks that a shape object can be added to a Reactor object with the
        correct stp filename property."""

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)], stp_filename="filename.stp"
        )
        test_shape.rotation_angle = 360
        test_shape.create_solid()
        test_reactor = paramak.Reactor([test_shape])
        assert len(test_reactor.stp_filenames) == 1
        assert test_reactor.stp_filenames[0] == "filename.stp"

    def test_adding_multiple_shape_with_stp_filename_to_reactor(self):
        """Checks that multiple shape objects can be added to a Reactor object
        with the correct stp filename properties."""

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)], stp_filename="filename.stp"
        )
        test_shape2 = paramak.RotateSplineShape(
            points=[(0, 0), (0, 20), (20, 20)], stp_filename="filename2.stp"
        )
        test_shape.rotation_angle = 360
        test_shape.create_solid()
        test_reactor = paramak.Reactor([test_shape, test_shape2])
        assert len(test_reactor.stp_filenames) == 2
        assert test_reactor.stp_filenames[0] == "filename.stp"
        assert test_reactor.stp_filenames[1] == "filename2.stp"

    def test_adding_shape_with_duplicate_stp_filename_to_reactor(self):
        """Adds shapes to a Reactor object to check errors are raised
        correctly."""

        def test_stp_filename_duplication():
            """Checks ValueError is raised when shapes with the same stp
            filenames are added to a reactor object"""

            test_shape_1 = paramak.RotateStraightShape(
                points=[(0, 0), (0, 20), (20, 20)], stp_filename="filename.stp"
            )
            test_shape_2 = paramak.RotateSplineShape(
                points=[(0, 0), (0, 20), (20, 20)], stp_filename="filename.stp"
            )
            test_shape_1.rotation_angle = 90
            my_reactor = paramak.Reactor([test_shape_1, test_shape_2])
            my_reactor.export_stp()

        self.assertRaises(ValueError, test_stp_filename_duplication)

    def test_adding_shape_with_None_stp_filename_to_reactor(self):
        """adds shapes to a Reactor object to check errors are raised correctly"""

        def test_stp_filename_None():
            """checks ValueError is raised when RotateStraightShapes with duplicate
            stp filenames are added"""

            test_shape = paramak.RotateStraightShape(
                points=[(0, 0), (0, 20), (20, 20)], stp_filename="filename.stp"
            )
            test_shape2 = paramak.RotateSplineShape(
                points=[(0, 0), (0, 20), (20, 20)], stp_filename=None
            )
            test_shape.create_solid()
            my_reactor = paramak.Reactor([test_shape, test_shape2])
            my_reactor.export_stp()

        self.assertRaises(ValueError, test_stp_filename_None)

    def test_adding_shape_with_duplicate_stl_filename_to_reactor(self):
        """Adds shapes to a Reactor object to checks errors are raised
        correctly"""

        def test_stl_filename_duplication():
            """Checks ValueError is raised when shapes with the same stl
            filenames are added to a reactor object"""

            test_shape_1 = paramak.RotateStraightShape(
                points=[(0, 0), (0, 20), (20, 20)], stl_filename="filename.stl"
            )
            test_shape_2 = paramak.RotateSplineShape(
                points=[(0, 0), (0, 20), (20, 20)], stl_filename="filename.stl"
            )
            test_shape_1.rotation_angle = 90
            my_reactor = paramak.Reactor([test_shape_1, test_shape_2])
            my_reactor.export_stl()

        self.assertRaises(ValueError, test_stl_filename_duplication)

    def test_adding_shape_with_the_same_default_stl_filename_to_reactor(self):
        """Adds shapes to a Reactor object to check errors are raised
        correctly."""

        def test_stl_filename_duplication_rotate_straight():
            """checks ValueError is raised when RotateStraightShapes with
            duplicate stl filenames (defaults) are added"""

            test_shape = paramak.RotateStraightShape(
                points=[(0, 0), (0, 20), (20, 20)])
            test_shape2 = paramak.RotateStraightShape(
                points=[(0, 0), (0, 20), (20, 20)])
            test_shape.rotation_angle = 360
            test_shape.create_solid()
            my_reactor = paramak.Reactor([test_shape, test_shape2])
            my_reactor.export_stl()

        self.assertRaises(
            ValueError,
            test_stl_filename_duplication_rotate_straight)

        def test_stl_filename_duplication_rotate_spline():
            """Checks ValueError is raised when RotateSplineShapes with
            duplicate stl filenames are added."""

            test_shape = paramak.RotateSplineShape(
                points=[(0, 0), (0, 20), (20, 20)], stl_filename="filename.stl"
            )
            test_shape2 = paramak.RotateSplineShape(
                points=[(0, 0), (0, 20), (20, 20)], stl_filename="filename.stl"
            )
            test_shape.rotation_angle = 360
            test_shape.create_solid()
            my_reactor = paramak.Reactor([test_shape, test_shape2])
            my_reactor.export_stl()

        self.assertRaises(
            ValueError,
            test_stl_filename_duplication_rotate_spline)

        def test_stl_filename_duplication_rotate_mixed():
            """Checks ValueError is raised when RotateMixedShapes with
            duplicate stl filenames are added."""

            test_shape = paramak.RotateMixedShape(
                points=[(0, 0, "straight"), (0, 20, "straight"), (20, 20, "straight")],
                stl_filename="filename.stl",
            )
            test_shape2 = paramak.RotateMixedShape(
                points=[(0, 0, "straight"), (0, 20, "straight"), (20, 20, "straight")],
                stl_filename="filename.stl",
            )
            test_shape.rotation_angle = 360
            test_shape.create_solid()
            my_reactor = paramak.Reactor([test_shape, test_shape2])
            my_reactor.export_stl()

        self.assertRaises(
            ValueError,
            test_stl_filename_duplication_rotate_mixed)

        def test_stl_filename_duplication_Rotate_Circle():
            """Checks ValueError is raised when RotateCircleShapes with
            duplicate stl filenames are added."""

            test_shape = paramak.RotateCircleShape(
                points=[(20, 20)],
                radius=10,
                rotation_angle=180,
                stl_filename="filename.stl",
            )
            test_shape2 = paramak.RotateCircleShape(
                points=[(20, 20)],
                radius=10,
                rotation_angle=180,
                stl_filename="filename.stl",
            )
            test_shape.rotation_angle = 360
            test_shape.create_solid()
            my_reactor = paramak.Reactor([test_shape, test_shape2])
            my_reactor.export_stl()

        self.assertRaises(
            ValueError,
            test_stl_filename_duplication_Rotate_Circle)

        def test_stl_filename_duplication_Extrude_straight():
            """Checks ValueError is raised when ExtrudeStraightShapes with
            duplicate stl filenames are added."""

            test_shape = paramak.ExtrudeStraightShape(
                points=[(0, 0), (0, 20), (20, 20)],
                distance=10,
                stl_filename="filename.stl",
            )
            test_shape2 = paramak.ExtrudeStraightShape(
                points=[(0, 0), (0, 20), (20, 20)],
                distance=10,
                stl_filename="filename.stl",
            )
            test_shape.rotation_angle = 360
            test_shape.create_solid()
            my_reactor = paramak.Reactor([test_shape, test_shape2])
            my_reactor.export_stl()

        self.assertRaises(
            ValueError,
            test_stl_filename_duplication_Extrude_straight)

        def test_stl_filename_duplication_Extrude_spline():
            """Checks ValueError is raised when ExtrudeSplineShapes with
            duplicate stl filenames are added."""

            test_shape = paramak.ExtrudeSplineShape(
                points=[(0, 0), (0, 20), (20, 20)],
                distance=10,
                stl_filename="filename.stl",
            )
            test_shape2 = paramak.ExtrudeSplineShape(
                points=[(0, 0), (0, 20), (20, 20)],
                distance=10,
                stl_filename="filename.stl",
            )
            test_shape.rotation_angle = 360
            test_shape.create_solid()
            my_reactor = paramak.Reactor([test_shape, test_shape2])
            my_reactor.export_stl()

        self.assertRaises(
            ValueError,
            test_stl_filename_duplication_Extrude_spline)

        def test_stl_filename_duplication_Extrude_mixed():
            """checks ValueError is raised when ExtrudeMixedShapes with duplicate
            stl filenames are added"""

            test_shape = paramak.ExtrudeMixedShape(
                points=[(0, 0, "straight"), (0, 20, "straight"), (20, 20, "straight")],
                distance=10,
                stl_filename="filename.stl",
            )
            test_shape2 = paramak.ExtrudeMixedShape(
                points=[(0, 0, "straight"), (0, 20, "straight"), (20, 20, "straight")],
                distance=10,
                stl_filename="filename.stl",
            )
            test_shape.rotation_angle = 360
            test_shape.create_solid()
            my_reactor = paramak.Reactor([test_shape, test_shape2])
            my_reactor.export_stl()

        self.assertRaises(
            ValueError,
            test_stl_filename_duplication_Extrude_mixed)

        def test_stl_filename_duplication_Extrude_Circle():
            """checks ValueError is raised when ExtrudeCircleShapes with duplicate
            stl filenames are added"""

            test_shape = paramak.ExtrudeCircleShape(
                points=[(20, 20)], radius=10, distance=10, stl_filename="filename.stl"
            )
            test_shape2 = paramak.ExtrudeCircleShape(
                points=[(20, 20)], radius=10, distance=10, stl_filename="filename.stl"
            )
            test_shape.rotation_angle = 360
            test_shape.create_solid()
            my_reactor = paramak.Reactor([test_shape, test_shape2])
            my_reactor.export_stl()

        self.assertRaises(
            ValueError,
            test_stl_filename_duplication_Extrude_Circle)

        def test_stl_filename_None():
            test_shape = paramak.ExtrudeCircleShape(
                points=[(20, 20)], radius=10, distance=10, stl_filename=None
            )
            my_reactor = paramak.Reactor([test_shape])
            my_reactor.export_stl()

        self.assertRaises(
            ValueError,
            test_stl_filename_None)

    def test_reactor_creation_with_default_properties(self):
        """creates a Reactor object and checks that it has no default properties"""

        test_reactor = paramak.Reactor([])

        assert test_reactor is not None

    def test_adding_component_to_reactor(self):
        """creates a Reactor object and checks that shapes can be added to it"""

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        test_shape.create_solid()
        test_reactor = paramak.Reactor([])
        assert len(test_reactor.shapes_and_components) == 0
        test_reactor = paramak.Reactor([test_shape])
        assert len(test_reactor.shapes_and_components) == 1

    def test_graveyard_exists(self):
        """creates a Reactor object with one shape and checks that a graveyard
        can be produced using the make_graveyard method"""

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        test_shape.create_solid()
        test_reactor = paramak.Reactor([test_shape])
        test_reactor.make_graveyard()

        assert isinstance(test_reactor.graveyard, paramak.Shape)

    def test_graveyard_exists_solid_is_none(self):
        """creates a Reactor object with one shape and checks that a graveyard
        can be produced using the make_graveyard method when the solid
        attribute of the shape is None"""

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        test_shape.create_solid()
        test_reactor = paramak.Reactor([test_shape])
        test_reactor.shapes_and_components[0].solid = None
        test_reactor.make_graveyard()

        assert isinstance(test_reactor.graveyard, paramak.Shape)

    def test_export_graveyard(self):
        """creates a Reactor object with one shape and checks that a graveyard
        can be exported to a specified location using the make_graveyard method"""

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        os.system("rm my_graveyard.stp")
        os.system("rm graveyard.stp")
        test_shape.stp_filename = "test_shape.stp"
        test_reactor = paramak.Reactor([test_shape])

        test_reactor.export_stp_graveyard()
        test_reactor.export_stp_graveyard(filename="my_graveyard.stp")

        for filepath in ["graveyard.stp", "my_graveyard.stp"]:
            assert Path(filepath).exists() is True
            os.system("rm " + filepath)

        assert test_reactor.graveyard is not None
        assert test_reactor.graveyard.__class__.__name__ == "HollowCube"

    def test_make_graveyard_offset(self):
        """checks that the graveyard can be exported with the correct default parameters
        and that these parameters can be changed"""

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        os.system("rm graveyard.stp")
        test_reactor = paramak.Reactor(
            [test_shape],
            graveyard_size=None,
            graveyard_offset=100)
        test_reactor.make_graveyard()
        # assert test_reactor.graveyard_offset == 100
        graveyard_volume_1 = test_reactor.graveyard.volume

        test_reactor.make_graveyard(graveyard_offset=50)
        assert test_reactor.graveyard.volume < graveyard_volume_1
        graveyard_volume_2 = test_reactor.graveyard.volume

        test_reactor.make_graveyard(graveyard_offset=200)
        assert test_reactor.graveyard.volume > graveyard_volume_1
        assert test_reactor.graveyard.volume > graveyard_volume_2

    def test_exported_stp_files_exist(self):
        """creates a Reactor object with one shape and checks that a stp file
        of the reactor can be exported to a specified location using the export_stp
        method"""

        os.system("rm test_reactor/*.stp")
        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360

        os.system("rm test_reactor/test_shape.stp")
        os.system("rm test_reactor/graveyard.stp")

        test_shape.stp_filename = "test_shape.stp"
        test_reactor = paramak.Reactor([test_shape])

        test_reactor.export_stp(output_folder="test_reactor")

        assert Path("test_reactor/test_shape.stp").exists() is True
        assert Path("test_reactor/graveyard.stp").exists() is True

    def test_exported_stl_files_exist(self):
        """creates a Reactor object with one shape and checks that a stl file
        of the reactor can be exported to a specified location using the
        export_stl method"""

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        os.system("rm test_reactor/test_shape.stl")
        os.system("rm test_reactor/graveyard.stl")
        test_shape.stl_filename = "test_shape.stl"
        test_reactor = paramak.Reactor([test_shape])

        test_reactor.export_stl(output_folder="test_reactor")

        for filepath in [
            "test_reactor/test_shape.stl",
                "test_reactor/graveyard.stl"]:
            assert Path(filepath).exists() is True
            os.system("rm " + filepath)

    def test_exported_svg_files_exist(self):
        """Creates a Reactor object with one shape and checks that a svg file
        of the reactor can be exported to a specified location using the
        export_svg method."""

        os.system("rm test_svg_image.svg")

        self.test_reactor.export_svg("test_svg_image.svg")

        assert Path("test_svg_image.svg").exists() is True
        os.system("rm test_svg_image.svg")

    def test_exported_svg_files_exist_no_extension(self):
        """creates a Reactor object with one shape and checks that an svg file
        of the reactor can be exported to a specified location using the export_svg
        method"""

        os.system("rm test_svg_image.svg")

        self.test_reactor.export_svg("test_svg_image")

        assert Path("test_svg_image.svg").exists() is True
        os.system("rm test_svg_image.svg")

    def test_export_svg_options(self):
        """Exports the test reacto to an svg image and checks that a svg file
        can be exported with the various different export options"""

        os.system("rm *.svg")
        self.test_reactor.export_svg("r_width.svg", width=900)
        assert Path("r_width.svg").exists() is True
        self.test_reactor.export_svg("r_height.svg", height=900)
        assert Path("r_height.svg").exists() is True
        self.test_reactor.export_svg("r_marginLeft.svg", marginLeft=110)
        assert Path("r_marginLeft.svg").exists() is True
        self.test_reactor.export_svg("r_marginTop.svg", marginTop=110)
        assert Path("r_marginTop.svg").exists() is True
        self.test_reactor.export_svg("r_showAxes.svg", showAxes=True)
        assert Path("r_showAxes.svg").exists() is True
        self.test_reactor.export_svg(
            "r_projectionDir.svg", projectionDir=(-1, -1, -1))
        assert Path("r_projectionDir.svg").exists() is True
        self.test_reactor.export_svg(
            "r_strokeColor.svg", strokeColor=(
                42, 42, 42))
        assert Path("r_strokeColor.svg").exists() is True
        self.test_reactor.export_svg(
            "r_hiddenColor.svg", hiddenColor=(
                42, 42, 42))
        assert Path("r_hiddenColor.svg").exists() is True
        self.test_reactor.export_svg("r_showHidden.svg", showHidden=False)
        assert Path("r_showHidden.svg").exists() is True
        self.test_reactor.export_svg("r_strokeWidth1.svg", strokeWidth=None)
        assert Path("r_strokeWidth1.svg").exists() is True
        self.test_reactor.export_svg("r_strokeWidth2.svg", strokeWidth=10)
        assert Path("r_strokeWidth2.svg").exists() is True

    def test_neutronics_description(self):
        """Creates reactor objects to check errors are raised correctly when
        exporting the neutronics description."""

        def test_neutronics_description_without_material_tag():
            """Checks ValueError is raised when the neutronics description is
            exported without material_tag."""

            test_shape = paramak.RotateStraightShape(
                points=[(0, 0), (0, 20), (20, 20)])
            test_shape.rotation_angle = 360
            test_shape.stp_filename = "test.stp"
            test_reactor = paramak.Reactor([test_shape])
            test_reactor.neutronics_description()

        self.assertRaises(
            ValueError,
            test_neutronics_description_without_material_tag)

        def test_neutronics_description_without_stp_filename():
            """Checks ValueError is raised when the neutronics description is
            exported without stp_filename."""

            test_shape = paramak.RotateStraightShape(
                points=[(0, 0), (0, 20), (20, 20)])
            test_shape.rotation_angle = 360
            test_shape.material_tag = "test_material"
            test_shape.stp_filename = None
            test_reactor = paramak.Reactor([test_shape])
            test_reactor.neutronics_description()

        self.assertRaises(
            ValueError,
            test_neutronics_description_without_stp_filename)

    def test_neutronics_description_without_plasma(self):
        """Creates a Reactor object and checks that the neutronics description
        is exported with the correct material_tag and stp_filename."""

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        test_shape.material_tag = "test_material"
        test_shape.stp_filename = "test.stp"
        test_reactor = paramak.Reactor([test_shape])
        neutronics_description = test_reactor.neutronics_description()

        assert len(neutronics_description) == 2
        assert "stp_filename" in neutronics_description[0].keys()
        assert "material_tag" in neutronics_description[0].keys()
        assert neutronics_description[0]["material_tag"] == "test_material"
        assert neutronics_description[0]["stp_filename"] == "test.stp"
        assert neutronics_description[1]["material_tag"] == "graveyard"
        assert neutronics_description[1]["stp_filename"] == "graveyard.stp"

    def test_export_neutronics_description(self):
        """Creates a Reactor object and checks that the neutronics description
        is exported to a json file with the correct material_name and
        stp_filename."""

        os.system("rm manifest_test.json")

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        test_shape.material_tag = "test_material"
        test_shape.stp_filename = "test.stp"
        test_shape.tet_mesh = "size 60"
        test_reactor = paramak.Reactor([test_shape])
        returned_filename = test_reactor.export_neutronics_description(
            filename="manifest_test.json"
        )
        with open("manifest_test.json") as json_file:
            neutronics_description = json.load(json_file)

        assert returned_filename == "manifest_test.json"
        assert Path("manifest_test.json").exists() is True
        assert len(neutronics_description) == 2
        assert "stp_filename" in neutronics_description[0].keys()
        assert "material_tag" in neutronics_description[0].keys()
        assert "tet_mesh" in neutronics_description[0].keys()
        assert neutronics_description[0]["material_tag"] == "test_material"
        assert neutronics_description[0]["stp_filename"] == "test.stp"
        assert neutronics_description[0]["tet_mesh"] == "size 60"
        assert neutronics_description[1]["material_tag"] == "graveyard"
        assert neutronics_description[1]["stp_filename"] == "graveyard.stp"
        os.system("rm manifest_test.json")

    def test_export_neutronics_description_with_sector_wedge(self):
        """Creates a Reactor object and checks that the neutronics description
        is exported to a json file with the correct entries, including the
        optional plasma."""

        os.system("rm manifest_test.json")

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)],
            rotation_angle=360,
            material_tag="test_material",
            stp_filename="test.stp",
        )

        test_plasma = paramak.Plasma(
            major_radius=500,
            minor_radius=100,
            stp_filename="plasma.stp",
            material_tag="DT_plasma",
        )
        test_reactor = paramak.Reactor([test_shape, test_plasma])

        test_reactor.rotation_angle = 270

        returned_filename = test_reactor.export_neutronics_description(
            include_plasma=False, include_sector_wedge=True, include_graveyard=False)
        with open("manifest.json") as json_file:
            neutronics_description = json.load(json_file)
        print(neutronics_description)
        assert returned_filename == "manifest.json"
        assert Path("manifest.json").exists() is True
        assert len(neutronics_description) == 2

        assert neutronics_description[0]["material_tag"] == "test_material"
        assert neutronics_description[0]["stp_filename"] == "test.stp"
        assert neutronics_description[1]["material_tag"] == "cutting_slice_mat"
        assert neutronics_description[1]["stp_filename"] == "sector_wedge.stp"
        assert neutronics_description[1]["surface_reflectivity"] is True
        assert neutronics_description[1]["stl_filename"] == "sector_wedge.stl"

        os.system("rm manifest.json")

    def test_export_neutronics_description_without_sector_wedge(self):
        """Creates a Reactor object and checks that the neutronics description is
        exported to a json file with the correct entires, exluding the optional
        plasma."""

        os.system("rm manifest_test.json")

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)],
            rotation_angle=360,
            material_tag="test_material",
            stp_filename="test.stp",
        )

        test_plasma = paramak.Plasma(major_radius=500, minor_radius=100)
        test_reactor = paramak.Reactor([test_shape, test_plasma])

        returned_filename = test_reactor.export_neutronics_description(
            include_plasma=False, include_sector_wedge=False, include_graveyard=False)
        with open("manifest.json") as json_file:
            neutronics_description = json.load(json_file)

        assert returned_filename == "manifest.json"
        assert Path("manifest.json").exists() is True
        assert len(neutronics_description) == 1

        assert neutronics_description[0]["material_tag"] == "test_material"
        assert neutronics_description[0]["stp_filename"] == "test.stp"

        os.system("rm manifest.json")

    def test_export_neutronics_description_with_plasma(self):
        """Creates a Reactor object and checks that the neutronics description
        is exported to a json file with the correct entries, including the
        optional plasma."""

        os.system("rm manifest_test.json")

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)],
            rotation_angle=360,
            material_tag="test_material",
            stp_filename="test.stp",
        )
        test_shape.tet_mesh = "size 60"
        test_plasma = paramak.Plasma(
            major_radius=500,
            minor_radius=100,
            stp_filename="plasma.stp",
            material_tag="DT_plasma",
        )
        test_reactor = paramak.Reactor([test_shape, test_plasma])
        returned_filename = test_reactor.export_neutronics_description(
            include_plasma=True, include_graveyard=True, include_sector_wedge=False)
        with open("manifest.json") as json_file:
            neutronics_description = json.load(json_file)

        assert returned_filename == "manifest.json"
        assert Path("manifest.json").exists() is True
        assert len(neutronics_description) == 3
        assert "stp_filename" in neutronics_description[0].keys()
        assert "material_tag" in neutronics_description[0].keys()
        assert "tet_mesh" in neutronics_description[0].keys()
        assert "stp_filename" in neutronics_description[1].keys()
        assert "material_tag" in neutronics_description[1].keys()
        assert "tet_mesh" not in neutronics_description[1].keys()
        assert neutronics_description[0]["material_tag"] == "test_material"
        assert neutronics_description[0]["stp_filename"] == "test.stp"
        assert neutronics_description[0]["tet_mesh"] == "size 60"
        assert neutronics_description[1]["material_tag"] == "DT_plasma"
        assert neutronics_description[1]["stp_filename"] == "plasma.stp"
        assert neutronics_description[2]["material_tag"] == "graveyard"
        assert neutronics_description[2]["stp_filename"] == "graveyard.stp"
        os.system("rm manifest.json")

    def test_export_neutronics_description_without_plasma(self):
        """Creates a Reactor object and checks that the neutronics description is
        exported to a json file with the correct entires, exluding the optional
        plasma."""

        os.system("rm manifest_test.json")

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)],
            rotation_angle=360,
            material_tag="test_material",
            stp_filename="test.stp",
        )
        test_shape.tet_mesh = "size 60"
        test_plasma = paramak.Plasma(major_radius=500, minor_radius=100)
        test_reactor = paramak.Reactor([test_shape, test_plasma])
        returned_filename = test_reactor.export_neutronics_description()
        with open("manifest.json") as json_file:
            neutronics_description = json.load(json_file)

        assert returned_filename == "manifest.json"
        assert Path("manifest.json").exists() is True
        assert len(neutronics_description) == 2
        assert "stp_filename" in neutronics_description[0].keys()
        assert "material_tag" in neutronics_description[0].keys()
        assert "tet_mesh" in neutronics_description[0].keys()
        assert neutronics_description[0]["material_tag"] == "test_material"
        assert neutronics_description[0]["stp_filename"] == "test.stp"
        assert neutronics_description[0]["tet_mesh"] == "size 60"
        assert neutronics_description[1]["material_tag"] == "graveyard"
        assert neutronics_description[1]["stp_filename"] == "graveyard.stp"
        os.system("rm manifest.json")

    def test_export_neutronics_without_extension(self):
        """checks a json file is created if filename has no extension"""

        os.system("rm manifest_test.json")
        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        test_shape.material_tag = "test_material"
        test_shape.stp_filename = "test.stp"
        test_shape.tet_mesh = "size 60"
        test_reactor = paramak.Reactor([test_shape])
        returned_filename = test_reactor.export_neutronics_description(
            filename="manifest_test"
        )
        assert returned_filename == "manifest_test.json"
        assert Path("manifest_test.json").exists() is True
        os.system("rm manifest_test.json")

    def test_export_2d_image(self):
        """Creates a Reactor object and checks that a png file of the reactor
        with the correct filename can be exported using the export_2D_image
        method."""

        os.system("rm 2D_test_image.png")
        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        test_reactor = paramak.Reactor([test_shape])
        returned_filename = test_reactor.export_2d_image(
            filename="2D_test_image.png")

        assert Path(returned_filename).exists() is True
        os.system("rm 2D_test_image.png")

    def test_export_2d_image_without_extension(self):
        """creates a Reactor object and checks that a png file of the reactor
        with the correct filename can be exported using the export_2d_image
        method"""

        os.system("rm 2d_test_image.png")
        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        test_reactor = paramak.Reactor([test_shape])
        returned_filename = test_reactor.export_2d_image(
            filename="2d_test_image")

        assert Path(returned_filename).exists() is True
        os.system("rm 2d_test_image.png")

    def test_export_html(self):
        """Creates a Reactor object and checks that a html file of the reactor
        with the correct filename can be exported using the export_html
        method."""

        os.system("rm test_html.html")
        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        test_reactor = paramak.Reactor([test_shape])
        test_reactor.export_html(filename="test_html.html")

        assert Path("test_html.html").exists() is True
        os.system("rm test_html.html")
        test_reactor.export_html(filename="test_html")

        assert Path("test_html.html").exists() is True
        os.system("rm test_html.html")

    def test_tet_meshes_error(self):
        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        test_reactor = paramak.Reactor([test_shape])
        assert test_reactor.tet_meshes is not None

    def test_largest_dimention(self):
        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_shape.rotation_angle = 360
        test_reactor = paramak.Reactor([test_shape])
        assert pytest.approx(test_reactor.largest_dimension, rel=0.1 == 20)
        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (30, 20)])
        test_shape.rotation_angle = 360
        test_reactor = paramak.Reactor([test_shape])
        assert pytest.approx(test_reactor.largest_dimension, rel=0.1 == 30)

    def test_shapes_and_components(self):
        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])

        def incorrect_shapes_and_components():
            paramak.Reactor(test_shape)
        self.assertRaises(ValueError, incorrect_shapes_and_components)

    def test_graveyard_error(self):
        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        test_reactor = paramak.Reactor([test_shape])

        def str_graveyard_offset():
            test_reactor.graveyard_offset = 'coucou'
        self.assertRaises(TypeError, str_graveyard_offset)

        def negative_graveyard_offset():
            test_reactor.graveyard_offset = -2
        self.assertRaises(ValueError, negative_graveyard_offset)

        def list_graveyard_offset():
            test_reactor.graveyard_offset = [1.2]
        self.assertRaises(TypeError, list_graveyard_offset)

    def test_compound_in_shapes(self):
        shape1 = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        shape2 = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20)])
        shape3 = paramak.Shape()
        shape3.solid = cq.Compound.makeCompound(
            [a.val() for a in [shape1.solid, shape2.solid]]
        )
        test_reactor = paramak.Reactor([shape3])
        assert test_reactor.solid is not None

    def test_adding_shape_with_None_stp_filename_physical_groups(self):
        """adds shapes to a Reactor object to check errors are raised
        correctly"""

        def test_stp_filename_None():
            """checks ValueError is raised when RotateStraightShapes with
            None as stp filenames are added"""

            test_shape = paramak.RotateStraightShape(
                points=[(0, 0), (0, 20), (20, 20)], stp_filename="filename.stp"
            )
            test_shape2 = paramak.RotateSplineShape(
                points=[(0, 0), (0, 20), (20, 20)], stp_filename=None
            )
            test_shape.create_solid()
            my_reactor = paramak.Reactor([test_shape, test_shape2])
            my_reactor.export_physical_groups()

        self.assertRaises(ValueError, test_stp_filename_None)


if __name__ == "__main__":
    unittest.main()


import os
import unittest
from pathlib import Path

import pytest

import paramak


class test_BlanketConstantThicknessArcV(unittest.TestCase):
    def test_BlanketConstantThickness_creation(self):
        """creates blanket from parametric shape and checks a solid is created"""

        test_shape = paramak.BlanketConstantThicknessArcV(
                         inner_lower_point=(300,-200),
                         inner_mid_point=(500,0),
                         inner_upper_point=(300,200),
                         thickness=20,
                         rotation_angle = 180
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

class test_ToroidalFieldCoilCoatHanger(unittest.TestCase):
    def test_ToroidalFieldCoilCoatHanger_creation(self):
        """creates blanket from parametric shape and checks a solid is created"""

        test_shape=paramak.ToroidalFieldCoilCoatHanger(
            horizontal_start_point=(200,500),
            horizontal_length=400,
            vertical_start_point=(700,50),
            vertical_length=500,
            thickness=50,
            distance=50,
            number_of_coils=5)

        assert test_shape.solid is not None
        assert test_shape.volume > 1000


class test_BlanketConstantThicknessArcH(unittest.TestCase):
    def test_BlanketConstantThickness_creation(self):
        """creates blanket from parametric shape and checks a solid is created"""

        test_shape = paramak.BlanketConstantThicknessArcH(
                         inner_lower_point=(300,-200),
                         inner_mid_point=(500,0),
                         inner_upper_point=(300,200),
                         thickness=20,
                         rotation_angle = 180
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000


class test_BlanketFP(unittest.TestCase):
    def test_BlanketFP_creation_plasma(self):
        """creates blanket from parametric shape and checks a solid is created"""
        plasma = paramak.Plasma(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
        )
        test_shape = paramak.BlanketFP(
            plasma=plasma,
            thickness=200,
            stop_angle=90,
            start_angle=270,
            offset_from_plasma=30,
            rotation_angle=180,
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_BlanketFP_creation_noplasma(self):
        """creates blanket from parametric shape and checks a solid is created"""

        test_shape = paramak.BlanketFP(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
            thickness=200,
            stop_angle=360,
            start_angle=0,
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_BlanketFP_creation_variable_thickness_from_tuple(self):
        """creates blanket from parametric shape and checks a solid is created"""

        test_shape = paramak.BlanketFP(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
            thickness=(100, 200),
            stop_angle=90,
            start_angle=270,
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_BlanketFP_creation_variable_thickness_function(self):
        """creates blanket from parametric shape and checks a solid is created"""
        def thickness(theta):
            return 100 + 3*theta
        test_shape = paramak.BlanketFP(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
            thickness=thickness,
            stop_angle=90,
            start_angle=270,
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_BlanketFP_physical_groups(self):
        """Creates default blanket and checks the exports of physical groups
        """
        test_shape = paramak.BlanketFP(
            100, stop_angle=90,
            start_angle=270,)
        test_shape.export_physical_groups('tests/blanket.json')

    def test_BlanketFP_full_cov_stp_export(self):
        """creates blanket from parametric shape and checks the STP export
        with full coverage"""

        test_shape = paramak.BlanketFP(
            major_radius=300,
            minor_radius=50,
            triangularity=0.5,
            elongation=2,
            thickness=200,
            stop_angle=360,
            start_angle=0,
            rotation_angle=180
        )

        test_shape.export_stp("tests/test_blanket_full_cov")


class test_PoloidalFieldCoilCase(unittest.TestCase):
    def test_PoloidalFieldCoilCase_creation(self):
        """creates a poloidal field coil from parametric shape and checks a solid is created"""
        test_shape = paramak.PoloidalFieldCoilCase(
            casing_thickness=5, coil_height=50, coil_width=50, center_point=(1000, 500)
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000


class test_Plasma(unittest.TestCase):
    def test_plasma_attributes(self):
        """creates a plasma object and checks its attributes"""

        test_plasma = paramak.Plasma()

        assert type(test_plasma.elongation) == float

        def test_plasma_elongation_min_setting():
            """checks ValueError is raised when an elongation < 0 is specified"""

            test_plasma.elongation = -1

        self.assertRaises(ValueError, test_plasma_elongation_min_setting)

        def test_plasma_elongation_max_setting():
            """checks ValueError is raised when an elongation > 4 is specified"""

            test_plasma.elongation = 400

        self.assertRaises(ValueError, test_plasma_elongation_max_setting)

    def test_plasma_x_points(self):
        """Checks the location of the x point for various plasma configurations
        """

        for triangularity, elongation, minor_radius, major_radius, \
                vertical_displacement in zip(
                    [-0.7, 0, 0.5],  # triangularity
                    [1, 1.5, 2],  # elongation
                    [100, 200, 300],  # minor radius
                    [300, 400, 600],  # major radius
                    [0, -10, 5]):  # displacement

            for config in ["non-null", "single-null", "double-null"]:

                # Run
                test_plasma = paramak.Plasma(
                    configuration=config,
                    triangularity=triangularity,
                    elongation=elongation,
                    minor_radius=minor_radius,
                    major_radius=major_radius,
                    vertical_displacement=vertical_displacement)

                # Expected
                expected_lower_x_point, expected_upper_x_point = None, None
                if config == "single-null" or \
                   config == "double-null":
                    expected_lower_x_point = (
                        1-(1+test_plasma.x_point_shift)*triangularity *
                        minor_radius,
                        -(1+test_plasma.x_point_shift)*elongation *
                        minor_radius + vertical_displacement
                    )

                    if config == "double-null":
                        expected_upper_x_point = (
                            expected_lower_x_point[0],
                            (1+test_plasma.x_point_shift)*elongation *
                            minor_radius + vertical_displacement
                        )

                # Check
                for point, expected_point in zip(
                        [test_plasma.lower_x_point,
                            test_plasma.upper_x_point],
                        [expected_lower_x_point,
                            expected_upper_x_point]):
                    assert point == expected_point

    def test_plasma_x_points_plasmaboundaries(self):
        """Checks the location of the x point for various plasma configurations
        for plasma from plasmaboundaries
        """

        for A, triangularity, elongation, minor_radius, major_radius in zip(
                [0, 0.05, 0.05],  # A
                [-0.7, 0, 0.5],  # triangularity
                [1, 1.5, 2],  # elongation
                [100, 200, 300],  # minor radius
                [300, 400, 600]):  # major radius

            for config in ["non-null", "single-null", "double-null"]:

                # Run
                test_plasma = paramak.PlasmaBoundaries(
                    configuration=config,
                    A=A,
                    triangularity=triangularity,
                    elongation=elongation,
                    minor_radius=minor_radius,
                    major_radius=major_radius)

                # Expected
                expected_lower_x_point, expected_upper_x_point = None, None
                if config == "single-null" or \
                   config == "double-null":
                    expected_lower_x_point = (
                        1-(1+test_plasma.x_point_shift)*triangularity *
                        minor_radius,
                        -(1+test_plasma.x_point_shift)*elongation *
                        minor_radius
                    )

                    if config == "double-null":
                        expected_upper_x_point = (
                            expected_lower_x_point[0],
                            -expected_lower_x_point[1]
                        )

                # Check
                for point, expected_point in zip(
                        [test_plasma.lower_x_point,
                            test_plasma.upper_x_point],
                        [expected_lower_x_point,
                            expected_upper_x_point]):
                    assert point == expected_point

    def test_export_plasma_source(self):
        """checks that export_stp() exports plasma stp file"""

        test_plasma = paramak.Plasma()

        os.system("rm plasma.stp")

        test_plasma.export_stp("plasma.stp")

        assert Path("plasma.stp").exists() == True
        os.system("rm plasma.stp")


    def test_export_plasma_from_points_export(self):
        """checks that export_stp() exports plasma stp file"""

        test_plasma = paramak.PlasmaFromPoints(outer_equatorial_x_point=500,
                                               inner_equatorial_x_point=300,
                                               high_point=(400,200),
                                               rotation_angle=180)

        os.system("rm plasma.stp")

        test_plasma.export_stp("plasma.stp")

        assert Path("plasma.stp").exists() == True
        os.system("rm plasma.stp")

# class test_DivertorBlock(unittest.TestCase):
# def test_DivertorBlock_creation(self):
#         test_shape = DivertorBlock(major_radius = 300,
#                                    minor_radius = 50,
#                                    triangularity = 0.5,
#                                    elongation = 2,
#                                    thickness = 50,
#                                    stop_angle = 120,
#                                    offset_from_plasma = 20,
#                                    start_x_value = 10)

#         assert test_shape.solid is not None
#         assert test_shape.volume > 1000

class test_DivertorITER(unittest.TestCase):
    def test_DivertorITER_creaction(self):
        test_shape = paramak.ITERtypeDivertor()
        assert test_shape.solid is not None

    def test_DivertorITER_STP_export(self):
        test_shape = paramak.ITERtypeDivertor()
        test_shape.export_stp("tests/ITER_div")


class test_DivertorITERNoDome(unittest.TestCase):
    def test_DivertorITER_creaction(self):
        test_shape = paramak.ITERtypeDivertorNoDome()
        assert test_shape.solid is not None

    def test_DivertorITER_STP_export(self):
        test_shape = paramak.ITERtypeDivertorNoDome()
        test_shape.export_stp("tests/ITER_div_no_dome")


class test_CenterColumnShieldFlatTopHyperbola(unittest.TestCase):
    def test_CenterColumnShieldFlatTopHyperbola_creation(self):
        """creates a CenterColumnShieldFlatTopHyperbola object and checks a solid is created"""

        test_shape = paramak.CenterColumnShieldFlatTopHyperbola(
            height=500,
            arc_height=300,
            inner_radius=50,
            mid_radius=100,
            outer_radius=150,
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000


class test_CenterColumnShieldPlasmaHyperbola(unittest.TestCase):
    def test_CenterColumnShieldPlasmaHyperbola_creation(self):
        """creates a CenterColumnShieldPlasmaHyperbola object and checks a solid is created"""

        test_shape = paramak.CenterColumnShieldPlasmaHyperbola(
            inner_radius=50, height=800, mid_offset=40, edge_offset=30
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000


class test_CenterColumnShieldHyperbola(unittest.TestCase):
    def test_CenterColumnShieldHyperbola_creation(self):
        """creates a CenterColumnShieldHyperbola object and checks a solid is created"""

        test_shape = paramak.CenterColumnShieldHyperbola(
            height=100, inner_radius=50, mid_radius=80, outer_radius=100
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000


class test_PoloidalFieldCoil(unittest.TestCase):
    def test_PoloidalFieldCoil_creation(self):
        """creates a PoloidalFieldCoil object and checks a solid is created"""

        test_shape = paramak.PoloidalFieldCoil(
            height=50, width=60, center_point=(1000, 500))

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

class test_ToroidalFieldCoilRectangle(unittest.TestCase):
    def test_ToroidalFieldCoilRectangle_creation(self):
        """creates a ToroidalFieldCoilRectangle object and checks a solid is created"""

        test_shape = paramak.ToroidalFieldCoilRectangle(
                        inner_upper_point=(100,700),
                        inner_mid_point=(800,0),
                        inner_lower_point=(100,-700),
                        thickness=150,
                        distance=50,
                        number_of_coils=8)
        assert test_shape.solid is not None
        assert test_shape.volume > 1000


class test_CenterColumnShieldCircular(unittest.TestCase):
    def test_CenterColumnShieldCircular_creation(self):
        """creates a CenterColumnShieldCircular object and checks a solid is created"""

        test_shape = paramak.CenterColumnShieldCircular(
            height=600, inner_radius=100, mid_radius=150, outer_radius=200
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000


class test_CenterColumnShieldFlatTopCircular(unittest.TestCase):
    def test_CenterColumnShieldFlatTopCircular_creation(self):
        """creates a CenterColumnShieldFlatTopCircular object and checks a solid is created"""

        test_shape = paramak.CenterColumnShieldFlatTopCircular(
            height=600, arc_height=200, inner_radius=100, mid_radius=150, outer_radius=200
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000


class test_CenterColumnShieldCylinder(unittest.TestCase):
    def test_CenterColumnShieldCylinder_creation(self):
        """creates a CenterColumnShieldCylinder object and checks a solid is created"""

        test_shape = paramak.CenterColumnShieldCylinder(
            height=600, inner_radius=100, outer_radius=200
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_volume_CenterColumnShieldCylinder(self):
        """creates a CenterColumnShieldCylinder object and checks that the volume is correct"""

        test_shape = paramak.CenterColumnShieldCylinder(
            rotation_angle=360,
            height=15,
            inner_radius=5,
            outer_radius=10,
            azimuth_placement_angle=0,
        )

        assert test_shape.volume == pytest.approx(3534.29)

        test_shape = paramak.CenterColumnShieldCylinder(
            rotation_angle=180,
            height=15,
            inner_radius=5,
            outer_radius=10,
            azimuth_placement_angle=95,
        )

        assert test_shape.volume == pytest.approx(3534.29 / 2.0)

    def test_export_stp_CenterColumnShieldCylinder(self):
        """checks that export_stp() can export an stp file of a CenterColumnShieldCylinder object"""

        test_shape = paramak.CenterColumnShieldCylinder(
            rotation_angle=360,
            height=15,
            inner_radius=5,
            outer_radius=10,
            azimuth_placement_angle=0,
        )

        os.system("rm center_column_shield.stp")

        test_shape.export_stp("center_column_shield.stp")

        assert Path("center_column_shield.stp").exists() == True

        os.system("rm center_column_shield.stp")


class test_PoloidalFieldCoilCaseFC(unittest.TestCase):
    def test_PoloidalFieldCoilCaseFC_creation(self):
        """creates a PoloidalFieldCoilCaseFC object and checks a solid is created"""

        pf_coil = paramak.PoloidalFieldCoil(
            height=50, width=60, center_point=(1000, 500))

        test_shape = paramak.PoloidalFieldCoilCaseFC(
            pf_coil=pf_coil, casing_thickness=5)

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

class test_InnerTfCoilsFlat(unittest.TestCase):
    def test_InnerTfCoilsFlat_creation(self):
        """creates a InnerTfCoilsFlat object and checks a solid is created"""

        test_shape = paramak.InnerTfCoilsFlat(
                    height=500,
                    inner_radius=50,
                    outer_radius=150,
                    number_of_coils=6,
                    gap_size=5,
            )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

class test_InnerTfCoilsCircular(unittest.TestCase):
    def test_InnerTfCoilsCircular_creation(self):
        """creates a InnerTfCoilsCircular object and checks a solid is created"""

        test_shape = paramak.InnerTfCoilsCircular(
                    height=500,
                    inner_radius=50,
                    outer_radius=150,
                    number_of_coils=6,
                    gap_size=5,
            )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

if __name__ == "__main__":
    unittest.main()

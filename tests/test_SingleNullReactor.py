import os
import unittest
from pathlib import Path

import pytest

import paramak


class test_SingleNullReactor(unittest.TestCase):
    def test_SingleNullReactor_creation_upper_divertor(self):
        """creates a SingleNullReactor using a parametric reactor with an upper divertor
        and checks all components are created"""

        test_reactor = paramak.SingleNullReactor(
            inner_bore_radial_thickness=50,
            inboard_tf_leg_radial_thickness=50,
            center_column_shield_radial_thickness=50,
            divertor_radial_thickness=100,
            inner_plasma_gap_radial_thickness=50,
            plasma_radial_thickness=200,
            outer_plasma_gap_radial_thickness=50,
            firstwall_radial_thickness=50,
            blanket_radial_thickness=100,
            blanket_rear_wall_radial_thickness=50,
            elongation=2,
            triangularity=0.55,
            number_of_tf_coils=16,
            rotation_angle=180,
            divertor_position="upper",
        )

        test_reactor.export_stp()

        assert len(test_reactor.shapes_and_components) == 7

    def test_SingleNullReactor_creation_lower_divertor(self):
        """creates a SingleNullReactor using a parametric reactor with a lower divertor
        and checks all components are created"""

        test_reactor = paramak.SingleNullReactor(
            inner_bore_radial_thickness=50,
            inboard_tf_leg_radial_thickness=50,
            center_column_shield_radial_thickness=50,
            divertor_radial_thickness=100,
            inner_plasma_gap_radial_thickness=50,
            plasma_radial_thickness=200,
            outer_plasma_gap_radial_thickness=50,
            firstwall_radial_thickness=50,
            blanket_radial_thickness=100,
            blanket_rear_wall_radial_thickness=50,
            elongation=2,
            triangularity=0.55,
            number_of_tf_coils=16,
            rotation_angle=180,
            divertor_position="lower",
        )

        test_reactor.export_stp()

        assert len(test_reactor.shapes_and_components) == 7

    def test_SingleNullReactor_creation_with_pf_coils(self):
        """creates a SingleNullReactor using a parametric reactor with pf coils and
        checks all components are created"""

        test_reactor = paramak.SingleNullReactor(
            inner_bore_radial_thickness=50,
            inboard_tf_leg_radial_thickness=50,
            center_column_shield_radial_thickness=50,
            divertor_radial_thickness=100,
            inner_plasma_gap_radial_thickness=50,
            plasma_radial_thickness=200,
            outer_plasma_gap_radial_thickness=50,
            firstwall_radial_thickness=50,
            blanket_radial_thickness=100,
            blanket_rear_wall_radial_thickness=50,
            elongation=2,
            triangularity=0.55,
            number_of_tf_coils=16,
            rotation_angle=180,
            divertor_position="lower",
            pf_coil_to_rear_blanket_radial_gap=50,
            pf_coil_vertical_thicknesses=[50, 50, 50, 50, 50],
            pf_coil_radial_thicknesses=[40, 40, 40, 40, 40],
            pf_coil_to_tf_coil_radial_gap=50,
        )

        test_reactor.export_stp()

        assert len(test_reactor.shapes_and_components) == 12

    def test_SingleNullReactor_creation_with_pf_tf_coils(self):
        """creates a SingleNullReactor using a parametric reactor with pf and tf coils
        and checks all components are created"""

        test_reactor = paramak.SingleNullReactor(
            inner_bore_radial_thickness=50,
            inboard_tf_leg_radial_thickness=50,
            center_column_shield_radial_thickness=50,
            divertor_radial_thickness=100,
            inner_plasma_gap_radial_thickness=50,
            plasma_radial_thickness=200,
            outer_plasma_gap_radial_thickness=50,
            firstwall_radial_thickness=50,
            blanket_radial_thickness=100,
            blanket_rear_wall_radial_thickness=50,
            elongation=2,
            triangularity=0.55,
            number_of_tf_coils=16,
            rotation_angle=180,
            divertor_position="lower",
            outboard_tf_coil_radial_thickness=50,
            pf_coil_to_rear_blanket_radial_gap=50,
            tf_coil_poloidal_thickness=70,
            pf_coil_vertical_thicknesses=[50, 50, 50, 50, 50],
            pf_coil_radial_thicknesses=[40, 40, 40, 40, 40],
            pf_coil_to_tf_coil_radial_gap=50,
        )

        test_reactor.export_stp()

        assert len(test_reactor.shapes_and_components) == 13

    def test_SingleNullReactor_svg_creation(self):
        """creates a SingleNullReactor using a parametric reactor and checks that an
        svg image of the reactor can be exported"""
        
        os.system("rm test_singlenullreactor_image.svg")

        test_reactor = paramak.SingleNullReactor(
            inner_bore_radial_thickness=50,
            inboard_tf_leg_radial_thickness=50,
            center_column_shield_radial_thickness=50,
            divertor_radial_thickness=100,
            inner_plasma_gap_radial_thickness=50,
            plasma_radial_thickness=200,
            outer_plasma_gap_radial_thickness=50,
            firstwall_radial_thickness=50,
            blanket_radial_thickness=100,
            blanket_rear_wall_radial_thickness=50,
            elongation=2,
            triangularity=0.55,
            number_of_tf_coils=16,
            rotation_angle=180,
            divertor_position="lower",
            outboard_tf_coil_radial_thickness=50,
            pf_coil_to_rear_blanket_radial_gap=50,
            tf_coil_poloidal_thickness=70,
            pf_coil_vertical_thicknesses=[50, 50, 50, 50, 50],
            pf_coil_radial_thicknesses=[40, 40, 40, 40, 40],
            pf_coil_to_tf_coil_radial_gap=50,
        )
        test_reactor.export_svg("test_singlenullreactor_image.svg")

        assert Path("test_singlenullreactor_image.svg").exists() is True 
        os.system("rm test_singlenullreactor_image.svg")
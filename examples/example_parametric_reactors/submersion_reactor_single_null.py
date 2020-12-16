"""
This example creates a single null submersion reactor using the
SubmersionTokamak parametric reactor. By default the script saves stp, stl,
html and svg files.
"""

from pathlib import Path

import paramak


def make_submersion_sn(outputs=['stp', 'neutronics', 'svg', 'stl', 'html'],
                       output_folder='SubmersionTokamak_sn'):

    my_reactor = paramak.SingleNullSubmersionTokamak(
        inner_bore_radial_thickness=30,
        inboard_tf_leg_radial_thickness=30,
        center_column_shield_radial_thickness=30,
        divertor_radial_thickness=80,
        inner_plasma_gap_radial_thickness=50,
        plasma_radial_thickness=200,
        outer_plasma_gap_radial_thickness=50,
        firstwall_radial_thickness=30,
        blanket_rear_wall_radial_thickness=30,
        number_of_tf_coils=16,
        rotation_angle=180,
        support_radial_thickness=90,
        inboard_blanket_radial_thickness=30,
        outboard_blanket_radial_thickness=30,
        elongation=2.00,
        triangularity=0.50,
        pf_coil_radial_thicknesses=[30, 30, 30, 30],
        pf_coil_vertical_thicknesses=[30, 30, 30, 30],
        pf_coil_to_tf_coil_radial_gap=50,
        outboard_tf_coil_radial_thickness=30,
        outboard_tf_coil_poloidal_thickness=30,
        tf_coil_to_rear_blanket_radial_gap=20,
        divertor_position="lower",
        support_position="lower"
    )

    if 'stp' in outputs:
        my_reactor.export_stp(output_folder=output_folder)
    if 'neutronics' in outputs:
        my_reactor.export_neutronics_description(
            Path(output_folder) / 'manifest.json')
    if 'svg' in outputs:
        my_reactor.export_svg(Path(output_folder) / 'reactor.svg')
    if 'stl' in outputs:
        my_reactor.export_stl(output_folder=output_folder)
    if 'html' in outputs:
        my_reactor.export_html(Path(output_folder) / 'reactor.html')


if __name__ == "__main__":
    make_submersion_sn(['stp', 'neutronics', 'svg', 'stl', 'html'])

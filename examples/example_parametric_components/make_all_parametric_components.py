"""
This python script demonstrates the creation of all parametric shapes available
in the paramak tool
"""

import paramak

def main():

    rot_angle = 180
    all_components = []

    plasma = paramak.Plasma(
        # default parameters
        rotation_angle = rot_angle,
        stp_filename = 'plasma_shape.stp'
    )
    all_components.append(plasma)

    component = paramak.BlanketFP(
        plasma=plasma,
        thickness=100,
        stop_angle=90,
        start_angle=-90,
        offset_from_plasma=30,
        rotation_angle=180,
        stp_filename='blanket_constant_thickness_outboard_plasma.stp'
    )
    all_components.append(component)

    component = paramak.BlanketFP(
        plasma=plasma,
        thickness=100,
        stop_angle=90,
        start_angle=250,
        offset_from_plasma=30,
        rotation_angle=180,
        stp_filename='blanket_constant_thickness_inboard_plasma.stp'
    )
    all_components.append(component)

    component = paramak.BlanketFP(
        plasma=plasma,
        thickness=100,
        stop_angle=250,
        start_angle=-90,
        offset_from_plasma=30,
        rotation_angle=180,
        stp_filename='blanket_constant_thickness_plasma.stp'
    )
    all_components.append(component)

    component=paramak.ToroidalFieldCoilCoatHanger(
        horizontal_start_point=(200,500),
        horizontal_length=400,
        vertical_start_point=(700,50),
        vertical_length=500,
        thickness=50,
        distance=50,
        stp_filename='toroidal_field_coil_coat_hanger.stp',
        number_of_coils=5)
    all_components.append(component)

    component = paramak.CenterColumnShieldCylinder(
        inner_radius = 80,
        outer_radius = 100,
        height = 300,
        rotation_angle = rot_angle,
        stp_filename='center_column_shield_cylinder.stp'
    )
    all_components.append(component)

    component = paramak.CenterColumnShieldHyperbola(
        inner_radius = 50,
        mid_radius = 75,
        outer_radius = 100,
        height = 300,
        rotation_angle = rot_angle,
        stp_filename='center_column_shield_hyperbola.stp'
    )
    all_components.append(component)

    component = paramak.CenterColumnShieldCircular(
        inner_radius = 50,
        mid_radius = 75,
        outer_radius = 100,
        height = 300,
        rotation_angle = rot_angle,
        stp_filename='center_column_shield_circular.stp'
    )
    all_components.append(component)

    component = paramak.CenterColumnShieldFlatTopHyperbola(
        inner_radius = 50,
        mid_radius = 75,
        outer_radius = 100,
        arc_height = 220,
        height = 300,
        rotation_angle = rot_angle,
        stp_filename='center_column_shield_flat_top_hyperbola.stp'
    )
    all_components.append(component)

    component = paramak.CenterColumnShieldFlatTopCircular(
        inner_radius = 50,
        mid_radius = 75,
        outer_radius = 100,
        arc_height = 220,
        height = 300,
        rotation_angle = rot_angle,
        stp_filename='center_column_shield_flat_top_Circular.stp'
    )
    all_components.append(component)

    component = paramak.CenterColumnShieldPlasmaHyperbola(
        inner_radius = 150,
        mid_offset = 50,
        edge_offset = 40,
        height = 800,
        rotation_angle = rot_angle,
        stp_filename='center_column_shield_plasma_hyperbola.stp'
    )
    all_components.append(component)


    #

    # component = paramak.DivertorBlock(
    #     major_radius = 800,
    #     minor_radius = 400,
    #     triangularity = 1.2,
    #     elongation = 0.9,
    #     thickness = 50,
    #     offset_from_plasma = 20,
    #     start
    # )



    component = paramak.InnerTfCoilsCircular(
        inner_radius = 25,
        outer_radius = 100,
        number_of_coils = 10,
        gap_size = 5,
        height = 300,
        stp_filename='inner_tf_coils_circular.stp'
    )
    all_components.append(component)

    component = paramak.InnerTfCoilsFlat(
        inner_radius = 25,
        outer_radius = 100,
        number_of_coils = 10,
        gap_size = 5,
        height = 300,
        stp_filename='inner_tf_coils_flat.stp'
    )
    all_components.append(component)

    pf_coil = paramak.PoloidalFieldCoil(
        center_point = (100, 100),
        height = 20,
        width = 20,
        rotation_angle = rot_angle,
        stp_filename='poloidal_field_coil.stp'
    )
    all_components.append(pf_coil)

    component = paramak.PoloidalFieldCoilCaseFC(
        pf_coil=pf_coil,
        casing_thickness = 10,
        rotation_angle = rot_angle,
        stp_filename='poloidal_field_coil_case_fc.stp'
    )
    all_components.append(component)

    component = paramak.PoloidalFieldCoilCase(
        center_point = (100, 100),
        coil_height = 20,
        coil_width = 20,
        casing_thickness = 10,
        rotation_angle = rot_angle,
        stp_filename='poloidal_field_coil_case.stp'
    )
    all_components.append(component)

    component = paramak.BlanketConstantThicknessArcV(
                            inner_lower_point=(300,-200),
                            inner_mid_point=(500,0),
                            inner_upper_point=(300,200),
                            thickness=100,
                            rotation_angle=rot_angle,
                            stp_filename='blanket_arc_v.stp'
                            )
    all_components.append(component)

    component = paramak.BlanketConstantThicknessArcH(
                            inner_lower_point=(300,-200),
                            inner_mid_point=(400,0),
                            inner_upper_point=(300,200),
                            thickness=100,
                            rotation_angle=rot_angle,
                            stp_filename='blanket_arc_h.stp'
                            )
    all_components.append(component)

    component = paramak.ToroidalFieldCoilRectangle(
                inner_upper_point=(100,700),
                inner_mid_point=(800,0),
                inner_lower_point=(100,-700),
                thickness=150,
                distance=60,
                stp_filename='tf_coil_rectangle.stp',
                number_of_coils=6)
    all_components.append(component)

    component = paramak.ITERtypeDivertor(
        # default parameters
        rotation_angle=rot_angle,
        stp_filename='ITER_type_divertor.stp'
    )
    all_components.append(component)

    return all_components


if __name__ == "__main__":
    all_components = main()
    for components in all_components:
        components.export_stp()

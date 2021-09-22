
import paramak

my_reactor = paramak.BallReactorLayered(
    inner_bore_radial_thickness=10,
    inboard_layer_thicknesses=[20, 30, 50],
    divertor_radial_thickness=150,
    inner_plasma_gap_radial_thickness=30,
    plasma_radial_thickness=300,
    outer_plasma_gap_radial_thickness=30,
    outboard_layer_thicknesses=[30, 40, 20, 20],
    elongation=2,
    triangularity=0.55,
    number_of_tf_coils=16,
    rotation_angle=180,
    pf_coil_case_thicknesses=[10, 10, 10, 10],
    pf_coil_radial_thicknesses=[20, 50, 50, 20],
    pf_coil_vertical_thicknesses=[20, 50, 50, 20],
    pf_coil_radial_position=[550, 625, 625, 550],
    pf_coil_vertical_position=[300, 100, -100, -300],
    rear_outboard_layer_to_tf_gap=100,
    outboard_tf_coil_radial_thickness=100,
    outboard_tf_coil_poloidal_thickness=50
)

my_reactor.export_stp('BallReactorLayered')
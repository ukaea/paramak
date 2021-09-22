
import openmc
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

my_source = openmc.Source()
my_source.space = openmc.stats.Point((my_reactor.major_radius, 0, 0))
my_source.angle = openmc.stats.Isotropic()
my_source.energy = openmc.stats.Discrete([14e6], [1])

my_model = paramak.NeutronicsModel(
    geometry=my_reactor,
    source=my_source,
    materials={
        "inboard_layer_1_mat": "eurofer",
        "inboard_layer_2_mat": "eurofer",
        "inboard_layer_3_mat": "eurofer",
        "divertor_mat": "tungsten",
        "outboard_layer_1_mat": "Li4SiO4",
        "outboard_layer_2_mat": "Li4SiO4",
        "outboard_layer_3_mat": "Li4SiO4",
        "outboard_layer_4_mat": "Li4SiO4",
        "pf_coil_mat": "copper",
        "tf_coil_mat": "copper"
    },
    simulation_batches=3,
    simulation_particles_per_batch=10000
)

my_model.simulate()

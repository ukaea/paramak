
import openmc
import paramak as p

shape_1 = p.CenterColumnShieldCylinder(
    inner_radius=10,
    outer_radius=20,
    height=100,
    stp_filename="shape_1.stp",
    stl_filename="shape_1.stl",
    material_tag="shape_1_mat"
)

my_reactor = p.Reactor([shape_1])

my_source = openmc.Source()
my_source.space = openmc.stats.Point((0, 0, 0))
my_source.angle = openmc.stats.Isotropic()
my_source.energy = openmc.stats.Discrete([14e6], [1])

my_model = p.NeutronicsModel(
    geometry=my_reactor,
    source=my_source,
    materials={
        "shape_1_mat": "Li4SiO4"
    },
    cell_tallies=["TBR"],
    nuclide_tallies=["TBR"],
    simulation_batches=5,
    simulation_particles_per_batch=100000
)

my_model.simulate()

nuclide_total_tbr = 0

for key, value in my_model.results.items():
    if key == "TBR":
        print("Total Integrated TBR in material = " + str(value["result"]))
    elif key == "shape_1_mat_TBR":
        pass
    else:
        nuclide_total_tbr += value["events per source particle"]["result"]

print("Nuclide total tbr = " + str(nuclide_total_tbr))

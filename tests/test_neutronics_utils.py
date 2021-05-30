
import json
import os
import unittest
import urllib.request
from pathlib import Path

import openmc
import paramak
from paramak.neutronics_utils import (add_stl_to_moab_core,
                                      define_moab_core_and_tags)


class TestNeutronicsUtilityFunctions(unittest.TestCase):

    def test_missing_dagmc_not_watertight_file(self):

        def missing_dagmc_not_watertight_file():
            """Trys to make a watertight dagmc.h5m file without a
            dagmc_not_watertight.h5m input file"""

            os.system('rm *.h5m')

            paramak.neutronics_utils.make_watertight(
                input_filename="dagmc_not_watertight.h5m",
                output_filename="dagmc.h5m",
            )

        self.assertRaises(
            FileNotFoundError,
            missing_dagmc_not_watertight_file
        )

    def test_moab_instance_creation(self):
        """passes three points on a circle to the function and checks that the
        radius and center of the circle is calculated correctly"""

        os.system('rm *.stl *.h5m')

        moab_core, moab_tags = define_moab_core_and_tags()

        test_shape = paramak.RotateStraightShape(
            points=[(0, 0), (0, 20), (20, 20), (20, 0)]
        )

        test_shape.export_stl('test_file.stl')

        new_moab_core = add_stl_to_moab_core(
            moab_core=moab_core,
            surface_id=1,
            volume_id=1,
            material_name='test_mat',
            tags=moab_tags,
            stl_filename='test_file.stl'
        )

        all_sets = new_moab_core.get_entities_by_handle(0)

        file_set = new_moab_core.create_meshset()

        new_moab_core.add_entities(file_set, all_sets)

        new_moab_core.write_file('test_file.h5m')

        assert Path('test_file.stl').exists()
        assert Path('test_file.h5m').exists()

    def test_create_inital_source_file(self):
        """Creates an initial_source.h5 from a point source"""

        os.system("rm *.h5")

        source = openmc.Source()
        source.space = openmc.stats.Point((0, 0, 0))
        source.energy = openmc.stats.Discrete([14e6], [1])

        paramak.neutronics_utils.create_inital_particles(source, 100)

        assert Path("initial_source.h5").exists() is True

    def test_extract_points_from_initial_source(self):
        """Creates an initial_source.h5 from a point source reads in the file
        and checks the first point is 0, 0, 0 as exspected."""

        os.system("rm *.h5")

        source = openmc.Source()
        source.space = openmc.stats.Point((0, 0, 0))
        source.energy = openmc.stats.Discrete([14e6], [1])

        paramak.neutronics_utils.create_inital_particles(source, 10)

        for view_plane in ['XZ', 'XY', 'YZ', 'YX', 'ZY', 'ZX', 'RZ', 'XYZ']:

            points = paramak.neutronics_utils.extract_points_from_initial_source(
                view_plane=view_plane)

            assert len(points) == 10

            for point in points:
                if view_plane == 'XYZ':
                    assert len(point) == 3
                    assert point[0] == 0
                    assert point[1] == 0
                    assert point[2] == 0
                else:
                    assert len(point) == 2
                    assert point[0] == 0
                    assert point[1] == 0

    def test_extract_points_from_initial_source_incorrect_view_plane(self):
        """Tries to make extract points on to viewplane that is not accepted"""

        def incorrect_viewplane():
            """Inccorect view_plane should raise a ValueError"""

            source = openmc.Source()
            source.space = openmc.stats.Point((0, 0, 0))
            source.energy = openmc.stats.Discrete([14e6], [1])

            paramak.neutronics_utils.create_inital_particles(source, 10)

            paramak.neutronics_utils.extract_points_from_initial_source(
                view_plane='coucou'
            )

        self.assertRaises(ValueError, incorrect_viewplane)

    def test_find_materials_in_h5_file(self):
        """exports a h5m with specific material tags and checks they are
        found using the find_material_groups_in_h5m utility function"""

        os.system('rm *.stl *.h5m')

        pf_coil = paramak.PoloidalFieldCoil(
            height=10,
            width=10,
            center_point=(100, 0),
            rotation_angle=180,
            material_tag='copper'
        )

        pf_coil.export_h5m_with_pymoab(
            filename='dagmc.h5',  # missing the m, but this is added
            include_graveyard=True,
        )

        list_of_mats = paramak.neutronics_utils.find_material_groups_in_h5m(
            filename="dagmc.h5m"
        )

        assert len(list_of_mats) == 2
        assert 'mat:copper' in list_of_mats
        assert 'mat:graveyard' in list_of_mats

    def test_create_inital_particles(self):
        """Creates an initial source file using create_inital_particles utility
        and checks the file exists and that the points are correct"""

        os.system('rm *.h5')

        source = openmc.Source()
        source.space = openmc.stats.Point((1, 2, 3))
        source.energy = openmc.stats.Discrete([14e6], [1])
        source.angle = openmc.stats.Isotropic()

        source_file = paramak.neutronics_utils.create_inital_particles(
            source=source,
            number_of_source_particles=10
        )

        assert source_file == "initial_source.h5"
        assert Path(source_file).exists() is True

        points = paramak.neutronics_utils.extract_points_from_initial_source(
            view_plane='XYZ', input_filename=source_file
        )

        assert len(points) == 10
        for point in points:
            assert point == (1, 2, 3)

    def test_make_watertight_cmd_with_example_dagmc_file(self):
        """downloads a h5m and makes it watertight, checks the the watertight
        file is produced."""

        os.system('rm *.h5m')

        url = 'https://github.com/Shimwell/fusion_example_for_openmc_using_paramak/raw/main/dagmc.h5m'
        urllib.request.urlretrieve(url, 'not_watertight_dagmc.h5m')

        output_filename = paramak.neutronics_utils.make_watertight(
            input_filename="not_watertight_dagmc.h5m",
            output_filename="watertight_dagmc.h5m"
        )

        assert Path("not_watertight_dagmc.h5m").exists() is True
        assert output_filename == "watertight_dagmc.h5m"
        assert Path("watertight_dagmc.h5m").exists() is True

    def test_export_vtk_without_h5m_raises_error(self):
        """exports a vtk file when shapes_and_components is set to a string"""

        def check_correct_error_is_rasied():
            os.system('rm *.h5m *.vtk')
            paramak.neutronics_utils.export_vtk(h5m_filename='dagmc.h5m')

        self.assertRaises(FileNotFoundError, check_correct_error_is_rasied)

    def test_export_vtk_without_h5m_suffix(self):
        """exports a vtk file when shapes_and_components is set to a string"""

        os.system('rm *.stl *.h5m *.vtk')

        pf_coil = paramak.PoloidalFieldCoil(
            height=10,
            width=10,
            center_point=(100, 0),
            rotation_angle=180,
            material_tag='copper'
        )

        pf_coil.export_h5m_with_pymoab(
            filename='dagmc',
            include_graveyard=True,
        )

        paramak.neutronics_utils.export_vtk(h5m_filename='dagmc')

        assert Path('dagmc.vtk').is_file()
        assert Path('dagmc.h5m').is_file()

    # these tests only work if trelis is avaialbe
    def test_make_watertight_cmd(self):
        """exports a h5m and makes it watertight, checks the the watertight
        file is produced."""

        os.system('rm *.stl *.h5m')

        # https: // github.com / Shimwell /
        # fusion_example_for_openmc_using_paramak / raw / main / dagmc.h5m

        pf_coil = paramak.PoloidalFieldCoil(
            height=10,
            width=10,
            center_point=(100, 0),
            rotation_angle=180,
            material_tag='copper',
            method='trelis'
        )

        pf_coil.export_h5m_with_trelis(
            filename='not_watertight_dagmc.h5m',
            include_graveyard=True,
        )

        assert Path('not_watertight_dagmc.h5m').is_file

        output_filename = paramak.neutronics_utils.make_watertight(
            input_filename="not_watertight_dagmc.h5m",
            output_filename="watertight_dagmc.h5m"
        )

        assert Path("not_watertight_dagmc.h5").exists() is True
        assert output_filename == "watertight_dagmc.h5m"
        assert Path("watertight_dagmc.h5").exists() is True

    def test_trelis_command_to_create_dagmc_h5m_with_default_mat_name(self):
        """Creats a h5m file with trelis and forms groups using the material_tag
        key in the manifest.json file. Then checks the groups in the resulting
        h5 file match those in the original dictionary"""

        pf_coil = paramak.PoloidalFieldCoil(
            height=10,
            width=10,
            center_point=(100, 0),
            rotation_angle=180,
        )

        pf_coil_case = paramak.PoloidalFieldCoilCaseFC(
            pf_coil=pf_coil,
            casing_thickness=5
        )

        pf_coil.export_stp('pf_coil.stp')
        pf_coil_case.export_stp('pf_coil_case.stp')

        manifest_with_material_tags = [
            {
                "material_tag": "copper",
                "stp_filename": "pf_coil_case.stp"
            },
            {
                "material_tag": "tungsten_carbide",
                "stp_filename": "pf_coil.stp"
            }
        ]
        with open('manifest.json', 'w') as outfile:
            json.dump(manifest_with_material_tags, outfile)

        paramak.neutronics_utils.trelis_command_to_create_dagmc_h5m(
            faceting_tolerance=1e-2,
            merge_tolerance=1e-4,
            material_key_name='material_tag',
            batch=True
        )

        list_of_mats = paramak.neutronics_utils.find_material_groups_in_h5m(
            filename="dagmc_not_watertight.h5m"
        )

        assert len(list_of_mats) == 2
        assert 'mat:copper' in list_of_mats
        assert 'mat:tungsten_carbide' in list_of_mats
        # assert 'mat:graveyard' in list_of_mats

    def test_trelis_command_to_create_dagmc_h5m_with_user_mat_name(self):
        """Creats a h5m file with trelis and forms groups using the material_id
        key in the manifest.json file. Then checks the groups in the resulting
        h5 file match those in the original dictionary"""

        os.system('rm *.stp *.h5m *.json')

        pf_coil = paramak.PoloidalFieldCoil(
            height=10,
            width=10,
            center_point=(100, 0),
            rotation_angle=180,
        )

        pf_coil_case = paramak.PoloidalFieldCoilCaseFC(
            pf_coil=pf_coil,
            casing_thickness=5
        )

        pf_coil.export_stp('pf_coil.stp')
        pf_coil_case.export_stp('pf_coil_case.stp')

        manifest_with_material_tags = [
            {
                "material_id": "42",
                "stp_filename": "pf_coil_case.stp"
            },
            {
                "material_id": 12,  # this is an int to check the str() works
                "stp_filename": "pf_coil.stp"
            }
        ]
        with open('manifest.json', 'w') as outfile:
            json.dump(manifest_with_material_tags, outfile)

        paramak.neutronics_utils.trelis_command_to_create_dagmc_h5m(
            faceting_tolerance=1e-2,
            merge_tolerance=1e-4,
            material_key_name='material_id',
            batch=True,
        )

        list_of_mats = paramak.neutronics_utils.find_material_groups_in_h5m(
            filename="dagmc_not_watertight.h5m"
        )

        assert len(list_of_mats) == 2
        assert 'mat:42' in list_of_mats
        assert 'mat:12' in list_of_mats
        # assert 'mat:graveyard' in list_of_mats

    def test_trelis_command_to_create_dagmc_h5m_with_custom_geometry_key(self):
        """Creats a h5m file with trelis and loads stp files using a custom
        key in the manifest.json file. Then checks the groups in the resulting
        h5 file match those in the original dictionary"""

        os.system('rm *.stp *.h5m *.json')

        pf_coil = paramak.PoloidalFieldCoil(
            height=10,
            width=10,
            center_point=(100, 0),
            rotation_angle=180,
        )

        pf_coil_case = paramak.PoloidalFieldCoilCaseFC(
            pf_coil=pf_coil,
            casing_thickness=5
        )

        pf_coil.export_stp('pf_coil_custom_key.stp')
        pf_coil_case.export_stp('pf_coil_case_custom_key.stp')

        manifest_with_material_tags = [
            {
                "material_tag": "copper",
                "geometry_filename": "pf_coil_custom_key.stp"
            },
            {
                "material_tag": "tungsten_carbide",
                "geometry_filename": "pf_coil_case_custom_key.stp"
            }
        ]
        with open('manifest.json', 'w') as outfile:
            json.dump(manifest_with_material_tags, outfile)

        paramak.neutronics_utils.trelis_command_to_create_dagmc_h5m(
            faceting_tolerance=1e-2,
            merge_tolerance=1e-4,
            geometry_key_name='geometry_filename',
            batch=True
        )

        list_of_mats = paramak.neutronics_utils.find_material_groups_in_h5m(
            filename="dagmc_not_watertight.h5m"
        )

        assert len(list_of_mats) == 2
        assert 'mat:copper' in list_of_mats
        assert 'mat:tungsten_carbide' in list_of_mats

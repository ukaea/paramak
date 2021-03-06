
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Optional, Tuple, List

import cadquery as cq
import matplotlib.pyplot as plt
from cadquery import exporters

import paramak
from paramak.neutronics_utils import (add_stl_to_moab_core,
                                      define_moab_core_and_tags)
from paramak.utils import get_hash


class Reactor:
    """The Reactor object allows shapes and components to be added and then
    collective operations to be performed on them. Combining all the shapes is
    required for creating images of the whole reactor and creating a Graveyard
    (bounding box) that is needed for neutronics simulations.

    Args:
        shapes_and_components (list): list of paramak.Shape
    """

    def __init__(self, shapes_and_components: list):

        self.material_tags = []
        self.stp_filenames = []
        self.stl_filenames = []
        self.tet_meshes = []
        self.graveyard = None
        self.solid = None

        self.shapes_and_components = shapes_and_components
        self.reactor_hash_value = None

        self.graveyard_offset = None  # set by the make_graveyard method

    @property
    def stp_filenames(self):
        values = []
        for shape_or_component in self.shapes_and_components:
            values.append(shape_or_component.stp_filename)
        return values

    @stp_filenames.setter
    def stp_filenames(self, value):
        self._stp_filenames = value

    @property
    def stl_filenames(self):
        values = []
        for shape_or_component in self.shapes_and_components:
            values.append(shape_or_component.stl_filename)
        return values

    @stl_filenames.setter
    def stl_filenames(self, value):
        self._stl_filenames = value

    @property
    def largest_dimension(self):
        """Calculates a bounding box for the Reactor and returns the largest
        absolute value of the largest dimension of the bounding box"""
        largest_dimension = 0
        for component in self.shapes_and_components:
            largest_dimension = max(
                largest_dimension,
                component.largest_dimension)
        self._largest_dimension = largest_dimension
        return largest_dimension

    @largest_dimension.setter
    def largest_dimension(self, value):
        self._largest_dimension = value

    @property
    def material_tags(self):
        """Returns a set of all the materials_tags used in the Reactor
        (excluding the plasma)"""
        values = []
        for shape_or_component in self.shapes_and_components:
            if not isinstance(
                shape_or_component,
                (paramak.Plasma,
                 paramak.PlasmaFromPoints,
                 paramak.PlasmaBoundaries)):
                values.append(shape_or_component.material_tag)
        return values

    @material_tags.setter
    def material_tags(self, value):
        self._material_tags = value

    @property
    def tet_meshes(self):
        values = []
        for shape_or_component in self.shapes_and_components:
            values.append(shape_or_component.tet_mesh)
        return values

    @tet_meshes.setter
    def tet_meshes(self, value):
        self._tet_meshes = value

    @property
    def shapes_and_components(self):
        """Adds a list of parametric shape(s) and or parametric component(s)
        to the Reactor object. This allows collective operations to be
        performed on all the shapes in the reactor. When adding a shape or
        component the stp_filename of the shape or component should be unique"""
        if hasattr(self, "create_solids"):
            ignored_keys = ["reactor_hash_value"]
            if get_hash(self, ignored_keys) != self.reactor_hash_value:
                self.create_solids()
                self.reactor_hash_value = get_hash(self, ignored_keys)
        return self._shapes_and_components

    @shapes_and_components.setter
    def shapes_and_components(self, value):
        if not isinstance(value, Iterable):
            raise ValueError("shapes_and_components must be a list")
        self._shapes_and_components = value

    @property
    def graveyard_offset(self):
        return self._graveyard_offset

    @graveyard_offset.setter
    def graveyard_offset(self, value):
        if value is None:
            self._graveyard_offset = None
        elif not isinstance(value, (float, int)):
            raise TypeError("graveyard_offset must be a number")
        elif value < 0:
            raise ValueError("graveyard_offset must be positive")
        self._graveyard_offset = value

    @property
    def solid(self):
        """This combines all the parametric shapes and compents in the reactor
        object.
        """

        list_of_cq_vals = []

        for shape_or_compound in self.shapes_and_components:
            if isinstance(
                    shape_or_compound.solid,
                    (cq.occ_impl.shapes.Shape, cq.occ_impl.shapes.Compound)):
                for solid in shape_or_compound.solid.Solids():
                    list_of_cq_vals.append(solid)
            else:
                list_of_cq_vals.append(shape_or_compound.solid.val())

        compound = cq.Compound.makeCompound(list_of_cq_vals)

        return compound

    @ solid.setter
    def solid(self, value):
        self._solid = value

    def neutronics_description(
            self,
            include_plasma: Optional[bool] = False,
            include_graveyard: Optional[bool] = True) -> dict:
        """A description of the reactor containing material tags, stp filenames,
        and tet mesh instructions. This is used for neutronics simulations
        which require linkage between volumes, materials and identification of
        which volumes to tet mesh. The plasma geometry is not included by
        default as it is typically not included in neutronics simulations. The
        reason for this is that the low number density results in minimal
        interaction with neutrons. However, it can be added if the
        include_plasma argument is set to True.

        Returns:
            dictionary: a dictionary of materials and filenames for the reactor
        """

        neutronics_description = []

        for entry in self.shapes_and_components:

            if include_plasma is False and isinstance(
                entry,
                (paramak.Plasma,
                 paramak.PlasmaFromPoints,
                 paramak.PlasmaBoundaries)) is True:
                continue

            if entry.stp_filename is None:
                raise ValueError(
                    "Set Shape.stp_filename for all the \
                                  Reactor entries before using this method"
                )

            if entry.material_tag is None:
                raise ValueError(
                    "set Shape.material_tag for all the \
                                  Reactor entries before using this method"
                )

            neutronics_description.append(entry.neutronics_description())

        # This add the neutronics description for the graveyard which is unique
        # as it is automatically calculated instead of being added by the user.
        # Also the graveyard must have 'Graveyard' as the material name
        if include_graveyard:
            self.make_graveyard()
            neutronics_description.append(
                self.graveyard.neutronics_description())

        return neutronics_description

    def export_neutronics_description(
            self,
            filename: Optional[str] = "manifest.json",
            include_plasma: Optional[bool] = False,
            include_graveyard: Optional[bool] = True) -> str:
        """
        Saves Reactor.neutronics_description to a json file. The resulting json
        file contains a list of dictionaries. Each dictionary entry comprises
        of a material and a filename and optionally a tet_mesh instruction. The
        json file can then be used with the neutronics workflows to create a
        neutronics model. Creating of the neutronics model requires linkage
        between volumes, materials and identification of which volumes to
        tet_mesh. If the filename does not end with .json then .json will be
        added. The plasma geometry is not included by default as it is
        typically not included in neutronics simulations. The reason for this
        is that the low number density results in minimal interactions with
        neutrons. However, the plasma can be added if the include_plasma
        argument is set to True.

        Args:
            filename (str, optional): the filename used to save the neutronics
                description
            include_plasma (Boolean, optional): should the plasma be included.
                Defaults to False as the plasma volume and material has very
                little impact on the neutronics results due to the low density.
                Including the plasma does however slow down the simulation.
            include_graveyard (Boolean, optional): should the graveyard be
                included. Defaults to True as this is needed for DAGMC models.
        """

        path_filename = Path(filename)

        if path_filename.suffix != ".json":
            path_filename = path_filename.with_suffix(".json")

        path_filename.parents[0].mkdir(parents=True, exist_ok=True)

        with open(path_filename, "w") as outfile:
            json.dump(
                self.neutronics_description(
                    include_plasma=include_plasma,
                    include_graveyard=include_graveyard,
                ),
                outfile,
                indent=4,
            )

        print("saved geometry description to ", path_filename)

        return str(path_filename)

    def export_stp(
            self,
            output_folder: Optional[str] = "",
            graveyard_offset: Optional[float] = 100,
            mode: Optional[str] = 'solid') -> List[str]:
        """Writes stp files (CAD geometry) for each Shape object in the reactor
        and the graveyard.

        Args:
            output_folder (str): the folder for saving the stp files to
            graveyard_offset (float, optional): the offset between the largest
                edge of the geometry and inner bounding shell created. Defaults
                to 100.
            mode (str, optional): the object to export can be either
                'solid' which exports 3D solid shapes or the 'wire' which
                exports the wire edges of the shape. Defaults to 'solid'.
        Returns:
            list: a list of stp filenames created
        """

        if len(self.stp_filenames) != len(set(self.stp_filenames)):
            raise ValueError(
                "Set Reactor already contains a shape or component \
                         with this stp_filename",
                self.stp_filenames,
            )

        filenames = []
        for entry in self.shapes_and_components:
            if entry.stp_filename is None:
                raise ValueError(
                    "set .stp_filename property for \
                                 Shapes before using the export_stp method"
                )
            filenames.append(
                str(Path(output_folder) / Path(entry.stp_filename)))
            entry.export_stp(
                filename=Path(output_folder) / Path(entry.stp_filename),
                mode=mode
            )

        # creates a graveyard (bounding shell volume) which is needed for
        # neutronics simulations
        self.make_graveyard(graveyard_offset=graveyard_offset)
        filenames.append(
            str(Path(output_folder) / Path(self.graveyard.stp_filename)))
        self.graveyard.export_stp(
            Path(output_folder) / Path(self.graveyard.stp_filename)
        )

        return filenames

    def export_stl(
            self,
            output_folder: Optional[str] = "",
            graveyard_offset: Optional[float] = 100,
            tolerance: Optional[float] = 0.001) -> List[str]:
        """Writes stl files (CAD geometry) for each Shape object in the reactor

        Args:
            output_folder (str): the folder for saving the stl files to
            graveyard_offset (float, optional): the offset between the largest
                edge of the geometry and inner bounding shell created. Defaults
                to 100.
            tolerance (float):  the precision of the faceting

        Returns:
            list: a list of stl filenames created
        """

        if len(self.stl_filenames) != len(set(self.stl_filenames)):
            raise ValueError(
                "Set Reactor already contains a shape or component \
                         with this stl_filename",
                self.stl_filenames,
            )

        filenames = []
        for entry in self.shapes_and_components:
            print("entry.stl_filename", entry.stl_filename)
            if entry.stl_filename is None:
                raise ValueError(
                    "set .stl_filename property for \
                                 Shapes before using the export_stl method"
                )

            filenames.append(
                str(Path(output_folder) / Path(entry.stl_filename)))
            entry.export_stl(
                Path(output_folder) /
                Path(
                    entry.stl_filename),
                tolerance)

        # creates a graveyard (bounding shell volume) which is needed for
        # neutronics simulations
        self.make_graveyard(graveyard_offset=graveyard_offset)
        filenames.append(
            str(Path(output_folder) / Path(self.graveyard.stl_filename)))
        self.graveyard.export_stl(
            Path(output_folder) / Path(self.graveyard.stl_filename)
        )

        print("exported stl files ", filenames)

        return filenames

    def export_h5m(
            self,
            filename: Optional[str] = 'dagmc.h5m',
            skip_graveyard: Optional[bool] = False,
            tolerance: Optional[float] = 0.001,
            graveyard_offset: Optional[float] = 100) -> str:
        """Converts stl files into DAGMC compatible h5m file using PyMOAB. The
        DAGMC file produced has not been imprinted and merged unlike the other
        supported method which uses Trelis to produce an imprinted and merged
        DAGMC geometry. If the provided filename doesn't end with .h5m it will
        be added

        Args:
            filename (str, optional): filename of h5m outputfile
                Defaults to "dagmc.h5m".
            skip_graveyard (boolean, optional): filename of h5m outputfile
                Defaults to False.
            tolerance (float, optional): the precision of the faceting
                Defaults to 0.001.
            graveyard_offset (float, optional): the offset between the largest
                edge of the geometry and inner bounding shell created. Defaults
                to 100.
        Returns:
            filename: output h5m filename
        """

        path_filename = Path(filename)

        if path_filename.suffix != ".h5m":
            path_filename = path_filename.with_suffix(".h5m")

        path_filename.parents[0].mkdir(parents=True, exist_ok=True)

        moab_core, moab_tags = define_moab_core_and_tags()

        surface_id = 1
        volume_id = 1

        for item in self.shapes_and_components:

            item.export_stl(item.stl_filename, tolerance=tolerance)
            moab_core = add_stl_to_moab_core(
                moab_core,
                surface_id,
                volume_id,
                item.material_tag,
                moab_tags,
                item.stl_filename)
            volume_id += 1
            surface_id += 1

        if skip_graveyard is False:
            self.make_graveyard(graveyard_offset=graveyard_offset)
            self.graveyard.export_stl(self.graveyard.stl_filename)
            volume_id = 2
            surface_id = 2
            moab_core = add_stl_to_moab_core(
                moab_core,
                surface_id,
                volume_id,
                self.graveyard.material_tag,
                moab_tags,
                self.graveyard.stl_filename
            )

        all_sets = moab_core.get_entities_by_handle(0)

        file_set = moab_core.create_meshset()

        moab_core.add_entities(file_set, all_sets)

        moab_core.write_file(str(path_filename))

        return str(path_filename)

    def export_physical_groups(
            self,
            output_folder: Optional[str] = "") -> List[str]:
        """Exports several JSON files containing a look up table which is
        useful for identifying faces and volumes. The output file names are
        generated from .stp_filename properties.

        Args:
            output_folder (str, optional): directory of outputfiles.
                Defaults to "".

        Raises:
            ValueError: if one .stp_filename property is set to None

        Returns:
            list: list of output file names
        """
        filenames = []
        for entry in self.shapes_and_components:
            if entry.stp_filename is None:
                raise ValueError(
                    "set .stp_filename property for \
                                 Shapes before using the export_stp method"
                )
            filenames.append(
                str(Path(output_folder) / Path(entry.stp_filename)))
            entry.export_physical_groups(
                Path(output_folder) / Path(entry.stp_filename))
        return filenames

    def export_svg(
            self,
            filename: Optional[str] = 'reactor.svg',
            projectionDir: Tuple[float, float, float] = (-1.75, 1.1, 5),
            width: Optional[float] = 1000,
            height: Optional[float] = 800,
            marginLeft: Optional[float] = 120,
            marginTop: Optional[float] = 100,
            strokeWidth: Optional[float] = None,
            strokeColor: Optional[Tuple[int, int, int]] = (0, 0, 0),
            hiddenColor: Optional[Tuple[int, int, int]] = (100, 100, 100),
            showHidden: Optional[bool] = True,
            showAxes: Optional[bool] = False) -> str:
        """Exports an svg file for the Reactor.solid. If the filename provided
        doesn't end with .svg it will be added.

        Args:
            filename: the filename of the svg file to be exported. Defaults to
                "reactor.svg".
            projectionDir: The direction vector to view the geometry from
                (x, y, z). Defaults to (-1.75, 1.1, 5)
            width: the width of the svg image produced in pixels. Defaults to
                1000
            height: the height of the svg image produced in pixels. Defaults to
                800
            marginLeft: the number of pixels between the left edge of the image
                and the start of the geometry.
            marginTop: the number of pixels between the top edge of the image
                and the start of the geometry.
            strokeWidth: the width of the lines used to draw the geometry.
                Defaults to None which automatically selects an suitable width.
            strokeColor: the color of the lines used to draw the geometry in
                RGB format with each value between 0 and 255. Defaults to
                (0, 0, 0) which is black.
            hiddenColor: the color of the lines used to draw the geometry in
                RGB format with each value between 0 and 255. Defaults to
               (100, 100, 100) which is light grey.
            showHidden: If the edges obscured by geometry should be included in
                the diagram. Defaults to True.
            showAxes: If the x, y, z axis should be included in the image.
                Defaults to False.

        Returns:
            str: the svg filename created
        """

        path_filename = Path(filename)

        if path_filename.suffix != ".svg":
            path_filename = path_filename.with_suffix(".svg")

        path_filename.parents[0].mkdir(parents=True, exist_ok=True)

        opt = {
            "width": width,
            "height": height,
            "marginLeft": marginLeft,
            "marginTop": marginTop,
            "showAxes": showAxes,
            "projectionDir": projectionDir,
            "strokeColor": strokeColor,
            "hiddenColor": hiddenColor,
            "showHidden": showHidden
        }

        if strokeWidth is not None:
            opt["strokeWidth"] = strokeWidth

        exporters.export(self.solid, str(path_filename), exportType='SVG',
                         opt=opt)

        print("Saved file as ", path_filename)

        return str(path_filename)

    def export_graveyard(
            self,
            graveyard_offset: Optional[float] = 100,
            filename: Optional[str] = "Graveyard.stp") -> str:
        """Writes an stp file (CAD geometry) for the reactor graveyard. This
        is needed for DAGMC simulations. This method also calls
        Reactor.make_graveyard with the offset.

        Args:
            filename (str): the filename for saving the stp file
            graveyard_offset (float): the offset between the largest edge of
                the geometry and inner bounding shell created. Defaults to
                Reactor.graveyard_offset

        Returns:
            str: the stp filename created
        """

        self.make_graveyard(graveyard_offset=graveyard_offset)
        new_filename = self.graveyard.export_stp(Path(filename))

        return new_filename

    def make_graveyard(
            self,
            graveyard_offset: Optional[float] = 100) -> paramak.Shape:
        """Creates a graveyard volume (bounding box) that encapsulates all
        volumes. This is required by DAGMC when performing neutronics
        simulations.

        Args:
            graveyard_offset (float): the offset between the largest edge of
                the geometry and inner bounding shell created. Defaults to
                Reactor.graveyard_offset

        Returns:
            CadQuery solid: a shell volume that bounds the geometry, referred
            to as a graveyard in DAGMC
        """

        self.graveyard_offset = graveyard_offset

        for component in self.shapes_and_components:
            if component.solid is None:
                component.create_solid()

        graveyard_shape = paramak.HollowCube(
            length=self.largest_dimension * 2 + graveyard_offset * 2,
            name="Graveyard",
            material_tag="Graveyard",
            stp_filename="Graveyard.stp",
            stl_filename="Graveyard.stl",
        )

        self.graveyard = graveyard_shape

        return graveyard_shape

    def export_2d_image(
            self,
            filename: Optional[str] = "2d_slice.png",
            xmin: Optional[float] = 0.0,
            xmax: Optional[float] = 900.0,
            ymin: Optional[float] = -600.0,
            ymax: Optional[float] = 600.0) -> str:
        """Creates a 2D slice image (png) of the reactor.

        Args:
            filename (str): output filename of the image created

        Returns:
            str: png filename created
        """

        path_filename = Path(filename)

        if path_filename.suffix != ".png":
            path_filename = path_filename.with_suffix(".png")

        path_filename.parents[0].mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots()

        # creates indvidual patches for each Shape which are combined together
        for entry in self.shapes_and_components:
            patch = entry._create_patch()
            ax.add_collection(patch)

        ax.axis("equal")
        ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        ax.set_aspect("equal", "box")

        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(filename, dpi=100)
        plt.close()

        print("\n saved 2d image to ", str(path_filename))

        return str(path_filename)

    def export_html(
            self,
            filename: Optional[str] = "reactor.html",
            view_plane: Optional[str] = 'RZ'):
        """Creates a html graph representation of the points for the Shape
        objects that make up the reactor. Shapes are colored by their .color
        property. Shapes are also labelled by their .name. If filename provided
        doesn't end with .html then .html will be added. Viewed from the XZ
        plane

        Args:
            filename: the filename used to save the html graph. Defaults to
                reactor.html
            view_plane: The axis to view the points and faceted edges from. The
                options are 'XZ', 'XY', 'YZ', 'YX', 'ZY', 'ZX', 'RZ'. Defaults
                to 'RZ'.
        Returns:
            plotly.Figure(): figure object
        """

        # accesses the Shape wires for each Shape and builds up a list of
        # traces
        all_wires = []
        for entry in self.shapes_and_components:
            if not isinstance(entry.wire, list):
                list_of_wires = [entry.wire]
            else:
                list_of_wires = entry.wire
            all_wires = all_wires + list_of_wires

        fig = paramak.utils.export_wire_to_html(
            wires=all_wires,
            filename=filename,
            view_plane=view_plane,
            facet_splines=True,
            facet_circles=True,
            tolerance=1e-3,
            title="coordinates of the " + self.__class__.__name__ +
            " reactor, viewed from the " + view_plane + " plane",
        )

        return fig

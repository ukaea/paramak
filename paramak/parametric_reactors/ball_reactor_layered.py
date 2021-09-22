
import warnings
from typing import List, Optional, Union

import paramak


class BallReactorLayered(paramak.Reactor):
    """Creates geometry for a simple ball reactor including a plasma, with an
    arbitrary number of inboard and outboard layers.

    Arguments:
    """

    def __init__(
        self,
        inner_bore_radial_thickness: float,
        inboard_layer_thicknesses: list,
        divertor_radial_thickness: float,
        inner_plasma_gap_radial_thickness: float,
        plasma_radial_thickness: float,
        outer_plasma_gap_radial_thickness: float,
        outboard_layer_thicknesses: list,
        elongation: float,
        triangularity: float,
        plasma_gap_vertical_thickness: Optional[float] = None,
        divertor_to_tf_gap_vertical_thickness: Optional[float] = 0,
        number_of_tf_coils: Optional[int] = 12,
        rear_outboard_layer_to_tf_gap: Optional[float] = None,
        pf_coil_radial_thicknesses: Optional[Union[float, List[float]]] = None,
        pf_coil_vertical_thicknesses: Optional[Union[float, List[float]]] = None,
        pf_coil_radial_position: Optional[Union[float, List[float]]] = None,
        pf_coil_vertical_position: Optional[Union[float, List[float]]] = None,
        pf_coil_case_thicknesses: Optional[Union[float, List[float]]] = 10,
        outboard_tf_coil_radial_thickness: float = None,
        outboard_tf_coil_poloidal_thickness: float = None,
        divertor_position: Optional[str] = "both",
        rotation_angle: Optional[str] = 360.0
    ):

        super().__init__([])

        self.method = "trelis"

        self.inner_bore_radial_thickness = inner_bore_radial_thickness
        
        self.inboard_layer_thicknesses = inboard_layer_thicknesses

        self.divertor_radial_thickness = divertor_radial_thickness
        self.inner_plasma_gap_radial_thickness = inner_plasma_gap_radial_thickness
        self.plasma_radial_thickness = plasma_radial_thickness
        self.outer_plasma_gap_radial_thickness = outer_plasma_gap_radial_thickness

        self.outboard_layer_thicknesses = outboard_layer_thicknesses

        self.pf_coil_vertical_position = pf_coil_vertical_position
        self.pf_coil_radial_position = pf_coil_radial_position
        self.pf_coil_radial_thicknesses = pf_coil_radial_thicknesses
        self.pf_coil_vertical_thicknesses = pf_coil_vertical_thicknesses
        self.rear_outboard_layer_to_tf_gap = rear_outboard_layer_to_tf_gap

        self.pf_coil_case_thicknesses = pf_coil_case_thicknesses
        self.outboard_tf_coil_radial_thickness = outboard_tf_coil_radial_thickness
        self.outboard_tf_coil_poloidal_thickness = outboard_tf_coil_poloidal_thickness
        self.divertor_position = divertor_position
        self.rotation_angle = rotation_angle

        self.plasma_gap_vertical_thickness = plasma_gap_vertical_thickness
        self.divertor_to_tf_gap_vertical_thickness = divertor_to_tf_gap_vertical_thickness
        if self.plasma_gap_vertical_thickness is None:
            self.plasma_gap_vertical_thickness = self.outer_plasma_gap_radial_thickness
        
        inner_equatorial_point = (
            inner_bore_radial_thickness 
            + sum(inboard_layer_thicknesses)
            + inner_plasma_gap_radial_thickness
        )

        outer_equatorial_point = \
            inner_equatorial_point + plasma_radial_thickness

        self.major_radius = \
            (outer_equatorial_point + inner_equatorial_point) / 2
        self.minor_radius = \
            self.major_radius - inner_equatorial_point

        self.elongation = elongation
        self.triangularity = triangularity

        self.number_of_tf_coils = number_of_tf_coils
        self.rotation_angle = rotation_angle

        self.offset_from_plasma = [
            self.major_radius - self.minor_radius,
            self.plasma_gap_vertical_thickness,
            self.outer_plasma_gap_radial_thickness,
            self.plasma_gap_vertical_thickness,
            self.major_radius - self.minor_radius]

    @property
    def inboard_layer_thicknesses(self):
        return self._inboard_layer_thicknesses

    @inboard_layer_thicknesses.setter
    def inboard_layer_thicknesses(self, value):
        if type(value) != list:
            raise TypeError("inboard_layer_thicknesses must be a list")
        self._inboard_layer_thicknesses = value

    @property
    def outboard_layer_thicknesses(self):
        return self._outboard_layer_thicknesses

    @outboard_layer_thicknesses.setter
    def outboard_layer_thicknesses(self, value):
        if type(value) != list:
            raise TypeError("outboard_layer_thicknesses must be a list")
        self._outboard_layer_thicknesses = value

    @property
    def rotation_angle(self):
        return self._rotation_angle

    @rotation_angle.setter
    def rotation_angle(self, value):
        if value == 360:
            msg = (
                "360 degree rotation may result in a "
                "Standard_ConstructionError or AttributeError"
            )
            warnings.warn(msg, UserWarning)
        elif value > 360:
            raise ValueError('rotation_angle can not be larger than 360')
        self._rotation_angle = value

    @property
    def pf_coil_vertical_position(self):
        return self._pf_coil_vertical_position

    @pf_coil_vertical_position.setter
    def pf_coil_vertical_position(self, value):
        if not isinstance(value, list) and value is not None:
            raise ValueError("pf_coil_vertical_position must be a list")
        self._pf_coil_vertical_position = value

    @property
    def pf_coil_radial_position(self):
        return self._pf_coil_radial_position

    @pf_coil_radial_position.setter
    def pf_coil_radial_position(self, value):
        if not isinstance(value, list) and value is not None:
            raise ValueError("pf_coil_radial_position must be a list")
        self._pf_coil_radial_position = value

    @property
    def pf_coil_radial_thicknesses(self):
        return self._pf_coil_radial_thicknesses

    @pf_coil_radial_thicknesses.setter
    def pf_coil_radial_thicknesses(self, value):
        if not isinstance(value, list) and value is not None:
            raise ValueError("pf_coil_radial_thicknesses must be a list")
        self._pf_coil_radial_thicknesses = value

    @property
    def pf_coil_vertical_thicknesses(self):
        return self._pf_coil_vertical_thicknesses

    @pf_coil_vertical_thicknesses.setter
    def pf_coil_vertical_thicknesses(self, value):
        if not isinstance(value, list) and value is not None:
            raise ValueError("pf_coil_vertical_thicknesses must be a list")
        self._pf_coil_vertical_thicknesses = value

    @property
    def divertor_position(self):
        return self._divertor_position

    @divertor_position.setter
    def divertor_position(self, value):
        acceptable_values = ["upper", "lower", "both"]
        if value in acceptable_values:
            self._divertor_position = value
        else:
            msg = "divertor_position must be 'upper', 'lower' or 'both'"
            raise ValueError(msg)

    
    def create_solids(self):
        """Insert description"""

        uncut_shapes = []

        uncut_shapes.append(self._make_plasma())
        self._make_radial_build()
        self._make_vertical_build()
        uncut_shapes += self._make_inboard_layers()
        uncut_shapes += self._make_outboard_layers()
        uncut_shapes.append(self._make_divertor())
        uncut_shapes += self._make_tf_coils()
        pf_coils = self._make_pf_coils()

        if pf_coils is None:
            shapes_and_components = uncut_shapes
        else:
            for shape in uncut_shapes:
                for pf_coil in pf_coils:
                    shape.solid = shape.solid.cut(pf_coil.solid)
            shapes_and_components = pf_coils + uncut_shapes

        self._shapes_and_components = shapes_and_components

    def _make_plasma(self):

        plasma = paramak.Plasma(
            major_radius=self.major_radius,
            minor_radius=self.minor_radius,
            elongation=self.elongation,
            triangularity=self.triangularity,
            rotation_angle=self.rotation_angle,
        )

        self._plasma = plasma
        return self._plasma

    def _make_radial_build(self):

        # this is the radial build sequence, where one component stops and
        # another starts

        self._inner_bore_start_radius = 0
        self._inner_bore_end_radius = (
            self._inner_bore_start_radius + self.inner_bore_radial_thickness
        )

        # group all inboard layers together
        self._inboard_layers_start_radius = self._inner_bore_end_radius
        self._inboard_layers_end_radius = (
            self._inboard_layers_start_radius
            + sum(self.inboard_layer_thicknesses)
        )

        self._divertor_start_radius = self._inboard_layers_end_radius
        self._divertor_end_radius = (
            self._inboard_layers_end_radius
            + self.divertor_radial_thickness
        )

        # group all outboard layers together
        self._outboard_layers_start_radius = (
            self._inboard_layers_end_radius
            + self.inner_plasma_gap_radial_thickness
            + self.plasma_radial_thickness
            + self.outer_plasma_gap_radial_thickness
        )
        self._outboard_layers_end_radius = (
            self._outboard_layers_start_radius
            + sum(self.outboard_layer_thicknesses)
        )

        if self.rear_outboard_layer_to_tf_gap is not None:
            self._tf_coil_start_radius = self._outboard_layers_end_radius + \
                self.rear_outboard_layer_to_tf_gap
            self._tf_coil_end_radius = (
                self._tf_coil_start_radius
                + self.outboard_tf_coil_radial_thickness
            )

    def _make_vertical_build(self):
        
        # this is the vertical build sequence, components build on each other
        # in a similar manner to the radial build

        # group all outboard layers together
        self._outboard_layers_start_height = (
            self._plasma.high_point[1]
            + self.plasma_gap_vertical_thickness
        )
        self._outboard_layers_end_height = (
            self._outboard_layers_start_height
            + sum(self.outboard_layer_thicknesses)
        )

        self._tf_coil_start_height = self._outboard_layers_end_height + \
            self.divertor_to_tf_gap_vertical_thickness

        self._center_column_shield_height = self._outboard_layers_end_height * 2

    def _make_inboard_layers(self):

        inboard_layers = []

        layer_number = 1
        layer_radius = self._inboard_layers_start_radius

        for layer_thickness in self.inboard_layer_thicknesses:

            inboard_layer = paramak.CenterColumnShieldCylinder(
                height=self._tf_coil_start_height * 2,
                inner_radius=layer_radius,
                outer_radius=layer_radius + layer_thickness,
                rotation_angle=self.rotation_angle,
                stp_filename="inboard_layer_" + str(layer_number) + ".stp",
                stl_filename="inboard_layer_" + str(layer_number) + ".stl",
                name="inboard_layer_" + str(layer_number),
                material_tag="inboard_layer_" + str(layer_number) + "_mat",
                color=(0, 0, 1)
            )

            inboard_layers.append(inboard_layer)

            layer_number += 1
            layer_radius += layer_thickness
        
        self._inboard_layers = inboard_layers

        return self._inboard_layers

        # we need to set self._inboard_layers so that we can update them later

    def _make_outboard_layers(self):

        self._center_column_cutter = paramak.CenterColumnShieldCylinder(
            # extra 0.5 to ensure overlap
            height=self._center_column_shield_height * 1.5,
            inner_radius=0,
            outer_radius=self._inboard_layers_end_radius,
            rotation_angle=360,
            color=(0., 0., 1.)
        )

        outboard_layers = []

        layer_number = 1
        layer_offset = self.offset_from_plasma
        
        for layer_thickness in self.outboard_layer_thicknesses:

            outboard_layer = paramak.BlanketFP(
                plasma=self._plasma,
                thickness=layer_thickness,
                offset_from_plasma=layer_offset,
                start_angle=-180,
                stop_angle=180,
                rotation_angle=self.rotation_angle,
                stp_filename="outboard_layer_" + str(layer_number) + ".stp",
                stl_filename="outboard_layer_" + str(layer_number) + ".stl",
                name="outboard_layer_" + str(layer_number),
                material_tag="outboard_layer_" + str(layer_number) + "_mat",
                color=(0., 1., 0.498),
                cut=[self._center_column_cutter]
            )

            outboard_layers.append(outboard_layer)

            layer_number += 1
            layer_offset = [i + layer_thickness for i in layer_offset]

        self._outboard_layers = outboard_layers

        return self._outboard_layers


    def _make_divertor(self):

        self._outboard_layer_envelope = paramak.BlanketFP(
            plasma=self._plasma,
            thickness=sum(self.outboard_layer_thicknesses),
            offset_from_plasma=self.offset_from_plasma,
            start_angle=-180,
            stop_angle=180,
            rotation_angle=self.rotation_angle
        )

        divertor_height = self._outboard_layers_end_height * 2

        divertor_height_top = divertor_height
        divertor_height_bottom = -divertor_height

        if self.divertor_position == "lower":
            divertor_height_top = 0
        elif self.divertor_position == "upper":
            divertor_height_bottom = 0
        self._divertor = paramak.RotateStraightShape(
            points=[
                (self._divertor_start_radius, divertor_height_bottom),
                (self._divertor_end_radius, divertor_height_bottom),
                (self._divertor_end_radius, divertor_height_top),
                (self._divertor_start_radius, divertor_height_top)
            ],
            intersect=self._outboard_layer_envelope,
            stp_filename="divertor.stp",
            stl_filename="divertor.stl",
            name="divertor",
            material_tag="divertor_mat",
            color=(1., 0.667, 0.),
            rotation_angle=self.rotation_angle
        )

        # cut the outboard layers
        for component in self._outboard_layers:
            component.cut.append(self._divertor)

        return self._divertor

    def _make_pf_coils(self):
        if None not in [self.pf_coil_vertical_thicknesses,
                        self.pf_coil_radial_thicknesses,
                        self.pf_coil_vertical_position,
                        self.pf_coil_radial_position]:
            list_of_components = []

            # TODO make use of counter in the name attribute

            center_points = [
                (x, y) for x, y in zip(
                    self.pf_coil_radial_position, self.pf_coil_vertical_position)]

            self._pf_coils = self._pf_coil = paramak.PoloidalFieldCoilSet(
                heights=self.pf_coil_vertical_thicknesses,
                widths=self.pf_coil_radial_thicknesses,
                center_points=center_points,
                rotation_angle=self.rotation_angle,
                stp_filename='pf_coils.stp',
                stl_filename='pf_coils.stl',
                name="pf_coil",
                material_tag="pf_coil_mat",
            )
            list_of_components.append(self._pf_coil)

            if self.pf_coil_case_thicknesses is not None:
                self._pf_coils_casing = paramak.PoloidalFieldCoilCaseSetFC(
                    pf_coils=self._pf_coil,
                    casing_thicknesses=self.pf_coil_case_thicknesses,
                    rotation_angle=self.rotation_angle,
                    stp_filename='pf_coil_cases.stp',
                    stl_filename='pf_coil_cases.stl',
                    name="pf_coil_case",
                    material_tag="pf_coil_case_mat",
                )
                list_of_components.append(self._pf_coils_casing)

            return list_of_components
        else:
            print(
                'pf_coil_vertical_thicknesses, pf_coil_radial_thicknesses, '
                'pf_coil_radial_position, pf_coil_vertical_position not '
                'so not making pf coils')
            return None

    def _make_tf_coils(self):
        comp = []
        # checks that all the required information has been input by the user
        if None not in [
                self.rear_outboard_layer_to_tf_gap,
                self.outboard_tf_coil_radial_thickness,
                self.outboard_tf_coil_poloidal_thickness,
                self.number_of_tf_coils] and self.number_of_tf_coils > 1:

            self._tf_coil = paramak.ToroidalFieldCoilRectangle(
                with_inner_leg=False,
                horizontal_start_point=(
                    self._inboard_tf_coils_start_radius,
                    self._tf_coil_start_height),
                vertical_mid_point=(
                    self._tf_coil_start_radius, 0),
                thickness=self.outboard_tf_coil_radial_thickness,
                number_of_coils=self.number_of_tf_coils,
                distance=self.outboard_tf_coil_poloidal_thickness,
                stp_filename="tf_coil.stp",
                name="tf_coil",
                material_tag="tf_coil_mat",
                stl_filename="tf_coil.stl",
                rotation_angle=self.rotation_angle
            )
            comp = [self._tf_coil]
        return comp

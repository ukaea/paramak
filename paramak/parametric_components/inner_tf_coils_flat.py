
import math

import numpy as np
from paramak import ExtrudeStraightShape


class InnerTfCoilsFlat(ExtrudeStraightShape):
    """A tf coil volume with straight inner and outer profiles and
    constant gaps between each coil.

    Args:
        height (float): height of tf coils.
        inner_radius (float): inner radius of tf coils.
        outer_radius (float): outer radius of tf coils.
        number_of_coils (int): number of tf coils.
        gap_size (float): gap between adjacent tf coils.
        azimuth_start_angle (float, optional): defaults to 0.0.
        stp_filename (str, optional): defaults to "InnerTfCoilsFlat.stp".
        stl_filename (str, optional): defaults to "InnerTfCoilsFlat.stl".
        material_tag (str, optional): defaults to "inner_tf_coil_mat".
        workplane (str, optional):defaults to "XY".
        rotation_axis (str, optional): Defaults to "Z".
    """

    def __init__(
        self,
        height,
        inner_radius,
        outer_radius,
        number_of_coils,
        gap_size,
        azimuth_start_angle=0.0,
        stp_filename="InnerTfCoilsFlat.stp",
        stl_filename="InnerTfCoilsFlat.stl",
        material_tag="inner_tf_coil_mat",
        workplane="XY",
        rotation_axis="Z",
        **kwargs
    ):

        super().__init__(
            distance=height,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            material_tag=material_tag,
            workplane=workplane,
            rotation_axis=rotation_axis,
            **kwargs
        )

        self.azimuth_start_angle = azimuth_start_angle
        self.height = height
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.number_of_coils = number_of_coils
        self.gap_size = gap_size
        self.distance = height

    @property
    def azimuth_start_angle(self):
        return self._azimuth_start_angle

    @azimuth_start_angle.setter
    def azimuth_start_angle(self, value):
        self._azimuth_start_angle = value

    @property
    def azimuth_placement_angle(self):
        self.find_azimuth_placement_angle()
        return self._azimuth_placement_angle

    @azimuth_placement_angle.setter
    def azimuth_placement_angle(self, value):
        self._azimuth_placement_angle = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def distance(self):
        return self.height

    @distance.setter
    def distance(self, value):
        self._distance = value

    @property
    def inner_radius(self):
        return self._inner_radius

    @inner_radius.setter
    def inner_radius(self, inner_radius):
        self._inner_radius = inner_radius

    @property
    def outer_radius(self):
        return self._outer_radius

    @outer_radius.setter
    def outer_radius(self, outer_radius):
        self._outer_radius = outer_radius

    @property
    def number_of_coils(self):
        return self._number_of_coils

    @number_of_coils.setter
    def number_of_coils(self, number_of_coils):
        self._number_of_coils = number_of_coils

    @property
    def gap_size(self):
        return self._gap_size

    @gap_size.setter
    def gap_size(self, gap_size):
        self._gap_size = gap_size

    def find_points(self):
        """Finds the points that describe the 2D profile of the tf coil shape"""

        if self.gap_size * self.number_of_coils > 2 * math.pi * self.inner_radius:
            raise ValueError('gap_size is too large')

        theta_inner = (
            (2 * math.pi * self.inner_radius) - (self.gap_size * self.number_of_coils)
        ) / (self.inner_radius * self.number_of_coils)
        omega_inner = math.asin(self.gap_size / (2 * self.inner_radius))

        theta_outer = (
            (2 * math.pi * self.outer_radius) - (self.gap_size * self.number_of_coils)
        ) / (self.outer_radius * self.number_of_coils)
        omega_outer = math.asin(self.gap_size / (2 * self.outer_radius))

        # inner points
        point_1 = (
            (self.inner_radius * math.cos(-omega_inner)),
            (-self.inner_radius * math.sin(-omega_inner)),
        )
        point_3 = (
            (
                self.inner_radius * math.cos(theta_inner) * math.cos(-omega_inner)
                + self.inner_radius * math.sin(theta_inner) * math.sin(-omega_inner)
            ),
            (
                -self.inner_radius * math.cos(theta_inner) * math.sin(-omega_inner)
                + self.inner_radius * math.sin(theta_inner) * math.cos(-omega_inner)
            ),
        )

        # outer points
        point_4 = (
            (self.outer_radius * math.cos(-omega_outer)),
            (-self.outer_radius * math.sin(-omega_outer)),
        )
        point_6 = (
            (
                self.outer_radius * math.cos(theta_outer) * math.cos(-omega_outer)
                + self.outer_radius * math.sin(theta_outer) * math.sin(-omega_outer)
            ),
            (
                -self.outer_radius * math.cos(theta_outer) * math.sin(-omega_outer)
                + self.outer_radius * math.sin(theta_outer) * math.cos(-omega_outer)
            ),
        )

        points = [
            (point_1[0], point_1[1]),
            (point_3[0], point_3[1]),
            (point_6[0], point_6[1]),
            (point_4[0], point_4[1]),
        ]

        self.points = points

    def find_azimuth_placement_angle(self):
        """Calculates the azimuth placement angles based on the number of tf
        coils"""

        angles = list(
            np.linspace(
                0 + self.azimuth_start_angle,
                360 + self.azimuth_start_angle,
                self.number_of_coils,
                endpoint=False))

        self.azimuth_placement_angle = angles

import scipy
import math

import numpy as np

from paramak import RotateMixedShape


class BlanketConstantThicknessD(RotateMixedShape):
    """

    :param thickness:  the thickness of the blanket (cm)
    :type thickness: float


    :return: a shape object that has generic functionality
    :rtype: paramak shape object
    """

    def __init__(
        self,
        height,
        thickness,
        minor_radius,
        workplane="XZ",
        points=None,
        stp_filename=None,
        rotation_angle=360,
        azimuth_placement_angle=0,
        solid=None,
        color=None,
        name=None,
        material_tag=None,
        cut=None,
    ):

        super().__init__(
            points,
            workplane,
            name,
            color,
            material_tag,
            stp_filename,
            azimuth_placement_angle,
            solid,
            rotation_angle,
            cut,
        )

        self.height = height
        self.thickness = thickness
        self.minor_radius = minor_radius
        self.points = points

    @property
    def points(self):
        self.find_points()
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    @property
    def cut(self):
        self.cut_inner_shape()
        return self._cut

    @cut.setter
    def cut(self, cut):
        self._cut = cut

    @property
    def minor_radius(self):
        return self._minor_radius

    @minor_radius.setter
    def minor_radius(self, minor_radius):
        self._minor_radius = minor_radius

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, thickness):
        self._thickness = thickness

    def cut_inner_shape(self):
        # TODO: make this follow the curve of the plasma
        F = (self.minor_radius + self.thickness, self.height/2 - self.thickness)
        G = (self.minor_radius + self.thickness, -(self.height/2 - self.thickness))
        H = (self.minor_radius + self.height/2, 0)
        inner_shape = RotateMixedShape(
            points=[
                (*F, 'straight'),
                (*G, 'circle'),
                (*H, 'circle')
            ],
            rotation_angle=self.rotation_angle)
        self.cut = inner_shape

    def find_points(self):
        # TODO: make this follow the curve of the plasma
        A = (self.minor_radius, self.height/2)
        B = (self.minor_radius + self.thickness, self.height/2)

        C = (self.minor_radius + self.thickness + self.height/2, 0)

        D = (self.minor_radius + self.thickness, -self.height/2)
        E = (self.minor_radius, -self.height/2)

        points = [
            (*A, 'straight'),
            (*B, 'circle'),
            (*C, 'circle'),
            (*D, 'straight'),
            (*E, 'straight'),
            (*A, 'straight'),  # is this necessary ?
        ]
        self.points = points

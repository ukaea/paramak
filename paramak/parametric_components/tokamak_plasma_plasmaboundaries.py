import math
from pathlib import Path

import numpy as np
import scipy
from plasmaboundaries import get_separatrix_coordinates

from paramak import RotateSplineShape


class PlasmaBoundaries(RotateSplineShape):
    """Creates a double null tokamak plasma shape that is controlled
       by 4 shaping parameters.

    :param major_radius: the major radius of the plasma (cm)
    :type major_radius: float
    :param minor_radius: the minor radius of the plasma (cm)
    :type minor_radius: float
    :param triangularity: the triangularity of the plasma
    :type triangularity: float
    :param elongation: the elongation of the plasma
    :type elongation: float
    :param vertical_displacement: the vertical_displacement of the plasma (cm)
    :type vertical_displacement: float
    :param num_points: number of points to described the shape
    :type num_points: int
    :param configuration: plasma configuration
     ("non-null", "single-null", "double-null"). Defaults to "non-null")
    :type configuration: str
    :param x_point_shift: Shift parameters for locating the X points in [0, 1].
     Default to 0.1.
    :type x_point_shift: float

    :return: a shape object that has generic functionality with 4 attributes
       (outer_equatorial_point, inner_equatorial_point, high_point, low_point)
       as tuples of 2 floats
    :rtype: paramak shape object
    """

    def __init__(
        self,
        name='plasma',
        material_tag='DT_plasma',
        A=0.05,
        elongation=2.0,
        major_radius=450,
        minor_radius=150,
        triangularity=0.55,
        vertical_displacement=0,
        num_points=50,
        configuration="non-null",
        x_point_shift=0.1,
        stp_filename="plasma.stp",
        color=None,
        rotation_angle=360,
        azimuth_placement_angle=0,
        **kwargs
    ):

        default_dict = {'points':None,
                        'workplane':"XZ",
                        'solid':None,
                        'hash_value':None,
                        'intersect':None,
                        'cut':None
        }

        for arg in kwargs:
            if arg in default_dict:
                default_dict[arg] = kwargs[arg]

        super().__init__(
            name=name,
            color=color,
            material_tag=material_tag,
            stp_filename=stp_filename,
            azimuth_placement_angle=azimuth_placement_angle,
            rotation_angle=rotation_angle,
            **default_dict
        )

        # properties needed for plasma shapes
        self.A = A
        self.elongation = elongation
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.triangularity = triangularity
        self.vertical_displacement = vertical_displacement
        self.num_points = num_points
        # self.points = points
        self.configuration = configuration
        self.x_point_shift = x_point_shift

        self.outer_equatorial_point = None
        self.inner_equatorial_point = None
        self.high_point = None
        self.low_point = None
        self.lower_x_point, self.upper_x_point = self.compute_x_points()

    @property
    def points(self):
        self.find_points()
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

    @property
    def vertical_displacement(self):
        return self._vertical_displacement

    @vertical_displacement.setter
    def vertical_displacement(self, value):
        self._vertical_displacement = value

    @property
    def openmc_install_directory(self):
        return self._openmc_install_directory

    @openmc_install_directory.setter
    def openmc_install_directory(self, openmc_install_directory):
        if Path(openmc_install_directory).exists() is False:
            raise ValueError("openmc_install_directory is out of range")
        else:
            self._openmc_install_directory = openmc_install_directory

    @property
    def minor_radius(self):
        return self._minor_radius

    @minor_radius.setter
    def minor_radius(self, value):
        if value > 2000 or value < 1:
            raise ValueError("minor_radius is out of range")
        else:
            self._minor_radius = value

    @property
    def major_radius(self):
        return self._major_radius

    @major_radius.setter
    def major_radius(self, value):
        if value > 2000 or value < 1:
            raise ValueError("major_radius is out of range")
        else:
            self._major_radius = value

    @property
    def elongation(self):
        return self._elongation

    @elongation.setter
    def elongation(self, value):
        if value > 10 or value < 0:
            raise ValueError("elongation is out of range")
        else:
            self._elongation = value

    def compute_x_points(self):
        """Computes the location of X points based on plasma parameters and
         configuration

        Returns:
            ((float, float), (float, float)): lower and upper x points
             coordinates. None if no x points
        """
        lower_x_point, upper_x_point = None, None  # non-null config
        minor_radius, major_radius = self.minor_radius, self.major_radius
        shift = self.x_point_shift
        elongation = self.elongation
        triangularity = self.triangularity
        if self.configuration == "single-null" or \
           self.configuration == "double-null":
            # no X points for non-null config
            lower_x_point = (
                1-(1+shift)*triangularity*minor_radius,
                -(1+shift)*elongation*minor_radius + self.vertical_displacement
            )

            if self.configuration == "double-null":
                # upper_x_point is up-down symmetrical
                upper_x_point = (
                    lower_x_point[0],
                    (1+shift)*elongation*minor_radius +
                    self.vertical_displacement
                )
        return lower_x_point, upper_x_point

    def find_points(self):
        """Finds the XZ points that describe the 2D profile of the plasma.
        """
        aspect_ratio = self.minor_radius/self.major_radius
        params = {
            "A": self.A,
            "aspect_ratio": aspect_ratio,
            "elongation": self.elongation,
            "triangularity": self.triangularity
        }
        points = get_separatrix_coordinates(params, self.configuration)
        # add vertical displacement
        points[:, 1] += self.vertical_displacement
        # rescale to cm
        points[:] *= self.major_radius

        # remove unnecessary points
        lower_x_point, upper_x_point = self.compute_x_points()
        # if non-null these are the y bounds
        lower_point_y = -self.elongation*aspect_ratio + \
            self.vertical_displacement
        upper_point_y = self.elongation*aspect_ratio + \
            self.vertical_displacement
        # else use x points
        if self.configuration == "single-null" or \
           self.configuration == "double-null":
            lower_point_y = lower_x_point[1]
            if self.configuration == "double-null":
                upper_point_y = upper_x_point[1]
        points2 = []
        for p in points:
            if p[1] >= lower_point_y and p[1] <= upper_point_y:
                points2.append(p)
        points = points2

        # add spline to points
        points = [[p[0], p[1], "spline"] for p in points]
        self.points = points

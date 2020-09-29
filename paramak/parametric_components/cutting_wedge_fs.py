from collections import Iterable

import cadquery as cq

from paramak import RotateStraightShape


class CuttingWedgeFS(RotateStraightShape):

    def __init__(
        self,
        shape,
        name=None,
        color=(0.5, 0.5, 0.5),
        stp_filename="CuttingSlice.stp",
        stl_filename="CuttingSlice.stl",
        rotation_angle=360,
        material_tag="cutting_slice_mat",
        azimuth_placement_angle=0,
        **kwargs
    ):

        default_dict = {
            "points": None,
            "workplane": "XZ",
            "solid": None,
            "intersect": None,
            "cut": None,
            "union": None,
            "tet_mesh": None,
            "physical_groups": None,
        }

        for arg in kwargs:
            if arg in default_dict:
                default_dict[arg] = kwargs[arg]

        super().__init__(
            name=name,
            color=color,
            material_tag=material_tag,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            azimuth_placement_angle=azimuth_placement_angle,
            rotation_angle=rotation_angle,
            hash_value=None,
            **default_dict
        )

        self.shape = shape
        self.create_wedge()

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        self._shape = value

    @property
    def solid(self):
        return self._solid

    @solid.setter
    def solid(self, value):
        self._solid = value

    def create_wedge(self):

        if self.shape.rotation_angle == 360:

            self.solid = None

        else:

            # self.shape.solid cannot be called because this calls create_solid() for the tf coil
            # this causes the build to be restarted
            # an estimation of the maximum dimension can be made with the points
            max_dimension = 0
            for point in self.shape.points:
                if abs(point[0]) > max_dimension:
                    max_dimension = abs(point[0])
                if abs(point[1]) > max_dimension:
                    max_dimension = abs(point[1])

            max_dimension = max_dimension * 3

            points = [
                (0, max_dimension),
                (max_dimension, max_dimension),
                (max_dimension, -max_dimension),
                (0, -max_dimension)
            ]

            solid = (
                cq.Workplane(self.workplane)
                .polyline(points)
                .close()
                .revolve(360 - self.shape.rotation_angle)
            )

            solid = solid.rotate(
                (0, 0, 1), (0, 0, -1), 360 - self.shape.rotation_angle
            )

            self.solid = solid

            return solid

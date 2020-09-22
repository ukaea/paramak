from collections import Iterable

import cadquery as cq

from paramak import Shape

from cadquery import exporters


class SweepStraightShape(Shape):
    """Sweeps a 2D shape created from points connected with straight lines along a
    defined spline path to create a 3D CadQuery solid.

    Args:
        points (list of tuples each containing X (float), Z (float)): A list of XY, YZ
            or XZ coordinates connected by straight connections which define the 2D shape
            to be swept. The coordinates are defined with respect to origins at the first
            and last points of the spline path.

    Returns:
        a paramak shape object: a Shape object that has generic functionality
    """

    def __init__(
        self,
        points,
        path_points,
        path_workplane="XZ",
        workplane="XY",
        name=None,
        color=(0.5, 0.5, 0.5),
        material_tag=None,
        stp_filename="SweepStraightShape.stp",
        stl_filename="SweepStraightShape.stl",
        azimuth_placement_angle=0,
        solid=None,
        cut=None,
        intersect=None,
        union=None,
        **kwargs
    ):

        default_dict = {"tet_mesh": None,
                        "physical_groups": None,
                        "hash_value": None}

        for arg in kwargs:
            if arg in default_dict:
                default_dict[arg] = kwargs[arg]

        super().__init__(
            points=points,
            name=name,
            color=color,
            material_tag=material_tag,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            azimuth_placement_angle=azimuth_placement_angle,
            workplane=workplane,
            cut=cut,
            intersect=intersect,
            union=union,
            **default_dict
        )

        self.path_points = path_points
        self.path_workplane = path_workplane
        self.solid = solid

    @property
    def solid(self):
        if self.get_hash() != self.hash_value:
            self.create_solid()
        return self._solid

    @solid.setter
    def solid(self, value):
        self._solid = value

    @property
    def path_points(self):
        return self._path_points

    @path_points.setter
    def path_points(self, value):
        self._path_points = value

    @property
    def path_workplane(self):
        return self._path_workplane

    @path_workplane.setter
    def path_workplane(self, value):
        if value[0] != self.workplane[0]:
            raise ValueError(
                "workplane and path_workplane must start with the same letter"
            )
        elif value == self.workplane:
            raise ValueError(
                "workplane and path_workplane must be different"
            )
        else:
            self._path_workplane = value

    def create_solid(self):
        """Insert docstring"""

        # print('create_solid()') has been called')

        path = cq.Workplane(self.path_workplane).spline(self.path_points)
        distance = float(self.path_points[-1][1] - self.path_points[0][1])

        if self.workplane == "XZ" or self.workplane == "YX" or self.workplane == "ZY":
            distance = -distance

        solid = (
            cq.Workplane(self.workplane)
            .workplane(offset=self.path_points[0][1])
            .moveTo(self.path_points[0][0], 0)
            .workplane()
            .polyline(self.points)
            .close()
            .moveTo(-self.path_points[0][0], 0)
            .workplane(offset=distance)
            .moveTo(self.path_points[-1][0], 0)
            .workplane()
            .polyline(self.points)
            .close()
            .sweep(path, multisection=True)
        )

        # Checks if the azimuth_placement_angle is a list of angles
        if isinstance(self.azimuth_placement_angle, Iterable):
            rotated_solids = []
            # Perform seperate rotations for each angle
            for angle in self.azimuth_placement_angle:
                rotated_solids.append(
                    solid.rotate(
                        (0, 0, -1), (0, 0, 1), angle))
            solid = cq.Workplane(self.workplane)

            # Joins the seperate solids together
            for i in rotated_solids:
                solid = solid.union(i)
        else:
            # Peform rotations for a single azimuth_placement_angle angle
            solid = solid.rotate(
                (0, 0, 1), (0, 0, -1), self.azimuth_placement_angle)

        self.perform_boolean_operations(solid)

        return solid

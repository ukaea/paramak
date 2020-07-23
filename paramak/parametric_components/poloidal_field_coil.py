from paramak import RotateStraightShape


class PoloidalFieldCoil(RotateStraightShape):
    """Creates a rectangular poloidal field coil

    :param height: the vertical (Z axis) height of the coil (cm)
    :type height: float
    :param width: the horizontal (X axis) width of the coil (cm)
    :type width: float
    :param center_point: the center of the coil (X,Z) values (cm)
    :type center_point: tuple of floats

    :return: a shape object that has generic functionality
    :rtype: paramak shape object
    """

    def __init__(
        self,
        height,
        width,
        center_point,
        rotation_angle=360,
        stp_filename="PoloidalFieldCoil.stp",
        color=None,
        azimuth_placement_angle=0,
        name='pf_coil',
        material_tag="pf_coil_mat",
        cut=None,
    ):

        super().__init__(
            points=None,
            workplane='XZ',
            name=name,
            color=color,
            material_tag=material_tag,
            stp_filename=stp_filename,
            azimuth_placement_angle=azimuth_placement_angle,
            solid=None,
            rotation_angle=rotation_angle,
            cut=cut,
            hash_value=None,
        )

        self.center_point = center_point
        self.height = height
        self.width = width

    @property
    def points(self):
        self.find_points()
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    @property
    def center_point(self):
        return self._center_point

    @center_point.setter
    def center_point(self, center_point):
        self._center_point = center_point

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    def find_points(self):
        """Finds the XZ points joined by straight connections that describe the 2D
        profile of the poloidal field coil shape."""

        points = [
            (
                self.center_point[0] + self.width / 2.0,
                self.center_point[1] + self.height / 2.0,
            ),  # upper right
            (
                self.center_point[0] + self.width / 2.0,
                self.center_point[1] - self.height / 2.0,
            ),  # lower right
            (
                self.center_point[0] - self.width / 2.0,
                self.center_point[1] - self.height / 2.0,
            ),  # lower left
            (
                self.center_point[0] - self.width / 2.0,
                self.center_point[1] + self.height / 2.0,
            ),  # upper left
            (
                self.center_point[0] + self.width / 2.0,
                self.center_point[1] + self.height / 2.0,
            ),
        ]

        self.points = points


from paramak import RotateMixedShape


class BlanketConstantThicknessArcH(RotateMixedShape):
    """An outboard blanket volume that follows the curvature of a circular
    arc and a constant blanket thickness. The upper and lower edges continue
    horizontally for the thickness of the blanket to back of the blanket.

    Arguments:
        inner_mid_point ((float, float)): the x,z coordinates of the mid
            point on the inner surface of the blanket.
        inner_upper_point ((float, float)): the x,z coordinates of the upper
            point on the inner surface of the blanket.
        inner_lower_point ((float, float)): the x,z coordinates of the lower
            point on the inner surface of the blanket.
        thickness (float): the radial thickness of the blanket in cm.
        stp_filename (str, optional): Defaults to
            "BlanketConstantThicknessArcH.stp".
        stl_filename (str, optional): Defaults to
            "BlanketConstantThicknessArcH.stl".
        material_tag (str, optional): Defaults to "blanket_mat".
    """

    def __init__(
        self,
        inner_mid_point,
        inner_upper_point,
        inner_lower_point,
        thickness,
        stp_filename="BlanketConstantThicknessArcH.stp",
        stl_filename="BlanketConstantThicknessArcH.stl",
        material_tag="blanket_mat",
        **kwargs
    ):

        super().__init__(
            material_tag=material_tag,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            **kwargs
        )

        self.inner_upper_point = inner_upper_point
        self.inner_lower_point = inner_lower_point
        self.inner_mid_point = inner_mid_point
        self.thickness = thickness

    def find_points(self):

        self.points = [
            (self.inner_upper_point[0], self.inner_upper_point[1], "circle"),
            (self.inner_mid_point[0], self.inner_mid_point[1], "circle"),
            (self.inner_lower_point[0], self.inner_lower_point[1], "straight"),
            (
                self.inner_lower_point[0] + abs(self.thickness),
                self.inner_lower_point[1],
                "circle",
            ),
            (
                self.inner_mid_point[0] + abs(self.thickness),
                self.inner_mid_point[1],
                "circle",
            ),
            (
                self.inner_upper_point[0] + abs(self.thickness),
                self.inner_upper_point[1],
                "straight",
            )
        ]

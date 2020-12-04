
from paramak import ExtrudeCircleShape


class PortCutterCircular(ExtrudeCircleShape):
    """Creates an extruded shape with a circular section that is used to cut
    other components (eg. blanket, vessel,..) in order to create ports.

    Args:
        center_point ((float, float)): Defaults to (0, 0).
        radius (float): radius (cm) of port.
        distance (float): extruded distance (cm) of the cutter.
        stp_filename (str, optional): defaults to "PortCutterCircular.stp".
        stl_filename (str, optional): defaults to "PortCutterCircular.stl".
        name (str, optional): defaults to "circular_port_cutter".
        material_tag (str, optional): defaults to "circular_port_cutter_mat".
        extrusion_start_offset (float, optional): the distance between 0 and
            the start of the extrusion. Defaults to 1..
    """

    def __init__(
        self,
        radius,
        distance,
        center_point=(0, 0),
        workplane="ZY",
        rotation_axis="Z",
        extrusion_start_offset=1.,
        stp_filename="PortCutterCircular.stp",
        stl_filename="PortCutterCircular.stl",
        name="circular_port_cutter",
        material_tag="circular_port_cutter_mat",
        **kwargs
    ):
        super().__init__(
            workplane=workplane,
            rotation_axis=rotation_axis,
            extrusion_start_offset=extrusion_start_offset,
            radius=radius,
            extrude_both=False,
            name=name,
            material_tag=material_tag,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            distance=distance,
            **kwargs
        )

        self.center_point = center_point
        self.radius = radius

    def find_points(self):
        self.points = [self.center_point]

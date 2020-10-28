from paramak import ExtrudeCircleShape


class CoolantChannelRingStraight(ExtrudeCircleShape):
    """A ring of equally-spaced circular straight coolant channels with
    constant thickness.

    Arguments:
        height (float): height of each coolant channel in ring.
        channel_radius (float): radius of each coolant channel in ring.
        number_of_coolant_channels (float): number of coolant channels in ring.
        stp_filename (str, optional): Defaults to 
            "CoolantChannelRingStraight.stp".
        stl_filename (str, optional): Defaults to
            "CoolantChannelRingStraight.stl".
        material_tag (str, optional): Defaults to "coolant_channel_mat".
    """

    def __init__(
        self,
        height,
        channel_radius,
        number_of_coolant_channels,
        stp_filename="CoolantChannelRingStraight.stp",
        stl_filename="CoolantChannelRingStraight.stl",
        material_tag="coolant_channel_mat",
        **kwargs
    ):

        super().__init__(
            material_tag=material_tag,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            **kwargs
        )

        self.height = height
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
    
    @property
    def channel_radius(self):
        return self._channel_radius

    @channel_radius.setter
    def channel_radius(self, channel_radius):
        self._channel_radius = channel_radius

    @property
    def number_of_coolant_channels(self):
        return self._number_of_coolant_channels

    @number_of_coolant_channels.setter
    def number_of_coolant_channels(self, number_of_coolant_channels):
        self._number_of_coolant_channels = number_of_coolant_channels

    def 
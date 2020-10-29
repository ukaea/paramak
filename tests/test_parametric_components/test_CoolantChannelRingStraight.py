
import os
import math
import unittest
from pathlib import Path

import paramak
import pytest


class test_CoolantChannelRingStraight(unittest.TestCase):
    def test_CoolantChannelRingStraight_creation(self):
        """creates a coolant channel ring using the CoolantChannelRingStraight parametric shape
        and checks that a cadquery solid is created"""

        test_shape = paramak.CoolantChannelRingStraight(
            height=200,
            channel_radius=10,
            ring_offset=70,
            number_of_coolant_channels=8
        )
        
        assert test_shape.solid is not None 
        assert test_shape.volume > 1000

    def test_CoolantChannelRingStraight_volume(self):
        """creates CoolantChannelRingStraight shapes and checks that the volumes are correct"""

        test_shape = paramak.CoolantChannelRingStraight(
            height=200,
            channel_radius=10,
            ring_offset=70,
            number_of_coolant_channels=8
        )
        assert test_shape.volume == pytest.approx(math.pi * (10 ** 2) * 200 * 8)

        test_shape = paramak.CoolantChannelRingStraight(
            height=100,
            channel_radius=20,
            ring_offset=100,
            number_of_coolant_channels=5
        )
        assert test_shape.volume == pytest.approx(math.pi * (20 ** 2) * 100 * 5)


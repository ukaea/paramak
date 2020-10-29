
import os
import math
import unittest
from pathlib import Path

import paramak
import pytest


class test_CoolantChannelRingCurved(unittest.TestCase):
    def test_CoolantChannelRingCurved_creation(self):
        """creates a coolant channel ring using the CoolantChannelRingCurved parametric shape
        and checks that a cadquery solid is created"""

        test_shape = paramak.CoolantChannelRingCurved(
            height=200,
            channel_radius=10,
            ring_offset=70,
            mid_offset=-20
            number_of_coolant_channels=8
        )
        
        assert test_shape.solid is not None 
        assert test_shape.volume > 1000


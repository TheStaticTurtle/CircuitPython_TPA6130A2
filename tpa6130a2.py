# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Samuel (TheStaticTurtle)
#
# SPDX-License-Identifier: MIT
"""
`thestaticturtle_tpa6130a2`
================================================================================

Library to control the tpa6130a2 headphone amplifier


* Author(s): Samuel (TheStaticTurtle)

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/TheStaticTurtle/Thestaticturtle_CircuitPython_TPA6130A2.git"

import board
from adafruit_bus_device.i2c_device import I2CDevice

class TPA6130A2:
    MODE_STEREO = 0b00
    MODE_DUAL_MONO = 0b01
    MODE_BRIDGE_TIED_LOAD = 0b10
    
    def __init__(self, i2c):
        self._device = I2CDevice(i2c, 0x60)
        self._mode = self.MODE_STEREO
        self._volume = 0b110100
        self._shutdown = False
        self._amp_left_en = True
        self._amp_right_en = True
        self._amp_left_mute = False
        self._amp_right_mute = False

    def _read_reg(self, reg):
        with self._device:
            result = bytearray(1)
            self._device.write_then_readinto(bytes([reg]), result)
            return result[0]
        
    def _write_reg(self, reg, value):
        with self._device:
            self._device.write(bytes([reg, value]))
    
    def _reconf_ctrl_reg(self):
        data = self._mode << 4
        data += int(self._amp_left_en)<<7
        data += int(self._amp_right_en)<<6
        data += int(self._shutdown)
        self._write_reg(1, data)
        
    def _reconf_volmute_reg(self):
        data = self._volume & 0b00111111
        data += int(self._amp_left_mute)<<7
        data += int(self._amp_right_mute)<<6
        self._write_reg(2, data)
        
        
    def soft_shutdown(self, shutdown):
        self._shutdown = shutdown
        self._reconf_ctrl_reg()
    
    def set_mute(self, left, right, change_enable=True):
        self._amp_left_mute = left
        self._amp_right_mute = right
        if change_enable:
            self._amp_left_en = not left
            self._amp_right_en = not right
            self._reconf_ctrl_reg()
        self._reconf_volmute_reg()
        
    def set_amp_enabled(self, left, right):
        self._amp_left_en = left
        self._amp_right_en = right
        self._reconf_ctrl_reg()
    
    def set_mode(self, mode):
        self._mode = mode
        self._reconf_ctrl_reg()
    
    def set_volume(self, volume):
        self._volume = volume
        self._reconf_volmute_reg()



# CircuitPython_TPA6130A2

Library to control the tpa6130a2 headphone amplifier

https://www.ti.com/lit/ds/symlink/tpa6130a2.pdf

## Usage Example

```py
import i2c
from tpa6130a2 import TPA6130A2
import board
import busio

i2c = busio.I2C(board.GP1, board.GP0)
tpa = TPA6130A2(i2c)

tpa.soft_shutdown(False) # Turn the ship on, the hardware pin bypasses the software shutdown
tpa.set_mute(False, False) # Disable the mute flags on the left and right speakers
tpa.set_mode(TPA6130A2.MODE_STEREO) #Set it to use stereo
tpa.set_volume(0b110101) # set the volume 0-63
```

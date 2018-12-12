# Osci-ADS1256
Python module for interfacing Texas Instruments SPI bus based analog-
to-digital converters with the Raspberry Pi and display the data through osciloscope visualization

This python module is modification from module below

Interfacing Module:
Download: https://github.com/ul-gh/PiPyADC

Osciloscope Visualization Module:
Download https://github.com/Suyash458/SoftwareOscilloscope

Dependencies
+ pyqtgraph
+ PySide or PyQt 4.8+
+ numpy
+ pySerial
+ WiringPi
+ VC++ for Python

How To Run:
- `sudo python osci.py`
- Open new console window type `python`
- 
```
>>>from SoftOscilloscope import SocketClientPlot
>>>plot = SocketClientPlot('localhost', 9000)
>>>plot.start()
```

For more configuration about interfacing and visualization please visit original creator of this module above.

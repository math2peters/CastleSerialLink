# CastleSerialLink
Pythonic implementation for communication with the castle serial link (http://www.castlecreations.com/en/serial-link-010-0121-00), a device used to communicate with and control Castle Electronic Speed Controllers (ESCs).

This is a small spinoff of code I implemented intended to help people communicate with ESCs via the castle serial link device. Below outlines the hardware steps to get this code to work:

1. Purchase:
   * a castle serial link device
   * a castle ESC
   * a castle link USB programming device (their naming conventions are confusing)
   * a generic FTDI to convert from USB to serial
   * a power supply for the ESC
   * a power supply for the serial link. Hopefully your ESC has a Battery Eliminator Circuit, in which case you don't need to worry, it's powered automatically. If not, a 6V lantern battery or something similar should work just fine
   * wires to connect everything together
   * soldering iron + solder to solder connections between serial link and FTDI
  
2. Wire these components together. Most of these connections are reasonably obvious. The difficult ones are connecting the FTDI and serial link. For my setup, I connected the 5V output of the serial link to my FTDI to power it, but the feasibility of this varies based on which FTDI you purchase. Make sure you connect their ground pins together and cross the Rx of the FTDI with the Tx of the serial link and visa versa.

3. Program both the ESC and the serial link with the castle link USB programming device. Most important is setting the ESC to accept live link communication. You can also modify the baud rate and device id of the castle serial link this way. The SerialLink class should be configured for the defaults.

4. Finally, you can plug a USB into the FDTI and your computer should detect the devices once they are powered. For windows computers, the USB port name should be COM followed by a number, e.g. COM6. This is the value used as input in the SerialLink class constructor.

Programming examples to come soon.

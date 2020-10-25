#!python

# This code was adapted from a forum post
# https://www.draisberghof.de/usb_modeswitch/bb/viewtopic.php?f=3&t=1938&view=next
# (which was in turn adapted from a pyusb tutorial)

import usb.core
import usb.util

# edit these according to the device manager
vid = 0x12d1
pid = 0x1f01

# find our device
dev = usb.core.find(idVendor=vid, idProduct=pid)
usb.core.show_devices()

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
interface_number = cfg[(0,0)].bInterfaceNumber
intf = usb.util.find_descriptor(
    cfg, bInterfaceNumber = interface_number,
)

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT
)

assert ep is not None

# write the data
message = '55534243123456780000000000000a11062000000000000100000000000000'
bytes_message = bytes.fromhex(message)
ep.write(bytes_message)
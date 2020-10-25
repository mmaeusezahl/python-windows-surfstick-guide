#!python

# This code was adapted from a forum post
# https://www.draisberghof.de/usb_modeswitch/bb/viewtopic.php?f=3&t=1938&view=next
# (which was in turn adapted from a pyusb tutorial)

import sys
import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0x12d1, idProduct=0x1f01)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# sys.exit()

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
interface_number = cfg[(0,0)].bInterfaceNumber
#alternate_settting = usb.control.get_interface(interface_number)
intf = usb.util.find_descriptor(
    cfg, bInterfaceNumber = interface_number,
#    bAlternateSetting = alternate_setting
)

print(dev.manufacturer)

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

#message from usb-modeswitch-data-20140129 for 12d1_1f17
#message = '55534243123456780002000080000a11062000000000000100000000000000'

#message from http://www.draisberghof.de/usb_modeswitch/bb/viewtopic.php?f=3&t=1809
message = '55534243123456780000000000000a11062000000000000100000000000000'

bytes_message = bytes.fromhex(message)

#send message to first found out endpoint
#ep.write()
ep.write(bytes_message)
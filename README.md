# How to use a Huawei surfstick under Windows with python to send and receive SMS

## Scope of this guide

This guide is meant as starting point for users who want to send SMS from a
python script under Windows. There are quite some tutorials out there for
Linux and MacOS but nothing that worked for my specific circumstances.

This guide was written for a E3135 surfstick by Huawei. I believe that the
information provided here might help for other similar surfsticks as well.
There is quite a good list of similar devices in the [USB ModeSwitch article][1]
together with some starting point information in the ubuntuusers forum.

Possible applications (partially beyond the scope of this guide) include:
* Sending and receiving SMS with a Huawei surfstick
* Modeswitching the surfstick under Windows
* Doing other things a surf stick can do (e.g. phone calls, reading SIM contacts
using the surfstick)
* ... ?

## Background

Using a Huawei surfstick from python becomes possible, since the surfstick
supports multiple modes. There are e.g.(to my knowledge):

* A USB "storage-device" mode, which is initially employed whenever the stick
gets powered
* A "high-speed" mode (for example called Hi-Link on Huawei surfsticks)
* A "modem"  mode with support for traditional modem commands (also known as 
[Hayes commands][2])

## References
This is simply a collection of all references for better display on the GITHub
page.

1. [https://wiki.ubuntuusers.de/USB_ModeSwitch/][1]
2. [https://en.wikipedia.org/wiki/Hayes_command_set][2]

[1]: https://wiki.ubuntuusers.de/USB_ModeSwitch/
[2]: https://en.wikipedia.org/wiki/Hayes_command_set
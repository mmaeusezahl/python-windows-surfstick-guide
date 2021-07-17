# How to use a Huawei surfstick in modem mode under Windows to send and receive SMS (with Python)

## Scope of this guide

This guide is meant as starting point for users who want to send SMS from a
Python script under Windows. There are quite some tutorials out there for
Linux and MacOS but nothing that worked for my specific circumstances.

This guide was written for a E3135 surfstick by Huawei. I believe that the
information provided here might help for other similar surfsticks as well.
There is quite a good list of similar devices in the [USB ModeSwitch article][1]
together with some starting point information in the ubuntuusers forum.

Possible applications (partially beyond the scope of this guide) include:
* Sending and receiving SMS with a Huawei surfstick
* Modeswitching the surfstick under Windows
* Modeswitching the surfstick under Linux or MacOS without the usb-modeswitch
software
* Doing other things a surf stick can do (e.g. phone calls, reading SIM contacts
using the surfstick)
* ... ?

## Background

Using a Huawei surfstick from Python becomes possible, since the surfstick
supports multiple modes. There are e.g.(to my knowledge):

* A USB "mass-storage" device mode, which is initially employed whenever the stick
gets powered
* A "high-speed" mode (for example called Hi-Link on Huawei surfsticks)
* A "modem"  mode with support for traditional modem commands (also known as 
[Hayes commands][2])

A "normal" use-case for a Windows user would therefore look like this:

1. The surfstick is attached to the computer. It identifies itself as a
"mass-storage" device and Windows treats it like a CD.
![Screenshot of the Windows Explorer showing the "CD"](https://github.com/mmaeusezahl/python-windows-surfstick-guide/blob/master/screenshots/mass-storage-device-explorer.PNG?raw=true)
From the perspective of the device manager this device looks like this:
![Screenshot of the Device Manager showing the "CD"](https://github.com/mmaeusezahl/python-windows-surfstick-guide/blob/master/screenshots/mass-storage-device-device-manager.PNG?raw=true)
Notice the identifying parameters (so to say the fingerprint) of this device to
the system. A "vendor ID" (called VID) unique to Huawei and a "product ID" 
(called PID) unique to this particular srufstick (a E3135). As a side note: 
These are the values that the operating system uses to determine which drivers 
to load when inserting the device. You can see that in my case the combination
12d1:1f01 (as written in linux terms vid:pid) matches [this list][1].
2. The user runs the `AutoRun.exe` and two things get installed:
   1. A tool called `mbbService`, which will look for the mass-storage device by
   means of its vid and pid
   2. The driver for the "high-speed" mode
3. Now a bit of magic happens. The freshly installed `mbbService` will identify
the attached surfstick in "mass-storage" mode. It will the send a "magic"
message to the surfstick which will immediately trigger a so called modeswitch
in the surfstick. It will briefly reset the connection and the reappear as a new
kind of device to the operation system. This happens very quickly, but sometimes
the user can quickly see the fake "CD" appearing before the actual surfstick
loads. Since the `mbbService` places itself in autostart, this will also happen
after the system is restarted or the surfstick is reinserted.
4. From the perspective of the device manager, the device now has a new ID (in
my case 12d1:14dc). It therefore loads the actual driver for the "high-speed"
mode and a webpage will open, querying the user to connect, provide a PIN etc.

This works well for actually connecting to the internet, but sometimes it is not
desired to have a fully fledged high-speed connection. In my case, I just wanted
to send SMS using a Python script. It seems possible to directly talk to the
HTML pages in the background, but this appeared rather complicated to me. (There
seems to be a project which does exactly this though 
[huawei-modem-python-api-client][3])

It is however well known, that there is the other "modem mode" which provides an
easy to use interface for sending SMS. There are also some Python libraries
which directly target this mode (see [python-gsmmodem-new][4] and [pyhumod][5]).
To me this seems to have the following advantages:

* More direct approach; less vulnerable to mistakes in the implementation
* Translates well to other modems of similar kind (even if the HTML changes)
* I don't want or need a mobile data connection
* I dislike the amount of software installed. Also I dislike that a new network
connection is visible.
* I like to emply FOSS as far as possible (it seems more future-proof)
* Some people apparently want to use their surfsticks with otherwise 
unsupported Windows versions

There is a plethora of resources how to use the modem mode under Linux (see e.g.
[this guide for a raspberry PI][7]), but not much information regarding Windows.
My idea is, that the official support for the modem mode got largely dropped
around 2014 and is no longer shipped with the official Windows drivers.

The central remaining challenges for this guide are therefore:
* Modeswitching the surfstick under Windows, ideally without using the
proprietary Huawei software
* Providing a suitable driver for the "modem-mode"

## Performing the modeswitch using Python

There is a similar guide [here][6], which I couldn't get working. The key idea
is to send a "magic" message like

```
55534243123456780000000000000011062000000100000000000000000000
```

encoded in hexadecimal to the USB mass-storage device to trigger the modeswitch.
These messages have been reverse engineered by the Linux community. The main
resource for this is the `usb-modeswitch` [software along its forum][8]. There
you can also find resources how to obtain the messages in the first place.

It is rather simple to trigger a mode-switch on Windows using Python. This 
[forum thread][9] came rather close and the code in `modeswitch.py` is based on
their proposed solution. The main issue there was, that they forgot to
hex-decode the message before sending it to the surfstick.

### Installing a driver

First you'll have to replace the default drive with a libusb compatible driver
such that PyUSB can send messages to the surfstick. For this I'd recommend using
the tool Zadig. Once downloaded you'll have to select 
"Options"->"List All Devices" and then find your surfstick from the list. This 
can be identified by the USB ID which matches the vendor and product id 
discussed earlier. **Be extra sure about this or you might unintentionally
uninstall and replcace the driver for a different device!** Then select 
`libusb-win32` from the list of options and click install

![Screenshot of Zadig shwoing the correct settings](https://github.com/mmaeusezahl/python-windows-surfstick-guide/blob/master/screenshots/zadig.PNG?raw=true)

### Running the script

To use the python script you'll have to install [PyUSB][10] which is a frontend
to the various libusb clones (like libusb-win32 we just installed).

```
pip install pyusb
```

The you can run

```
python modeswitch.py
```

and your surfstick should finally be in modem-mode! Please note that the 
message, vid and pid are hard-coded into this script, but it should be easy
enough to adapt for your needs.

### Thougts about the "magic" messages

I have no idea why, but my surfstick will end up in different states depending
on the magic message. Some examples using a E3135 surfstick:

| message                                                        | result    | mode   |
|----------------------------------------------------------------|-----------|--------|
| 55534243123456780000000000000011062000000100000000000000000000 | 12d1:1001 | modem |
| 55534243123456780000000000000a11062000000000000100000000000000 | 12d1:14dc | HiLink  |

Note that neither of those examples end up with a product ID actually associated
to my particular stick. You are essentially looking for a combination that will
end up in a state for that you can find a Windows driver (see next section).
In my case the device ends up as a 12d1:1001
"Huawei Technologies Co., Ltd. E161/E169/E620/E800 HSDPA Modem"...

## Loading the correct driver

(TODO: document current state of the installation process for the user)

### Downloading the driver

The trick is to install a driver from the [UTPSMobile Partner][13] software. 
Look  for the "HUAWEI Stick UTPS-V200R003B015D16SP02C983( for win10)" file on 
the Huawei Download page or through the page search ([direct link][14]). After 
downloading **unpack**  the `*.rar` file, then unpack the `*.zip` file inside.

Inside the zip file you'll find a `Setup.exe` and a `data.bin`. **Don't install
it unless you really want the UTPS software** (which you probably
shouldn't because it [used to have severy security issues](https://www.cvedetails.com/cve/CVE-2014-8358/) 
and is not actively maintained to my knowledge)!

Now extract the `data.bin` and find the 

```
common\Driver
```

directory. This finally contains the driver files we are looking for. There also
seems to be an installer, which I did not use.

### Using the driver

The final state according to the device manager can be seen in the following
screenshot:

![Screenshot of the Device Manager after sucessfully installing the driver](https://github.com/mmaeusezahl/python-windows-surfstick-guide/blob/master/screenshots/final-state-device-manager.PNG?raw=true)

You can see that three "composite devices" have been correctly installed. One is
a modem and two are serial interface we are going to use in the next stept to 
send SMS etc.

### SHA256 checksums

| Filename                                                  | SHA256                                                           |
|-----------------------------------------------------------|------------------------------------------------------------------|
| HUAWEI Stick UTPS-V200R003B015D16SP02C983( for win10).rar | E00E6FFE488AC21B53AAED6D2C6AB0EC07D3E7F2CD844BE9CADC8F5EFF246238 |
| HUAWEI Stick UTPS-V200R003B015D16SP02C983( for win10).zip | 93ED95B2A8D734AA217CA333C91E202667B9D869DC1AC4EEA87CC76C8EC1AE4B |
| data.bin                                                  | 16541E0AD7AE64BC87B6FE18BD7DE1FBA4000AA1B5E3F3B9133DEA74896DD2EB |

## Sending and receiving SMS

(TODO: add actual example code)

For now I had sucess using the commands as shown in step 5 of ![this guide](https://www.instructables.com/Giving-the-Raspberry-Pi-a-Serial-Modem-Using-the-H/).

The only thing you'll have to adapt is to replace the `ttyUSB` port in the line
```python
ser = serial.Serial('/dev/ttyUSB0', 460800, timeout=1)
```

with the Windows COM Port, i.e. in the example above 'COM8' like this
```python
ser = serial.Serial('COM8', 460800, timeout=1)
```

## Final thoughs

After you have set the drivers once, Windows will remember them. You are going 
to have to do the modeswitching whenever the surfstick is reset. So you might
considering writing a script for doing so in the style of the usb-modeswitch
udev rule for Linux (or even using the Huawei pplication directly).

If someone ever feels like porting the "Option" Linux driver to Windows it
would make the whole thing using FOSS. On the other hand, why not use Linux in
the first place (given you are not bound by other factors).

I believe that I might use the HiLink mode for future projects (e.g. when actual
access to the internet is desired additionally). It is not clear how 
"future-proof" this approach is however.

## Some hints and troubleshooting

* Make sure the SIM card is inserted the correct way... Seriously, this cost me
multiple hours of debugging. There is a small engraving in the surfstick showing
the orientation.
* Use a USB 2.0 port with no in-between USB switches.
* If you are using this the first time, I'd recommend to use the full driver
installation first (maybe in a virtual machine) and see if your stick e.g. has
a SIM lock. This will save you hours of work.
* Linux will load the option driver to provide the serial ports on 
´/dev/ttyUSB0´ to 
* If you are using VirtualBox with USB passthrough (e.g. to test under Linux)
  * Use the "USB 2.0 (OHCI, EHCI)" mode from the extension pack. Neither
  * Make plenty use of the `lsusb` and `usb-device` commands to see, which VID
  and PID are currently loaded.
* If you want to uninstall the driver and `mbbService` once installed do the
following:
  1. Run the uninstaller from `C:\Program Files (x86)\MobileBrServ` or 
  `C:\Program Files (x86)\mbbService` (or similar)
  2. Uninstall the various Huawei devices from the device manager. You can 
  easily find all of them if susing View->Device by container. There should be 
  a category called "Huawei Mobile" which lists the various described modes as 
  explained in this guide. Usually you can just uninstall all of them.
  3. It should not be necessary to restart Windows. If done correctly, the next
  time you attach the surfstick, it will be in "mass-storage" mode again.
* If the stick is in "mass-storage" mode, but no files show up in the explorer?
This could happen after using Zadig or installing the official drivers.
  * There are actually two drivers to choose from
  * Go to the device manager
  * Right click the mass-storage device which is your Huawei surfstick
  * Select "Update driver"
  * Select "Browser my computer for files"
  * Select "Let me pick from a list of installed drivers on this computer"
  * Usually there will be two drivers. One of them works ;)

## References
This is simply a collection of all references for better display on the GITHub
page.

1. [https://wiki.ubuntuusers.de/USB_ModeSwitch/][1]
2. [https://en.wikipedia.org/wiki/Hayes_command_set][2]
3. [https://github.com/pablo/huawei-modem-python-api-client][3]
4. [https://github.com/babca/python-gsmmodem][4]
5. [https://github.com/oozie/pyhumod][5]
6. [https://zedt.eu/tech/hardware/switch-huawei-e3131-hilink-modem-mode/][6]
7. [https://www.instructables.com/Giving-the-Raspberry-Pi-a-Serial-Modem-Using-the-H/][7]
8. [https://www.draisberghof.de/usb_modeswitch/][8]
9. [https://www.draisberghof.de/usb_modeswitch/bb/viewtopic.php?f=3&t=1938&view=next][9]
10. [https://github.com/pyusb/pyusb][10]
11. [https://github.com/pyserial/pyserial][11]
12. [https://zadig.akeo.ie/][12]
13. [https://consumer.huawei.com/de/search/?keyword=mobile%20partner&tag=support][13]
14. [https://consumer-tkb.huawei.com/weknow/servlet/download/public?contextNo=S1600345804&view=true][14]

[1]: https://wiki.ubuntuusers.de/USB_ModeSwitch/
[2]: https://en.wikipedia.org/wiki/Hayes_command_set
[3]: https://github.com/pablo/huawei-modem-python-api-client
[4]: https://github.com/babca/python-gsmmodem
[5]: https://github.com/oozie/pyhumod
[6]: https://zedt.eu/tech/hardware/switch-huawei-e3131-hilink-modem-mode/
[7]: https://www.instructables.com/Giving-the-Raspberry-Pi-a-Serial-Modem-Using-the-H/
[8]: https://www.draisberghof.de/usb_modeswitch/
[9]: https://www.draisberghof.de/usb_modeswitch/bb/viewtopic.php?f=3&t=1938&view=next
[10]: https://github.com/pyusb/pyusb
[11]: https://github.com/pyserial/pyserial
[12]: https://zadig.akeo.ie/
[13]: https://consumer.huawei.com/de/search/?keyword=mobile%20partner&tag=support
[14]: https://consumer-tkb.huawei.com/weknow/servlet/download/public?contextNo=S1600345804&view=true

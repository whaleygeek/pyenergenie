# pyenergenie
A python interface to the Energenie line of products

https://energenie4u.co.uk/


## Where is the best place to get the code?

The most tested code is in the Energenie repo here:

[Energenie Repo](https://github.com/Energenie/pyenergenie)

i.e. Energenie test on devices before updating the public repo
and linking external product pages to the code download. But, this might
be quite a bit older than the current ongoing development work.



The most leading-edge code is in whaleygeek's repo here:

[Whaleygeek repo](https://github.com/whaleygeek/pyenergenie)

i.e. This is whaleygeek's development area, master is reasonably
well tested, and there may be multiple feature branches with ongoing
development work that is still in progress. But, this might be
the most up to date code with support for newer devices, and there
may be experimental items in here that you would like to get early
access to.


## What is this all about?

Energenie devices (both the green button devices, and the newer MiHome range)
can be controlled and monitored by this Python library on a Raspberry Pi.
With it you can turn sockets on and off, and monitor energy usage.

There are two ways to control Energenie devices from a Raspberry Pi.
One of their boards maps 4 GPIO's to transmit 4 standard messages.
For that board, use this code from Ben Nuttall and Amy Mather:
[Ben and Amy's code](https://pypi.python.org/pypi/energenie)

The second board, the ENER314-RT board, is a full radio that is programmable
from the SPI interface of the Raspberry Pi. For that board, please use
this code, which now supports all models of Raspberry Pi, and all devices
from Energenie (including the old green button devices and the new
MiHome monitor devices).

The Energenie product line uses the HopeRF radio transciever, and the OpenThings 
protocol from Sentec. Energenie have built a RaspberryPi add-on board that 
interfaces to the HopeRF RFM69, and allows both control and monitoring of their 
products from a Raspberry Pi.

Energenie have some (old) sample code written in C to control and monitor
their devices, but this package is now considered to be far superior. Energenie
have been very kind in supporting this work by loaning devices to help with the
testing of this code.

This python library uses a 'zero install' strategy, by embedding everything
that is needed in once place. In theory, you can just press the DownloadZip
button, unzip the code, and run it, and it will work. (None of that
sudo apt-get install nonsense!)

This code *should* work with both Python 2 and Python 3. It has been tested
with both, but note that ongoing development occurs in Python 3 and the
support for Python2 is disappearing gradually.


## Purpose

This library of code is designed to be everything you need to get going with
writing a fully functional application for the Energenie devices (both 
monitoring and control).


## Getting Going

1) Plug in your ENER314-RT-VER01 board from Energenie onto the 26 pin or 40 pin 
connector of your Raspberry Pi. This is tested on Raspberry Pi B, B+ B2 and 2B, 3 and PiZero. There is
no reason why it should not work on the A and A+ but it hasn't been specially tested on
those combinations yet.

2) Press the CLONE OR DOWNLOAD button to the right of this page, and choose the
DOWNLOAD ZIP option.

3) unzip the software (from a terminal prompt, e.g. LXTerminal)

```
unzip pyenergenie-master.zip
cd pyenergenie-master
cd src
```

4) If you have legacy green button devices, run the setup_tool to learn those devices
to your code


```
./setup_tool
option 1. legacy learn mode
ENTER for default house code (or type in a hex number with 5 digits like 12345 or CAB12)
ENTER for switch 1 (or choose 1,2,3,4)
```

Hold the green button on your legacy device until it starts to flash. It should then
learn the house code being broadcast by the setup tool, and then start switching on and
off.

You can edit the registry.kvs to ADD a record for an ENER002 to give this device a
friendly name - look at the examples already in the file.

If you know the house code assigned to an RF hand controller, you can program that into
your code (and your registry.kvs) to make the socket work with both. (Note: I will be adding
a learn mode for RF hand remotes in a later release, you can't learn their codes yet without
having special diagnostics equipment to hand).

5) If you have a MiHome device, run the setup_tool to learn those devices

```
./setup_tool
option 2. mihome discovery mode
```

Wait for data to arrive from your mihome device (every 10 seconds) and accept it
when it says 'remember device' - the device is now in the registry.kvs file
and can be used in all other demo programs easily.

6) Try the other demo programs, the simplest one to start using and modifying
is control_any_auto.py as it shows how to refer to devices in your registry
by a simple variable name, and you can switch them on and off in a device
agnostic way (all switchable devices have a turn_on and turn_off function).
This is probably the best way to write your app, by learning your devices
into the registry (or hand coding them in there) and then just referring to them
by name in your python program.

7) Try the other demo programs

These other python programs show off some other features of the Energenie Python
library:

```
control_any_auto.py       auto variable creation from your registry.kvs
control_any_noreg.py      creating your variables manually without a registry
control_any_reg.py        control all switchable devices regardless of name, from registry
discover_mihome.py        a discovery example, there are 4 standard discovery behaviours
mihome_energy_monitor.py  a simple logger that logs all energy messages to energenie.csv
```

## Gotcha's

Please note that there are two different radio standards in use in this library. 
There is an OOK (On Off Keying) based system that is used by the original legacy green-button sockets.
There is also an FSK (Frequency Shift Keying) based system used by the MiHome range.

This library supports both. However, please note that some Energenie products are
branded as the MiHome range, but are internally a legacy device. This means that you will
need to use the Legacy Learn feature with those, instead of the MiHome discovery.

The MIHO002 for example is an OOK device, so you need to use the legacy learn mode
with that. 

As a general rule, if a device is receive-only, it uses the OOK legacy protocol.
If a device has any transmit features, it uses the MiHome FSK protocol.

There is a full list of devices in the energenie/devices.py file along with their 
OOK or FSK mode. OOK means Legacy Learn, FSK means MiHome Discovery.

## Other Contributions

For support for EV1527 remote from Digoo (DG-HAMA/HOSA) there is support
for a generic EV1527 based switch here:
[EV1527](https://github.com/steadramon/pyenergenie)

There is a NodeRed package, which was based on this work and kindly provided by 
another user. The package is well written and well maintained, and is a thorough
and representative implementation of all the features you would get from this
Python library.
[node-red-contrib-energenie-ener314rt](https://flows.nodered.org/node/node-red-contrib-energenie-ener314rt)


## Current focus

I am currently supporting more devices gradually, some of these are by contributions
by others, and some are by me. I am working on reliable support for the 2-gang
light switch at present, which has some interesting timing restrictions that must
be dealt with for reliable operation.

## Future work

For details about future plans and work, please see the github issues log here:

https://github.com/whaleygeek/pyenergenie/issues


David Whale

@whaleygeek

April 2021


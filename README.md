# pyenergenie
A python interface to the Energenie line of products

https://energenie4u.co.uk/

Note
====

This is the beginnings of an open source library to access the Energenie 
range of power control and monitoring products from within Python.

The Energenie product line uses the HopeRF radio transciever, and the OpenThings 
protocol from Sentec. Energenie have built a RaspberryPi add-on board that 
interfaces to the HopeRF RFM69, and allows both control and monitoring of their 
products from a Raspberry Pi.

There are some existing Python libraries for some Energenie products, but they
do not support the full radio interface and full product range.

Energenie also have a modified set of C test code based on the HopeRF test harness,
but this does not support all products, all variants of Raspberry Pi hardware,
or all versions of the Raspbian OS, unless you bring in later versions of
the BCM module to support the new device tree on the BCM2836.

This project aims to develop an open source Python module, providing 
access to many or all of the features of the OpenHEMS, HopeRF and Energenie 
product line.


Note that there are two ways to control Energenie's from a Raspberry Pi.
One of the boards maps 4 GPIO's to transmit 4 standard messages.
For that board, use this code from Ben and Amy:
https://pypi.python.org/pypi/energenie

The second board, the ENER314-RT board, is a full radio that is programmable
from the SPI interface of the Raspberry Pi. For that board, please use
this code, which now supports all models of Raspberry Pi, and all devices
from Energenie (including the old green button devices and the new
MiHome monitor devices).


Purpose
====

This is an early release, and is the beginnings of this work.
It is not representative of the final API, but it is a starting point for me to
start experimenting with ideas and testing out reliability.

With it, you can receive monitor payloads from an Energenie MiHome Adaptor Plus,
directly within Python programs. This type of plug can be used for energy monitoring
and also for relay control of the socket.

You can also turn switches on MiHome Adaptor Plus on and off.

There is support for the legacy green-button switch devices ENER002,
but it is not yet fully tested, and not integrated into the main application
flow yet - it is a separate test program legacy.py.

I've tried to make this a 'zero install' and 'zero configuration' experience.
In theory (at least) you should be able to download the zip or git-clone,
plug in your Energenie radio, plug in your MiHome Adapter Plus, and run the code
to see data coming back.


Getting Going
====

1. Plug in your ENER314-RT-VER01 board from energine onto the 26 pin connector of
your Raspberry Pi. At the moment I have only tested this with a Raspberry Pi B,
although there is no reason why it should not work with any of the models currently
available on the market. The underlying GPIO and SPI has been tested in other
projects on a Pi2 for example.

2. Use the Download As Zip link to the right, and unzip the files onto your
Raspberry Pi. 

3. unzip the software

```
unzip pyenergenie-master.zip
cd pyenergenie-master
cd src
```

4. run the monitor test program with your MiHome adaptors

```
sudo python monitor.py
```

After a few seconds, you should see some packet dumps appearing on the screen.
These packets are then decoded and displayed in a dictionary format,
and for certain messages, also in a more friendly format.

5. run the switch test program with MiHome control adaptors

```
sudo python switch.py
```

This will listen for any MiHome adaptor plus devices, and then turn their
switch on and off every 10 seconds.

6. Try the legacy device support with your green button devices

```
sudo python legacy.py
```

At the moment, this just switches socket 1 on and off repeatedly,
but there are other test modes in the software.


Note that the protocol module (OpenThings) is completely generic and will
pretty much work with any device. Try plugging in an E-TRV and see what
messages get reported. Construct new template messages as pydict initialisers
and encode and send those in to make the device do something in response.


Plans
====

1. Finish off support for the legacy green-button devices.
(This is nearly completed)

2. Write a message scheduler, so that transmits only occur in safe
timeslots that are less likely to collide with transmits from devices
(and thus increase reliability of messaging in a large device installation)

3. Write a Python object interface for devices - i.e. one object per
physical device on the network, with a method for each feature of that
device. This will allow very high level object oriented access to a set of
devices in an installation, in a very expressive and easy to use manner.

4. Write javascript NodeRed wrappers around the Python (like GPIO nodes do)
so that you can drop NodeRed nodes for Energenie devices into a flow.

David Whale

@whaleygeek

April 2016

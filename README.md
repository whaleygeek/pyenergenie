# pyenergenie
A python interface to the Energenie line of products

https://energenie4u.co.uk/


Energenie devices (both the green button devices, and the newer MiHome range)
can be controlled and monitored by this python library on a Raspberry Pi.
With it you can turn sockets on and off, and monitor energy usage.

There are two ways to control Energenie devices from a Raspberry Pi.
One of their boards maps 4 GPIO's to transmit 4 standard messages.
For that board, use this code from Ben Nuttall and Amy Mather:
https://pypi.python.org/pypi/energenie

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


Purpose
====

This is an early release, and is the beginnings of this work.
It is not representative of the final API, but it is a starting point for me to
start experimenting with ideas and testing out reliability.

With it, you can receive monitor payloads from an Energenie MiHome Adaptor Plus,
directly within Python programs. This type of plug can be used for energy monitoring
and also for relay control of the socket.

You can also turn switches on MiHome Adaptor Plus on and off.

There is now also support for the legacy green-button switch devices ENER002,
which you can access from the legacy.py program.

Work is ongoing to build up the higher layers of this software, so that devices
from the MiHome (MIHO) and ENER ranges can be used interchangeably. Please look
at the issues log to see how this work is progressing.


Getting Going
====

1. Plug in your ENER314-RT-VER01 board from Energenie onto the 26 pin or 40 pin connector of
your Raspberry Pi. This is tested on Raspberry Pi B, B+ B2 and 2B and PiZero. There is
no reason why it should not work on the A and A+ but I haven't tested those combinations
yet.

2. Use the Download As Zip link to the right of this page

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

6. Run the legacy device support program with your green button devices

```
sudo python legacy.py
```


Note that the protocol module (OpenThings) is completely generic and will
pretty much work with any device. Try plugging in an E-TRV and see what
messages get reported. Construct new template messages as pydict initialisers
and encode and send those in to make the device do something in response.


Experimental
====

You can try combined.py which is an example of how to switch both the
purple MiHome plugs, and the green button legacy plugs in the same
application (at the moment you have to use the unified_radio branch
to do this, as I haven't merged this to master), but I tried it here
and it works.


Plans
====

1. Build a device-agnostic interface so that any device can be registered
with a friendly name, and then controlled with helpful commands like

```
tv.turn_on()
p = tv.get_power()
```

https://github.com/whaleygeek/pyenergenie/issues/18


2. Write a message scheduler, so that transmits only occur in safe
timeslots that are less likely to collide with transmits from devices
(and thus increase reliability of messaging in a large device installation)

https://github.com/whaleygeek/pyenergenie/issues/9


3. Write javascript NodeRed wrappers around the Python (like GPIO nodes do)
so that you can drop NodeRed nodes for Energenie devices into a flow.

https://github.com/whaleygeek/pyenergenie/issues/38


David Whale

@whaleygeek

May 2016

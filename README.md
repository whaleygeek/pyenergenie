# pyenergenie
A python interface to the Energenie line of products


This is the beginnings of an open source library to access the Energine range of
power control and monitoring products from within Python.

The Energenie product line uses the HopeRF radio transciever, and the OpenHEMS 
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


Purpose
====

This is an early release, and is the beginnings of this work.
It is not representative of the final API, but it is a starting point for me to
start experimenting with ideas and testing out reliability, with a view to using
these products to integrate into an Internet of Things solution provided by
Iotic-Labs Ltd.

With it, you can receive monitor payloads from an Energenie MiHome Adaptor Plus,
directly within Python programs. This type of plug can be used for energy monitoring
and also for relay control of the socket.

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

4. run the monitor test program

```
sudo python monitor.py
```

After a few seconds, you should see some packet dumps appearing on the screen.
These packets are then decoded and displayed in a dictionary format,
and for certain messages, also in a more friendly format.

If it crashes, it sometimes leaves the radio in an indeterminite state, remove
and replace the radio board and it should reset it (but see notes below about this).


Note that the protocol module (OpenHEMS) is completely generic and will
pretty much work with any device. Try plugging in an E-TRV and see what
messages get reported. Construct new template messages as pydict initialisers
and encode and send those in to make the device do something in response.


Plans
====

1. Finish off the message scheduler, so that transmits only occur in safe
timeslots that are less likely to collide with transmits from devices
(and thus increase reliability of messaging in a large device installation)

2. Write a Python object interface for devices - i.e. one object per
physical device on the network, with a method for each feature of that
device. This will allow very high level object oriented access to a set of
devices in an installation, in a very expressive and easy to use manner.

3. Push a fair amount of the radio interface and some of OpenHEMS back down into
a C library that implements the same interface as what we have at this point in the
Python. Write a ctypes wrapper around this, so that the identical Python internal
API is presented. The idea being that the first pass of Python coding defines the
API we want to use, and the second pass turns this into a single library that
does everything, exposed to Python via ctypes, but linkable to other applications
and languages too.


David Whale

@whaleygeek

October 2015

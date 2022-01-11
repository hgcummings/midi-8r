# MIDI-8R

Assistant for musicians with MIDI-based pedalboards. Built using Raspberry Pi Pico and MicroPython.

Responds to incoming MIDI messages by outputting other messages and displaying information.

Think of it as a co-pilot, navigator, or butler for your pedalboard.

**On stage**
* Extend MIDI patches to control pedals that have limited or no preset storage
* Show reminders for changing guitars, re-tuning, etc. (optionally turn on the tuner automatically)
* Any other info you like (e.g. which band member starts the next song)

**In the studio**
* Extend MIDI patches to control pedals that have limited or no preset storage
* Store additional information against patches, like the exact guitar and pickup selection
  (to allow the same sound to be recreated when re-tracking any recorded parts)

## Functionality

The default implementation is a Patch Editor that stores data against patches selected via MIDI
program change events. This is a modular editor which can support multiple components, each dealing
with different data associated with the patch.

Current components include:
* [**M5**](src/components/m5.py) for use with the Line 6 M5 pedals, which only support 24 presets.
  This component allows a chosen preset (and initial on/off state) to be stored against each
  of the 128 possible MIDI patches. This component updates the M5 pedal automatically via MIDI.
  This patch could easily be adapted to work with other effects pedals.
* [**Tuning**](src/components/tuning.py) for selecting the current tuning.
  Will automatically switch on the tuner when selecting a patch that uses a different tuning
* [**Guitar**](src/components/guitar.py) for storing the guitar and pickup selection

To implement your own component, start from the [template component](src/components/template.py)
or one of the above. More details on the API can be found in the template components doc comments.

Components and hardware configuration (e.g. GPIO pins used) can be modified in [config.py](src/config.py)

## Hardware

Components:
* Raspberry Pi Pico
* MIDI breakout
* Rotary encoder
* RGB LED matrix
* Footswitch
* 5V step-down buck converter
* Enclosure
* DC barrel jack, for pedalboard power connection
* 3.5mm jack sockets (or 5-pin DIN sockets if you prefer), for MIDI connections

Most of these can be picked up for under a few pounds/dollars/euros each
The most expensive component is the RGB LED matrix. These can be found for about 15 dollars.

### Build

This pedal can be built entirely with hand tools.

For details on the exact components I used and steps I took, see the [hardware build page](BUILD.md).

## Commercial products

There are similar products on the market, although none with the exact same functionality:
* [Step Audio STATUS](https://stepaudio.net/products/status/STATUS_-_MIDI_Display_Clock_and_Mapper_-_by_StepAudio_net.html)
  Has very flexible MIDI mapping and the ability to display extra info per patch
* [Selah effects Quartz](http://www.selaheffects.com/product/quartz-v3/)
  A compact pedal with a variety of MIDI functionality and custom labels for patches
* [MIDI Solutions Event Processor Plus](http://www.midisolutions.com/prodepp.htm)
  A below-board pedal (no buttons or display) supporting up to 32 MIDI mapping rules

## Related projects

* [galczo5/open-midi-controller](https://github.com/galczo5/open-midi-controller)
  Arduino-based MIDI controller. Has different goals to this project (designed to trigger
  MIDI events rather than respond to them), but some similarities in approach.

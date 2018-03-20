# kWhack

Etymology: *Kilowatt hour acknowledge* or *kWh hack* 

A simple power consumption tracker running on a Raspberry Pi 
and using a simple LDR rig connected to the GPIO pins.


## Installation

```bash
$ pip install git+https://github.com/hbldh/kwhack#egg=kwhack
```
## Usage

1. Build this [LDR rig](https://pimylifeup.com/raspberry-pi-light-sensor/).
2. Connect to Raspberry Pi, and attach the LDR to the 
blinking light on the power central.
3. Create a MongoDB server and store the URI as environment 
variable `MONGODB_URI` on the Raspberry Pi.  
4. Run `f47-server` and `f47-client`.


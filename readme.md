# Digital Pipette Server

This repo contains code to run the [science-jubilee](https://science-jubilee.readthedocs.io/en/latest/index.html)  implementation of the [Digital Pipette](https://doi.org/10.1039/D3DD00115F) tool. `digital_pipette.py` contains methods to manage state and perform actions with individual syringe tools. `serve_pipette.py` exposes this funcitonality for multiple syringes as an HTTP api. This service is intended to interface with the [science-jubilee HTTPSyringe tool](https://github.com/machineagency/science-jubilee/blob/main/src/science_jubilee/tools/HTTPSyringe.py). See the [documentation] for this tool for more information on required hardware and instructions to configure the tool with a Jubilee. Brief instructions for configuring and running the service are included here. 

## Implementation notes

The digital syringe tool uses a servo linear actuator to move the plunger of a syringe to perform liquid handling tasks. Code in this repo is responsible for managing the positioning of the actuator/plunger system to deliver desired volumes of liquids. The [companion tool definition over at science-jubilee](https://github.com/machineagency/science-jubilee/blob/main/src/science_jubilee/tools/HTTPSyringe.py) is reponsible for positioning the syringe tool in the correct location on the deck to perform the desired liquid handling task. 

Servo motors use a closed loop feedback system to control positioning. Position is controlled by sending timed voltage pulses. The length of the 'high' pulse tells the servo where to move. Generally a 1000us pulse is fully closed, 2000us is fully open, and intermediate values set position between these limits. This implementation uses the [pigpio library](https://abyz.me.uk/rpi/pigpio/index.html) to handle the servo control. The DigitalPipette object translates requests to dispense or aspirate a particular volume into a servo pulsewidth by 1) converting the volume into a pulswidth change using a conversion factor defined in a config.json file, 2) Adding/subtracting the pulswidth change to the current servo pulsewidth value (ie, current servo/syringe position), and 3) Updating the servo pulsewidth signal so the motor moves to then new position. Speed control of the movement is accomplished by moving the servo through a series of small timed intermediate movements.

## Setup
 
### Requirements

You will need:
- A raspberry pi (assuming a model 4B here, anything should work in theory) running raspberry pi OS and set up with a known static ip address. 
- A digital_syringe tool, built and wired according to the [science-jubilee documentation](https://science-jubilee.readthedocs.io/en/latest/building/http_syringe.html#). 

### Installation
1. Set up and activate a new [python venv](https://docs.python.org/3/library/venv.html) for this project.
2. Install pigpio following [their instructions](https://abyz.me.uk/rpi/pigpio/download.html). Install this in a separate directory from the `digital_pipette_server` repo. 
3. Clone this repository
4. Install the `digital_pipette_server` dependencies in `requirements.txt` by running `pip install -r requirements.txt` from the root of the digital_pipette_server repo.

### Configuration

1. You will need to set up a config.json file for each syringe tool you have. There are examples in the `configs` directory. You will need to set:
- us_per_uL: conversion factor, the change in pulsewidth (in microseconds) to dispense 1 microliter. Obtain this with a gravimetric calibration or linear interpolation from full and empty positions (see below)
- gpio_ping: The pi GPIO pin that the signal wire of the servo is plugged into
- name: name of the syringe tool, used to id the syringe in API requests
- full_position: The pulsewidth of the servo when the syringe is full. Obtain through trial and error
- empty_position: The pulsewidth of the servo when the syringe is empty. obtain through trial and error. Set it so the syringe plunger bottoms out on the bottom of the barrel, but isn't squished too much.
- capacity: total capacity of the syringe between empty_position and full_position in microliters
- time_step_size: Resolution of movement steps for speed controlled movements. Suggested default of 0.1
- min_pw_step: Minimum pulsewidth step to make when performing speed controlled move. Suggested minimum of 3, too small and the servo will stall

2. Edit the `serve_piptte.py` file to instantiate a DigitalPipette instance for your new pipette and add it to the `pipettes` dictionary:
```
pipette_10cc_1 = digital_pipette.DigitalPipette.from_config('~/digital_pipette_server/10_cc_1_config.json')
logger.info('Instantiated pipette_10cc_1')

pipettes = {'10cc_1':pipette_10cc_1}
```



### Starting the service
1. Start the [pigpio dameon](https://abyz.me.uk/rpi/pigpio/pigpiod.html) which allows this service to set pulsewidths: ` 
```
sudo pigpiod
```

2. Start the flask app to serve the endpoint:
```
flask --app serve_pipette run
```

Note: if flask command does not let curl commands received, try running the app through python by:
```
python serve_pipette.py
```

### Loading a syringe
After you start the service, you will need to "load" your syringes before they can be used. This is needed to tell the DigitalPipette python object where it's plunger/actuator system is. It is set up this way instead of doing a homing procedure so that you can load a syringe manually before installing it into the syringe tool. You load a syringe in software by calling the `/load_syringe` route with the current volume and pulsewidth of the syringe. Send a POST request to `/load_syringe` with the json payload {"name":$<syringe_name>, "volume":$<current syringe volume>, "pulsewidth":$<current syringe pulsewidth>"}. Anywhere there is a $<notes>, replace it (including $<>) with your values. The POST request is made through curl. The example command for loading syringe looks like this:

```
curl -d '{"name":$<syringe_name>, "volume":$<current syringe volume>, "pulsewidth":$<current syringe pulsewidth>"}' -X POST http://RaspberryUserName@192.168.0.0:5000/load_syringe -H "Content-Type: application/json"
```

How do you know the current pulsewidth? You probably need to set it first. Do that with the `/set_pulsewidth` route. POST a request here with json payload {"name":$<syringe_name>, "pulsewidth":$<desired pulswidth>", "speed":$<speed to move in uL/s>}.

[!WARNING]
If you don't set the pulsewidth to the correct current pulsewidth when calling the `/load_syringe` route, your first dispense volume will be inaccurate as the movement is calculated off of the current position. Weird things (ex aspirating when you mean to dispense) can also occur when pulsewidth is set incorrectly due to the intermediate movements set by the speed control. 

### Using the syringe
Once the syringe is loaded, it can be used to aspirate and dispense liquids. Aspirate (suck up liquid) with the `/aspirate` endpoint and dispense (push out liquid) with the `/dispense` endpoint. For both, POST a json payload containing {"name":$<syringe name>, "volume":$<volume in uL to aspirate/dispense>, "speed":$<speed to move in uL/S>}. All positioning of the syringe is handled separately, for example by using the science-jubilee HTTPsyringe tool versions of the aspirate and dispense methods. 


### Setting the pi up for headless use

It is ideal to set up pgpiod and the flask app as system services so they start on startup. Registering them as system services will enable this.

1. Enable pigpiod as a system service:
```
sudo systemctl enable pigpiod
```

2. Create a new service file for the flask app at `/etc/systemd/system/'. Name it `pipette-service.service`

3. Enter the following into this file. Note the filepaths to edit
```

[Unit]
Description=pipette server
After=network-online.target
Wants=network-online.target

[Service]
WorkingDirectory=$<absolute path to this repo>/digital_pipette_server
ExecStart=$<absolute path to your venv for this project>/servo/bin/python serve_pipette.py
Restart=always

[Install]
WantedBy=basic.target

```

4. Enable the service with `sudo systemctl enable pipette-service`

Reboot. The app should now come online automatically at boot. 



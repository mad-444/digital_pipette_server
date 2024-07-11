from flask import Flask, request, Response
from flask.json import jsonify

app = Flask(__name__)

import digital_pipette

pipette = digital_pipette.DigitalPipette.from_config('10_cc_config.json')

@app.route('/load_syringe', methods = ['POST'])
def load_syringe():
    data = request.json

    volume = data['volume']
    pulsewidth = data['pulsewidth']

    pipette.load_syringe(volume, pulsewidth)

    return


@app.route('/dispense', methods = ['POST'])
def dispense():
    data = request.json

    volume = data['volume']

    assert volume < pipette.remaining_volume, 'Volume greater than remaining volume'

    pipette.dispense(volume)

    return


@app.route('/aspirate', methods = ['POST'])
def aspirate():
    data = request.json
    volume = data['volume']

    assert volume + pipette.remaining_volume < pipette.capacity

    pipette.aspirate(volume)

    return


@app.route('/set_pulsewidth', methods = ['POST'])
def set_pulsewidth():
    data = request.json
    pulsewidth = data['pulsewidth']

    assert ((pulsewidth < 2000) and (pulsewidth > 1000)), 'Pulsewidth must be between 1000 and 2000'

    pipette.set_pulsewidth(pulsewidth)
           
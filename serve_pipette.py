from flask import Flask

app = Flask(__name__)

@app.route('/get_status', methods = ['GET'])
def get_status():
    pass


@app.route('set_status', methods = ['POST'])
def set_status():
    pass

@app.route('/dispense', methods = ['POST'])
def dispense():


    pass


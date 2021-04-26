import flask

from lenscalc import Lens

app = flask.Flask(__name__)

variables_info = {
    "D1": {"HTML": "D<sub>1</sub>", "description": "Surface 1 (object) power", "unit": "mm"},
    "D2": {"HTML": "D<sub>2</sub>", "description": "Surface 2 (image) power", "unit": "mm"},
    "D": {"HTML": "D", "description": "Lens power", "unit": "mm"},
    "n1": {"HTML": "n<sub>1</sub>", "description": "Object space index", "placeholder": "1.0003"},
    "nL": {"HTML": "n<sub>L</sub>", "description": "Lens index", "placeholder": "1.5"},
    "n2": {"HTML": "n<sub>2</sub>", "description": "Image space index", "placeholder": "1.0003"},
    "r1": {"HTML": "r<sub>1</sub>", "description": "Surface 1 (object) radius", "unit": "mm", "placeholder": "50"},
    "r2": {"HTML": "r<sub>2</sub>", "description": "Surface 2 (image) radius", "unit": "mm", "placeholder": "-40"},
    "CT": {"HTML": "CT", "description": "Central thickness", "unit": "mm", "placeholder": "3"},
    "P1": {"HTML": "P<sub>1</sub>", "description": "Primary principle point", "unit": "mm"},
    "P2": {"HTML": "P<sub>2</sub>", "description": "Secondary principle point", "unit": "mm"},
    "f1": {"HTML": "f<sub>1</sub>", "description": "Front (object) focal point", "unit": "mm"},
    "f2": {"HTML": "f<sub>2</sub>", "description": "Back (image) focal point", "unit": "mm"},
    "EFL": {"HTML": "EFL", "description": "Effective focal length", "unit": "mm"},
    "FFL": {"HTML": "FFL", "description": "Front focal length", "unit": "mm"},
    "BFL": {"HTML": "BFL", "description": "Back focal length", "unit": "mm"},
    "NPS": {"HTML": "NPS", "description": "Shift in nodal point", "unit": "mm"}
}


@app.route("/")
def index():
    return flask.render_template("index.html", variables=variables_info)


@app.route("/result/")
def result(variables=None, values=None):
    replacements = {}
    for arg in flask.request.args:
        if flask.request.args[arg] != "":
            # The type of the value from the web app is a string.
            # It is converted to float before it is passed to lenscalc.
            replacements[arg] = float(flask.request.args[arg])

    lens = Lens(**replacements)
    lens.calculate()

    values = lens.__dict__["parameters"]

    return flask.render_template("result.html", variables=variables_info, values=values)

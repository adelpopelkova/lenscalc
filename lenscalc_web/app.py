import flask

from lenscalc import Lens

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html", variables=Lens.variables)


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

    return flask.render_template("result.html", variables=Lens.variables, values=values)

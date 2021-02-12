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
            replacements[arg] = flask.request.args[arg]

    lens = Lens(**replacements)
    lens.calculate()

    values = lens.__dict__["parameters"]

    return flask.render_template("result.html", variables=Lens.variables, values=values)


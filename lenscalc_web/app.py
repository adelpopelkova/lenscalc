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

    l = Lens(**replacements)
    l.calculate()

    for var in dir(l):
        if var in Lens.variables:
            replacements[var] = l.__getattribute__(var)

    return flask.render_template("result.html", variables=Lens.variables, values=replacements)


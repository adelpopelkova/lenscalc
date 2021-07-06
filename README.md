# lenscalc

Lenscalc is a more universal version of
[Edmund Optics' Focal Length Calculator](https://www.edmundoptics.com/knowledge-center/tech-tools/focal-length/).

Unlike the original version,
lenscalc gives you the option to enter any set of parameters.
Now you don't have to slightly adjust the *surface radius* to get your
desired *back focal length*, you can just type it in.
In the background there are the exact same equations.

## Lens variables

The variables used to define the lens are the same as in the original calculator.
Some of them have been renamed to be easier to type
(e.g. Φ<sub>OS</sub> → D<sub>1</sub>).
Only the variables that have been renamed have all three columns filled in.

Lenscalc name | Original name  | Description
:-----------: | :------------: | --------------------------
D<sub>1</sub> | Φ<sub>OS</sub> | Surface 1 (object) power
D<sub>2</sub> | Φ<sub>IS</sub> | Surface 2 (image) power
D             | Φ              | Lens power
n<sub>1</sub> | n<sub>OS</sub> | Object space index
n<sub>L</sub> |                | Lens index
n<sub>2</sub> | n<sub>IS</sub> | Image space index
r<sub>1</sub> | R<sub>1</sub>  | Surface 1 (object) radius
r<sub>2</sub> | R<sub>2</sub>  | Surface 2 (image) radius
CT            |                | Central thickness
P<sub>1</sub> | P              | Primary principle point
P<sub>2</sub> | P"             | Secondary principle point
f<sub>1</sub> | f<sub>F</sub>  | Front (object) focal point
f<sub>2</sub> | f<sub>R</sub>  | Back (image) focal point
EFL           |                | Effective focal length
FFL           |                | Front focal length
BFL           |                | Back focal length
NPS           |                | Shift in nodal point

If you are using lenscalc in your code (i.e. you aren't using the web version),
the variables have the same name, they are just written without the subscript,
(e.g. D<sub>1</sub> → `D1`).

All variables except refractive indexes
(n<sub>1</sub>, n<sub>L</sub>, n<sub>2</sub>)
have the same unit (usually mm or cm).

## How to use the calculator

There are a few ways how you can use the calculator.

### Using the web version

The web app currently runs [here](http://adelpopelkova.pythonanywhere.com/).

### Using it in your Python code

1. Download or clone the repository.
1. Create and/or activate a virtual environment.
(Optional, although highly recommended).
1. Install needed dependencies using this command:
    ```
    $ python -m pip install -r requirements.txt
    ```
1. Import the Lens class.
    ```python
    from lenscalc import Lens
    ```
1. Using one of these two ways create a lens:
    ```python
    # The first one
    lens = Lens(
        n1 = 1.0003,
        nL = 1.5,
        n2 = 1.0003,
        r1 = 50,
        r2 = -40,
        CT = 3
    )
    ```
    ```python
    # The second one
    lens = Lens()
    lens.n1 = 1.0003
    lens.nL = 1.5
    lens.n2 = 1.0003
    lens.r1 = 50
    lens.r2 = -40
    lens.CT = 3
    ```
1. Calculate the missing variables using the `calculate` method.
    ```python
    lens.calculate()
    ```
1. To get the calculated variables use `print(lens)` for all variables
or `print(lens.BFL)` and similar to get them one by one.

### Using the web app locally

1. Create and/or activate a virtual environment.
1. Install the dependencies using this command:
    ```
    $ python -m pip install -r requirements-web.txt
    ```
1. Use these commands to run the web app
(On Windows use `set` instead of `export`.)
    ```
    $ export FLASK_APP=lenscalc_web
    $ export FLASK_ENV=development
    $ export FLASK_DEBUG=1
    $ flask run
    ```

## Testing the calculator
1. To an activated virtual environment install the dependencies for testing.
    * You can use this command to install only the necessary ones:
        ```
        $ python -m pip install -r requirements-dev.txt
        ```
    * If you want to install some extra tools (for easier development) use:
        ```
        $ python -m pip install -r requirements-extra.txt
        ```
1. Run the tests
    * The easiest way to run the test is this command:
        ```
        $ python -m pytest
        ```
    * Use this command to get also the time of the 5 slowest tests.
        ```
        $ python -m pytest -v --durations=5
        ```
    * If you don't want to run the tests with the combinations
    (there are a lot of them and they take a bit longer to run),
    use this command:
        ```
        $ python -m pytest --ignore=test_variable_combinations.py
        ```
    * To run the tests with combinations faster, you can use the following
    command (you'll need to install extra requirements or only
    [pytest-xdist](https://pypi.org/project/pytest-xdist/)
    for this command to work) to run the tests in parallel:
        ```
        $ python -m pytest -n <Number of CPUs>
        ```

## License
This project is licensed under the [MIT License](LICENSE).

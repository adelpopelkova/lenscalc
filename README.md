# lenscalc

:construction: This README is currently a Work In Progress.

## How to use the calculator

There are two ways how you can create the lens:

The first one:
```python
lens = Lens(
    n1 = 1.0003,
    nL = 1.5,
    n2 = 1.0003,
    r1 = 50,
    r2 = -40,
    CT = 3
)
```
The second one:
```python
lens = Lens()
lens.n1 = 1.0003
lens.nL = 1.5
lens.n2 = 1.0003
lens.r1 = 50
lens.r2 = -40
lens.CT = 3
```

Calculate the lens using the `calculate` method.

## Using the web app
The web app currently runs [here](http://adelpopelkova.pythonanywhere.com/).

To run the web app locally, use the following commands.
(On Windows use `set` instead of `export`.)
```
$ export FLASK_APP=lenscalc_web
$ export FLASK_ENV=development
$ flask run
```

## Testing the calculator
Use this command to get also the time of the 5 slowest tests.
```
$ python -m pytest -v --durations=5
```
If you don't want to run the tests with the combinations, use this command:
```
$ python -m pytest --ignore=test_variable_combinations.py
```

## License
This project is licensed under the [MIT License](LICENSE).

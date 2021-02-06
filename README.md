# lenscalc

:construction: This README is currently a Work In Progress.

## How to use the calculator

There are two ways how you can create the lens:
The first one:
```python
l = Lens(
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
l = Lens()
l.n1 = 1.0003
l.nL = 1.5
l.n2 = 1.0003
l.r1 = 50
l.r2 = -40
l.CT = 3
```

Calculate the lens using the `calculate` method.

## Using the web app

To run the web app locally, use the following comands.
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
$ python -m pytest -v -k test_lenscalc.py 
```

# lenscalc

:construction: This README is currently a Work In Progress.

## How to use the calculator

There are two ways how you can create the lens:
The first one:
```
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
```
l = Lens()
l.n1 = 1.0003,
l.nL = 1.5,
l.n2 = 1.0003,
l.r1 = 50,
l.r2 = -40,
l.CT = 3
```

Calculate the lens using the `calculate` method.


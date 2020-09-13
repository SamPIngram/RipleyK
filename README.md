# RipleyK
Calculation of the Ripley K ([spatial statistics](https://en.wikipedia.org/wiki/Spatial_descriptive_statistics)) value in python. This project is still being developed and currently only supports 'circle' based bounding regions for automated boundary correction. Can support 'rectangle' based bounding regions if you do not require boundary corrections. This package allows quick calculatation (using [kd-trees](https://en.wikipedia.org/wiki/K-d_tree)) the RipleyK values for 1D-3D systems. 

## Installation
You can install the RipleyK package using the following pip command:
```
pip install ripleyk
```

To get started from source quickly follow these steps:

1. Clone or download this respository and launch python within the folder.

2. Make a python environment to run in. Always recommend the use of virtual environments for safety. Must be Python3 and currently only tested with Python 3.8.

3. Install requirement.txt file into your new python environment
```
pip install -r requirements.txt
```

## Example

For these examples lets create a random subset of points in a sphere of radius 1:
```python
import random
xs = []
ys = []
zs = []
radius = 1
random.seed(0)
for i in range(0,10000):
    positioned = False
    while positioned is False:
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        z = random.uniform(-radius, radius)
        if (x**2)+(y**2)+(z**2) < radius**2:
            xs.append(x)
            ys.append(y)
            zs.append(z)
            positioned = True
xs = np.array(xs)
ys = np.array(ys)
zs = np.array(zs)
```

Now we can use our list of points within the RipleyK calculation method. Note that all point list are numpy arrays.

### Single radius calculation (2D)
Let us start simply. We shall calculate the Ripley K value for the circle (r=1) boundaing space. As it is a cirlce we only require two dimensions (d1 and d2). The calculate ripley method should be given the radius and bounding space as it's first two inputs. Then the points should be given as a numpy list of each dimension.

```python
import ripleyk

radius = 0.5
bounding_radius = 1
k = ripleyk.calculate_ripley(radius, bounding_radius, d1=xs, d2=ys)
print(k)
```

You should get a value of ```0.7576``` as k.

By default this will not include any boundary correction. To add this simply add ```boundary_correct=True``` to the above function. This should always results in an increase of the value. Now we get a value of ```0.8650``` as k.

Finally, there is a normalisation which can be applied to evaluate the clustering of the k-value in comparison to a completely spatially random (CSR). If the distribution is close to CSR the value should tend to 0. Below is the same calculation, but now includes boundarry correction and normalisation:

```python
import ripleyk

radius = 0.5
bounding_radius = 1
k = ripleyk.calculate_ripley(radius, bounding_radius, d1=xs, d2=ys, boundary_correct=True, CSR_Normalise=True)
print(k)
```

As we generated points randomly, we see that this normalisation does make the value much closer to 0, here we got ```0.0796```.

### Multiple radii calculation (3D)

It is also possible to run the method evluating multiple radii for their Ripley K values. This is the predominate way people evluate the distribution, by looking over a range of radii and plotting the k value or normalised k value against radius. Below is an example of doing this for the 3D dataset we generated:

```python
import ripleyk

radii = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
k = ripleyk.calculate_ripley(radii, 1, d1=xs, d2=ys, d3=zs,boundary_correct=True, CSR_Normalise=True)
print(k)
```

You should get the following results: 
```
[0.004040007680256669, 0.014698354446450401, 0.031055984373102252, 0.052700761751369396, 0.07963484721284364, 0.1114734068553147, 0.14820166805628499, 0.1880258651911193, 0.2271020312695291, 0.2608857812403329]
```

This can be simply plotted against the radii inputted.


## Dependencies
- [Numpy](https://numpy.org/)
- [Scipy](https://www.scipy.org/)

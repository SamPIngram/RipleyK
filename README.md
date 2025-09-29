# RipleyK

[![CI](https://github.com/SamPIngram/RipleyK/actions/workflows/python-package.yml/badge.svg)](https://github.com/SamPIngram/RipleyK/actions/workflows/ci.yml)

Calculation of the Ripley K ([spatial statistics](https://en.wikipedia.org/wiki/Spatial_descriptive_statistics)) value in python. This project is still being developed and currently only supports 'circle' based bounding regions for automated boundary correction. Can support 'rectangle' based bounding regions if you do not require boundary corrections. This package allows quick calculation (using [kd-trees](https://en.wikipedia.org/wiki/K-d_tree)) the RipleyK values for 1D-3D systems.

## Installation
You can install the RipleyK package using the following pip command:
```
pip install ripleyk
```

To get started from source quickly follow these steps:

1. Clone or download this repository.

2. Make a python environment to run in. We recommend the use of virtual environments. This package is tested on Python 3.9, 3.10, 3.11, 3.12 and 3.13.

3. Install requirements using the `requirements.txt` file into your new python environment:
```
pip install -r requirements.txt
```

## Theory
The mathematical equations for the calculated Ripley K value and normalised L value at each dimension is as follows:

### 1D Equations:

$$K(r) = D \frac{\sum_{i=1}^{n} \sum_{i\ne j} I[D(i,j)\leq r]}{\omega n^{2}}$$
<br/>

$$L(r) = D \frac{\sum_{i=1}^{n} \sum_{i\ne j} I[D(i,j)\leq r]}{\omega n^{2}} - 2r$$

### 2D Equations:

$$K(r) = A \frac{\sum_{i=1}^{n} \sum_{i\ne j} I[D(i,j)\leq r]}{\omega n^{2}}$$
<br/>

$$L(r) = A \frac{\sum_{i=1}^{n} \sum_{i\ne j} I[D(i,j)\leq r]}{\omega n^{2}} - \pi r^{2}$$

### 3D Equations:

$$K(r) = V \frac{\sum_{i=1}^{n} \sum_{i\ne j} I[D(i,j)\leq r]}{\omega n^{2}}$$
<br/>

$$L(r) = V \frac{\sum_{i=1}^{n} \sum_{i\ne j} I[D(i,j)\leq r]}{\omega n^{2}} - \frac{4}{3} \pi r^{3}$$

Note the term "region" is being used interchangeably for distance, area and volume for the 1D, 2D and 3D descriptions respectively. r is the line (1D) or radius (2D/3D) of the search region. ω is the ratio of overlap of the search region with the whole sample region, this is 1 if the search region is entirely within the sample region and <1 if some of the search region is outside of the sample region. If all of the search region is outside of the sample region this is 0 and the Ripley value will not be calculated. I is the indicator function which will be either 1 if the condition D(i,j)≤r is true or will be 0, where D(i,j) is the euclidean distance between points i and j. The size of the sample region is defined as a distance (D), area (A) or volume (V) within the 1D, 2D and 3D equations respectively.

## Code Example

For these examples lets create a random subset of points in a sphere of radius 1:
```python
import random
import numpy as np
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
Let us start simply. We shall calculate the Ripley K value for the circle (r=1) bounding space. As it is a circle we only require two dimensions (d1 and d2). The ```calculate_ripley``` method should be given the radius and bounding space as it's first two inputs. The points should be given as a numpy list for each dimension, where the spatial location of point[0] would be xs[0], ys[0].

```python
import ripleyk

radius = 0.5
bounding_radius = 1
k = ripleyk.calculate_ripley(radius, bounding_radius, d1=xs, d2=ys)
print(k)
```

You should get a value of ```0.7573``` as k.

By default this will not include any boundary correction. To add this simply add ```boundary_correct=True``` to the above function. This should always increase the value. Now we get a value of ```0.8646``` as k.

Finally, there is a normalisation which can be applied to evaluate the clustering of the k-value in comparison to a completely spatially random (CSR). If the distribution is close to CSR the value should tend to 0. Below is the same calculation, but now includes boundary correction and normalisation:

```python
import ripleyk

radius = 0.5
bounding_radius = 1
k = ripleyk.calculate_ripley(radius, bounding_radius, d1=xs, d2=ys, boundary_correct=True, CSR_Normalise=True)
print(k)
```

As we generated the points randomly, we see that this normalisation does make the value much closer to 0, here we got ```0.0792```. For non randomly distributed points a postive value indicates clustering and a negative value indicates dispersion.

### Multiple radii calculation (3D)

It is also possible to use this function to evaluate multiple radii for their Ripley K values. This is the predominant way to evaluate the distribution, by looking over a range of radii and plotting the k value or normalised k value against radius. Below is an example of doing this for the 3D dataset we generated:

```python
import ripleyk

radii = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
k = ripleyk.calculate_ripley(radii, 1, d1=xs, d2=ys, d3=zs,boundary_correct=True, CSR_Normalise=True)
print(k)
```

You should get the following results:
```
[-9.29e-06, -0.000105, -0.000391, -0.000728, -0.001386, -0.002302, -0.002896, -0.004294, -0.005930, -0.007915]
```

This can be simply plotted against the radii inputted as seen below (would require installation of [matplotlib](https://pypi.org/project/matplotlib/)):

```python
import ripleyk
import matplotlib.pyplot as plt

radii = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
k = ripleyk.calculate_ripley(radii, 1, d1=xs, d2=ys, d3=zs,boundary_correct=True, CSR_Normalise=True)

plt.plot(radii, k, 'bo')
plt.show()
```


## Dependencies
- [Numpy](https://numpy.org/) (>=1.21.0)
- [Scipy](https://www.scipy.org/) (>=1.7.0)

## Contributing
Contributions are welcome! To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch with a descriptive name.
3. Make your changes and add tests for them.
4. Run the tests to ensure everything is working correctly:
   ```
   pytest
   ```
5. Create a pull request.

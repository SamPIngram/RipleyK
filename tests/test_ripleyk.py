import numpy as np
import pytest
from ripleyk import ripleyk
import random


@pytest.fixture(scope="module")
def random_points_3d():
    """
    Generates a set of random 3D points within a sphere of radius 1,
    based on the data generation code provided in the README.md.
    `random.seed(0)` is used for reproducibility.
    """
    xs = []
    ys = []
    zs = []
    radius = 1
    random.seed(0)
    # The loop runs 10,000 times, but the number of points generated
    # will be lower because some points fall outside the sphere.
    for _ in range(10000):
        positioned = False
        while not positioned:
            x = random.uniform(-radius, radius)
            y = random.uniform(-radius, radius)
            z = random.uniform(-radius, radius)
            if (x**2) + (y**2) + (z**2) < radius**2:
                xs.append(x)
                ys.append(y)
                zs.append(z)
                positioned = True
    return np.array(xs), np.array(ys), np.array(zs)


def test_calculate_ripley_2d_single_radius(random_points_3d):
    xs, ys, _ = random_points_3d
    radius = 0.5
    bounding_radius = 1
    k = ripleyk.calculate_ripley(radius, bounding_radius, d1=xs, d2=ys)
    assert np.isclose(k, 0.757289, atol=1e-6)


def test_calculate_ripley_2d_single_radius_boundary_correct(random_points_3d):
    xs, ys, _ = random_points_3d
    radius = 0.5
    bounding_radius = 1
    k = ripleyk.calculate_ripley(
        radius, bounding_radius, d1=xs, d2=ys, boundary_correct=True
    )
    assert np.isclose(k, 0.864648, atol=1e-6)


def test_calculate_ripley_2d_single_radius_boundary_correct_csr_normalise(
    random_points_3d,
):
    xs, ys, _ = random_points_3d
    radius = 0.5
    bounding_radius = 1
    k = ripleyk.calculate_ripley(
        radius,
        bounding_radius,
        d1=xs,
        d2=ys,
        boundary_correct=True,
        CSR_Normalise=True,
    )
    assert np.isclose(k, 0.079249, atol=1e-6)


def test_calculate_ripley_3d_multiple_radii(random_points_3d):
    xs, ys, zs = random_points_3d
    radii = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    expected_k = [
        -9.290137551123609e-06,
        -0.00010544767161566743,
        -0.00039142698870800463,
        -0.0007282757869681578,
        -0.0013863220751694216,
        -0.002301632731796177,
        -0.002895761209242842,
        -0.004294205083374969,
        -0.005929855937486295,
        -0.007915443959695345,
    ]
    k = ripleyk.calculate_ripley(
        radii,
        1,
        d1=xs,
        d2=ys,
        d3=zs,
        boundary_correct=True,
        CSR_Normalise=True,
    )
    assert np.allclose(k, expected_k, atol=1e-6)

from scipy import spatial
import numpy as np


def make_tree(d1=None, d2=None, d3=None):
    active_dimensions = [
        dimension for dimension in [d1, d2, d3] if dimension is not None
    ]
    assert len(active_dimensions) > 0, "Must have at least 1-dimension to make tree"
    if len(active_dimensions) == 1:
        points = np.c_[active_dimensions[0].ravel()]
    elif len(active_dimensions) == 2:
        points = np.c_[active_dimensions[0].ravel(), active_dimensions[1].ravel()]
    else:
        points = np.c_[
            active_dimensions[0].ravel(),
            active_dimensions[1].ravel(),
            active_dimensions[2].ravel(),
        ]
    return spatial.cKDTree(points), len(active_dimensions)


def calculate_overlap(
    point_of_interest, bounding_size, score_radius, sample_shape, dimensions
):
    if dimensions == 1:
        d = point_of_interest[0][0]
        if d <= abs(score_radius - bounding_size):
            vol = score_radius
        elif d >= score_radius + bounding_size:
            vol = 0
        else:
            vol = max(
                0,
                min(bounding_size, d + score_radius)
                - max(-bounding_size, d - score_radius),
            )
    elif sample_shape == "circle":
        if dimensions == 2:
            d = np.sum((np.array(point_of_interest)) ** 2) ** 0.5
            if d <= abs(score_radius - bounding_size):
                vol = np.pi * score_radius**2
            elif d >= score_radius + bounding_size:
                vol = 0
            else:
                r2, R2, d2 = score_radius**2, bounding_size**2, d**2
                r, R = score_radius, bounding_size
                alpha = np.arccos((d2 + r2 - R2) / (2 * d * r))
                beta = np.arccos((d2 + R2 - r2) / (2 * d * R))
                vol = (
                    r2 * alpha
                    + R2 * beta
                    - 0.5 * (r2 * np.sin(2 * alpha) + R2 * np.sin(2 * beta))
                )
        elif dimensions == 3:
            d = np.sum((np.array(point_of_interest)) ** 2) ** 0.5
            if d >= score_radius + bounding_size:
                vol = 0
            elif bounding_size > (
                d + score_radius
            ):  # scoring radius is entirely contained in nucleus
                vol = (4 / 3) * np.pi * score_radius**3
            else:
                vol = (
                    np.pi
                    * (score_radius + bounding_size - d) ** 2
                    * (
                        d**2
                        + (
                            2 * d * score_radius
                            - 3 * score_radius**2
                            + 2 * d * bounding_size
                            - 3 * bounding_size**2
                        )
                        + 6 * score_radius * bounding_size
                    )
                ) / (12 * d)
    elif sample_shape == "rectangle":
        if dimensions == 2:
            pass
        elif dimensions == 3:
            pass

    assert vol > 0, (
        "Attempted to boundary correct a point not within the sample. "
        "Check sample_size and points."
    )
    return vol


def calculate_ripley(
    radii,
    sample_size,
    d1=None,
    d2=None,
    d3=None,
    sample_shape="circle",
    boundary_correct=False,
    CSR_Normalise=False,
):
    results = []
    tree, dimensions = make_tree(d1=d1, d2=d2, d3=d3)
    if type(radii) is not list:
        radii = [radii]
    for radius in radii:
        if dimensions == 1:
            score_vol = radius * 2
            bound_size = sample_size
            counts = 0
            for x in zip(d1):
                if boundary_correct:
                    vol = calculate_overlap(
                        [x], sample_size, radius, sample_shape, dimensions
                    )
                    boundary_correction = vol / score_vol
                    counts += (
                        len(tree.query_ball_point([x], radius)) - 1
                    ) / boundary_correction
                else:
                    counts += len(tree.query_ball_point([x], radius)) - 1
        elif dimensions == 2:
            score_vol = np.pi * radius**2
            if sample_shape == "circle":
                bound_size = np.pi * sample_size**2
            elif sample_shape == "rectangle":
                bound_size = sample_size[0] * sample_size[1]
            counts = 0
            for x, y in zip(d1, d2):
                if boundary_correct:
                    vol = calculate_overlap(
                        [x, y], sample_size, radius, sample_shape, dimensions
                    )
                    boundary_correction = vol / score_vol
                    counts += (
                        len(tree.query_ball_point([x, y], radius)) - 1
                    ) / boundary_correction
                else:
                    counts += len(tree.query_ball_point([x, y], radius)) - 1
        else:
            score_vol = (4 / 3) * np.pi * radius**3
            if sample_shape == "circle":
                bound_size = (4 / 3) * np.pi * sample_size**3
            elif sample_shape == "rectangle":
                bound_size = sample_size[0] * sample_size[1] * sample_size[2]
            counts = 0
            for x, y, z in zip(d1, d2, d3):
                if boundary_correct:
                    vol = calculate_overlap(
                        [x, y, z], sample_size, radius, sample_shape, dimensions
                    )
                    boundary_correction = vol / score_vol
                    counts += (
                        len(tree.query_ball_point([x, y, z], radius)) - 1
                    ) / boundary_correction
                else:
                    counts += len(tree.query_ball_point([x, y, z], radius)) - 1
        k_value = bound_size * counts / len(d1) ** 2
        if CSR_Normalise:
            k_value -= score_vol
        results.append(k_value)
    if len(results) == 1:
        return results[0]
    else:
        return results

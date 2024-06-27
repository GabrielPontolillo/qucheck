from QiskitPBT.property import Property
from QiskitPBT.stats.assertion import Assertion


def holm_bonferroni_correction(assertions_per_property: dict[Property, list[Assertion]], p_values_per_property: dict[Property, dict[Assertion, list[float]]], family_wise_alpha=0.05) -> dict[Property, dict[Assertion, list[float]]]:
    p_vals = []
    for property, assertions in assertions_per_property.items():
        for assertion in assertions:
            for p_value in p_values_per_property[property][assertion]:
                p_vals.append([p_value, property, assertion])
            
    # sort by p_val ascending order
    p_vals.sort(key=lambda x: x[0])
    for i, p_val in enumerate(p_vals):
        p_val[0] = (family_wise_alpha / (len(p_vals) - i))


    expected_p_vals = {}
    for p_value, property, assertion in p_vals:
        if property in expected_p_vals:
            if assertion in expected_p_vals[property]:
                expected_p_vals[property][assertion].append(p_value)
            else:
                expected_p_vals[property][assertion] = [p_value]
        else:
            expected_p_vals[property] = {assertion: [p_value]}

    return expected_p_vals

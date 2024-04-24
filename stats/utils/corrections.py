from QiskitPBT.stats.assertion import Assertion


def holm_bonferroni_correction(assertion_list: list[Assertion], p_values_per_assertion: list[list[float]], family_wise_alpha=0.05) -> list[list[float]]:
    p_vals = []
    for assertion_index in range(len(assertion_list)):
        for p_value_index, p_val in enumerate(p_values_per_assertion[assertion_index]):
            p_vals.append([assertion_index, p_value_index, p_val, None])

    # sort by p_val ascending order
    p_vals.sort(key=lambda x: x[2])
    for i, p_val in enumerate(p_vals):
        p_val[3] = (family_wise_alpha / (len(p_vals) - i))

    # sort by first then second index
    p_vals.sort(key=lambda x: (x[0], x[1]))
    
    expected_p_vals = [[x[3] for x in p_vals if x[0] == i] for i in range(len(assertion_list))]
    
    return expected_p_vals

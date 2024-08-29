# helper code to extract multiple experiments from a single, large experiment.
import random


def split_into_subsamples(counts: dict[str, int], number_of_subsamples: int = 50) -> list[dict[str, int]]:
    subsamples = []
    total_number_of_shots = sum(counts.values())

    for i in range(number_of_subsamples):
        # TODO: not sure about the floor division here
        # number of measurements needs to be evenly divisible by number of subsamples
        subsample = weighted_sample(counts, total_number_of_shots//number_of_subsamples)
        subsamples.append(subsample)

    return subsamples


def weighted_sample(counts: dict[str, int], number_of_samples: int) -> dict[str, int]:
    subsample = {}

    # sample without replacement from dictionary
    for i in range(number_of_samples):
        outcome = random.choices(list(counts.keys()), weights=counts.values())[0]

        # add the outcome to the subsample
        subsample[outcome] = subsample.get(outcome, 0) + 1

        # remove the outcome from the dictionary
        counts[outcome] -= 1
        if counts[outcome] == 0:
            del counts[outcome]

    return subsample
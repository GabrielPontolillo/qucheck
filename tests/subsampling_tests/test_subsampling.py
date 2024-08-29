import unittest


from qucheck.stats.utils.sampling import split_into_subsamples, weighted_sample

class TestSamplingUtils(unittest.TestCase):
    def tearDown(self):
        pass

    def test_split_into_subsamples_even_distribution(self):
        counts = {'11': 100, '10': 100, '00': 100}
        subsamples = split_into_subsamples(counts, 3)
        assert len(subsamples) == 3
        for subsample in subsamples:
            assert sum(subsample.values()) == 100

    def test_split_into_subsamples_uneven_distribution(self):
        counts = {'11': 100, '01': 50, '10': 25}
        subsamples = split_into_subsamples(counts, 5)
        assert len(subsamples) == 5
        for subsample in subsamples:
            assert sum(subsample.values()) == 35

    def test_split_into_subsamples_single_subsample(self):
        counts = {'11': 100, '10': 50, '00': 25}
        subsamples = split_into_subsamples(counts, 1)
        assert len(subsamples) == 1
        assert sum(subsamples[0].values()) == 175

    def test_weighted_sample_correct_distribution(self):
        counts = {'11': 100, '01': 50, '10': 25}
        subsample = weighted_sample(counts, 10)
        assert sum(subsample.values()) == 10

    def test_weighted_sample_empty_counts(self):
        self.assertRaises(IndexError, weighted_sample, {}, 10)

    def test_weighted_sample_more_samples_than_counts(self):
        counts = {'11': 5, '10': 3}
        self.assertRaises(IndexError, weighted_sample, counts, 10)
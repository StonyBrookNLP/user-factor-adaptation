import cPickle

import config


def load_factors_dict(fname):
    with open(fname, "rb") as f:
        factors_dict = cPickle.load(f)
    return factors_dict


def load_factors():
    config.factors = {}
    config.factors["age"] = load_factors_dict(config.age_pkl)
    config.factors["gender"] = load_factors_dict(config.gender_pkl)
    config.factors["personality"] = load_factors_dict(config.personality_pkl)
    config.factors["userembed"] = load_factors_dict(config.userembed_pkl)

    config.factors_metadata = {factor_name: None for factor_name in config.factors}


def compute_factor_metadata(factor_name, uids):
    """
    Compute the min, max, and average value for each factor.
    """
    factor_dict = config.factors[factor_name]
    num_dims = len(factor_dict.values()[0])
    factor_scores = [[] for _ in range(num_dims)]
    for uid in uids:
        for d in range(num_dims):
            factor_scores[d].append(factor_dict[uid][d])

    metadata = []
    for d in range(num_dims):
        min_score = min(factor_scores[d])
        max_score = max(factor_scores[d])
        avg_score = sum(factor_scores[d]) / len(factor_scores[d])
        metadata.append((min_score, max_score, avg_score))
    config.factors_metadata[factor_name] = metadata


def get_data():
    load_factors()
    data = {}
    uids = []
    with open(config.data_f, "r") as f:
        for i, line in enumerate(f):
            # Skip header line
            if i == 0:
                continue
            tid, uid, train_test, target, stance, tweet = line.strip().split("\t")
            if target not in data:
                data[target] = {"test": {}, "train": {}, "tune": {}}
            data[target][train_test][tid] = (uid, stance, tweet)
            if uid not in uids:
                uids.append(uid)
    for factor_name in config.factors:
        compute_factor_metadata(factor_name, uids)
    return data

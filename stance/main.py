import numpy as np

from scipy.sparse import coo_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.svm import LinearSVC

import config
import parse_data

from feature_extraction import extract_features


def create_feature_matrix(data, feat_dict=None):
    is_train = False
    if not feat_dict:
        is_train = True
        feat_dict = {}

    X = [[], [], []]
    Y = []

    cur_row = 0
    for tid in data:
        uid = data[tid][0]
        stance = data[tid][1]
        tweet = data[tid][2]

        if stance == "AGAINST":
            Y.append(-1)
        elif stance == "FAVOR":
            Y.append(1)
        else:
            Y.append(0)

        feats = extract_features(tweet, uid)

        for feat_name, feat_val in feats:
            if feat_name not in feat_dict:
                if is_train:
                    feat_dict[feat_name] = len(feat_dict)
                else:
                    continue
            feat_idx = feat_dict[feat_name]
            X[0].append(feat_val)
            X[1].append(cur_row)
            X[2].append(feat_idx)
        cur_row += 1
    nrows = len(Y)
    X_mat = coo_matrix((X[0], (X[1], X[2])), shape=(nrows, len(feat_dict)))
    X_array = X_mat.toarray()
    Y_array = np.array(Y)
    return X_array, Y_array, feat_dict


def compute_f1(predictions, labels):
    """
    Compute the F1 for FAVOR and AGAINST classes, as well as the average of the two.
    """
    _, _, f1, _ = precision_recall_fscore_support(predictions, labels,
                                                  warn_for=("f1"))
    f1_against = f1[0]
    f1_favor = f1[2]
    f1_overall = (f1_against + f1_favor) / 2
    return f1_against, f1_favor, f1_overall


def train_model(train_X, train_Y, tune_X, tune_Y):
    # SVM parameters
    fit_intercept = True
    penalty = "l2"
    loss = "squared_hinge"
    dual = True
    tol = .0001
    max_iter = 1000
    random_state = 5

    # Use tuning set to determine best value for c
    c_cands = [10 ** i for i in range(-5, 1, 1)]
    c_votes = {c: 0 for c in c_cands}
    f1s = []
    for c in c_cands:
        classif = LinearSVC(C=c, random_state=random_state, penalty=penalty,
                            fit_intercept=fit_intercept, loss=loss, dual=dual,
                            tol=tol, max_iter=max_iter)
        classif.fit(train_X, train_Y)
        predictions = classif.predict(tune_X)
        _, _, f1 = compute_f1(predictions, tune_Y)
        f1s.append(f1)
    best_f1 = max(f1s)
    best_cs = []
    for i in range(len(f1s)):
        if f1s[i] == best_f1:
            best_cs.append(str(c_cands[i]))
            c_votes[c_cands[i]] += 1

    # Train model using best value for c
    votes = [(y, x) for x, y in c_votes.items()]
    c_opt = sorted(votes, reverse=True)

    classif = LinearSVC(C=c_opt[0][1], random_state=random_state, penalty=penalty,
                        fit_intercept=fit_intercept, loss=loss, dual=dual, tol=tol,
                        max_iter=max_iter)
    classif.fit(train_X, train_Y)
    return classif


def initialize():
    config.tokenizer = None

    config.adapt = None
    if config.factor_type and config.adapt_type:
        config.adapt = "{}_{}".format(config.factor_type.lower(),
                                      config.adapt_type.lower())


def main():
    initialize()
    data = parse_data.get_data()

    all_predictions = []
    all_gold = []
    for target in data:
        if config.verbose:
            print target
        train_X, train_Y, feat_dict = create_feature_matrix(data[target]["train"],
                                                            feat_dict=None)
        tune_X, tune_Y, _ = create_feature_matrix(data[target]["tune"],
                                                  feat_dict=feat_dict)
        test_X, test_Y, _ = create_feature_matrix(data[target]["test"],
                                                  feat_dict=feat_dict)
        model = train_model(train_X, train_Y, tune_X, tune_Y)
        predictions = model.predict(test_X)

        _, _, f1 = compute_f1(predictions, test_Y)
        if config.verbose:
            print "\t", "F1:", round(f1 * 100, 2)
        all_predictions += list(predictions)
        all_gold += list(test_Y)
    f1_against, f1_favor, f1_overall = compute_f1(all_predictions, all_gold)
    print "F1 Against:", round(f1_against * 100, 2)
    print "F1 Favor:", round(f1_favor * 100, 2)
    print "---> Overall F1:", round(f1_overall * 100, 2)


if __name__ == '__main__':
    main()

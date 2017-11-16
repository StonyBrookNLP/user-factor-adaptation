import config

from adapt import apply_user_factor_adaptation
from happierfuntokenizing import Tokenizer


def extract_features(tweet, uid):
    if not config.tokenizer:
        config.tokenizer = Tokenizer()

    tokens = config.tokenizer.tokenize(tweet)

    feats = []

    # Character ngram features
    for n in range(2, 6):
        feats += get_char_ngram_feats(tweet, n)

    # Word ngram features
    for n in range(1, 4):
        feats += get_word_ngram_feats(tokens, n)

    feats += apply_user_factor_adaptation(feats, uid)

    return feats


def get_char_ngram_feats(tweet, n):
    feat_template = "CHAR:{}::".format(n)
    feats = []
    for i in range(len(tweet)):
        if i + n <= len(tweet):
            feat = feat_template + tweet[i:i + n]
            pair = (feat, 1)
            if pair not in feats:
                feats.append(pair)
    return feats


def get_word_ngram_feats(tokens, n):
    feat_template = "WORD:{}::".format(n)
    feats = []
    for i in range(len(tokens)):
        if i + n <= len(tokens):
            feat = feat_template + "|".join(tokens[i:i + n])
            pair = (feat, 1)
            if pair not in feats:
                feats.append(pair)
    return feats

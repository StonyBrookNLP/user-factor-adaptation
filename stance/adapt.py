import math

import config


def apply_user_factor_adaptation(feats, uid):
    age = config.factors["age"][uid][0]
    gender = config.factors["gender"][uid][0]
    persona = config.factors["personality"][uid]
    userembed = config.factors["userembed"][uid]

    new_feats = []
    if config.adapt == "age_disc":
        for feat_name, feat_val in feats:
            if age >= 28:
                adapted_feat_name = "ADAPT:AGE1:" + feat_name
                new_feats.append((adapted_feat_name, feat_val))
            elif age < 24:
                adapted_feat_name = "ADAPT:AGE2:" + feat_name
                new_feats.append((adapted_feat_name, feat_val))
    if config.adapt == "gender_disc":
        for feat_name, feat_val in feats:
            if gender >= 0:
                adapted_feat_name = "ADAPT:GENDER1:" + feat_name
                new_feats.append((adapted_feat_name, feat_val))
            else:
                adapted_feat_name = "ADAPT:GENDER2:" + feat_name
                new_feats.append((adapted_feat_name, feat_val))
    if config.adapt == "age_cont":
        age_sqrt = math.sqrt(age)
        age_min = config.factors_metadata["age"][0][0]
        age_max = config.factors_metadata["age"][0][1]
        for feat_name, feat_val in feats:
            age_adapt = feat_val
            age_adapt *= (age_sqrt - age_min) / (age_max - age_min)
            adapted_feat_name = "ADAPT:AGE:" + feat_name
            new_feats.append((adapted_feat_name, age_adapt))
    if config.adapt == "gender_cont":
        gender_min = config.factors_metadata["gender"][0][0]
        gender_max = config.factors_metadata["gender"][0][1]
        for feat_name, feat_val in feats:
            gender_adapt = feat_val
            gender_adapt *= (gender - gender_min) / (gender_max - gender_min)
            adapted_feat_name = "ADAPT:GENDER:" + feat_name
            new_feats.append((adapted_feat_name, gender_adapt))
    if config.adapt == "personality_disc":
        for feat_name, feat_val in feats:
            for i in range(len(persona)):
                if persona[i] >= 0:
                    adapted_feat_name = "ADAPT:PERSONALITY{}:".format(i + 1) + feat_name
                    new_feats.append((adapted_feat_name, feat_val))
    if config.adapt == "personality_cont":
        for feat_name, feat_val in feats:
            for i in range(len(persona)):
                min_val, max_val = config.factors_metadata["personality"][i][:2]
                persona_adapt = feat_val * (persona[i] - min_val) / (max_val - min_val)
                adapted_feat_name = "ADAPT:PERSONALITY{}:".format(i + 1) + feat_name
                new_feats.append((adapted_feat_name, persona_adapt))
    if config.adapt == "userembed_disc":
        for feat_name, feat_val in feats:
            for i in range(len(userembed)):
                avg = config.factors_metadata["userembed"][i][2]
                if userembed[i] >= avg:
                    adapted_feat_name = "ADAPT:USEREMBED{}:".format(i + 1) + feat_name
                    new_feats.append((adapted_feat_name, feat_val))
    if config.adapt == "userembed_cont":
        for feat_name, feat_val in feats:
            for i in range(len(userembed)):
                userembed_adapt = feat_val * userembed[i]
                adapted_feat_name = "ADAPT:USEREMBED{}:".format(i + 1) + feat_name
                new_feats.append((adapted_feat_name, userembed_adapt))
    return new_feats


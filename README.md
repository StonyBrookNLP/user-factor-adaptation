# User-Factor Adaptation

User-factor adaptation is the general task of adapting NLP models to real-valued human attributes, or *factors*.

Details about user-factor adaptation and our approach to this problem can be found in:
```
@inproceedings{Lynn2017EMNLP,
title={Human Centered {NLP} with User-Factor Adaptation},
author={Veronica E. Lynn and Youngseo Son and Vivek Kulkarni and Niranjan Balasubramanian and H. Andrew Schwartz},
booktitle={Empirical Methods in Natural Language Processing},
location={Copenhagen, Denmark},
year={2017}
}
```

Please contact velynn@cs.stonybrook.edu with questions or comments.

## PP-Attachment Dataset

This is all the data that was used for the prepositional-phrase attachment task.

The data is formatted as follows:
```
TWEET    <message id>    <user id>
<token index>    <token>    <parent index>
<token index>    <token>    <parent index>
...
```
Note that a token will only have its parent listed if it's a preposition. A parent index of 0 indicates that the parent is outside the parse tree. Note that some tweets may contain more than one preposition.

333 of these tweets were obtained from the [Tweeboparser dataset](https://github.com/ikekonglp/TweeboParser). The remaining 986 are new tweets that we annotated.

## User-Factor Adaptation for Stance Detection

This is an implementation of the top performing stance detection system from [SemEval-2016 Task 6](http://alt.qcri.org/semeval2016/task6/), SVM-ngrams, with user-factor adaptation added to it.

To run with adaptation, change the following variables in ``config.py``.
- ``adapt_type`` : Whether to use discrete or continuous adaptation. Options are None, "disc", "cont".
- ``factor_type``: Which factor to adapt to. Options are None, "age", "gender", "personality", "userembed". *TF-IDF and word2vec coming soon.*

If one or both variables is set to ``None``, no adaptation will be used. Once that's done, simply run ``python main.py``.

## User Factor Inference

Coming soon!
# User-Factor Adaptation

User-factor adaptation is the general task of adapting NLP models to real-valued human attributes, or *factors*.

Detail about user-factor adaptation and our approach to this problem can be found in:
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

Coming soon!

## User Factor Inference

Coming soon!
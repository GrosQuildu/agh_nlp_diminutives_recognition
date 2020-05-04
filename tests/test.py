#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test quality of rozpoznawaczek tool.

    Authors:
    * Izabela Stechnij
    * Dominik Sepioło
    * Paweł Płatek
"""

import logging
from functools import partial
from typing import Optional, Tuple

from rozpoznawaczek import (IsDiminutiveFunc, diminutive_sets,
                            find_diminutives, has_diminutive_suffix)

L = logging.getLogger(__name__)


# not using that one anywhere
def count_diminutives_whole_text(filename: str, is_diminutive_func: Optional[IsDiminutiveFunc] = None) -> Tuple[int, int]:
    """Counts how many words were recognized as diminutives in the given file.

    Args:
        filename: count words in the file with filename filename :D
        is_diminutive_func: None to use default function

    Returns:
        diminutives, not_diminutives
    """
    with open(filename, 'r') as f:
        text = f.read()

    if is_diminutive_func:
        results = find_diminutives(text, is_diminutive_func)
    else:
        results = find_diminutives(text)

    return len(results), len(text.split('\n')) - len(results)


def count_diminutives(filename: str, is_diminutive_func: Optional[IsDiminutiveFunc] = None) -> Tuple[int, int]:
    """Counts how many words were recognized as diminutives in the given file.

    Args:
        filename: count words in the file with filename filename :D
                  the file must have one word per line
        is_diminutive_func: None to use default function

    Returns:
        diminutives, not_diminutives
    """
    diminutives = 0
    not_diminutives = 0
    with open(filename, 'r') as f:
        for line in f:
            word = line.strip().lower()
            if word:
                if is_diminutive_func:
                    results = find_diminutives(word, is_diminutive_func)
                else:
                    results = find_diminutives(word)

                # we are parsing one word at a time
                assert len(results) <= 1

                if len(results) == 1:
                    result = results[0]

                    # match start of the word
                    assert result[0] == 0

                    # match end of the word
                    assert result[1] == len(word)

                    diminutives += 1
                    L.debug('%s - diminutive', word)
                else:
                    not_diminutives += 1
                    L.debug('%s - normal word', word)

    return diminutives, not_diminutives


def get_statistical_measures(is_diminutive_func: Optional[IsDiminutiveFunc] = None)\
        -> Tuple[int, int, int, int, float, float]:
    """For given function compute:
        true-positives, true-negatives, false-positives, false-negatives,
        precision, recall

    Args:
        is_diminutive_func: None to use default function
    """
    diminutives_file = './tests/training_diminutives.txt'
    not_diminutives_file = './tests/training_not_diminutives.txt'

    L.debug('')
    L.debug('Diminutives:')
    tp, fn = count_diminutives(diminutives_file, is_diminutive_func)
    L.debug('-' * 30)

    L.debug('Normal words:')
    fp, tn = count_diminutives(
        not_diminutives_file, is_diminutive_func)
    L.debug('-' * 30)

    L.info(f'True positives: {tp}')
    L.info(f'False negatives: {fn}')
    L.info(f'False positives: {fp}')
    L.info(f'True negatives: {tn}')

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    L.warning(f'Precision: {precision}')
    L.warning(f'Recall: {recall}')
    L.warning('~*'*30)

    return tp, fn, fp, tn, precision, recall


def is_diminutive_simple_partial(word: str, _: IsDiminutiveFunc, **kwargs) -> bool:
    """Just check word's suffix"""
    return has_diminutive_suffix(word, kwargs['suffix_set'])


def test_training_data():
    # our cool function is ok in general
    L.warning('Our function:')
    *{}[1], precision_our, recall_our = get_statistical_measures()
    assert precision_our > 0.8
    assert recall_our > 0.55

    # compare our sophisticated function with the simplest suffix matching function (with different suffixes sets)
    for suffix_set_name, suffix_set in diminutive_sets.items():
        L.warning('Suffix set %s:', repr(suffix_set_name))
        is_diminutive_simple = partial(
            is_diminutive_simple_partial, suffix_set=suffix_set)
        *{}[1], precision_simple, recall_simple = get_statistical_measures(is_diminutive_simple)
        assert precision_our >= precision_simple or precision_simple > 0.95
        assert recall_our >= recall_simple or recall_simple > 0.95


L.setLevel('INFO')
test_training_data()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
~IS, DS, PP
'''


from rozpoznawaczek import parse_text


def count_diminitives(filename):
    """
    Given file with one word in a line
    Count how many words were recognized as diminutives

    Args:
        filename(str)

    Returns
        tuple(int,int) - (diminutives, not_diminutives)
    """
    diminutives = 0
    not_diminutives = 0
    with open(filename, 'r') as f:
        for line in f:
            word = line.strip().lower()
            if word:
                results = parse_text(word)

                # we are parsing one word at a time
                assert len(results) <= 1

                if len(results) == 1:
                    result = results[0]

                    # match start of the word
                    assert result[0] == 0

                    # match end of the word
                    assert result[1] == len(word)

                    diminutives += 1
                    print(f'{word} - diminutive')
                else:
                    not_diminutives += 1
                    print(f'{word} - normal word')

    return diminutives, not_diminutives


def test_training_data():
    diminutives_file = './tests/training_diminutives.txt'
    not_diminutives_file = './tests/training_not_diminutives.txt'

    print('')
    print('Diminutives:')
    tp, fn = count_diminitives(diminutives_file)
    print('-'*30)

    print('Normal words:')
    fp, tn = count_diminitives(not_diminutives_file)
    print('-'*30)

    print(f'True positives: {tp}')
    print(f'False negatives: {fn}')
    print(f'False positives: {fp}')
    print(f'True negatives: {tn}')

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    print(f'Precision: {precision}')
    print(f'Recall: {recall}')

    assert precision > 0.8
    assert recall > 0.55

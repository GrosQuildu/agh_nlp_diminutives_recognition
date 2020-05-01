#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
~IS, DS, PP
'''

import morfeusz2  # http://morfeusz.sgjp.pl/download/
from random import randint
import sys
from collections import defaultdict


# http://www.ipipan.waw.pl/~wolinski/publ/znakowanie.pdf
GRAM_FLEX = defaultdict(lambda: 'nieznane', {
    'subst':   'rzeczownik',  #
    'depr':    'rzeczownik',  # forma deprecjatywna
    'adj':     'przymiotnik', # 
    'adja':    'przymiotnik', # przymiotnik przyprzymiotnikowy
    'adjp':    'przymiotnik', # przymiotnik poprzyimkowy
    'adv':     'przyslowek',  # przysłówek odprzymiotnikowy i/lub stopniowalny
    'num':     'przymiotnik', # liczebnik
    'ppron12': 'zaimek',      # nietrzecioosobowy
    'ppron3':  'zaimek',      # trzecioosobowy
    'siebie':  'siebie',      # magiczne słowo "siebie"
    'fin':     'czasownik',   # forma nieprzeszła
    'bedzie':  'czasownik',   # forma przyszła czasownika 
    'aglt':    'czasownik',   # aglutynant czasownika "być"
    'praet':   'czasownik',   # pseudoimiesłów
    'impt':    'czasownik',   # rozkaźnik
    'imps':    'czasownik',   # bezosobnik
    'inf':     'czasownik',   # bezokolicznik
    'pcon':    'czasownik',   # imiesłów przys. współczesny
    'pant':    'czasownik',   # imiesłów przys. uprzedni
    'ger':     'czasownik',   # odsłownik
    'pact':    'czasownik',   # imiesłów przym. czynny
    'ppas':    'czasownik',   # imiesłów przym. bierny
    'winien':  'winien',      # potężne słowo "winien"
    'pred':    'predykatyw',  #
    'prep':    'przyimek',    #
    'conj':    'spójnik',     #
    'qub':     'kublik',      # partykuło-przysłówek
    'xxs':     'obce',        # ciało obce nominalne
    'xxx':     'obce',        # ciało obce luźne
    'sp':      'separator',   # whitespace, spacja itp
    'interp':  'separator',   # kropki itp
    'ign':     'nieznane',    # nie wiadomo, nie wiaaaadooomooo...
})

GRAM_CATEGORY = {
    'sg':      'liczba',          # pojedyncza
    'pl':      'liczba',          # mnoga
    'nom':     'przypadek',       # mianownik
    'gen':     'przypadek',       # dopełniacz
    'dat':     'przypadek',       # celownik
    'acc':     'przypadek',       # biernik
    'inst':    'przypadek',       # narzędnik
    'loc':     'przypadek',       # miejscownik
    'voc':     'przypadek',       # wołacz
    'm1':      'rodzaj',          # męski osobowy
    'm2':      'rodzaj',          # męski zwierzęcy
    'm3':      'rodzaj',          # męski rzeczowy
    'f':       'rodzaj',          # żeński
    'n1':      'rodzaj',          # nijaki zbiorowy
    'n2':      'rodzaj',          # nijaki zwykły
    'p1':      'rodzaj',          # przymnogi osobowy
    'p2':      'rodzaj',          # przymnogi zwykły
    'p3':      'rodzaj',          # przymnogi opisowy
    'pri':     'osoba',           # pierwsza
    'sec':     'osoba',           # druga
    'ter':     'osoba',           # trzecia
    'pos':     'stopień',         # równy
    'comp':    'stopień',         # wyższy
    'sup':     'stopień',         # najwyższy
    'imperf':  'aspekt',          # niedokonany
    'perf':    'aspekt',          # niedokonany
    'aff':     'zanegowanie',     # niezanegowana
    'neg':     'zanegowanie',     # zanegowana
    'akc':     'akcentowość',     # akcentowana
    'nakc':    'akcentowość',     # nieakcentowana
    'praep':   'poprzyimkowość',  # poprzyimkowa
    'npraep':  'poprzyimkowość',  # niepoprzyimkowa
    'congr':   'akomodacyjność',  # uzgadniająca
    'rec':     'akomodacyjność',  # rządząca
    'agl':     'aglutynacyjność', # aglutynacyjna
    'nagl':    'aglutynacyjność', # nieaglutynacyjna
    'wok':     'wokaliczność',    # wokaliczna
    'nwok':    'wokaliczność',    # niewokaliczna
    'col':     'przyrodzaj',      # zbiorowy
    'ncol':    'przyrodzaj',      # główny
    'pt':      'przyrodzaj',      # zbiorowy plurale tantum
}


# Paulina Biały – Polish and English Diminutives in Literary Translation: Pragmatic and Cross-Cultural Perspectives
# Długosz, nouns
suf_dlugosz_noun_masculine = ['ak', 'ek', 'uszek', 'aszek', 'ątek', 'ik', 'yk', 'czyk']
suf_dlugosz_noun_feminine = ['ka', 'eczka', 'yczka', 'ułka', 'uszka', 'etka', 'eńka']
suf_dlugosz_noun_neuter = ['ko', 'eczko', 'eńko', 'etko', 'uszko', 'onko', 'ątko', 'ączko']
suf_dlugosz_noun_plural_and_plurale_tantum =  ['ki', 'iki', 'yki', 'iczki', 'uszki', 'ka', 'eczka']
suf_dlugosz_noun_other = ['ę', 'iszek']

# Grzegorczykowa and Puzynina, Dobrzyński, Kaczorowska
suf_gpdk_noun = ['a', 'aś', 'cia', 'cio', 'eniek', 'ina', 'isia', 'ysia', 'nia', 'onek', 'sia', 'sio', 'siu', 'uchna', 'uchno', 'uchny', 'ula', 'ulek', 'ulo', 'alek', 'unia', 'unio', 'uń', 'usia', 'usio', 'usiek', 'uś', 'inka', 'ynka', 'aczek']
suf_gpdk_noun += ['isko']  # Kreja

# Grzegorczykowa
suf_grzeg_adjectives = ['utki', 'uteńki', 'usieńki', 'uchny', 'uśki', 'eńki', 'usi', 'uteczki', 'utenieczki', 'usienieczki']
suf_grzeg_adjectives += ['awy']  # Szymanek


DIMINUTIVE_PROBABILITY_TRESHOLD = 0.51


def diminutive_probability(word):
    """
    Diminutive recognition

    Args:
        list(tuple(start_segment, end_segment, morfology interpretation))

    Returns:
        bool
    """
    # text_form, lemma, morfology_marker, ordinariness, stylistic_qualifiers = word_morfology
    # return randint(0,2) / 2
    return 1


def parse_text(text, is_diminutive_func):
    """
    1. Tokenize (split to a list of words) the text
    2. Lemmatise (find base forms) every token/word.
    3. Check every word (as a list of lemmas) if it's a diminutive
    4. Returns list of start and end positions of diminutive words

    Args:
        text(str)
        is_diminutive_func(callable)
            input: same as `morf.analyse` output

    Returns:
        list(tuple(int, int)) - list with start and end position of diminutives
    """
    morf = morfeusz2.Morfeusz(whitespace=morfeusz2.KEEP_WHITESPACES)
    text_analyzed = morf.analyse(text)

    position_in_text = 0  # position in input text (string)
    i = 0  # position in analyzed text (list)
    '''
    text = 'miałaś babo kurę'
    text_analyzed =
        [(0, 1, ('miała', 'mieć', 'praet:sg:f:imperf', [], [])),
         (1, 2, ('ś', 'być', 'aglt:sg:sec:imperf:nwok', [], [])),
         (2, 3, (' ', ' ', 'sp', [], [])),
         (3, 4, ('babo', 'baba:s1', 'subst:sg:voc:f', ['nazwa_pospolita'], [])),
         (3, 4, ('babo', 'baba:s2', 'subst:sg:voc:m1', ['nazwa_pospolita'], [])),
         (4, 5, (' ', ' ', 'sp', [], [])),
         (5, 6, ('kurę', 'kura', 'subst:sg:acc:f', ['nazwa_pospolita'], []))]

    `i` just iterates over the list, whereas
    `position_in_text` keeps track on original words (f.e. 'miała' + 'ś')
    '''

    # skip leading separators
    normal_word_found = False
    while i < len(text_analyzed) and not normal_word_found:
        segment_start, segment_end, word_morfology = text_analyzed[i]
        text_form, _, morfology_marker, _, _ = word_morfology

        if GRAM_FLEX[morfology_marker] != 'separator':
            normal_word_found = True
        else:
            # assumption: separators have only one item in text_analyzed
            position_in_text += len(text_form)
            i += 1

    # ok, go trough the rest of analyzed text
    diminutives = []
    while i < len(text_analyzed):
        # invariant: i < len(text_analyzed)
        # invariant: text_analyzed[i] is some word (not a separator)
        # invariant: position_in_text points to the beginning of the word

        # collect all possible segments related to the word
        segments = []
        word_morfology = None
        whitespace_found = False
        while i < len(text_analyzed) and not whitespace_found:
            _, _, word_morfology = text_analyzed[i]
            _, _, morfology_marker, _, _ = word_morfology

            if GRAM_FLEX[morfology_marker] == 'separator':
                whitespace_found = True
            else:
                segments.append(word_morfology)
                i += 1
        # invariant: i==len(text_analyzed) or text_analyzed[i] is separator
        # invariant: len(segments) > 0
        # invariant: word_morfology == text_analyzed[i][2]

        # update positions in the text
        if i == len(text_analyzed):
            end_position_in_text = len(text)
            to_skip = 0
        else:
            separator = word_morfology[0]
            end_position_in_text = text.index(separator, position_in_text)
            to_skip = len(separator)
            i += 1
        # invariant: (position_in_text, end_position_in_text) matches one word

        # is diminutive?
        if is_diminutive_func(segments):
            diminutives.append((position_in_text, end_position_in_text))

        # update positions in the text
        position_in_text = end_position_in_text + to_skip

        # skip following separators
        normal_word_found = False
        while i < len(text_analyzed) and not normal_word_found:
            segment_start, segment_end, word_morfology = text_analyzed[i]
            text_form, _, morfology_marker, _, _ = word_morfology

            if GRAM_FLEX[morfology_marker] != 'separator':
                normal_word_found = True
            else:
                # assumption: separators have only one item in text_analyzed
                position_in_text += len(text_form)
                i += 1

    return diminutives


def main():
    # read text line by line
    while True:
        text = sys.stdin.readline()
        if not text:
            break

        # find diminutives
        diminutives = parse_text(text)

        # print them
        print(f'line: {repr(text)}')
        for diminutive in diminutives:
            start_position, end_position = diminutive
            print(f'd: {text[start_position:end_position]}')


if __name__ == "__main__":
    main()

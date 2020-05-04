#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tool for recognizing diminutives in a text.

    Example:
    L.setLevel('INFO')
    text = 'A potem gorzki los tych niewiniątek\nWiędnąć na włosach i sercach dziewczątek;'
    print([text[start:end] for start, end in find_diminutives(text)])

    Authors:
    * Izabela Stechnij
    * Dominik Sepioło
    * Paweł Płatek
"""

from rozpoznawaczek.rozpoznawaczek import (Interpretation, IsDiminutiveFunc, L,
                                           diminutive_sets, find_diminutives,
                                           has_diminutive_suffix, main)

__all__ = ['find_diminutives', 'main', 'L', 'Interpretation', 'IsDiminutiveFunc', 'has_diminutive_suffix',
           'diminutive_sets']

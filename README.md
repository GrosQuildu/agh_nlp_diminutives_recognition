# Rozpoznawaczek

Tool for recognizing [polish diminutives](https://en.wikipedia.org/wiki/List_of_diminutives_by_language#Polish).

```sh
usage: rozpoznawaczek [-h] [-f FILE] [-v]

Recognise diminutives

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Load text from a file
  -v, --verbose         debug output
```

Examples:
```sh
$ echo 'Kawki, herbatki moje kochanie?' | rozpoznawaczek
Parsing line: 'Kawki, herbatki moje kochanie?'
Diminutives:
- 'Kawki'
- 'herbatki'

$ echo 'Jajeczko' | rozpoznawaczek -v
Parsing line: 'Jajeczko'
Probability for `Jajeczko` (Jajeczko, jajeczko, subst:sg:nom.acc.voc:n:ncol)
    -> rzeczownik
        -> liczba pojedyncza
        -> rodzaj nijaki
    -> probability: 0.666667
Diminutives:
- 'Jajeczko'
```

## Algorith

1. Tokenize (split to a list of words) the text
2. Lemmatise (find possible base forms) every token/word
3. Check every word (with the list of possible lemmas) if it's a diminutive

    3.1. For every possible lemma of the word compute probability of the lemma being a diminutive
    
        3.1.1. Find what part of speech the lemma is (nount, adjective, unknown, something other)
        3.1.2. If "something other" return 0
        3.1.3. Else choose appropriate sets of suffixes
        3.1.4. For every such set check if the lemma "matches": ends with any suffix from the set
        3.1.5. Return probability as number of "matching" sets divided by number of selected sets
    
    3.2. Compute mean probability from all lemmas probabilities
    3.3. Check if the mean is greater than hardcoded treshold 

## Build'n'run

Docker:
```sh
git clone https://github.com/GrosQuildu/agh_nlp_diminutives_recognition
cd agh_nlp_diminutives_recognition
docker build -t rozpoznawaczek .
docker run -it rozpoznawaczek
```

Local dev:
```sh
git clone https://github.com/GrosQuildu/agh_nlp_diminutives_recognition
cd agh_nlp_diminutives_recognition

# install morfeusz2 for your environment: http://morfeusz.sgjp.pl/download/

pip install rozpoznawaczek -e '.[dev]'
python -m pytest -s ./tests/test.py
```

# Authors
* Izabela Stechnij
* Dominik Sepioło
* Paweł Płatek

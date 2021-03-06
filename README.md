# Rozpoznawaczek

Tool for recognizing [polish diminutives](https://en.wikipedia.org/wiki/List_of_diminutives_by_language#Polish).

```sh
usage: rozpoznawaczek [-h] [-i INPUT] [-v]

Recognise diminutives

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Load text from a file
  -v, --verbose         debug output
```

Examples:
```sh
$ echo 'Kawki, herbatki moje kochanie?' | rozpoznawaczek
Parsing line: 'Kawki, herbatki moje kochanie?'
Diminutives:
- 'Kawki'
- 'herbatki'

$ echo 'Jajeczkami' | rozpoznawaczek -v
Parsing line: 'Jajeczkami'
Probability for `Jajeczkami` (Jajeczkami, jajeczko, subst:pl:inst:n:ncol)
    -> Matched against Paweł Miczko
    -> rzeczownik
        -> liczba mnoga
    -> Not matched against Długosz
    -> re-running checks for lemma!
~*~*~*~*~*
Probability for `jajeczko` (jajeczko, jajeczko, subst:sg:nom.acc.voc:n:ncol)
    -> Matched against Paweł Miczko
    -> rzeczownik
        -> liczba pojedyncza
        -> rodzaj nijaki
    -> Matched against Długosz
    -> Not matched against GPDK
    -> probability: 0.666667
~*~*~*~*~*
    -> Not matched against GPDK
    -> probability: 0.500000
Diminutives:
- 'Jajeczkami'
```

## Algorithm

1. Tokenize (split to a list of words) the text
2. Lemmatise (find possible base forms) every token/word
3. Check every word (with the list of possible lemmas) if it's a diminutive

    3.1. For every possible lemma of the word compute probability of the word being a diminutive                
    * 3.1.1. Find what part of speech the word is (noun, adjective, unknown or something other)
    * 3.1.2. If "something other" return 0
    * 3.1.3. Else choose appropriate sets of suffixes
    * 3.1.4. For every such set check if the lemma (or word) "matches": ends with any suffix from the set
    * 3.1.5. Return probability as a number of "matching" sets divided by a number of selected sets
    
    3.2. Compute mean probability from all lemmas probabilities
    
    3.3. Check if the mean is greater than hardcoded threshold 

## Highlighter
```sh
usage: rozpoznawaczek-docx [-h] -i INPUT -o OUTPUT [-f]
                           [-c {AUTO,BLACK,BLUE,BRIGHT_GREEN,DARK_BLUE,...}]
                           [-v]

Hightlight diminutives in `docx` document

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input docx file
  -o OUTPUT, --output OUTPUT
                        Output docx file
  -f, --force           Force output overwrite
  -c {AUTO,BLACK,BLUE,,...}, --color {AUTO,BLACK,BLUE,...}
                        Color to highlight diminutives
  -v, --verbose         debug output
```

![Example docx](example.png?raw=true "Example docx")

## Build'n'run

Docker:
```sh
git clone https://github.com/GrosQuildu/agh_nlp_diminutives_recognition
cd agh_nlp_diminutives_recognition
docker build -t rozpoznawaczek .

# run interactive tool
docker run -it rozpoznawaczek

# to highlight document
mkdir output && chmod 777 output
docker run --mount type=bind,source="$(pwd)",target=/nlp -it rozpoznawaczek \
    rozpoznawaczek-docx -i /nlp/example.docx -o /nlp/output/example.docx -f -c VIOLET
```

Local dev:
```sh
git clone https://github.com/GrosQuildu/agh_nlp_diminutives_recognition
cd agh_nlp_diminutives_recognition

# install morfeusz2 for your environment: http://morfeusz.sgjp.pl/download/

pip install -e '.[DEV]'
python -m pytest --log-cli-level=INFO ./tests/test.py
```

## Quality

How good is our algorithm compared to simple suffix matching function (with different suffix sets):

```yaml
Our function:
Precision: 0.85
Recall: 0.6710526315789473
~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
Suffix set 'dlugosz':
Precision: 0.75
Recall: 0.6710526315789473
~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
Suffix set 'gpdk':
Precision: 0.6981132075471698
Recall: 0.4868421052631579
~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
Suffix set 'grzegorczykowa':
Precision: 1.0
Recall: 0.14473684210526316
~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
Suffix set 'miczko':
Precision: 0.9696969696969697
Recall: 0.42105263157894735
~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
```

# Authors
* Izabela Stechnij
* Dominik Sepioło
* Paweł Płatek

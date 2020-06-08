# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tool for highlighting diminutives in a docx file.
    Example:
        
    Authors:
    * Izabela Stechnij
    * Dominik Sepioło
    * Paweł Płatek
"""


import argparse
from os.path import isfile

from docx.enum.text import WD_COLOR_INDEX
from docx.shared import RGBColor
from docx import Document
from copy import copy

from rozpoznawaczek.rozpoznawaczek import L, find_diminutives


def highlight(document):
    for paragraph in document.paragraphs:
        for run in paragraph.runs:
            original_text = run.text
            diminutives = find_diminutives(original_text)
            run.clear()

            coursor = 0
            for start_position, end_position in diminutives:
                run.add_text(original_text[coursor:start_position])  # normal text
                run.add_text(original_text[start_position:end_position])  # diminutive
                coursor = end_position
            run.add_text(original_text[coursor:len(original_text)])  # normal text

    return document


def main():
    parser = argparse.ArgumentParser(description='Hightlight diminutives')
    parser.add_argument(
        '-i', '--input', help='Input docx file', required=True)
    parser.add_argument(
        '-o', '--output', help='Output docx file', required=True)
    parser.add_argument(
        '-f', '--force', help='Force output overwrite', action='store_true')
    parser.add_argument("-v", "--verbose", help="d,ebug output",
                        action="store_true")

    args = parser.parse_args()

    L.setLevel('INFO')
    if args.verbose:
        L.setLevel('DEBUG')

    if not isfile(args.input):
        L.error('Not such file: %s', args.input)
        return

    if not args.force and isfile(args.output):
        L.error('File exists: %s', args.output)
        return

    try:
        document = Document(args.input)
    except PythonDocxError as e:
        L.error('Error when opening input file: %s', e)
        return

    highlighted_document = highlight(document)
    highlighted_document.save(args.output)


if __name__ == "__main__":
    main()

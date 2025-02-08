#!/usr/bin/env python3
"""
Usage: cccards.py [-h -o cards.pdf -w 5 -d ,] FRONT_CSV [BACK_CSV]

Generate a PDF of cards for the Newcastle Code Club game:

    Who Programs The Programmers?

A CSV of functions and their weighting should be provided for the
front of the cards. If double side printing is required (e.g. for
both Strudel and Hydra) you can optionally also provide a CSV for
the back of the cards.

-h --help           Show this help
-o --output=FILE    Output PDF fle [default: cards.pdf]
-w --wildcards=<n>  Number of wildcards to generate [default: 5]
-d --delimiter=<c>  Character to use as delimiter [default: ,]
"""

import random
import math
import csv
from typing import List
from docopt import docopt
from fpdf import FPDF, Align

class DeckBuilder:
    """
    Generates a PDF from a set of CSV files, positioning 4 cards per row and
    7 rows per page (for a total of 28 cards per page).

    If only one CSV file is provided then the cards are designed to be printed
    single sided. If two CSV files are provided then the pages are interleaved
    to allow double sided printing.

    If printing two sided, then the number of cards in the front and back are
    automatically balanced.

    Optionally, a number of wildcards can also be printed. If two sided
    printing is used then the wildcards will be aligned to be wild on both
    sides.
    """

    CARDS_PER_PAGE = 28
    CARD_WIDTH = 48
    CARD_HEIGHT = 40

    def __init__(self,
                 front_csv: str,
                 back_csv: str = None,
                 wildcards: int = 5,
                 delimiter: str = ',') -> None:
        self.front_cards = self.load_csv(front_csv, delimiter)
        if back_csv:
            self.back_cards = self.load_csv(back_csv, delimiter)
            self.balance()
            self.shuffle()
            self.back_cards += ["*"] * wildcards
        else:
            self.back_cards = []
        self.front_cards += ["*"] * wildcards

    def load_csv(self, filename: str, delim: str =',') -> List:
        """
        Load a card CSV file. This should be of the format:

        card text,weight

        Where 'card text' is the text to appear on the card and 'weight;
        is the number of that card which should appear in the deck.

        This function applies the supplied weights and returns a final list
        of cards.
        """
        cards = []
        with open(filename, 'r', encoding='utf-8') as f:
            data = csv.reader(f, delimiter=delim)
            for row in data:
                cards += [row[0]] * int(row[1])
        return cards

    def balance(self) -> None:
        """
        Balance the front and back decks so they have the same number of cards.
        This is done by randomly selecting cards from the deck with the fewest
        cars until both decks match.
        """
        while len(self.front_cards) > len(self.back_cards):
            self.back_cards.append(random.choice(self.back_cards))
        while len(self.back_cards) > len(self.front_cards):
            self.front_cards.append(random.choice(self.front_cards))

    def save(self, filename: str) -> None:
        """
        Generates a PDF of cards and saves it to 'filename'
        """
        pdf = FPDF()
        page = 0
        total_pages = math.ceil(max(
            len(self.front_cards) / self.CARDS_PER_PAGE,
            len(self.back_cards) / self.CARDS_PER_PAGE))
        side = self.front_cards
        while page < total_pages:
            pdf.add_page()
            pdf.ln(10)
            cell = 0
            card_in_row = 1
            for card in side[page * self.CARDS_PER_PAGE:(page+1) * self.CARDS_PER_PAGE]:
                if card == '*':
                    pdf.set_font('helvetica', style='B', size=32)
                else:
                    pdf.set_font('helvetica', style='B', size=14)
                if side == self.back_cards:
                    # Reverse direction so wildcard front and back matches up
                    # after page is flipped
                    pdf.set_x(-self.CARD_WIDTH * card_in_row - 9)
                pdf.cell(self.CARD_WIDTH, None, card, align=Align.C)
                cell+=1
                card_in_row+=1
                if cell % 4 == 0:
                    card_in_row = 1
                    pdf.ln(self.CARD_HEIGHT)
            if self.back_cards and side == self.front_cards:
                side = self.back_cards
            else:
                page += 1
                side = self.front_cards
        pdf.output(filename)

    def shuffle(self) -> None:
        """
        Shuffle the front and back of the decks to get random pairings.
        """
        random.shuffle(self.front_cards)
        random.shuffle(self.back_cards)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    deck = DeckBuilder(arguments['FRONT_CSV'],
                       arguments['BACK_CSV'],
                       int(arguments['--wildcards']),
                       arguments['--delimiter'])
    deck.save(arguments['--output'])

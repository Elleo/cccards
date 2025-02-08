# Creative Code Cards

Generates a PDF from a set of CSV files, positioning 4 cards per row and 7 rows per page (for a total of 28 cards per page).

If only one CSV file is provided then the cards are designed to be printed single sided. If two CSV files are provided then the pages are interleaved to allow double sided printing.

If printing two sided, then the number of cards in the front and back are automatically balanced.

Optionally, a number of wildcards can also be printed. If two sided printing is used then the wildcards will be aligned to be wild on both sides.

## Usage

```
cccards.py [-h -o cards.pdf -w 5 -d ,] FRONT_CSV [BACK_CSV]

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
```

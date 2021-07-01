from collections import namedtuple

QuoteModel = namedtuple('Quote', ['body', 'author'])
# I am using namedtuple and not coding a class from scratch
# file is named differently from the class to avoid confusion

"""Natural Language Processor
"""
import sys
import argparse
import nltk.data
from nltk.tokenize import word_tokenize
import enchant  # needs 'es_ES' dict
from helpers import data_manager as dm


class StandUpError(Exception):
    pass


class Processor():
    DICT_TAG = 'es_ES'

    def __init__(self):
        self._stand_up()
        self._dictionary = enchant.Dict(tag=self.DICT_TAG)
        self._corrector = LanguageCorrector()

    def _stand_up(self):
        """ Assert dependencies OK"""
        if dm.require_updates():
            raise StandUpError("Missing data packages")
        self._load_dictionary()

    def _load_dictionary(self):
        try:
            self._dictionary = enchant.Dict(tag=self.DICT_TAG)
        except enchant.errors.DictNotFoundError:
            raise StandUpError("Missing " + self.DICT_TAG + " dictionary")

    def process(self, text):
        corrected_text = self._corrector.correct_text(text)
        print text
        print corrected_text


class LanguageCorrector():
    TOKENIZER = 'tokenizers/punkt/spanish.pickle'

    def __init__(self):
        self._tokenize_sentence = nltk.data.load(self.TOKENIZER).tokenize
        self._tokenize_word = word_tokenize

    def correct_text(self, text):
        sentences = self._tokenize_sentence(text)
        corrected_sentences = list()
        for sentence in sentences:
            correct_sentence = self._correct_sentence(sentence)
            corrected_sentences.append(correct_sentence)
        return " ".join(corrected_sentences)

    def _correct_sentence(self, sentence):
        words = self._tokenize_word(sentence)
        corrected_words = list()
        for word in words:
            corrected_word = self._correct_word(word)
            corrected_words.append(corrected_word)
        return " ".join(corrected_words)

    def _correct_word(self, word):
        return word


if __name__ == "__main__":
    formater = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=formatter)
    parser.add_argument("-t", "--text", dest='text',
                        help="Process given text")

    if not len(sys.argv) > 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.text:
            processor = Processor()
            processor.process(args.text)

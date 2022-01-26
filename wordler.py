import re

class Wordler:

    def __init__(self, dictionary_filepath='./english-words/words_alpha.txt', letter_count = 5):
        self._letter_count = letter_count
        viables = set()
        with open(dictionary_filepath, 'r') as f:
            for line in f.readlines():
                word = line.strip()
                if len(word) == self._letter_count:
                    viables.add(word)
        self._viables = viables
        self._debug = False


    def dprint(self, str):
        if self._debug:
            print(str)


    def print_viables(self):
        col_chars = 120
        columns = col_chars // (self._letter_count + 1)
        line = []
        for i, word in enumerate(sorted(self._viables)):
            if i % columns == 0 and i != 0:
                print(' '.join(line))
                line = []
            line.append(word)
        print(' '.join(line))

    
    def _is_word_viable(self, word, guessed_word, result_code):
        green_letters_found = set()
        for i, guessed_letter in enumerate(guessed_word):
            # gray letter - no more in word
            if result_code[i] == '.' and guessed_letter in word and guessed_letter not in green_letters_found:
                self.dprint(f'{word} ruled out - it has a  {guessed_letter}')
                return False                
            # yellow letter - must not be at this index, but must be in word
            elif result_code[i] == 'y':
                if guessed_letter == word[i]:
                    self.dprint(f'{word} ruled out - it has a  {guessed_letter} at index {i}')
                    return False
                elif guessed_letter not in word:
                    self.dprint(f'{word} ruled out - it has no {guessed_letter}')
                    return False
            # green letter - must be at this location
            elif result_code[i] == 'g':
                if guessed_letter != word[i]:
                    self.dprint(f'{word} ruled out - it has no {guessed_letter}')
                    return False
                else:
                    green_letters_found.add(guessed_letter)
        return True

    
    def guess(self, guessed_word, result_code):
        """
        guessed_word is the n-letter word you guessed.
        result-code is n letters where a '.' indicates a gray letter (no match),
        a 'y' indicates yellow (a match somewhere, but not at this position),
        and a 'g' indicates a matched character.
        For example, if the correct word is 'bingo', and the guessed word is 'bogum',
        the result_code should be 'gyy..'
        """
        guessed_word = guessed_word.lower()
        result_code = result_code.lower()
        assert len(guessed_word) == self._letter_count
        assert len(result_code) == self._letter_count
        assert re.match('[\.yg]{5}', result_code)
        to_remove = set()
        for word in self._viables:
            if not self._is_word_viable(word, guessed_word, result_code):
                to_remove.add(word)
        self._viables.difference_update(to_remove)
        self.print_viables()
                
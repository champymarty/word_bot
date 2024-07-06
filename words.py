import random
import os

from constant import WORD_FILE

class WordsRepo:

    def __init__(self) -> None:
        self.words: set[str] = set()
        self._load_words()

    def add_word(self, word: str):
        if word in self.words:
            return
        
        self.words.add(word)
        with open(WORD_FILE, "a") as myfile:
            myfile.write(f"{word}\n")

    def is_in(self, word: str)  -> bool:
        return word in self.words
    
    def remove_word(self, word: str) -> bool:
        if not self.is_in(word):
            return False
        try:
            self.words.remove(word)
            self._remove_word_from_file([word])
            return True
        except KeyError:
            return False

    def consume_word(self, word_count: int):
        words = list(self.words)
        random.shuffle(list(self.words))

        if len(words) <= word_count:
            to_return = words
        else:
            to_return = words[:word_count]
            
        for word in to_return:
            self.words.remove(word)
        self._remove_word_from_file(to_return)
        return to_return
    
    def get_words(self):
        return self.words
    
    def get_word_paginator(self):
        raise NotImplementedError()
    
    def get_length(self) -> int:
        return len(self.words)

    def _load_words(self):
        if not os.path.exists(WORD_FILE):
            with open(WORD_FILE, 'w') as fp:
                return
        with open(WORD_FILE, "r") as file_input:
            for line in file_input:
                self.words.add(line.strip())

    def _write_words(self):
        with open(WORD_FILE, "w") as myfile:
            for word in self.words:
                myfile.write(f"{word}\n")

    def _remove_word_from_file(self, words: list[str]):
        words = set(words)
        with open(WORD_FILE, "r") as file_input:
            with open(WORD_FILE, "w") as output: 
                for line in file_input:
                    if line.strip() not in words:
                        output.write(line)
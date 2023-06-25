
from unidecode import unidecode
import json

class LetterShapeSorter:
    def __init__(self, vectors : dict = json.load(open("data\\vectors_1_d.json", "r"))) -> None:
        self.vectors = vectors
    
    def get_shapes(self, letter : chr, case_sensitive :bool = False)-> list:
        letter = unidecode(letter)
        cases = []
        if not case_sensitive:
            cases.extend([letter.lower(),letter.upper()])
        else:
            cases.append(letter)
        
        matches = set([vector for vector, letters in self.vectors.items() for case in cases if case in letters])
        return list(matches)
    
    def get_letters(self, vector : str)-> list:
        if vector not in self.vectors:
            return []
        return self.vectors[vector]
    
class WordShapeSorter(LetterShapeSorter):
    def __init__(self, vectors : dict = json.load(open("data\\vectors_1_d.json", "r"))) -> None:
        super().__init__(vectors)
        
    def get_shapes(self, word : str)-> list:
        matches = []
        for index, letter in enumerate(word):
            case_sensitive = index != 0
            matches.append(super(WordShapeSorter, self).get_shapes(letter, case_sensitive))

        return matches

if __name__ == "__main__": 
    sorter = WordShapeSorter()
    print(sorter.get_shapes("hello"))
    

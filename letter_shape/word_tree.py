from letter_shape import WordShapeSorter
import json 

class WordTree :
    HIGH = "(1;0)"
    LOW = "(0;1)"
    BOTH = "(1;1)"
    FLAT = "(0;0)"
    
    def __init__(self, sorter = WordShapeSorter()) -> None:
        self.childs = {self.HIGH : None, self.LOW : None, self.BOTH : None, self.FLAT : None}
        self.values = []
        self.sorter = sorter
        
    def _add(self, word, shapes : list) -> None:
        if len(shapes) == 0:
            self.values.append(word)
            return
        
        for shape in shapes[0]:
            if self.childs[shape] is None:
                self.childs[shape] = WordTree(sorter= self.sorter)
            self.childs[shape]._add(word, shapes[1:])
                    
        
    def add(self, word) -> None:
        shapes = self.sorter.get_shapes(word)
        self._add(word, shapes)

            
    def get(self, shapes, index = 0):
        if index == len(shapes) - 1:
            return self.values
        shape = shapes[index]
        if shape not in self.childs:
            return []
        return self.childs[shape].get(shapes, index + 1)

        
    def to_json(self):
        tree = {"values" : self.values}
        for shape, child in self.childs.items():
            if child is not None:
                tree[shape] = child.to_json()
        return tree
        
    def dump(self, file = "data/tree.json"):
        json.dump(self.to_json(), open(file, "w", encoding="UTF-8"), indent=6)
        
    # def from_json(file, ):
    #     data = json.load(open(file, "r", encoding="UTF-8"))
    #     tree = WordTree()
    #     for k, v in data.items():
    #         if k == "values":
    #             tree.values = v
    #         else:
    #             tree.childs[k] = WordTree.from_json(v)

            
tree = WordTree()
words = [ word[:-1] for word in open("data/600_mots.txt", "r", encoding="UTF-8").readlines()]
[tree.add(word) for word in words]

tree.dump()
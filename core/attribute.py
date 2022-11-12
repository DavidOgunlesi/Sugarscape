
class Attribute:
    def __init__(self, attribName:str, minValue:int = None, maxValue:int = None, defaultValue:int = 0):
        self.attribName = attribName
        self.minValue = minValue
        self.maxValue = maxValue
        self.defaultValue = defaultValue

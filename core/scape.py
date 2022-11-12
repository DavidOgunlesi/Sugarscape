from core.imports import *
from core.attribute import Attribute

class Scape():
    def __init__(self, width: int, height: int, scapeAttribute: Attribute): 
        self.width = width
        self.height = height
        self.scapeAttribute = scapeAttribute
        self.intialState = []
        self._scape: List[float] = [scapeAttribute.defaultValue for _ in range(self.width)] * self.height
        self.unsetIndexes = [i for i in range(len(self._scape))]
        self.dfCache = None
        self.updated = True
        self.normaliseOnPlot = False
        self.properties: Dict[str, Any] = {}
        
    def GetProperty(self, property_name: str):
        if property_name in self.properties:
            return self.properties[property_name]
        else:
            return None
        
    def SetProperty(self, property_name: str, value):
        self.properties[property_name] = value
    
    def GetInitial(self, x: int, y: int) -> int:
        idx = x + y * self.width
        
        if idx >= len(self._scape):
            return self.scapeAttribute.defaultValue
        
        return self.intialState[idx]    
        
    def GetValue(self, x: int, y: int) -> int:
        idx = x + y * self.width
        
        if idx >= len(self._scape):
            return self.scapeAttribute.defaultValue
        
        return self._scape[idx]
    
    def SetDefault(self, x: int, y: int):
        idx = x + y * self.width
        
        if idx >= len(self._scape):
            logging.exception(f"Cannot set default at {x}, {y} because it is out of bounds of scape")
            return
        
        self.unsetIndexes.append(idx)
        self._scape[idx] = self.scapeAttribute.defaultValue
        self.updated = True
        
    def SetValue(self, x: int, y: int, value: int):
        
        if not self.IsInBounds(x,y):
            logging.exception(f"Cannot set value {value} at {x}, {y} because it is out of bounds of scape")
        
        if self.scapeAttribute.minValue is not None:
            value = max(value, self.scapeAttribute.minValue)
        
        if self.scapeAttribute.maxValue is not None:
            value = min(value, self.scapeAttribute.maxValue)
        
        idx = x + y * self.width
        
        if idx >= len(self._scape):
            logging.exception(f"Cannot set value {value} at {x}, {y} because it is out of bounds of scape")
            return
        
        if idx in self.unsetIndexes:
            self.unsetIndexes.remove(idx)
            
        self._scape[idx] = value
        self.updated = True
    
    def FillWithRandomValues(self, minValue: int, maxValue: int, discrete: bool = False):
        if discrete:
            self._scape = np.random.randint(minValue, maxValue,  len(self._scape))
        else:
            self._scape = np.random.uniform(minValue, maxValue, (len(self._scape),))

    def FillWithPerlinNoise(self, scale: Tuple[float, float] = None, octaves: int = 1, persistence: float = 0.5, lacunarity: float = 2, seed: int = 1):
        self.Clear()
        if scale == None:
            scale = (self.width, self.height)
        
        noiseMaps = []
        for i in range(octaves):
            noiseMaps.append(PerlinNoise(octaves=i+1, seed=seed))
        
        for i in range(len(self._scape)):
            x, y = self.IndexToCoordinates(i)
            currPers = 1
            currScale = scale
            for noiseMap in noiseMaps:
                val = noiseMap([x / currScale[0], y / currScale[1]]) * currPers  
                val *= (self.scapeAttribute.maxValue - self.scapeAttribute.minValue)
                val += self.scapeAttribute.minValue
                self._scape[i] += min(val, self.scapeAttribute.maxValue)
                currPers *= persistence
                currScale = currScale[0]/lacunarity, currScale[1] / lacunarity
        
    def FindFirstValue(self, value: int) -> int:
        for i, v in enumerate(self._scape):
            if v == value:
                return i
                
        return -1
    
    def SaveInitialState(self):
        self.intialState = copy.deepcopy(self._scape)
    
    def IndexToCoordinates(self, idx: int) -> Tuple[int, int]:
        x = idx % self.width
        y = idx // self.width
        return x, y
    
    def IsInBounds(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.width and y >= 0 and y < self.height
    
    def IsCellDefault(self, x: int, y: int) -> bool:
        return self.GetValue(x, y) == self.scapeAttribute.defaultValue
    
    def Clear(self):
        self._scape = [self.scapeAttribute.defaultValue for _ in range(len(self._scape))]
    
    def PrintScape(self) -> str:
        result = ""
        for i in range(len(self._scape) // self.width):
            sub_list = self._scape[i * self.width:(i + 1) * self.width]
            sub_list_padded = map(lambda s : s.ljust(3), map(str, sub_list))
            result += ('|'.join(sub_list_padded)) + "\n"
        print(result)
        
    def SetRandomUnit(self, value: int, avoidSetValues: bool):
        if avoidSetValues:
            if len(self.unsetIndexes) == 0:
                return
            #np.random.seed(self.seed)
            idx = np.random.choice(self.unsetIndexes)
            self.unsetIndexes.remove(idx)
        else:
            idx = np.random.randint(0, len(self._scape))
            
        self._scape[idx] = value
    
    def NormaliseOnPlot(self, value: bool):        
        self.normaliseOnPlot = value
    
    def Normalise(self, normaliseToRange:bool):
        min = np.min(self._scape)
        max = np.max(self._scape)
        lst = np.array(self._scape)
        lst: np.ndarray = (lst - min) / (max - min)
        self._scape = lst.tolist()
        
        if normaliseToRange:
            arr = np.array(self._scape)
            arr *= (self.scapeAttribute.maxValue - self.scapeAttribute.minValue)
            arr += self.scapeAttribute.minValue
            self._scape = arr.tolist()
     
    def DefaultValuesByCutOff(self, cutOff: float, reverse: bool = False):
        for i in range(len(self._scape)):
            #print(self._scape[i])
            if self._scape[i] >= cutOff and not reverse:
                continue
            elif self._scape[i] < cutOff and reverse:
                continue
            #print("setting default")
            self._scape[i] = self.scapeAttribute.defaultValue
            self.unsetIndexes.append(i)
        
    def Sum(self):
        return np.sum(np.array(self._scape))
        
    def FilledValueCount(self, fromNormalised:bool = False):
        if fromNormalised:
            defaultValue = 0
        else:
            defaultValue = self.scapeAttribute.defaultValue
            
        return len(self._scape) - self._scape.count(defaultValue)    
        
    def Plot(self, width, height):
        if self.updated:
            data = np.array(self._scape)
            
            if self.normaliseOnPlot:
                deft = self.scapeAttribute.defaultValue
                data[data > deft] = self.scapeAttribute.defaultValue+1
                data[data < deft] = self.scapeAttribute.defaultValue+1
                
            scapeData = data.reshape(height, width)
                
            X = np.arange(0, self.width, 1, dtype=int)
            Y = np.arange(0, self.height, 1)

            self.dfCache = pd.DataFrame(data=scapeData, columns=X, index=Y)
            self.updated = False
            
        #plot = sns.heatmap(self.dfCache, annot=False, fmt="d", linewidths=.5, ax=plt.gca(), cmap="crest")
        sns.heatmap(self.dfCache, annot=False, yticklabels=[], xticklabels=[])

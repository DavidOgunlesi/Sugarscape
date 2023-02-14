from __future__ import annotations
from typing import List


def CulturalSimilarityFunction(culturalTag: List[int]):
    # count the number of 1's in the tag
    one_count = culturalTag.count(1)
    if one_count > len(culturalTag) / 2:
        return "red"
    
    return "blue"
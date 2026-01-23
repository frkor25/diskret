# set_operations

def power_set(a: set) -> list[any]:
    """Returns a list of all subsets of a set
    sorted by size of set.
    """
    result = []
    _power_set(result, a)
    result = [None] + sorted(result, key=len)
    return result

def _power_set(result: list, a: set) -> None:
    """A backtracking algorithm to find
    every possible subset of a set and add
    it to result.
    """
    for element in a:
        _power_set(result, a - {element})
    if len(a) > 0 and a not in result:
        result.append(a)
        
    
def cartesian_product(a: set, b: set) -> list[tuple[any]]:
    """Returns every pairing of one element
    from a and one element from b.
    A × B = {(a,b) | a ∈ A og b ∈ B}    
    """
    product = []
    for element_a in a:
        for element_b in b:
            product.append((element_a,element_b))
    return product

def intersection(a: set, b: set) -> set:
    """Returns A ∩ B"""
    return a & b

def union(a: set, b: set) -> set:
    """Returns A ∪ B"""
    return a | b

def difference(a: set, b: set) -> set:
    """Returns A - B (\)"""
    return a - b

def complement(a: set, universal: set) -> set:
    """Returns Ā (A complement in universal set)"""
    return universal - a

def is_subset(a: set, b: set) -> bool:
    """Returns True if A ⊆ B (A is a subset of B)"""
    return a <= b

def is_proper_subset(a: set, b: set) -> bool:
    """Returns True if A ⊂ B (A is a proper subset of B)"""
    return a < b

def verify_distributive_law(a: set, b: set, c: set) -> bool:
    """Verifies the distributive law: A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)"""
    left = a & (b | c)
    right = (a & b) | (a & c)
    return left == right

def verify_complement_law(a: set, universal: set) -> bool:
    """Verifies the complement law: A ∩ Ā = ∅"""
    return (a & (universal - a)) == set()
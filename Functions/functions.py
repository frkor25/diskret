# functions
# dette skal køres som et script for at teste funktionsegenskaber

# definer en funktion i <def f(x)> og kør programmet

def f(x):
    """definer en funktion f her"""
    return x**2 -1

# Standardindstillinger for tests
DOMAIN_START = 1
DOMAIN_END = 100
CODOMAIN_END = 10000

# Test injektivitet
def is_injective(f, domain_start=DOMAIN_START, domain_end=DOMAIN_END):
    """Check if f is injective on domain"""
    if domain_start >= domain_end:
        raise ValueError(f"domain_start ({domain_start}) må være mindre end domain_end ({domain_end})")
    
    outputs = {}
    for x in range(domain_start, domain_end):
        y = f(x)
        if y in outputs:
            return False  # To forskellige x'er giver samme y
        outputs[y] = x
    return True

# Test surjektivitet
def is_surjective(f, domain_start=DOMAIN_START, domain_end=DOMAIN_END, codomain_end=CODOMAIN_END):
    """Check if f is surjective"""
    if domain_start >= domain_end:
        raise ValueError(f"domain_start ({domain_start}) må være mindre end domain_end ({domain_end})")
    if codomain_end <= 0:
        raise ValueError(f"codomain_end ({codomain_end}) må være større end 0")
    
    outputs = set()
    for x in range(domain_start, domain_end):
        outputs.add(f(x))
    
    # Check om alle tal fra codomain bliver ramt
    for y in range(1, codomain_end):
        if y not in outputs:
            return False
    return True

# Test biektivitet
def is_bijective(f, domain_start=DOMAIN_START, domain_end=DOMAIN_END, codomain_end=CODOMAIN_END):
    """Check if f is bijective (both injective and surjective)"""
    return is_injective(f, domain_start, domain_end) and is_surjective(f, domain_start, domain_end, codomain_end)

# Find billedmængden (image)
def image(f, domain_start=DOMAIN_START, domain_end=DOMAIN_END):
    """Find the actual image (output set) of f"""
    return set(f(x) for x in range(domain_start, domain_end))

# Test surjektivitet på specifik codomain
def is_surjective_onto(f, domain_start=DOMAIN_START, domain_end=DOMAIN_END, codomain_values=None):
    """Check if f maps onto exactly the codomain_values"""
    if codomain_values is None:
        raise ValueError("codomain_values må være specificeret")
    outputs = image(f, domain_start, domain_end)
    return outputs == set(codomain_values)

# Find fikspunkter
def fixed_points(f, domain_start=DOMAIN_START, domain_end=DOMAIN_END):
    """Find all x where f(x) = x"""
    return [x for x in range(domain_start, domain_end) if f(x) == x]

# Test periodisitet
def is_periodic(f, period, domain_start=DOMAIN_START, domain_end=DOMAIN_END):
    """Check if f(x + period) = f(x)"""
    if period <= 0:
        raise ValueError(f"period ({period}) må være større end 0")
    if domain_start + period >= domain_end:
        raise ValueError(f"domain_end må være mindst domain_start + period")
    
    for x in range(domain_start, domain_end - period):
        if f(x) != f(x + period):
            return False
    return True

# Find invers relation
def inverse_relation(f, domain_start=DOMAIN_START, domain_end=DOMAIN_END):
    """Find the inverse relation as a dictionary {y: x}"""
    inverse = {}
    for x in range(domain_start, domain_end):
        y = f(x)
        if y in inverse:
            # Ikke injektiv - flere x'er giver samme y
            if inverse[y] != x:
                inverse[y] = None  # Markér som ikke-unik
        else:
            inverse[y] = x
    return inverse

# Test funktionskomposition
def compose(f, g):
    """Returns f(g(x))"""
    return lambda x: f(g(x))

fog = compose(f, f)
print(f"f(f(1)) = {fog(1)}")  # (1² + 1)² + 1 = 2² + 1 = 5
print(f"1⁴ + 2 = {1**4 + 2}")  # 3 (IKKE 5, så x⁴ + 2 er FALSKT)



# Test monotonitet (strengt voksende)
def is_strictly_increasing(f, domain_start=DOMAIN_START, domain_end=DOMAIN_END):
    """Check if f is strictly increasing"""
    if domain_start >= domain_end:
        raise ValueError(f"domain_start ({domain_start}) må være mindre end domain_end ({domain_end})")
    
    prev = f(domain_start)
    for x in range(domain_start + 1, domain_end):
        curr = f(x)
        if curr <= prev:
            return False
        prev = curr
    return True

# Test monotonitet (strengt aftagende)
def is_strictly_decreasing(f, domain_start=DOMAIN_START, domain_end=DOMAIN_END):
    """Check if f is strictly decreasing"""
    if domain_start >= domain_end:
        raise ValueError(f"domain_start ({domain_start}) må være mindre end domain_end ({domain_end})")
    
    prev = f(domain_start)
    for x in range(domain_start + 1, domain_end):
        curr = f(x)
        if curr >= prev:
            return False
        prev = curr
    return True

# Kør tests
print(f"f er injektiv: {is_injective(f)}")  # True
print(f"f er surjektiv: {is_surjective(f)}")  # False
print(f"f er bijektiv: {is_bijective(f)}")  # False (da ikke surjektiv)
print(f"f er strengt voksende: {is_strictly_increasing(f)}")  # True
print(f"f er strengt aftagende: {is_strictly_decreasing(f)}")  # False
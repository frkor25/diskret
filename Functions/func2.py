# functions
# dette skal køres som et script for at teste funktionsegenskaber

# definer en funktion i <def f(x)> og kør programmet

def f(x):
    """definer en funktion f her"""
<<<<<<< HEAD
    return x ** 3 + 1

def g(x):
    """definer en anden funktion g her"""
    return x ** 2 - (2 * x) - 1

# Standardindstillinger for tests
DOMAIN_START = 1
=======
    return (x + 1)**2 -1

def g(x):
    """definer en anden funktion g her"""
    return x * 2

# Standardindstillinger for tests
DOMAIN_START = 0
>>>>>>> b1d1da2f9ae83b185af05f7c323264b230f98b6b
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

    return True

# Test funktionskomposition
def compose(f, g):
    """Returns f(g(x))"""
    return lambda x: f(g(x))

# Find invers relation
def inverse_function_samples(f, domain_start=DOMAIN_START, domain_end=DOMAIN_END):
    """Find sample inverse pairs {y: x}"""
    inverse = {}
    for x in range(domain_start, domain_end):
        y = f(x)
        if y in inverse:
            if inverse[y] != x:
                inverse[y] = None  # Markér som ikke-unik hvis f ikke er injektiv
        else:
            inverse[y] = x
    # Returner kun første 10 par
    return dict(list(inverse.items())[:10])

# print results
print("=" * 50)
print("EGENSKABER FOR F(X):")
print("=" * 50)
print(f"f er injektiv: {is_injective(f)}") 
print(f"f er surjektiv: {is_surjective(f)}") 
print(f"f er bijektiv: {is_bijective(f)}")  
print(f"f er invertibel: {is_bijective(f)}")  # Invertibel = Bijektiv
print(f"f er strengt voksende: {is_strictly_increasing(f)}") 
print(f"f er strengt aftagende: {is_strictly_decreasing(f)}")  

print("\n" + "=" * 50)
print("EGENSKABER FOR G(X):")
print("=" * 50)
print(f"g er injektiv: {is_injective(g)}") 
print(f"g er surjektiv: {is_surjective(g)}") 
print(f"g er bijektiv: {is_bijective(g)}")  
print(f"g er invertibel: {is_bijective(g)}")  # Invertibel = Bijektiv
print(f"g er strengt voksende: {is_strictly_increasing(g)}") 
print(f"g er strengt aftagende: {is_strictly_decreasing(g)}")  

print("\n" + "=" * 50)
print("KOMPOSITIONER:")
print("=" * 50)
# f(f(x)) - f komponeret med sig selv
ff = compose(f, f)
print(f"f(f(1)) = {ff(1)}")
print(f"f(f(2)) = {ff(2)}")
print(f"f(f(3)) = {ff(3)}")

# g(f(x)) - g komponeret med f
gf = compose(g, f)
print(f"\ng(f(1)) = {gf(1)}")
print(f"g(f(2)) = {gf(2)}")
print(f"g(f(3)) = {gf(3)}")

# f(g(x)) - f komponeret med g
fg = compose(f, g)
print(f"\nf(g(1)) = {fg(1)}")
print(f"f(g(2)) = {fg(2)}")
print(f"f(g(3)) = {fg(3)}")

# g(g(x)) - g komponeret med sig selv
gg = compose(g, g)
print(f"\ng(g(1)) = {gg(1)}")
print(f"g(g(2)) = {gg(2)}")
print(f"g(g(3)) = {gg(3)}")

print("\n" + "=" * 50)
print("INVERSE FUNKTIONER (SAMPLES):")
print("=" * 50)

# f inverse
f_inv_dict = inverse_function_samples(f)
print("f⁻¹:")
for y, x in list(f_inv_dict.items())[:5]:
    if x is not None:
        print(f"f⁻¹({y}) = {x}")

# g inverse
print("\ng⁻¹:")
g_inv_dict = inverse_function_samples(g)
for y, x in list(g_inv_dict.items())[:5]:
    if x is not None:
        print(f"g⁻¹({y}) = {x}")  
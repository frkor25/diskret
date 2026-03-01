###############################################################
#   NUMBER THEORY TOOLKIT – CLEAN & SIMPLE
###############################################################

from math import gcd

# ===== 1. Hjælpefunktioner (Logik & Tal) =====

def implies(p, q): return (not p) or q
def iff(p, q): return p == q

def lcm(a, b):
    if a == 0 or b == 0: return 0
    return abs(a * b) // gcd(a, b)

class Z(int):
    """Tillader syntax: a | b"""
    def __or__(self, other): return self != 0 and other % self == 0
    def __ror__(self, other): return other != 0 and self % other == 0

def mod(a,b,n):
    # """Tillader syntax: mod(n)(a, b)"""
    # def cong(a, b): return (a - b) % n == 0
    # return cong
    if (a - b) % n == 0:
        return True
    else:
        return False

# ===== 2. Test-motoren (Kører loops) =====
# For at teste Z+ U {0} skal "-limit" sættes til 0

def for_all_abc(prop, limit=12):
    for a in range(limit, limit + 1):
        for b in range(limit, limit + 1):
            for c in range(limit, limit + 1):
                if not prop(a, b, c):
                    return False, (a, b, c)
    return True, None

def run_test(statement_func, limit=12):
    """
    Kører testen og printer resultatet pænt.
    """
    navn = statement_func.__name__
    print(f"--- Tester: '{navn}' i området [-{limit}, {limit}] ---")
    
    ok, counter = for_all_abc(statement_func, limit)

    if ok:
        print(f"✓ '{navn}' er SANDT (ingen modeksempler fundet).\n")
    else:
        a, b, c = counter
        print(f"✗ '{navn}' er FALSK.")
        print(f"  Modeksempel: a={a}, b={b}, c={c}\n")

###############################################################
#   3. DIT UDSAGN træk det her ud og lav i en separat celle nede under 
# opgaven skrives efter return 
###############################################################

def Udsagn(a, b, c):
    # Setup: Wrapper tallene
    a, b, c = Z(a), Z(b), Z(c)
    
    # Skriv din matematik her:
    # a | b – "a deler b"
    # implies(p, q)
    # iff(p,q)


    # For at teste Z+ U {0} skal "-limit" sættes til 0 ^^^
    # + tilføj "c == 0 or ..." i return
    # fx:
    # a≡b(mod n) ⇒ 2a≡2b(mod n)
    # return c == 0 or implies(mod(a, b, c), mod(2*a, 2*b, c))

    # For at udelukke fx. a=0 og/eller b=0 fra testen:
    # Tilføj "a == 0 or b == 0 or ..." i return
    # fx:
    # a|b ∧ b|c ⇒ a|c (kun for a,b ≠ 0)
    # return a == 0 or b == 0 or implies(a | b and b | c, a | c)

    #implies(mod(a, b, 10), (a - b) == 10 or (b - a) == 10 )
    
    
   # skirv udsagn her: 
    return implies(mod(a,4,10) and mod(b,3,5),mod(a+b,7,15))

run_test(Udsagn)

###############################################################
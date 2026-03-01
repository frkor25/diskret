import sympy as sp
import itertools

# Vi definerer x globalt
x = sp.Symbol("x", real=True)

# ===========================================================
#  HJÆLPE-FUNKTION (Bruges KUN til visning af invers)
# ===========================================================
def pæn_tekst(expr):
    """Laver kun 'makeup' på den inverse formel"""
    s = str(sp.expand(expr)) 
    s = s.replace("*2", "²").replace("**3", "³").replace("*", "^") 
    s = s.replace("*", "") 
    s = s.replace("sqrt", "√")
    return s

# ===========================================================
#  LOGIK-MOTOR
# ===========================================================

def get_test_config(domain):
    # HELTAL (Z)
    if domain == "Z_pos_med_0":   return range(0, 50)
    if domain == "Z_pos_uden_0":  return range(1, 50)
    if domain == "Z_neg_med_0":   return range(-50, 1)
    if domain == "Z_neg_uden_0":  return range(-50, 0)
    if domain == "Z_hele":        return range(-25, 26)
    
    # REELLE TAL (R)
    if domain == "R_pos_med_0":   return [0, 0.1, 0.5, 1, 2, 5, 10, 20]
    if domain == "R_pos_uden_0":  return [0.1, 0.5, 1, 2, 5, 10, 20]
    if domain == "R_neg_med_0":   return [-20, -10, -5, -2, -1, -0.1, 0]
    if domain == "R_neg_uden_0":  return [-20, -10, -5, -2, -1, -0.1]
    if domain == "R_hele":        return [-10, -5, -1, 0, 1, 5, 10]
    
    # Standard fallback
    return range(-10, 11)

def eval_val(expr, n, domain):
    try:
        val = expr.subs(x, n)
        if "Z" in domain: return int(val)
        else: return float(val.evalf())
    except: return None

def check_injective(expr, domain):
    test_points = get_test_config(domain)
    seen_values = {}
    
    for val_x in test_points:
        val_y = eval_val(expr, val_x, domain)
        if val_y is None: continue
        
        check_val = val_y if "Z" in domain else round(val_y, 5)
        
        if check_val in seen_values:
            return False 
        seen_values[check_val] = val_x
    return True

def check_surjective(expr, domain):
    if "Z" in domain:
        outputs = set()
        
        if "pos" in domain:     scan = range(0, 201)
        elif "neg" in domain:   scan = range(-201, 1)
        else:                   scan = range(-100, 101)

        for n in scan:
            if "uden_0" in domain and n == 0: continue
            try: outputs.add(eval_val(expr, n, domain))
            except: pass
        
        targets = []
        if "pos" in domain:
            targets = list(range(1, 11))
            if "med_0" in domain: targets.insert(0, 0)
            
        elif "neg" in domain:
            targets = list(range(-10, 0))
            if "med_0" in domain: targets.append(0)
            
        else: 
            targets = list(range(-5, 6))
        
        return all(t in outputs for t in targets)

    else:
        low  = -2000 if "neg" in domain or "hele" in domain else (0.001 if "uden_0" in domain else 0)
        high = 2000  if "pos" in domain or "hele" in domain else (-0.001 if "uden_0" in domain else 0)
        
        y1 = eval_val(expr, low, domain)
        y2 = eval_val(expr, high, domain)
        
        if y1 is None or y2 is None: return False
        
        diff = abs(y1 - y2)
        return diff > 1000 

def check_monotonic(expr, domain):
    points = get_test_config(domain)
    valid_points = sorted([p for p in points if eval_val(expr, p, domain) is not None])
    vals = [eval_val(expr, p, domain) for p in valid_points]
    
    if len(vals) < 2: return "Ukendt"
    if all(vals[i] < vals[i+1] for i in range(len(vals)-1)): return "Strengt voksende"
    if all(vals[i] > vals[i+1] for i in range(len(vals)-1)): return "Strengt aftagende"
    return "Ikke monoton"

def get_inverse_candidate(expr):
    y = sp.Symbol('y', real=True)
    try:
        sol = sp.solve(sp.Eq(y, expr), x)
        if not sol: return None
        return [pæn_tekst(s.subs(y, x)) for s in sol]
    except: return None

def run_analysis(func_dict, domain="R_hele"):
    names = list(func_dict.keys())
    
    print("\n" + "="*60)
    print(f" ANALYSE I DOMÆNE: {domain}")
    print("="*60)

    # 1. EGENSKABER
    print("\n--- 1. EGENSKABER ---")
    for name, expr in func_dict.items():
        inj = check_injective(expr, domain)
        sur = check_surjective(expr, domain)
        mon = check_monotonic(expr, domain)
        
        bij = (inj and sur)
        inv_list = get_inverse_candidate(expr)
        
        # Original format (Rå Python kode)
        print(f"Funktion {name}(x) = {sp.expand(expr)}")
        print(f"  • Injektiv (1-til-1):   {inj}")
        print(f"  • Surjektiv (På):       {sur}")
        print(f"  • Bijektiv:             {bij}")
        print(f"  • Monotoni:             {mon}")
        
        # Vis kun invers hvis den findes og er gyldig (Bijektiv)
        if bij and inv_list:
             print(f"  • Invers forskrift:     {' eller '.join(inv_list)}")
        elif not bij:
             problem = []
             if not inj: problem.append("ikke injektiv")
             if not sur: problem.append("ikke surjektiv")
             reason = " og ".join(problem)
             print(f"  • Invers forskrift:     Ingen ({reason} i {domain})")
        else:
             print(f"  • Invers forskrift:     Kunne ikke beregnes")
             
        print("-" * 30)

    # 2. SAMMENSÆTNINGER
    print("\n--- 2. SAMMENSÆTNINGER ---")
    for name1 in names:
        for name2 in names:
            res = func_dict[name1].subs(x, func_dict[name2])
            print(f"({name1} ∘ {name2})(x) = {sp.expand(res)}")

    # 3. KRYDSTJEK
    print("\n--- 3. TJEK: (f ∘ g) vs (g ∘ f) ---")
    for name1, name2 in itertools.combinations(names, 2):
        res1 = sp.expand(func_dict[name1].subs(x, func_dict[name2]))
        res2 = sp.expand(func_dict[name2].subs(x, func_dict[name1]))
        match = (res1 == res2)
        print(f"  Er ({name1}∘{name2}) == ({name2}∘{name1})? -> {match}")

    # 4. REGNING
    print("\n--- 4. REGNING (+ og *) ---")
    for name1, name2 in itertools.combinations_with_replacement(names, 2):
        sum_res = sp.expand(func_dict[name1] + func_dict[name2])
        mult_res = sp.expand(func_dict[name1] * func_dict[name2])
        print(f"({name1} + {name2})(x) = {sum_res}")
        print(f"({name1} · {name2})(x) = {mult_res}")

# ===========================================================
#  DIN ARBEJDSPLADS
# ===========================================================

# 1. Definer funktionerne

f = x + 2 #  (x+1)² - 1
g = x**2                #  2x
#h = x**2 - 1 # Eksempel på tredje funktion (kommentar for nu)

# 2. Saml dem
mine_funktioner = {
    "f": f,
    "g": g,  #  husk komma efter hver funktioon hvis flere funktioner tilføjes
#    "h": h # Eksempel på tredje funktion (kommentar for nu)
}



# 3. Kør analysen        #skift  domain under her
run_analysis(mine_funktioner, domain="Z_hele")
   # Domæne muligheder:
# --- HELTAL (Z) ---
    # "Z_pos_med_0"   : 0, 1, 2...       (DIN OPGAVE: Z+ U {0})
    # "Z_pos_uden_0"  : 1, 2, 3...       (Kun positive heltal, Z+)
    # "Z_neg_med_0"   : ... -2, -1, 0    (Negative heltal inkl. 0)
    # "Z_neg_uden_0"  : ... -3, -2, -1   (Kun negative heltal)
    # "Z_hele"        : ... -1, 0, 1 ... (Alle heltal)

    # --- REELLE TAL (R - decimaltal) ---
    # "R_pos_med_0"   : Alle tal >= 0
    # "R_pos_uden_0"  : Alle tal > 0
    # "R_neg_med_0"   : Alle tal <= 0
    # "R_neg_uden_0"  : Alle tal < 0
    # "R_hele"        : Alle tal fra -uendelig til +uendelig
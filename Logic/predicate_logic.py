# predicate_logic.py
# Evaluerer prædikatslogiske udsagn over domæner som ℤ
import re
from itertools import product

# Operator syntax:
# forall / ∀ : universal quantifier
# exists / ∃ : existential quantifier  
# and / ∧
# or / ∨
# not / ¬ / -
# imp / → / ⇒ : implication
# bimp / ↔ / ⇔ : bi-implication
# > , < , >= , <= , == , != : relationer

# =============================================================================
# AVANCERET PRÆDIKATSLOGIK EVALUATOR
# Understøtter nestede kvantorer, flere variable, implikation, biimplikation
# =============================================================================

def normalize_expression(expression: str) -> str:
    """Normaliserer Unicode-symboler til ASCII."""
    replacements = [
        ("∀", "forall "),
        ("∃!", "exists! "),  # Skal komme før ∃
        ("∃", "exists "),
        ("∈", " in "),
        ("ℤ", "Z"),
        ("ℕ", "N"),
        ("ℝ", "R"),
        ("²", "**2"),
        ("³", "**3"),
        ("≥", ">="),
        ("≤", "<="),
        ("≠", "!="),
        ("·", "*"),  # Multiplikation med dot
        ("×", "*"),
        ("÷", "//"),
        ("⇒", " imp "),
        ("⇔", " bimp "),
        ("→", " imp "),
        ("↔", " bimp "),
        ("∧", " and "),
        ("∨", " or "),
        ("¬", "not "),
    ]
    for old, new in replacements:
        expression = expression.replace(old, new)
    
    # Fjern dobbelte mellemrum
    expression = re.sub(r'\s+', ' ', expression).strip()
    return expression


def convert_predicate_to_python(predicate: str) -> str:
    """Konverterer prædikat til gyldig Python."""
    # Konverter enkelt = til == (men ikke <=, >=, !=, ==)
    predicate = re.sub(r'(?<![<>!=])=(?!=)', '==', predicate)
    
    # Konverter 'imp' til Python implikation: (not A) or B
    # A imp B bliver (not (A)) or (B)
    while ' imp ' in predicate:
        # Find imp og split korrekt
        match = re.search(r'\(([^()]+)\)\s+imp\s+\(([^()]+)\)', predicate)
        if match:
            a, b = match.groups()
            predicate = predicate.replace(match.group(0), f'((not ({a})) or ({b}))')
        else:
            # Simpel version uden parenteser
            parts = predicate.split(' imp ', 1)
            if len(parts) == 2:
                predicate = f'((not ({parts[0].strip()})) or ({parts[1].strip()}))'
    
    # Konverter 'bimp' til Python biimplikation: A == B (boolean equality)
    while ' bimp ' in predicate:
        match = re.search(r'\(([^()]+)\)\s+bimp\s+\(([^()]+)\)', predicate)
        if match:
            a, b = match.groups()
            predicate = predicate.replace(match.group(0), f'(({a}) == ({b}))')
        else:
            parts = predicate.split(' bimp ', 1)
            if len(parts) == 2:
                predicate = f'(({parts[0].strip()}) == ({parts[1].strip()}))'
    
    return predicate


def split_top_level_connective(expression: str, connective: str) -> list:
    """
    Splitter udtryk på top-level connective (bimp, imp, and, or).
    Tager højde for nestede udtryk med kolon.
    """
    # Tæl kolon for at finde hvor kvantorer slutter
    # Vi leder efter connective der er på "top level"
    parts = []
    depth = 0
    current = ""
    tokens = expression.split()
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Tjek om vi er på top level og finder connective
        if depth == 0 and token == connective:
            if current.strip():
                parts.append(current.strip())
            current = ""
            i += 1
            continue
        
        # Tæl kvantorer (øger depth)
        if token in ["forall", "exists", "exists!"]:
            depth += 1
        
        # Kolon afslutter en kvantor-binding
        if token.endswith(":"):
            depth = max(0, depth - 1)
        
        current += " " + token
        i += 1
    
    if current.strip():
        parts.append(current.strip())
    
    return parts if len(parts) > 1 else None


def parse_quantified_expression(expression: str) -> dict:
    """
    Parser et prædikatslogisk udtryk med støtte for:
    - Nestede kvantorer: ∃x ∈ ℤ : ∀y ∈ ℤ : ...
    - Flere variable: ∀x, y ∈ ℤ : ...
    - Negation: ¬∀x ∈ ℤ : ...
    - Top-level biimplikation: ¬∀x : P(x) ⇔ ∀x : Q(x)
    """
    expression = normalize_expression(expression)
    
    # Check for top-level biimplikation først
    bimp_parts = split_top_level_connective(expression, "bimp")
    if bimp_parts and len(bimp_parts) == 2:
        left = parse_quantified_expression(bimp_parts[0])
        right = parse_quantified_expression(bimp_parts[1])
        return {
            "type": "biconditional",
            "left": left,
            "right": right
        }
    
    # Check for top-level implikation
    imp_parts = split_top_level_connective(expression, "imp")
    if imp_parts and len(imp_parts) == 2:
        left = parse_quantified_expression(imp_parts[0])
        right = parse_quantified_expression(imp_parts[1])
        return {
            "type": "implication",
            "left": left,
            "right": right
        }
    
    # Check for negation
    negated = False
    if expression.startswith("not "):
        negated = True
        expression = expression[4:].strip()
    
    # Find quantifier
    quantifier = None
    rest = expression
    
    if expression.startswith("forall "):
        quantifier = "forall"
        rest = expression[7:].strip()
    elif expression.startswith("exists! "):
        quantifier = "exists!"
        rest = expression[8:].strip()
    elif expression.startswith("exists "):
        quantifier = "exists"
        rest = expression[7:].strip()
    else:
        # Ingen kvantor - det er bare et prædikat
        return {"type": "predicate", "expression": expression}
    
    # Find variable(r) og domæne
    if " in " not in rest:
        return {"error": "Mangler 'in' mellem variabel og domæne"}
    
    var_part, domain_and_rest = rest.split(" in ", 1)
    
    # Parse variable (kan være "x" eller "x, y" eller "x,y")
    variables = [v.strip() for v in var_part.split(",")]
    
    # Find domæne og resten
    if ":" not in domain_and_rest:
        return {"error": "Mangler ':' efter domæne"}
    
    domain_str, rest_expr = domain_and_rest.split(":", 1)
    domain_str = domain_str.strip().upper()
    rest_expr = rest_expr.strip()
    
    # Check om resten indeholder en nested kvantor
    rest_normalized = normalize_expression(rest_expr)
    if rest_normalized.startswith(("forall ", "exists ", "exists! ", "not forall ", "not exists ")):
        body = parse_quantified_expression(rest_expr)
    else:
        # Det er prædikatet
        body = {
            "type": "predicate",
            "expression": convert_predicate_to_python(rest_normalized)
        }
    
    return {
        "type": "quantifier",
        "quantifier": quantifier,
        "negated": negated,
        "variables": variables,
        "domain": domain_str,
        "body": body
    }


def get_domain_range(domain_str: str, default_range: range) -> range:
    """Returnerer range baseret på domæne-streng."""
    domain_str = domain_str.upper()
    if domain_str in ["Z", "INT", "INTEGER", "INTEGERS"]:
        return default_range
    elif domain_str in ["N", "NAT", "NATURAL"]:
        return range(max(0, default_range.start), default_range.stop)
    elif domain_str in ["N+", "POSITIVE"]:
        return range(max(1, default_range.start), default_range.stop)
    else:
        return default_range


def evaluate_quantified(parsed: dict, domain_range: range, bindings: dict) -> dict:
    """
    Evaluerer et parset kvantificeret udtryk rekursivt.
    """
    if "error" in parsed:
        return parsed
    
    # Håndter biconditional (A ⇔ B)
    if parsed["type"] == "biconditional":
        left_result = evaluate_quantified(parsed["left"], domain_range, bindings)
        right_result = evaluate_quantified(parsed["right"], domain_range, bindings)
        
        if "error" in left_result:
            return left_result
        if "error" in right_result:
            return right_result
        
        left_val = left_result["result"]
        right_val = right_result["result"]
        result = left_val == right_val
        
        return {
            "result": result,
            "explanation": f"({left_val}) ⇔ ({right_val}) = {result}",
            "left_result": left_result,
            "right_result": right_result
        }
    
    # Håndter implication (A ⇒ B)
    if parsed["type"] == "implication":
        left_result = evaluate_quantified(parsed["left"], domain_range, bindings)
        right_result = evaluate_quantified(parsed["right"], domain_range, bindings)
        
        if "error" in left_result:
            return left_result
        if "error" in right_result:
            return right_result
        
        left_val = left_result["result"]
        right_val = right_result["result"]
        result = (not left_val) or right_val
        
        return {
            "result": result,
            "explanation": f"({left_val}) ⇒ ({right_val}) = {result}",
            "left_result": left_result,
            "right_result": right_result
        }
    
    if parsed["type"] == "predicate":
        # Evaluer prædikatet med current bindings
        expr = parsed["expression"]
        try:
            result = eval(expr, {"__builtins__": {}}, bindings)
            return {"result": bool(result)}
        except Exception as e:
            return {"error": f"Evalueringsfejl: {e}, udtryk: {expr}, bindings: {bindings}"}
    
    # Det er en kvantor
    quantifier = parsed["quantifier"]
    negated = parsed.get("negated", False)
    variables = parsed["variables"]
    domain = get_domain_range(parsed["domain"], domain_range)
    body = parsed["body"]
    
    # Generer alle kombinationer af variable værdier
    if len(variables) == 1:
        value_combinations = [(v,) for v in domain]
    else:
        value_combinations = list(product(domain, repeat=len(variables)))
    
    if quantifier == "forall":
        # For alle: tjek at body er sand for alle kombinationer
        for values in value_combinations:
            new_bindings = bindings.copy()
            for var, val in zip(variables, values):
                new_bindings[var] = val
            
            sub_result = evaluate_quantified(body, domain_range, new_bindings)
            
            if "error" in sub_result:
                return sub_result
            
            if not sub_result["result"]:
                # Fundet modeksempel
                counterex = {var: val for var, val in zip(variables, values)}
                result = {
                    "result": False,
                    "counterexample": counterex,
                    "explanation": f"Modeksempel: {counterex}"
                }
                # Hvis negeret, flip resultatet
                if negated:
                    result["result"] = True
                    result["explanation"] = f"¬∀ er sand pga. modeksempel: {counterex}"
                return result
        
        # Alle opfyldte
        result = {
            "result": True,
            "explanation": f"Sandt for alle {variables} i domænet"
        }
        if negated:
            result["result"] = False
            result["explanation"] = f"¬∀ er falsk fordi ∀ er sand"
        return result
    
    elif quantifier == "exists":
        # Der findes: tjek om body er sand for mindst én kombination
        examples = []
        for values in value_combinations:
            new_bindings = bindings.copy()
            for var, val in zip(variables, values):
                new_bindings[var] = val
            
            sub_result = evaluate_quantified(body, domain_range, new_bindings)
            
            if "error" in sub_result:
                return sub_result
            
            if sub_result["result"]:
                example = {var: val for var, val in zip(variables, values)}
                examples.append(example)
                if len(examples) >= 3:
                    break
        
        if examples:
            result = {
                "result": True,
                "examples": examples,
                "explanation": f"Eksempler: {examples}"
            }
            if negated:
                result["result"] = False
                result["explanation"] = f"¬∃ er falsk fordi der findes eksempler: {examples}"
            return result
        else:
            result = {
                "result": False,
                "explanation": f"Ingen {variables} opfylder betingelsen"
            }
            if negated:
                result["result"] = True
                result["explanation"] = f"¬∃ er sand fordi ingen opfylder betingelsen"
            return result
    
    elif quantifier == "exists!":
        # Unik eksistens: præcis én
        examples = []
        for values in value_combinations:
            new_bindings = bindings.copy()
            for var, val in zip(variables, values):
                new_bindings[var] = val
            
            sub_result = evaluate_quantified(body, domain_range, new_bindings)
            
            if "error" in sub_result:
                return sub_result
            
            if sub_result["result"]:
                example = {var: val for var, val in zip(variables, values)}
                examples.append(example)
                if len(examples) > 1:
                    break
        
        if len(examples) == 1:
            return {
                "result": not negated,
                "examples": examples,
                "explanation": f"Præcis ét element opfylder: {examples[0]}"
            }
        elif len(examples) == 0:
            return {
                "result": negated,
                "explanation": "Ingen elementer opfylder betingelsen"
            }
        else:
            return {
                "result": negated,
                "examples": examples,
                "explanation": f"Mere end ét element opfylder: {examples}"
            }
    
    return {"error": f"Ukendt kvantor: {quantifier}"}


def evaluate_advanced(expression: str, domain_range=None) -> dict:
    """
    Evaluerer et avanceret prædikatslogisk udtryk.
    
    Understøtter:
    - ∃x ∈ ℤ : x = 5
    - ∀x, y ∈ ℤ : x² + y² > 0
    - ∃x ∈ ℤ : ∀y ∈ ℤ : x + y > 100
    - ∀x ∈ ℤ : (x² < 0 ⇒ x³ = 14)
    - ¬∀x ∈ ℤ : x² < 4
    """
    if domain_range is None:
        domain_range = range(-20, 21)  # Mindre range for nested (performance)
    
    parsed = parse_quantified_expression(expression)
    
    if "error" in parsed:
        return parsed
    
    return evaluate_quantified(parsed, domain_range, {})


def test_examples():
    """Test de specifikke eksempler fra opgaven."""
    print("\n" + "=" * 70)
    print("TEST AF PRÆDIKATSLOGISKE UDSAGN")
    print("=" * 70)
    
    examples = [
        ("∃x ∈ ℤ : x = 5", True, "5 er et heltal"),
        ("∃x ∈ ℤ : x² < 0", False, "x² er aldrig negativ"),
        ("∀x ∈ ℤ : (x² < 0 ⇒ x³ = 14)", True, "Vacuously true - antecedent er altid falsk"),
        ("∀x, y ∈ ℤ : x² + y² > 0", False, "Modeksempel: x=0, y=0"),
        ("∃x ∈ ℤ : ∀y ∈ ℤ : x + y > 100", False, "For ethvert x findes y der gør x+y ≤ 100"),
        ("∀x ∈ ℤ : ∃y ∈ ℤ : (x + y) * z = 0", None, "Kræver z=0 eller y=-x"),
    ]
    
    for expr, expected, note in examples:
        print(f"\n{'─' * 70}")
        print(f"Udtryk: {expr}")
        print(f"Forventet: {expected} ({note})")
        
        result = evaluate_advanced(expr, range(-10, 11))
        
        print(f"Resultat: {result.get('result', 'FEJL')}")
        if "explanation" in result:
            print(f"Forklaring: {result['explanation']}")
        if "counterexample" in result:
            print(f"Modeksempel: {result['counterexample']}")
        if "examples" in result:
            print(f"Eksempler: {result['examples']}")
        if "error" in result:
            print(f"Fejl: {result['error']}")


def evaluate_predicate(expression: str, domain_range=None) -> dict:
    """
    Evaluerer et prædikatslogisk udsagn.
    
    Args:
        expression: Udsagnet som string, f.eks. "forall n in Z: n >= 2"
        domain_range: Range for domænet at teste, f.eks. range(-100, 100)
    
    Returns:
        Dictionary med result (True/False/Unknown) og counterexamples hvis relevant
    """
    if domain_range is None:
        domain_range = range(-100, 101)  # Default: test -100 til 100
    
    parsed = parse_expression(expression)
    result = evaluate_parsed(parsed, domain_range, {})
    
    return result


def parse_expression(expression: str) -> dict:
    """Parser udtrykket til en struktur vi kan evaluere"""
    # Normaliser input
    expression = expression.replace("∀", "forall")
    expression = expression.replace("∃", "exists")
    expression = expression.replace("∈", "in")
    expression = expression.replace("ℤ", "z")
    expression = expression.replace("∧", "and")
    expression = expression.replace("∨", "or")
    expression = expression.replace("¬", "not")
    expression = expression.replace("→", "imp")
    expression = expression.replace("↔", "bimp")
    expression = expression.replace("⇒", "imp")
    expression = expression.replace("⇔", "bimp")
    
    # TODO: Implementér parser
    # Dette er komplekst og ville kræve en ordentlig parser
    return {"type": "parsed", "expression": expression}


def evaluate_parsed(parsed: dict, domain_range, variable_bindings: dict) -> dict:
    """Evaluerer et parset udtryk"""
    # TODO: Implementér evaluering baseret på udtrykstype
    # - Håndter forall: tjek at prædikatet holder for alle værdier
    # - Håndter exists: tjek om prædikatet holder for mindst én værdi
    # - Håndter relationer: evaluer med givne variable bindings
    pass


def evaluate_simple_statements():
    """Eksempler på simple udsagn fra billedet"""
    
    statements = [
        ("∃n ∈ ℤ: n > 2", True, "n=3 er et eksempel"),
        ("∃!n ∈ ℤ: n = 2", True, "Præcis n=2 opfylder dette"),
        ("∀n ∈ ℤ: n ≥ 2", False, "Modeksempel: n=0"),
        ("∀n ∈ ℤ: n² > n", False, "Modeksempel: n=0 giver 0² = 0 ≯ 0"),
        ("∃n ∈ ℤ: n + n ≠ 2n", False, "n + n = 2n for alle heltal"),
    ]
    
    print("\nEvaluering af udsagn:")
    print("-" * 60)
    
    for stmt, expected, explanation in statements:
        print(f"\n{stmt}")
        print(f"Forventet: {expected}")
        print(f"Forklaring: {explanation}")


# Simpel version der kan håndtere nogle cases
def check_simple_predicate(statement_type: str, variable: str, domain, predicate_fn) -> dict:
    """
    Simpel evaluering for basic cases.
    
    Args:
        statement_type: "forall" eller "exists"
        variable: variabel navn, f.eks. "n"
        domain: iterable at teste over
        predicate_fn: funktion der tager værdi og returnerer bool
    """
    if statement_type == "forall":
        for value in domain:
            if not predicate_fn(value):
                return {
                    "result": False,
                    "counterexample": {variable: value}
                }
        return {"result": True}
    
    elif statement_type == "exists":
        examples = []
        for value in domain:
            if predicate_fn(value):
                examples.append(value)
        
        if examples:
            return {
                "result": True,
                "examples": examples[:5]  # Vis op til 5 eksempler
            }
        return {"result": False}


def parse_simple_expression(expression: str) -> dict:
    """
    Parser et simpelt prædikatslogisk udtryk.
    
    Understøtter formater som:
        forall n in Z: n**2 >= 0
        exists n in Z: n > 5
        forall x in Z: x + 1 > x
    """
    expression = expression.strip()
    
    # Normaliser input
    expression = expression.replace("∀", "forall")
    expression = expression.replace("∃!", "exists!")  # Skal komme før ∃
    expression = expression.replace("∃", "exists")
    expression = expression.replace("∈", "in")
    expression = expression.replace("ℤ", "Z")
    expression = expression.replace("²", "**2")
    expression = expression.replace("³", "**3")
    expression = expression.replace("≥", ">=")
    expression = expression.replace("≤", "<=")
    expression = expression.replace("≠", "!=")
    expression = expression.replace("÷", "//")
    
    # Konverter matematisk notation til Python
    # Håndter = som == (men ikke <=, >=, !=, ==)
    # Vi skal gøre dette efter vi har håndteret de andre operatorer
    
    # Find quantifier type
    if expression.startswith("forall"):
        quantifier = "forall"
        rest = expression[6:].strip()
    elif expression.startswith("exists!"):
        quantifier = "exists!"
        rest = expression[7:].strip()
    elif expression.startswith("exists"):
        quantifier = "exists"
        rest = expression[6:].strip()
    else:
        return {"error": "Udtryk skal starte med 'forall', 'exists' eller 'exists!'"}
    
    # Find variabel og domæne
    if " in " not in rest:
        return {"error": "Mangler 'in' mellem variabel og domæne"}
    
    var_part, domain_and_predicate = rest.split(" in ", 1)
    variable = var_part.strip()
    
    # Find domæne og prædikat
    if ":" not in domain_and_predicate:
        return {"error": "Mangler ':' mellem domæne og prædikat"}
    
    domain_str, predicate = domain_and_predicate.split(":", 1)
    domain_str = domain_str.strip()
    predicate = predicate.strip()
    
    # Konverter enkelt = til == i prædikatet (men ikke <=, >=, !=, ==)
    # Matcher = som ikke er en del af <=, >=, !=, ==
    predicate = re.sub(r'(?<![<>!=])=(?!=)', '==', predicate)
    
    return {
        "quantifier": quantifier,
        "variable": variable,
        "domain": domain_str,
        "predicate": predicate
    }


def evaluate_expression(expression: str, domain_range=None) -> dict:
    """
    Evaluerer et prædikatslogisk udtryk.
    
    Args:
        expression: Udtryk som string, f.eks. "forall n in Z: n**2 >= 0"
        domain_range: Range at teste over (default: -100 til 100)
    
    Returns:
        Dictionary med resultat og forklaring
    """
    if domain_range is None:
        domain_range = range(-100, 101)
    
    parsed = parse_simple_expression(expression)
    
    if "error" in parsed:
        return parsed
    
    quantifier = parsed["quantifier"]
    variable = parsed["variable"]
    predicate = parsed["predicate"]
    
    # Opret lambda funktion til prædikatet
    try:
        # Sikker evaluering med kun variablen
        predicate_fn = eval(f"lambda {variable}: {predicate}")
    except SyntaxError as e:
        return {"error": f"Syntaksfejl i prædikat: {e}"}
    
    # Evaluer baseret på quantifier type
    try:
        if quantifier == "forall":
            for value in domain_range:
                if not predicate_fn(value):
                    return {
                        "result": False,
                        "counterexample": {variable: value},
                        "explanation": f"Modeksempel fundet: {variable}={value}"
                    }
            return {
                "result": True,
                "explanation": f"Sandt for alle {variable} i [{domain_range.start}, {domain_range.stop-1}]"
            }
        
        elif quantifier == "exists":
            examples = []
            for value in domain_range:
                if predicate_fn(value):
                    examples.append(value)
                    if len(examples) >= 5:
                        break
            
            if examples:
                return {
                    "result": True,
                    "examples": examples,
                    "explanation": f"Eksempler: {variable} ∈ {{{', '.join(map(str, examples))}}}"
                }
            return {
                "result": False,
                "explanation": f"Ingen {variable} i [{domain_range.start}, {domain_range.stop-1}] opfylder prædikatet"
            }
        
        elif quantifier == "exists!":
            # Find alle værdier der opfylder prædikatet
            examples = []
            for value in domain_range:
                if predicate_fn(value):
                    examples.append(value)
                    if len(examples) > 1:
                        # Mere end én - stop tidligt
                        break
            
            if len(examples) == 1:
                return {
                    "result": True,
                    "examples": examples,
                    "explanation": f"Præcis ét element opfylder: {variable} = {examples[0]}"
                }
            elif len(examples) == 0:
                return {
                    "result": False,
                    "explanation": f"Ingen {variable} i [{domain_range.start}, {domain_range.stop-1}] opfylder prædikatet"
                }
            else:
                return {
                    "result": False,
                    "examples": examples,
                    "explanation": f"Mere end ét element opfylder prædikatet, f.eks. {variable} ∈ {{{', '.join(map(str, examples))}}}"
                }
    except Exception as e:
        return {"error": f"Evalueringsfejl: {e}"}


def print_result(result: dict) -> None:
    """Printer resultatet pænt formateret."""
    print("")
    if "error" in result:
        print(f"FEJL: {result['error']}")
    else:
        print(f"Resultat: {result['result']}")
        if "explanation" in result:
            print(f"Forklaring: {result['explanation']}")
        if "counterexample" in result:
            print(f"Modeksempel: {result['counterexample']}")
        if "examples" in result:
            print(f"Eksempler: {result['examples']}")


def main():
    """Kør prædikatslogik evaluator interaktivt."""
    print("")
    print("=" * 70)
    print("        PRÆDIKATSLOGIK EVALUATOR")
    print("=" * 70)
    print("")
    print("Understøttede kvantorer:")
    print("  forall / ∀   : universel kvantor (for alle)")
    print("  exists / ∃   : eksistentiel kvantor (der findes)")
    print("  exists! / ∃! : unik eksistens (der findes præcis én)")
    print("  ¬∀ / ¬∃      : negation af kvantorer")
    print("")
    print("Understøttede operatorer:")
    print("  ⇒ / imp      : implikation (A ⇒ B)")
    print("  ⇔ / bimp     : biimplikation (A ⇔ B)")
    print("  ∧ / and      : konjunktion")
    print("  ∨ / or       : disjunktion")
    print("  ¬ / not      : negation")
    print("")
    print("Relationer og aritmetik:")
    print("  >, <, >=, <=, =, !=")
    print("  +, -, *, /, **, ·")
    print("  ², ³         : potenser")
    print("")
    print("Eksempler:")
    print("  ∃x ∈ ℤ : x = 5")
    print("  ∀x ∈ ℤ : x² >= 0")
    print("  ∀x, y ∈ ℤ : x² + y² >= 0")
    print("  ∃x ∈ ℤ : ∀y ∈ ℤ : x + y > 0")
    print("  ∀x ∈ ℤ : (x² < 0 ⇒ x = 0)")
    print("  ¬∀x ∈ ℤ : x² < 4")
    print("")
    print("Kommandoer:")
    print("  'test'  : Kør test-eksempler")
    print("  'q'     : Afslut")
    print("")
    
    while True:
        print("-" * 70)
        expression = input("Indtast udtryk: ")
        
        if expression.lower() in ['q', 'quit', 'exit']:
            print("Farvel!")
            break
        
        if expression.lower() == 'test':
            test_examples()
            continue
        
        if expression.strip() == "":
            continue
        
        # Prøv først den avancerede evaluator
        result = evaluate_advanced(expression)
        
        if "error" in result:
            # Fallback til simpel evaluator
            result = evaluate_expression(expression)
        
        print_result(result)


if __name__ == "__main__":
    main()

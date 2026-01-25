# predicate_logic.py
# Evaluerer prædikatslogiske udsagn over domæner som ℤ
import re

# Operator syntax:
# forall / ∀ : universal quantifier
# exists / ∃ : existential quantifier  
# and / ∧
# or / ∨
# not / ¬ / -
# imp / → : implication
# bimp / ↔ : bi-implication
# > , < , >= , <= , == , != : relationer

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
    print("=" * 60)
    print("        Prædikatslogik Evaluator")
    print("=" * 60)
    print("")
    print("Understøttede kvantorer:")
    print("  forall / ∀  : universel kvantor (for alle)")
    print("  exists / ∃  : eksistentiel kvantor (der findes)")
    print("  exists! / ∃! : unik eksistens (der findes præcis én)")
    print("")
    print("Operatorer:")
    print("  **          : potens (f.eks. n**2)")
    print("  >, <        : større end, mindre end")
    print("  >=, <=      : større/mindre eller lig")
    print("  =, ==       : lig med")
    print("  !=          : forskellig fra")
    print("  +, -, *, /  : aritmetiske operatorer")
    print("  //, %       : heltalsdivision, modulo")
    print("")
    #print("Eksempler på udtryk:")
    #print("  forall n in Z: n**2 >= 0")
    #print("  exists n in Z: n > 5")
    #print("  forall x in Z: x + 1 > x")
    #print("  exists n in Z: n**2 == 16")
    print("Operator syntax:")
    print("forall / ∀ : universal quantifier")
    print("exists / ∃ : existential quantifier")
    print("# and / ∧")
    print("# or / ∨")
    print("# not / ¬ / -")
    print("# imp / → : implication")
    print("# bimp / ↔ : bi-implication")
    print("# > , < , >= , <= , == , != : relationer")

    print("")
    
    while True:
        print("-" * 60)
        expression = input("Indtast udtryk (eller 'q' for at afslutte): ")
        
        if expression.lower() in ['q', 'quit', 'exit']:
            print("Farvel!")
            break
        
        if expression.strip() == "":
            continue
        
        result = evaluate_expression(expression)
        print_result(result)


if __name__ == "__main__":
    main()

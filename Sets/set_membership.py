# set_membership.py
# Verificerer mængde-identiteter med membership tables (ligesom truth tables)

# Kør dette program i terminalen!!!

# Operator syntax:
# U, |, ∪    : Union (foreningsmængde)
# &, ∩       : Intersection (fællesmængde)  
# -, \       : Difference (differens)
# '          : Complement (komplement), f.eks. A'
# =          : Lighed
# =>         : Implikation

# Mængde-variabler: A, B, C, D, E, F, G, H, I, J

MembershipTable = tuple[str, list[str], list[list[bool]], list[tuple[bool, bool]], str]

def generate_membership_table(expression: str) -> MembershipTable:
    """Genererer en membership table for et mængde-udtryk."""
    left, right, expr_type = parse_statement(expression)
    variables = find_variables(expression)
    
    # Generer alle kombinationer af medlemskab (som truth table)
    membership_rows = bool_combinations(len(variables))
    
    outputs = []
    for row in membership_rows:
        # Opret dict: variabel -> bool (er x medlem af denne mængde?)
        membership = dict(zip(variables, row))
        
        left_result = evaluate_set_expr(left, membership)
        right_result = evaluate_set_expr(right, membership)
        
        outputs.append((left_result, right_result))
    
    return (expression, variables, membership_rows, outputs, expr_type)

def parse_statement(statement: str) -> tuple[str, str, str]:
    """Parser udsagn og returnerer (venstre, højre, type)."""
    stmt = normalize_operators(statement)
    
    if '=>' in stmt:
        parts = stmt.split('=>')
        return (parts[0].strip(), parts[1].strip(), 'implication')
    
    if '=' in stmt:
        parts = stmt.split('=')
        return (parts[0].strip(), parts[1].strip(), 'equality')
    
    if '<=' in stmt:
        parts = stmt.split('<=')
        return (parts[0].strip(), parts[1].strip(), 'subset')
    
    raise ValueError("Udsagn skal indeholde =, => eller <=")

def normalize_operators(expr: str) -> str:
    """Normaliserer operatorer til standard format."""
    result = expr
    
    # Union varianter -> |
    result = result.replace('∪', '|')
    result = result.replace(' U ', ' | ')
    result = result.replace(' u ', ' | ')
    result = result.replace('(U ', '(| ')
    result = result.replace('(u ', '(| ')
    result = result.replace(' U)', ' |)')
    result = result.replace(' u)', ' |)')
    
    # Intersection varianter -> &
    result = result.replace('∩', '&')
    
    # Difference
    result = result.replace('\\', '-')
    
    # Tom mængde
    result = result.replace('∅', 'Ø')
    result = result.replace('EMPTY', 'Ø')
    
    # Universel mængde
    result = result.replace('𝕌', '𝑈')
    result = result.replace('UNI', '𝑈')
    
    return result

def evaluate_set_expr(expr: str, membership: dict[str, bool]) -> bool:
    """
    Evaluerer om et vilkårligt element x er medlem af mængde-udtrykket.
    membership[A] = True betyder x ∈ A
    """
    tokens = tokenize(expr)
    return eval_tokens(tokens, membership)

def tokenize(expr: str) -> list[str]:
    """Opdeler udtryk i tokens."""
    tokens = []
    i = 0
    expr = expr.replace(' ', '')
    
    while i < len(expr):
        if expr[i] in 'ABCDEFGHIJ':
            tokens.append(expr[i])
            i += 1
        elif expr[i] in '()|&-':
            tokens.append(expr[i])
            i += 1
        elif expr[i] == "'":
            tokens.append("'")
            i += 1
        elif expr[i] == 'Ø':
            tokens.append('Ø')
            i += 1
        elif expr[i] == '𝑈':
            tokens.append('𝑈')
            i += 1
        else:
            i += 1
    
    return tokens

def eval_tokens(tokens: list[str], membership: dict[str, bool]) -> bool:
    """Evaluerer tokens til boolean ved at bygge et Python-udtryk."""
    # Konverter tokens til Python-udtryk med korrekt komplement-håndtering
    py_expr = tokens_to_python(tokens, membership)
    
    if not py_expr.strip():
        return False
    
    try:
        return eval(py_expr)
    except:
        return False

def tokens_to_python(tokens: list[str], membership: dict[str, bool]) -> str:
    """Konverterer tokens til Python-udtryk med korrekt komplement-håndtering."""
    result = []
    i = 0
    
    while i < len(tokens):
        token = tokens[i]
        
        if token in 'ABCDEFGHIJ':
            # Check om næste token er komplement
            value = str(membership.get(token, False))
            # Tæl antal komplement-tegn efter
            complements = 0
            while i + 1 < len(tokens) and tokens[i + 1] == "'":
                complements += 1
                i += 1
            # Ulige antal komplement = negér
            if complements % 2 == 1:
                result.append(f"(not {value})")
            else:
                result.append(value)
        elif token == '(':
            result.append('(')
        elif token == ')':
            result.append(')')
            # Check for komplement efter parentes
            complements = 0
            while i + 1 < len(tokens) and tokens[i + 1] == "'":
                complements += 1
                i += 1
            if complements % 2 == 1:
                # Wrap hele parentesen i not
                # Find matchende åben parentes
                depth = 1
                j = len(result) - 2  # Start før den lukkede parentes
                while j >= 0 and depth > 0:
                    if result[j] == ')':
                        depth += 1
                    elif result[j] == '(':
                        depth -= 1
                    j -= 1
                j += 1  # j peger nu på åben parentes
                # Indsæt "not " før parentesen
                result.insert(j, '(not ')
                result.append(')')
        elif token == '|':
            result.append(' or ')
        elif token == '&':
            result.append(' and ')
        elif token == '-':
            result.append(' and not ')
        elif token == 'Ø':
            result.append('False')
        elif token == '𝑈':
            result.append('True')
        elif token == "'":
            # Standalone komplement (skulle være håndteret ovenfor)
            pass
        
        i += 1
    
    return ''.join(result)


def find_variables(expr: str) -> list[str]:
    """Finder mængde-variabler."""
    expr_normalized = normalize_operators(expr)
    
    # Fjern Ø og 𝑈 så vi ikke finder dem som variabler
    expr_clean = expr_normalized.replace('Ø', '').replace('𝑈', '')
    
    variables = []
    for char in expr_clean:
        if char in 'ABCDEFGHIJ' and char not in variables:
            variables.append(char)
    
    return sorted(variables)

def bool_combinations(n: int) -> list[list[bool]]:
    """Alle kombinationer af True/False med længde n."""
    if n == 0:
        return [[]]
    
    results = []
    for combo in bool_combinations(n - 1):
        results.append([True] + combo)
        results.append([False] + combo)
    return results

def verify_statement(expression: str) -> tuple[bool, MembershipTable]:
    """Verificerer et mængde-udsagn."""
    table = generate_membership_table(expression)
    expr, variables, rows, outputs, expr_type = table
    
    is_valid = True
    
    if expr_type == 'implication':
        is_valid = verify_implication(expression)
    else:
        for left_result, right_result in outputs:
            if expr_type == 'equality':
                if left_result != right_result:
                    is_valid = False
                    break
            elif expr_type == 'subset':
                if left_result and not right_result:
                    is_valid = False
                    break
    
    return (is_valid, table)

def verify_implication(expression: str) -> bool:
    """Verificerer implikation: P => Q."""
    stmt = normalize_operators(expression)
    parts = stmt.split('=>')
    antecedent = parts[0].strip()
    consequent = parts[1].strip()
    
    variables = find_variables(expression)
    rows = bool_combinations(len(variables))
    
    for row in rows:
        membership = dict(zip(variables, row))
        
        ante_valid = evaluate_equation(antecedent, membership)
        cons_valid = evaluate_equation(consequent, membership)
        
        if ante_valid and not cons_valid:
            return False
    
    return True

def evaluate_equation(equation: str, membership: dict[str, bool]) -> bool:
    """Evaluerer om en ligning er sand."""
    if '=' not in equation:
        return evaluate_set_expr(equation, membership)
    
    parts = equation.split('=')
    left = evaluate_set_expr(parts[0].strip(), membership)
    right = evaluate_set_expr(parts[1].strip(), membership)
    return left == right

def print_membership_table(table: MembershipTable) -> None:
    """Printer membership table."""
    expr, variables, rows, outputs, expr_type = table
    
    stmt = normalize_operators(expr)
    if '=>' in stmt:
        left_h, right_h = stmt.split('=>')[0].strip(), stmt.split('=>')[1].strip()
    elif '=' in stmt:
        left_h, right_h = stmt.split('=')[0].strip(), stmt.split('=')[1].strip()
    else:
        left_h, right_h = "L", "R"
    
    print(f"\nMembership Table:")
    print(f"{'─' * 50}")
    
    # Header
    var_header = "  ".join(variables)
    print(f"{var_header}  │  L  R  │ =")
    print("─" * 50)
    
    # Rows
    for i, row in enumerate(rows):
        row_str = "  ".join(['1' if v else '0' for v in row])
        left_val = '1' if outputs[i][0] else '0'
        right_val = '1' if outputs[i][1] else '0'
        match = 'T' if outputs[i][0] == outputs[i][1] else 'F'
        print(f"{row_str}  │  {left_val}  {right_val}  │ {match}")
    
    print(f"\nL = {left_h}")
    print(f"R = {right_h}")

def print_result(expression: str, is_valid: bool, table: MembershipTable) -> None:
    """Printer resultat."""
    print("\n" + "=" * 50)
    print(f"Udsagn: {expression}")
    print("=" * 50)
    
    if is_valid:
        print("✓ SANDT for alle mængder!")
    else:
        print("✗ FALSK - ikke en gyldig identitet")
        print_membership_table(table)

def main() -> None:
    """Kører programmet."""
    print("\n" + "=" * 55)
    print("MÆNGDE-IDENTITETS VERIFICERING (Membership Table)")
    print("=" * 55)
    print("\nOperatorer:")
    print("  U, |, ∪   : Union")
    print("  &, ∩      : Intersection")
    print("  -, \\      : Difference")
    print("  '         : Complement (f.eks. A')")
    print("  =         : Lighed")
    print("  =>        : Implikation")
    print("  Ø, ∅      : Tom mængde")
    print("  𝕌, UNI    : Universel mængde")
    print("\nVariabler: A, B, C, D, E, F, G, H, I, J")
    print("\nEksempler:")
    print("  A & (B U C) = (A & B) U (A & C)")
    print("  A - B = A => A & B = Ø")
    print("  A U A' = 𝕌")
    print("-" * 55)
    
    while True:
        try:
            statement = input("\nIndtast udsagn (eller 'quit'): ")
            
            if statement.lower() in ['quit', 'exit', 'q']:
                break
            
            if not statement.strip():
                continue
            
            is_valid, table = verify_statement(statement)
            print_result(statement, is_valid, table)
            
        except KeyboardInterrupt:
            print("\nAfbrudt.")
            break
        except Exception as e:
            print(f"Fejl: {e}")

if __name__ == "__main__":
    main()

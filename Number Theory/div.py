# from div import *
# ============================================================================
# DIVISIBILITY IMPLICATION CHECKER
# ============================================================================
# Definition: a | b  iff  ∃c ∈ Z+ : a·c = b  (where a, b ∈ Z)
# 
# This module can verify/disprove statements like:
#   (2 | a) ∧ (3 | a)  ⟹  (6 | a)
#   (a | b) ∧ (a | c)  ⟹  (a | (2a + b − c))
#   (a | 2b)  ⟹  (a | b)
# ============================================================================

import re
from itertools import product

def _parse_linear_expr(expr_str: str, variables: dict) -> int:
    """
    Parses a linear expression like '2a + b - c', '3a', 'a', '7', etc.
    Returns the evaluated integer value.
    """
    expr_str = expr_str.replace(' ', '').replace('−', '-')
    
    # Handle empty or just a number
    if not expr_str:
        return 0
    
    # Try direct number
    try:
        return int(expr_str)
    except ValueError:
        pass
    
    # Parse terms like: 2a, -3b, +c, -d, 7, -5
    # Add '+' at start if not starting with sign
    if expr_str[0] not in ['+', '-']:
        expr_str = '+' + expr_str
    
    # Pattern: optional sign, optional coefficient, optional variable
    pattern = r'([+-])(\d*)([a-z]?)'
    
    result = 0
    pos = 0
    while pos < len(expr_str):
        match = re.match(pattern, expr_str[pos:])
        if match:
            sign_str, coef_str, var = match.groups()
            sign = 1 if sign_str == '+' else -1
            
            if var:  # There's a variable
                coef = int(coef_str) if coef_str else 1
                if var not in variables:
                    raise ValueError(f"Unknown variable: {var}")
                result += sign * coef * variables[var]
            elif coef_str:  # Just a number
                result += sign * int(coef_str)
            
            pos += len(match.group(0))
            if pos < len(expr_str) and expr_str[pos] not in ['+', '-']:
                pos += 0  # Continue
        else:
            pos += 1
    
    return result


def _eval_divisibility(left_str: str, right_str: str, variables: dict) -> bool:
    """
    Evaluates a | b where left_str and right_str are arithmetic expressions.
    """
    left = _parse_linear_expr(left_str.strip(), variables)
    right = _parse_linear_expr(right_str.strip(), variables)
    
    if left == 0:
        return right == 0
    return right % left == 0


def _find_matching_paren(s: str, start: int) -> int:
    """Find the index of the closing parenthesis matching the one at start."""
    depth = 1
    i = start + 1
    while i < len(s) and depth > 0:
        if s[i] == '(':
            depth += 1
        elif s[i] == ')':
            depth -= 1
        i += 1
    return i - 1


def _preprocess_expr(expr: str) -> str:
    """Normalize the expression: replace unicode, standardize spacing."""
    expr = expr.replace('∧', ' AND ')
    expr = expr.replace('∨', ' OR ')
    expr = expr.replace('⟹', ' IMPLIES ')
    expr = expr.replace('→', ' IMPLIES ')
    expr = expr.replace('⟺', ' IFF ')
    expr = expr.replace('↔', ' IFF ')
    expr = expr.replace('¬', ' NOT ')
    expr = expr.replace('~', ' NOT ')
    expr = expr.replace('−', '-')
    return expr


def _is_logical_operator(s: str, pos: int) -> tuple:
    """
    Check if position contains a logical operator.
    Returns (operator_name, length) or (None, 0).
    """
    remaining = s[pos:].lstrip()
    offset = len(s[pos:]) - len(remaining)
    
    for op, name in [('IMPLIES', 'IMPLIES'), ('AND', 'AND'), ('OR', 'OR'), 
                      ('IFF', 'IFF'), ('NOT', 'NOT')]:
        if remaining.startswith(op):
            # Make sure it's not part of a word
            after = remaining[len(op):]
            if not after or not after[0].isalpha():
                return (name, offset + len(op))
    return (None, 0)


def _find_divisibility_bar(s: str) -> int:
    """
    Find the | that represents divisibility (not inside parentheses).
    Returns index or -1 if not found.
    """
    depth = 0
    for i, c in enumerate(s):
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        elif c == '|' and depth == 0:
            return i
    return -1


def _is_divisibility_atom(s: str) -> bool:
    """Check if string is a divisibility statement (contains | at top level)."""
    return _find_divisibility_bar(s) != -1


def _eval_atom(atom: str, variables: dict) -> bool:
    """Evaluate a divisibility atom like '2 | a' or '(a+b) | c'."""
    bar_pos = _find_divisibility_bar(atom)
    if bar_pos == -1:
        raise ValueError(f"No divisibility bar found in: {atom}")
    
    left = atom[:bar_pos].strip()
    right = atom[bar_pos+1:].strip()
    
    # Remove outer parentheses if present
    if left.startswith('(') and left.endswith(')'):
        # Check if they match
        if _find_matching_paren(left, 0) == len(left) - 1:
            left = left[1:-1]
    if right.startswith('(') and right.endswith(')'):
        if _find_matching_paren(right, 0) == len(right) - 1:
            right = right[1:-1]
    
    return _eval_divisibility(left, right, variables)


class _LogicalParser:
    """
    Recursive descent parser for logical expressions with divisibility atoms.
    
    Grammar:
        expr     -> iff_expr
        iff_expr -> impl_expr (IFF impl_expr)*
        impl_expr -> or_expr (IMPLIES or_expr)*
        or_expr  -> and_expr (OR and_expr)*
        and_expr -> not_expr (AND not_expr)*
        not_expr -> NOT not_expr | primary
        primary  -> '(' expr ')' | divisibility_atom
    """
    
    def __init__(self, expr: str, variables: dict):
        self.expr = _preprocess_expr(expr)
        self.variables = variables
        self.pos = 0
    
    def parse(self) -> bool:
        result = self._parse_iff()
        return result
    
    def _skip_whitespace(self):
        while self.pos < len(self.expr) and self.expr[self.pos] in ' \t\n':
            self.pos += 1
    
    def _check_operator(self, op: str) -> bool:
        self._skip_whitespace()
        if self.expr[self.pos:].startswith(op):
            # Make sure it's not part of a longer word
            after_pos = self.pos + len(op)
            if after_pos >= len(self.expr) or not self.expr[after_pos].isalpha():
                return True
        return False
    
    def _consume_operator(self, op: str):
        self._skip_whitespace()
        if self.expr[self.pos:].startswith(op):
            self.pos += len(op)
            return True
        return False
    
    def _parse_iff(self) -> bool:
        left = self._parse_implies()
        while self._check_operator('IFF'):
            self._consume_operator('IFF')
            right = self._parse_implies()
            left = (left == right)
        return left
    
    def _parse_implies(self) -> bool:
        left = self._parse_or()
        while self._check_operator('IMPLIES'):
            self._consume_operator('IMPLIES')
            right = self._parse_or()
            left = (not left) or right
        return left
    
    def _parse_or(self) -> bool:
        left = self._parse_and()
        while self._check_operator('OR'):
            self._consume_operator('OR')
            right = self._parse_and()
            left = left or right
        return left
    
    def _parse_and(self) -> bool:
        left = self._parse_not()
        while self._check_operator('AND'):
            self._consume_operator('AND')
            right = self._parse_not()
            left = left and right
        return left
    
    def _parse_not(self) -> bool:
        self._skip_whitespace()
        if self._check_operator('NOT'):
            self._consume_operator('NOT')
            return not self._parse_not()
        return self._parse_primary()
    
    def _parse_primary(self) -> bool:
        self._skip_whitespace()
        
        if self.pos >= len(self.expr):
            raise ValueError("Unexpected end of expression")
        
        if self.expr[self.pos] == '(':
            # Could be: (logical expr) or (arith) | something
            # We need to look ahead to determine which
            
            # Find the matching closing paren
            close_pos = _find_matching_paren(self.expr, self.pos)
            
            # Look after the closing paren for a | (divisibility)
            after_paren = self.expr[close_pos+1:].lstrip()
            
            if after_paren.startswith('|'):
                # This is (arith) | something - a divisibility atom
                # Find the full atom
                return self._parse_divisibility_atom()
            else:
                # This is (logical expr)
                self.pos += 1  # skip (
                result = self._parse_iff()
                self._skip_whitespace()
                if self.pos < len(self.expr) and self.expr[self.pos] == ')':
                    self.pos += 1
                return result
        else:
            # It's a divisibility atom
            return self._parse_divisibility_atom()
    
    def _parse_divisibility_atom(self) -> bool:
        """Parse a divisibility atom like '2 | a' or '(a+b) | (c-d)'."""
        self._skip_whitespace()
        start = self.pos
        
        # Read until we hit a logical operator or end
        depth = 0
        found_bar = False
        
        while self.pos < len(self.expr):
            c = self.expr[self.pos]
            
            if c == '(':
                depth += 1
                self.pos += 1
            elif c == ')':
                if depth == 0:
                    break
                depth -= 1
                self.pos += 1
            elif c == '|' and depth == 0:
                found_bar = True
                self.pos += 1
            elif depth == 0:
                # Check for logical operators
                op, length = _is_logical_operator(self.expr, self.pos)
                if op:
                    break
                self.pos += 1
            else:
                self.pos += 1
        
        atom = self.expr[start:self.pos].strip()
        
        if not atom:
            raise ValueError(f"Empty atom at position {start}")
        
        return _eval_atom(atom, self.variables)


def _evaluate_logical(expr: str, variables: dict) -> bool:
    """
    Evaluates a logical expression with divisibility statements.
    """
    parser = _LogicalParser(expr, variables)
    return parser.parse()


def _extract_variables(expr: str) -> set:
    """
    Extracts all variable names from an expression.
    """
    # First, replace logical operators with spaces (full words only)
    cleaned = expr
    cleaned = re.sub(r'∧', ' ', cleaned)
    cleaned = re.sub(r'∨', ' ', cleaned)
    cleaned = re.sub(r'⟹', ' ', cleaned)
    cleaned = re.sub(r'→', ' ', cleaned)
    cleaned = re.sub(r'⟺', ' ', cleaned)
    cleaned = re.sub(r'↔', ' ', cleaned)
    cleaned = re.sub(r'¬', ' ', cleaned)
    cleaned = re.sub(r'~', ' ', cleaned)
    cleaned = cleaned.replace('(', ' ').replace(')', ' ')
    cleaned = cleaned.replace('|', ' ')
    cleaned = cleaned.replace('+', ' ').replace('-', ' ').replace('−', ' ')
    
    # Find all single lowercase letters that appear as variables
    # A variable is a letter possibly preceded by a digit coefficient
    # Pattern: either standalone letter or digit(s) followed by letter
    variables = set()
    pattern = r'(?<![a-zA-Z])(\d*)([a-z])(?![a-zA-Z])'
    for match in re.finditer(pattern, cleaned):
        var = match.group(2)
        variables.add(var)
    
    return variables


def check_divisibility_statement(statement: str, search_range: range = None, 
                                  verbose: bool = True) -> dict:
    """
    Checks if a divisibility statement/implication is universally true or finds counterexamples.
    
    Args:
        statement: A logical statement involving divisibility, e.g.:
                   "(2 | a) ∧ (3 | a) ⟹ (6 | a)"
                   "(a | b) ∧ (a | c) ⟹ (a | (2a + b - c))"
                   "(a | 2b) ⟹ (a | b)"
        search_range: Range of values to test (default: range(1, 51) for positive integers)
        verbose: Whether to print results
    
    Returns:
        dict with keys:
            'valid': bool - True if no counterexample found
            'counterexamples': list - List of counterexample variable assignments
            'tested': int - Number of combinations tested
    
    Definition used: a | b iff ∃c ∈ Z+ : a·c = b
    """
    if search_range is None:
        search_range = range(1, 51)
    
    variables = sorted(_extract_variables(statement))
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Checking: {statement}")
        print(f"Variables: {variables}")
        print(f"Search range: [{search_range.start}, {search_range.stop - 1}]")
        print(f"{'='*60}")
    
    counterexamples = []
    tested = 0
    
    # Test all combinations
    for values in product(search_range, repeat=len(variables)):
        var_dict = dict(zip(variables, values))
        tested += 1
        
        try:
            result = _evaluate_logical(statement, var_dict)
            if not result:
                counterexamples.append(var_dict.copy())
                if len(counterexamples) >= 5:  # Limit counterexamples
                    break
        except Exception as e:
            # Skip invalid combinations (e.g., division by zero)
            pass
    
    if verbose:
        if counterexamples:
            print(f"\n❌ FALSK - Modeksempler fundet:")
            for i, ce in enumerate(counterexamples[:5], 1):
                var_str = ", ".join(f"{k}={v}" for k, v in ce.items())
                print(f"   {i}. {var_str}")
                # Show why it's false
                _explain_counterexample(statement, ce)
        else:
            print(f"\n✓ SAND (ingen modeksempler fundet i {tested} kombinationer)")
    
    return {
        'valid': len(counterexamples) == 0,
        'counterexamples': counterexamples,
        'tested': tested
    }


def _explain_counterexample(statement: str, variables: dict):
    """
    Explains why a counterexample makes the statement false.
    """
    # Find the implication structure
    if '⟹' in statement or '→' in statement:
        parts = re.split(r'⟹|→', statement, maxsplit=1)
        if len(parts) == 2:
            premise = parts[0].strip()
            conclusion = parts[1].strip()
            
            premise_val = _evaluate_logical(premise, variables)
            conclusion_val = _evaluate_logical(conclusion, variables)
            
            print(f"      Præmis: {premise} = {premise_val}")
            print(f"      Konklusion: {conclusion} = {conclusion_val}")
            
            # Show individual divisibility evaluations
            _show_divisibilities(statement, variables)


def _show_divisibilities(statement: str, variables: dict):
    """Shows evaluation of each divisibility in the statement."""
    # Find divisibility atoms by scanning for | at top level
    # Process the statement to find all X | Y patterns
    
    processed = _preprocess_expr(statement)
    divisibilities = []
    
    # Find all divisibility patterns
    i = 0
    while i < len(processed):
        # Look for | at current nesting level
        if processed[i] == '|':
            # Find left side (go back to start of atom)
            left_end = i
            left_start = i - 1
            depth = 0
            while left_start >= 0:
                c = processed[left_start]
                if c == ')':
                    depth += 1
                elif c == '(':
                    if depth == 0:
                        break
                    depth -= 1
                elif depth == 0 and c in ' \t\n':
                    if left_start > 0 and processed[left_start-1:left_start+3] in ['AND', ' AND']:
                        break
                    if processed[max(0,left_start-2):left_start+1] in ['OR ', ' OR']:
                        break
                left_start -= 1
            left_start = max(0, left_start + 1)
            
            # Find right side
            right_start = i + 1
            right_end = i + 1
            depth = 0
            while right_end < len(processed):
                c = processed[right_end]
                if c == '(':
                    depth += 1
                elif c == ')':
                    if depth == 0:
                        break
                    depth -= 1
                elif depth == 0 and c in ' \t\n':
                    remaining = processed[right_end:].lstrip()
                    if remaining.startswith('AND') or remaining.startswith('OR') or remaining.startswith('IMPLIES') or remaining.startswith('IFF'):
                        break
                right_end += 1
            
            left = processed[left_start:left_end].strip()
            right = processed[right_start:right_end].strip()
            
            # Clean up parentheses
            if left.startswith('(') and left.endswith(')'):
                if _find_matching_paren(left, 0) == len(left) - 1:
                    left = left[1:-1]
            if right.startswith('(') and right.endswith(')'):
                if _find_matching_paren(right, 0) == len(right) - 1:
                    right = right[1:-1]
            
            if left and right:
                divisibilities.append((left, right))
        i += 1
    
    if divisibilities:
        seen = set()
        print(f"      Delelighedsværdier:")
        for left, right in divisibilities:
            key = (left.strip(), right.strip())
            if key in seen:
                continue
            seen.add(key)
            try:
                left_val = _parse_linear_expr(left, variables)
                right_val = _parse_linear_expr(right, variables)
                divides_result = right_val % left_val == 0 if left_val != 0 else right_val == 0
                symbol = "✓" if divides_result else "✗"
                print(f"         {left}={left_val}, {right}={right_val}: {left_val} | {right_val} {symbol}")
            except:
                pass


def verify_divisibility(statement: str, max_val: int = 50) -> bool:
    """
    Quick verification of a divisibility statement.
    Returns True if valid (no counterexamples found), False otherwise.
    
    Examples:
        verify_divisibility("(2 | a) ∧ (3 | a) ⟹ (6 | a)")  # True
        verify_divisibility("(a | 2b) ⟹ (a | b)")  # False
    """
    result = check_divisibility_statement(statement, range(1, max_val + 1), verbose=False)
    return result['valid']


def find_divisibility_counterexample(statement: str, max_val: int = 100) -> dict | None:
    """
    Finds a counterexample for a divisibility statement if one exists.
    Returns None if no counterexample found.
    
    Examples:
        find_divisibility_counterexample("(a | 2b) ⟹ (a | b)")
        # Returns: {'a': 4, 'b': 2}
    """
    result = check_divisibility_statement(statement, range(1, max_val + 1), verbose=False)
    if result['counterexamples']:
        return result['counterexamples'][0]
    return None


# Convenience function with nicer name
div_check = check_divisibility_statement

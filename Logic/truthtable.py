PY_OPERATORS = ["and", "or", "==", "not", "!="]

# Run this program as a whole
# Kør dette program i terminalen!!!

#Operator syntax:
#and
#or
#not (can be written either as "-" or "not")
#imp = implication
#bimp = bi-implication
#xor: exclusive or

TruthTable = tuple[str, list, list, list]

def generate_truthtable(expression: str) -> TruthTable:
    """Generates a tuple with the information of a truthtable"""
    new_expression = remove_redundant_not(translate_ops(space_format(expression)))
    variables = find_variables(new_expression)
    truth_rows = bool_combinations(len(variables))
    outputs = []
    for row in truth_rows:
        i = 0
        current_expression = new_expression.split()
        while i < len(row):
            j = 0
            while j < len(current_expression):
                if current_expression[j] == variables[i]:
                    current_expression[j] = str(row[i])
                j += 1
            i += 1
        current_expression = " ".join(current_expression)
        outputs.append(calc_bool(current_expression))
    return (expression, variables, truth_rows, outputs)

def translate_ops(expression) -> str:
    """Translates exclusive operations to python operators"""
    translated_expression = []
    lst_expression = expression.split()
    i = 0
    while i < len(lst_expression):
        if lst_expression[i] == "imp":
            j = len(translated_expression) - 1
            bracket_balance = 0
            while j >= 0:
                if translated_expression[j] == ")":
                    bracket_balance -= 1
                elif translated_expression[j] == "(":
                    bracket_balance += 1

                if bracket_balance == 0:
                    translated_expression.insert(j, "not")
                    break
                j -= 1
            translated_expression.append("or")
        elif lst_expression[i] == "rimp":
            translated_expression.append("or")
            translated_expression.append("not")
        elif lst_expression[i] == "bimp":
            if lst_expression[i+1] == "not":
                translated_expression.append("!=")
                i+=1
            else:
                translated_expression.append("==")
        elif lst_expression[i] == "xor":
            if lst_expression[i+1] == "not":
                translated_expression.append("==")
                i+=1
            else:
                translated_expression.append("!=")
        else:
            translated_expression.append(lst_expression[i])
        i += 1
    return " ".join(translated_expression)

def calc_bool(expression: str) -> bool:
    """Evaluates the boolean value of a proposition"""
    expression = expression.replace("not True", "False")
    expression = expression.replace("not False", "True")
    return eval(expression)

def bool_combinations(n: int) -> list[list[bool]]:
    """Returns a list with all combinations of True and False with n length"""
    results = []
    _bool_combinations(results, n, [])
    return results

def _bool_combinations(results: list, n: int, combination_list: list) -> None:
    """Appends all combinations of True and False with n length to results"""
    if n == 0:
        results.append(combination_list)
    else:
        for value in [True, False]:
            if combination_list == []:
                _bool_combinations(results, n-1, [value])
            else:
                _bool_combinations(results, n-1, combination_list + [value])    

def find_variables(expression: str) -> list[str]:
    """Returns a list of the variabes of a proposition"""
    unique_variables = []
    for sub in expression.split(" "):
        if (sub not in unique_variables and
            sub not in (PY_OPERATORS + ["(", ")"])):
            unique_variables.append(sub)
    return unique_variables

def space_format(expression: str) -> str:
    """Spaces parts of an expression appropiately"""
    spaced_expression = ""
    for char in expression:
        if char == "(":
            spaced_expression += char + " "
        elif char == "-":
            spaced_expression += "not" + " "
        elif char == ")":
            spaced_expression += " " + char
        else:
            spaced_expression += char
    return spaced_expression

def remove_redundant_not(expression: str) -> str:
    """Removes redundant negations "not not not A" = "not A"""
    stack = []
    for sub in expression.split():
        if stack and stack[-1] == "not" and sub == "not":
            stack.pop()
        else:
            stack.append(sub)
    return " ".join(stack)

def print_truthtable(table_info: TruthTable) -> None:
    """Prints the information of a truthtable appropiately."""
    expression = table_info[0]
    variables = table_info[1]
    truth_rows = table_info[2]
    results = table_info[3]
    print("")
    print("Truthtable for:", expression, '\n')
    print("    ".join(variables))
    for i, row in enumerate(truth_rows):
        print("    ".join([str(value)[0] for value in row]), "  =  ", results[i])

def main() -> None:
    """Runs truthtable program."""
    valid_operators = [["and"],
                       ["or"],
                       ["xor"],
                       ["-", "not"],
                       ["imp", "implication"],
                       ["bimp", "bi-implication"],
                       ["rimp", "reverse implication"]]
    print("")
    print("Valid operators:\n")
    for operator in valid_operators:
        print(" : ".join(operator))
    while True:
        print("--------------------------")
        truthtable = generate_truthtable(input("Input expression: "))
        print_truthtable(truthtable)
        
if __name__ == "__main__":
    main()

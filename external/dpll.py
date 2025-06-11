def dpll(clauses, assignment={}):
    clauses, assignment = unit_propagation(clauses, assignment)
    if clauses is None:
        return None  # Conflict detected
    if not clauses:
        return assignment  # All clauses satisfied
    clauses, assignment = pure_literal_elimination(clauses, assignment)
    if clauses is None:
        return None
    if not clauses:
        return assignment
    var = choose_variable(clauses)
    
    if var is None:
        return assignment

    for value in [True, False]:  # Try assigning True, then False
        new_clauses = simplify_clauses(clauses, var, value)
        new_assignment = assignment.copy()
        new_assignment[var] = value
        result = dpll(new_clauses, new_assignment)
        if result is not None:
            return result
    return None

def simplify_clauses(clauses, var, value):
    new_clauses = []
    for clause in clauses:
        new_clause = []
        for literal in clause:
            if abs(literal) == var:
                if (literal > 0) == value:
                    new_clause = None  # Clause is satisfied
                    break
            else:
                new_clause.append(literal)
        if new_clause is not None:
            if not new_clause:
                return None  # Conflict
            new_clauses.append(new_clause)
    return new_clauses

def unit_propagation(clauses, assignment):
    while True:
        unit_clauses = [clause for clause in clauses if len(clause) == 1]
        if not unit_clauses:
            break  # No more unit clauses
        
        literal = unit_clauses[0][0]  # Pick the first unit clause
        var, value = abs(literal), literal > 0
        if var in assignment and assignment[var] != value:
            return None, assignment
        assignment[var] = value
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue  # Clause satisfied, remove it
            new_clause = [lit for lit in clause if lit != -literal]
            if not new_clause:
                return None, assignment  # Conflict detected
            new_clauses.append(new_clause)
        
        clauses = new_clauses  # Update clauses after simplification
    return clauses, assignment

def pure_literal_elimination(clauses, assignment):
    literals = {lit for clause in clauses for lit in clause}
    pure_literals = {lit for lit in literals if -lit not in literals}
    
    for literal in pure_literals:
        var = abs(literal)
        value = literal > 0
        if var in assignment and assignment[var] != value:
            return None, assignment
        assignment[var] = value
        clauses = [clause for clause in clauses if literal not in clause]
    return clauses, assignment

def choose_variable(clauses):
    for clause in clauses:
        for literal in clause:
            return abs(literal)  # Pick the first variable found
    return None

# Example CNF: (A OR B) AND (NOT A OR C) AND (B OR NOT C)
cnf = [[1, 2], [-1, 3], [2, -3]]
dictionary={1:'A',2:'B',3:'C'}
result = dpll(cnf)
if result:
    pretty_result = {dictionary[var]: value for var, value in result.items()}
    print("Satisfiable with assignment:", pretty_result)
else:
    print("Unsatisfiable")
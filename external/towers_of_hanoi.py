import heapq

class TowersOfHanoiSolver:
    def __init__(self, n):
        self.n = n
        self.goal = tuple([(2, i) for i in range(n)])  # All on peg C
    
    def heuristic(self, state):
        """Manhattan distance heuristic"""
        return sum(1 for peg, _ in state if peg != 2)
    
    def successors(self, state):
        """Generate valid moves"""
        pegs = [[] for _ in range(3)]
        for disk, (peg, _) in enumerate(state):
            pegs[peg].append(disk)
        
        moves = []
        for from_peg in range(3):
            if not pegs[from_peg]: continue
            disk = min(pegs[from_peg])
            for to_peg in range(3):
                if from_peg != to_peg and (not pegs[to_peg] or min(pegs[to_peg]) > disk):
                    new_state = list(state)
                    new_state[disk] = (to_peg, disk)
                    moves.append(tuple(new_state))
        return moves
    
    def solve(self):
        """A* search"""
        start = tuple([(0, i) for i in range(self.n)])
        open_set = [(self.heuristic(start), 0, start, [])]
        closed = set()
        
        while open_set:
            f, g, state, path = heapq.heappop(open_set)
            if state == self.goal: return path
            if state in closed: continue
            closed.add(state)
            
            for next_state in self.successors(state):
                if next_state not in closed:
                    # Find moved disk
                    disk = next(i for i in range(self.n) if state[i][0] != next_state[i][0])
                    move = (disk, state[disk][0], next_state[disk][0])
                    new_g = g + 1
                    heapq.heappush(open_set, (new_g + self.heuristic(next_state), 
                                            new_g, next_state, path + [move]))
        return None

def solve_hanoi(n):
    """Solve using A* search"""
    solver = TowersOfHanoiSolver(n)
    solution = solver.solve()
    
    if solution:
        plan = [(disk+1, ['A','B','C'][from_peg], ['A','B','C'][to_peg]) 
               for disk, from_peg, to_peg in solution]
        print(f"\nSolution for n={n}:")
        for i, (disk, from_peg, to_peg) in enumerate(plan, 1):
            print(f"Step {i}: Move disk {disk} from {from_peg} to {to_peg}")
        print(f"Total moves: {len(plan)} (Optimal: {2**n-1})")
        return len(plan)
    else:
        print(f"No solution found for n={n}")
        return 0

# Test the solver
print("=== TOWERS OF HANOI A* SOLVER ===")
for n in range(3,6):  # Test up to n=5
    moves = solve_hanoi(n)
    if moves == 2**n - 1:
        print(f"✓ Optimal solution found")
    print("-" * 40)
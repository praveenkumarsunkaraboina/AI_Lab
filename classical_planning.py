class State:
    def __init__(self, monkey_loc, box_loc, bananas_loc, monkey_height, bananas_height,
has_bananas):
        self.monkey_loc = monkey_loc
        self.box_loc = box_loc
        self.bananas_loc = bananas_loc
        self.monkey_height = monkey_height
        self.bananas_height = bananas_height
        self.has_bananas = has_bananas
        self.original_box_loc = box_loc  # Store the original box location
    def __str__(self):
        return (f"Monkey at {self.monkey_loc} ({self.monkey_height}), "
                f"Box at {self.box_loc}, "
                f"Bananas at {self.bananas_loc} ({self.bananas_height}), "
                f"Has bananas: {self.has_bananas}")

# Action definitions with intermediate printouts
def go(state, dest):
    print(f"\nAction: Go from {state.monkey_loc} to {dest}.")
    state.monkey_loc = dest
    print(state)

def push(state, dest):
    print(f"\nAction: Push box (and monkey) from {state.box_loc} to {dest}. ")
    # Monkey and box must be co-located and monkey should be Low to push.
    if state.monkey_loc == state.box_loc and state.monkey_height == "Low":
        state.monkey_loc = dest
        state.box_loc = dest
    else:
        print("Error: Cannot push because the monkey isn't with the box or is not Low!")
    print(state)

def climb_up(state):
    print("\nAction: Climb up onto the box.")
    # To climb, monkey must be at the same location as the box and be on the floor.
    if state.monkey_loc == state.box_loc and state.monkey_height == "Low":
        state.monkey_height = "High"
    else:
        print("Error: Cannot climb up because conditions are not met!")
    print(state)

def climb_down(state):
    print("\nAction: Climb down from the box.")
    # Monkey can climb down if currently High.
    if state.monkey_height == "High":
        state.monkey_height = "Low"
    else:
        print("Error: Monkey is already on the floor!")
    print(state)

def grasp(state):
    print("\nAction: Grasp the bananas.")
    # To grasp, monkey must be at the same location as bananas and at the same height.
    if state.monkey_loc == state.bananas_loc and state.monkey_height == state.bananas_height:
        state.has_bananas = True
    else:
        print("Error: Cannot grasp bananas; monkey must be at the same location and height as the bananas!")
    print(state)

def ungrasp(state):
    print("\nAction: Ungrasp (drop) the bananas.")
    if state.has_bananas:
        state.has_bananas = False
        # When dropping, bananas take on monkey's current location and height.
        state.bananas_loc = state.monkey_loc
        state.bananas_height = state.monkey_height
    else:
        print("Error: Monkey doesn't have bananas to ungrasp!")
    print(state)

def goal_achieved(state):
    # The final goal is that the monkey has the bananas and the box is at its original location.
    return state.has_bananas and state.box_loc == state.original_box_loc

# ---------------------------------------------------------------------------
# Initialize the state:
# Monkey at A (Low), Box at B, Bananas at C (High)
state = State(monkey_loc="A", box_loc="B", bananas_loc="C",
              monkey_height="Low", bananas_height="High", has_bananas=False)
print("[Initial State]")
print(state)
# ---------------------------------------------------------------------------
# Plan steps to fool the scientists and achieve the goal:
#
# Step 1. Go to the box at B.
go(state, "B")
# Step 2. Push the box from B to bananas location C.
push(state, "C")
# Step 3. Climb up onto the box at C.
climb_up(state)
# Step 4. Grasp the bananas (both at C and now High).
grasp(state)
# Step 5. Climb down from the box (monkey becomes Low).
climb_down(state)
# Step 6. Ungrasp (drop) the bananas (bananas now become Low, at current monkey location C).
ungrasp(state)
# Step 7. Push the box back to its original location.
push(state, state.original_box_loc)
# Step 8. Go back to where the bananas are (C).
go(state, "C")

# Step 9. Grasp the bananas again now that monkey and bananas are both High at C.
grasp(state)

print("\n[Final State]")
print(state)

if goal_achieved(state):
    print("\n✅ Goal Achieved: Monkey has the bananas and the box is at its original position.")
else:
    print("\n❌ Goal Not Achieved.")
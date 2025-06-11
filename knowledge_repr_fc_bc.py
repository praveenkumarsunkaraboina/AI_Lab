room_kb = {
    "furniture": ["desk", "chair", "bed", "wardrobe", "bookshelf"],
    "windows": {"window1": "wall3", "window2": "wall4"},
    "door": {"door": "wall1"},
    "corners": {
        "corner1": ["wardrobe"],
        "corner2": [],
        "corner3": ["bed"],
        "corner4": ["desk"]

    },
    "locations": {
        "desk": "corner 4, wall4, in front of window2",
        "chair": "right(front) of desk",
        "bed": "wall3, corner3",
        "wardrobe": "corner1, wall1",
        "bookshelf": "wall2"
    },
    "relations": {
        "left_of": {"desk": "window2", "chair": "desk"},
        "right_of": {"bookshelf": "wall2", "bed": "wall2", "desk": "chair"},
        
        "next_to": {"desk": "chair", "chair": "desk", "bed": "bookshelf", "bookshelf": "bed"},
        "is_near": {"desk": ["chair", "window2"], "chair": ["desk", "bed"], "bed": ["chair",
"bookshelf"], "bookshelf": ["bed"]}
    }
}
# Rules (Query Functions)
def get_furniture():
    """Returns a list of furniture in the room."""
    return room_kb["furniture"]

def count_items(category):
    """Counts the number of items in a given category (e.g., doors, windows)."""
    return len(room_kb.get(category, {}))

def where_is(item):
    """Returns the location of a given item."""
    return room_kb["locations"].get(item, "Unknown location")

def what_is_at_wall(wall):
    """Returns a list of items located at a given wall."""
    return [item for item, loc in room_kb["locations"].items() if wall in loc]

def what_is_at_corner(corner):
    """Returns a list of items located at a given corner."""
    return room_kb["corners"].get(corner, [])

def left_of(item):
    """Returns what is to the left of a given item."""
    return room_kb["relations"]["left_of"].get(item, "Nothing to the left")

def right_of(item):
    """Returns what is to the right of a given item."""
    return room_kb["relations"]["right_of"].get(item, "Nothing to the right")

def next_to(item):
    """Returns what is next to a given item."""
    return room_kb["relations"]["next_to"].get(item, "Nothing next to it")

def is_near(item):
    """Returns a list of items near a given item."""
    return room_kb["relations"]["is_near"].get(item, "Nothing nearby")

print("1. What furniture is in the room?", get_furniture())
print("2. How many doors are in the room?", count_items("door"))
print("   How many windows are in the room?", count_items("windows"))

print("3. Where is the table (desk)?", where_is("desk"))
print("   Where is the chair?", where_is("chair"))
print("4. What is to the left of the desk?", left_of("desk"))
print("   What is to the right of the chair?", right_of("chair"))
print("6. What is at wall2?", what_is_at_wall("wall2"))
print("7. What is in corner1?", what_is_at_corner("corner1"))
print("8. What is next to the bed?", next_to("bed"))
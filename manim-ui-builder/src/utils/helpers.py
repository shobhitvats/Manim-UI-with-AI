def load_json(file_path):
    import json
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(file_path, data):
    import json
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def generate_unique_id(existing_ids):
    import uuid
    new_id = str(uuid.uuid4())
    while new_id in existing_ids:
        new_id = str(uuid.uuid4())
    return new_id

def validate_color(color):
    if isinstance(color, str) and color.startswith('#') and len(color) == 7:
        return True
    return False

def interpolate(start, end, fraction):
    return start + (end - start) * fraction

def format_latex(equation):
    return f"$${equation}$$"
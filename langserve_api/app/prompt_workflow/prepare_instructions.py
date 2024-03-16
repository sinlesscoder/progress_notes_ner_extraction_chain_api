from yaml import safe_load

# Load YAML
def load_yaml(file_path: str) -> dict:
    # Create a context manager
    with open(file_path) as buffer:
        results = safe_load(buffer)
    
    return results

# Design the instructions
def get_instructions(element_name: str, file_path: str) -> str:

    # Get the configuration
    yml_config = load_yaml(file_path=file_path)

    # Index the dictionary based on the element name
    return yml_config[element_name]['instructions']

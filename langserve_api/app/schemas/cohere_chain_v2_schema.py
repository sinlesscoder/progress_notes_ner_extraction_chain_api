def generate_schema(list_elements: list[str]) -> dict:
    # Generate the schema
    schema = {}

    schema['properties'] = {elem_name : {"type": "string"} for elem_name in list_elements}

    return schema

# Setup the schema
element = ['medications','labs','Social Determinants of Health','Cardiovascular Problems']

# Generate the schema
schema = generate_schema(list_elements=element)

print(schema)
def generate_schema(list_elements: list[str]) -> dict:
    # Generate the schema
    schema = {}

    schema['properties'] = {elem_name : {"type": "string"} for elem_name in list_elements}

    return schema

# Setup the schema
#elements = ['admission_date', 'discharge_date', 'date_of_birth', 'chief_complaint', 'allergies', 'surgical_or_invasive_procedure', 'patient_age', 'smoking_status']
element = ['medications','labs','Social Determinants of Health','Cardiovascular Problems']
# Generate the schema
schema = generate_schema(list_elements=element)
import pandas as pd
from os import getcwd, environ
from langchain.chains import create_extraction_chain_pydantic
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from schemas.cohere_chain_v1_pydantic_schema import CohereV1
from prompt_workflow.prepare_instructions import get_instructions
from postgres_connect import load_env_vars, postgres_engine
from sqlalchemy import text
from sqlalchemy.engine import Engine

# Configurations

# JSON
sql_json_path = getcwd() + "/postgres_creds.json"
openai_json_path = getcwd() + "/openai_api_key.json" #"/home/aahmed/Pathrise_DEDS_Ali_Tutorials/src/frameworks/generative_ai/llms/langchain/openai_api_key.json"
# Get YAML file
yml_path = getcwd() + '/prompt_workflow/instructions.yml'

# Update env var for OpenAI API Key
load_env_vars(file_path=openai_json_path)

# Setup an extraction chain
llm = ChatOpenAI(temperature=0, api_key=environ["OPENAI_API_KEY"])

# Extraction Template
extraction_template = """Extract and save the relevant entities mentioned \
in the following passage together with their properties.

Only extract the properties mentioned in the 'information_extraction' function.

If a property is not present and is not required in the function parameters, do not include it in the output.

{instructions}

Passage:
{input}
"""

# Generate custom prompt template
prompt = PromptTemplate(input_variables=['input', 'instructions'], template=extraction_template)

# Setup your extraction chain
chain = create_extraction_chain_pydantic(pydantic_schema=CohereV1, llm=llm, prompt=prompt)

# Create connection to PostgreSQL
engine = postgres_engine(file_path=sql_json_path)

def extract_results(query: str, table_name: str, schema_name: str, engine: Engine) -> pd.DataFrame:
    
    # Setup a cursor
    cursor = engine.connect()
    
    # Query
    query = text(query)

    # Get the table into pandas
    df = pd.read_sql_query(query, con=cursor)

    # Get 3 examples from Cohere Notes
    doc_ids = df['doc_id'].tolist()
    notes = df['text'].tolist()

    # Final Results
    final_results = []

    # Get the instructions
    instructions = get_instructions(element_name=schema_name, file_path=yml_path)

    # Iterate through examples and see results
    for i, note in enumerate(notes):
        # Get the output from Langchain
        result = chain.run(input=note, instructions=instructions)

        # Get only the dictionary
        result = result[0]

        # Add the doc_id
        result['doc_id'] = doc_ids[i]

        # Append to the final_results
        final_results.append(result)

        print(f'Document {i+1} finished processing')

    # Normalize the DataFrame
    frame = pd.json_normalize(data=final_results)

    # Write to a new table
    frame.to_sql(name=table_name, con=cursor, schema=schema_name, index=False, if_exists='replace')

    # Close the connection
    cursor.close()

    return frame
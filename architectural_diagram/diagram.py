from os import getcwd
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2Instance
from diagrams.aws.storage import SimpleStorageServiceS3BucketWithObjects
from diagrams.programming.framework import FastAPI
from diagrams.programming.language import Python
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.container import Docker
from diagrams.onprem.compute import Server
from diagrams.generic.os import LinuxGeneral
from diagrams.custom import Custom

# Helper Functions
def custom_edge(text: str, double_ended: bool = False) -> Edge:
    """
    Inputs:
        - text (string) : Label to define your specific edge between nodes
        - double_ended (boolean) : Choice of whether or not the edge connecting nodes should have arrows on both ends or not
    
    Output:
        - edge (diagrams.Edge) : Edge object that gets rendered in the diagram.
    """

    # Instantiate edge as None
    edge = None

    # Create logic to check if input double_ended
    if double_ended:
        edge = Edge(label=text, forward=True, reverse=True)
    else:
        edge = Edge(label=text)

    return edge

# Paths
img_path = getcwd() + "/architectural_diagram/img"
output_path = getcwd() + "/architectural_diagram/output"

# Create a context manager for the Diagram
with Diagram(filename=f'{output_path}/architecture_diagram', node_attr={'fontsize': '20'}, edge_attr={'fontsize': '20'}):
    
    # Database Deployment Cluster
    with Cluster(label='   PostgreSQL Deployment', graph_attr={'fontsize': '30', 'margin': '20'}):
        # Server Node
        server_node = Server(label='SSDNodes \n VPS')

        # Docker Node
        docker_db_node = Docker(label='Postgres 12.14 \n Image')

        server_node >> custom_edge(text='deploys') >> docker_db_node

    # ETL Cluster
    with Cluster(label='                                 ETL', graph_attr={'fontsize': '30', 'margin': '22'}):
        # S3 Node
        s3_node = SimpleStorageServiceS3BucketWithObjects(label='\n notes \n bucket')

        # Python ETL Script
        python_etl_script = Python(label="\n etl.py")

        # PostgreSQL Node
        postgresql_node = PostgreSQL("\n PostgreSQL")

        s3_node >> custom_edge(text='extracts') >> python_etl_script >> custom_edge(text='loads to') >> postgresql_node
    
    # 
    
    # Cluster for Hosting
    with Cluster(label='                         API Deployment', graph_attr={'fontsize': '30', 'margin': '17'}):
        with Cluster(label='           EC2 Development', graph_attr={'fontsize': '25', 'margin': '14'}):
            # EC2 Instance
            ec2_node = EC2Instance(label='\n EC2')

            # Linux General
            linux_node = LinuxGeneral(label="Amazon Linux \n AMI")

            ec2_node >> custom_edge(text='leverages') >> linux_node

        # Docker
        docker_api_node = Docker("Custom Image")

        linux_node >> custom_edge(text='deploys') >> docker_api_node
    
    # Cluster for API Development
    with Cluster(label='                   API', graph_attr={'fontsize': '30', 'margin' : '40'}):
        # Fast API
        fastapi_node = FastAPI("REST API \n via FastAPI")

        # Python Script
        python_api_script = Python(label="server.py")

        python_api_script >> fastapi_node
    
    # Cluster for Response Creation from the API
    with Cluster(label='                                                                       API Response', graph_attr={'fontsize': '30', 'margin': '10'}):
                
        with Cluster(label='                User Workflow', graph_attr={'fontsize': '25', 'margin': '40'}):
            # User Node
            user_node = Custom(label='User', icon_path=f'{img_path}/user_logo.png')

            # Input JSON Request
            input_json_node = Custom(label='Progress Note \n Input', icon_path=f'{img_path}/json_logo.png')

            user_node >> custom_edge(text='initiates request') >> input_json_node

        with Cluster(label='                                                Extraction Workflow', graph_attr={'fontsize': '25', 'margin': '40'}):
            # Langchain Node
            langchain_node = Custom(label='\n Langchain', icon_path=f'{img_path}/langchain--logo.png')

            # OpenAI Node
            openai_node = Custom(label='\n GPT 3.5', icon_path=f'{img_path}/openai_logo.png')

            # NER Node
            ner_node = Custom(label='\n named entity recognition', icon_path=f'{img_path}/ner_example.png')

            # Output JSON Response
            output_json_node = Custom(label='\n Output Response', icon_path=f'{img_path}/json_logo.png')

        langchain_node >> custom_edge(text='initiates') >> openai_node >> custom_edge(text='extracts') >> ner_node

    docker_api_node >> python_api_script
    python_api_script >> custom_edge(text='\n\n\n\n') >> postgresql_node
    docker_db_node >> postgresql_node
    fastapi_node >> custom_edge(text='\n\n\n\n\n') >> langchain_node
    input_json_node >> fastapi_node
    ner_node >> custom_edge(text='transmits response') >> output_json_node >> user_node

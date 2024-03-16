from os import getcwd
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2Instance
from diagrams.programming.framework import FastAPI
from diagrams.programming.language import Python
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.container import Docker
from diagrams.custom import Custom

# Paths
img_path = getcwd() + "/architectural_diagram/img"
output_path = getcwd() + "/architectural_diagram/output"

# Create a context manager for the Diagram
with Diagram(filename='architecture_diagram'):
    # PostgreSQL Node
    postgresql_node = PostgreSQL("PostgreSQL \n progress notes")
    
    # Cluster for Hosting
    with Cluster(label='Deployment'):
        # EC2 Instance
        ec2_node = EC2Instance(label='EC2')

        # Docker
        docker_node = Docker("Custom Image")

        ec2_node >> docker_node
    
    # Cluster for API Development
    with Cluster(label='API Development'):
        # Fast API
        fastapi_node = FastAPI("REST API \n via FastAPI")

        # Python Script
        python_script = Python(label="server.py")

        python_script >> fastapi_node
    
    docker_node >> python_script
    python_script >> Edge(forward=True, reverse=True) >> postgresql_node
    

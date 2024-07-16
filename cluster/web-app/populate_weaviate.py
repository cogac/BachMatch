
import weaviate
import pandas as pd
import json
from weaviate.util import generate_uuid5
import os


def get_weav_connection():
    client = weaviate.connect_to_custom(
        http_host=str(os.environ['WEAVSERVERHOST']),
        http_port=int(os.environ['WEAVSERVERPORT']),
        http_secure=False,
        grpc_host=str(os.environ['WEAVGRPCSERVERHOST']),
        grpc_port=int(os.environ['WEAVGRPCSERVERPORT']),
        grpc_secure=False,
    )
    return client
#
# client = weaviate.connect_to_custom(
#     http_host="10.107.139.48",
#     http_port="80",
#     http_secure=False,
#     grpc_host="10.104.91.155",
#     grpc_port="50051",
#     grpc_secure=False,
# )

# supes = client.collections.get("scientific_supervisors")


def populate_weaviate(client: weaviate.WeaviateClient):

    supes = client.collections.get("ScientificSupervisors")
    df = pd.read_csv('./data/supervisors_information.csv')
    # supes.query.near_vector()

    with supes.batch.dynamic() as batch:
        # Loop through the data
        for i, supervisor in enumerate(df.itertuples(index=False)):

            data = {
                "fname": supervisor.fname,
                "lname": supervisor.lname,
                "statement": supervisor.statement,
                "expertise": supervisor.expertise,
                "pre_cluster": supervisor.cluster

            }

            # Get the vector
            vector = json.loads(supervisor.vector)

            # Add object (including vector) to batch queue
            batch.add_object(
                properties=data,
                uuid=generate_uuid5(supervisor.id_hash),
                vector=vector  # Add the custom vector
                # references=reference_obj  # You can add references here
            )

    sc_works = client.collections.get("ExampleAbstract")

    df = pd.read_csv('./data/example_abstracts.csv')

    with sc_works.batch.dynamic() as batch:
        # Loop through the data
        for i, sc_work in enumerate(df.itertuples(index=False)):

            data = {
                "title": sc_work.title,
                "abstract": sc_work.text,
                "topic": sc_work.topic,
                "pre_cluster": sc_work.cluster

            }

            # Get the vector
            vector = json.loads(sc_work.vector)

            # Add object (including vector) to batch queue
            batch.add_object(
                properties=data,
                uuid=generate_uuid5(sc_work.id_hash),
                vector=vector  # Add the custom vector
                # references=reference_obj  # You can add references here
            )

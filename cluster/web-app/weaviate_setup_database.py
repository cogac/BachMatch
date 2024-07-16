import json
import weaviate
import weaviate.classes.config as wc
from weaviate.classes.config import Property, DataType
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


def create_all_collections(client):
    client.collections.create(
        name="ScientificSupervisors",
        properties=[
            wc.Property(name="fname", data_type=wc.DataType.TEXT),
            wc.Property(name="lname", data_type=wc.DataType.TEXT),
            wc.Property(name="statement", data_type=wc.DataType.TEXT),
            wc.Property(name="expertise", data_type=wc.DataType.TEXT),
            wc.Property(name="pre_cluster", data_type=wc.DataType.NUMBER)
        ],
    )

    client.collections.create(
        name="ExampleAbstract",
        properties=[
            wc.Property(name="title", data_type=wc.DataType.TEXT),
            wc.Property(name="abstract", data_type=wc.DataType.TEXT),
            wc.Property(name="topic", data_type=wc.DataType.TEXT),
            wc.Property(name="pre_cluster", data_type=wc.DataType.NUMBER)
        ],
    )

    client.collections.create(
        name="UserAbstract",
        properties=[
            wc.Property(name="title", data_type=wc.DataType.TEXT),
            wc.Property(name="abstract", data_type=wc.DataType.TEXT),
            wc.Property(name="topic", data_type=wc.DataType.TEXT)
        ],
    )
    print('created all collections')


def delete_all_collections(client):
    client.collections.delete('ScientificSupervisors')
    client.collections.delete('ExampleAbstract')
    client.collections.delete('UserAbstract')
    print('Deleted all collections')

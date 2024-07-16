from flask import Flask, render_template, request, redirect, session, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from weaviate.classes.query import Filter
import weaviate
import os

from wtforms.widgets import TextInput
import populate_weaviate
import weaviate_setup_database
import vectorizer
import weaviate.classes.query as wq
from kafka import KafkaProducer, KafkaConsumer, consumer
import json
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ['FLASK_FORM_SECRET'])
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line

# will be done in spark instead of the web server


# form classes


class UseAbstract(FlaskForm):
    submit = SubmitField('Try to find a Supervisor')


class AbstractInputForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(10, 400)])
    topic = StringField('Topic', validators=[DataRequired(), Length(10, 400)])
    absctract = TextAreaField('Abstract', validators=[DataRequired(), Length(0, 5000)])
    submit = SubmitField('Submit 2')

# Kafka stuff


def get_kafka_consumer():
    bootstrap = os.environ['KAFKABOOTSTRAP']
    consumer = KafkaConsumer('bachmatch', bootstrap_servers=bootstrap)
    return consumer


def get_kafka_producer():
    bootstrap = os.environ['KAFKABOOTSTRAP']
    producer = KafkaProducer(bootstrap_servers=bootstrap, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    return producer

# near vector query to weaviate


def get_near_vectors(client, collection_name, vector, vec_limit):
    collection = client.collections.get(collection_name)
    # Perform query
    response = collection.query.near_vector(
        near_vector=vector,  # A list of floating point numbers
        limit=vec_limit,
        return_metadata=wq.MetadataQuery(distance=True),
    )

    # Inspect the response
    possible_supervisors = [
        {"fname": obj.properties["fname"],
         "lname": obj.properties["lname"],
         "statement": obj.properties["statement"],
         "expertise": obj.properties["expertise"]} for obj in response.objects]
    return possible_supervisors


def make_vector_from_text(text):
    vector = vectorizer.vectorize([text]).toarray()[0].tolist()[:25]
    return vector

# connection client to weaviate database -- not one connection the whole part, would be bad for fault tolerance


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

# weaviate query to get all example abstracts


def get_example_abstracts(client):

    works = client.collections.get('ExampleAbstract')
    works_collector = [{"id": item.uuid, "title": item.properties['title']}
                       for item in works.iterator()]
    return works_collector


def get_user_abstracts(client):

    works = client.collections.get('UserAbstract')
    works_collector = [{"topic": item.properties['topic'], "title": item.properties['title'],
                        "abstract": item.properties['abstract']} for item in works.iterator()]
    return works_collector
# weaviate query to get a single abstract by the database uuid


def get_example_abstract(client, abstract_id):
    abstracts = client.collections.get('ExampleAbstract')
    abstract = abstracts.query.fetch_object_by_id(abstract_id, include_vector=True)
    return abstract.properties, abstract.vector['default']


# homepage
@app.route('/')
def homepage():

    return render_template('homepage.html')

# page with form to let user write text


@app.route('/new', methods=['GET', 'POST'])
def form():
    form = AbstractInputForm()
    message = ''
    possibles = ''
    possible_supes = ''
    if form.validate_on_submit():

        title = form.title.data
        topic = form.topic.data
        abstract = form.absctract.data
        producer = get_kafka_producer()
        producer.send('bachmatch', {'topic': topic, 'title': title,
                      'abstract': abstract, 'timestamp': time.time()//1000})
        client = get_weav_connection()
        possibles = get_user_abstracts(client)
        if not possibles:
            possibles = 'Weaviate does not contain any user abstracts'
        else:
            possible_supes = get_near_vectors(client, 'ScientificSupervisors',
                                              make_vector_from_text(possibles[-1]['abstract']), 10)

        client.close()

    return render_template('new_form.html', form=form, message=message, possibles=possibles,
                           possible_supes=possible_supes)


@app.route('/abstracts')
def show_abstracts():
    client = get_weav_connection()
    abstracts = get_example_abstracts(client)
    client.close()

    return render_template('show_examples.html', abstracts=abstracts)

# page to show a single abstract in detail


@app.route('/abstracts/<ab_id>', methods=['GET', 'POST'])
def show_abstract(ab_id):

    client = get_weav_connection()

    abstract, vector = get_example_abstract(client, ab_id)

    form = UseAbstract()

    possible_supervisors = ''
    if form.validate_on_submit():
        possible_supervisors = get_near_vectors(client, 'ScientificSupervisors', vector, 5)

    client.close()
    return render_template('show_abstract.html', abstract=abstract, form=form, possibles=possible_supervisors)


# startup stuff
with app.app_context():
    setup_client = get_weav_connection()
    weaviate_setup_database.delete_all_collections(setup_client)
    weaviate_setup_database.create_all_collections(setup_client)
    populate_weaviate.populate_weaviate(setup_client)
    setup_client.close()

# only needed if page is run directly instead of calling flask with the environment variable like in the docker file
if __name__ == "__main__":
    app.run(debug=True)

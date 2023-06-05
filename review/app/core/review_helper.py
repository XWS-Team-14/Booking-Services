import json

from kafka import KafkaConsumer

from app.constants import kafka_server


class ReviewHelper:
    def listen_to_reservations(self):
        consumer = KafkaConsumer('reservations',
                                 group_id='reservations',
                                 bootstrap_servers=[kafka_server],
                                 value_deserializer=lambda m: json.loads(m.decode('ascii')))

        for message in consumer:
            print(message)


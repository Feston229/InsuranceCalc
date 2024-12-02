import logging
from datetime import datetime
from enum import Enum

from aiokafka import AIOKafkaProducer


class KafkaTopic(Enum):
    """Kafka topic names."""

    INSURANCE = "insurance"


class KafkaMessage(Enum):
    """Kafka message types."""

    UPDATE = "User with ID {user_id} has updated {table} with ID {instance_id} at {timestamp}."
    CREATE = "User with ID {user_id} has created {table} with ID {instance_id} at {timestamp}."
    DELETE = "User with ID {user_id} has deleted {table} with ID {instance_id} at {timestamp}."


async def send_batch(
    producer: AIOKafkaProducer,
    topic: KafkaTopic,
    user_id: int,
    table: str,
    instance_list: list,
):
    await producer.start()

    partitions = await producer.partitions_for(topic)
    partition = list(partitions)[0]
    batch = producer.create_batch()

    for instance in instance_list:
        msg = KafkaMessage.CREATE.value.format(
            user_id=user_id,
            table=table,
            instance_id=instance.id,
            timestamp=datetime.now(),
        ).encode("utf-8")
        batch.append(key=None, value=msg, timestamp=None)

    await producer.send_batch(batch, topic, partition=partition)
    logging.info(f"{batch.record_count()} messages sent to partition {partition}")
    await producer.stop()

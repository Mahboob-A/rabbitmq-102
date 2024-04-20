import os, json
import pika
from dotenv import load_dotenv
from typing import Callable

load_dotenv()


class CloudAMQPHelper:
    class Config:
        QUEUE_NAME = "job_search_queue"
        ROUTING_KEY = "job_search"

    def __init__(self) -> None:
        url = os.environ.get("CLOUD_AMQP_URL")
        params = pika.URLParameters(url)

        self.__connection = pika.BlockingConnection(params)

    async def __get_channel_helper(self) -> pika.BlockingConnection:
        channel = self.__connection.channel()
        return channel

    async def __set_or_create_queue_helper(self) -> None:
        channel = await self.get_channel()

        # declare queue
        channel.queue_declare(queue=self.Config.QUEUE_NAME)

    # methods to interact from child class
    async def set_or_create_queue(self):
        await self.__set_or_create_queue_helper()

    async def get_channel(self):
        return await self.__get_channel_helper()

    def close_connection(self):
        self.__connection.close()


class JobConsumer(CloudAMQPHelper):

    async def consume_jobs(self,  callback: Callable) -> None:

        await self.set_or_create_queue()

        channel = await self.get_channel()

        channel.basic_consume(
            self.Config.QUEUE_NAME,
            callback,
            auto_ack=True
        )

        print("[x] Info: Consuming message!")

        # self.close_connection()


# if __name__ == '__main__':
cloudamqp_jobconsumer = JobConsumer()





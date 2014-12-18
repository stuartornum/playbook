import os
import boto.sqs
from boto.sqs.message import Message


def create_event(msg):
    try:
        aws_region = os.environ['AWS_REGION']
        aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        aws_queue = os.environ['AWS_QUEUE']

        conn = boto.sqs.connect_to_region(aws_region,
                                          aws_access_key_id=aws_access_key_id,
                                          aws_secret_access_key=aws_secret_access_key)

        queue = conn.get_queue(aws_queue)
        m = Message()
        m.set_body(msg)
        queue.write(m)
        return True
    except:
        return False


def get_events():
    while queue_count() != 0:
        aws_region = os.environ['AWS_REGION']
        aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        aws_queue = os.environ['AWS_QUEUE']

        conn = boto.sqs.connect_to_region(aws_region,
                                          aws_access_key_id=aws_access_key_id,
                                          aws_secret_access_key=aws_secret_access_key)

        queue = conn.get_queue(aws_queue)
        rs = queue.get_messages(10)

        for i in rs:
            print "Message:", i.get_body()
            queue.delete_message(i)


def queue_count():
    aws_region = os.environ['AWS_REGION']
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    aws_queue = os.environ['AWS_QUEUE']

    conn = boto.sqs.connect_to_region(aws_region,
                                      aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key)

    queue = conn.get_queue(aws_queue)
    return queue.count()

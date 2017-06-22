#!/usr/bin/env python2.7

import json
import os
from requests import Request, Session
import pprint
import boto3

pp = pprint.PrettyPrinter(indent=4)

def lambda_handler(event, context):
    pp.pprint(event)

    aws_sns_topic_arn = event['sns']
    url = event['url']
    method = event.get('method', 'GET')
    headers = event.get('headers')
    body = event.get('body')

    session = Session()
    request = Request(method, url).prepare()
    if headers is not None:
        request.headers = headers
    if body is not None:
        request.body = body
    response = session.send(request)

    if response.status_code == 200:
        content = response.text
        pp.pprint(content)
        publish_command_to_sns(aws_sns_topic_arn, content)
    else:
        pp.pprint(response)


# --------------- Helpers that build all of the responses ----------------


def publish_command_to_sns(aws_sns_topic_arn, message):
    client = boto3.client('sns')

    response = client.publish(
        TargetArn=aws_sns_topic_arn,
        #Message=json.dumps({'default': json.dumps(message)}),
        #Message=json.dumps(message),
        Message=message,
        MessageStructure='text'
    )

    print(response['ResponseMetadata'])

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        message = 'SNS Publish returned {} response instead of 200.'.format(
            response['ResponseMetadata']['HTTPStatusCode'])
        raise SNSPublishError(message)


class SNSPublishError(Exception):
    """ If something goes wrong with publishing to SNS """
    pass

#lambda_handler(None, None)

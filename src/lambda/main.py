#!/usr/bin/env python2.7

import json
import os
from requests import get
import pprint
import boto3

pp = pprint.PrettyPrinter(indent=4)

pun_url = 'https://pun.andrewmacheret.com'

def lambda_handler(event, context):
    pp.pprint(event)
    aws_sns_topic_arn = event['sns']

    response = get(pun_url)
    if response.status_code == 200:
        pun = response.json()['pun']
        pp.pprint(pun)
        publish_command_to_sns(aws_sns_topic_arn, pun)
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

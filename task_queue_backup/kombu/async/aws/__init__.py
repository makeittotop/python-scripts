# -*- coding: utf-8 -*-
from __future__ import absolute_import


def connect_sqs(aws_access_key_id=None, aws_secret_access_key=None, **kwargs):
    from .sqs.connection import AsyncSQSConnection
    return AsyncSQSConnection(
        aws_access_key_id, aws_secret_access_key, **kwargs
    )

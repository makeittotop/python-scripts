# -*- coding: utf-8 -*-
from __future__ import absolute_import

from kombu.async.aws.ext import boto, get_regions

from .connection import AsyncSQSConnection

__all__ = ['regions', 'connect_to_region']


def regions():
    if boto is None:
        raise ImportError('boto is not installed')
    return get_regions('sqs', connection_cls=AsyncSQSConnection)


def connect_to_region(region_name, **kwargs):
    for region in regions():
        if region.name == region_name:
            return region.connect(**kwargs)

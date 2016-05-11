#!/usr/bin/env python

import redis
import json
import base64
import sys

r = redis.StrictRedis(host='lic', port=4444, db=0)

# Get items from redis as json strings
items = r.lrange("download", 0, -1)

# Convert them to json or dicts
json_items = map(lambda x: json.loads(x), items)

print >>sys.stderr, "Total Items: ", len(json_items), "\n"

for item in json_items:
    body_decoded = json.loads(base64.b64decode(item['body']))
    (owner, task_id, retry) = body_decoded['args']
    print >>sys.stderr, owner, task_id, body_decoded['id']


sys.exit(0)

# Play along with the priority
json_items[3]['properties']['delivery_info']['priority'] = 10

# rearrange them in descending order of priorities
json_items.sort(key=lambda k: k['properties']['delivery_info']['priority'], reverse=True)

# Dump them back as strings 
items = map(lambda x : json.dumps(x), json_items)

# Delete the existing queue
r.delete("download")

# Push the items back in the queue as desired
for item in items:
  r.lpush("download", item)




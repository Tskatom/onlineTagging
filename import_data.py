#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Wei Wang"
__email__ = "tskatom@vt.edu"

import sys
import os
import sqlite3
import json

def import_data(data_file, db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    events = []
    with open(data_file) as df:
        max_num = 1
        for line in df:
            event = json.loads(line)
            eventId = max_num
            title = event["title"]
            content = event['eventText']
            date = event["DATEADDED"]
            location = event["ActionGeo_FullName"]
            actor1 = event["Actor1Name"]
            actor2 = event["Actor2Name"]
            eventType = event["EventRootCode"]
            eventCode = event["EventCode"]
            events.append([eventId, title, content, date, location, actor1, actor2, eventType, eventCode])
            max_num += 1

    sql = "insert into records values (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    c.executemany(sql, events)
    conn.commit()
    conn.close()

def import_task_instances(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    sql = "select event_id from records"
    task_id = 0
    instance_id = 0
    instances = []
    insert_sql = "insert into TaskInstances values (?, ?, ?, ?)"
    for row in c.execute(sql):
        event_id = row[0]
        for i in range(3):
            instances.append([instance_id, task_id, event_id, '0'])
            instance_id += 1
    c.executemany(insert_sql, instances)
    conn.commit()
    conn.close()

def main():
    data_file = sys.argv[1]
    db_file = sys.argv[2]
    import_data(data_file, db_file)

if __name__ == "__main__":
    main()


#!/usr/bin/env python

from celery import Celery


def q_monitor(app):

    state = app.events.State()

    def on_event(event):
        print "EVENT HAPPENED: ", event

    def announce_succeeded_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK SUCCEEEDED: %s[%s] %s' % (
            task.name, task.uuid, task.info(), ))

    def announce_sent_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK SENT: %s[%s] %s' % (
            task.name, task.uuid, task.info(), ))

    def announce_received_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK RECEIVED: %s[%s] %s' % (
            task.name, task.uuid, task.info(), ))

    def announce_revoked_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK REVOKED: %s[%s] %s' % (
            task.name, task.uuid, task.info(), ))

    def announce_started_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK STARTED: %s[%s] %s' % (
            task.name, task.uuid, task.info(), ))

    def announce_failed_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK FAILED: %s[%s] %s' % (
            task.name, task.uuid, task.info(), ))

    def announce_retried_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK RETRIED: %s[%s] %s' % (
            task.name, task.uuid, task.info(), ))

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                'task-succeeded' : announce_succeeded_tasks,
	        'task-sent' : announce_sent_tasks,
	        'task-received' : announce_received_tasks,
	        'task-revoked' : announce_revoked_tasks,
	        'task-started' : announce_started_tasks,
	        'task-retried' : announce_retried_tasks,
                #'*': state.event,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)

if __name__ == '__main__':
    app = Celery(broker='redis://lic:4444/0')
    q_monitor(app)


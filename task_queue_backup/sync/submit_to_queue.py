import sys
from os.path import basename
from uuid import uuid4

from task_queue.tasks import SyncTask, SpoolTask
from celery import chain

from bs_pipeline.sync import find_scene_deps
from bs_pipeline.sync import submit_cmds

def submit(**kwargs):
    operation = kwargs.get('launch_type')
    dep_file = kwargs.get('dep_file')
    ascp_cmd = submit_cmds.get_ascp_cmd(kwargs.get('sync_list'))
    #spool_cmd = submit_cmds.get_tractor_spool_cmd(kwargs.get('alf_script'), kwargs.get('spool_dry_run'))
    engine='fox:1503'
    priority=50
    alf_script=kwargs.get('alf_script')

    print >>sys.stderr, "dep file path:  ", dep_file
    print >>sys.stderr, "ascp cmd:  ", ascp_cmd
    #print >>sys.stderr, "spool cmd: ", spool_cmd

    new_uuid = uuid4()
    file_base_name = basename(dep_file).split('.')[0]
    sync_task_uuid = ("sync__{0}__{1}").format(file_base_name, new_uuid)    
    spool_task_uuid = ("spool__{0}__{1}").format(file_base_name, new_uuid)    

    # Prepare the `SyncTask`
    sync_task = SyncTask.subtask(args=(dep_file, ascp_cmd), task_id=sync_task_uuid)
    # Prepare the `RenderTask`
    spool_task = SpoolTask.subtask(args=(engine, priority, alf_script), task_id=spool_task_uuid, immutable=True)

    print >>sys.stderr, "operation: ", operation

    # Submit a `CHAIN` to the queue
    if operation == 'SYNC_RENDER':
        # with both - sync and spool tasks
        chain(sync_task, spool_task)()
        return sync_task_uuid
    elif operation == 'SYNC':
        # with just the sync task
        chain(sync_task)()
        return sync_task_uuid
    elif operation == 'RENDER':
        # with just the spool task
        chain(spool_task)()
        return spool_task_uuid
    
    #return (sync_task_uuid, spool_task_uuid)
    

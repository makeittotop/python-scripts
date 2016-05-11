"""
    Gather the 10 largest jobs spooled in the last hour
    >>> jobs = tq.jobs("spooltime > -1m")

    list all jobs for a user
    >>> jobs = tq.jobs("user=lizzy")

    list all the errored jobs for a user
    >>> jobs = tq.jobs("user=margaret and numerror")

    list all the ready jobs and sort by number of ready tasks
    >>> jobs = tq.jobs("numready", sort=["numready"])

    list all jobs with priority over 400 for a group of users
    >>> jobs = tq.jobs("priority > 400 and user in [john paul george ringo]")


    Example usage to perform an operation:

    Pause all jobs spooled in the last 1 minute
    >>> tq.pause("spooltime > -1m")

    or using the keyword
    >>> tq.pause(search="spooltime > -1m")

    or using a dictionary that identifies the job
    >>> job = {"jid": 12632, "other": "attributes"}
    >>> tq.pause(job)

    or using a list of dictionaries:
    >>> jobs = [{"jid": 1234}, {"jid", 1337}]
    >>>  tq.pause(jobs)

    or using results from other queries:
    >>> tq.pause(tq.jobs("spooltime > -1m"))
"""

import datetime, operator, types, os

import tractor.base.EngineClient as EngineClient
import tractor.base.EngineDB as EngineDB
import rpg.timeutil as timeutil

__all__ = (
    "jobs",
    "tasks",
    "commands",
    "invocations",
    "blades",
    "params",

    "chcrews",
    "chpri",
    "delay",
    "pause",
    "jattr",
    "delete",
    "undelete",
    "jtree",
    "interrupt",
    "restart",
    "retryallerrs",
    "skipallerrs",
    "undelay",
    "unpause",

    "retry",
    "resume",
    "skip",
    "log",

    "chkeys",
    "cattr",
    
    "nimby",
    "unnimby",
    "trace"
)

class TractorQueryError(Exception):
    pass

# an EngineClient is required for operations
ModuleEngineClient = EngineClient.TheEngineClient

def _setEngineClient(anEngineClient):
    """Set the global engine client object."""
    global ModuleEngineClient
    ModuleEngineClient = anEngineClient

def setEngineClientParam(**kw):
    """Permit setting of engine connection parameters: hostname, port, user, and password."""
    ModuleEngineClient.setParam(**kw)

def closeEngineClient():
    """Close connection to engine, ensuring engine no longer needs to maintain session."""
    ModuleEngineClient.close()
    
    
def _tractorSelect(table=None, where="", columns=[], sortby=[], limit=None, archive=False):
    """Query the specified table using the postgres server-side function TractorSelect(),
    using the engine as a proxy.
    """
    if where == "":
        raise TractorQueryError("A search clause must be specified.")
    try:
        rows = ModuleEngineClient.select(table, where, columns=columns, sortby=sortby, limit=limit, archive=archive)
    except EngineClient.EngineClientError, err:
        raise TractorQueryError(str(err))
    return rows

"""The next several functions are used for retrieving rows from the database.
They each have the same list of arguments:

search=

An optionally specified search string.  It uses the same
natural-language-like syntax as used on the command line, not SQL.

*BE AWARE* that not specifying a search clause will get *ALL* of the
objects from the database and could impact database and/or engine
performance for large result sets.

Because it is the first argument, the argument name does not need to
be specified.  For example, the following two queries are the same:

active_jobs = jobs(search="active")
active_jobs = jobs("active")

columns=

An optionally specified list of columns.  Not specifying
any columns will retrieve all columns for the give table.
Using this argument to specify only the required columns
may be used to achieve Space and time efficiencies since
less data will need to be retrieved from the database.

Columns of other tables can be specified with a dot
notation.  For example, to get the jobs' owner when
retrieving errored tasks:

errored_tasks = tasks(search="error", columns=["Job.owner"]

sortby=

The result set can be sorted on the database server
on the specified columns before being sent to the client.  Multiple columns
can be specified for secondary sorting.  Prefixing the column
name with '-' causes reverse sorting order.  For example, the
following call retrieves jobs spooled in the last hour, with
the jobs sorted alphabetically by owner, and secondarily with 
each owner's most recently spooled jobs appearing first.

recent_jobs = jobs("spooltime > -1h", sortby=["owner", "-spooltime"])

While item sorting could be done client side, it is not possible
to do so if the result set is truncated with the limit= argument,
since truncation will happen server side, before the client
has a chance to sort the results.

*BE AWARE* that sorting can have an impact on the database server.

limit=

Space and time efficiencies can be obtained by using the limit=
argument to place an upper bound on the number of rows returned
by the database server.

*BE AWARE* that the default setting of 0 places *NO LIMIT* on the
number of records returned, as opposed to returning no results
whatsoever.  Keep this in mind if the limit will be programmatically
determined.

archives=

This is a boolean flag that will search the archive tables, which
represent the records of jobs that have been deleted (plus associated
tasks, commands, etc.)

*BE AWARE* that archives can be *much* bigger than the live data
set, so queries can be *MUCH* more expensive to execute,
transmit, and store in memory.

Such expense can be avoided by:
* using well-specified search clauses to ensure small result sets
* not sorting on the server for larger sets
* using the limit argument and no sorting for potentially large result sets
"""

def jobs(search="", columns=[], sortby=[], limit=None, archive=False):
    """Retrieve a list of jobs."""
    return _tractorSelect("job", where=search, columns=columns, sortby=sortby, limit=limit, archive=archive)

def tasks(search="", columns=[], sortby=[], limit=None, archive=False):
    """Retrieve a list of tasks."""
    return _tractorSelect("task", where=search, columns=columns, sortby=sortby, limit=limit, archive=archive)

def commands(search="", columns=[], sortby=[], limit=None, archive=False):
    """Retrieve a list of commands."""
    return _tractorSelect("command", where=search, columns=columns, sortby=sortby, limit=limit, archive=archive)

def invocations(search="", columns=[], sortby=[], limit=None, archive=False):
    """Retrieve a list of invocations."""
    return _tractorSelect("invocation", where=search, columns=columns, sortby=sortby, limit=limit, archive=archive)

def blades(search="", columns=[], sortby=[], limit=None, archive=False):
    """Retrieve a list of blades."""
    return _tractorSelect("blade", where=search, columns=columns, sortby=sortby, limit=limit, archive=archive)

def params(search="", columns=[], sortby=[], limit=None, archive=False):
    """Retrieve a list of engine parameters."""
    return _tractorSelect("param", where=search, columns=columns, sortby=sortby, limit=limit, archive=archive)

def _checkRequiredAttributes(objs, attrs):
    """Raises an exception if any object is missing the specified attributes.
    Separate tests are done whether the object is an EngineDB.Row or a dict."""
    for obj in objs:
        for attr in attrs:
            if type(obj) is dict:
                if not obj.has_key(attr):
                    raise TractorQueryError("Target dictionary does not have required key %s: %s" % (attr, str(obj)))
            elif isinstance(obj, EngineDB.Row):
                if not hasattr(obj, attr):
                    raise TractorQueryError("Target row does not have required attribute %s: %s" % (attr, str(obj)))

def _jidsForArgs(firstarg, sortby, limit, archive=False):
    """Determine the jids for the specified jobs, which could be
    expressed as a dictionary, a list of dictionaries, or a search clause."""
    if firstarg == "":
        raise TractorQueryError("A search clause must be specified.")
    if type(firstarg) is str:
        # user has specified a search string; fetch the jobs
        jobz = jobs(firstarg, columns=["jid"], sortby=sortby, limit=limit, archive=archive)
    elif type(firstarg) is list:
        if sortby:
            raise TractorQueryError("'sortby' is not allowed when passing a list of objects to an operation.")
        if limit:
            jobz = firstarg[:limit]
        else:
            jobz = firstarg
        _checkRequiredAttributes(jobz, ["jid"])
    else:
        jobz = [firstarg]
        _checkRequiredAttributes(jobz, ["jid"])
    jids = [job["jid"] for job in jobz]
    return jids

"""The next several functions are used to perform operations on jobs,
tasks, and blades.  They each have a similar list of arguments:

*** BE CAREFUL *** using these operation functions because they are
*VERY* powerful and can be *VERY* *VERY* *VERY* *DESTRUCTIVE*.

firstarg=

The name of this generically-named argument is not intended to be
explicitly specified by the caller, but is merely used as a
place holder for a first argument of various types.  This permits
an operation to be specified by:
* a search clause
* a single object from a list returned by a query function
* a list of objects returned by a query function
* a dictionary specifying the required attributes for the operation
* a list of dictionaries specifying the required attributes for the operation

For example, all of the following are equivalent:

retry("jid=123 and tid=1")
retry(tasks("jid=123 and tid=1")[0])
retry(tasks("jid=123 and tid=1"))
retry({"jid": 123, "tid": 1})
retry([{"jid": 123, "tid": 1}])

search=

An optionally specified search string.  It uses the same
natural-language-like syntax as used on the command line, not SQL.

*BE AWARE* that not specifying a search clause will get *ALL* of the
objects from the database and could impact database and/or engine
performance for large result sets.

sort=

The result set can be sorted on the database server
on the specified columns before being sent to the client.  Multiple columns
can be specified for secondary sorting.  Prefixing the column
name with '-' causes reverse sorting order.  For example, the
following call pauses jobs spooled in the last hour, with
the operations performed in order of job owner, and secondarily by
pausing each owner's most recently spooled jobs first.

pause("spooltime > -1h", sortby=["owner", "-spooltime"])

While item sorting could be done client side, it is not possible
to do so if the result set is truncated with the limit= argument,
since truncation will happen server side, before the client
has a chance to sort the results.

*BE AWARE* that sorting can have an impact on the database server
for certain queries.

limit=

Space and time efficiencies can be obtained by using the limit=
argument to place an upper bound on the number of rows returned
by the database server, and hence the number of items operated on.

*BE AWARE* that the default setting of 0 places *NO LIMIT* on the
number of records returned, as opposed to returning no results
whatsoever.  Keep this in mind if the limit will be programmatically
determined.

ANOTHER WARNING LABEL

*** BE CAREFUL *** using these operation functions because they are
*VERY* powerful and can be *VERY* *VERY* *VERY* *DESTRUCTIVE*.

For exampe, either of these very short commands will delete
*every job*.

delete(jobs()) 
delete("jid")  # "jid" means "jid != 0", which is every job

Remember, you can use limit= to reduce the number of operations
performed at any one time.  So, for example, if you just want to
delete a single job, you could use limit=1 to ensure that a typo in
the search clause doesn't cause widespread damage.

In the following example, an accidentally specified "or jid"
would cause all jobs to be matched; although an incorrect job may be
deleted here, widespread damage has been avoided with limit=1.

delete("jid=123 or jid", limit=1)

Have fun!
"""

def chcrews(search="", sortby=[], limit=None, crews=None):
    """Change crews of matching jobs.  crews= specifies the new list of crews."""
    if crews is None:
        raise TractorQueryError("chcrews(): crews must be specified")
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.setJobCrews(jids, crews)
        
def chpri(search="", sortby=[], limit=None, priority=None):
    """Change priority of matching jobs.  priority= specifies the new priority."""
    if priority is None:
        raise TractorQueryError("chpri(): priority must be specified")
    if not operator.isNumberType(priority):
        raise TractorQueryError("chpri(): priority is not numeric")
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.setJobPriority(jids, priority)
        
def jattr(search="", sortby=[], limit=None, key=None, value=None):
    """Set an attribute of matching jobs.  key= specifies the attribute,
    and value= specifies the attribute value."""
    if key is None:
        raise TractorQueryError("jattr(): key must be specified")
    if value is None:
        raise TractorQueryError("jattr(): value is not specified")
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.setJobAttribute(jids, key, value)

def pause(search="", sortby=[], limit=None):
    """Pause matching jobs."""
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.pauseJob(jids)
        
def unpause(search="", sortby=[], limit=None):
    """Unpause matching jobs."""
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.unpauseJob(jids)
        
def interrupt(search="", sortby=[], limit=None):
    """Interrupt matching jobs."""
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.interruptJob(jids)
        
def restart(search="", sortby=[], limit=None):
    """Restart matching jobs."""
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.restartJob(jids)
        
def retryactive(search="", sortby=[], limit=None):
    """Retry all active tasks of matching jobs."""
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.retryAllActiveInJob(jids)
        
def retryerrors(search="", sortby=[], limit=None):
    """Retry all errored tasks of matching jobs."""
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.retryAllErrorsInJob(jids)
        
def skiperrors(search="", sortby=[], limit=None):
    """Skip all errored tasks of matching jobs."""
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.skipAllErrorsInJob(jids)
        
def delay(search="", sortby=[], limit=None, aftertime=None):
    """Delay matching jobs.  aftertime= specifies the time at which
    the job should be undelayed."""
    if aftertime is None:
        raise TractorQueryError("delay(): aftertime must be specified")
    elif isinstance(aftertime, datetime.datetime):
        aftertime = int(timeutil.date2secs(aftertime))
    elif isinstance(aftertime, str):
        try:
            aftertime = int(timeutil.date2secs(datetime.datetime.strptime(aftertime, "%Y-%m-%d %H:%M:%S")))
        except ValueError, err:
            raise TractorQueryError("aftertime, %s, is not of the format Y-m-d H:M:S : %s" % \
                (aftertime, str(err)))
    elif not operator.isNumberType(aftertime):
        raise TractorQueryError("aftertime %s is not seconds after the epoch or a datetime object or string." % \
             str(aftertime))
    
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.delayJob(jids, aftertime)
        
def undelay(search="", sortby=[], limit=None):
    """Undelay matching jobs."""
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.undelayJob(jids)
    
def delete(search="", sortby=[], limit=None):
    """Delete matching jobs."""
    jids = _jidsForArgs(search, sortby, limit)
    ModuleEngineClient.deleteJob(jids)
        
def undelete(search="", sortby=[], limit=None):
    """Restore matching jobs from the archive."""
    jids = _jidsForArgs(search, sortby, limit, archive=True)
    ModuleEngineClient.undeleteJob(jids)
        
def _jidsTidsOthersForArgs(firstarg, sortby, limit, otherMembers=[]):
    """Determine the jids and tids for the specified tasks, which could be
    expressed as a dictionary, a list of dictionaries, or a search clause."""
    if firstarg == "":
        raise TractorQueryError("A search clause must be specified.")
    if type(firstarg) is str:
        # user has specified a search string; fetch the tasks
        taskz = tasks(firstarg, columns=["jid", "tid"] + otherMembers, sortby=sortby, limit=limit)
    elif type(firstarg) is list:
        if sortby:
            raise TractorQueryError("'sortby' is not allowed when passing a list of objects to an operation.")
        if limit:
            taskz = firstarg[:limit]
        else:
            taskz = firstarg
        _checkRequiredAttributes(taskz, ["jid", "tid"] + otherMembers)
    else:
        taskz = [firstarg]
        _checkRequiredAttributes(taskz, ["jid", "tid"] + otherMembers)
    jidsTidsOthers = [tuple([task[member] for member in ["jid", "tid"] + otherMembers]) for task in taskz]
    return jidsTidsOthers

def retry(search="", sortby=[], limit=None):
    """Retry matching tasks."""
    jidsTids = _jidsTidsOthersForArgs(search, sortby, limit)
    for jidTid in jidsTids:
        ModuleEngineClient.retryTask(jidTid[0], jidTid[1])

def resume(search="", sortby=[], limit=None):
    """Resume matching tasks."""
    jidsTids = _jidsTidsOthersForArgs(search, sortby, limit)
    for jidTid in jidsTids:
        ModuleEngineClient.resumeTask(jidTid[0], jidTid[1])

def skip(search="", sortby=[], limit=None):
    """Skip matching tasks."""
    jidsTids = _jidsTidsOthersForArgs(search, sortby, limit)
    for jidTid in jidsTids:
        ModuleEngineClient.skipTask(jidTid[0], jidTid[1])

def log(search="", sortby=[], limit=None):
    """Fetch logs of matching tasks.  Logs are returned in a dictionary keyed by (jid, tid).
    Job.owner must be a key in the object.
    """
    # the requirement of Job.owner to be in the object may need to be relaxed for
    # sites that wish to use the API but don't organize their log files by owner.
    
    jidsTidsOwners = _jidsTidsOthersForArgs(search, sortby, limit, otherMembers=["Job.owner"])
    logByJidTid = {}
    for jidTidOwner in jidsTidsOwners:
        jid, tid, owner = jidTidOwner
        logByJidTid[(jid, tid)] = ModuleEngineClient.getTaskLog(jid, tid, owner)
    return logByJidTid

def _jidsCidsForArgs(firstarg, sortby, limit):
    """Determine the jids and cids for the specified commmands, which could be
    expressed as a dictionary, a list of dictionaries, or a search clause."""
    if firstarg == "":
        raise TractorQueryError("A search clause must be specified.")
    if type(firstarg) is str:
        # user has specified a search string; fetch the commands
        cmdz = commands(firstarg, columns=["jid", "cid"], sortby=sortby, limit=limit)
    elif type(firstarg) is list:
        if sortby:
            raise TractorQueryError("'sortby' is not allowed when passing a list of objects to an operation.")
        if limit:
            cmdz = firstarg[:limit]
        else:
            cmdz = firstarg
        _checkRequiredAttributes(cmdz, ["jid", "cid"])
    else: # assume type(firstarg) is dict or issubclass(firstarg.__class__, EngineDB.Row)
        cmdz = [firstarg]
        _checkRequiredAttributes(cmdz, ["jid", "cid"])
    jidsCids = [(cmd["jid"], cmd["cid"]) for cmd in cmdz]
    return jidsCids

def cattr(search="", sortby=[], limit=None, key=None, value=None):
    """Set an attribute of matching commands.  key= specifies the attribute
    and value= specifies the new attribute value."""
    if key is None:
        raise TractorQueryError("cattr(): key must be specified")
    if value is None:
        raise TractorQueryError("cattr(): value is not specified")
    jidsCids = _jidsCidsForArgs(search, sortby, limit)
    for jidCid in jidsCids:
        ModuleEngineClient.setCommandAttribute(jidCid[0], jidCid[1], key, value)

def chkeys(search="", sortby=[], limit=None, keystr=None):
    """Set the service key expression of matching commands.  keystr=
    specifies the new service key expression."""
    if keystr is None:
        raise TractorQueryError("chkeys(): keystr must be specified")
    jidsCids = _jidsCidsForArgs(search, sortby, limit)
    for jidCid in jidsCids:
        ModuleEngineClient.setCommandAttribute(jidCid[0], jidCid[1], "service", keystr)

def _namesIpaddrsForArgs(firstarg, sortby, limit):
    """Determine the names for the specified blades, which could be
    expressed as a dictionary, a list of dictionaries, or a search clause."""
    if firstarg == "":
        raise TractorQueryError("A search clause must be specified.")
    if type(firstarg) is str:
        # user has specified a search string; fetch the blades
        bladez = blades(firstarg, columns=["name", "ipaddr"], sortby=sortby, limit=limit)
    elif type(firstarg) is list:
        if sortby:
            raise TractorQueryError("'sortby' is not allowed when passing a list of objects to an operation.")
        if limit:
            bladez = firstarg[:limit]
        else:
            bladez = firstarg
        _checkRequiredAttributes(bladez, ["name", "ipaddr"])
    else: # assume type(firstarg) is dict or issubclass(firstarg.__class__, EngineDB.Row)
        bladez = [firstarg]
        _checkRequiredAttributes(bladez, ["name", "ipaddr"])
    namesIpaddrs = [(blade["name"], blade["ipaddr"]) for blade in bladez]
    return namesIpaddrs

def nimby(search="", sortby=[], limit=None):
    """Nimby matching blades."""
    namesIpaddrs = _namesIpaddrsForArgs(search, sortby, limit)
    for nameIpaddr in namesIpaddrs:
        ModuleEngineClient.nimbyBlade(nameIpaddr[0], nameIpaddr[1])

def unnimby(search="", sortby=[], limit=None):
    """Unnimby matching blades."""
    namesIpaddrs = _namesIpaddrsForArgs(search, sortby, limit)
    for nameIpaddr in namesIpaddrs:
        ModuleEngineClient.unnimbyBlade(nameIpaddr[0], nameIpaddr[1])

def trace(search="", sortby=[], limit=None):
    """Fetch trace output of matching blades.  Output is returned as a dict keyed by (name, ipaddr)."""
    namesIpaddrs = _namesIpaddrsForArgs(search, sortby, limit)
    traceByNameIpaddr = {}
    for nameIpaddr in namesIpaddrs:
        traceByNameIpaddr[nameIpaddr] = ModuleEngineClient.traceBlade(nameIpaddr[0], nameIpaddr[1])
    return traceByNameIpaddr

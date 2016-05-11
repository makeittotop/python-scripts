#!/usr/bin/env python

import sys, os
sys.path.append("/nas/projects/development/productionTools/tactic/src/client")

from tactic_client_lib import TacticServerStub

import ipdb; ipdb.set_trace();

server = TacticServerStub.get()               
ticket=server.get_login_ticket()              
server.set_ticket(ticket)   
                  
server.set_server("172.16.10.22")             
server.set_project("bilal")                   
username="abhishek"                           
passwd="abhishek"                             
ticket=server.get_ticket(username, passwd)    
server.set_ticket(ticket)                     

pub_file = sys.argv[1] #'/nas/projects/Tactic/sandbox/bilal/ashish/sequences/seq29/scn46/sh005_SHOT00001280/compositing/compositing/seq29_scn46_sh005_cmp_compositing_v005.nk'
mode = sys.argv[2]

base_name = os.path.basename(pub_file)
type = base_name.split('.')[-1]
(seq, scn, shot, elem, process, ver) = base_name.split('.')[0].split('_')
if elem == 'lig':
    context = 'lighting'
    process = context
elif elem == 'cmp':
    context = 'compositing'
    process = context    

expr = ("@SOBJECT(%s/seq['name','%s']['s_status', 'is', 'NULL'])" % ('bilal', seq))
result = server.eval(expr, search_keys=[])
seq_code = result[0]['code']

expr = ("@SOBJECT(%s/scn['name','%s']['s_status', 'is', 'NULL'])" % ('bilal', scn))
expr = ("@SOBJECT(%s/scn['name','%s']['seq_code','%s']['s_status', 'is', 'NULL'])" % ('bilal', scn, seq_code))
result = server.eval(expr, search_keys=[])
scn_code = result[0]['code']

expr = ("@SOBJECT(%s/shot['name','%s']['scn_code','%s']['seq_code','%s']['s_status', 'is', 'NULL'])" % ('vfx', shot, scn_code, seq_code))
result = server.eval(expr, search_keys=[])
shot_code = result[0]['code']
search_code = shot_code

filters = []
filters.append(("project_code", 'bilal'))
filters.append(("search_code", search_code))
filters.append(("process", process))
filters.append(("context", context))
tasks = server.query("sthpw/task", filters=filters)

search_key = tasks[0]['__search_key__']

#expr = ("@SOBJECT(%s/seq['name','%s']['s_status', 'is', 'NULL'])" % ('bilal', 'seq30'))
#result = server.eval(expr, search_keys=[])                                             
#file_path = "/home/abhishek/Downloads/8b45c11d06e232b2e3a0b2de32d89719.jpg"            
#search_key="sthpw/task?code=TASK00040625"                                             
#context='lighting'                                                                     

cmp_dir = '{project.code}/sequences/%s/%s/{parent.name}_{parent.code}/{process[0]}/compositing/{context[1]}' % (seq, scn) 
light_dir = '{project.code}/sequences/%s/%s/{parent.name}_{parent.code}/{process[0]}/lighting/scenes/{context[1]}' % (seq, scn)
exr_dir = '{project.code}/sequences/%s/%s/{parent.name}_{parent.code}/{process[0]}/compositing/images/{context[1]}' % (seq, scn)

if type == 'exr':
    pattern = '/nas/projects/Tactic/sandbox/bilal/abhishek/asset/images/v035/{0}_{1}_{2}_{3}_{4}_{5}.%0.4d.{6}'.format(seq, scn, shot, elem, process, ver, type) 
    dir = exr_dir
    snapshot = server.group_checkin(search_key, context, pattern, '1001-1120', description="test image checkin", mode=mode, snapshot_type='sequence', file_type='exr')
elif context == 'lighting':
    dir = light_dir
    desc='foo bar checkin'                                                                 
    #snapshot = server.simple_checkin(search_key, context, pub_file, description=desc, mode=mode)
    snapshot = server.create_snapshot(search_key, context, description=desc)
    snapshot_code = snapshot['code']
    snapshot = server.add_file(snapshot_code, pub_file, file_type='nuke', mode=mode, dir_naming=dir)
elif context == 'compositing':
    dir = cmp_dir
    desc='foo bar checkin'                                                                 
    #snapshot = server.simple_checkin(search_key, context, pub_file, description=desc, mode=mode)
    snapshot = server.create_snapshot(search_key, context, description=desc)
    snapshot_code = snapshot['code']
    snapshot = server.add_file(snapshot_code, pub_file, file_type='nuke', mode=mode, dir_naming=dir)
        
print snapshot.get('snapshot')

#file_path = "/home/abhishek/Downloads/8b45c11d06e232b2e3a0b2de32d89719.jpg"


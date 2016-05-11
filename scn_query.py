#!/usr/bin/env python

import sys,os
sys.path.append("/nas/projects/development/productionTools/assetPublisher/tactic_modules")
import queryClass as qClass

u = qClass.queryClass("bjTactic", "bilal")

#(seq_arg, scn_arg, shot_arg) = sys.argv[1:].split("_")

seq_arg = sys.argv[1]
seq_obj = u.getSeqSObjectbyName(seq_arg)
scn_obj = u.server.query("bilal/scn", filters=[("seq_code", seq_obj[0]['code'])])
#scn_name = u.getScnSObjectbyNameAndSeqCode(scn_obj[0]['name'], seq_obj[0]['code'])
seq_code = seq_obj[0]['code']
seq = seq_obj[0]['name']
scn = scn_obj[0]['name']

path = "/nas/projects/Tactic/bilal/sequences/"
no_cloth_sim_scenes = []
no_hair_sim_scenes = []
cloth_sim_scenes = []
hair_sim_scenes = []
for sh in u.getShtSObjectbyName(seq_code, scn_obj[0]['code']):
    shot_name = sh['name']
    shot = '{0}_{1}'.format(sh['name'], sh['code'])

    cloth_sim_path = '{0}/{1}/{2}/{3}/clothSim/clothSim/scenes'.format(path, seq, scn, shot)
    _path = '{0}_{1}_{2}'.format(seq, scn, shot_name)
    if os.path.exists(cloth_sim_path) is False:
        #print cloth_sim_path
        no_cloth_sim_scenes.append(_path)
    else:
        cloth_sim_scenes.append(_path)    

    hair_sim_path = '{0}/{1}/{2}/{3}/hairSim/hairSim/scenes'.format(path, seq, scn, shot)
    if os.path.exists(hair_sim_path) is False:    
        #print hair_sim_path
        no_hair_sim_scenes.append(_path)
    else:
        hair_sim_scenes.append(_path)    
 
#print cloth_sim_scenes
#print hair_sim_path_scenes    
print "ClothSim items: " 
for item in no_cloth_sim_scenes:
    print item, "maya cloth and hair setup files missing"

print "\n"
for item in cloth_sim_scenes:
    print item, "approved"    

print "\nHairSim items: " 
for item in no_hair_sim_scenes:
    print item, "maya cloth and hair setup files missing"

print "\n"
for item in hair_sim_scenes:
    print item, "approved"    


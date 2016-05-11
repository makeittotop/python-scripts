#!/usr/bin/env python

from pymel.core import *
def gen():
    txFiles = ls(type='file')
    abcs = ls(type='bs_alembicNode')
    refs = ls(type='reference')
    ASSs = ls(type='aiStandIn')
    dynGlobals = ls(type='dynGlobals')
    
    deps = []
    
    # appending scene name:
    deps.append('%s'%sceneName()+'\n')
    
    # processing refs:
    for ref in refs:
        try:
            deps.append(referenceQuery(ref, f=True)+'\n')
        except:
            print ("Warning: scene has unknow ref nodes that doesn't relate to files")
    
    # processing texutres:
    '''
    TODO: Add support for image texture sequence
    '''
    for tx in txFiles:
        tmpName = '%s'%getAttr('%s.fileTextureName'%tx)
        tmpName = tmpName.replace('//', '/')
        tmpName = tmpName.replace('///', '/')
        tmpName = tmpName.replace('////', '/')
        tmpName = tmpName.replace('.tiff', '.tx')
        tmpName = tmpName.replace('.tif', '.tx')
        tmpName = tmpName.replace('.tga', '.tx')
        tmpName = tmpName.replace('.jpg', '.tx')
        tmpName = tmpName.replace('.png', '.tx')
        tmpName = tmpName.replace('.hdr', '.tx')
        tmpName = tmpName.replace('.exr', '.tx')
        tmpName = tmpName.replace('<udim>', '*')
        
        deps.append(tmpName+'\n')
    
    # processing alembics:
    for abc in abcs:
        tmpName = getAttr('%s.abc_File'%abc)+'\n'
        tmpName = tmpName.replace('//', '/')
        tmpName = tmpName.replace('///', '/')
        tmpName = tmpName.replace('////', '/')
        deps.append(tmpName)
    
    # processing ASSs:
    for ass in ASSs:
        tmpAss = getAttr('%s.dso'%ass)
        tmpAss = tmpAss.replace('#', '*')
        tmpAss = tmpAss.replace('//', '/')
        tmpAss = tmpAss.replace('///', '/')
        tmpAss = tmpAss.replace('////', '/')
        deps.append(tmpAss+'\n')
        
    # processing particle caches:
    for dyn in dynGlobals:
        deps.append(getAttr('%s.cacheDirectory'%dyn)+'\n')
        
    # processing Yeti caches:
    yetiShapes = ls(type='pgYetiMaya')
    for yeti in yetiShapes:
        yetiCache = getAttr('%s.cacheFileName'%yeti)
        if yetiCache:
            yetiCache = yetiCache.replace('%04d', '*') + '\n'
            deps.append(yetiCache)

    # cleaning up deps by removing duplicates
    deps = list(set(deps))
    
    depsFile = '/nas/projects/Tactic/bilal/render/.depsTemp/%s_filtered.lst'%os.path.basename(sceneName())
    resultFile = depsFile
    
    depsFile = open(depsFile,'w')
    depsFile.writelines(deps)
    depsFile.close()
    
    print '\n\n#################################################################'
    print '####               SCENE DEPENDENCIES FOUND                 #####'
    print '#################################################################'
    for dep in deps:
        print dep[:-1]
    print '#################################################################'
    print 'Deps file generated successfully.'
    print 'file: %s'%resultFile
    
    return (resultFile, deps)

    '''
    deps = []
    
    for dep in depsList:
        deps.append(dep[:-1])
    
    cleanDeps = list(set(deps))
    
    cpList=''
    print '--------------------------------------------------------'
    print 'These scene dependencies will be uploaded to vendor nas:'
    print 'Note: deps coming from "asset" will not be uploaded'
    print '      To upload them, please request that from Admin'
    print 'Evaluating from lst file: %s'%filteredFile
    print '--------------------------------------------------------'
    for dep in cleanDeps:
        print dep
        cpList = cpList + dep + ' '
    print '--------------------------------------------------------'
    
    # eval the ascp command:
    print     'ascp -P 33001 -O 33001 -l 15M -p --overwrite=diff -d --src-base=/nas/projects %s render@113.107.235.11:/'%cpList
    os.system('ascp -P 33001 -O 33001 -l 15M -p --overwrite=diff -d --src-base=/nas/projects %s render@113.107.235.11:/'%cpList)
    '''

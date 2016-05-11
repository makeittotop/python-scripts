def get_ascp_cmd(sync_list):
    return 'ascp -P 33001 -O 33001 -k 3 -p --overwrite=diff -d --src-base=/nas/projects {0} render@113.107.235.11:/'.format(sync_list)

def get_tractor_spool_cmd(alf_script, spool_dry_run=False):
    if spool_dry_run:
        return '/opt/pixar/Tractor-2.0/bin/tractor-spool --engine=fox:1503 --priority=50 --print-alfscript {0}'.format(alf_script)
    else:
        return '/opt/pixar/Tractor-2.0/bin/tractor-spool --engine=fox:1503 --priority=50 {0}'.format(alf_script)

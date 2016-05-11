#!/usr/bin/env python

import sys

# amazon web services api
import boto
from boto.glacier.exceptions import UnexpectedHTTPResponseError

AWS_ACCESS_KEY_ID='AKIAIVZLHF74OTT3U4EA'
AWS_SECRET_ACCESS_KEY='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'

def main():
    upload_file = '/home/abhishek/vagrant_box/essential_commands_bak'
    vault_name = 'my_backups'

    layer2_glacier_obj = boto.connect_glacier(region_name='us-west-2', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    # List all vaults belonging to a user
    my_vaults = layer2_glacier_obj.list_vaults()
	# Get a particular vault
    my_vault = layer2_glacier_obj.get_vault(vault_name)

    '''
	glacier_connection = boto.connect_glacier(aws_access_key_id=ACCESS_KEY_ID,                                                                                
	                                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)                                                                          
	glacier_connection.create_vault("myvault") 

	# Layer1

	layer1_glacier_obj = boto.glacier.layer1.Layer1(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-west-2')
	layer1_glacier_obj.list_vaults()

	archive_id = my_vault.upload_archive("/home/abhishek/vagrant_box/essential_commands", "lots of essential commands, api etc for linux, python, ruby etc")
	retrieve_job = my_vault.retrieve_archive(archive_id)

    retrieve_job.download_to_file("/tmp/foo")
    ''' 

    # Asynchronous upload to glacier via a `vault` object
    upload_id = my_vault.create_archive_from_file(filename=upload_file, description="lots of essential commands, api etc for linux, python, ruby etc")
    print >>sys.stderr, "File {0} successfully uploaded to glacer in vault {1}!".format(upload_file, vault_name)

    # List all current running jobs - upload / download
    print >>sys.stderr, my_vault.list_jobs()

    try:
        # Get info about a particular job
        my_vault.get_job(upload_id)
    except UnexpectedHTTPResponseError as e:
    	print >>sys.stderr, e.message

    
main()
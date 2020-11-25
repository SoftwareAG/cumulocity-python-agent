import configparser
from os import path
import logging
import os
import API.inventory
import API.authentication as auth
import subprocess

logger = logging.getLogger('Settings')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for settings was initialised')

def basics():
    logger.info('Basic function was called')
    configInit = configparser.ConfigParser(interpolation=None)
    configInit.read('./config/config.ini')
    basics = {}
    basics['tenantInstance'] = configInit['C8Y']['tenantInstance']
    basics['registrationUser'] = configInit['Registration']['user']
    basics['registrationPassword'] = configInit['Registration']['password']
    basics['registrationTenant'] = configInit['Registration']['tenant']
    try:
        basics['deviceID'] = subprocess.Popen(["cat", "/etc/hostname"],stdout=subprocess.PIPE).stdout.read().decode('utf-8').replace('\n','')
    except:
        logger.warning('Could not get hostname, using backup device ID')
        basics['deviceID'] = "Backup_0815"
    basics['tenantPostFix'] = configInit['Registration']['tenantPostFix']
    return basics

def credentials():
    logger.info('Credentials function was called, checking if file exists')
    if path.exists('./config/credentials.key'):
        logger.info('Credential key file exists')
        configCredentials = configparser.ConfigParser(interpolation=None)
        configCredentials.read('./config/credentials.key')
        logger.info('Key file was read')
        credentials = {}
        credentials['c8yUser'] = configCredentials['Credentials']['Username']
        logger.debug('Following user was found in key file: ' + str(credentials['c8yUser']))
        credentials['tenantID'] = configCredentials['Credentials']['tenantID']
        logger.debug('Following user was found in key file: ' + str(credentials['tenantID']))
        credentials['c8yPassword'] = configCredentials['Credentials']['Password']
        return credentials
    else:
        print("No file")

def device():
    device ={}
    try:
        managedDeviceObject = API.inventory.getSpezificManagedObject(auth.get().internalID)['c8y_Configuration']['config'].replace('\n','').split(';')
        for counter, value in enumerate(managedDeviceObject):
            if len(value) > 0:
                device[str(value.split('=')[0])] = value.split('=')[1]
            else:
                pass
        return device
    except Exception as e:
        logger.error('The following error occured: %s'% (str(e)))
        return device

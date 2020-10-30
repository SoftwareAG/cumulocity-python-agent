import API.authentication as auth
import logging
import requests
import json
import API.inventory
from API.device_proxy import DeviceProxy, WebSocketFailureException
import sys
import os
import utils.settings
import deviceControl.configurationUpdate
import API.operations
from random import randint
import time
import random

logger = logging.getLogger('OperationHandler')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for handling operations was initialised')

def start(internalID, operation):
    logger.debug('Getting the managedObject to check the Supported Operations')
    operationID = operation['id']
    operationClassification(operation, operationID)

def operationClassification(operation, operationID):
    if 'c8y_Restart' in str(operation):
        logger.info('Found c8y_Restart operation')
        time.sleep(randint(0,2))
        API.operations.setOperationMode(operationID, 'EXECUTING')
        time.sleep(randint(0,5))
        choice=random.choice(['SUCCESSFUL','FAILED'])
        API.operations.setOperationMode(operationID, choice)
    elif 'c8y_Configuration' in str(operation):
        logger.info('Found c8y_Configuration operation')
        try:
            deviceControl.configurationUpdate.start(operation, operationID)
            API.operations.setOperationMode(operationID, 'SUCCESSFUL')
        except Exception as e:
            logger.error('The following error occured: %s'%(str(e)))
            API.operations.setOperationMode(operationID, 'FAILED')
    elif 'c8y_Software' in str(operation):
        logger.info('Found c8y_Software operation')
        time.sleep(randint(0,2))
        API.operations.setOperationMode(operationID, 'EXECUTING')
        time.sleep(randint(0,5))
        choice=random.choice(['SUCCESSFUL','FAILED'])
        logger.debug('Choice is %s'%(str(choice)))
        API.operations.setOperationMode(operationID, choice)
    elif 'c8y_Firmware' in str(operation):
        logger.info('Found c8y_Firmware operation')
        time.sleep(randint(0,2))
        API.operations.setOperationMode(operationID, 'EXECUTING')
        time.sleep(randint(0,5))
        choice=random.choice(['SUCCESSFUL','FAILED'])
        logger.debug('Choice is %s'%(str(choice)))
        API.operations.setOperationMode(operationID, choice)
    elif 'c8y_Command' in str(operation):
        logger.info('Found c8y_Command operation')
        API.operations.setOperationMode(operationID, 'EXECUTING')
        time.sleep(randint(0,5))
        choice=random.choice(['SUCCESSFUL','FAILED'])
        API.operations.setOperationMode(operationID, choice)
    elif 'c8y_RemoteAccessConnect' in str(operation):
        logger.info('Found c8y_RemoteAccessConnect operation')
        API.operations.setOperationMode(operationID, 'EXECUTING')
        connect = operation['c8y_RemoteAccessConnect']
        device_proxy = DeviceProxy(connect['hostname'], connect['port'], None, connect['connectionKey'], auth.get().tenantInstance, auth.get().tenantID, utils.settings.credentials()['c8yUser'],utils.settings.credentials()['c8yPassword'], None)
        try:
            device_proxy.connect()
            API.operations.setOperationMode(operationID, 'SUCCESSFUL')
        except Exception as e:
            logger.error('The following error occured: %s'%(str(e)))
            API.operations.setOperationMode(operationID, 'FAILED')
    else:
        logger.warning('Unknown operation type')

import sys
import logging
from os import path
from os import remove
import requests
import deviceRegistration.registrationProcess
import API.authentication as auth
import deviceControl.operationsWatcher
import API.identity
import time
import threading
import utils
import utils.threadCommunication as communication
import deviceStatus.sendDeviceStats



logger = logging.getLogger('deviceAgent')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for deviceAgent was initialised')

def checkUsabilityCredentials():
    logger.info('Cecking if available credentials work')
    url = "https://%s/user/currentUser"%(auth.get().tenant)
    logger.debug('Requesting the following url: ' + str(url))
    response = requests.request("GET", url, headers=auth.get().headers)
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        logger.info('Credentials valid')
        return True
    else:
        logger.info('Deleting Credential File')
        remove("./config/credentials.key")
        return False

def start():
    logger.info('Checking for credentials')
    if not path.exists('./config/credentials.key'):
        logger.info('No credentials found, starting registration')
        deviceRegistration.registrationProcess.start()
    logger.info('Credentials available')
    if not checkUsabilityCredentials():
        sys.exit(1)
    logger.info('Starting checking of existing device')
    if API.identity.getInternalID(utils.settings.basics()['deviceID']) is False:
        logger.info('No device found in c8y, starting edge device creation.')
        deviceRegistration.newDeviceRegistration.createEdgeDevice(utils.settings.basics()['deviceID'])
    auth.get().internalID = API.identity.getInternalID(utils.settings.basics()['deviceID'])
    utils.settings.device()
    logger.info('Finishing start sequency')

def operation():
    logger.info('Starting operationsWatcher')
    threadOperatiosnWatcher = threading.Thread(target=deviceControl.operationsWatcher.start, daemon=True)
    threadOperatiosnWatcher.start()
    return threadOperatiosnWatcher

def deviceStatsStatus():
    logger.info('Starting Device Status')
    threadDeviceStatus = threading.Thread(target=deviceStatus.sendDeviceStats.start, daemon=True)
    threadDeviceStatus.start()
    return threadDeviceStatus

if __name__== "__main__":
    try:
        start()
        statusDevice = deviceStatsStatus()
        statusOperation = operation()
        while True:
            time.sleep(1)
            print("Heartbeat")
            if statusOperation.is_alive() is False:
                logger.error('Listener on operations not alive, restarting')
                time.sleep(5)
                statusOperation = operation()
            elif statusDevice.is_alive() is False:
                logger.error('Status on device update not alive, restarting')
                time.sleep(5)
                statusDevice = deviceStatsStatus()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        logger.error('The following error occured: ' + str(e))
        raise

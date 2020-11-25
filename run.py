import sys
import logging
from os import path
from os import remove
import requests
import deviceRegistration.registrationProcess
import API.authentication as auth
import deviceControl.operationsListener
import API.identity
import time
import threading
import utils
import utils.threadCommunication as communication
import deviceStatus.sendDeviceStats
import deviceControl.smartRest


logger = logging.getLogger('deviceAgent')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for deviceAgent was initialised')

def start():
    logger.info('Checking for credentials')
    if not path.exists('./config/credentials.key'):
        logger.info('No credentials found, starting registration')
        deviceRegistration.registrationProcess.start()
    logger.info('Credentials available')
    logger.info('Starting checking of existing device')
    if API.identity.getInternalID(utils.settings.basics()['deviceID']) is False:
        logger.info('No device found in c8y, starting edge device creation.')
        deviceRegistration.newDeviceRegistration.createEdgeDevice(utils.settings.basics()['deviceID'])
    auth.get().internalID = API.identity.getInternalID(utils.settings.basics()['deviceID'])
    utils.settings.device()
    deviceControl.smartRest.checkSmartRestTemplateExists()
    logger.info('Finishing start sequency')

def operation():
    logger.info('Starting operationsWatcher')
    threadOperatiosnWatcher = threading.Thread(target=deviceControl.operationsListener.start, daemon=True)
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

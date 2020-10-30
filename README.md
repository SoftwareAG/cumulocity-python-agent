# Python-Agent
A cumulocity Agent in Python containing the basic functionalities.


Cumulocity is an IoT platform that enables rapid connections of many, many different devices and applications. It allows you to monitor and respond to IoT data in real time and to spin up this capability in minutes. More information on Cumulocity IoT and how to start a free trial can be found [here](https://www.softwareag.cloud/site/product/cumulocity-iot.html#/).

Cumulocity IoT enables companies to to quickly and easily implement smart IoT solutions.

![Dashboard](pics/Dashboard.png)

______________________
For more information you can Ask a Question in the [TECHcommunity Forums](http://tech.forums.softwareag.com/techjforum/forums/list.page?product=webmethods-io-b2b).

You can find additional information in the [Software AG TECHcommunity](http://techcommunity.softwareag.com/home/-/product/name/webmethods-io-b2b).
______________________

These tools are provided as-is and without warranty or support. They do not constitute part of the Software AG product suite. Users are free to use, fork and modify them, subject to the license agreement. While Software AG welcomes contributions, we cannot guarantee to include every contribution in the master project.

Contact us at [TECHcommunity](mailto:technologycommunity@softwareag.com?subject=Github/SoftwareAG) if you have any questions.

## Getting Started

Getting stated is much easier on linux than on windows. For developement we used a Cent OS system but this bascially works on any machine that can run python.


### Start

Before run the first time install the requirements via pip:

```shell
pip install -r requirements.txt
```

After that you can run the script via:

```shell
python run.py
```

### Device Registration

On Cumulocity side you have to register the device in your tenant. In the config.ini you have to use an identifier such as the serial number or mac address.
This serial number will be used for the registration purpose.

![Devie Registration](https://recordit.co/NbNj1VdQu4.gif)

### Change Configuration

Configurations can be changed on the device. Most devices support a text-based system configuration file that can be presented and edited using this procedure. In the inventory, “c8y_Configuration” represents the currently active configuration on the device. As part of an operation, “c8y_Configuration” requests the device to switch the transmitted configuration to the currently active one.

![Monitor Update](https://recordit.co/9Eukt7VH5E.gif)

## Device-Agent

Basically theses tasks are handled in different modules:

1. Registration of the device and handling of the credential file as well as device creation -> (deviceRegistration)
2. Basic RestAPI capabilities -> (API)
3. Capability to get operations from the platform -> (deviceControl)

Debugger is set to Info in every module, this makes debugging a lot easier. Change if you want.

### API

Required and most commonly used RestAPI calls are modulized inside here. The naming of the modules is mainly derived from its API path such as e.g. alarm, event, measurement or Inventory. The authentification module is initialized at the very beginning of every module an uses the 'credentials.key' file in the config directory. If not available the device Registration starts. If the credentials are not valid they will be deleted. Every API module has its own logger.

### deviceControl

Device control handles everything around operations handling from the platform to the device.
There are two main modules:

1. operationsWatcher -> Watches for operations on the particualar device and hands them over to the handler
2. operationsHandler -> Handles the logic of the operations and hands them over to dedicated modules

Dedicated modules in this context are e.g. the update of configuration with updating the managed object or the exchange of files on the local machine for e.g. epl files. Others can be added for later use-cases.

### deviceRegistration

The device registration is implemented and documented here:

[Device Registration using Rest](https://cumulocity.com/guides/device-sdk/rest/)

After the registration process it is checked whether an managed object with particular identity is already available. If not a new device is created. The layout of the device can be changed in device.txt in the config directory.

### deviceStatus

### Remote Access

[Remote Access](https://github.com/SoftwareAG/cumulocity-remote-access-agent)

### utils


### deviceStatus

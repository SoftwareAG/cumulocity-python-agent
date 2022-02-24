# Python-Agent
A cumulocity Agent in Python containing the basic functionalities.


Cumulocity is an IoT platform that enables rapid connections of many, many different devices and applications. It allows you to monitor and respond to IoT data in real time and to spin up this capability in minutes. More information on Cumulocity IoT and how to start a free trial can be found [here](https://www.softwareag.cloud/site/product/cumulocity-iot.html#/).

Cumulocity IoT enables companies to to quickly and easily implement smart IoT solutions.

![Dashboard](pics/Dashboard.png)

______________________
For more information you can Ask a Question in the [TECHcommunity Forums](https://tech.forums.softwareag.com/tags/c/forum/1/Cumulocity-IoT).

You can find additional information in the [Software AG TECHcommunity](https://tech.forums.softwareag.com/tag/Cumulocity-IoT).
______________________

These tools are provided as-is and without warranty or support. They do not constitute part of the Software AG product suite. Users are free to use, fork and modify them, subject to the license agreement. While Software AG welcomes contributions, we cannot guarantee to include every contribution in the master project.

Contact us at [TECHcommunity](mailto:technologycommunity@softwareag.com?subject=Github/SoftwareAG) if you have any questions.

## Getting Started

Getting stated is much easier on linux than on windows. For developement we used a Cent OS system but this bascially works on any machine that can run python.
Install Python 2 or Python3 if not already installed. This module has been tested with Python3.

### Start

Before run the first time install the requirements via pip:

```shell
pip install -r requirements.txt
```

After that you can run the script via:

```shell
python run.py
```

Docker is also available. So basically

```shell
docker build .
```

or use the start.sh script together with the numbers of instances you want to use

```shell
. start.sh 5
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

Required and most commonly used RestAPI calls are modulized inside here. The naming of the modules is mainly derived from its API path such as e.g. alarm, event, measurement or Inventory. The authentification module is initialized at the very beginning of every module and uses the 'credentials.key' file in the config directory. If not available the device Registration starts. If the credentials are not valid they will be deleted. Every API module has its own logger.

### deviceControl

Device control handles everything around operations handling from the platform to the device.
There are two main modules:

1. operationsListener -> Watches for operations on the particualar device via MQTT and triggers the handler
2. operationsHandler -> Handles the logic of the operations and hands them over to dedicated modules

Dedicated modules in this context are e.g. the update of configuration with updating the managed object or starts the remote access process from device. Others can be added for later use-cases.

### deviceRegistration

The device registration is implemented and documented here:

[Device Registration using Rest](https://cumulocity.com/guides/device-sdk/rest/)

After the registration process it is checked whether an managed object with particular identity is already available. If not a new device is created. The layout of the device can be changed in device.txt in the config directory.

### Remote Access

To provide the best level of control, remote devices should be represented as devices in the Device Management of Cumulocity IoT, with the corresponding reporting, remote control and real-time functionality.

In some cases however, it is not possible or not economic to implement every aspect of a machine or remote device in a Cumulocity IoT agent. For example, it might be a legacy device that does not have APIs for accessing certain parts of the functionality, or it may have many very low-level configuration parameters that would be very involved to map to Cumulocity IoT.

In this case, you can use Cloud Remote Access to securely manage remote devices. The benefit is that you manage the device in the same way as if you had it physically close to you.

See the repository of S.Witschel here on how its implemented technically:

[Remote Access](https://github.com/SoftwareAG/cumulocity-remote-access-agent)

For achieving a connection via SSH or VNC simple configure the connection where the device of the agent is the jump host. Meaning you can reach every ssh endpoint or VNC server from there could be used within the platform.

# Acqua - Data Acquisition and Processing unit

![https://deeemm.com/images/acqua.png](https://deeemm.com/images/acqua.png)


Acqua is a simple extensible data acquisition controller that can also perform time and event based control functions. Acqua uses pre-configured signal processing 'nodes' connected via I2C to provide clean formatted and filtered data to the main controller which can then be easily logged or processed.

## Overview

The Acqua project is based on the Raspberry pi and Arduino nano. The Raspberry Pi acts as the main Acqua controller and runs a flask based web application server that can be accessed via network connection. All control, configuration and monitoring functions are accessible via the browser allowing the Raspberry Pi to be deployed headless. 

External devices are connected via the I2C network and are known as 'nodes'. A Node is essentially an intelligent data interface made from an Arduino Nano. Arduino Nano's are cheap, accessible, relatively low power and easy to program. They therefore provide the perfect platform for undertaking simple data acquisition, data manipulation and control. Arduino Nanos are easy to integrate into existing equipment, both due to thier small footprint but also due to the quantity and variety of available I/O and communication protocols and control schemas. 

Data is read from Nodes, and where supported, control actions can be written to Nodes via a simple serial API. In some cases Nodes can also carry out control actions autonomously. One such example is a heated sensor, where the heater control and regulation is carried out entirely on the Nano. In this case the heat setpoint is sent to the Nano via the Serial API and stored in the NVM on the Nano. This decentralises control tasks which in turn simplifies them. It also reduces overheads on the Acqua controller which increases scalability. Any Arduino device can be used as a node as can any other device that can communcate via I2C using the Node API protocol.

All Nodes run standard code and the capabilities of each Node are enabled and defined within their configuration files at compile time. Further actions may also be configurable at run time via the API on some Node types. A complete list of available Node types along with configuration information can be found in the Github repository.

## Control Actions

Once the Node has been added to Acqua, you can then associate control actions with it. A control action is a user defined task that is initiated by a time or event based trigger. These actions can be system based, for example sending a notification email or logging a value, or they can be Node based, for example enabling an output or changing a setpoint. Control actions can also be joined using logical operators which allows complex control schemas to be created. The Acqua system is also easily extensible by the end user with the creation of custom Node code if required.

# Basic Specs

## Main Rpi functions
- Web app server to serve main control interface - accessible via users browser
- Programmable timers (using cron)
- Conditional control engine - if-this-then-that
- Device (node) configuration - name / node type (sets api requirements) / polling frequency / watchdog (+frequency) / data logged? / 
- GPIO configuration
- Data logging inc manual data entry for test results
- Alerts

## Basic I2C protocol

- Communication between the master(RPi) and slave(Arduino Nano) devices is by simple state interrogation > response protocol. 
- RPi can poll nodes to check if they are still alive
- RPi can interrogate node to obtain device capabilities
- RPi can interrogate nodes and obtain data
- Rpi can send control commands to nodes to configure them (configuration stored in flash memory)
- RPi can send control commands to nodes to perform control actions where they are available

Note: Nodes are slave devices however they could also can act as master to other slaves on the I2C network as I2C supports multiple masters. Not really sure of a use case where this may be needed (synchronised wave-makers?) will explore later.

## I/O data types
- Digital input
- Digital output
- Analog Input
- Analog output
- PWM output
- Data Node
  - Analytical probe (PH / ORP / RH / Temp / Whatever) - returns a scaled integer value
  - PWM controller (Direct control / Auto Cyclic Control / setpoint (PID) control)
  - Display driver (LED / LCD / OLED display / touchscreen driver)
  - Digital Input Status (Polled)
  - Digital Output Control
  - Analog Input Status (Polled)
  - Analog Output Control

Note: Data scaling of I/O from Data node needs to match in both node + RPi. This can be achieved by having predefined data types in the Rpi and boiler plate code in the nano that is selectable via the API (restrictive), or simply from user input in RPi I/O set up and hard coding in Nano (unrestricted). All cases will potentially require user to flash nano.

My preference would be for the system to be unrestricted as then the user is not reliant on the devs to perform integration of new devices, however this does increase complexity of system.

There is also possibility of multiple data channels per data node as each Nano has multiple I/O. This may result in a network topology with one nano controlling the 'top of tank' devices and one controlling the sump devices. The RPi acting as the data sequencer and reporting interface. This topology could also be extended to use other Arduino devices such as the Mega 2560 which has many more inputs.

There are a considerable number of nano shields already available that can be utilised. For example:
- PWM/H-bridge motor shields 2 chan up to 16A - easily enough to drive skimmer and return pump
- Screw terminal breakout boards
- Stepper motor shields
- Display shields
- Relay Shields (typically 4 channel)

Then there are proprietary I2C systems such as Qwiic by sparkfun which provide a plug-and-play kind of set up and includes a large variety of sensors which might suit the technology adverse amongst us.


## Web interface

The web interface provides a dynamic layout that provides a way for the user to analyse recorded trends and control connected equipment. It also makes provision for the user to manually enter recorded data - for instance parameter test data.

The admin navigation is broken up into the basic functions

- Configuration
- I/O Configuration
- Node configuration
- Communications
- Macros
 - Conditional control
 - Time based control
- Trend data

All configuration is accessed from a single administration menu. There is also a dynamically generated top level user menu, where items are added based on the configuration settings chosen by the user (There is a display in menu check box on each sensor item). In this manner both the name and layout can be configured by the end user, which means that the system can be dedicated to each application.

So in the case of an Aquarium controller you might have the following top level menu items and associated macros...

- Heater - conditional control - if temp less than setpoint  
- Light - time based control - light on 9:pm + light off 9 am  
- ATC - conditional control - if float switch then ATC on  
- Doser - time based control - Doser on 4 secs speed 4 at 9 pm / doser run for 1 sec speed 1 every 25 minutes  
- Feeder - time based control - feeder operate 9am every day  
- Wavemaker - time based control - 25% for 3 secs 100% for 3 secs  
- Return pump - conditional control - if feeding mode on return pump 15%  
- Skimmer pump - conditional control - if feeding mode on skimmer pump off  
  
It should also be noted that with each item it is also possible to enable data logging. This way historical trend data can be recorded. Logged data is displayed in a trend graph and can also be analysed in a dedicated trend analysis page which can display multiple traces on the same graph. Very useful for analysing how different system elements interact or impact each other.


## Data logging

Basic time based data logging is achieved by utilising the CRON capabilities of the RPi. It should also be possible to undertake conditional logging where logging is triggered by macro conditions - if-this-then-log-that - i.e. if PH less than 8 record temp 

- Data log format SQL
- Data logs should be downloadable
- Data log management needs to be implemented (max size / SD support / external HDD / remote FTP)


## Program structure

- Simple cyclic scanning of enabled conditional and time based macros.
- Execution of code at appropriate time / under appropriate conditions / as called by CRON
- Web interface instigated by URL calls as accessed by user.

- Nodes run cyclical program as appropriate for use.
- All nodes could share same general code with all basic functions included. Functions are then enabled by API.
- For more complex implementations custom nano code can be used. 

Basic API interrogation for sensor value should be aligned with magnitude of value. All values returned are integers that are then divided by an appropriate operand as defined by the user when they set the sensor units. For example a value of 400 could simply mean 400A. But it could also mean 400mA when the divisor is set to 1000. 

so values recorded for each sensor are:

- Name
- Description
- Units
- Divisor
- Enable Logging
- Show in Menu
- Source

A unique UID is also set for each unit which then allows SQL join operations across tables for data logging and data analysis. 


## Contributing

If you would like to get involved with the project, or wish to get in touch, you can contact me via email or catch me on the Acqua Discord Channel:

Email: deeemm@deeemm.com  
Discord: [https://discord.gg/3kXX4f4](https://discord.gg/3kXX4f4)

Please note that at this stage support is limited to active contributors only. Beta testing will be announced at a later date.
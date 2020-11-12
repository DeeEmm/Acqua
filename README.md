# Acqua - Data Acquisition and Processing unit

![https://deeemm.com/images/acqua.png](https://deeemm.com/images/acqua.png)


Acqua is a simple extensible data acquisition controller that can also perform time and event based control functions. Acqua uses pre-configured signal processing 'nodes' connected via dedicated network to provide clean formatted and filtered data to the main controller which can then be easily logged or processed.

The project combines the strengths of both the Raspberry Pi and Arduino to produce a very capable programmable data-logging controller


## Overview

The Acqua project is based on the Raspberry pi and Arduino nano. The Raspberry Pi acts as the main Acqua controller and runs a flask based web application server that can be accessed via network connection. All control, configuration and monitoring functions are accessible via the browser allowing the Raspberry Pi to be deployed headless. 

External devices are connected via the I2C network and are known as 'nodes'. A Node is essentially an intelligent data interface made from an Arduino Nano. Arduino Nano's are cheap, accessible, relatively low power and easy to program. They therefore provide the perfect platform for undertaking simple data acquisition, data manipulation and control. Arduino Nanos are easy to integrate into existing equipment, both due to their small footprint but also due to the quantity and variety of available I/O, communication protocols and control schemas. 

Data is read from the Nodes, and where supported, control actions can be written to the Nodes via a simple serial API. In some cases Nodes can also carry out control actions autonomously. One such example is a heated sensor, where the heater control and regulation is carried out entirely on the Nano. In this case the heat setpoint is sent to the Nano via the Serial API and stored in the NVM on the Nano. This decentralises control tasks which in turn simplifies them. It also reduces overheads on the Acqua controller which increases scalability. Any Arduino device can be used as a node and each node can have multiple data points. There is no limitation what kind of device can be connected to a node as long as it produces a trend-able output.

All Nodes run standard code and the capabilities of each Node are enabled and defined within their configuration files at compile time. Further actions may also be configurable at run time via the API on some Node types. A complete list of available Node types along with configuration information can be found in the Github repository. This list is growing and user contributions are welcomed. 


## Project Goal

The main aim of the project is to develop a simple, extensible, easily deployed, remote controlled data logging system that is also capable of simple control tasks.


## Control Actions

Once a Node has been added to Acqua, you can then associate control actions with it. A control action is a user defined task that is initiated by a time or event based trigger. These actions can be system based, for example sending a notification email or logging a value, or they can be Node based, for example enabling an output or changing a setpoint. Control actions can also be joined using logical operators which allows complex control schemas to be created. The Acqua system is also easily extensible by the end user with the creation of custom Node code if required. 

# Basic Specifications

## Main Raspberry Pi functions
- Web app server to serve main control interface - accessible via the users browser
- Programmable timers (using cron)
- Conditional control engine - if-this-then-that
- Device (node) configuration - name / node type (sets api requirements) / polling frequency / watchdog (+frequency) / data logged? / etc
- GPIO configuration for simple local control
- Data logging inc manual data entry for test results
- Alerts

## Basic Acqua Node protocol
- Communication between the master(RPi) and slave(Arduino Nano) devices is by simple state interrogation > response protocol across a dedicated I2C network. 
- RPi can poll nodes to check if they are still alive
- RPi can interrogate node to obtain device capabilities
- RPi can interrogate nodes and obtain data
- Rpi can send control commands to nodes to configure them (configuration stored in flash memory)
- RPi can send control commands to nodes to perform control actions where they are available
- Note regular I2C devices need to be connected to a node as no provision is made on the Node network for direct communication of I2C devices.

## I/O data types
- Digital input
- Digital output
- Analog Input
- Analog output
- PWM output
- Data Nodes
  - Analytical probe (PH / ORP / RH / Temp / Whatever) - returns a scaled integer value
  - PWM controller (Direct control / Auto Cyclic Control / setpoint (PID) control)
  - I2C bus controller (for connection of other I2C devices)
  - Display driver (LED / LCD / OLED display / touchscreen driver)
  - Digital Input Status (Polled)
  - Digital Output Control
  - Analog Input Status (Polled)
  - Analog Output Control

Note: Data scaling of I/O from Nodes needs to match in both node + RPi. This can be achieved by having predefined data types in the Rpi and boiler plate code in the nano that is selectable via the API (restrictive), or simply from user input in RPi I/O set up and hard coding in Nano (unrestricted). All cases will potentially require user to flash nano. My preference would be for the system to be unrestricted as then the user is not reliant on the devs to perform integration of new devices, however this does increase complexity of system which means that adoption of the system becomes more complex

There is also possibility of multiple data channels per data node as each Nano has multiple I/O. In an aquarium application this may result in a network topology with one nano controlling the 'top of tank' devices and one controlling the sump devices. The RPi acting as the data sequencer and reporting interface. This topology could also be extended to use other Arduino devices such as the Mega 2560 which has many more inputs.

There are a considerable number of nano shields already available that can be utilised. For example:
- PWM/H-bridge motor shields 2 chan up to 16A - easily enough to drive skimmer and return pump
- Screw terminal breakout boards
- Stepper motor shields
- Display shields
- Relay Shields (typically 4 channel)

Then there are proprietary I2C systems such as Qwiic by sparkfun which provide a plug-and-play kind of set up and includes a large variety of sensors which might suit the technology adverse amongst us.

Slave I2C devices such as these are controlled via a secondary I2C network which uses a Node as a master controller. This adds a layer of separation between the Raspberry Pi and the I2C devices which is good form a reliability point of view. It also means that all such devices are then exposed to the main Acqua (RPi) controller via the standard Node protocol. This means that additionof such sensors does not require core code changes but simply the adaptation of the node code which is easily achieved by the end user using the online examples provided by the I2C device manufacturer.

For more complex integrations, for example retrofitting of nodes into existing control equipment, changes to the core code may be required. THis would need to be assessed on a case-by-case basis.


## Web interface

The web interface provides a dynamic layout that provides a way for the user to analyse recorded trends and control connected equipment. It also makes provision for the user to manually enter recorded data - for instance parameter test data.

The admin navigation is broken up into the following basic functions

- General settings
- Communication
- Node configuration
- GPIO Configuration
- Control Schema
- CRON Tasks
- Conditional control
- User management
- Trend data
- Event History
- Database management

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

- Data log format SQLite
- Data logs should be downloadable (CSV)
- Data log management needs to be implemented (max size / SD support / external HDD / remote FTP)


## Program structure

- Simple cyclic scanning of enabled conditional and time based macros.
- Execution of code at appropriate time / under appropriate conditions / as called by master CRON task. 
- Default master CRON task frequency set to 1 Minute which gives system granularity of 1 Minute. (Default time period subject to review but can easily be changed by the user using `crontab -e`)
- Web interface instigated by URL calls as accessed by user (flask `end-points`)
- Nodes run cyclical programs as appropriate for use.
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

## Current project status.

The project is very much in the Alpha stage with development focusing on getting a basic working framework up and running. Current development tasks can be viewed in the Alpha project - https://github.com/DeeEmm/Acqua/projects/1

When the basic system is up and running we will move into beta stage and invite developers to participate in further development.


## Contributing

If you would like to get involved with the project, or wish to get in touch, you can contact me via email or catch me on the Acqua Discord Channel:

Email: deeemm@deeemm.com  
Discord: [https://discord.gg/3kXX4f4](https://discord.gg/3kXX4f4)

Please note that at this stage support is limited to active contributors only. Beta testing will be announced at a later date.
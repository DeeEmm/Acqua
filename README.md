# Acqua
Acqua - Data Acquisition and Processing unit

The Acqua project is a data acquisition and processing system based on the Raspberry pi and Arduino nano.

The Raspberry Pi acts as the master controller and web app server and the Arduino nano/micros act as slave devices on an I2C network. The slave system is user extensible and has the ability for nodes to be created to interface to practically anything. Whilst the original idea was in the context of a reef tank controller, by using generalised descriptors the program can be used as a datalogger or programmable controller for any system requiring automation. This includes systems like irrigation, aquariums, aquaponics, motorsport, experimental systems, in fact anywhere where a simple user programmable datalog / control system is required. The extensibility of the system allows quick integration of any kind of device and includes wide capabilities as standard. Additional cases can easily be catered for by editing the nano code to suit.


## Basic I2C protocol

- Communication between the master(RPi) and slave(Arduino Nano) devices is by simple state interrogation > response protocol. 
- RPi can poll nodes to check if they are still alive
- RPi can interrogate node to obtain device capabilities
- RPi can interrogate nodes and obtain data
- Rpi can send control commands to nodes to configure them (configuration stored in flash memory)
- RPi can send control commands to nodes to perform control actions where they are available

Note: Nodes are slave devices however they could also can act as master to other slaves on the I2C network as I2C supports multiple masters. Not really sure of a use case where this may be needed (synchronised wave-makers?) will explore later.


## Main Rpi functions
- Web app server to serve main control interface - accessible via users browser
- Programmable timers (using cron)
- Conditional control engine - if-this-then-that
- Device (node) configuration - name / node type (sets api requirements) / polling frequency / watchdog (+frequency) / data logged? / 
- GPIO configuration
- Data logging inc manual data entry for test results
- Alerts


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


# IoT Water Level Control System with Satellite

## 1. Abstract
Farmers and the agricultural industry face major challenges in coming years, with water becoming an increasingly scarce resource and climate change responsible for causing prolonged periods of drought. Technological intervention and automation, is therefore becoming a requirement for farmers, to better manage their water supplies and water storage systems. The demand for IoT (Internet of Things) -based solutions, to enable farmers within the industry to increase their efficiency, conserve resources and maximise yield, is growing exponentially. The analogue methods farmers have historically used, are no longer fit for purpose or cost effective, with large OpEx spend required to send workers to site to take manual measurements of water levels. This paper designs an efficient, low-cost IoT-based solution, that enables water level monitoring within a water trough for livestock, with the ability to continuously maintain water levels using a robust IoT system driven by a Raspberry Pi microprocessor and low-powered sensors. Water levels are maintained in a trough with the use of a low-powered DC water pump; controlled by embedded software microservices written in Python. Using a local webUI with a graphical representation, the end-user is able to monitor the real-time water levels and water temperature within a trough, being measured by an ultrasonic sensor and submersible thermometer. Additional components including LEDs and an active buzzer have also been connected in the prototype tank enclosure with an OLED display, outputting real-time system metrics. The LEDs are configured to warn the user when issues occur, such as maximum or minimum water level thresholds are breached. 

## 2. Project Aims/ Objectives
The aims of this self-determined final year IoT project, is to design and build a robust, low-cost IoT water level control solution, that autonomously monitors and maintains the water levels within a water storage tank. This concept simulates an industrial water storage system, that farmers use to supply water irrigation systems, and could also be adapted for livestock farmers for trough management. IoT provides farmers access to real-time data that enables better informed decision making, with increased situational awareness across all fields, simultaneously. The water level control system will effectively monitor water levels and temperature within a storage tank, reporting metrics to an end user both locally on site via an OLED display, as well as pushing the sensor data to a cloud-based mailbox, where a customer’s application could retrieve the sensor data via a RESTful API. LEDs will be used to warn users when issues occur, such as maximum or minimum water level thresholds are breached. This IoT solution will also look to be integrated to a commercially available off the shelf satellite modem, to provide a globally accessible solution with seamless connectivity.

The high-level objectives for my work-related project are; 
1.	To align university study with a work-related IoT project to accelerate my learning and professional development within my current job role at Inmarsat;
2.	To build and develop an IoT end-to-end edge solution to gain an in-depth knowledge and practical understanding of how a full stack solution is created;
3.	To integrate LED indicators into the solution to show system status and critical water level thresholds to demonstrate the solution is working correctly, equipped with a buzzer to alert users when threshold limits are reached;
4.	To carryout IoT sensor integration and pre-processing of data to increase the efficiency of the solution;
5.	To integrate the IoT solution into an Inmarsat type approved satellite modem for transit over the Inmarsat satellite network; 
6.	Inmarsat network API integration to pull sensor data into a cloud infrastructure with a graphical representation of near real-time water levels in tanks;


## 3. Deliverables
For this final year work-related IoT project, the key deliverables outlined below form part of the key project milestones, and are fundamental to achieving the expected outcomes.

The project deliverables are as follows;

1.	Use a professional software development environment, to carryout embedded/Edge development on a single board computer, that could be deployed in a remote environment;
2.	Sensor integration - successfully integrate IoT devices to a single board computer using calibration, averaging readings and data conversion techniques, to generate reliable sensor data;
3.	Display real-time water level and temperature metrics for the main tank on a local display, which will also be outputting the dynamic power consumption of the system at any given time, as well as its IP address in case the system requires SSH access for in-field troubleshooting;
4.	Build a local (downstream) web-server GUI, that will be used to monitor the real-time water level and sensor metrics within the system. The GUI will simulate what a simple customer cloud application might look like, by creating a digital twin on the remote machine. The GUI could also be used in a practical sense for an installer in the field, that does not have access to internet connectivity and needs to monitor liquid levels within a sealed container on site;
5.	Carryout pre-processing of sensor data to optimize payload and reduce airtime costs, of data being sent over the satellite air interface;
6.	Retrieve satellite data and push into a cloud infrastructure, in order to simulate sensor data being pushed into a customer’s middleware/application platform. From here, edge intelligence would initiate/automate workstreams, using report by exception from the cloud-side. 


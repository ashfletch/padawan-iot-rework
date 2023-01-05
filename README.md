# IoT Water Level Monitoring System via Satellite

## 1. Executive Summary
For my final year project at London South Bank University, I have chosen to opt for a self-determined project that aligns with work related industry applications within our Enterprise markets. For my self-determined project, I will design and build a full end-to-end IoT solution that monitors and reports the water level within a coupled tank system, and push that sensor data into a cloud infrastructure over satellite backhaul. As part of my project design, I will be using a Raspberry Pi as an IoT edge gateway for pre-processing of data and transmitting the optimized payload to an application server over the Inmarsat satellite network. The application server will include some functionality and Inmarsat API integration, accompanied with a near real-time graphical representation of the current state of water within the main tank. 
This project has been chosen to develop my skill-set and understanding of building IoT solutions to better position myself within the Enterprise Solutions Engineering Team at Inmarsat. With this knowledge I will be able to contribute more to our partners and their development of solutions, to accelerate our go to market and generate new revenue streams.

## 2. Project Aims/ Objectives
The objectives for my final year project are; 

1. To build and develop an IoT end-to-end solution to monitor and control the water level within a system and report sensor data to the cloud; 
2. To gain an in-depth knowledge and practical understanding of how a full stack solution is created; 
3. To carryout IoT sensor integration to develop an understanding of how to calibrate and interpret the data from a physical device to present that as measurement data in a decision support system; 
4. To explore data pre-processing techniques to increase the efficiency of the solution, and push into a cloud infrastructure to simulate a customer’s middleware or IoT platform; 
5. To use a commercially available Inmarsat satellite modem and airtime service to demonstrate the ability to deploy the IoT solution in remote environments anywhere in the World without cellular or terrestrial Wi-Fi coverage; 
6. To align university study and the apprenticeship standard with a work-related IoT project, to target key knowledge/skills/behaviours related to software development processes, problem solving and considerations for practical deployment, and re-use of modular components to accelerate my learning and professional development within my job role

## 3. Expected Outcomes
The expected outcomes for this IoT project are: 

1. To automate water level control using edge processing on a single board computer, which will maintain the water level within a nominal range. If the water level exceeds certain thresholds, i.e., water level is too high or water level is critically low, the system will then trigger actions at the edge. If the water level is too high, the edge computer will initiate the water pump to remove excess water from the main tank with a buzzer and red LED, until the water level returns to a nominal range. If the water level becomes critically low, the system will sound the buzzer and illuminate an amber LED as a warning only, with no pump required. If the water level is within a nominal range, a green LED will be illuminated and remain lit with no further action required to indicate the system is O.K.; 
2. I also aim to be able to develop a local web-server GUI to view the real-time water level and temperature data without the need of internet connectivity; 
3. Satellite integration will be one of the final stages that I hope to achieve as part of the project. Integrating satellite will allow me to send the remote sensor data over-the-air and into a cloud infrastructure such as AWS or Azure IoT. This will simulate a customer’s middleware or application platform where remote/field data is translated into human readable information, to trigger workflows from the cloud-side. 

## 4. Resources

### Equipment:

    - Raspberry Pi 3 Model B+ thepihut.com 
    - Raspberry Pi T-Cobbler Cable (prototyping phase) thepihut.com
    - PoE (12V + 5VDC output) HAT for Raspberry Pi thepihut.com 
    - Power monitoring HAT thepihut.com 
    - Breadboard (prototyping phase) amazon.co.uk 
    - LEDs (green/ amber/ red) amazon.co.uk 
    - 5V buzzer amazon.co.uk 
    - Resistors amazon.co.uk 
    - Jumper Cables (prototyping phase) amazon.co.uk 
    - Ultra-sonic sensor HC-SR04 amazon.co.uk
    - Submersible temperature sensor DS18B20 thepihut.com 
    - Inmarsat IsatData Pro Satellite Modem – ST2100 orbcomm.com 
    - Mini OLED Screen thepihut.com 
    - 22AWG cabling (mixed colours) thepihut.com 
    - Ferrule connectors + crimping tool amazon.co.uk 
    - 3VDC water pump thepihut.com 
    - 2-Channel Relay Module amazon.co.uk 
    - 6mm tubing thepihut.com 
    - Prototyping Soldering board thepihut.com 
    - Power module board (5-3.3VDC) amazon.co.uk 
    - DIN rail amazon.co.uk 
    - 4A RCBO or RCD cpc.farnell.com
    - C14 panel mount with switched fuse spur uk.rs-online.com 
    - PoE injector + RJ45 cable (RPi power supply) amazon.co.uk 
    - RPi DIN rail mounts thepihut.com 
    - Raspberry PI GPIO Screw HAT thepihut.com 
    - Electrical enclosure 300 x 220 x 400mm screwfix.com
    - Push-fit glands for tank lids amazon.co.uk

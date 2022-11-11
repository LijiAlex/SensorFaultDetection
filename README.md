# Sensor-Fault-Detection

### Problem Statement
The Air Pressure System (APS) is a critical component of a heavy-duty vehicle that uses compressed air to force a piston to provide pressure to the brake pads, slowing the vehicle down. The benefits of using an APS instead of a hydraulic system are the easy availability and long-term sustainability of natural air.

This is a Binary Classification problem, in which the affirmative class indicates that the failure was caused by a certain component of the APS, while the negative class
indicates that the failure was caused by something else.

### Solution Proposed 
In this project, the system in focus is the Air Pressure system (APS) which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes. The datasets positive class corresponds to component failures for a specific component of the APS system. The negative class corresponds to trucks with failures for components not related to the APS system.

The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.

## Strategies
* Drop columns with more than 70% missing values
* Scaling the data using Robust scaler
* KNN Imputer for missing values
* SMOTETomek for handling imbalanced data
* XGboost classifier for training. Accuracy>95% Cost:minimal

## Tech Stack Used
1. Python 
2. FastAPI 
3. Machine learning algorithms
4. Docker
5. MongoDB

## Infrastructure Required.

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions

## Data Collections
<img width="397" alt="Data Collections" src="https://user-images.githubusercontent.com/59106185/201272285-8dccf265-680a-4d1b-940a-b4f59ceafd0a.png">

## Project Architecture
![project architecture](https://user-images.githubusercontent.com/59106185/201272669-cce9984f-f30a-46c7-9677-2b14c6bbd11f.png)

## Deployment Architecture
<img width="426" alt="deployment architecture" src="https://user-images.githubusercontent.com/59106185/201272727-f5e4a537-ca6a-43ed-8288-93d8b5aedc82.png">

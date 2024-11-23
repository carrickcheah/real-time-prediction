# Project: Predict Bitcoin Price

This repository contains code and resources to predict Bitcoin prices.

## Overview

![Portfolios3](./image/portfolios3.jpg)  
**Table of contents**  
1.Project Overview  
2.System Design  
3.Feature Pipeline  
4.Training Pipeline  
5.Inference Pipeline  
6.Microservices in the System  
7.Engineering Data  
8.Train and Retrain for Continuous Improvement  
9.Build REST API  
10.Deployment on Cloud  
11.*Coding Session*  
&nbsp;
&nbsp;

## System Design

![Slide2](./image/Slide2.JPG)  
Here’s a quick look at the system’s basic design. The goal is to make the process efficient, scalable, and suitable for real-time predictions.  

Our system revolves around 3 main components:  

Feature Pipeline – Prepares and transforms raw data.  
Training Pipeline – Builds and optimizes the machine learning models.  
Inference Pipeline – Delivers real-time predictions. Let’s look at each in detail.  
&nbsp;
&nbsp;

## Feature pipeline

![Slide3](./image/Slide3.JPG)  
The feature pipeline consists of 3 microservices:

t_ingest: It connects to the broker’s WebSocket, fetches live data, and sends it to Kafka.  
t_transform: This service processes the raw data into OHLC format.  
t_push: Finally, it pushes the cleaned data to the feature store.  
Once built, these microservices are dockerized to ensure seamless integration and scalability.  
&nbsp;
&nbsp;

## Training pipeline

![Slide4](./image/Slide4.JPG)  
In the training pipeline, we use an XGBoost model to train our data.  
We also tune hyperparameters and leverage CometML to track experiments.  
Afterward, the best-performing model is pushed to a model registry for deployment.  
&nbsp;
&nbsp;

## Inference pipeline

![Slide5](./image/Slide5.JPG)  
For the inference pipeline, we deploy a REST API that serves real-time predictions.  
Additionally, we set up a training job to ensure the model remains up-to-date with fresh data.  
&nbsp;
&nbsp;

## Microservices in the system

![Slide6](./image/Slide6.JPG)
Within this system, we're going to build 5 microservices. These microservices will handle the core functionalities of the system, ensuring modularity and scalability.  
&nbsp;
&nbsp;

## Engineerng data

![Slide7](./image/Slide7.JPG)  
First, let’s build the feature pipeline, which consists of three microservices:  

t_ingest: This connects to the broker’s WebSocket, downloads data, and sends it to Kafka topic 1.  
t_transform: This microservice processes and transforms the data into OHLC format.  
t_push: It pushes the processed data to the feature store.  
After building these services, we’ll dockerize them to streamline deployment and integration.  
&nbsp;
&nbsp;

## Train and Retrain for Continuous Improvement

![Slide8](./image/Slide8.JPG)  
In the training pipeline, we train the data using an XGBoost model.  

We fine-tune the model with hyperparameter optimization.  
CometML is used to track experiments and manage retraining.  
The best-performing model is then pushed to the model registry for deployment.  
&nbsp;
&nbsp;

## Build rest-api

![Slide9](./image/Slide9.JPG)  
In the inference pipeline, we deploy the REST API to serve predictions.  

Real-time features are deployed to the cloud to ensure fast and reliable predictions.  
Additionally, we deploy a training job to keep the model updated with fresh data, maintaining performance over time.  
&nbsp;
&nbsp;

## Deployment on cloud

![Slide10](./image/Slide10.JPG)  
Finally, the entire system is deployed to Quix Cloud. With this setup, we can serve predictions seamlessly via the API we built.  
The system is now fully operational and ready for real-time use.  
&nbsp;
&nbsp;

## Coding Sessions

### Task 1: Create a Feature Pipeline with 3 Microservices and Dockerize Them

#### 1.1 First micro service : t_ingest

- [X] Setup Redpanda locally, mske it up and running  
    Redpanda is an event streaming platform: it provides the infrastructure for streaming real-time data.  

- [X] poetry add quixstreams  
    Test send event for processing data in Kafka . Later use to transfer data in real time.  

- [X] Connect to the Kraken API to download data  
- [X] Extract config parameters  
- [X] Push data to kafka topic  
![live_data](./image/live_data.jpg)  
  
- [X] Dockerize it  
![docker_ingest](./image/docker_ingest.jpg)  

#### 1.2 Build next mirco services: t_transform

- [X] Read data from kafka_input_topic, transform data and write it to kafka_output_topic.  
- [X] Dockerize it  
.

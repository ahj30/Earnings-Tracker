# Earnings Tracker

##Introduction
Welcome to the Earnings Tracker! 
Created by Chris Jayson and Andrew Joel

Georgetown University -- OPIM 244 -- May 2020

This program compiles the past ten years of earnings for a stock of your choice and provides price performance that occured during the earnings period. 

##Installation 
Fork this repository, then clone it to download it locally onto your computer.
Choose a familiar download location like the Desktop.

After cloning the repository, navigate there from the command line:

```sh
cd ~/"Your download location"/Earnings-Tracker
```
## Environment Setup and Security Setup

Create and activate a new Anaconda virtual environment:
```sh
conda create -n tracker-env python=3.7 # (first time only)
conda activate tracker-env
```
From within the virtual environment, install the required packages specified in the "requirements.txt" file:

```sh
pip install -r requirements.txt
```
The program will need an API Key to issue requests to the [AlphaVantage API](https://www.alphavantage.co). But the program's source code should absolutely not include the secret API Key value. Instead, you should set an environment variable called `ALPHA_KEY`, and your program should read the API Key from this environment variable at run-time.

Create a ".env" file and place the following inside:

```
ALPHA_KEY="your API key"
```
## Usage 
To run the program:

```sh
python app/tracker.py
```




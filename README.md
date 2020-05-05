# Earnings Tracker

## Introduction

Welcome to the Earnings Tracker! 

Created by Chris Jayson and Andrew Joel

Georgetown University -- OPIM 244 -- May 2020

This program compiles the past ten years of earnings for a stock of your choice and provides price performance that occured during the earnings period. 

Use of this program is inteded for persons with a familiar knowledge of the stock market (i.e. traders).

## Installation 
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

## Example Output
```sh
(tracker-env)
"USER NAME" ~/Desktop/Earnings-Tracker (master)
$ python app/tracker.py
Welcome to the Earnings Tracker! Stock tickers cannot include numbers or be longer than five characters.
Please input a stock ticker: AAPL
--------------------------------------------------
Valid ticker identified! . . .
Web Requests fulfilled successfully! . . .
PREPARING DATA ON AAPL EARNINGS REPORTING . . .
--------------------------------------------------
AAPL 52-week trading range (low, last close, high): $170.27 -- $289.07 -- $327.85
--------------------------------------------------
   Filing Date Closing Price 2-Day Return
0   2020-07-28          NEXT   DISCLOSURE
1   2020-05-01       $289.07         nan%
2   2020-01-29       $324.34        1.93%
3   2019-10-31       $248.76        5.03%
4   2019-07-31       $213.04       -0.17%
5   2019-05-01       $210.52        4.14%
6   2019-01-30       $165.25        7.33%
7   2018-11-05       $201.59       -1.80%
8   2018-08-01       $201.50        8.61%
9   2018-05-02       $176.57        4.50%
10  2018-02-02       $160.50       -6.97%
11  2017-11-03       $172.50        3.59%
12  2017-08-02       $157.14        3.61%
13  2017-05-03       $147.06       -0.67%
14  2017-02-01       $128.75        5.75%
15  2016-10-26       $115.59       -3.24%
16  2016-07-27       $102.95        7.64%
17  2016-04-27        $97.82       -9.57%
18  2016-01-27        $93.42       -6.08%
19  2015-10-28       $119.27        5.09%
20  2015-07-22       $125.22       -4.37%
21  2015-04-28       $130.56       -3.07%
22  2015-01-28       $115.31        8.57%
23  2014-10-27       $105.11        1.43%
24  2014-07-23        $97.19        2.41%
25  2014-04-24       $567.77        8.61%
26  2014-01-28       $506.50       -9.47%
27  2013-10-30       $524.90        1.16%
28  2013-07-24       $440.51        4.55%
29  2013-04-24       $405.46        0.55%
30  2013-01-24       $450.50      -15.57%
31  2012-10-31       $595.32       -1.24%
32  2012-07-25       $574.97       -4.43%
33  2012-04-25       $610.00        8.12%
34  2012-01-25       $446.66        5.60%
35  2011-10-26       $400.60        1.72%
36  2011-07-20       $386.90        2.73%
37  2011-04-21       $350.70        3.05%
38  2011-01-19       $338.84       -2.37%
39  2010-10-27       $307.83       -0.92%
40  2010-07-21       $254.24        2.79%
--------------------------------------------------
Descriptive statistics for AAPL earnings date returns:
        2-Day Returns
Mean            0.99%
Std Dev         5.58%
Min           -15.57%
25%            -2.08%
Median          1.93%
75%             4.79%
Max             8.61%
--------------------------------------------------
```

## Licensing
This project is licensed under the terms of the MIT license.
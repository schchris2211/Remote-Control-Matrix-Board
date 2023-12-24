# Remote Control Matrix Board

A tool to keep people connected.

## Description

This project remotely controls the display of an Adafruit M4 Matrix Board. The top-level module, main.py, handles all connectivity 
logic and executes a display file, run_file.py, after downloading it from a GitHub repository if the update_info Text file determines so. 

The Matrix Board is reset every morning to check the repository for updates. This can also be done by resetting the board manually.

## Hardware and Installing
The required hardware can be found [here](https://www.adafruit.com/product/4812). Adafruit offers a great, beginner-friendly [manual](https://learn.adafruit.com/adafruit-matrixportal-m4/overview) for setting up 
the Matrix Board and installing Circuitpython. Additionally, the manual offers a guide to basic libraries and example scripts.

Please note, that the internet connection is handled via a non-public secrets.py file as described [here](https://learn.adafruit.com/adafruit-matrixportal-m4/internet-connect).

## Contact
Email: christopher.schoenwaelder@gmail.com

## Acknowledgments
This project was motivated by Moses Swai's Harbinger project, which can be found [here](https://github.com/mosesswai/harbinger?tab=readme-ov-file).

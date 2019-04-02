# Nutanix RCA Script
Nutanix Cluster RCA script
File name: rca.py

Author: Mehul Ashara  

Date created: 04/01/2019

Date last modifed: 04/02/2019

Python version: 2.7.5

Purpose: This hypervisor agnostic script is to be run from CVM to simplify RCA process for SREs. 

Usage: python rca.py >> /home/nutanix/tmp/rca_"$(date +"%Y-%m-%d_%H-%M").log"

Run the script ONLY as nutanix user

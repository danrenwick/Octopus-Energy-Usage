import pandas as pd
import requests
import json
import csv
import datetime
import time
from requests.auth import HTTPBasicAuth
from datetime import date, timedelta

#Date Range params
period_from = input("Enter start Date (format: yyyy-mm-dd): ")+ "T00:00:00"
period_to = input("Enter end Date (format: yyyy-mm-dd): ")+ "T00:00:00"
start = date(int(period_from[:4]),int(period_from[5:7]),int(period_from[8:10]))
end = date(int(period_to[:4]),int(period_to[5:7]),int(period_to[8:10]))
delta = end - start

#Request params
base_url = "https://api.octopus.energy/"
api = "YOUR API KEY"
mpan = "YOUR MPAN NUMBER"
mprn = "YOUR MPRN NUMBER"
e_serial = "YOUR ELECTRICITY METER SERIAL NUMBER"
g_serial = "YOUR GAS METER SERIAL NUMBER"
params = "period_from="+period_from+"&"+"period_to="+period_to

def electricity_usage ():
    
    global e_usage
    e_usage = pd.DataFrame()

    for i in range(delta.days + 1):
        
        EXT = "v1/electricity-meter-points/{}/meters/{}/consumption/".format(mpan, e_serial)
        x = requests.get(base_url+EXT,params="period_from="+(start+timedelta(days = i)).strftime("%Y-%m-%d")+"T00:00"+"&"+"period_to="+((start+timedelta(i)+timedelta(days=1)).strftime("%Y-%m-%d"))+"T00:00", auth=(api,""))
        if x.status_code == 200:
            print("Successful Electricity Call: "+(start+timedelta(i)).strftime("%Y-%m-%d"))
        elif x.status_code == 400:
            print("Successful Electricity call but errors in inputs: "+(start+timedelta(i)).strftime("%Y-%m-%d"))
        elif x.status_code == 404:
            print("Unsuccessful Electricity Call: "+(start+timedelta(i)).strftime("%Y-%m-%d"))
        else:
            print("Electricity Error Code "+x.status_code+": "+(start+timedelta(i)).strftime("%Y-%m-%d"))
    
        e_data = x.json()
    
        e_results = e_data["results"]

        if len(e_results) == 0:
            e_usage = e_usage.append([{'consumption': 0.0, 'interval_start': (start+timedelta(days = i)).strftime("%Y-%m-%d")+'T00:00:00Z', 'interval_end': ((start+timedelta(i)+timedelta(days=1)).strftime("%Y-%m-%d"))+"T00:00:00Z"}], ignore_index = True)
        else:
            e_usage = e_usage.append(e_results, ignore_index = True)

    e_usage['type'] = "Electricity"

def gas_usage ():

    global g_usage
    g_usage = pd.DataFrame()
    
    for i in range(delta.days + 1):
        
        EXT = "v1/gas-meter-points/{}/meters/{}/consumption/".format(mprn, g_serial)
        x = requests.get(base_url+EXT,params="period_from="+(start+timedelta(days = i)).strftime("%Y-%m-%d")+"T00:00"+"&"+"period_to="+((start+timedelta(i)+timedelta(days=1)).strftime("%Y-%m-%d"))+"T00:00", auth=(api,""))
        if x.status_code == 200:
            print("Successful Gas Call: "+(start+timedelta(i)).strftime("%Y-%m-%d"))
        elif x.status_code == 400:
            print("Successful Gas call but errors in inputs: "+(start+timedelta(i)).strftime("%Y-%m-%d"))
        elif x.status_code == 404:
            print("Unsuccessful Gas Call: "+(start+timedelta(i)).strftime("%Y-%m-%d"))
        else:
            print("Gas Error Code "+x.status_code+": "+(start+timedelta(i)).strftime("%Y-%m-%d"))
    
        g_data = x.json()
    
        g_results = g_data["results"]

        if len(g_results) == 0:
            g_usage = g_usage.append([{'consumption': 0.0, 'interval_start': (start+timedelta(days = i)).strftime("%Y-%m-%d")+'T00:00:00Z', 'interval_end': ((start+timedelta(i)+timedelta(days=1)).strftime("%Y-%m-%d"))+"T00:00:00Z"}], ignore_index = True)
        else:
            g_usage = g_usage.append(g_results, ignore_index = True)

    g_usage['type'] = "Gas"

def merge_frames():
    global consumption
    consumption = pd.DataFrame()
    consumption = pd.concat([e_usage, g_usage])
    
    consumption['interval_start'] = pd.to_datetime(consumption['interval_start'], utc = True).astype('datetime64[ns]')
    consumption['interval_end'] = pd.to_datetime(consumption['interval_end'], utc = True).astype('datetime64[ns]')

    consumption = consumption[['type','interval_start','interval_end','consumption']]

def get_usage():
    electricity_usage()
    gas_usage()
    merge_frames()

def usage_to_csv():
    filename = "Consumption " + (start.strftime("%Y-%m-%d")) + " to " + (end.strftime("%Y-%m-%d")) + ".csv"
    consumption.to_csv(filename, index = False)

try:
    get_usage()
    usage_to_csv()
except:
    print("Something went wrong!")   

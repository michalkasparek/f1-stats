#!/usr/bin/env python

"""
Don't repeat yourself, they say. So this is the stuff that goes in the beginning of all my 
Jupyter Notebooks exploring various F1 statistics. https://github.com/michalkasparek/f1-stats/
"""

import pandas as pd
import matplotlib
import os

# Let's define some useful lists first

unknownResult = ["nan0n", "NaN", "NA", "inf"]
crashes = ["Accident", "Collision", "Fatal accident", "Collision damage", "Spun off"]
Europe = ["Austrian", "Belgian", "British", "Czech", "Danish", "Dutch", "East German", "Finnish", "French", "German", "Hungarian", "Irish", "Italian", "Liechtensteiner", "Monegasque", "Polish", "Portuguese", "Russian", "Spanish", "Swedish", "Swiss"]
NAmerica = ["American", "Canadian", "Mexican"]
SAmerica = ["Argentine", "Brazilian", "Chilean", "Colombian", "Uruguayan", "Venezuelan"]
Asia = ["Chinese", "Indian", "Indonesian", "Japanese", "Malaysian", "Thai", "Hong Kong"]
Africa = ["Rhodesian", "South African"]
Oceania = ["Australian", "New Zealander"]
multiple = ["American-Italian", "Argentine-Italian"]
streetCircuits = ["Melbourne", "Monte-Carlo", "Montreal", "Valencia", "Marina Bay", "Sochi", "Baku", "Jeddah", "Adelaide", "Phoenix", "Detroit", "Dallas", "Nevada", "California", "Oporto", "Lisbon"]

# Now let's load the stats. Source: https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020

drivers = pd.read_csv(os.path.join("data", "drivers.csv"))
results = pd.read_csv(os.path.join("data", "results.csv"))
races = pd.read_csv(os.path.join("data", "races.csv"))
circuits = pd.read_csv(os.path.join("data", "circuits.csv"))
status = pd.read_csv(os.path.join("data", "status.csv"))
constructors = pd.read_csv(os.path.join("data", "constructors.csv"))

# Merge all the tables into a single dataframe

results = results.merge(drivers, on="driverId", how="right")
races = races.merge(circuits, on="circuitId", how="right")
results = results.merge(races, on="raceId", how="right")
results = results.merge(status, on="statusId", how="right")
results = results.merge(constructors, on="constructorId", how="right")

# Make the columns more useful 

results["fullname"] = results["forename"] + " " + results["surname"]
results["date"] = results["date"].str.slice(0,6) + results["year"].astype(str).str.slice(0,4)
results["date"] = pd.to_datetime(results["date"], format="%d/%m/%Y")
results["year"] = results["year"].apply(pd.to_numeric, errors = "coerce").astype(int, errors="ignore")
results["round"] = results["round"].apply(pd.to_numeric, errors = "coerce").astype(int, errors="ignore")
results["position"] = results["position"].apply(pd.to_numeric, errors = "coerce").astype(int, errors="ignore")

# Make some new columns

results["year_round"] = results["year"].astype(str).str.slice(0,4) + results["round"].astype(str).str.slice(0,-2).str.zfill(2)
results = results[~results.year_round.isin(unknownResult)]
results["year_round"] = results["year_round"].apply(pd.to_numeric, errors = "coerce").astype(int)

results.loc[results.nationality_x.isin(Europe),"driverContinent"]="Europe"
results.loc[results.nationality_x.isin(NAmerica),"driverContinent"]="NAmerica"
results.loc[results.nationality_x.isin(SAmerica),"driverContinent"]="SAmerica"
results.loc[results.nationality_x.isin(Asia),"driverContinent"]="Asia"
results.loc[results.nationality_x.isin(Africa),"driverContinent"]="Africa"
results.loc[results.nationality_x.isin(Oceania),"driverContinent"]="Oceania"
results.loc[results.nationality_x.isin(multiple),"driverContinent"]="multiple"

results.loc[results.location.isin(streetCircuits),"street"]=True

entries = pd.Series(results.groupby(["driverId"]).size(), name="entries")
results = results.merge(entries, on = ["driverId"], how = "right")

# Split the main dataframe for wins, podiums and top 6 finishes only 

wins = results[results["position"] == 1]
podiums = results[results["position"] < 4]
top6 = results[results["position"] < 7]
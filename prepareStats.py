#!/usr/bin/env python

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Let's define some useful lists first:

unknownResult = ["nan0n", "NaN", "NA", "inf"]
lapped = ["+1 Lap", "+2 Laps", "+3 Laps", "+4 Laps", "+5 Laps", "+6 Laps", "+7 Laps", "+8 Laps", "+9 Laps", "+10 Laps", "+11 Laps", "+12 Laps", "+13 Laps"]
crashes = ["Accident", "Collision", "Fatal accident", "Collision damage", "Spun off"]
fails = ["Accident", "Collision", "Engine", "Gearbox", "Transmission", "Clutch", "Hydraulics" ,"Electrical", "Spun off", "Radiator" ,"Suspension", "Brakes", "Differential", "Overheating", "Mechanical", "Tyre", "Driver Seat", "Puncture", "Driveshaft", "Retired", "Fuel pressure", "Front wing", "Water pressure", "Refuelling", "Wheel", "Throttle", "Steering", "Technical", "Electronics", "Broken wing", "Heat shield fire", "Exhaust", "Oil leak", "+11 Laps", "Wheel rim", "Water leak", "Fuel pump", "Track rod", "+17 Laps", "Oil pressure", "+42 Laps", "+13 Laps", "Withdrew", "+12 Laps", "Engine fire", "Engine misfire", "+26 Laps", "Tyre puncture", "Out of fuel", "Wheel nut", "Not classified", "Pneumatics", "Handling", "Rear wing", "Fire", "Wheel bearing", "Physical", "Fuel system", "Oil line", "Fuel rig", "Launch control", "Injured", "Fuel", "Power loss", "Vibrations", "107% Rule", "Safety", "Drivetrain", "Ignition", "Did not qualify", "Injury", "Chassis", "Battery", "Stalled", "Halfshaft", "Crankshaft", "+10 Laps", "Safety concerns", "Not restarted", "Alternator", "Underweight", "Safety belt", "Oil pump", "Fuel leak", "Excluded", "Did not prequalify", "Injection", "Distributor", "Driver unwell", "Turbo", "CV joint", "Water pump", "Fatal accident", "Spark plugs", "Fuel pipe", "Eye injury", "Oil pipe", "Axle", "Water pipe", "+14 Laps", "+15 Laps", "+25 Laps", "+18 Laps", "+22 Laps", "+16 Laps", "+24 Laps", "+29 Laps", "+23 Laps", "+21 Laps", "Magneto", "+44 Laps", "+30 Laps", "+19 Laps", "+46 Laps", "Supercharger", "+20 Laps", "Collision damage", "Power Unit", "ERS", "+49 Laps", "+38 Laps", "Brake duct", "Seat", "Damage", "Debris", "Illness", "Undertray", "Cooling system"]
dnqs = ["Did not qualify", "Did not prequalify", "107% Rule"]
dns = ["Did not qualify", "Did not prequalify", "107% Rule", "Safety", "Injured", "Not restarted", "Launch control", "Safety concerns", "Underweight"]

Europe = ["Austria", "Austrian", "Azerbaijan", "Belgian", "Belgium", "British", "Czech", "Danish", "Dutch", "East German", "Finnish", "France", "French", "German", "Germany", "Hungarian", "Hungary", "Irish", "Italian", "Italy", "Liechtensteiner", "Monaco", "Monegasque", "Netherlands", "Polish", "Portugal", "Portuguese", "Russia", "Russian", "Spanish", "Spain", "Sweden", "Swedish", "Swiss", "Switzerland", "Turkey", "UK"]
NAmerica = ["American", "Canada", "Canadian", "Mexican", "Mexico", "USA"]
SAmerica = ["Argentina", "Argentine", "Brazil", "Brazilian", "Chilean", "Colombian", "Uruguayan", "Venezuelan"]
Asia = ["Bahrain", "Chinese", "China", "Hong Kong", "India", "Indian", "Indonesian", "Japan", "Japanese", "Korea", "Malaysia", "Malaysian", "Qatar", "Saudi Arabia", "Singapore", "Thai", "UAE"]
Africa = ["Morocco", "Rhodesian", "South Africa", "South African"]
Oceania = ["Australia", "Australian", "New Zealander"]
multiple = ["American-Italian", "Argentine-Italian"]
westernEurope = ["Austria", "Belgium", "Germany", "France", "Italy", "Monaco", "Netherlands", "Portugal", "Spain", "Sweden", "Switzerland", "UK"]

streetCircuits = ["Melbourne", "Monte-Carlo", "Montreal", "Valencia", "Marina Bay", "Sochi", "Baku", "Jeddah", "Adelaide", "Phoenix", "Detroit", "Dallas", "Nevada", "California", "Oporto", "Lisbon"]

# Now we're gonna load the stats… (source: http://ergast.com/mrd/db/#csv):

drivers = pd.read_csv(os.path.join("dataErgast", "drivers.csv"))
results = pd.read_csv(os.path.join("dataErgast", "results.csv"))
races = pd.read_csv(os.path.join("dataErgast", "races.csv"))
circuits = pd.read_csv(os.path.join("dataErgast", "circuits.csv"))
status = pd.read_csv(os.path.join("dataErgast", "status.csv"))
constructors = pd.read_csv(os.path.join("dataErgast", "constructors.csv"))

# …merge all the tables into a single dataframe…:

drivers["driverUrl"] = drivers["url"]
results = results.merge(drivers[['driverId', 'driverRef', 'code', 'forename', 'surname', 'dob', 'nationality', 'driverUrl']], on="driverId", how="inner")
circuits["circuitUrl"] = circuits["url"]
circuits["circuit"] = circuits["name"]
races["gp"] = races["name"]
races = races.merge(circuits[["circuitId", "circuitRef", "location", "country", "circuitUrl", "circuit"]], on="circuitId", how="inner")
results = results.merge(races[["raceId","year","round","date","quali_date","quali_time","location","country","gp"]], on="raceId", how="inner")
results = results.merge(status, on="statusId", how="inner")
constructors["constructor"] = constructors["name"]
constructors["constructorUrl"] = constructors["url"]
constructors["constructorNationality"] = constructors["nationality"]
results = results.merge(constructors[["constructorId", "constructor", "constructorNationality", "constructorRef"]], on="constructorId", how="inner")

# …make the columns more useful…:

results["name"] = results["forename"] + " " + results["surname"]
results["date"] = pd.to_datetime(results["date"], format="%Y-%m-%d")
results["quali_date"] = pd.to_datetime(results["date"], format="%Y-%m-%d")
results["dob"] = pd.to_datetime(results["dob"], format="%Y-%m-%d")
results["number"] = results["number"].apply(pd.to_numeric, errors = "coerce").astype(np.int64, errors="ignore")
results["age"] = results["date"] - results["dob"]
results["year"] = results["year"].apply(pd.to_numeric, errors = "coerce").astype(np.int64, errors="ignore")
results["round"] = results["round"].apply(pd.to_numeric, errors = "coerce").astype(np.int64, errors="ignore")
results["position"] = results["position"].apply(pd.to_numeric, errors = "coerce").astype(np.int64, errors="ignore")
results["fastestLapSpeed"] = results["fastestLapSpeed"].apply(pd.to_numeric, errors = "coerce").astype(np.int64, errors="ignore")

# …and create some new columns and variables:

results.loc[results.nationality.isin(Europe),"driverContinent"]="Europe"
results.loc[results.nationality.isin(NAmerica),"driverContinent"]="NAmerica"
results.loc[results.nationality.isin(SAmerica),"driverContinent"]="SAmerica"
results.loc[results.nationality.isin(Asia),"driverContinent"]="Asia"
results.loc[results.nationality.isin(Africa),"driverContinent"]="Africa"
results.loc[results.nationality.isin(Oceania),"driverContinent"]="Oceania"
results.loc[results.nationality.isin(multiple),"driverContinent"]="multiple"

results["street"]=False
results.loc[results.location.isin(streetCircuits),"street"]=True

entries = pd.Series(results.groupby(["driverId"]).size(), name="entries")
results = results.merge(entries, on = ["driverId"], how = "right")

winners = results[results["position"] == 1].name.drop_duplicates().tolist()

firstGPdate = results["date"].min()
lastGPdate = results["date"].max()
lastGP = results[results["date"] == lastGPdate].iloc[0]
lastGP = str(lastGP["year"]) + " " + str(lastGP["gp"])
firstGPdrivers = results[results["date"] == firstGPdate].name.tolist()
lastGPdrivers = results[results["date"] == lastGPdate].name.tolist()
currentSeason = results["year"].max()
currentDrivers = results[results["year"] == currentSeason].name.drop_duplicates().tolist()
currentConstructors = results[results["year"] == currentSeason].constructor.drop_duplicates().tolist()

# Now split the main dataframe for wins, podiums and top 6 finishes only:

wins = results[results["position"] == 1]
podiums = results[results["position"] < 4]
top6 = results[results["position"] < 7]

# Human-readable lap times → machine-readable lap times:

def millisecondize(time):
    try:
        time = str(time).replace("+","")
        minutes = int(time.split(":")[0])
        milliseconds = int(time[-3:])
        seconds = int(time[-6:-4])
        time = ( minutes * 60000 ) + (seconds * 1000) + milliseconds
    except:
        time = time
    return time

# Let's give the plots some swag:

plt.style.use("_mpl-gallery")
plt.rcParams["figure.figsize"] = (20,3)

# Say hi

print("Last GP in the database: " + lastGP)
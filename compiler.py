import pandas as pd
import os

#get the filenames of the raw dataset
filenames = os.listdir('raw_data')

years = [1991, 1996, 2001, 2006, 2011]

##################################################
#Extract values
def monthly(month):
  #TMAX, TMIN, PRCP, SNOW 
  precipitation = month['PRCP'].sum()
  cold = month[month['TMIN'] < 32].count()['TMIN']
  heat = month[month['TMAX'] > 90].count()['TMAX']
  return [precipitation, cold, heat]

##################################################
#Repeat for every month of the year
def yearly(year):
  prcp_summary = list()
  cold_summary = list()
  heat_summary = list()
  for j in range(1, 13):
    values = monthly(year.loc[(raw['DATE'].dt.month==j)])
    prcp_summary.append(values[0])
    cold_summary.append(values[1])
    heat_summary.append(values[2])
  
  #Find yearly totals
  total_prcp = sum(prcp_summary)
  total_cold = sum(cold_summary)
  total_heat = sum(heat_summary)
  
  #Amalgomate
  summary = list()
  summary = summary + prcp_summary
  summary.append(total_prcp)
  summary = summary + cold_summary
  summary.append(total_cold)
  summary = summary + heat_summary
  summary.append(total_heat)
  return summary

##################################################
#Repeat the process for each filename
#for filename in filenames:
for file in range(1):
  raw = pd.read_csv('raw_data/'+filenames[0])
  raw['DATE'] = pd.to_datetime(raw['DATE'], format='%Y-%m-%d')

  col_names = ['year', 'janprcp', 'febprcp', 'marprcp', 'aprprcp', 'mayprcp', 'junprcp', 'julprcp', 'augprcp', 'sepprcp', 'octprcp', 'novprcp', 'decprcp', 'totprcp', 'jancold', 'febcold', 'marcold', 'aprcold', 'maycold', 'juncold', 'julcold', 'augcold', 'sepcold', 'octcold', 'novcold', 'deccold', 'totcold', 'janheat', 'febheat', 'marheat', 'aprheat', 'mayheat', 'junheat', 'julheat', 'augheat', 'sepheat', 'octheat', 'novheat', 'decheat', 'totheat']
  annual = pd.DataFrame(columns = col_names)
  index = 0
  for i in range(1960, 2012): 
    summary = yearly(raw.loc[(raw['DATE'].dt.year==i)])
    row  = [int(i)] + summary
    annual.loc[index] = row
    index = index + 1
  print(annual['year'][0])
  print(type(annual['year'][0]))
  #print(annual.loc[(annual['year'] > 1959 & annual['year'] < 1961)])



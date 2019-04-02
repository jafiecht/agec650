import pandas as pd
import os

#get the filenames of the raw dataset
filenames = os.listdir('raw_data')

#Years of interest
years = [1991, 1996, 2001, 2006, 2011]

#Names of the data to be summarized annually
annual_names = ['year', 'janprcp', 'febprcp', 'marprcp', 'aprprcp', 'mayprcp', 'junprcp', 'julprcp', 'augprcp', 'sepprcp', 'octprcp', 'novprcp', 'decprcp', 'totprcp', 'jancold', 'febcold', 'marcold', 'aprcold', 'maycold', 'juncold', 'julcold', 'augcold', 'sepcold', 'octcold', 'novcold', 'deccold', 'totcold', 'janheat', 'febheat', 'marheat', 'aprheat', 'mayheat', 'junheat', 'julheat', 'augheat', 'sepheat', 'octheat', 'novheat', 'decheat', 'totheat']

##################################################
#Create a dataframe to write to
col_names = ['year', 'state'] + annual_names[1:]
for i in range(1,6):
  for annual_name in annual_names[1:]:
    col_names.append(annual_name + '_' + str(i))

master = pd.DataFrame(columns = col_names)

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
overall_index = 0
for filename in filenames:
  state = os.path.splitext(filename)[0]
  print(state)
  
  raw = pd.read_csv('raw_data/'+filename)
  raw['DATE'] = pd.to_datetime(raw['DATE'], format='%Y-%m-%d')

  annual = pd.DataFrame(columns = annual_names)
  index = 0
  for i in range(1960, 2012):
    summary = yearly(raw.loc[(raw['DATE'].dt.year==i)])
    row  = [i] + summary
    annual.loc[index] = row
    index = index + 1
  
  #If it's needed to normalize, this will be how it's done
  #historical = annual.loc[(annual['year'] > 1959) & (annual['year'] < 1991)].copy()
  #for col_name in col_names[1:]:
    #average = historical[col_name].mean()
    #annual[col_name] = annual[col_name] / average
 
  for year in years:
    row = [year, state] 
    primary =  annual.loc[(annual['year'] == year)].values.tolist()[0][1:]
    lag1 = annual.loc[(annual['year'] == (year-1))].values.tolist()[0][1:]
    lag2 = annual.loc[(annual['year'] == (year-2))].values.tolist()[0][1:]
    lag3 = annual.loc[(annual['year'] == (year-3))].values.tolist()[0][1:]
    lag4 = annual.loc[(annual['year'] == (year-4))].values.tolist()[0][1:]
    lag5 = annual.loc[(annual['year'] == (year-5))].values.tolist()[0][1:]
    row = row + primary + lag1 + lag2 + lag3 + lag4 + lag5

    master.loc[overall_index] = row
    overall_index = overall_index + 1

master.to_csv('climatic_data.csv', index=False)
print(master)

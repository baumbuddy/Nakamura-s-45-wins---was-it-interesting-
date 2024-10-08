# initiate python
reticulate()

# modules
import pandas as pd
import numpy as np
from plotnine import *

# create function to process data sets
def CheatData_processor(data, eval_range, label, save_name):
  
  # streak frequencies by simulation
  frequency = data.groupby('simID')['streakCount'].value_counts().unstack(fill_value=0)
  frequency = frequency.reset_index().iloc[:,1:]
  frequency_tf = frequency >= 1
  colSums = frequency_tf.sum().reset_index()
  colnames = list(colSums.columns)
  colnames[1] = "freq"
  colSums.columns = colnames
  
  # in how many simuls did we get at least one event above x
  simdata = []
  
  ## for each simul
  for n in range(eval_range[0], eval_range[1] + 1):
    number_of_sims = []
    
    ### for each increasing streak find how many simuls have said streak
    for i in range(0, len(frequency_tf)):
      df = frequency_tf.loc[i] 
      df_new = pd.DataFrame({"streakCount":list(df.index), "present":list(df)})
      outcome = len(df_new[(df_new["present"]) & (df_new["streakCount"] > n)]) > 0
      number_of_sims.append(outcome)
      
    ### append results
    simdata.append([n, sum(number_of_sims)/1000*100])
  
  # store output
  outcomes = pd.DataFrame(simdata, columns = ["Streak","sum"])
  
  # add label
  outcomes["scenario"] = label
  
  # print outcome
  print(outcomes)
  
  # save results
  outcomes.to_csv(save_name, index = False)

# read simul data
data_generous = pd.read_csv("results/results_generous.csv")
data_midway = pd.read_csv("results/results_midway.csv")
data_sceptic = pd.read_csv("results/results_sceptic.csv")
data_chesscom = pd.read_csv("results/results_chesscom.csv")

# process data
CheatData_processor(data = data_generous, eval_range = [1, 300], label = "generous", save_name = "results/percentsimuloutcomes_generous.csv")
CheatData_processor(data = data_midway, eval_range = [1, 300], label = "midway", save_name = "results/percentsimuloutcomes_midway.csv")
CheatData_processor(data = data_sceptic, eval_range = [1, 300], label = "sceptic", save_name = "results/percentsimuloutcomes_sceptic.csv")
CheatData_processor(data = data_chesscom, eval_range = [1, 300], label = "Chess.com", save_name = "results/percentsimuloutcomes_chesscom.csv")

# keep only first sim of each and add
data_generous_1sim = data_generous[data_generous["simID"] == 1]
data_midway_1sim = data_midway[data_midway["simID"] == 1]
data_sceptic_1sim = data_sceptic[data_sceptic["simID"] == 1]
data_chesscom_1sim = data_chesscom[data_chesscom["simID"] == 1]

# save to csv
data_generous_1sim.to_csv("results/data_generous_1sim.csv", index = False)
data_midway_1sim.to_csv("results/data_midway_1sim.csv", index = False)
data_sceptic_1sim.to_csv("results/data_sceptic_1sim.csv", index = False)
data_chesscom_1sim.to_csv("results/data_chesscom_1sim.csv", index = False)

#############################################################
####    count number of games played by each opponent    ####
#############################################################
# read pgns
pgn = open("chesscom_winstreak_games.pgn","r")

# open as readable text
pgn_content = pgn.read()

# prepare list for string search outcomes
white = []
black = []

# extract white and black players
for item in pgn_content.split("\n"):
  if "[White " in item:
    white.append(item.strip())
  if "[Black " in item:
    black.append(item.strip())

# combine lists
allgames = white + black

# create frequency table
allgames_df = pd.DataFrame(allgames, columns = ["player"])
allgames_df["player"].value_counts().reset_index()

# calculate opponent rating
FIDE = np.repeat([2478, 2260, 2279, 2417, 2379, 2584], [16, 9, 8, 8, 3, 1])
FIDE_df = pd.DataFrame(FIDE, columns = ["FIDE"])
FIDE_df["FIDE"].quantile([0.25,0.5,0.75])
FIDE_df.quantile(q=[0.25, 0.75], axis=0, numeric_only=True, interpolation='midpoint')
2584 - (2584 - 2384)/2
FIDE_df["FIDE"].mean()

chesscom = np.repeat([3026, 2990, 3132, 2977, 3104, 3140], [16, 9, 8, 8, 3, 1])
chesscom_df = pd.DataFrame(chesscom, columns = ["chesscom"])
chesscom_df["chesscom"].mean()

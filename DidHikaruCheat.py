# initiate python
reticulate()

# modules
import pandas as pd
import numpy as np
import random

# function to carry out a single simulation of ngames
def set_simulation_event(simID, ngames, tilt_factor = 1.00, winprop = 1.00, drawprop = 0.00):
  
  # initialize counters and objects
  streakID = 0
  streakCounter = 0
  drawCounter = 0
  streakCounter_alt = 0
  drawCounter_alt = 0
  data = []
  
  # draw a game and tally up streak durations
  for i in range(1,ngames+1):
    
    # define tilt factor
    if streakCounter > 5:
      win_prop_actual = winprop*tilt_factor
      draw_prop_actual = drawprop
      loss_prop_actual = 1 - win_prop_actual - draw_prop_actual
    else:
      win_prop_actual = winprop
      draw_prop_actual = drawprop
      loss_prop_actual = 1 - win_prop_actual - draw_prop_actual
    
    # play game
    game_outcomes = ["w", "d", "l"]
    weights = [win_prop_actual, draw_prop_actual, loss_prop_actual]
    outcome = random.choices(game_outcomes, weights, k = 1)[0]
    
    # if win
    ## when one streakcounter should run (second streakcounter may be added further down based on conditions)
    if outcome == "w" and drawCounter == 0 and i < ngames:
      streakCounter = streakCounter + 1
    
    ## when both streakcounters should run and can run   
    if outcome == "w" and drawCounter == 1 and i < ngames:
      streakCounter = streakCounter + 1
      streakCounter_alt = streakCounter_alt + 1
      
    ## when second streakcounter must be added (this avoids certain scenarios) 
    if outcome == "w" and drawCounter_alt == 1 and i < ngames:
      streakCounter_alt = streakCounter_alt + 1
    
    # if draw
    if outcome == "d" and i < ngames:
      # add draw to both draw counters
      drawCounter = drawCounter + 1
      drawCounter_alt = drawCounter_alt + 1
      # check to see if d is a second (or more) d in a row (and reset if so)
      if streakCounter == 0 and streakCounter_alt == 0 and drawCounter == 1 and drawCounter_alt == 1:
        drawCounter = 0
        drawCounter_alt = 0
      # check if draw counters are the same after potential reset above (this marks beginning of streak)
      if drawCounter == 1 and drawCounter_alt == 1:
        drawCounter_alt = drawCounter_alt - 1
      # check if d ends the streak of the first counter
      if drawCounter == 2:
        data.append([simID, streakID, streakCounter])
        streakCounter = 0
        drawCounter = 0
      # check if d ends the streak of the second counter
      if drawCounter_alt == 2:
        data.append([simID, streakID, streakCounter_alt])
        streakCounter_alt = 0
        drawCounter_alt = 0
    
    # when outcome is a win that should be added to the first streak counter and it is the final game
    if outcome == "w" and drawCounter == 0 and i == ngames:
      streakCounter = streakCounter + 1
      data.append([simID, streakID, streakCounter])
    
    # when outcome is a win that should be added to both streak counters and it is the final game
    if outcome == "w" and drawCounter == 1 and i == ngames:
      streakCounter = streakCounter + 1
      streakCounter_alt = streakCounter_alt + 1
      data.append([simID, streakID, streakCounter])
      data.append([simID, streakID, streakCounter_alt])
    
    # when outcome is a draw, and it is the final game  
    if outcome == "d" and i == ngames:
      data.append([simID, streakID, streakCounter])
      data.append([simID, streakID, streakCounter_alt])
      
    # when outcome is a loss
    if outcome == "l":
      data.append([simID, streakID, streakCounter])
      data.append([simID, streakID, streakCounter_alt])
      streakCounter = 0
      streakCounter_alt = 0
      drawCounter = 0
      drawCounter_alt = 0
  
  # function return    
  return(data)

# build simulator
def chess_streak_simulator(ngames, nsim, winprop, drawprop, tilt_factor, save_name):
  
  # create data object to store simulation data
  sim_outcomes = []
  
  # run simulations
  for i in range(1, nsim+1):   
    # carry simulations out
    sim_outcomes.append(set_simulation_event(simID = i, ngames = ngames, winprop = winprop, drawprop = drawprop, tilt_factor = tilt_factor))
    # print iteration number to keep track
    print(i)
    
  # flatten list
  sim_outcomes_flat = [item for sublist in sim_outcomes for item in sublist]
    
  # convert to DataFrame
  sim_outcomes_df = pd.DataFrame(sim_outcomes_flat, columns = ["simID","streakID","streakCount"])
    
  # save results to disc
  sim_outcomes_df.to_csv(save_name, index = False)

################################################################################
# run experiments
################################################################################
# Generous scenario
chess_streak_simulator(ngames = 25000, nsim = 1000, winprop = 0.950, drawprop = 0.046, tilt_factor = 1.00, save_name = "results/results_generous.csv")

# Midway scenario
chess_streak_simulator(ngames = 20000, nsim = 1000, winprop = 0.894, drawprop = 0.096, tilt_factor = 1.00, save_name = "results/results_midway.csv")

# Sceptic scenario 
chess_streak_simulator(ngames = 15000, nsim = 1000, winprop = 0.800, drawprop = 0.179, tilt_factor = 1.00, save_name = "results/results_sceptic.csv")

# Sceptic scenario 
chess_streak_simulator(ngames = 20000, nsim = 1000, winprop = 0.808, drawprop = 0.187, tilt_factor = 1.00, save_name = "results/results_chesscom.csv")


# TEST
def set_simulation_event(simID, ngames, tilt_factor = 1.00, winprop = 1.00, drawprop = 0.00):
  
  # initialize counters and objects
  streakID = 0
  streakCounter = 0
  drawCounter = 0
  streakCounter_alt = 0
  drawCounter_alt = 0
  data = []
  
  # draw a game and tally up streak durations
  for i in range(1,ngames+1):
    
    # define tilt factor
    if streakCounter > 5:
      win_prop_actual = winprop*tilt_factor
      draw_prop_actual = drawprop
      loss_prop_actual = 1 - win_prop_actual - draw_prop_actual
    else:
      win_prop_actual = winprop
      draw_prop_actual = drawprop
      loss_prop_actual = 1 - win_prop_actual - draw_prop_actual
    
    # play game
    game_outcomes = ["w", "d", "l"]
    weights = [win_prop_actual, draw_prop_actual, loss_prop_actual]
    outcome = random.choices(game_outcomes, weights, k = 1)[0]
    print(outcome)
    
    # if win
    ## when one streakcounter should run (second streakcounter may be added further down based on conditions)
    if outcome == "w" and drawCounter == 0 and i < ngames:
      streakCounter = streakCounter + 1
    
    ## when both streakcounters should run and can run   
    if outcome == "w" and drawCounter == 1 and i < ngames:
      streakCounter = streakCounter + 1
      streakCounter_alt = streakCounter_alt + 1
      
    ## when second streakcounter must be added (this avoids certain scenarios) 
    if outcome == "w" and drawCounter_alt == 1 and i < ngames:
      streakCounter_alt = streakCounter_alt + 1
    
    # if draw
    if outcome == "d" and i < ngames:
      # add draw to both draw counters
      drawCounter = drawCounter + 1
      drawCounter_alt = drawCounter_alt + 1
      # check to see if d is a second (or more) d in a row (and reset if so)
      if streakCounter == 0 and streakCounter_alt == 0 and drawCounter == 1 and drawCounter_alt == 1:
        drawCounter = 0
        drawCounter_alt = 0
      # check if draw counters are the same after potential reset above (this marks beginning of streak)
      if drawCounter == 1 and drawCounter_alt == 1:
        drawCounter_alt = drawCounter_alt - 1
      # check if d ends the streak of the first counter
      if drawCounter == 2:
        data.append([simID, streakID, streakCounter])
        streakCounter = 0
        drawCounter = 0
      # check if d ends the streak of the second counter
      if drawCounter_alt == 2:
        data.append([simID, streakID, streakCounter_alt])
        streakCounter_alt = 0
        drawCounter_alt = 0
    
    # when outcome is a win that should be added to the first streak counter and it is the final game
    if outcome == "w" and drawCounter == 0 and i == ngames:
      streakCounter = streakCounter + 1
      data.append([simID, streakID, streakCounter])
    
    # when outcome is a win that should be added to both streak counters and it is the final game
    if outcome == "w" and drawCounter == 1 and i == ngames:
      streakCounter = streakCounter + 1
      streakCounter_alt = streakCounter_alt + 1
      data.append([simID, streakID, streakCounter])
      data.append([simID, streakID, streakCounter_alt])
    
    # when outcome is a draw, and it is the final game  
    if outcome == "d" and i == ngames:
      data.append([simID, streakID, streakCounter])
      data.append([simID, streakID, streakCounter_alt])
      
    # when outcome is a loss
    if outcome == "l":
      data.append([simID, streakID, streakCounter])
      data.append([simID, streakID, streakCounter_alt])
      streakCounter = 0
      streakCounter_alt = 0
      drawCounter = 0
      drawCounter_alt = 0
  
  # function return    
  return(data)

#set_simulation_event(simID = "test", ngames = 10, winprop = 0.85, drawprop = 0.10)


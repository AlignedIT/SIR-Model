# SIR-Model
# Trying to model this on DWave will have a number of challenges

# It has to be decided what is being measured and optimized

# The output from DWave will be binary {0,1}
# Thus the output variable has to be picked that is relevant
# and is can be represented as a binary choice

# A QUBO formulation is needed keeping in mind that DWave
# uses to QUBO to find a minimum energy configuration

# What is the minimum configuration that we are looking for?

# Do we want to take time into consideration? Or is this based on x?

# Also the problem should not have a trivial answer like 
#      transmission factor=0, or gamma=0 

#Step1: Convert the formulation into an optimziation problem with a minimum at t=infinity

#       For example, how can the number of dead be minimized
#                    how can the number of infected by minimized
#                    Optimal lockdown policy (shortest lockdown per location, and shortest total lockdown)
#                            This needs to consider effects of opening up and resurgences

#Step2: Convert the formulation to include a lockdown variable between each location x[i],x[i+1]
#       look at different models where infection has already spread within the population
#       The model should allow for changing the transmission, infection and death rates per location (rather than an average)
#       The model already allows for changing the population per location (this could be seen as population density)

# The lockdown variable will be the boolian {1,0}. We will consider this to be a wall between two infected spots
#      Assumption 
#         a) that a lockdown is only done once
#         b) The lockdown start can be specified.  It might be too late for some, 
#           but does any lockdown configuration minimize deaths
#         c) Does the lockdown 
# The lockdown should have a cost associated, which needs to be minimized 
# along with the cost of deaths and/or maximum number of infected at a location
# 
# Note: In order to connect locations together in a i to j configuration, each location can have travel or transmission
# with any other location due to air and other travel.

# Even though the initial model is 1-D with max x, the final model will see each n as a separate location, with connections
#         between each location. Thus the lockdown will be on each edge, while the initial conditions will be on each node
#         This means that the lockdown will be the qubit turned {1} while the bias on the qubit will indicate travel parameters
#         While the coupling will be the initial condition of the city (or location)

# Alternative formulation can be where a lockdown is on the node, thus the city is the qubit. And it represents the city 
#         is entirely closed. And the edges will be the connections between the city and thus the coupling.

# Possible scenarios and answers
# 
# 1. will the optimal answer always be to shut everthing down?
# 2. Is there a balanced approach where some connections can be shut down while others remain open,
#    Or some cities are shut down while others remain open?
#    What is the impact to total deaths of partial opening
#    What is the impact of reopening to resurgence

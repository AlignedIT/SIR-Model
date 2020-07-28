 Introduction:
 
 Hi All,

I am working on a Covid problem for DWave.  I started with the SIR model which describes the transmission of a disease through a number of partial differential equations. I converted this model to a finite element model where I can see the actual transmission with distance through a population, and also with time. 

I am now converting it to an optimization problem that would determine what is the optimal way to balance lockdowns vs keeping cities open.  My current idea is to have each city be respresented by a qubit, and each city to city transmission be respresented as the coupling between qubits (in the finite element model this is the transfer_rate). The goal is for Dwave to balance the negative cost of closing a city (possibly revenue and economy impact) vs the negative cost of keeping it open (which would be the disease transmitted from more infected cities to lower infected cities). When a city is in lockdown it would be represented by 0, when it is open it would be represented by a 1. In other words the city would not be "visible" and not be transmitting any disease when the qubit is 0, while it would be visible when 1.  DWave would be given the initial conditions in terms of the QUBO. These would be initial values on the linear terms (the qubits representing the condition of the city or node), and the quadratic terms (the links, or edges between the cities). These initial conditions in the form of a QUBO would be a snapshot in time, based on the evolution of the finte element model. Next DWave will optimize (and balance) between the negative costs of shutting a city vs the negative cost of staying open. This optimization would give a picture in time of the optimal step to take based on the current outbreaks. Which cities should be kept open and which should be closed. Then the classical algorithm would move the disease forward in time with new outbreaks using the finite element model. Then Dwave would be used to reoptimize the ideal lockdowns. Some cities would open again, others would close.  The goal is to find whether such a hybrid fea-evolution to quantum-optimization can be used to minimize the economic and disease impacts.

This is very preliminary work, and I am open to ideas and questions. 

The SIR model code can be found at https://github.com/AlignedIT/SIR-Model
Some initial ideas are in the readme page. The jupyter code is the SIR finite element model. Anyone interested in working with me in converting this to the optimization formulation and then converting to a QUBO, please let me know. Best place to connect and chat is on LinkedIn  https://www.linkedin.com/in/alexkhanmba/

Alex Khan

Herd vs Lockdown meets Dijkstra Shortest Path (Updated July 28 2020)
=============================================

Aligned IT, LLCA team in India is taking the Herd vs Lockdown COVID SIRD model and applying it to a pressing need of 

a) determining which sections of a city should be optimally locked down

b) what are the optimal routes that can be travelled to avoid lockdown areas

c) how the re-routed traffic further helps or hinders the economy and disease transmission

d) can quantum-annealing inform the most optimized schedule of lockdown taking the above factors to reduce disruption to the economy while also reducing the transmission and impact of the disease

We will continue to inform the D-Wave teams and D-Wave COVID community on our progress.  Please continue to make resources available as we look at new formulations and validate our model and results.



SIR-Model with Objective Function (Updated June 3 2020)
=================================
This version contains an objective function that is balanced and is converted into a QUBO and sent to DWave.

Check out "SIR QUBO reformulate for cities, links and object function.ipynb"
 
SIR-Model with Cities (update May 25th 2020)
====================
Latest updates are in check out: 
"SIR QUBO reformulate to cities and links.ipynb"

I changed the code from 1-D to a set of n cities with links between them.
This is going to be the beginnings of converting the model to a QUBO.
 
 
 SIR-Model (update May 23rd 2020)
 ==========
 Trying to model this on DWave will have a number of challenges

 It has to be decided what is being measured and optimized

 The output from DWave will be binary {0,1}
 Thus the output variable has to be picked that is relevant
 and is can be represented as a binary choice

 A QUBO formulation is needed keeping in mind that DWave
 uses to QUBO to find a minimum energy configuration

 What is the minimum configuration that we are looking for?

 Do we want to take time into consideration? Or is this based on x?

 Also the problem should not have a trivial answer like 
      transmission factor=0, or gamma=0 

Step1: Convert the formulation into an optimization problem with a minimum at t=infinity

       For example, how can the number of dead be minimized
                    How can the number of infected by minimized?
                    Optimal lockdown policy (shortest lockdown per location, and shortest total lockdown)
                            This needs to consider effects of opening up and resurgences

Step2: Convert the formulation to include a lockdown variable between each location x[i],x[i+1]
       look at different models where infection has already spread within the population
       The model should allow for changing the transmission, infection, and death rates per location (rather than an average)
       The model already allows for changing the population per location (this could be seen as population density)

 The lockdown variable will be the Boolean {1,0}. We will consider this to be a wall between two infected spots
      Assumption 
         a) that a lockdown is only done once
         b) The lockdown start can be specified.  It might be too late for some, 
           but does any lockdown configuration minimize deaths
         c) Does the lockdown 
 
 Step 3: Convert to an Optimization problem
 
 The lockdown should have a cost associated, which needs to be minimized 
 along with the cost of deaths and/or maximum number of infected at a location
 
 Note: In order to connect locations together in a i to j configuration, each location can have travel or transmission
 with any other location due to air and other travel.

 Even though the initial model is 1-D with max x, the final model will see each n as a separate location, with connections
         between each location. Thus the lockdown will be on each edge, while the initial conditions will be on each node
         This means that the lockdown will be the qubit turned {1} while the bias on the qubit will indicate travel parameters
         While the coupling will be the initial condition of the city (or location)

 Alternative formulation can be where a lockdown is on the node, thus the city is the qubit. And it represents the city 
         is entirely closed. And the edges will be the connections between the city and thus the coupling.

 Step 4: Possible scenarios and answers
 
 1. Will the optimal answer always be to shut everything down?
 2. Is there a balanced approach where some connections can be shut down while others remain open,
    Or some cities are shut down while others remain open?
    What is the impact to total deaths of partial opening?
    What is the impact of reopening to resurgence?

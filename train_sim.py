#!/usr/bin/env python
import random
import matplotlib.pyplot as plt

# setting train speed
train_speed = 40


## A SIMPLE SIMULATOR OF TRAIN SERVICE RUNS WITH LOADING/UNLOADING AT ONE STATION ##


class Station:
    
    def __init__(self, initial_queue):
        #set the initial population
        self.station_queue_array = [initial_queue]
        self.queue = initial_queue
        self.number_of_steps = 0

    # get function
    def getQueue(self):
        return self.queue

    # get function for station queue array
    def getQueueArray(self):
        return self.station_queue_array

    # for logical printing
    def __repr__(self):
        return str(self.queue)

    # Function to update the current population of the train
    def appendStationQueue(self):
        self.station_queue_array.append(self.queue)

    # Function to increment the station's Population in each iteration
    def incrementQueue(self):
        randomNumber = random.uniform(70, 130) #Change here
        randomNumber = int(randomNumber)
        # Realisation of number of passengers arriving upon each train arrival
        # HEADWAY   = 45 MINUTES
        self.queue = self.queue + randomNumber
        self.number_of_steps = self.number_of_steps + 1
        return randomNumber

#    def addPopulation(self, num):
#        self.queue = self.queue + num
#        return self.queue

    # function to handle the passengers leaving the platform upon each train arrival 
    # HEADWAY  = 45 MINUTES
    def decreaseQueue(self, num):
        self.queue = self.queue - num
        return self.queue

    # randomly dropping people from station
    def decreaseRandomQueue(self):
        random_queue = random.uniform(35, 65) 
        random_queue = int(random_queue)
        self.queue = self.queue - random_queue
        return random_queue



class Train:
    
    def __init__(self, initial_occu, array_of_stops, max_capacity):
        # initializing the initial train occupancies,
        # array of stops set by user,
        # and current stop of the train, and number of steps.
        self.train_occu_array = [initial_occu]
        self.occu = initial_occu
        self.stops_array = array_of_stops
        self.current_index = 0
        self.number_of_steps = 0
        self.max_capacity = max_capacity


    # get function for train occupancies
    def getOccu(self):
        return self.occu

    def addCurrentOccu(self, occu):
        self.train_occu_array.append(occu)

    # for logical printing
    def __repr__(self):
        # returns the population and array of stops in an arranged fashion
        return "[" + str(self.occu) + ": " + str(self.stops_array) + " : " + str(self.current_index) + "]"

    # get function to get current_index(Station)
    def getCurrentIndex(self):
        return self.current_index

    # get function to get current Occupancy Array
    def getOccuArray(self):
        return self.train_occu_array

    # function to let passengers off the train
    def dropOccu(self):
        # random percentage of people will drop off the
        # train, that random percent will be in the range 15% - 35 %
        dropPercent = random.uniform(0.15, 0.35) #set here
        # dropvalue = droppercent * current_population
        dropValue = int(dropPercent * self.occu)
        # adjusting the current population
        self.occu = self.occu - dropValue
        ## HEADWAY  = 45 MINUTES
        return dropValue

    def addOccu(self, num):
        # this function increases the current_occu with passengers getting on-board
        self.occu = self.occu + num
        ## ONE ITERATION  = 45 MINUTES
        return self.occu

    # function to move train to the next station
    # Error handling done!(boundary condition)
    def nextIndex(self):
        # incrementing the train to next stop
        self.current_index = self.current_index + 1
        # boundary condition check
        if self.current_index > len(self.stops_array):
            self.current_index = 0
        # returning the variable for testing
        self.number_of_steps = self.number_of_steps + 1
        return self.current_index

    # getter function for number of steps
    def getNumberOfSteps(self):
        return self.number_of_steps


##  Function that plot graph
def showGraph(array, xlab, ylab, name_of_file):
    ## X axis = iteration == some constant time value ex: 45 mins
    plt.figure() # plt.figure(figsize=(24,16))
    plt.title(name_of_file)
    if "velocity" in name_of_file:
        plt.plot([k+1 for k in range(len(array))], array, 'bo-')
    else:
        plt.plot([k+1 for k in range(len(array))], array, 'bo:')
    # setting x and y label
    plt.xlabel(xlab)
    plt.ylabel(ylab)

    if "station" in name_of_file:
        plt.savefig("station_image/"+name_of_file+".png")

    elif "train" in name_of_file:
        plt.savefig("train_image/"+name_of_file+".png")
    else:
        plt.savefig("speed_graph.png")
    #plt.close()
    plt.show()



## Function to simulate the one time of each frame,
## this function takes the train object as it's output
def runTrainOnce(train, train_array, station_array):
    ## using get function
    platform_index = train.getCurrentIndex()

    station = station_array[platform_index]
    # random number of people arrive at the station
    station_increment = station.incrementQueue()
    # people getting off the train, and also coming out of the
    # station => no accumulation of passengers
    drop_occu = train.dropOccu()
    station.decreaseQueue(drop_occu)
    remove_random = station.decreaseRandomQueue()
    if train.getOccu() + remove_random <= train.max_capacity:
        train.addOccu(remove_random)
        # safely going to next station,
        # without index outOfBound Exception
        train.nextIndex()
        ## Adding population to the  train's object array
        train.addCurrentOccu(train.getOccu())
        ## Adding population to station object's array
        station.appendStationQueue()
    else:
        station.addQueue(remove_random)
    print(train)




## Main Function
if __name__ == "__main__":
    #Array of station objects
    station_array = [Station(1000) for i in range(5)] #set here
    #Array of train objects
    ##                       CONSTRUCTOR DESCRIPTION            ##
    ## Train(initial_population, [array of stations in which this train is gonna stop.])
    #set here
    train_array = [Train(0,[0,1,2,3],400), Train(250,[0,1,2,3],400), Train(230,[0,1,2,3],400)]
    print("station_array: ", station_array)
    print("train_array: ", train_array)

    ## running each train fixed number of times
    ## can be varied, just change the number in range(num)
    for i in range(100):
        print("TRAIN RUN " + str(i+1) + "\n")
        print("     =====     ")
        for train in train_array:
            runTrainOnce(train, train_array, station_array)
        print("     =====     \n")
        print("station_array: ", station_array)
        print("\n")
        print("train_array: ", train_array)
        print("\n--------------------------------\n")


    print("\n\n\n FINAL TRAIN OCCUPANCIES")
    print("------------------------------------------\n\n\n")
    for train in train_array:
        #pass
        print(str(train.getOccuArray()) + str("\n"))


    print("\n\n\n FINAL STATION QUEUES")
    print("------------------------------------------ \n\n\n")
    for station in station_array:
        #pass
        print(str(station.getQueueArray()) + str("\n"))



## Generating plots 

    for i in range(len(train_array)):
        showGraph(train_array[i].getOccuArray(), "train run", "occupancy", "train_number_" + str(i+1))
    
    for i in range(len(station_array)):
        showGraph(station_array[i].getQueueArray(), "train run", "queue length", "station_number_" + str(i+1))


    showGraph([train_speed for i in range(40)],"time", "speed", "speed_graph")



############################################    END OF FILE    #################################













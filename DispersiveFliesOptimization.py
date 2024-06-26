import numpy as np
import matplotlib.pyplot as plt


class DispersiveFliesOptimization :
    '''
    this class implements the Dispersive Flies Optimization algorithm
    '''
    def __init__(self, num_flies, env_bounds, dim, delta,max_iter) :

        self.num_flies = num_flies # the number of flies in our environement
        self.bounds = env_bounds # the bounds of the optimization environment
        self.dim = dim # the dimension of our optimization space (number of features)
        self.max_iter = max_iter # max number of iterations
        self.delta = delta # disturbence threashold

        # we initialize the positions of flies and their fitness with an empty array
        self.positions = self.initilize_flies()
        self.fitness = np.empty([self.num_flies, 1])

    def fitness_function(self, x):
        '''
        sphere fitness function for a fly 
        '''
        sum = 0
        for feature in x : 
            sum += feature ** 2
        return sum  + 1
    

    def initilize_flies(self):
        '''
        this function is used to initialize the positions of the flies following a bounded uniform distribution 
        '''
        pos = np.empty([self.num_flies, self.dim])
        for fly in range(self.num_flies):
            for ft in range(self.dim):
                pos[fly][ft] = np.random.uniform(-self.bounds, self.bounds)
        return pos

    def train(self):
        """
        find the best firefly position to optimize the problem. 
        """

        # we initialize the positions of our flies in the environement
        self.initilize_flies()
  
        best_fly = 0

        for itr in range(self.max_iter):
            
            # we calculate the fitness of each fly 
            for fly in range(self.num_flies):
                self.fitness[fly] = self.fitness_function(self.positions[fly])
            
            # we extract the position of the best fly with the lowest fitness
            best_idx = np.argmin(self.fitness)
            best_fly = self.positions[best_idx]

            print('the current best fly pos :' , best_fly, 'with value :', self.fitness_function(best_fly))

            for fly in range(self.num_flies): 
                
                if fly != best_idx : 
                    left_idx, right_idx = self.positions[(fly-1)%self.num_flies], self.positions[(fly+1)%self.num_flies]  
                    Xi = left_idx if self.fitness_function(left_idx) < self.fitness_function(right_idx) else right_idx    

                    for ft in range(self.dim):
                        
                        if np.random.uniform() < self.delta:
                            self.positions[fly][ft] = np.random.uniform(-self.bounds, self.bounds)
                        
                        else:
                            u = np.random.uniform()
                            self.positions[fly][ft] = Xi[ft] + u * (best_fly[ft] - self.positions[fly][ft])
                            
                            if self.positions[fly][ft] < (- self.bounds) or self.positions[fly][ft] > self.bounds : 
                                self.positions[fly][ft] = np.random.uniform(-self.bounds, self.bounds)
        
        return best_fly

        

if __name__ == '__main__':

    plt.figure()
    inst = DispersiveFliesOptimization(1000, 5, 2, 0.001, 1000)
    plt.scatter(inst.positions[:, 0],inst.positions[:, 1], c ='b')
    res = inst.train()
    print('the best fly :', res)
    plt.scatter(inst.positions[:, 0],inst.positions[:, 1], c='r')
    plt.show()







import numpy as np
import Ind

def FeedForward(indvs:Ind.Indvs,X:np.ndarray):
    #m: layer i's number of nerons, n: layer (i+1)'s number of nerons
    Y = X.copy() #[num of ind, 1, m]
    for i in range(len(indvs.layersW)): #num of layers - 1 OLHA
        Y = np.matmul(Y,indvs.layersW[i]) #[num of ind, 1, m] x [num of ind, m, n] = 
                                          #= [num of ind, 1, n]
        Y += indvs.layersB[i] #[num of ind, 1, n] + [num of ind, 1, n]
        Y = indvs.functions[i](Y)
        print("\n\noutputs: ",Y.shape,"\n",Y)
    return Y


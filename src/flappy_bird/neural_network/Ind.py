import numpy as np

class Indvs():
    def __init__(self,disp:list[int],
                 functions,
                 layersWB:list[list[np.ndarray]]):
        #m: layer i's number of nerons, n: layer (i+1)'s number of nerons
        # 0 <= i <= num of layers - 1
        self.layersW = layersWB[0] #[num of layers - 1, num of ind, m, n] 
        self.layersB = layersWB[1] #[num of layers - 1, num of ind, 1, n] 
        self.disp = disp #number of neurons in each layer (doesn't evolve) [num of layers]
        self.functions = functions #activation functions (don't evolve) [num of layers - 1]
                                   #function's input format: [num of ind, 1, n]
        self.ids  = np.arange((self.layersB[0].shape[0])) #array from 0 to num of ind
        self.idsC = len(self.ids) #number of individuals
        #self.attr = Attr(...)
        
    #remove especified individuals by ids
    def remove(self, ids):
        removeIDS = np.where(self.ids==ids)
        print("remove ids: ",removeIDS)
        for l in range(len(self.layersB)): #num of layers OLHA
            self.layersB[l] = np.delete(self.layersB[l],removeIDS,axis=0)
            self.layersW[l] = np.delete(self.layersW[l],removeIDS,axis=0)
        self.ids = np.delete(self.ids,removeIDS)
        
    #add individuals, need to inform their weights and bias
    def add(self, addlayersWB):
        for l in range(len(self.layersB)): #num of layers OLHA
            np.insert(self.layersB[l],0,addlayersWB[1][l],axis=0)
            np.insert(self.layersW[l],0,addlayersWB[0][l],axis=0)
            #nao precisa atualizar os ids? OLHA
            
    #return weights and bias of especified individuals by ids
    def takeMultiple(self,idsselect:np.ndarray):
        Wcopy = []
        Bcopy = []
        for l in range(len(self.layersW)): #num of layers - 1 OLHA
            Wcopy.append( self.layersW[l][idsselect,:,:] )
            Bcopy.append( self.layersB[l][idsselect,:,:] )
        return [Wcopy.copy(),Bcopy.copy()]
    
    #return weights and bias of one especified individual by id
    def takeOne(self,idselect:int):
        Wcopy = []
        Bcopy = []
        for l in range(len(self.layersW)): #num of layers - 1 OLHA
            Wcopy.append(self.layersW[l][idselect, :, :])
            Bcopy.append(self.layersB[l][idselect, :, :])
        return [Wcopy.copy(), Bcopy.copy()]
    
    #print the disposition, and the dimentions of layersW and layersB
    def dispositionTest(self):
        print("disposition [SETTED]: ",self.disp)
        print("Weights:")
        for l in range(len(self.layersW)): #num of layers - 1
            print("  --> ",self.layersW[l].shape)
        print("Biases:")
        for l in range(len(self.layersB)): #num of layers
            print("  --> ",self.layersB[l].shape)
            
    #[number of individuals, 1, number of inputs]
    def getInputShape(self):
        return np.array([self.layersW[0].shape[0],1,self.layersW[0].shape[1]])

class Attr():
    def __init__(self,qind):
        #self.vetorposition = np.array(qind ...)
        self.score = np.zeros([qind,],dtype=float)
        #self.direcaodecorpo
        #self.direcaodevisao
        #self.vetorvelocidade
        #self.vetoraceleracao


        ##Separar entre comportamentais (mudança na velocidade,direção de visão,pular ou não)[decisões que mudam no brain]
        #             e ambientais (espaço,velocidade etc)[mudam na engine]
        pass
"""
Main cria os blobs, o jogo e a rede
ciclo principal:
    - Jogo retorna as posições (matriz dos obstáculos)      
    - Gerar um tipo de input                                (jogo)
    - Inputs entram na rede neural que gera um output       (rede)
    - O output da rede é transformado em algo "fazivel"     (jogo)
    - Os blobs tomam uma decisão                            (jogo)
    - Decisão é atualizada no jogo                          (jogo)
------------ jogo acabou
- método de pontuação
- seleção natural
- criação de novos blobs
- reinicio
"""
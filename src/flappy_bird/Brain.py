from neural_network import Ind, NNM
from gaming import Game
import pygame



class Brain():
    def __init__(self,jogo,
                 indvs:Ind.Indvs,
                 rede:NNM.Rede,):
        pygame.init()
        game = Game(450, 800)
        
        #define nn's functions and disposition
        #generate initial population
        pass

    def Run(): 
        inputs = game.run(0)
        while(inputs):
            
        
        #       jogo atualiza                           (posições, distancias)
        #transforma dados do jogo em inputs de rede
        #       Feed forward da rede com os inputs
        #tomada de decisão do cérebro com base nos outputs (pula pra cima)
        #       atualiza os atributos comportamentais dos blobs         (tomada de decisão para o próximo round)
        #muda a pontuação dos blobs
        pass
    def Geracao():
        #avaliar os individuos          (pega os scores e monta o fitness)
        #sistema de ranqueamento        [100,98,97,97.97....,96]
        #       seleção dos que sobreviveram   [100,100,100,100]
        #       cria novos individuos (crossover, mutação,aleatorio)
        pass
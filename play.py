import retro
import time
import numpy as np
from rominfo import *
from utils import *
from util import * # meu utils 
import sys

def jogarAgente(agente, gravarInformacoes = False):
    env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', players=1)
    env.reset()

    if gravarInformacoes:
        baseDados = {}
        baseDados["input"] = []
        baseDados["output"] = []

    dead = False
    penalidade = 0 # flag para saber se travou em alguma parede, entrou em loop etc
    score = [0, 0] # grava posicao anterior e a atual
    while not dead:
        ram = getRam(env)

        inputs, x, y = getInputs(ram)

        entrada = gerarEntrada(inputs)

        if gravarInformacoes:
            baseDados["input"].append(entrada.tolist()) 

        agente.feedforward(entrada)

        acao = np.argmax(agente.output)

        if gravarInformacoes:
            baseDados["output"].append(int(acao))

        obs, rew, done, info = env.step(dec2bin(actions_list[acao]))

        dead = ram[0x71]

        env.render()

        score[0] = score[1]
        score[1] = x	
        pontuacao = score[1] - score[0]
        if pontuacao == 0:
            penalidade += 1
        agente.fitness += pontuacao
        if penalidade == 200:
            dead = True
        
        obs = np.array(obs[0])
        if (obs.sum() == 0):
            agente.fitness += 1000
            print("Finalizou !!!")
            break

    print(agente.fitness)
    agente.fitness = 0

    if gravarInformacoes:
        salvarInformacoes( baseDados)

def main(argv):
    gravar = False

    if len(argv) > 1 and argv[1] == 'dados':
        gravar = True

    agente = recuperarMelhorAgente()
    if agente != 0:
        jogarAgente(agente, gravar)
    else:
        print("Não foi possivel recuperar o agente")
    
if __name__ == '__main__':
    main(sys.argv)


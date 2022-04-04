import retro
from rominfo import *
from utils import *
from util import *
from rede_neural import *
import numpy as np
import time
import json
import sys
from play import jogarAgente

def treino(env, players):
	try:
		# flag para indicar se conseguiu atingir o objetivo durante o treinamento
		# primeiro atributo indica se atingiu o objetivo sem interrupção
		# o segundo indica finalizado com interrupção (não é considerado como o melhor agente)
		finalizou = [False, False]

		# contagem para indicar o player atual 
		count = 1 
		for player in players:
			print("player " + str(count), end=' = ')
			
			env.reset()
			dead = False

			# flag/contador para saber se travou em alguma parede, entrou em loop etc
			penalidade = 0 
			# grava posicao anterior e a atual, para contabilizar a pontuacao
			score = [0, 0] 
			while not dead:
				ram = getRam(env)

				inputs, x, y = getInputs(ram)

				entrada = gerarEntrada(inputs)

				player.feedforward(entrada)

				acao = np.argmax(player.output)

				obs, rew, done, info = env.step(dec2bin(actions_list[acao]))

				dead = ram[0x71]

				env.render()

				if atingiuObjetivo(obs):
					player.fitness += 1000
					print(player.fitness)
					print("Atingiu o Objetivo ! lol")
					finalizou[0] = True
					break
				
				score[0] = score[1]
				score[1] = x	
				# pontuacao fica negativa caso escolha se movimentar para a esquerda (evitar loops)
				pontuacao = score[1] - score[0]	

				# recebe punicao caso não tenha avanço
				if pontuacao == 0:
					penalidade += 1

				# se receber 200 punicoes, provavelmente é pq está em loop ou travado em algum obstáculo
				if penalidade == 200:
					dead = True

				player.fitness += pontuacao


			print(player.fitness)
			if finalizou[0]:
				break
			
			count += 1

		return getTop(players, 2), finalizou

	except KeyboardInterrupt:
		finalizou[1] = True
		print("\rInterrompido durante o treinamento!")
		return getTop(players, 2), finalizou
	
	except Exception as ex:
		print(str(ex))

def zerarFitness(players):
	for player in players:
		player.fitness = 0

def evolucao(inicio = True, inicioGeracao = 0, melhorAgente = False):
	try:
		env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', players=1)

		start = time.time()
		
		qtdPlayers = int(input("Quantidade de players: "))
		geracoes = int(input("Total de geracoes: "))

		if inicio:
			players = geraPlayers(qtdPlayers)
		elif melhorAgente:
			players = geraPlayers(qtdPlayers, inicio = False, melhor = True)
		else:
			players = geraPlayers(qtdPlayers, inicio = False, geracao = inicioGeracao)
		
		if len(players) == 0:
			raise Exception("Não foi possivel gerar players")

		# flag para indicar se o treinamento gerou um agente que terminou a fase
		mestre = False

		# contador de geracoes
		geracao = 0
		while (geracao < geracoes):
			print("Geracao: ", geracao + 1)
			top, finalizou = treino(env, players) 

			if finalizou[0] or finalizou[1]:
				# seleciona o agente de maior pontuacao
				if finalizou[0]:
					mestre = True

				players[0] = players[list(top.keys())[0]]
				break

			print(top)

			pai, mae = getPaiMae(top, players)

			qtdNovosPlayers = len(players) - 2	
			players = []

			players.append(pai)
			players.append(mae)
			filhos = cruzamento(pai, mae, qtdNovosPlayers)
			for f in filhos:
				f.mutacao()
				players.append(f)

			print("Salvando melhor player da {}º geracao ...".format(geracao + 1))
			salvarPlayer(pai, geracao + 1, True, pai.fitness)

			zerarFitness(players)
			geracao += 1
		
		melhorPlayer = players[0]

		final = time.time()
		print("Tempo total:", end=' ')
		mostrarTempo(final - start)

		print("\rSalvando melhor player da {}º geracao ...".format(geracao + 1))
		salvarPlayer(melhorPlayer, geracao, True, melhorPlayer.fitness)
			

	except Exception as ex:
		print(str(ex))

		print("Salvando melhor player da {}º geracao ...".format(geracao + 1))
		salvarPlayer(melhorPlayer, geracao + 1, mestre, melhorPlayer.fitness)

	finally:
		env.close()

def ensinarAgente(dados, geracoes = 10, taxaAprendizagem = 0.3):
	agente = RedeNeural(INPUT, HIDDEN, OUTPUT, taxaAprendizagem)

	total = len(dados["input"])

	for geracao in range(geracoes):
		print("Geracao: {}".format(geracao + 1))

		it = 0 
		for registro in dados["input"]:
			print("{:.2f}%".format(it/total * 100), end='\r')

			entrada = np.array(registro)

			objetivo = np.zeros(OUTPUT) + 0.01
			idx = dados["output"][it]

			objetivo[idx] = 0.99

			agente.treino(entrada, objetivo)

			it += 1

	return agente

def teste(agente, dados):
	score = []

	it = 0 
	for registro in dados["input"]:
		entrada = np.array(registro)

		gabarito = dados["output"][it]

		saida = agente.teste(entrada)

		acao = np.argmax(saida)

		if acao == gabarito:
			score.append(1)
		else:
			score.append(0)

		it += 1

	scoreArray = np.asarray(score)

	resultado = (scoreArray.sum() / scoreArray.size) * 100

	return resultado

def supervisionado():
	dados = getDados()

	if len(dados) == 0:
		print("Não foi possível recuperar os dados base")
		return 

	start = time.time()

	qtdGeracoes = int(input("Total de geracoes: "))

	agente = ensinarAgente(dados, geracoes=qtdGeracoes)
	resultado = teste(agente, dados)
	print("\rPorcentagem aprendizado: {:.1f}%".format(resultado))
	print()

	jogarAgente(agente)

def main(argv):
	try:
		arg = argv[1]

		if arg == 'evolucao':
			arg = argv[2]

			if arg == 'geracao':
				arg = argv[3]

				print(arg)
				evolucao(inicio = False, inicioGeracao = int(arg))
			elif arg == 'melhor':
				evolucao(inicio = False, melhorAgente = True)
			elif arg == 'inicio':
				evolucao()

		elif arg == 'supervisionado':
			supervisionado()
		else:
			print("Argumento invalido")


	except Exception as ex:
		print("Argumento invalido")


if __name__ == "__main__":
	main(sys.argv)
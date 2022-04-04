import json
import copy
from rede_neural import *
from banco_dados import *

INPUT = 6
HIDDEN = 10
OUTPUT = 5

def salvarPlayer(player, geracao, mestre, pontuacao = 0):
	mente = {
		"wInput" : player.wInput.tolist(),
		"wHidden": player.wHidden.tolist()
	}

	mente = json.dumps(mente)

	if mestre:
		mestre = 1
	else:
		mestre = 0
	
	salvarAgente(mente, mestre, geracao, pontuacao)
	
def recuperarMelhorAgente():
	mente = getMenteMelhorAgente()
	if len(mente) > 0:
		agente = RedeNeural(INPUT, HIDDEN, OUTPUT)

		wI = np.array(mente["wInput"])
		wH = np.array(mente["wHidden"])
		agente.mudarGenetica(wI, wH)

		return agente
	
	return 0

def salvarInformacoes(info):
	info = json.dumps(info)
	
	salvarDados(info)

def getAgente(pontuacao = False, n_geracao = 0):

	if pontuacao:
		mente = getMenteMaiorPontuacao()
	else:
		mente = recuperarMenteGeracao(n_geracao)	
	
	if len(mente) > 0:
		agente = RedeNeural(INPUT, HIDDEN, OUTPUT)
		wI = np.array(mente["wInput"])
		wH = np.array(mente["wHidden"])
		agente.mudarGenetica(wI, wH)

		return agente
	
	return 0

def geraPlayers(total, inicio = True, geracao = 0, melhor = False):
	players = []
	
	if inicio:
		for i in range(total):
			players.append(RedeNeural(INPUT, HIDDEN, OUTPUT))
		
		return players
	elif melhor:
		agente = getAgente(pontuacao = True)
	else:
		agente = getAgente(n_geracao = geracao)

	if agente != 0:
		players.append(agente)
		for i in range(total - 1):
			player = copy.deepcopy(agente)
			player.mutacao()
			players.append(player)

	return players

def bin2dec(binario, tamanho):
	dec = 0
	for i in range(len(binario)):
		if binario[i]:
			dec += pow(2, tamanho - i - 1)

	if (tamanho < 32):
		dec = dec << (32 - tamanho)
	return dec

def gerarEntrada(inputs):
	entrada = []
	aux = []
	for i in range(len(inputs)):
		if i % 32 == 0 and i != 0:
			entrada.append(aux)
			aux = []

		aux.append(inputs[i])

	entrada.append(aux)

	
	for i in range(len(entrada)):
		entrada[i] = bin2dec(entrada[i], len(entrada[i]))


	entradaModificada = (np.asfarray(entrada[0:]) / 4294967295 * 0.99) + 0.01

	return entradaModificada

def getRank(players):
	rank = {}

	for i in range(len(players)):
		rank[i] = players[i].fitness

	resultado = dict(sorted(rank.items(), key=lambda item: item[1], reverse=True))

	return resultado

def getPaiMae(top, players):
	casal = []
	for k, v in top.items():
		casal.append(players[k])

	pai = casal[0]
	mae = casal[1]

	return pai, mae

def getTop(players, posicao):
	ranking = getRank(players)

	top = dict(list(ranking.items())[:posicao])

	return top

def atingiuObjetivo(obs):
	obs = np.array(obs[0])
	if (obs.sum() == 0):
		return True
	
	return False

def mostrarTempo(tempo):
	horas = tempo / 3600
	minutos = (tempo % 3600) / 60
	segundos =  (tempo % 3600) % 60

	print("{}h {}m {}s".format(int(horas), int(minutos), int(segundos)))

def getDados():
	dados = recuperarDados()
	
	return dados

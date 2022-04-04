import numpy as np
import scipy.special

class RedeNeural:
    def __init__(self, nEntradas, nHiddens, nSaidas, taxaAprendizagem = 0.2):
        self.nEntradas = nEntradas
        self.nHiddens = nHiddens
        self.nSaidas = nSaidas
        self.taxaAprendizagem = taxaAprendizagem
        
        self.input = []
        self.hidden = 0
        self.output = 0
        self.fitness = 0

        desvioPadraoHidden = pow(nHiddens, -0.5)
        desvioPadraoOutput = pow(nSaidas, -0.5)
        self.wInput = np.random.normal(0, desvioPadraoHidden, (nEntradas, nHiddens))
        self.wHidden = np.random.normal(0, desvioPadraoOutput, (nHiddens, nSaidas))

        self.funcaoAtivacao = lambda x : scipy.special.expit(x) 

    def feedforward(self, entrada):
        self.input = np.array(entrada, ndmin=1)

        self.hidden = self.funcaoAtivacao(np.dot(self.input, self.wInput))
        self.output = self.funcaoAtivacao(np.dot(self.hidden, self.wHidden))

    def backpropagation(self, erros):
        hiddenErros = np.dot(erros, self.wHidden.T)

        tmp = erros * self.output * (1 - self.output) 

        tmp = tmp.reshape((1, tmp.shape[0]))    
        aux = self.hidden.reshape((self.hidden.shape[0], 1))

        w = self.taxaAprendizagem * np.dot(aux, tmp)

        self.wHidden += self.taxaAprendizagem * np.dot(aux, tmp)

        tmp = hiddenErros * self.hidden * (1 - self.hidden)

        tmp = tmp.reshape((1, tmp.shape[0]))    
        aux = self.input.reshape((self.input.shape[0], 1))

        self.wInput += self.taxaAprendizagem * np.dot(aux, tmp)

    def _mudarWInput(self):
        qtd = np.random.randint(5)

        for _ in range(qtd):
            i = np.random.randint(self.nEntradas)
            j = np.random.randint(self.nHiddens)

            self.wInput[i][j] = np.random.uniform(-1, 1)
        
    def _mudarWHidden(self):
        qtd = np.random.randint(5)

        for _ in range(qtd):
            a = np.random.randint(self.nHiddens)
            b = np.random.randint(self.nSaidas)

            self.wHidden[a][b] = np.random.uniform(-1, 1)

    def mutacao(self):
        aleatorio = np.random.randint(100)

        if (aleatorio < 30):
            self._mudarWInput()
        elif (aleatorio < 60):
            self._mudarWHidden()
        else:
            self._mudarWInput()
            self._mudarWHidden()
    
    def mudarGenetica(self, wi, wh):
        self.wInput = wi
        self.wHidden = wh

    def treino(self, entrada, objetivo):
        objetivo = np.array(objetivo, ndmin=1).T

        self.feedforward(entrada)

        erros = objetivo - self.output

        self.backpropagation(erros)

    def teste(self, entrada):
        self.feedforward(entrada)

        return self.output


# Pega uma parte aleatoria do pai e a outra parte da mae e cruza os pesos
def misturarPesos(wPai, wMae, x, y):
    wFilho = []

    for i in range(len(wPai)):
        if i == x:
            break


        wFilho.append([])
        for j in range(len(wPai[i])):
            if j == y:
                break

            wFilho[-1].append(wPai[i][j])

    for i in range(len(wMae)):
        if i >= x:
            wFilho.append([])

        for j in range(len(wMae[i])):
            if i < x and j < y:
                continue

            wFilho[i].append(wMae[i][j])

    return np.array(wFilho)

def cruzamento(p1, p2, qtd):
    filhos = []

    for _ in range(qtd):
        x = np.random.randint(p1.nEntradas)
        y = np.random.randint(p1.nHiddens)
        a = np.random.randint(p1.nHiddens)
        b = np.random.randint(p1.nSaidas)

        wiFilho = misturarPesos(p1.wInput, p2.wInput, x, y)
        whFilho = misturarPesos(p1.wHidden, p2.wHidden, a, b)

        filho = RedeNeural(p1.nEntradas, p1.nHiddens, p1.nSaidas)
        filho.mudarGenetica(wiFilho, whFilho)

        filhos.append(filho)

    return filhos

def main():
    mario = RedeNeural(3, 6, 3)

    mario.feedforward(1, 0, 1)


if __name__ == '__main__':
    main()
O projeto foi dividido em 2 códigos fontes: train.py e play.py

No train.py existe duas possiblidades de treinar um agente a passar de fase YoshiIsland2
do SuperMarioWorld: por evolução e por aprendizado supervisionado.

Em evolução, dada uma quantidade de agentes e número de gerações, serão gerados n
agentes que tentaram completar a fase, sendo que a cada geração os n indivíduos tem
uma nova tentativa. Porém, ao final de uma geração, é gerado um ranking e selecionado
os 2 melhores, que serão considerados como pai e mãe para gerar uma nova população
baseado nas suas genéticas. Cada filho desse casal, sofrerá uma mutação para gerar mais
diversidade na população, evitando soluções que sejam ótimos locais, ou seja, que não
conseguem avançar de um determinado ponto da fase.

Obs: A quantidade de agentes e o número de gerações razoáveis com base nos meus
testes são 50 e 10, respectivamente. Devido a aleatoridade do algoritmo, esses valores
podem ser maiores, mas caso algum agente termine a fase antes, o programa será
finalizado como explicado mais adiante.

Cada indivíduo de uma população possui sua pontuação feita durante sua tentativa, que é
contabilizada levando em conta o quão ele avança na fase, dessa forma, quanto mais
perto do final dela, sua pontuação vai aumentando, e quanto mais se distancia, irá
dimnuindo. Após gerado o ranking baseado na pontuação, o melhor indiíviduo é salvo
na banco de dados para ser recuperado mais a frente caso necessário. Caso ele termine a
fase durante a geração, o programa é finalizado salvando ele no banco.

Obs: Para iniciar o banco de dados, basta usar a seguinte linha de comando: ‘python
banco_dados.py’. Ela criará duas tabelas chamadas agente e informações,
respectivamente. Na primeira, armazenará os agentes, tendo um histórico do melhor
agente de cada geração e também daqueles que solucionaram o problema, indicados com
flag mestre ativa. E a segunda, guarda as informações de input e output do agente que
solucionou o problema, servindo de base para o aprendizado supervisionado explicado
mais à frente.

O uso do programa train.py no modo evolução, existe 3 opções a serem escolhidas. A
primeira segue a seguinte linha de comando: ‘python train.py evolucao inicio’, em que
será gerada uma nova população aleatória de n indivíduos que formarão o início do
processo evolutivo. A segunda opção ‘python train.py evolucao geracao x’ iniciará uma
população com o melhor indíviduo de uma determinada geração realizada em treinos
anterioes, assim, caso ainda não tenha nenhum registro, não será possível utilizar ela
ainda. A útlima opção ‘python train.py evolucao melhor’ selecionará o melhor indíviduo
dos últimos treinos baseado em sua pontuação, portanto, semelhante a opção anterior,
não será possível utilizar se não tiver registros, ou seja, a primeria opção ainda não foi
usada.

Obs: Caso demore muito para aprender, pode ser usado o ctrl + c, que irá setar uma
exceção e o melhor agente da geração atual será salvo finalizando o programa.
Na segunda opção, x representa um inteiro.

O segundo modo do train.py é o aprendizado supervisionado, e que para ser utilizado
deve seguir a seguinte linha de comando:‘python.py train.py supervisionado’. Neste
modo, será recuperado do banco de dados as informações geradas pelo agente de maior
pontuação feita até o momento. A partir disto, será criado uma rede neural que será
treinada com esses dados fornecidos. A cada geração ela passará pelo processo de
feedforward gerando uma determinada ação a ser feita, e corrigida no processo de
backpropagation que leva em conta como gabarito os dados recuperados do banco. Ao
finalizar o total de gerações fornecidas pelo usuário, mostrará o percentual de
desempenho, indicando a proporção de acertos dado a quantidade de dados como
entrada. Em seguida, inicia a sua tentativa de finalizar a fase.

Obs: Para gerar os dados base, deve-se executar comando explicado abaixo. Após isto,
caso eles sejam gerados por um agente que já concluiu a fase, qualquer diferença
durante o aprendizado implica no fracasso do novo indivíduo. Para isso, é necessário
escolher uma quantidade de gerações que resulte em 99% ou mais de desempenho (no
geral, pelo menos 25 gerações).

No programa play.py, será utilizado o agente que conseguiu a maior pontuação durante o
treinamento. Além disso, com a seguinte instrução ‘python play.py dados’ o programa
executará a fase com o melhor agente atual e irá registrar no banco as informações de
input e output que serão usadas para treinar um indíviduo através de aprendizagem
supervisionada.
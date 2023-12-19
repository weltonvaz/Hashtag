from pyamaze import maze, agent
from queue import PriorityQueue

destino = (1, 1)

def h_score(celula, destino):
  return abs(celula[1] - destino[1]) + abs(celula[0] - destino[0])

def proxima_celula(celula, direcao):
  deltas = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}
  return tuple(map(sum, zip(celula, deltas[direcao])))

def aestrela(labirinto):
  f_score = {celula: float("inf") for celula in labirinto.grid}
  g_score = {celula: float("inf") for celula in labirinto.grid}
  celula_inicial = (labirinto.rows, labirinto.cols)
  
  g_score[celula_inicial] = 0
  f_score[celula_inicial] = h_score(celula_inicial, destino)
  
  fila = PriorityQueue()
  fila.put((f_score[celula_inicial], celula_inicial))

  caminho = {}
  while not fila.empty():
    _, celula = fila.get()

    if celula == destino:
      break

    for direcao in "NSEW":
      if labirinto.maze_map[celula][direcao] == 1:
        prox_celula = proxima_celula(celula, direcao)
        novo_g_score = g_score[celula] + 1
        novo_f_score = novo_g_score + h_score(prox_celula, destino)

        if novo_f_score < f_score[prox_celula]:
          f_score[prox_celula] = novo_f_score
          g_score[prox_celula] = novo_g_score
          fila.put((novo_f_score, prox_celula))
          caminho[prox_celula] = celula

  caminho_final = {}
  celula_analisada = destino
  while celula_analisada != celula_inicial:
    caminho_final[caminho[celula_analisada]] = celula_analisada
    celula_analisada = caminho[celula_analisada]
  return caminho_final

labirinto = maze(50, 50)
labirinto.CreateMaze()

agente = agent(labirinto, filled=True, footprints=True)
caminho = aestrela(labirinto)
labirinto.tracePath({agente: caminho}, delay=10)

labirinto.run()

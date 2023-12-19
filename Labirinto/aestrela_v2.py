from pyamaze import maze, agent
from queue import PriorityQueue

destino = (1, 1)

def h_score(celula, destino):
    linhac, colunac = celula
    linhad, colunad = destino
    return abs(colunac - colunad) + abs(linhac - linhad)

def aestrela(labirinto):
    f_score = {celula: float("inf") for celula in labirinto.grid}
    g_score = {celula: float("inf") for celula in labirinto.grid}
    
    celula_inicial = (labirinto.rows, labirinto.cols)
    g_score[celula_inicial] = 0
    f_score[celula_inicial] = g_score[celula_inicial] + h_score(celula_inicial, destino)

    fila = PriorityQueue()
    fila.put((f_score[celula_inicial], h_score(celula_inicial, destino), celula_inicial))

    caminho = {}
    while not fila.empty():
        _, _, celula = fila.get()

        if celula == destino:
            break

        for direcao in "NSEW":
            if labirinto.maze_map[celula][direcao] == 1:
                linha_celula, coluna_celula = celula
                movimentos = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}
                proxima_celula = (linha_celula + movimentos[direcao][0], coluna_celula + movimentos[direcao][1])

                novo_g_score = g_score[celula] + 1
                novo_f_score = novo_g_score + h_score(proxima_celula, destino)

                if novo_f_score < f_score[proxima_celula]:
                    f_score[proxima_celula] = novo_f_score
                    g_score[proxima_celula] = novo_g_score
                    fila.put((novo_f_score, h_score(proxima_celula, destino), proxima_celula))
                    caminho[proxima_celula] = celula

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

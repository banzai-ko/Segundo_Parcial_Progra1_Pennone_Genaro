from settings import (
 RANK_FILE,
)

def sort_matrix(matrix: list[list]):
    for i in range(len(matrix) - 1):
        for j in range(i + 1, len(matrix)):
            # Ensure the second element is an integer (score) and compare
            try:
                if int(matrix[i][1].strip()) > int(matrix[j][1].strip()):
                    matrix[i], matrix[j] = matrix[j], matrix[i]
            except ValueError:
                # Handle cases where the score is not an integer
                continue



def ranking(file):
    ranking = []
    with open(file, 'r') as rkng:
        lineas = rkng.read()
        for linea in lineas.split('\n'):
            ranking.append(linea.split(','))
    
    sort_matrix(ranking)
    
    return ranking
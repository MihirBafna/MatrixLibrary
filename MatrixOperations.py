import numpy as np

def loadMatrix(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    rows = len(lines)
    cols = len(lines[0].split())
    matrix = np.zeros(shape=(rows, cols))
    for i in range(rows):
        line = lines[i].split()
        for j in range(cols):
            matrix[i][j] = line[j]
    print("matrix loaded ...")
    return matrix

def numCols(matrix):
    return len(matrix[0])

def numRows(matrix):
    return len(matrix)


def transpose(mat):
    rows = numRows(mat)
    cols = numCols(mat)
    matrix = np.zeros(shape=(cols, rows))
    for i in range(rows):
        for j in range(cols):
            matrix[j][i] = mat[i][j]
    return matrix


def isVector(matrix):
    rows = numRows(matrix)
    cols = numCols(matrix)
    return (cols == 1 or rows == 1)


def isSquare(matrix):
    return numCols(matrix) == numRows(matrix)


def identity(dim):
    matrix = np.zeros(shape=(dim, dim))
    for i in range(dim):
        for j in range(dim):
            if i == j:
                matrix[i][j] = 1
    return matrix


def add(mat1,mat2):
    if numRows(mat1) != numRows(mat2) or numCols(mat1) != numCols(mat2):
        print( "ERROR: operation not possible")
    else:
        rows = numRows(mat1)
        cols = numCols(mat1)
        matrix = np.zeros(shape=(rows, cols))
        for i in range(rows):
            for j in range(cols):
                matrix[i][j] = mat1[i][j]+mat2[i][j]
        return matrix


def subtract(mat1, mat2):
    if numRows(mat1) != numRows(mat2) or numCols(mat1) != numCols(mat2):
        print("ERROR: operation not possible")
    else:
        rows = numRows(mat1)
        cols = numCols(mat1)
        matrix = np.zeros(shape=(rows, cols))
        for i in range(rows):
            for j in range(cols):
                matrix[i][j] = mat1[i][j]-mat2[i][j]
        return matrix
            
def scale(mat,scale):
    rows = numRows(mat)
    cols = numCols(mat)
    matrix = np.zeros(shape=(rows, cols))
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = scale*mat[i][j]
    return matrix


def dot(vector1,vector2):
    rows1 = numRows(vector1)
    rows2 = numRows(vector2)
    cols1 = numCols(vector1)
    cols2 = numCols(vector2)
    ans = 0
    if(cols1 == 1):
        vector1 = transpose(vector1)
    if(rows2==1):
        vector2 = transpose(vector2)
    if(numCols(vector1)!=numRows(vector2)):
        return "ERROR: vectors must be in the same dimension (same # of entries)"
    if(isVector(vector1) and isVector(vector2)):
        for i in range(numCols(vector1)):
            ans+=vector1[0][i]*vector2[i][0]
    else:
        return "ERROR: must use a vector (single column matrix) to use the dot() function"
    return ans

# def cross(vector1,vector2):
#     rows1 = numRows(vector1)
#     rows2 = numRows(vector2)
#     cols1 = numCols(vector1)
#     cols2 = numCols(vector2)
#     ans = np.zeros(shape=(1, 3))
#     if(cols1 == 1):
#         vector1 = transpose(vector1)
#     if(rows2==1):
#         vector2 = transpose(vector2)
#     if(numCols(vector1)!=numRows(vector2)):
#         return "ERROR: vectors must be in the same dimension (same # of entries)"
#     if(isVector(vector1) and isVector(vector2)):
#         for i in range(numCols(vector1)):
#             ans += vector1[0][i]*vector2[i][0]
#     else:
#         return "ERROR: must use a vector (single column matrix) for the cross() function"
#     return ans

def multiply(mat1,mat2):
    rows1 = numRows(mat1)
    rows2 = numRows(mat2)
    cols1 = numCols(mat1)
    cols2 = numCols(mat2)
    if cols1 != rows2:
        return "ERROR: to be multiplied, the # of columns in matrix 1 must be equal to the # of rows in matrix 2"
    ans = np.zeros(shape=(rows1,cols2))
    for i in range(rows1):
        for j in range(cols2):
            for n in range(cols1):
                ans[i][j] += mat1[i][n]*mat2[n][j]
    return ans

def swap(matrix,row1,row2):
    temp = matrix[row1]
    matrix[row1] = matrix[row2]
    matrix[row2] = temp
    return matrix

def pivot(matrix, colindex):
    i = colindex
    rows = numRows(matrix)
    while matrix[i][colindex] == 0:
        if(i>=rows-1):
            i=-1
            break
        i += 1
    return i


def echelon(matrix):
    rows = numRows(matrix)
    cols = numCols(matrix)
    for n in range(min(rows, cols)):
        pivotpos = pivot(matrix, n)
        if (pivotpos == -1):
            break
        matrix = swap(matrix, n, pivotpos)
        for i in range(pivotpos+1, rows):
            ratio = matrix[i][pivotpos]/matrix[pivotpos][pivotpos]
            for j in range(pivotpos, cols):
                matrix[i][j] -= ratio*matrix[pivotpos][j]
    return matrix

# def reducedEchelon(matrix):
#     rows = numRows(matrix)
#     cols = numCols(matrix)
#     replacements = 0
#     scale = 0
#     for j in range(cols):
#         for i in range(1,rows+1):
#             if matrix[i][j]!= 0 and matrix[i][j]:


def submatrix(matrix, indexi, indexj):
    rows = numRows(matrix)
    cols = numCols(matrix)
    icount = 0
    jcount = 0
    submatrix = np.zeros(shape=(rows-1, cols-1))
    for i in range(rows):
        if (i == indexi):
            icount = 1
            continue
        for j in range(cols):
            if (j == indexj):
                jcount = 1
                continue
            submatrix[i-icount][j-jcount] = matrix[i][j]
        jcount = 0
    return submatrix

def augment(matrix, ans):
    rows = numRows(matrix)
    cols = numCols(matrix)
    if len(ans) != rows:
        return "ERROR: answer does not have enough entries to be augmented with the given matrix"
    augment = np.zeros(shape=(rows, cols+1))
    for i in range(rows):
        for j in range(cols+1):
            if j == cols:
                augment[i][j] = ans[i][0]
            else:
                augment[i][j] = matrix[i][j]
    return augment

def determinant(matrix):
    det = 0
    if(not isSquare(matrix)):
        return "ERROR: must use a square matrix for the determinant() function"
    if(numRows(matrix)==2):
        return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    else:
        for j in range(numCols(matrix)):
            det += (-1)**(j)*matrix[0][j]*determinant(submatrix(matrix,0,j))
    return det    





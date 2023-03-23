import pandas as pd
from scipy import sparse
import numpy as np

#pd.read_csv()  is for csv like excel like files
#pd.read_table() is for text files and then you can directly read the data in
df = pd.DataFrame(pd.read_table('/Users/tasminahassan/ag-randmat/data/ospC-NE.diff'))
df
#converter = pd.read_csv('ospC-NE.diff')

#converter

def create_dict(df):  ####this could be so much more effient... screw it... going to go with it. 
    translator =  {}
    counter = 0
    for index, row in df.iterrows():
        if row[0] not in translator.keys():
            translator[row[0]]=counter
            counter+=1
        else:
            continue
    
    translator['U']=counter
    return translator
translator = create_dict(df)
print(len(translator))
        
def adjacency_matrix(df, translator):
       
        dicter = {}
        row = []
        col = []
        data = []

        for index, val in df.iterrows():
            row.append(translator[val[0]])  #best I have for now. I dont like doing it this way
            col.append(translator[val[1]])
            data.append(val[10])
            dicter[translator[val[0]],translator[val[1]]]=val[10]
            ## the data is actually nxn .. hence it is a square matrix nxn.. so this
            ## makes the adjacnecy matrix bidirectional
            row.append(translator[val[1]])
            col.append(translator[val[0]])
            data.append(val[10])
            dicter[translator[val[1]],translator[val[0]]]=val[10]



        shape = (len(row), len(col))
        A = sparse.coo_matrix((data, (row, col)), shape=shape)

        return A, row, col, data, dicter
    



adjac, row, col, data, dicter = adjacency_matrix(df, translator)

def create_numpy_matrix(translator, dicter):
    a_shape = (len(translator),len(translator))
    a= np.ones(a_shape)
    for i,j in dicter:
        a[i,j]=dicter[i,j]
    return a
numpy_matrix_form = create_numpy_matrix(translator, dicter)
print(numpy_matrix_form)


eigenvalues, eigenvectors = np.linalg.eig(numpy_matrix_form)
sorted_eigenvalues = sorted(eigenvalues)
eigenvalues_spacing = []
for i in range(len(eigenvalues)-1):
    eigenvalues_spacing.append(abs(eigenvalues[i]-eigenvalues[i+1]))

print("THIS IS FOR FRACTIONAL VARIABILITY FEATURE :::")
print(" The eigenvalues are : \n", eigenvalues)
print(" The eigenvectors are : \n", eigenvectors)
print("The sorted eigenvalues are: \n", sorted_eigenvalues)
print("The spacings between each eigenvalue are: \n", eigenvalues_spacing)

def create_dict(df): 
    translator =  {}
    counter = 0
    for index, row in df.iterrows():
        if row[0] not in translator.keys():
            translator[row[0]]=counter
            counter+=1
        else:
            continue
    
    translator['U']=counter
    return translator
translator = create_dict(df)

        
def adjacency_matrix(df, translator):
       
        dicter = {}

        for index, val in df.iterrows():
          
            dicter[translator[val[0]],translator[val[1]]]=val[9]
            dicter[translator[val[1]],translator[val[0]]]=val[9]

        shape = (len(row), len(col))
        
        return  dicter

dicter = adjacency_matrix(df, translator)

def create_numpy_matrix(translator, dicter):
    a_shape = (len(translator),len(translator))
    a= np.zeros(a_shape)
    for i,j in dicter:
          a[i,j]=dicter[i,j]
      
          a[i,i]=1
    
    return a
numpy_matrix_form = create_numpy_matrix(translator, dicter)
print(numpy_matrix_form)

eigenvalues, eigenvectors = np.linalg.eig(numpy_matrix_form)
sorted_eigenvalues = sorted(eigenvalues)
eigenvalues_spacing = []
for i in range(len(eigenvalues)-1):
    eigenvalues_spacing.append(abs(eigenvalues[i]-eigenvalues[i+1]))

print("THIS IS FOR FRACTIONAL GAPLESS FEATURE:::")
print(" The eigenvalues are : \n", eigenvalues)
print(" The eigenvectors are : \n", eigenvectors)
print("The sorted eigenvalues are: \n", sorted_eigenvalues)
print("The spacings between each eigenvalue are: \n", eigenvalues_spacing)

def transposeMatrix(inputMatrix, t, rows):
  
      for p in range(rows):
        
         for q in range(rows):
         
               t[p][q] = inputMatrix[q][p]

def checkingSymmetric(inputMatrix, rows):
   
      t = [[0 for q in range(len(inputMatrix[0]))]
         for p in range(len(inputMatrix))]
     
      transposeMatrix(inputMatrix, t, rows)
  
      for p in range(rows):
       
         for q in range(rows):
          
               if (inputMatrix[p][q] != t[p][q]):
               
                  return False

      return True

inputMatrix = [[6, 3, 5], [3, 2, 4], [5, 4, 6]]

if (checkingSymmetric(numpy_matrix_form, 16)):
   print("Input matrix is a Symmetric matrix")
else:
   print("Input matrix is NOT a Symmetric matrix")
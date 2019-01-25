#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

def rysujDaneGrup(X, y, marker, xlabel, ylabel,legend_list):
    '''X - macierz wartości wejściowych zorganizowana tak, że kolejne przykłady są
    w wierszach, kolumny to kolejne wynmiary  wejścia,
    y - wektor określający przynależność do grupy, indeksy tego wektora odpowiadają wireszom macierzy X,
    marker - zestaw markerów do oznaczania elementów grup, markerów powinno być tyle ile jest grup'''
    p=[]
    for i,g in enumerate(np.unique(y)):
        g = int(g)
        tmp =plt.plot(X[np.where(y==g),0],X[np.where(y==g),1],marker[i])
        p.append(tmp[0])
    plt.legend(p,legend_list)
    # Dodajemy napisy
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
def svmPredict(model,X):
    '''model - model otrzymany z funkcji svmTrain
     X - macierz m x n ,
                       w której wierszach są przykłady do sklasyfikowania (m)
                       każdy przykład ma wymiar n
     funkcja zwraca wektor pred - i-ty element to predykcja dla i-tego przykładu
    '''
    
    # pobieramy rozmiary:
    m,n = X.shape
    #print 'm,n',m,n
    # przygotowujemy tablice:
    pred = np.zeros(m) # predyktory
    margines = np.zeros(m)     # wartości marginesów
    if model['kernelFunction'] == 'linearKernel':
        margines = np.dot(X , model['w']) + model['b']
    elif model['kernelFunction'] =='gaussianKernel':
        for i in range(m): #ta pętla iteruje po przykładach z macierzy X
            for j in range(len(model['alphas'])): # ta pętlla iteruje po wektorach wspierających
                margines[i] += model['alphas'][j]*model['Y'][j]* gaussianKernel(X[i,:],model['X'][j,:],model['sigma'])
            margines[i] += model['b']
    else:
        print('niezaimplementowane jądro '+ model['kernelFunction'])
    
    pred[margines >= 0] =  1    
    pred[margines <  0] = -1
    
    return pred

def svmTrain(X, Y, C, kernelFunction, tol = 1e-3, max_passes = 5, sigma=0.1):
    '''VMTRAIN Trenuje klasyfikator  SVM za pomocą uproszczonego algorytmu SMO.
         X - macierz wejściowa  przykładów z ciągu uczącego wiersze - przyklady, kolumny - cechy
         Y - wektor etykiet klas {-1,1}
         C  - regularyzacja SVM
         tol - tolerancja na odstępstwa od wrunków KTT
         max_passes - ile iteracji bez zmian mnożników Lagrangaea wykonać zanim uznamy, że już nie ma co poprawiać
        kernelFunction - funkcja jądra, zaimplementowane są:
            - gaussianKernel
            - linearKernel
        sigma - standardowe odchylenie dla jądra gaussowskiego
    
    funkcja zwraca parametry doapsowanego modelu w słowniku model
    '''

    # Pobieramy rozmiary
    m,n = X.shape #m - ilość przykładów, n - wymiar wejścia
  

    # Zmienne
    alphas = np.zeros(m)
    b = 0
    E = np.zeros(m)
    passes = 0
    eta = 0
    L = 0
    H = 0

    # Pre-compute the Kernel Matrix since our dataset is small
    # (in practice, optimized SVM packages that handle large datasets
    #  gracefully will _not_ do this)
    # 
    # We have implemented optimized vectorized version of the Kernels here so
    # that the svm training will run faster.
    print('Obliczam macierz jądra')
    if kernelFunction =='linearKernel':
        # to jądro można policzyć od razu dla wszystkich przykładów
        K = np.dot(X,X.T)
    else:
        # Jak nie możemy wymyśleć wektoryzacji obliczeń to
        # obliczamy każdy element macierzy jądra osobno
        K = np.zeros((m,m))
        for i in range(m):
            for j in range(i,m):
                K[i,j] = gaussianKernel(X[i,:].T, X[j,:].T,sigma)
                K[j,i] = K[i,j] #the matrix is symmetric
       
       
    print('Trenuję ...')
    dots = 12
    while passes < max_passes:        
        num_changed_alphas = 0
        for i in range(m): #dla każdego przykładu z ciągu uczącego
            # obliczamy błąd predykcji dla wektora i
            E[i] = b + np.sum (alphas*Y*K[:,i]) - Y[i]
            # jeśli jest co poprawiać:
            if (( (Y[i]*E[i] < -tol) & (alphas[i] < C)) | ((Y[i]*E[i] > tol) & (alphas[i] > 0))):
            
                # In practice, there are many heuristics one can use to select
                # the i and j. In this simplified code, we select them randomly.
                j = int(np.floor(m * np.random.rand()))
                while j == i:  # Make sure i \neq j
                    j = int(np.floor(m * np.random.rand()))
            
                # Obliczamy błąd predykcji dla wektora j.
                E[j] = b + np.sum (alphas*Y*K[:,j]) - Y[j]

                # Save old alphas
                alpha_i_old = alphas[i]
                alpha_j_old = alphas[j]
            
                # Oblicz przycięcia do pudełka [0,C] 
                if (Y[i] == Y[j]):
                    L = np.max((0, alphas[j] + alphas[i] - C))
                    H = np.min((C, alphas[j] + alphas[i]))
                else:
                    L = np.max((0, alphas[j] - alphas[i]))
                    H = np.min((C, C + alphas[j] - alphas[i]))
                if (L ==    H):
                    # continue to next i. 
                    continue
                # Compute eta by (15).
                eta = 2 * K[i,j] - K[i,i] - K[j,j]
                if (eta >= 0):
                    # continue to next i. 
                    continue
                # Compute and clip new value for alpha j using (16) and (17).
                alphas[j] = alphas[j] - (Y[j] * (E[i] - E[j])) / eta
            
                # Clip 
                alphas[j] = np.min ((H, alphas[j]))
                alphas[j] = np.max ((L, alphas[j]))
            
                #Check if change in alpha is significant
                if (np.abs(alphas[j] - alpha_j_old) < tol):
                    # continue to next i. 
                    # replace anyway
                    alphas[j] = alpha_j_old
                    continue
            
                # Determine value for alpha i using (16). 
                alphas[i] = alphas[i] + Y[i]*Y[j]*(alpha_j_old - alphas[j])
            
                # Compute b1 and b2 using (20) and (21) respectively. 
                b1 = b - E[i] - Y[i] * (alphas[i] - alpha_i_old) *  K[i,j] - Y[j] * (alphas[j] - alpha_j_old) *  K[i,j].T
                b2 = b - E[j] - Y[i] * (alphas[i] - alpha_i_old) *  K[i,j] - Y[j] * (alphas[j] - alpha_j_old) *  K[j,j].T

                # Compute b by (19). 
                if ( (0 < alphas[i]) & (alphas[i] < C)):
                    b = b1
                elif (0 < alphas[j]) & (alphas[j] < C):
                    b = b2
                else:
                    b = (b1+b2)/2
                num_changed_alphas = num_changed_alphas + 1    
        if (num_changed_alphas == 0):
            passes = passes + 1
        else:
            passes = 0
        #print(num_changed_alphas)
    print(' Gotowe! \n\n')

    # Save the model
    idx = alphas > 0    
    model = {}
    model['X'] = X[idx,:]
    model['Y'] = Y[idx]
    model['kernelFunction'] = kernelFunction
    model['b'] = b
    model['alphas']= alphas[idx]
    model['w'] = (np.dot((alphas*Y).T, X)).T
    model['sigma'] = sigma
    print('ilość wektorów wspierających: ', len(model['alphas']))
    return model

def rysujPodzial(model, X):
    # wytworzymy siatkę punktów pokrywających obszar danych:
    N = 100 # ilość punktów siatki w jednym wymiarze
    os_x = np.linspace(X.min(),X.max(),N)
    klasa = np.zeros((N,N))
    for ix1, x1 in enumerate(os_x):
        for ix2, x2 in enumerate(os_x):
            XX = np.array([x1,x2]).reshape(1,2)
            klasa[ix1,ix2] = svmPredict(model, XX) # dla każdego punktu siatki obliczamy jego klasę
    
    x1_grid,x2_grid = np.meshgrid(os_x,os_x)
    plt.contourf(x1_grid, x2_grid, klasa.T,2)   


if len(sys.argv) !=2:
	print("./draw.py input_file")
else:
	with open(sys.argv[1]) as f:
		content = f.readlines()
	process = []
	m1 = []
	m2 = []
	result = []
	for line in content:
		if line[0] == '#':
			pass
		else:
			splitted = line.split('\t')
			process.append(splitted[0])
			m1.append(float(splitted[1]))
			m2.append(float(splitted[2]))
			result.append(int(splitted[3][0]))

	X = []
	for ii in range(0, len(m1)):
		X.append([m1[ii], m2[ii]])
	X = np.array(X)
	y = np.array(result)

	model  = svmTrain(X, y, C=100, kernelFunction = 'linearKernel', tol = 1e-3, max_passes = 20,sigma = 10) 
	rysujDaneGrup(X, y, marker=('or','xb'), xlabel='m1', ylabel='m2',legend_list=('klasa0','klasa1'))
	rysujPodzial(model,X)

	plt.show()
	
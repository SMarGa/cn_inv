#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Robótica Computacional - 
# Grado en Ingeniería Informática (Cuarto)
# Práctica: Resolución de la cinemática inversa mediante CCD
#           (Cyclic Coordinate Descent).


import sys
from math import *
import numpy as np
import matplotlib.pyplot as plt
import colorsys as cs

from read_data import get_info

# ******************************************************************************
# Declaración de funciones

def muestra_origenes(O,final=0):
  # Muestra los orígenes de coordenadas para cada articulación
  print('Origenes de coordenadas:')
  for i in range(len(O)):
    print('(O'+str(i)+')0\t= '+str([round(j,3) for j in O[i]]))
  if final:
    print('E.Final = '+str([round(j,3) for j in final]))

def muestra_robot(O,obj,aType):
  # Muestra el robot graficamente
  plt.figure()
  plt.xlim(-L,L)
  plt.ylim(-L,L)
  T = [np.array(o).T.tolist() for o in O]
  for i in range(len(T)):
    
    plt.plot(T[i][0], T[i][1], '-o', color=cs.hsv_to_rgb(i/float(len(T)),1,1))
    

  plt.plot(obj[0], obj[1], '*')
  plt.pause(0.0001)
  plt.show()
  
#  input()
  plt.close()

def matriz_T(d,th,a,al):
  # Calcula la matriz T (ángulos de entrada en grados)
  
  return [[cos(th), -sin(th)*cos(al),  sin(th)*sin(al), a*cos(th)]
         ,[sin(th),  cos(th)*cos(al), -sin(al)*cos(th), a*sin(th)]
         ,[      0,          sin(al),          cos(al),         d]
         ,[      0,                0,                0,         1]
         ]

def cin_dir(th,a):
  #Sea 'th' el vector de thetas
  #Sea 'a'  el vector de longitudes
  T = np.identity(4)
  o = [[0,0]]
  for i in range(len(th)):
    T = np.dot(T,matriz_T(0,th[i],a[i],0))
    tmp=np.dot(T,[0,0,0,1])
    o.append([tmp[0],tmp[1]])
  return o


def sum_th(th,no_a):
  w = 0
  for i in range(no_a):
    w += th[i]
  return w

# ******************************************************************************

# ******************************************************************************
# Cálculo de la cinemática inversa de forma iterativa por el método CCD

# valores articulares arbitrarios para la cinemática directa inicial

#plt.ion() # modo interactivo

# introducción del punto para la cinemática inversa
if len(sys.argv) != 2:
  sys.exit("python " + sys.argv[0] + " falta nombre de archivo")

filename= sys.argv[1]

data = get_info(filename)
th = data["th"]
a = data["a"]
objetivo = data["objetivo"]
a_type = data["tipo"]
limites = data["limite"]

L = max(objetivo[0],objetivo[1],sum(a)) + 5 # variable para representación gráfica
EPSILON = .01

O=cin_dir(th,a)
#O=zeros(len(th)+1) # Reservamos estructura en memoria
 # Calculamos la posicion inicial
print ("- Posicion inicial:")
muestra_origenes(O)

dist = float("inf")
prev = 0.
iteracion = 1
while (dist > EPSILON and abs(prev-dist) > EPSILON/100.):
  prev = dist
  O=[cin_dir(th,a)]
  # Para cada combinación de articulaciones:

  for i in range(len(th)):
  

    if(a_type[-i-1] == "R"):
      # cálculo de la cinemática inversa:
      v1_x = objetivo[0] - O[i][-i -2][0]
      v1_y = objetivo[1] - O[i][-i -2][1]

      v2_x = O[i][-1][0] - O[i][-i -2][0]
      v2_y = O[i][-1][1] - O[i][-i -2][1]

      alpha1 = atan2(v1_y,v1_x)
      alpha2 = atan2(v2_y,v2_x)
      alpha = alpha1 - alpha2
      th[-i-1] += alpha
      if(th[-i-1] < limites[-i-1][0]):
        th[-i-1] = limites[-i-1][0]
      if(th[-i-1] > limites[-i-1][1]):
        th[-i-1] = limites[-i-1][1]

      th[-i-1] = (th[-i-1] + pi) % (2*pi) - pi
      


    if(a_type[-i-1] == "P"):

      w = sum_th(th,len(th)-i -1)

      v1_x = objetivo[0] - O[i][len(th)][0]
      v1_y = objetivo[1] - O[i][len(th)][1]

      v2_x = cos(w)
      v2_y = sin(w)
      
      d = v1_x * v2_x + v1_y * v2_y
      a[-i-1] += d

      if(a[-i-1] > limites[-i-1]):
        a[-i-1] = limites[-i-1]

  
    
    O.append(cin_dir(th,a))
 
 
  dist = np.linalg.norm(np.subtract(objetivo,O[-1][-1]))
  print ("\n- Iteracion " + str(iteracion) + ':')
  muestra_origenes(O[-1])
  muestra_robot(O,objetivo,a_type)
  for i in range(len(th)):
    print ("  theta" + str(i+1) + " = " + str(round(th[i],3)))
  for i in range(len(th)):
   print ("  L" + str(i+1) + "     = " + str(round(a[i],3)))
  print ("Distancia al objetivo = " + str(round(dist,5)))
  iteracion+=1
  O[0]=O[-1]

if dist <= EPSILON:
  print ("\n" + str(iteracion) + " iteraciones para converger.")
else:
  print ("\nNo hay convergencia tras " + str(iteracion) + " iteraciones.")
print ("- Umbral de convergencia epsilon: " + str(EPSILON))
print ("- Distancia al objetivo:          " + str(round(dist,5)))
print ("- Valores finales de las articulaciones:")
for i in range(len(th)):
  print ("  theta" + str(i+1) + " = " + str(round(th[i],3)))
for i in range(len(th)):
  print ("  L" + str(i+1) + "     = " + str(round(a[i],3)))


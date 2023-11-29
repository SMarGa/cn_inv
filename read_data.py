import sys
import math


def get_info(filename):
  file = open(filename, "r")
  lines = file.readlines()
  count = 0
  objetivo=[]
  th = []
  a = []
  tipo = []
  limite =[]
  for line in lines:
    info = line.split()
    while("" in info):
        info.remove("")
    
    if(count == 0):
      if(len(info) != 2):
        raise Exception("Solo se permiten dos números para la pocisión inicial")
      objetivo = [float(info[0]),float(info[1])]
    else:
      if(len(info) < 4 ):
        raise Exception("Se necesitan como mínimo 4 parámetros para definir una articulación")
      th_inicial = math.radians(float(info[0]))
      th.append(th_inicial)
      a.append(float(info[1]))

      if(info[2] != "R" and info[2]!= "P"):
        raise Exception("Tipo de articulación no permitido (solo P o R) en linea", count)
      tipo.append(info[2])
      if(info[2] == "R"):
        if(len(info) != 5 ):
          raise Exception("Se necesitan 5 parámetros para definir una articulación de revolución")
      
        limite_inferiror= math.radians(float(info[3]))
        limite_superior= math.radians(float(info[4]))
        if(th_inicial< limite_inferiror or th_inicial > limite_superior):
          raise Exception("Angulo inicial fuera de rango en linea", count)
        
        limite.append([limite_inferiror,limite_superior])
      else:
        if(float(info[3]) < float(info[1])):
          raise Exception("Longitud inicial fuera de rango en linea", count)
        limite.append(float(info[3]))
    count +=1

  result = dict()
  result["th"] = th
  result["a"] = a
  result["tipo"] = tipo
  result["limite"] = limite
  result["objetivo"] = objetivo
  return result

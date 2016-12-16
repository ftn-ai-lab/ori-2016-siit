# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 22:18:35 2016

@author: Nemanja Zunic sw63-2014
Ucestalost koriscenja marihuane i posecivanja zurki kod mladih.
"""

import matplotlib.pyplot as plt

def linear_regression(x, y):
    b = 0.0  # nagib linije  -  b
    a = 0.0  # tacka preseka na y-osi  -  a
    
    meanX = 0.0
    meanY = 0.0
    numb = len(x)
    i = 0
    
    for i in range(numb):
        meanX += x[i]
        meanY += y[i]
        
    meanX /= numb
    meanY /= numb
    
    br1 = 0.0
    br2 = 0.0
    
    for i in range(numb):
        br1 += (x[i] - meanX) * (y[i] - meanY)
        br2 += (x[i] - meanX) * (x[i] - meanX)
        
    br1 /= numb
    br2 /= numb
    
    b = br1 / br2
    
    for i in range(numb):
        a += y[i] - b * x[i]
    a /= numb
    
    return b, a
  
  
def create_line(x, slope, intercept):
    y = [predict(xx, slope, intercept) for xx in x]
    return y
    
    
def predict(x, b, a):
    return a + b*x


if __name__ == '__main__':
    
    #otvaramo fajl u modu za citanje
    file = open("marij.csv", 'r')
    #ucitavamo sadrzaj tako da red fajla predstavlja jedan element liste
    content = file.readlines()
    file.close()

    #tri prazne liste 
    ucest_mari, ucest_zur, br_opredeljenih = [], [], []
    
    #za svaki red fajla
    for i in range(len(content)):
        #splitujemo red po separatoru ','
        red_sadrzaja = content[i].split(",")
        """od 0 do broja koji se nalazi u koloni 3 iz i-tog reda fajla
           treca kolona predstavlja broj studenata koji su odabrali jednu od
           kombinacija ucestalost koriscenja marihuane  :  ucestalost posecivanja zurki"""
        for j in range(int(red_sadrzaja[2])):
            #u jednu listu smestamo odgovore za koriscenje marihuane
            ucest_mari.append(int(red_sadrzaja[0]))
            #u drugu smestamo odgovore za posecivanje zurki
            ucest_zur.append(int(red_sadrzaja[1]))
         
         
    slope, intercept = linear_regression(ucest_mari, ucest_zur)
    line = create_line(ucest_mari, slope, intercept)
    
    plt.plot(ucest_mari, ucest_zur, '.')
    plt.plot(ucest_mari, line, 'b')
    plt.title('Slope: {0}, intercept: {1}'.format(slope, intercept))
    plt.show()
# -*- coding: utf-8 -*-
import numpy as np
import random
#数据结构：tau matrix 
#########################一些参数###################################
Q=1  #信息素增加强度系数
rho=0.75 #挥发率   或者0.9
ant_size=20#ant 数量
distanceMatrixFileName="d:\\0622-new\\distance.csv"
distanceMatrix=np.genfromtxt(distanceMatrixFileName,delimiter=',')#读取距离矩阵
alpha=5
beta=1
#这两个是计算plist用的

#############################每次选点#########################

class Ant(object):#checked
    def __init__(self,number):
        self.no=number #0-ant_size
        self.tabulist=[]#传入一个空list
        self.length=0.0 # 每次选择点之后进行累加，在得到最佳点之后清零
def initiateAnts(numbers):#checked
    return [Ant(i) for i in range(numbers)]
    
def randomChoiceFromList(Plist):#checked
    rnd=random.random()
    choice=len(Plist)-1
    accumulatePlist=[sum(Plist[0:i+1]) for i in range(len(Plist))]
    for i in range(len(accumulatePlist)):
        if rnd<accumulatePlist[i]:
            choice=i
            break
    return choice

def calculateArc(ant,origin,tauMatrix):#####checked   
    Plist=[0.0 for i in range(len(distanceMatrix))]  #先搞一个list 所有元素都是0.0， 长度是distanceMatrix
    for i in range(len(distanceMatrix)):
        if i in ant.tabulist:#如果在tabulist里就0.0
            Plist[i]=0.0
        else:
            start=ant.tabulist[origin]#如果不在，那么就从上一个点为origin
            end=i#（可能）重点为i
            Plist[i]=tauMatrix[start,end]**alpha*(1/distanceMatrix[start,end])**beta#用公式计算
    Plist=Plist/sum(Plist)
    choice=randomChoiceFromList(Plist)
    arc=[origin,choice]    
    ant.tabulist.append(choice)
    ant.length+=distanceMatrix[origin,choice]
    return arc

def updateTau(ant,distanceMatrix,tauMatrix,rho):
       
    ####################tauMatrix
    for i in range(len(ant)):
        deltaTau=np.zeros(len(distanceMatrix)*len(distanceMatrix))  #每次iteration的 信息素增量，每次iteration之后与原tau矩阵结合，然后清零
        for j in range(len(ant[i].tabulist)-1):#此段存疑
            deltaTau[ant[i].tabulist[j],ant[i].tabulist[j+1]]+=Q/ant[i].length 
        tauMatrix=tauMatrix*(1-rho)+rho*deltaTau
    #做某些规范化操作          

def iterate(ant,distanceMatrix,tauMatrix,rho):
    #
    #all ants go to 00 point
    for i in range(len(distanceMatrix)):###i代表每一个ant要走的路程 （298个点）
        for j in range(len(ant)):
            calculateArc(ant[j],i)#i是出发点，
    
    for j in range(len(ant)):
         updateTau(ant[j],distanceMatrix,tauMatrix,rho)

def main():
    
    #################################data##############################
    
    tauMatrix=np.ones([len(distanceMatrix),len(distanceMatrix)])#初始化tau矩阵(全部值都是1）
    ant=initiateAnts(ant_size)                          #初始化ant列表
    
    #############################每次迭代都会清零#######################
    
    #tabuList=[[np.nan for i in range(len(distanceMatrix))] for j in range(ant_size)]#在每次选择点之后对此次选择的点进行记录，在一个迭代周期结束后进行清零
    #lengthList=[np.nan for i in range(ant_size)]
    
    #下面开始初始化ants
    #补充圆心点0 所有的点都从这个点出发
    while xxx and xxx:
        iterate(ant,distanceMatrix)
    
       
            
            
main()




                       
####################################################################################            
            
  
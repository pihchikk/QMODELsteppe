import math as m
import matplotlib.pyplot as plt
import random

########################################################Описание########################################################

#Модель описывает изменение содержания Сорг, изменение качества Сорг в степных почвах, оставленных под паром.
#параметры подобраны для опытного участка ФГБНУ Курского НИИ АПП
#параметризация и калибровка модели в оригинальном исследовании проводилась в соответствии с данными, полученными при долгосрочных экспериментах на этом участке;
#Формулы и значения параметров приводятся в соответствии с Menicheti et. al, 2019, если не указано иное.

########################################################Входные параметры модели########################################################

l=20 #Титлянова и др., 2018
e0=0.303 #Menicheti et. al, 2019
q0=0.98 #Menicheti et. al, 2019
h11=0.31 #Menicheti et. al, 2019
u0=0.49 #калибруемый параметр 
Re=1 #калибруемый параметр (rtemp*rmoist)
b0=6.75 #Menicheti et. al, 2019 (локальный параметр)
x=27 #содержание ила, %, реестр почвенных ресурсов, 2014
Css=100 #Щепаченко и др., 2017
qtM=[]
tM=[] #массивы для визуализации
CtM=[]
CptM=[]

########################################################Промежуточные элементы########################################################

b=b0+0.01*x #параметр b показывает то, насколько быстро изменяется скорость прироста биомассы при изм. качества
qss=q0*(1-e0-h11*e0*b)/(1-e0-h11*e0*(b-1)) #среднее качество ПОВ в равновесном состоянии
Cpss=l*(e0/(u0*q0**b)) #содержание фракции растительного материала в почве (plant-derived material) в р.с.

########################################################Циклы разложения########################################################

t=0
while t <=200:
    Re=random.uniform(0.7, 0.98)
    qt=q0/(1+b*h11*u0*Re*t*q0**b)**(1/b) #снижение качества со временем
    Cpt=Cpss*m.exp(-t*(e0/(u0*q0**b))) #изменение содержания фракции растительного материала
    Ct=Css*(qt/q0)**(abs((1-e0)/(h11*e0))-b) #изменение общего содержания Сорг со временем в условиях пара
    CtM.append(Ct)
    CptM.append(Cpt)
    qtM.append(qt)
    tM.append(t)
    t+=1
    
########################################################Визуализация########################################################

def plotFIN(Years,Store,title,Xlab,Ylab):
    fig, ax = plt.subplots()
    ax.stackplot(Years, Store)
    fig.set_figwidth(12)   
    fig.set_figheight(6)   
    fig.set_facecolor('floralwhite')
    ax.set_facecolor('seashell')
    ax.set_ylabel(Ylab,fontsize=15)
    ax.set_xlabel(Xlab,fontsize=15)
    ax.set_title(title,fontsize=18)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.show()
    fig.savefig('C:/Users/Admin/Desktop/модель/plots/'+str(title))
plotFIN(tM,qtM,'Качество','Годы','Качество остающегося органического вещества')
plotFIN(tM,CtM,'Запасы Сорг','Годы','Сорг, т/га')

fig, ax = plt.subplots() 
ax.stackplot(tM, CptM)
fig.set_figwidth(12)   
fig.set_figheight(6)   
fig.set_facecolor('floralwhite')
ax.set_facecolor('seashell')
ax.set_xlabel('Years',fontsize=15)
ax.set_title('remaining plant fraction',fontsize=18)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.xlim([0, 10])
plt.show()
fig.savefig('C:/Users/Admin/Desktop/модель/plots/'+'Remaining plant fraction')

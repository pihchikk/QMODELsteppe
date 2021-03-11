import math
import matplotlib.pyplot as plt
#Модель описывает разложение и накопление органического вещества в лесных экосистемах 
#В качестве входных параметров используются: 
l=float(input()) #количество подстилки продуцируемой в единицу времени (т/га*год)
q0=float(input()) #исходное качество органического вещества, см. блок-схему
#референтные значения: q0=0,99 для древесных остатков, q0=1 для листьев
r0=float(input()) #исходное соотношение C/N в подстилке, см. блок-схему   
T=float(input()) #среднегодовая температура, °C
e0=float(0.25) #отношение продуцируемого микробиомом C биомассы к ассимилируемому C (Cп/Cа)
h11=float(0.36) #среднее смещение качества С, см. блок-схему
b=7 #параметр, определяемый содержанием ила, см. блок-схему
fC=float(input()) #концентрация углерода в биомассе микробов (C/m), (Cг/Bg)
fN=float(input()) #концентрация азота в микробной биомассе (N/m), (Nг/Bg)
u0=float(0.075)+float(0.014)*T #исходный темп прироста микробной биомассы (B/C*t – кг/кг*год)
#Все вычисления выполняются в два этапа. 
#Во-первых, рассчитывается среднее снижение качества на каждой итерации микробной трансформации
#Затем рассчитывается количество углерода и азота исходя из снижения качества. 
alpha=b*h11*fC*u0*q0**b #мера снижения качества в единицу времени (?) см. блок-схему
zeta=(1-e0)/(e0*h11)#степень в уравнении (5), см. блок-схему
k0=fC*(1-e0)*u0*q0**q0/e0 #удельная скорость разложения биомассы
def CSS(l,fC,u0,q0,b,e0,h11): #содержание углерода в равновесном состоянии
    return l/(fC*u0*q0**b)*e0/(1-e0-e0*h11*b)
CSS1=float(l/(fC*u0*q0**b)*e0/(1-e0-e0*h11*b))
NSS1=float(CSS1*fN/fC) #содержание азота в равновесном состоянии
NSS2=float((fN/fC-r0)*(1-e0-e0*h11*b)/(1-e0*h11*b)*CSS1) #содержание азота в равновесном состоянии (?)
def NSS(NSS1, NSS2): 
    return (NSS1-NSS2) #содержание азота в равновесном состоянии 
print('C steady state =',CSS(l,fC,u0,q0,b,e0,h11),'N steady state =',NSS(NSS1, NSS2))
step=0 #"шаг разложения" - количество циклов ассимиляции-продукции-отмирания биомассы, 
#в результате кажого из которых происходит смещение кач-ва
qq=1 #(отношение текущего уровня качества к исходному(для отдельной фракции подстилки), q/q0)
tk=1 #время, за которое осуществляется один цикл ассимиляции-продукции-отмирания (для отд. фракции), лет
g=1 #отношение содержания С в субстрате к исходному Ci/C0 
h=1 #отношение содержания N к исходному содержанию C (Ni/C0)
CM=[]
NM=[]
tkM=[]
tsM=[]
gM=[]
hM=[]
qM=[]
while step <=25: #число шагов разложения прозвольно принимается равным 25 (см. Bosatta, Agren)
    tk=step*5/alpha/25 #см. блок-схему
    qq=(1+alpha*tk)**(-1/b) #см. блок-схему
    g=qq**zeta #см. блок-схему
    h=(r0-fN/fC)*qq**(1/(e0*h11))+fN/fC*g #h - отношение содержания N к исходному содержанию C (Ni/C0)
    exp=math.exp(-k0*tk) #
    ts=step*50/alpha/25
    qqs=(1+alpha*ts)**(-1/b)
    C=CSS(l, fC, u0, q0, b, e0, h11)*(1-qqs**(zeta-b)) #совокупное содержание углерода в почве
    N=fN/fC*C-(fN/fC-r0)*e0/(1-e0*h11*b)*(1-qqs**(1/(e0*h11)-b))/(fC*u0*q0**b) #совокупное содержание азота в почве
    step+=1
    CM.append(C)
    tkM.append(tk)
    tsM.append(ts)
    NM.append(N)
    gM.append(g)
    hM.append(h)
    qM.append(qqs)
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
plotFIN(tsM,CM,'Запасы углерода в почве','Годы','Запасы углерода, кгС/га')
plotFIN(tsM,NM,'Запасы азота в почве','Годы','Запасы азота, кгС/га')
plotFIN(tkM,gM,'Фракция подстилки','годы','C/C0, доля от изначального содержания Сорг')
plotFIN(tkM,hM,'Фракция подстилки','годы','N/С0, доля от изначального содержания Сорг')
plotFIN(tsM,qM,'Снижение качества отдельной фракции со временем','годы','качество')



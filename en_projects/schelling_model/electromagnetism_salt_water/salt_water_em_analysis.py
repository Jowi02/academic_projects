from numpy import *
from pylab import *

clf()

#permeabilidad
mu = pi*4*10**(-7)

#permitividad
eps0 = 8.854*10**(-12)
epsr = 81
eps = epsr*eps0

c=299792458 

#conductividad
sigma = 4

#Ecuaciones generales
def w(f):
    w=2*pi*f
    return w

def alfa_gen(w):
    alfa_g = w*(0.5*mu*eps*(((1+(sigma/(w*eps))**2)**(1/2)) -1))**(1/2)
    return alfa_g

def delta_g(alfa_g):
    delta_g = 1/alfa_g
    return delta_g
def beta_gen(w):
    beta_g = w*(0.5*mu*eps*(sqrt(1+(sigma/(w*eps)))+1))**(1/2)
    return beta_g
    
def vel_gen(w, beta_g):
    v = w/beta_g
    return v
    
def lambda_gen(beta_g):
    lambda_g = 2*pi/beta_g
    return lambda_g

def modulo_eta_gen(w, alfa_g, beta_g):
    m_eta_g = ((w*mu)/sqrt(alfa_g**2 + beta_g**2))
    return m_eta_g

def fase_eta_gen(alfa_g, beta_g):
    f_eta_g = pi/2 - arctan(beta_g/alfa_g) # no está como multiplo de pi!!!!!
    return f_eta_g
    
#frecuencias de cuasi conductor, limites
#tangente de pérdidas <1/100:
f_diel = sigma*100/(2*pi*eps)
print("Para buen dielectrico la frecuencia es: %f (GHz)"  %(f_diel/10**9))
f_cond = sigma/(2*pi*eps*100)

print("\n" + "Para buen conductor la frecuencia es: %f (MHz)"  %(f_cond/10**6))

#Buen dielectrico
alfa_bd1 = (sigma/2)*sqrt(mu/eps)

def alfa_bd(f):
    alfa_bd = alfa_bd1 + 0*f
    return alfa_bd

def beta_bd(w):
    beta_bc = w*sqrt(mu*eps)
    return beta_bc

def fase_eta_bd(w):
    f_eta_bc = sigma/(2*w*eps)
    return f_eta_bc

#Buen conductor alfa = beta!!!!!
def alfa_bc(w):
    alfa_bc = sqrt((w*mu*sigma)/2)
    return alfa_bc

def modulo_eta_bc(w):
    m_eta_bc = sqrt(2)*alfa_bc(w)/sigma
    return m_eta_bc
    
fase_eta_bc = pi/4

f= linspace(60*10**3, 10**12, 10**4)

#Comaparamos alfa en cada caso con el general
plot(log10(f),log10(alfa_gen(w(f))), "r-", label = r"$\alpha_{general}$")
plot(log10(f),log10(alfa_bc(w(f))), "g-", label = r"$\alpha_{good \ conductor}$")
plot(log10(f), log10(alfa_bd(f)), "b-", label = r"$\alpha_{good \  dielectric}$")

#Comparamos alfa en cada caso con el general
plot(log10(f), (alfa_gen(w(f))/alfa_bc(w(f))), "m-.", label = r"$(\frac{\alpha_{general}}{\alpha_{good \  conductor}})$")
plot(log10(f), (alfa_gen(w(f))/alfa_bd(w(f))), "c-.", label = r"$(\frac{\alpha_{general}}{\alpha_{good \  dielectric}})$")

#Embellecemos la gráfica
xlabel(r"$log_{10}(f)$", fontsize = 20)
ylabel((r"$log_{10}(\alpha$)"), fontsize = 20)
legend(loc = 2, fontsize = 16)
grid()

xlim(left = log10(40*10**3))
axvspan(log(1), log10(f_cond), alpha = 0.3, color = "palegreen")
axvspan(log10(f_diel), log10(f_diel*10**3), alpha = 0.3, color = "paleturquoise")

#print((alfa_gen(w(f_cond*10**(2)))/alfa_bd(w(f_cond*10**(2)))))

f_pruebas_alfa_bd = array([f_diel*10**(-3), f_diel*10**3])

def frecs_pruebaspos(f, interv):
    frecs = f*10**(interv)
    return frecs

def frecs_pruebasneg(f, interv):
    frecs = f/10**(abs(interv))
    return frecs

rangopos = array([ 0, 1, 2, 3])
rangoneg = array([-1, -2, -3,])

print("\n")
print("Para el dielectrico la alfa varia")
print("")
print(frecs_pruebaspos(f_diel, rangopos))
print("Por encima: \n")

#COMPARACION DE LA ALFA CON LA FRECUENCIA
f_comparacion_dielpos = alfa_gen(w(frecs_pruebaspos(f_diel, rangopos)))/alfa_bd(w(frecs_pruebaspos(f_diel, rangopos)))
print(f_comparacion_dielpos)
    
f_comparacion_dielneg = alfa_gen(w(frecs_pruebasneg(f_diel, rangoneg)))/alfa_bd(w(frecs_pruebasneg(f_diel, rangoneg)))
print("")
print("Por debajo: \n")
print(frecs_pruebasneg(f_diel, rangoneg))
print(f_comparacion_dielneg)

# PARA EL CONDUCTOR
f_comparacion_condpos = alfa_gen(w(frecs_pruebaspos(f_cond, rangopos)))/alfa_bc(w(frecs_pruebaspos(f_cond, rangopos)))
print("")
print("Para el conductor la alfa varia")
print("")
print(frecs_pruebaspos(f_cond, rangopos))
print("Por encima: \n")
print(f_comparacion_condpos)    

f_comparacion_condneg = alfa_gen(w(frecs_pruebasneg(f_cond, rangoneg)))/alfa_bc(w(frecs_pruebasneg(f_cond, rangoneg)))
print("")
print("Por debajo: \n")
print(frecs_pruebasneg(f_cond, rangoneg))
print(f_comparacion_condneg)
print("---------------------------------------------------")

#PONGO UN CLF PARA NO TENER LA FIGURA DE LAS ALFAS
clf()

plot(log10(f),log10(beta_gen(w(f))), "r-", label = r"$\beta_{general}$")
plot(log10(f),log10(alfa_bc(w(f))), "g-", label = r"$\beta_{good \ conductor}$")
plot(log10(f), log10(beta_bd(f)), "b-", label = r"$\beta_{good \  dieléctrico}$")

#Comparamos beta en cada caso con el general
plot(log10(f), abs((beta_gen(w(f))/alfa_bc(w(f)))), "m-.", label = r"$(\frac{\beta_{general}}{\beta_{good \  conductor}})$")
plot(log10(f), abs((beta_gen(w(f))/beta_bd(w(f)))), "c-.", label = r"$(\frac{\beta_{general}}{\beta_{good \  dielectric}})$")

#Embellecemos la gráfica
xlabel(r"$log_{10}(f)$", fontsize = 20)
ylabel((r"$log_{10}(\beta$)"), fontsize = 20)
legend(loc = 2, fontsize = 16)
grid()

xlim(left = log10(40*10**3))
axvspan(log(1), log10(f_cond), alpha = 0.3, color = "palegreen")
axvspan(log10(f_diel), log10(f_diel*10**3), alpha = 0.3, color = "paleturquoise")

print("\n")

print("Para el dielectrico la beta varia")
print("")
print(frecs_pruebaspos(f_diel, rangopos))
print("Por encima: \n")

#COMPARACION DE LA ALFA CON LA FRECUENCIA

f_comparacion_betadielpos = beta_gen(w(frecs_pruebaspos(f_diel, rangopos)))/beta_bd(w(frecs_pruebaspos(f_diel, rangopos)))
print(f_comparacion_betadielpos)

# PARA EL CONDUCTOR
f_comparacion_betacondpos = beta_gen(w(frecs_pruebaspos(f_cond, rangopos)))/alfa_bc(w(frecs_pruebaspos(f_cond, rangopos)))

print("")
print("Para el conductor la alfa varia")
print("")
print(frecs_pruebaspos(f_cond, rangopos))
print("Por encima: \n")
print(f_comparacion_betacondpos)    

f_comparacion_betadielneg = beta_gen(w(frecs_pruebasneg(f_diel, rangoneg)))/alfa_bd(w(frecs_pruebasneg(f_diel, rangoneg)))

print("")
print("Por debajo: \n")
print(frecs_pruebasneg(f_diel, rangoneg))
print(f_comparacion_dielneg)

f_comparacion_betacondneg = beta_gen(w(frecs_pruebasneg(f_cond, rangoneg)))/alfa_bc(w(frecs_pruebasneg(f_cond, rangoneg)))

print("")
print("Por debajo: \n")
print(frecs_pruebasneg(f_cond, rangoneg))
print(f_comparacion_betacondneg)

"""
clf()

plot(log10(f),log10(beta_gen(w(f))), "r-", label = r"$\beta_{general}$")
plot(log10(f),log10(alfa_bc(w(f))), "g-", label = r"$\beta_{good \ conductor}$")
plot(log10(f), log10(beta_bd(f)), "b-", label = r"$\beta_{good \  dielectric}$")

#Comparamos beta en cada caso con el general
plot(log10(f), abs((beta_gen(w(f))/alfa_bc(w(f)))), "m-.", label = r"$(\frac{\beta_{general}}{\beta_{good \  conductor}})$")
plot(log10(f), abs((beta_gen(w(f))/beta_bd(w(f)))), "c-.", label = r"$(\frac{\beta_{general}}{\beta_{good \  dielectric}})$")

#Embellecemos la gráfica
xlabel(r"$log_{10}(f)$", fontsize = 20)
ylabel((r"$log_{10}(\beta$)"), fontsize = 20)
legend(loc = 2, fontsize = 16)
grid()

xlim(left = log10(40*10**3))
axvspan(log(1), log10(f_cond), alpha = 0.3, color = "palegreen")
axvspan(log10(f_diel), log10(f_diel*10**3), alpha = 0.3, color = "paleturquoise")
"""

#IMPEDANCIA
"""
clf()

plot(log(f), vel_gen(w(f), beta_gen(w(f))), "r-.", label= r"$v_{general}")
"""
"""
#Velocidad

clf()

plot(log10(f),log10(vel_gen(w(f), beta_gen(w(f)))), "r-", label = r"$v_{\beta, general}$")
plot(log10(f),log10(vel_gen(w(f), beta_bd(w(f)))), "b-", label = r"$v_{\beta, \ good \ diel}$")
plot(log10(f),log10(vel_gen(w(f), alfa_bc(w(f)))), "g-", label = r"$v_{\beta, \ good \ cond}$")

#Comparamos beta en cada caso con el general
#plot(log10(f), abs((beta_gen(w(f))/alfa_bc(w(f)))), "m-.", label = r"$(\frac{\beta_{general}}{\beta_{good \  conductor}})$")
#plot(log10(f), abs((beta_gen(w(f))/beta_bd(w(f)))), "c-.", label = r"$(\frac{\beta_{general}}{\beta_{good \  dielectric}})$")

#Embellecemos la gráfica
xlabel(r"$log_{10}(f)$", fontsize = 20)
ylabel((r"$log_{10}(v$)"), fontsize = 20)
legend(loc = 2, fontsize = 20)

grid()

xlim(left = log10(40*10**3))
axvspan(log(1), log10(f_cond), alpha = 0.3, color = "palegreen")
axvspan(log10(f_diel), log10(f_diel*10**3), alpha = 0.3, color = "paleturquoise")

"""
#MODULO DE ETA

"""
clf()

def modulo_eta_bd(f):
    mod_eta_bd = sqrt(mu/eps)
    return mod_eta_bd

plot(log10(f),log10(modulo_eta_gen(w(f), alfa_gen(w(f)), beta_gen(w(f)))), "r-", label = r"$\eta_{general}$")
plot(log10(f),log10(modulo_eta_bd(f)), "b-", label = r"$\eta_{good \ diel}$")
axhline(y = log10(sqrt(mu/eps)), color="b", linestyle = "-", label = r"$\eta_{good \ diel}$")

#plot(log10(f),log10(modulo_eta_bc(w(f))), "g-", label = r"$\eta_{good \ cond}$")

#Comparamos beta en cada caso con el general
#plot(log10(f), abs((beta_gen(w(f))/alfa_bc(w(f)))), "m-.", label = r"$(\frac{\beta_{general}}{\beta_{good \  conductor}})$")
#plot(log10(f), abs((beta_gen(w(f))/beta_bd(w(f)))), "c-.", label = r"$(\frac{\beta_{general}}{\beta_{good \  dielectric}})$")

#Embellecemos la gráfica
xlabel(r"$log_{10}(f)$", fontsize = 20)
ylabel((r"$log_{10}(|\eta|$)"), fontsize = 20)
legend(loc = 2, fontsize = 20)

grid()

xlim(left = log10(40*10**3))
axvspan(log(1), log10(f_cond), alpha = 0.3, color = "palegreen")
axvspan(log10(f_diel), log10(f_diel*10**3), alpha = 0.3, color = "paleturquoise")

"""
"""
clf()


def modulo_eta_bd(f):
    mod_eta_bd = sqrt(mu/eps)
    return mod_eta_bd

plot(log10(f),log10(fase_eta_gen(alfa_gen(w(f)), beta_gen(w(f)))), "r-", label = r"$\eta_{general}$")
#plot(log10(f),log10(modulo_eta_bd(f)), "b-", label = r"$\eta_{good \ diel}$")
axhline(y = log10(pi/4), color="g", linestyle = "-", label = r"$\eta_{good \ diel}$")

plot(log10(f),log10(fase_eta_bd(w(f))), "b-", label = r"$\eta_{good \ cond}$")

#Comparamos beta en cada caso con el general
#plot(log10(f), abs((beta_gen(w(f))/alfa_bc(w(f)))), "m-.", label = r"$(\frac{\beta_{general}}{\beta_{good \  conductor}})$")
#plot(log10(f), abs((beta_gen(w(f))/beta_bd(w(f)))), "c-.", label = r"$(\frac{\beta_{general}}{\beta_{good \  dielectric}})$")

#Embellecemos la gráfica
xlabel(r"$log_{10}(f)$", fontsize = 20)
ylabel((r"$log_{10}(|\eta|$)"), fontsize = 20)
legend(loc = 2, fontsize = 20)

grid()

xlim(left = log10(40*10**3))
axvspan(log(1), log10(f_cond), alpha = 0.3, color = "palegreen")
axvspan(log10(f_diel), log10(f_diel*10**3), alpha = 0.3, color = "paleturquoise")

"""
def derive(data, dt):
# Dérivation numérique 
# data = vecteur de données
# dt   = pas de temps
    drv = []
    for i in range(len(data)):
        if i == 0: # point 1 : dérivé avant
            drv.append(((data[i+1]-data[i])/dt))
        elif i == (len(data) - 1):# point final : dérivé arrière
            drv.append(((data[i]-data[i-1])/dt))
        else: # point médiants : dérivé centré (plus précis)
            drv.append(((data[i+1]-data[i-1])/(2*dt)))
    return drv
    
    
def integral(data, dt):
# Dérivation numérique 
# data = vecteur de données
# dt   = pas de temps
    int = []   # vecteur de sortie
    hs3 = dt/3 # h/3 
    for i in range(len(data)):
        if i == 0 or i == (len(data) - 1): # point 1 ou final : methode des rectangles
            drv.append((data[i]*dt))
        else: # point médiants : méthode de simpson (plus précis) 
              # ref: https://en.wikipedia.org/wiki/Simpson's_rule
            drv.append(((data[i-1]+4*data[i]+data[i+1])*hs3))
    return int
    
    
    
    
    
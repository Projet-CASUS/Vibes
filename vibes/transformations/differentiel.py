def derive(data, dt):
    """
    Derivation numerique
    !!! -> attention cette methode fait perdre la premiere et la derniere donnee du vecteur
    TODO Faire recevoir et retourner un vecteur panda
    :param data: -> vecteur panda > Contient les donnees a deriver
    :param dt: TODO Louis-Philippe que veux tu dire par "pas de temps" ??
    :return: -> vecteur panda > vecteur des donnees derivees
    """
# Dérivation numérique 
# data = vecteur de données
# dt   = pas de temps
    drv_list = [0]
    for i in range(len(data)):
        if i == 0: # point 1 : dérivé avant
            drv_list.append(((data[i + 1] - data[i]) / dt))
        elif i == (len(data) - 1):# point final : dérivé arrière
            drv_list.append(((data[i] - data[i - 1]) / dt))
        else: # point médiants : dérivé centré (plus précis)
            drv_list.append(((data[i + 1] - data[i - 1]) / (2 * dt)))
    return drv_list
    
    
def integral(data, dt):
    """
    Integration numerique
    !!! -> attention cette methode fait perdre la premiere et la derniere donnee du vecteur
    TODO Faire recevoir et retourner un vecteur panda
    :param data: -> vecteur panda > Contient les donnees a integrer
    :param dt: TODO Louis-Philippe que veux tu dire par "pas de temps" ??
    :return: -> vecteur panda > vecteur des donnees integrees
    """
    integ_list = []   # vecteur de sortie
    hs3 = dt/3 # h/3 
    for i in range(len(data)):
        if i == 0 or i == (len(data) - 1): # point 1 ou final : methode des rectangles
            integ_list.append((data[i]*dt))
        else: # point médiants : méthode de simpson (plus précis) 
              # ref: https://en.wikipedia.org/wiki/Simpson's_rule
            integ_list.append(((data[i-1]+4*data[i]+data[i+1])*hs3))
    return integ_list

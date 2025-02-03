"""
Type d'apprentissage : Q_learning
 --- > Parametre d'entree : 
coordonnées de mon tank, 
direction, 
sens, 
direction de la tourelle, 
si ma tourelle est chargée,
coordonnées de la boite,
coordonnées tank adverse,


 --- > Parametre caché : 
taille entre 64 et 256
 
 --- > Parametre de sortie : 
rien,
avancer,
reculer,
tourner la base a gauche,
tourner la base a droite,
tourner la tourelle a gauche,
tourner la touelle a droite,
tirer,
  
self.model = Linear_QNet(11, 256, 3) #input size, hidden size, output size
                    
    
    
"""
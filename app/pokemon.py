class Pokemon():

    def __init__(self, name, taille, categorie, poids, stats, image_path):
        self.name  = name
        self.taille = taille
        self.categorie = categorie
        self.poids = poids
        self.stats = stats
        self.image_path = image_path
    
    
    def toString(self):
        print(self.name)
        print(self.taille)
        print(self.categorie)
        print(self.poids)
        print(self.stats)

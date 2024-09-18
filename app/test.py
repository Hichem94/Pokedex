import cv2

# Ouvrir la caméra (indice 0 pour la première caméra)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Impossible d'accéder à la caméra")
else:
    print("Caméra trouvée et accessible")

while True:
    # Capture image par image
    ret, frame = cap.read()
    if ret:
        # Afficher l'image capturée
        cv2.imshow('frame', frame)

        # Quitter avec la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Problème avec la capture")

# Libérer la caméra
cap.release()
cv2.destroyAllWindows()

import cv2
import datetime
import os

#Funktionen für:
#Umrandung menschlicher Gesichter
#Ausschneidung menschlicher Gesichter
#Einlesen von Bildern aus einem Verzeichnis
#Speicherung einer Bildliste
#Löschen der Dateien eines Verzeichnisses


#Greift auf die Webcam zu und schießt ein Bild.
#destPath: Zielpfad der Bildaufnahme
def takeImage(destPath):
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise Exception("takeImage: Camera already open")

    result, image = camera.read()

    camera.release()
    if result:
        date = datetime.datetime.now().strftime("%Y-%m-%d H_%H M_%M S_%S")
        cv2.imwrite(destPath+date+".png", image)
    else:
        raise Exception("Camera read error")

#Umrandet menschliche Gesichter mit einem Rechteck.
#Return: Bilder mit Umrandungen als Liste
def rectangleImage(imageList, scaleFactor = 1.1):

    if len(imageList) == 0:
        raise ValueError("rectangleImage: Liste mit Bildern leer -> Keine Speicherung moeglich")

    cascade = cv2.CascadeClassifier('venv/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml')
    rectangleBorder = 2
    rectangledImages = []

    for image in imageList:
        #Haar Klassifizierer erkennt nur monotonfarbige Bilder
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces_rect = cascade.detectMultiScale(gray_image, scaleFactor=scaleFactor, minNeighbors=5)

        for (x, y, w, h) in faces_rect:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), rectangleBorder)
        rectangledImages.append(image)

    return rectangledImages

#Schneidet alle (erkannten) menschlichen Gesichter innerhalb eines Bildes aus
#Return: Ausgeschnittene Gesichter als Liste
def cropImages(imageList, scaleFactor = 1.1):

    if len(imageList) == 0:
        raise ValueError("cropImages: Liste mit Bildern leer -> Keine Speicherung moeglich")

    cascade = cv2.CascadeClassifier('venv/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml')

    rectangleBorder = 2
    croppedImages = []

    for image in imageList:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_rect = cascade.detectMultiScale(gray_image, scaleFactor, 5)
        for (x, y, w, h) in faces_rect:
            crop = image[y + rectangleBorder:y + h - rectangleBorder, x + rectangleBorder:x + w - rectangleBorder]
            croppedImages.append(crop)

    return croppedImages

#Speichert die Bilder in einer Liste
#imageList: Liste mit Bildern
#destPath: Speicherort
def saveImages(imageList, destPath):
    if len(imageList) == 0:
        raise ValueError("saveImages: Liste mit Bildern leer -> Keine Speicherung moeglich")
    counter = 0
    if len(imageList)!=0:
        for image in imageList:
            counter += 1
            date = datetime.datetime.now().strftime("%Y-%m-%d H_%H M_%M S_%S"+ " " + str(counter))
            cv2.imwrite(destPath + date+ ".png", image)

#srcPath: Liest Bilder an einem Zielort ein
#Return: Bilder innerhalb einer Liste
def readImages(srcPath):
    imageNames = os.listdir(srcPath)
    if len(imageNames) == 0:
        raise ValueError("readImages: Verzeichnis enthaelt keine Dateien -> Keine Dateiauslesung moeglich")
    imageList = [cv2.imread(srcPath+imageName) for imageName in imageNames]

    return imageList

#Entfernt Files innerhalb eines Verzeichnisses
def clearFolder(location):
    imageList = os.listdir(location)
    for imageName in imageList:
        os.remove(location+imageName)


#TakeAndFrontFaceDetect(2)
#takeImage();
#clearFolder("OutputImages/rectangleImages/")


#imageList = readImages("Beispielpfad/Beispielverzeichnis/")
#imageList = cropImages(imageList)
#saveImages(imageList, "Beispielpfad/Beispielverzeichnis")
# Librerias utilizadas
import cv2
import mediapipe as mp
import time
import numpy as np

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Alto y ancho de frames
width = 600
height = 400


# Definicion de captura de camara 0, 1, 2, 3 (Dependiendo de qu e camara quiero usar)
cap = cv2.VideoCapture(0)

# Tiempo transcurrido
pTime = 0


# Definicion de color Inical RGB
r = 173
g = 255
b = 47

# Inicia contador de tiempo
inicio = time.time()
contador = 1

# Definicion del estado (0 = Dibujo constante / 1 = Personaje estatico)
estado = 0


# Definicion de fondo a usar
fondo = cv2.imread("persp2.png")

# Punto utilizado como referencia
pp1 = 20

# Periodo de reseteo de imagen
T = 10

while True:

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    fps = cap.get(cv2.CAP_PROP_FPS)
    pTime = cTime
    fin = time.time()
    seg = int(fin - inicio)
    #print(seg)

    if estado == 1:
        fondo = cv2.imread("persp2.png")
    elif estado == 0:
        if seg == (T * contador):
            fondo = cv2.imread("persp2.png")
            seg = 0
            contador += 1
    print(estado)

    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    results = pose.process(imgRGB)

    try:
        x1 = int(results.pose_landmarks.landmark[pp1].x * w)
        y1 = int(results.pose_landmarks.landmark[pp1].y * h)
    except AttributeError:
        x1 = 0
        y1 = 0



    # print(results.pose_landmarks)
    if results.pose_landmarks is not None:
        # Dibujo de landmarks de todo el cuerpo
        mpDraw.draw_landmarks(fondo, results.pose_landmarks, mpPose.POSE_CONNECTIONS,
                              mpDraw.DrawingSpec(color=(b, g, r), thickness=3, circle_radius=1),
                              mpDraw.DrawingSpec(color=(r, g, b), thickness=3, circle_radius=4))

        # Seleccion del punto especifico de referencia
        x1 = int(results.pose_landmarks.landmark[pp1].x * width)
        y1 = int(results.pose_landmarks.landmark[pp1].y * height)

        # print(fondo.shape[0])

        # Dibujo de circulo en punto de referencia
        cv2.circle(fondo, (x1, y1), 5, (255, 255, 255), 10)

        # Linea horizontal en la pantalla
        cv2.line(fondo,
                 (int(fondo.shape[1]/6)*2, int(fondo.shape[1]/15)),
                 (int(fondo.shape[1]/6)*4, int(fondo.shape[1]/15)),
                 (255, 255, 255), 4)

        cv2.line(fondo,
                 (int(fondo.shape[1] / 6) * 2, 0),
                 (int(fondo.shape[1] / 6) * 2, int(fondo.shape[1] / 15)),
                 (255, 255, 255), 4)

        cv2.line(fondo,
                 (int(fondo.shape[1] / 6) * 3, 0),
                 (int(fondo.shape[1] / 6) * 3, int(fondo.shape[1] / 15)),
                 (255, 255, 255), 4)

        cv2.line(fondo,
                 (int(fondo.shape[1] / 6) * 4, 0),
                 (int(fondo.shape[1] / 6) * 4, int(fondo.shape[1] / 15)),
                 (255, 255, 255), 4)


        #cv2.line(fondo, (150, 0), (150, 50), (255, 255, 255), 4)  # Primera linea de division
        #cv2.line(fondo, (300, 0), (300, 50), (255, 255, 255), 4)  # Segunda linea de division
        #cv2.line(fondo, (450, 0), (450, 50), (255, 255, 255), 4)  # Tercera linea de division


        cv2.circle(fondo, (int(fondo.shape[1]/15), int(fondo.shape[0]/5)), 10, (12, 141, 232), 20)
        cv2.circle(fondo, (int(fondo.shape[1]/15), int(fondo.shape[0]/5)*2), 10, (0, 255, 189), 20)
        cv2.circle(fondo, (int(fondo.shape[1]/15), int(fondo.shape[0]/5)*3), 10, (107, 0, 255), 20)
        cv2.circle(fondo, (int(fondo.shape[1]/15), int(fondo.shape[0]/5)*4), 10, (232, 22, 21), 20)

        cv2.circle(fondo, (int(fondo.shape[1] / 15)*14, int(fondo.shape[0] / 5)), 10, (242, 136, 200), 20)
        cv2.circle(fondo, (int(fondo.shape[1] / 15)*14, int(fondo.shape[0] / 5) * 2), 10, (242, 183, 34), 20)
        cv2.circle(fondo, (int(fondo.shape[1] / 15)*14, int(fondo.shape[0] / 5) * 3), 10, (98, 217, 35), 20)
        cv2.circle(fondo, (int(fondo.shape[1] / 15)*14, int(fondo.shape[0] / 5) * 4), 10, (65, 65, 191), 20)


    # Cambio de estados
    if (int(fondo.shape[1] / 6) * 2 < x1 < int(fondo.shape[1] / 6) * 3) and (0 < y1 < int(fondo.shape[1] / 15)):
        estado = 1
    if (int(fondo.shape[1] / 6) * 3 < x1 < int(fondo.shape[1] / 6) * 4) and (0 < y1 < int(fondo.shape[1] / 15)):
        estado = 0

    # Si el punto de referencia se encuentra dentro de las casillas se cambia el color
    # Cuadrante Izquierda
    if (0 < x1 < int(fondo.shape[1]/15)) and (0 < y1 < int(fondo.shape[0]/5)):
        b, g, r = 232, 141, 12

    elif (0 < x1 < int(fondo.shape[1]/15)) and (int(fondo.shape[0]/5) < y1 < int(fondo.shape[0]/5)*2):
        b, g, r = 189, 255, 0

    elif (0 < x1 < int(fondo.shape[1]/15)) and (int(fondo.shape[0]/5)*2 < y1 < int(fondo.shape[0]/5)*3):
        b, g, r = 255, 0, 107

    elif (0 < x1 < int(fondo.shape[1]/15)) and (int(fondo.shape[0]/5)*3 < y1 < int(fondo.shape[0]/5)*4):
        b, g, r = 21, 22, 232

    # Colores Derecha
    elif (int(fondo.shape[1] / 15)*14 < x1 < int(fondo.shape[1])) and (0 < y1 < int(fondo.shape[0]/5)):
        b, g, r = 200, 136, 242

    elif (int(fondo.shape[1] / 15)*14 < x1 < int(fondo.shape[1])) and (int(fondo.shape[0]/5) < y1 < int(fondo.shape[0]/5)*2):
        b, g, r = 34, 183, 242

    elif (int(fondo.shape[1] / 15)*14 < x1 < int(fondo.shape[1])) and (int(fondo.shape[0]/5)*2 < y1 < int(fondo.shape[0]/5)*3):
        b, g, r = 35, 217, 98

    elif (int(fondo.shape[1] / 15)*14 < x1 < int(fondo.shape[1])) and (int(fondo.shape[0]/5)*3 < y1 < int(fondo.shape[0]/5)*4):
        b, g, r = 191, 65, 65


    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    img = cv2.resize(img, (width, height))
    fondo = cv2.resize(fondo, (width, height))

    cv2.imshow("Image", fondo)
    cv2.imshow("Imagen2", img)
    cv2.waitKey(10)
# -*- coding: utf-8 -*-
# библиотека opencv (получение и обработка изображения)
import cv2
# библиотека mediapipe (распознавание рук)
import mediapipe as mp


# получаем изображение с камеры (0 - порядковый номер камеры в системе)
camera = cv2.VideoCapture(0)
mpHands = mp.solutions.hands            # подключаем раздел распознавания рук
hands = mpHands.Hands()                 # создаем объект класса "руки"
mpDraw = mp.solutions.drawing_utils     # подключаем инструменты для рисования


# создаем массив из 21 ячейки для хранения высоты каждой точки
ph = [0 for i in range(21)]
pw = [0 for i in range(21)]
# создаем массив из 5 ячеек для хранения положения каждого пальца
finger = [0 for i in range(5)]

# функция, возвращающая расстояние по модулю (без знака)


def distance(point1, point2):
    return abs(point1 - point2)


def pifagor(ph, pw):
    return(ph**2+pw**2)**0.5


while True:
    # получаем один кадр из видеопотока
    good, img = camera.read()
    # преобразуем кадр в RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # получаем результат распознавания
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:                            # если обнаружили точки руки
        for handLms in results.multi_hand_landmarks:            # получаем координаты каждой точки

            # при помощи инструмента рисования проводим линии между точками
            # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # работаем с каждой точкой по отдельности
            # создаем список от 0 до 21 с координатами точек
            for id, point in enumerate(handLms.landmark):
                # получаем размеры изображения с камеры и масштабируем
                width, height, color = img.shape
                width, height = int(point.x * height), int(point.y * width)

                ph[id] = height           # заполняем массив высотой каждой точки
                pw[id] = width
                # if id == 8:              # выбираем нужную точку
                # рисуем нужного цвета кружок вокруг выбранной точки
                #    cv2.circle(img, (width, height), 15, (255, 0, 255), cv2.FILLED)
                # if id == 12:
                #    cv2.circle(img, (width, height), 15, (0, 0, 255), cv2.FILLED)

            # получаем расстояние, с которым будем сравнивать каждый палец
            distanceGood = pifagor(
                distance(ph[0], ph[5]), distance(pw[0], pw[5]))*1.3
            # заполняем массив 1 (палец поднят) или 0 (палец сжат)
            finger[1] = 1 if pifagor(distance(ph[0], ph[8]), distance(
                pw[0], pw[8])) > distanceGood else 0
            finger[2] = 1 if pifagor(distance(ph[0], ph[12]), distance(
                pw[0], pw[12])) > distanceGood else 0
            finger[3] = 1 if pifagor(distance(ph[0], ph[16]), distance(
                pw[0], pw[16])) > distanceGood else 0
            finger[4] = 1 if pifagor(distance(ph[0], ph[20]), distance(
                pw[0], pw[20])) > distanceGood else 0
            finger[0] = 1 if pifagor(distance(ph[0], ph[4]), distance(
                pw[0], pw[4])) > distanceGood else 0

            # готовим сообщение для отправки
            msg = ''
            # 0 - большой палец, 1 - указательный, 2 - средний, 3 - безымянный, 4 - мизинец
            # жест "коза" - 01001
            if finger[0] and not finger[1] and not finger[2] and not finger[3] and not finger[4]:
                msg = 'большой палец'
            elif not finger[0] and finger[1] and not finger[2] and not finger[3] and not finger[4]:
                msg = 'указателный палец'
            elif finger[0] and finger[1] and not finger[2] and not finger[3] and finger[4]:
                msg = 'Я тебя люблю'
            elif finger[1] and finger[2] and not finger[3] and not finger[4]:
                msg = 'Peace'
            elif not (finger[1] and finger[2] and finger[3] and finger[4]):
                msg = "сжатый кулак"

            cv2.putText(img, msg, (pw[2], ph[2]),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow("Image", img)           # выводим окно с нашим изображением
    if cv2.waitKey(1) == ord('q'):     # ждем нажатия клавиши q в течение 1 мс
        break                          # если нажмут, всё закрываем
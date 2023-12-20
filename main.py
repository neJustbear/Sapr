import json
import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import QRectF, Qt, QLineF
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMessageBox, QGraphicsRectItem, QGraphicsScene, \
    QGraphicsView, QGraphicsItem, QGraphicsLineItem
from numpy import linalg
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import pandas as pd

Form, Window = uic.loadUiType("1.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

stergn = {}
sos_nag = {}
ras_nag = {}
zadelka = ''

def add_row(table):
    row_Count = table.rowCount()
    table.insertRow(row_Count)

def delete_row(table):
    row_Count = table.rowCount()
    table.removeRow(row_Count - 1)

form.pushButton_3.clicked.connect(lambda : add_row(form.tableWidget_2))
form.pushButton_4.clicked.connect(lambda : delete_row(form.tableWidget_2))

form.pushButton_5.clicked.connect(lambda : add_row(form.tableWidget_3))
form.pushButton_6.clicked.connect(lambda : delete_row(form.tableWidget_3))

form.pushButton_7.clicked.connect(lambda : add_row(form.tableWidget_4))
form.pushButton_8.clicked.connect(lambda : delete_row(form.tableWidget_4))

def get_data1(table):
    for row in range(table.rowCount()):
        stergn[row + 1] = [int(table.item(row, i).text())
            for i in range(table.columnCount())
            if table.item(row, i) is not None]

def get_data2(table):
    for row in range(table.rowCount()):
        sos_nag[row + 1] = [int(table.item(row, i).text())
            for i in range(table.columnCount())
            if table.item(row, i) is not None]

def get_data3(table):
    for row in range(table.rowCount()):
        ras_nag[row + 1] = [int(table.item(row, i).text())
            for i in range(table.columnCount())
            if table.item(row, i) is not None]

def num2(row, column):
    try:
        float(form.tableWidget_2.item(row, column).text())
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Ошибка")
        msg.setInformativeText('Данные введены неправильно')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

def num3(row, column):
    try:
        float(form.tableWidget_3.item(row, column).text())
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Ошибка")
        msg.setInformativeText('Данные введены неправильно')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

def num4(row, column):
    try:
        float(form.tableWidget_4.item(row, column).text())
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Ошибка")
        msg.setInformativeText('Данные введены неправильно')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

def set_zadelka(box):
    global zadelka
    if box.currentText() == "Заделка слева":
        zadelka = 'left'
    elif box.currentText() == "Заделка справа":
        zadelka = 'right'
    else:
        zadelka = 'from two sides'

def save():
    file_path = "save.json"
    with open(file_path, "w") as file:
        json.dump([{"Kernel": stergn}, {"Concentrated load": sos_nag}, {"Distributed load": ras_nag}, {"Support": zadelka}], file, indent=4)
        print("JSON сохранен успешно.")


def visualization(view):
    global stergn, zadelka, sos_nag, ras_nag
    x = 0
    y = 0
    count = len(stergn.keys())
    scene = QGraphicsScene()
    scene_rect = QRectF(0, 0, 941, 621)
    view.setSceneRect(scene_rect)
    for key, val in stergn.items():
        y = 25 * val[1]
        rect = QGraphicsRectItem(QRectF(30+x, 310.5 - y, 100*val[0], 50*val[1]))
        scene.addItem(rect)
        for key2, val2 in ras_nag.items():
            if val2[0] == key:
                line2 = QGraphicsLineItem(QLineF(30 + x, 310.5, 30+100*val[0]+x, 310.5))
                scene.addItem(line2)
                for i in np.arange(30+x, 30+100*val[0]+x, 10):
                    if val2[1] < 0:
                        line5 = QGraphicsLineItem(QLineF(i, 310.5, i + 5, 315.5))
                        line6 = QGraphicsLineItem(QLineF(i, 310.5, i + 5, 306.5))
                        scene.addItem(line5)
                        scene.addItem(line6)
                    elif val2[1] > 0:
                        line3 = QGraphicsLineItem(QLineF(i + 10, 310.5, i + 5, 315.5))
                        line4 = QGraphicsLineItem(QLineF(i + 10, 310.5, i + 5, 306.5))
                        scene.addItem(line3)
                        scene.addItem(line4)
        for key1, val1 in sos_nag.items():
            if val1[0] == key:
                if val1[1] < 0:
                    line7 = QGraphicsLineItem(QLineF(30 + x, 310.5, x, 310.5))
                    scene.addItem(line7)
                    line9 = QGraphicsLineItem(QLineF(x, 310.5, x + 15, 320.5))
                    scene.addItem(line9)
                    line10 = QGraphicsLineItem(QLineF(x, 310.5, x + 15, 300.5))
                    scene.addItem(line10)
                elif val1[1] > 0:
                    line8 = QGraphicsLineItem(QLineF(30 + x, 310.5, 30 + x + 30, 310.5))
                    scene.addItem(line8)
                    line11 = QGraphicsLineItem(QLineF(30 + x + 30, 310.5, 30 + x + 15, 320.5))
                    scene.addItem(line11)
                    line12 = QGraphicsLineItem(QLineF(30 + x + 30, 310.5, 30 + x + 15, 300.5))
                    scene.addItem(line12)
            if val1[0] == count + 1 and key == count:
                if val1[1] < 0:
                    line13 = QGraphicsLineItem(QLineF(30 + x + 100*val[0], 310.5, x + 100*val[0], 310.5))
                    scene.addItem(line13)
                    line14 = QGraphicsLineItem(QLineF(x + 100*val[0], 310.5, x + 15 + 100*val[0], 320.5))
                    scene.addItem(line14)
                    line15 = QGraphicsLineItem(QLineF(x + 100*val[0], 310.5, x + 15 + 100*val[0], 300.5))
                    scene.addItem(line15)
                elif val1[1] > 0:
                    line16 = QGraphicsLineItem(QLineF(30 + x + 100*val[0], 310.5, 30 + x + 30 + 100*val[0], 310.5))
                    scene.addItem(line16)
                    line17 = QGraphicsLineItem(QLineF(30 + x + 30 + 100*val[0], 310.5, 30 + x + 15 + 100*val[0], 320.5))
                    scene.addItem(line17)
                    line18 = QGraphicsLineItem(QLineF(30 + x + 30 + 100*val[0], 310.5, 30 + x + 15 + 100*val[0], 300.5))
                    scene.addItem(line18)
        x += 100*val[0]
        if zadelka == 'left' and key == 1:
            point1 = 310.5 - val[1] * 35
            point2 = 310.5 + val[1] * 35
            line = QGraphicsLineItem(QLineF(30, point1, 30, point2))
            scene.addItem(line)
            for i in np.arange(point1, point2, 7):
                line1 = QGraphicsLineItem(QLineF(30, i, 23, i+7))
                scene.addItem(line1)
        if zadelka == 'right' and key == count:
            point1 = 310.5 - val[1] * 35
            point2 = 310.5 + val[1] * 35
            line = QGraphicsLineItem(QLineF(30+x, point1, 30+x, point2))
            scene.addItem(line)
            for i in np.arange(point1, point2, 7):
                line1 = QGraphicsLineItem(QLineF(30+x, i+7, 37+x, i))
                scene.addItem(line1)
        if zadelka == 'from two sides':
            if key == 1:
                point1 = 310.5 - val[1] * 35
                point2 = 310.5 + val[1] * 35
                line = QGraphicsLineItem(QLineF(30, point1, 30, point2))
                scene.addItem(line)
                for i in np.arange(point1, point2, 7):
                    line1 = QGraphicsLineItem(QLineF(30, i, 23, i + 7))
                    scene.addItem(line1)
            if key == count:
                point1 = 310.5 - val[1] * 35
                point2 = 310.5 + val[1] * 35
                line = QGraphicsLineItem(QLineF(30 + x, point1, 30 + x, point2))
                scene.addItem(line)
                for i in np.arange(point1, point2, 7):
                    line1 = QGraphicsLineItem(QLineF(30 + x, i + 7, 37 + x, i))
                    scene.addItem(line1)
    view.setScene(scene)
    view.show()


def generateReactionsMatrix(st, z):
    count = len(st)
    j = 0
    A = np.zeros((count+1, count+1), dtype=int).tolist()
    for keys, vals in st.items():
        A[j][j] += vals[1]*vals[2]/vals[0]
        A[j][j+1] -= vals[1]*vals[2]/vals[0]
        A[j+1][j] -= vals[1]*vals[2]/vals[0]
        A[j+1][j+1] += vals[1]*vals[2]/vals[0]
        j += 1
    if z == 'left':
        A[0][0] = 1
        A[1][0] = 0
        A[0][1] = 0
    if z == 'right':
        A[count][count] = 1
        A[count-1][count] = 0
        A[count][count-1] = 0
    if z == 'from two sides':
        A[0][0] = 1
        A[1][0] = 0
        A[0][1] = 0
        A[count][count] = 1
        A[count-1][count] = 0
        A[count][count-1] = 0
    return A

def generateReactionsGlobalVector(st, sn, rs, z):
    count = len(st)
    knots = [0] * (count+1)
    for keys, vals in sn.items():
        knots[vals[0]-1] = vals[1]
    B = [0] * (count+1)
    for i in range(count+1):
        B[i] += knots[i]
        # if i != 0 and i-1 in rs:
        #     B[i] += rs[i-1][1] * st[i-1][0]/2
        # if i != count and i in rs:
        #     B[i] += rs[i][1] * st[i][0]/2
    for keys1, vals1 in rs.items():
        if vals1[0] != 1:
            B[vals1[0]-1] += vals1[1] * st[vals1[0]][0]/2
        if vals1[0] != count:
            B[vals1[0]] += vals1[1] * st[vals1[0]][0]/2
    if z == 'left':
        B[0] = 0
    if z == 'right':
        B[count] = 0
    if z == 'from two sides':
        B[0] = 0
        B[count] = 0
    return B

def generateDeltas(st, sn, rn, z):
    count = len(st)
    A = generateReactionsMatrix(st, z)
    B = generateReactionsGlobalVector(st, sn, rn, z)
    try:
        A = linalg.inv(A)
    except:
        linalg.lstsq(A, A)
    ans = np.dot(A,B)
    return ans

def N(st, sn, rn, z):
    count = len(st)
    A = generateReactionsMatrix(st, z)
    B = generateReactionsGlobalVector(st, sn, rn, z)
    try:
        A = linalg.inv(A)
    except:
        linalg.lstsq(A, A)
    v6 = np.dot(A,B)
    N = np.zeros((count, 2), dtype=int).tolist()
    for keys, val in st.items():
        N[keys-1][0] = (val[1] * val[2]/val[0]) * (v6[keys] - v6[keys-1])
        N[keys-1][1] = (val[1] * val[2] / val[0]) * (v6[keys] - v6[keys - 1])
    for keys1, val1 in rn.items():
        N[val1[0]-1][0] += (val1[1] * st[val1[0]][0] / 2)
        N[val1[0]-1][1] -= val1[1] * st[val1[0]][0] / 2
    return N

def U(st, sn, rn, z):
    count = len(st)
    A = generateReactionsMatrix(st, z)
    B = generateReactionsGlobalVector(st, sn, rn, z)
    try:
        A = linalg.inv(A)
    except:
        linalg.lstsq(A, A)
    v6 = np.dot(A,B)
    U = np.zeros((count, 3), dtype=int).tolist()
    for i in range(count):
        U[i][0] = v6[i]
        U[i][1] = (v6[i+1] - v6[i]) / st[i+1][0]
    for key, val in rn.items():
        U[val[0]-1][1] += (val[1] * st[val[0]][0]) / (2 * st[val[0]][2] * st[val[0]][1])
        U[val[0]-1][2] = -(val[1] / (2*st[val[0]][2] * st[val[0]][1]))
    return U

def Q(st, sn, rn, z):
    count = len(st)
    n1 = N(st, sn, rn, z)
    Q = np.zeros((count, 2), dtype=int).tolist()
    for key, val in st.items():
        Q[key-1][0] = n1[key-1][0] / val[1]
        Q[key - 1][1] = n1[key - 1][1] / val[1]

    return Q

def graphicNx(N, st):
    try:
        sumL = 0
        for key, kern in st.items():
            sumL += kern[0]
        y = []
        for i in range(len(st)):
            x = np.linspace(0, st[i+1][0], int(round(500 * st[i+1][0] / sumL)))
            y1 = (N[i][1] - N[i][0]) / st[i+1][0]
            if y1 != 0:
                y += [N[i][0] + _x * y1 for _x in x]
            else:
                y += [N[i][0] for _x in x]
        x1 = np.linspace(0, sumL, len(y))
        plt.title("N(X)")
        plt.xlabel("L")
        plt.ylabel("N(x)")
        plt.grid()
        plt.plot(x1, y, 'b-')
        plt.show()
    except:
        pass

def graphicUx(U, st):
    sumL = 0
    for key, kern in st.items():
        sumL += kern[0]
    y = []
    for i in range(len(st)):
        x = np.linspace(0, st[i+1][0], int(round(500 * st[i+1][0] / sumL)))
        y += [U[i][0] + _x * U[i][1] + (_x ** 2) * U[i][2] for _x in x]
    x1 = np.linspace(0, sumL, len(y))
    plt.title("U(X)")
    plt.xlabel("L")
    plt.ylabel("U(x)")
    plt.grid()
    plt.plot(x1, y, 'b-')
    plt.show()

def graphicQx(Q, st):
    try:
        sumL = 0
        print(Q)
        for key, kern in st.items():
            sumL += kern[0]
        y = []
        for i in range(len(st)):
            x = np.linspace(0, st[i+1][0], int(round(500 * st[i+1][0] / sumL)))
            y1 = (Q[i][1] - Q[i][0]) / st[i+1][0]
            if y1 != 0:
                y += [Q[i][0] + _x * y1 for _x in x]
            else:
                y += [Q[i][0] for _x in x]
        x1 = np.linspace(0, sumL, len(y))
        plt.title("Q(X)")
        plt.xlabel("L")
        plt.ylabel("Q(x)")
        plt.grid()
        plt.plot(x1, y, 'b-')
        plt.show()
    except:
        pass

def table_N(N, st):
    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    sumL = 0
    totable = []
    for i in range(len(st)):
        x = np.linspace(0, st[i+1][0], 8)
        y = (N[i][1] - N[i][0]) / st[i + 1][0]
        if y != 0:
            for _x in x:
                totable.append([round(_x + sumL, 2), round(N[i][0] + _x * y, 2)])
            sumL += st[i+1][0]
        else:
            for _x in x:
                totable.append([round(_x + sumL, 2), round(N[i][0], 2)])
            sumL += st[i+1][0]
    df = pd.DataFrame(totable,
                      columns=['L (длина)', 'Nx'])

    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', bbox=[0, 0, 1, 1])
    table.scale(1, 2)

    fig.tight_layout()
    plt.show()

def table_U(U, st):
    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    sumL = 0
    totable = []
    for i in range(len(st)):
        x = np.linspace(0, st[i+1][0], 8)
        for _x in x:
            totable.append([round(_x + sumL, 2), round(U[i][0] + _x * U[i][1] + (_x ** 2) * U[i][2], 2)])
        sumL += st[i+1][0]
    df = pd.DataFrame(totable,
                      columns=['L (длина)', 'Ux'])

    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', bbox=[0, 0, 1, 1])
    table.scale(1, 2)

    fig.tight_layout()
    plt.show()

def table_Q(Q, st):
    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    sumL = 0
    totable = []
    for i in range(len(st)):
        x = np.linspace(0, st[i+1][0], 8)
        y = (Q[i][1] - Q[i][0]) / st[i + 1][0]
        if y != 0:
            for _x in x:
                totable.append([round(_x + sumL, 2), round(Q[i][0] + _x * y, 2)])
            sumL += st[i+1][0]
        else:
            for _x in x:
                totable.append([round(_x + sumL, 2), round(Q[i][0], 2)])
            sumL += st[i+1][0]
    df = pd.DataFrame(totable,
                      columns=['L (длина)', 'Qx'])

    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', bbox=[0, 0, 1, 1])
    table.scale(1, 2)

    fig.tight_layout()
    plt.show()

form.pushButton.clicked.connect(lambda : get_data1(form.tableWidget_2))
form.pushButton.clicked.connect(lambda : get_data2(form.tableWidget_3))
form.pushButton.clicked.connect(lambda : get_data3(form.tableWidget_4))
form.pushButton.clicked.connect(lambda : set_zadelka(form.comboBox))
form.pushButton.clicked.connect(lambda : save())
form.pushButton.clicked.connect(lambda : visualization(form.graphicsView))

# form.pushButton_14.clicked.connect(lambda : generateReactionsMatrix(stergn, zadelka))
# form.pushButton_14.clicked.connect(lambda : generateReactionsGlobalVector(stergn, sos_nag, ras_nag, zadelka))
# form.pushButton_14.clicked.connect(lambda : generateDeltas(stergn, sos_nag, ras_nag, zadelka))
# form.pushButton_14.clicked.connect(lambda : N(stergn, sos_nag, ras_nag, zadelka))
# form.pushButton_14.clicked.connect(lambda : U(stergn, sos_nag, ras_nag, zadelka))
# form.pushButton_14.clicked.connect(lambda : Q(stergn, sos_nag, ras_nag, zadelka))

form.pushButton_2.clicked.connect(lambda : graphicNx(N(stergn, sos_nag, ras_nag, zadelka), stergn))
form.pushButton_10.clicked.connect(lambda : graphicUx(U(stergn, sos_nag, ras_nag, zadelka), stergn))
form.pushButton_9.clicked.connect(lambda : graphicQx(Q(stergn, sos_nag, ras_nag, zadelka), stergn))
form.pushButton_11.clicked.connect(lambda : table_N(N(stergn, sos_nag, ras_nag, zadelka), stergn))
form.pushButton_13.clicked.connect(lambda : table_U(U(stergn, sos_nag, ras_nag, zadelka), stergn))
form.pushButton_12.clicked.connect(lambda : table_Q(Q(stergn, sos_nag, ras_nag, zadelka), stergn))

form.tableWidget_2.cellChanged.connect(num2)
form.tableWidget_3.cellChanged.connect(num3)
form.tableWidget_4.cellChanged.connect(num4)


app.exec_()

print(stergn)
print(sos_nag)
print(ras_nag)
print(zadelka)


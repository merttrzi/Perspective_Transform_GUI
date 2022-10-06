from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys
import cv2
import numpy as np

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui file
        uic.loadUi("pers_trans_gui.ui", self)

        # Define our widgets
        self.lineEdit1 = self.findChild(QLineEdit, "lineEdit")
        self.lineEdit2 = self.findChild(QLineEdit, "lineEdit_2")
        self.lineEdit3 = self.findChild(QLineEdit, "lineEdit_3")
        self.lineEdit4 = self.findChild(QLineEdit, "lineEdit_4")
        self.lineEdit5 = self.findChild(QLineEdit, "lineEdit_5")
        self.lineEdit6 = self.findChild(QLineEdit, "lineEdit_6")
        self.lineEdit7 = self.findChild(QLineEdit, "lineEdit_7")
        self.label = self.findChild(QLabel, "label_6")
        self.button = self.findChild(QPushButton, "pushButton")
        
        

        # Click The Dropdown Box
        self.button.clicked.connect(self.clicker)
        
                        
        # Show The App
        self.show()

    def clicker(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "d:\\Images_for_gui\\", "All Files (*);;PNG Files (*.png);;Jpg Files (*.jpg)")

        # Open The Image
        if fname:
            self.pixmap = QPixmap(fname[0])
             

        x1s = self.lineEdit1.text()
        x2s = self.lineEdit2.text()
        y1s = self.lineEdit3.text()
        y2s = self.lineEdit4.text()
       
        MinThresholds= self.lineEdit5.text()

        x1=int(x1s)
        x2=int(x2s)
        y1=int(y1s)
        y2=int(y2s)
        
        MinThreshold=int(MinThresholds)
    
        img1 =cv2.imread(fname[0])

        img_size_x= img1.shape[1]

        scaleFactor=round(1200/img_size_x,1)

        img1 =cv2.resize(img1,(0,0),fx=scaleFactor,fy=scaleFactor)

        roi = img1[y1:y2, x1:x2]
        img = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        ret, dst = cv2.threshold(img, MinThreshold, 255, cv2.THRESH_BINARY_INV)

        kernel =np.ones((10,10),np.uint8)
        img_erosion=cv2.erode(dst,kernel,iterations=1)

        edge = cv2.Canny(img_erosion, 100, 200)


        contours, hierarchy = cv2.findContours(edge, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)


        cnt = contours[0]
        epsilon = 0.05*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)

       #Sorting corner points
        approx_array=[approx[0][0],approx[1][0],approx[2][0],approx[3][0]]
        approx_array.sort(key=lambda row: (row[1]))

        if(approx_array[0][0]>approx_array[1][0]):
            temp= approx_array[0][0]
            approx_array[0][0]=approx_array[1][0]
            approx_array[1][0]=temp
        else:
            pass    
        if(approx_array[2][0]>approx_array[3][0]):

            temp= approx_array[2][0]
            approx_array[2][0]=approx_array[3][0]
            approx_array[3][0]=temp

        else:
            pass   


        width =approx_array[1][0]-approx_array[0][0]
        heigth =approx_array[2][1]-approx_array[0][1]
        heigth = int(0.6/scaleFactor*heigth)
        width = int(0.6/scaleFactor*width)

    
        pts1=np.float32([[approx_array[0]],[approx_array[1]],[approx_array[2]],[approx_array[3]]])
        pts2 = np.float32([[0,0],[width,0],[0,heigth],[width,heigth]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(roi, matrix, (width,heigth))


        cv2.imwrite("Result.jpg", result)

        if fname:
            self.pixmap = QPixmap("Result.jpg")
            # Add Pic to label
            self.label.setPixmap(self.pixmap)
    

# Initialize The App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
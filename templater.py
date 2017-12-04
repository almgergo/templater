#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we create a bit
more complicated window layout using
the QGridLayout manager. 

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""
import codecs
import sys, re
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import (QWidget, QLabel, QLCDNumber, QLineEdit, 
    QTextEdit, QGridLayout, QApplication, QCheckBox, QMenu, QSizePolicy, QAction, QMainWindow, QPushButton,QMessageBox)

import os, errno
print(os.getcwd())

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

dictionaryFile = 'wololololoConfig.config'
dictionary = {}
with open(dictionaryFile) as f:
    for line in nonblank_lines(f):
        li=line.strip()
        if (not li.startswith("#")):
            (key, val) = re.split('[ \t]',line,1)
            dictionary[key] = val.strip()
            print (key + ' ' + val)


class MyLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(MyLineEdit, self).__init__(parent)
        self.textChanged.connect(self.onTextChange)
        self.edited = False;

    def mousePressEvent(self, e):
        if(self.edited == False):
            self.selectAll()  
        else:
            super(MyLineEdit,self).mousePressEvent(e)
    
    def onTextChange(self,e):
        self.edited=True
        
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()    
            
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isdir(path):
                self.setText(path)

class MainWindow(QWidget):
    
    def __init__(self):
        self.aliases = str(dictionary['customVariablesToReplace']).split(',');
        super().__init__()
        self.initUI()
        
    def closeEvent(self, event):
        global dictionary;
        global dictionaryFile;
        
        #if (self.saveProjBox.isChecked()):
        #    dictionary['defaultProject'] = self.projectPathEdit.text(); 
        #
        #    file = open(dictionaryFile, 'w');
        #    for key, value in dictionary.items():
        #        file.write(key + '\t' +value +'\n');
        #    file.close();
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()     
        
    def prepareVariables(self, projectType, fileNamePostfix, preFileName,templateName):
        
        finalPackage = self.packagePre + projectType + '.' + self.packageEditPost.text();
        print('FINAL PACKAGE: ' + finalPackage);
        
        directory = self.projectPathEdit.text() + '/' + preFileName + '-' + projectType + '/';
        directory = directory + dictionary['srcPath'] + finalPackage.replace('.','/');
        fileName = directory + '/' + self.classNameEdit.text() + fileNamePostfix + '.java';
        print ('FILENAME INC: ' + fileName)
        
        self.createFileFromTemplate(self.classNameEdit.text(),
                                    dictionary[templateName],
                                    fileName,
                                    finalPackage,directory)
        
    def createFileFromTemplate(self,className,templateFile,fileName,package,directory):
        global dictionary;
        #print(package)
        with open(templateFile,'r') as myfile:
            template = myfile.read();
        #print(template);
        
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        
        file = open(fileName, 'w');
        #print(fileName)
        #/collection-ing-product-ejb/src/main/resources/META-INF
        
        template = template.replace(dictionary['tmpl_className'],className);
        template = template.replace(dictionary['tmpl_package'],package)
        
        for alias in self.aliases:
            template = template.replace(alias,dictionary[alias]);        

        file.write(template);
        file.close();
    
    def appendEJBxml(self,preFileName,xmlFile,insertionBlockRegex,insertionPointRegex):
        ejbXml = self.projectPathEdit.text() + '/' + preFileName + '-ejb/' + xmlFile;
        
        file = open(ejbXml, 'r');
        data=file.read()
        file.close()
        saveFile = open(ejbXml+'Old', 'w');
        saveFile.write(data)
        saveFile.close()
        
        #print('insertion block:' + insertionBlockRegex)
        #print('insertion point:' + insertionPointRegex)
        firstBlockFromXml = re.search(insertionBlockRegex,data,flags=re.IGNORECASE).group()
        newEjbBlock = re.sub(insertionBlockRegex,r'\1'+self.classNameEdit.text()+r'\4',firstBlockFromXml,flags=re.IGNORECASE)
	
        data = re.sub(insertionPointRegex,newEjbBlock+'\n'+r'\1',data)
        file = open(ejbXml, 'w');
        file.write(data)
        file.close();
           
    
    
    def createStructure(self):
        global dictionary;
        global SRC;
        preFileName = self.projectPathEdit.text().split('/')[-1];
        print(preFileName)
        if (self.beanBox.isChecked()):
            self.prepareVariables('web','Bean',preFileName,'tmpl_bean');
        if (self.ejbifBox.isChecked()):
            self.prepareVariables('ejbif','',preFileName,'tmpl_ejbif');
        if (self.ejbBox.isChecked()):
            self.prepareVariables('ejb','EJB',preFileName,'tmpl_ejb');
        ## ejb.jar-s
        if (self.jbossBox.isChecked()):
            self.appendEJBxml(preFileName,dictionary['jbossEjb'],dictionary['jbossInsertionBlockRegex'],dictionary['jbossInsertionPointRegex']);
        if (self.weblogicBox.isChecked()):
            self.appendEJBxml(preFileName,dictionary['weblogicEjb'],dictionary['weblogicInsertionBlockRegex'],dictionary['weblogicInsertionPointRegex']);

        if (self.blBox.isChecked()):
            self.prepareVariables('bl','Helper',preFileName,'tmpl_bl');
        
        
    def initUI(self):
        global dictionary;
        projectPathLabel = QLabel('Project path: ');
        self.projectPathEdit = MyLineEdit(dictionary['defaultProject']);
        
        classNameLabel = QLabel('Class name: ');
        self.classNameEdit = MyLineEdit('class name here...');
        
        self.packagePre = (dictionary['packagePrefix'] + dictionary['packageProject']);
        packageLabel = QLabel(self.packagePre + 'web/ejbif/ejb/bl.') ;
        self.packageEditPost = MyLineEdit('your package here...');
        
        bean     = QLabel('Bean');
        self.beanBox  = QCheckBox();
        self.beanBox.setChecked(True);

        ejbif    = QLabel('EJBIF');
        self.ejbifBox = QCheckBox();
        self.ejbifBox.setChecked(True);

        ejb      = QLabel('EJB');
        self.ejbBox   = QCheckBox();
        self.ejbBox.setChecked(True);
        
        weblogic = QLabel('Weblogic');
        self.weblogicBox = QCheckBox();
        self.weblogicBox.setChecked(True);
        
        jboss           = QLabel('JBoss');
        self.jbossBox   = QCheckBox();
        self.jbossBox.setChecked(True);

        bl       = QLabel('BL');
        self.blBox    = QCheckBox();
        self.blBox.setChecked(True);
        
        #saveProjectPath       = QLabel('Save project path on exit?');
        #self.saveProjBox    = QCheckBox();
        #self.saveProjBox.setChecked(True);
        
        createSkeletonButton = QPushButton('Create skeleton');
        createSkeletonButton.clicked.connect(self.createStructure);

        grid = QGridLayout();
        grid.setSpacing(1);

        i=0;
        grid.addWidget(projectPathLabel, i, 0);
        grid.addWidget(self.projectPathEdit, i, 1,1,2);
        i+=1;
        grid.addWidget(classNameLabel, i, 0);
        grid.addWidget(self.classNameEdit, i, 1,1,2);
        i+=1;
        grid.addWidget(packageLabel, i, 0,1,2);
        grid.addWidget(self.packageEditPost, i, 2,1,1);
        i+=1;
        grid.addWidget(bean,i,0);
        grid.addWidget(self.beanBox,i,1);
        i+=1;
        grid.addWidget(ejbif,i,0);
        grid.addWidget(self.ejbifBox,i,1);
        i+=1;
        grid.addWidget(ejb, i, 0);
        grid.addWidget(self.ejbBox, i, 1);
        i+=1;        
        grid.addWidget(bl, i, 0);
        grid.addWidget(self.blBox, i, 1);
        i+=1;
        grid.addWidget(weblogic, i, 0);
        grid.addWidget(self.weblogicBox, i, 1);
        i+=1;
        grid.addWidget(jboss, i, 0);
        grid.addWidget(self.jbossBox, i, 1);
        i+=1;
        #grid.addWidget(saveProjectPath, i-2, 2);
        #grid.addWidget(self.saveProjBox, i-1, 2);
        
        
        
        grid.addWidget(createSkeletonButton, i, 0, 1, 2)
#
        self.setLayout(grid) 
        
        self.setGeometry(500, 500, 1000, 400)
        self.setWindowTitle('Create skeleton for screen')    
        self.show()
        
class OptionsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__();

        
 
        

        
        
if __name__ == '__main__':
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

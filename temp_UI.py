#-*- decoding: utf-8 -*-#
# coding or decoding?Just use unicode?
# filename:    temp_UI
# author:   1
# created:   2021/10/16の18:50
# finished:
# 标准库

import sys
# 第三方库
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# 模块
try:
    from code import cacheTemp
except:
    pass
initialize_number = 0


def initialize_function() :
    global initialize_number
    initialize_number += 1
    print("This is an initial line,times=%d" % initialize_number)


class TempUI(QWidget):
    def __init__(self):
        super(TempUI, self).__init__()
        layout=QHBoxLayout()
        self.tab_docker=QTabWidget()
        self.tab_docker.setTabPosition(QTabWidget.South)
        self.tab_docker.setTabShape(QTabWidget.Triangular)
        self.tab_docker.setMovable(True)
        self.tab_docker.setTabBarAutoHide(True)
        # self.tab_docker.setTabsClosable(True)

        self.new_tab2(simplify(cacheTemp.test_cache)[0])

        layout.addWidget(self.tab_docker)
        self.setLayout(layout)

    def new_tab(self,a0):
        temp_row=0
        table=QTableWidget()
        table.setRowCount(len(a0))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['变量名','值','附加值'])
        # table.setVerticalHeaderLabels(['11','22','33'])
        # table.setItem(1,2,QTableWidgetItem('QAQ'))
        for i in a0:
            table.setItem(temp_row,0,QTableWidgetItem(i[0]))
            table.setItem(temp_row,1,QTableWidgetItem(i[1]))
            table.setItem(temp_row,2,QTableWidgetItem(i[2]))
            temp_row+=1
        return table
    def new_tab2(self,a0):
        for k,v in a0.items():
            tab=self.new_tab(v)
            self.tab_docker.addTab(tab,k)
class TempUI2(QWidget):
    def __init__(self):
        super(TempUI2, self).__init__()
        layout=QHBoxLayout()
        self.root=QTreeWidgetItem()
        self.tree=QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(['变量名','值','附加值'])
        self.new_spot2(simplify(cacheTemp.test_cache)[0])
        self.tree.insertTopLevelItem(0,self.root)

        layout.addWidget(self.tree)
        self.setLayout(layout)

    def new_spot(self,k,v):
        temp_row=0
        child=QTreeWidgetItem()
        child.setText(0,k)
        for i in v:
            j=QTreeWidgetItem()
            j.setFlags(Qt.ItemIsEditable|Qt.ItemIsEnabled)
            j.setText(0,i[0])
            j.setText(1,i[1])
            j.setText(2,i[2])
            child.addChild(j)
        return child
    def new_spot2(self,a0):
        for k,v in a0.items():
            branch=self.new_spot(k,v)
            self.root.addChild(branch)

def simplify(all_content) :
    to_new_content = set()
    new_content = {}
    for index in all_content :
        if '_' in index['Label'] and ':' not in index['Label'] :
            to_new_content.add(index['Label'].split('_')[0])
        else :
            to_new_content.add(index['Label'].split(':')[0])
    for index2 in to_new_content :
        new_content[index2] = []
    for index3 in all_content :
        if '_' in index3['Label'] and ':' not in index3['Label'] :
            tempSet = []
            tempSet.append(index3['Label'].split('_' , 1)[-1])
            tempSet.append(index3['Value'])
            tempSet.append(index3['ExValue'])
            new_content[index3['Label'].split('_')[0]].append(tempSet)
        else :
            tempSet = []
            tempSet.append(index3['Label'].split(':')[-1])
            tempSet.append(index3['Value'])
            tempSet.append(index3['ExValue'])
            new_content[index3['Label'].split(':')[0]].append(tempSet)

    return new_content,to_new_content

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ui = TempUI2()
    ui.show()
    sys.exit(app.exec_())


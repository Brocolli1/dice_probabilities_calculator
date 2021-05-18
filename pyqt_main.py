#!/usr/bin/env python3

from operator import index
import sys

from functools import partial

import sys
from PyQt5.QtGui import QIntValidator
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_qt5 import FigureCanvasQT
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QBoxLayout, QCheckBox, QComboBox, QFormLayout, QLayout, QListView, QListWidget, QMessageBox, QRadioButton, QLabel

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
import dice



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)



class PyCalcUi(QMainWindow):
    """PyCalc's View (GUI)."""

    def __init__(self):
        """View initializer."""
        super().__init__()

        self.setWindowTitle("Kości")
        self.setFixedSize(1200, 800)

        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.left = QVBoxLayout()
        self.right = QVBoxLayout()
        self.generalLayout.addLayout(self.left)
        self.generalLayout.addLayout(self.right)

        self._createPlot()
        self._createDisplay()
        self._createList()
        self._createLabels()
        self._createButtons()
        self._createRadio()
        self._createMenu()

    def _createPlot(self):
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        #self.canvas.axes.bar([0,1,2,3,4], [10,1,20,3,40])
        self.left.addWidget(self.canvas)

    def _createDisplay(self):
        """Create the display."""

        self.display = QLineEdit()

        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignLeft)
        self.display.setReadOnly(True)

        self.left.addWidget(self.display)

    def _createLabels(self):
        """Create the buttons."""
        self.labels = {}
        self.names = {}
        labelsLayout = QVBoxLayout()

        labels = {
            "ściany": (0, 0),
            "kości": (0, 1),
            "sukces": (0, 2),
            "liczba": (0, 3),
            "modyfikator": (0, 4),
        }

        for lblText, pos in labels.items():
            self.labels[lblText] = QLineEdit(lblText)
            
            self.labels[lblText].setValidator(QIntValidator())

            self.names[lblText] = QLabel(lblText + ":")
            #self.labels[lblText].setFixedSize(40, 40)
            labelsLayout.addWidget(self.names[lblText])
            labelsLayout.addWidget(self.labels[lblText])
            
            if lblText == "liczba":
                self.check = QCheckBox()
                labelsLayout.addWidget(self.check)

        self.right.addLayout(labelsLayout)

    def _createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()

        buttons = {
            "oblicz": (0, 0),
            "rzuć": (0, 1),
            "dodaj element łańcucha": (0, 2),
        }

        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            #self.buttons[btnText].setFixedSize(15, 40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])

        self.right.addLayout(buttonsLayout)

    def _createList(self):
      self.cb = QComboBox()
      self.cb.addItem("Krok 1")
      self.right.addWidget(self.cb)

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Informacje', self.information)
        self.clear = self.menu.addAction('&Wyczyść')

    def _createRadio(self):
        self.rb = []
        self.radioLayout = QVBoxLayout()
        self.rb.append( QRadioButton("Brak przerzutu", self) )
        self.rb.append( QRadioButton("Przerzut jedynek", self) )
        self.rb.append( QRadioButton("Przerzut nieudanych", self) )
        self.rb.append( QRadioButton("Przerzut x kości", self) )

        self.x_name = QLabel("x: ")
        self.x_input = QLineEdit()
        
        self.x_input.setValidator(QIntValidator())

        self.radioLayout.addWidget(self.rb[0])
        self.radioLayout.addWidget(self.rb[1])
        self.radioLayout.addWidget(self.rb[2])
        self.radioLayout.addWidget(self.rb[3])
        self.radioLayout.addWidget(self.x_name)
        self.radioLayout.addWidget(self.x_input)
        self.radioLayout.addStretch()
        self.right.addLayout(self.radioLayout)

    def setDisplayText(self, text):
        """Set display's text."""
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        """Get display's text."""
        return self.display.text()

    def clearDisplay(self):
        """Clear the display."""
        self.setDisplayText("")

    def information(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Informacje")
        msg.setInformativeText("Aplikacja ma być ułatwieniem dla osób grających w gry planszowe, rpg i bitewne. Jej zadaniem jest obliczanie prawdopodobieństw uzyskania wskazanych wyników rzutów kośćmi oraz dokonywanie symulacji takich rzutów")
        msg.setWindowTitle("Informacje")
        msg.exec_()
            
    def plot(self, roller):
        self.canvas.axes.cla() 
        data = roller.calculate()
        x = list(range(len(data)))
        self.canvas.axes.bar(x, data)

        self.canvas.draw()

    def showRollResult(self, roller):
        result = roller.roll()
        success = ""
        if result[2]:
            success = " Rzut udany!"
        else:
            success = " Rzut nieudany"
        self.setDisplayText("Wyniki rzutu:" + str(result[0]) + " Sukcesy:" + str(result[1]) + success)

    def addStep(self, chain):
        roller = dice.rolling_step()
        chain.add_step(roller)
        self.cb.addItem("Krok " + str(chain.num_of_steps()))

    def changeStep(self, chain):
        index = self.cb.currentIndex()
        self.labels["ściany"].setText(str(chain.steps[index].sides)) 
        self.labels["kości"].setText(str(chain.steps[index].amount_of_dice)) 
        self.labels["sukces"].setText(str(chain.steps[index].success)) 
        self.labels["liczba"].setText(str(chain.steps[index].needed_successes)) 
        self.labels["modyfikator"].setText(str(chain.steps[index].modifier)) 

        self.check.setCheckState(chain.steps[index].success_required  )

        self.x_input.setText(str(chain.steps[index].dice_for_reroll))

        self.rb[int(chain.steps[index].rerolls)].setChecked(True)

    def updateDice(self, chain):
        chain.steps[self.cb.currentIndex()].amount_of_dice = int(self.labels["kości"].text())

    def updateSides(self, chain):
        chain.steps[self.cb.currentIndex()].sides = int(self.labels["ściany"].text())

    def updateSuccess(self, chain):
        chain.steps[self.cb.currentIndex()].success = int(self.labels["sukces"].text())

    def updateNeededSuccesses(self, chain):
        chain.steps[self.cb.currentIndex()].needed_successes = int(self.labels["liczba"].text())

    def updateModifier(self, chain):
        chain.steps[self.cb.currentIndex()].modifier = int(self.labels["modyfikator"].text())

    def updateDiceForRerolls(self, chain):
        chain.steps[self.cb.currentIndex()].dice_for_reroll = int(self.x_input.text())
    
    def updateRerolls(self, chain):
        if self.rb[0].isChecked():
            chain.steps[self.cb.currentIndex()].rerolls = dice.Rerolls.none
        if self.rb[1].isChecked():
            chain.steps[self.cb.currentIndex()].rerolls = dice.Rerolls.ones
        if self.rb[2].isChecked():
            chain.steps[self.cb.currentIndex()].rerolls = dice.Rerolls.all
        if self.rb[3].isChecked():
            chain.steps[self.cb.currentIndex()].rerolls = dice.Rerolls.dice

        
    def updateSuccessRequired(self, chain): 
        chain.steps[self.cb.currentIndex()].success_required = not chain.steps[self.cb.currentIndex()].success_required
   
    def clearChain(self, chain):
        chain.steps = []
        chain.steps.append(dice.rolling_step()) 
        self.cb.clear()
        self.cb.addItem("Krok 1")


class PyCalcCtrl:
    """PyCalc's Controller."""

    def __init__(self, view):
        """Controller initializer."""
        self._view = view
        self.chain = dice.rolling_chain()
        self._connectSignals()
   
    def _connectSignals(self):
        """Connect signals and slots."""

        self._view.buttons["dodaj element łańcucha"].clicked.connect(partial(self._view.addStep, self.chain))
        self._view.buttons["oblicz"].clicked.connect(partial(self._view.plot, self.chain))
        self._view.buttons["rzuć"].clicked.connect(partial(self._view.showRollResult, self.chain))
        self._view.cb.currentIndexChanged.connect(partial(self._view.changeStep, self.chain))
        self._view.labels["kości"].textChanged.connect(partial(self._view.updateDice, self.chain))
        self._view.labels["ściany"].textChanged.connect(partial(self._view.updateSides, self.chain))
        self._view.labels["sukces"].textChanged.connect(partial(self._view.updateSuccess, self.chain))
        self._view.labels["liczba"].textChanged.connect(partial(self._view.updateNeededSuccesses, self.chain))
        self._view.labels["modyfikator"].textChanged.connect(partial(self._view.updateModifier, self.chain))
        self._view.check.stateChanged.connect(partial(self._view.updateSuccessRequired, self.chain))
        
        
        self._view.rb[0].toggled.connect(partial(self._view.updateRerolls, self.chain))
        self._view.rb[1].toggled.connect(partial(self._view.updateRerolls, self.chain))
        self._view.rb[2].toggled.connect(partial(self._view.updateRerolls, self.chain))
        self._view.rb[3].toggled.connect(partial(self._view.updateRerolls, self.chain))

        self._view.x_input.textChanged.connect(partial(self._view.updateDiceForRerolls, self.chain))

        self._view.clear.triggered.connect(partial(self._view.clearChain, self.chain))

        self._view.cb.setCurrentIndex(0)
        self._view.changeStep(self.chain)

        
def main():
    """Main function."""
    pycalc = QApplication(sys.argv)
    view = PyCalcUi()
    view.show()
    PyCalcCtrl(view=view)
    sys.exit(pycalc.exec_())


if __name__ == "__main__":
    main()


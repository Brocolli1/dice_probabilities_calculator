#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import dice

import matplotlib
matplotlib.use('GTK3Agg')  # or 'GTK3Cairo'
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)


def numOnly(source):
        text = source.get_text().strip()
        source.set_text(''.join([i for i in text if i in '0123456789']))

class MyWindow(Gtk.Window):
    def __init__(self):
        """View initializer."""
        super().__init__()

        self.set_title("Kości")
        self.set_default_size(500, 800)

        self.generalLayout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(self.generalLayout)
        self.left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        

        self._createMenu()
        self.generalLayout.add(self.left)
        self.generalLayout.add(self.right)
        self._createPlot()
        self._createDisplay()
        self._createList()
        self._createLabels()
        self._createButtons()
        self._createRadio()

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def _createPlot(self):
        self.fig = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot()
        
        self.canvas = FigureCanvas(self.fig)  # a Gtk.DrawingArea
        self.canvas.set_size_request(800, 600)
        self.left.add(self.canvas)
        #ax.plot(t, s)

    def _createDisplay(self):
        """Create the display."""

        self.display = Gtk.Label("")

        #self.display.setFixedeight(50)
        #self.display.setAlignment(Qt.AlignLeft)
        #self.display.setReadOnly(True)

        self.left.add(self.display)

    def _createLabels(self):
        """Create the buttons."""
        self.labels = {}
        self.names = {}
        labelsLayout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        labels = {
            "liczba ścian": (0, 0),
            "kości": (0, 1),
            "próg sukcesu": (0, 2),
            "wymagana liczba sukcesów": (0, 3),
            "modyfikator": (0, 4),
        }

        for lblText, pos in labels.items():
            self.labels[lblText] = Gtk.Entry()
            self.labels[lblText].set_text(lblText)
            
            self.names[lblText] = Gtk.Label(lblText + ":")
            #self.labels[lblText].setValidator(QIntValidator())

            #self.labels[lblText].setFixedSize(40, 40)
            labelsLayout.add(self.names[lblText])
            labelsLayout.add(self.labels[lblText])

            if lblText == "wymagana liczba sukcesów":
                self.check = Gtk.CheckButton()
                labelsLayout.add(self.check)

        self.right.add(labelsLayout)

    def _createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        buttons = {
            "oblicz": (0, 0),
            "rzuć": (0, 1),
            "dodaj element łańcucha": (0, 2),
        }

        for btnText, pos in buttons.items():
            self.buttons[btnText] = Gtk.Button(label=btnText)
            #self.buttons[btnText].setFixedSize(15, 40)
            buttonsLayout.add(self.buttons[btnText])

        self.right.add(buttonsLayout)

    def _createList(self):
      self.cb = Gtk.ComboBoxText()
      self.cb.append_text("Krok 1")
      self.right.add(self.cb)

    def _createMenu(self):
  
        mb = Gtk.MenuBar()
      
        menu1 = Gtk.Menu()
        
        file = Gtk.MenuItem("Menu")
        file.set_submenu(menu1)
        acgroup = Gtk.AccelGroup()
        self.add_accel_group(acgroup)
        
        
        self.info = Gtk.MenuItem("Informacje")
        self.clear = Gtk.MenuItem("Wyczyść")
        
        menu1.append(self.info)
        menu1.append(self.clear)
        self.info.connect("activate", self.information)
        
        mb.append(file)
        vbox = Gtk.VBox(False, 2)
        vbox.pack_start(mb, False, False, 0)
        
        self.generalLayout.add(vbox)

    def _createRadio(self):
        
        self.radios = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.rb = []
        
        self.rb.append( Gtk.RadioButton(label="Brak przerzutu") )
        self.rb.append( Gtk.RadioButton(label="Przerzut jedynek") )
        self.rb.append( Gtk.RadioButton(label="Przerzut nieudanych") )
        self.rb.append( Gtk.RadioButton(label="Przerzut x kości") )

        self.x_name = Gtk.Label("x: ")

        self.x_input = Gtk.Entry()
        self.x_input.set_text(str(0))
            
        self.radios.pack_start(self.rb[0], True, True, 0)
        self.radios.pack_start(self.rb[1], True, True, 0)
        self.radios.pack_start(self.rb[2], True, True, 0)
        self.radios.pack_start(self.rb[3], True, True, 0)
        self.radios.add(self.x_name)
        self.radios.add(self.x_input)

        self.rb[1].join_group(self.rb[0])
        self.rb[2].join_group(self.rb[0])
        self.rb[3].join_group(self.rb[0])

        self.right.add(self.radios)

    def setDisplayText(self, text):
        """Set display's text."""
        self.display.set_text(text)

    def displayText(self):
        """Get display's text."""
        return self.display.text()

    def clearDisplay(self):
        """Clear the display."""
        self.setDisplayText("")

    def information(self, source):
        msg = Gtk.MessageDialog(parent=self,
                                          flags=Gtk.DialogFlags.MODAL,
                                          type=Gtk.MessageType.INFO,
                                          buttons=Gtk.ButtonsType.OK,
                                          message_format="Aplikacja ma być ułatwieniem dla osób grających w gry planszowe, rpg i bitewne. Jej zadaniem jest obliczanie prawdopodobieństw uzyskania wskazanych wyników rzutów kośćmi oraz dokonywanie symulacji takich rzutów")
        
        msg.run()
        msg.destroy()
        
    def plot(self, source, roller):
        self.ax.cla() 
        data = roller.calculate()
        x = list(range(len(data)))
        self.ax.bar(x, data)

        self.canvas.draw()

    def showRollResult(self, button, roller):
        result = roller.roll()
        success = ""
        if result[2]:
            success = " Rzut udany!"
        else:
            success = " Rzut nieudany"
        self.setDisplayText("Wyniki rzutu:" + str(result[0]) + " Sukcesy:" + str(result[1]) + success)

    def addStep(self, source, chain):
        roller = dice.rolling_step()
        chain.add_step(roller)
        self.cb.append_text("Krok " + str(chain.num_of_steps()))

    def changeStep(self, source, chain):
        index = self.cb.get_active()
        self.labels["liczba ścian"].set_text(str(chain.steps[index].sides)) 
        self.labels["kości"].set_text(str(chain.steps[index].amount_of_dice)) 
        self.labels["próg sukcesu"].set_text(str(chain.steps[index].success)) 
        self.labels["wymagana liczba sukcesów"].set_text(str(chain.steps[index].needed_successes)) 
        self.labels["modyfikator"].set_text(str(chain.steps[index].modifier)) 

        self.x_input.set_text(str((chain.steps[index].dice_for_reroll)))

        self.check.set_active(chain.steps[index].success_required  )

        self.rb[int(chain.steps[index].rerolls)].set_active(True)

    

    def updateDice(self, source, event ,chain):
        numOnly(source)
        chain.steps[self.cb.get_active()].amount_of_dice = int(self.labels["kości"].get_text())

    def updateSides(self, source, event ,chain):
        numOnly(source)
        chain.steps[self.cb.get_active()].sides = int(self.labels["liczba ścian"].get_text())

    def updateSuccess(self, source, event ,chain):
        numOnly(source)
        chain.steps[self.cb.get_active()].success = int(self.labels["próg sukcesu"].get_text())

    def updateNeededSuccesses(self, source, event ,chain):
        numOnly(source)
        chain.steps[self.cb.get_active()].needed_successes = int(self.labels["wymagana liczba sukcesów"].get_text())

    def updateModifier(self, source, event ,chain):
        numOnly(source)
        chain.steps[self.cb.get_active()].modifier = int(self.labels["modyfikator"].get_text())

    def updateDiceToReroll(self, source, event ,chain):
        numOnly(source)
        chain.steps[self.cb.get_active()].dice_for_reroll = int(self.x_input.get_text())
    
    def updateRerolls(self, source, chain):
        if self.rb[0].get_active():
            chain.steps[self.cb.get_active()].rerolls = dice.Rerolls.none
        if self.rb[1].get_active():
            chain.steps[self.cb.get_active()].rerolls = dice.Rerolls.ones
        if self.rb[2].get_active():
            chain.steps[self.cb.get_active()].rerolls = dice.Rerolls.all
        if self.rb[3].get_active():
            chain.steps[self.cb.get_active()].rerolls = dice.Rerolls.dice

        
    def updateSuccessRequired(self, source, chain): 
        chain.steps[self.cb.get_active()].success_required = not chain.steps[self.cb.get_active()].success_required
   
    def clearChain(self, source, chain):
        chain.steps = []
        chain.steps.append(dice.rolling_step()) 
        self.cb.remove_all()
        self.cb.append_text("Krok 1")
        self.cb.set_active(0)


class PyCalcCtrl:
    """PyCalc's Controller."""

    def __init__(self, view):
        """Controller initializer."""
        self._view = view
        self.chain = dice.rolling_chain()
        self._connectSignals()
   
    def _connectSignals(self):
        """Connect signals and slots."""

        self._view.buttons["dodaj element łańcucha"].connect("clicked", self._view.addStep, self.chain)
        self._view.buttons["oblicz"].connect("clicked", self._view.plot, self.chain)
        self._view.buttons["rzuć"].connect("clicked",self._view.showRollResult, self.chain)
        self._view.cb.connect("changed", self._view.changeStep, self.chain)
        self._view.labels["kości"].connect("key-release-event", self._view.updateDice, self.chain)
        self._view.labels["liczba ścian"].connect("key-release-event", self._view.updateSides, self.chain)
        self._view.labels["próg sukcesu"].connect("key-release-event",self._view.updateSuccess, self.chain)
        self._view.labels["wymagana liczba sukcesów"].connect("key-release-event",self._view.updateNeededSuccesses, self.chain)
        self._view.labels["modyfikator"].connect("key-release-event",self._view.updateModifier, self.chain)
        self._view.check.connect("clicked", self._view.updateSuccessRequired, self.chain)
        
        
        self._view.rb[0].connect("toggled", self._view.updateRerolls, self.chain )
        self._view.rb[1].connect("toggled", self._view.updateRerolls, self.chain )
        self._view.rb[2].connect("toggled", self._view.updateRerolls, self.chain )
        self._view.rb[3].connect("toggled", self._view.updateRerolls, self.chain )

        self._view.x_input.connect("key-release-event",self._view.updateDiceToReroll, self.chain)

        self._view.cb.set_active(0)

        self._view.clear.connect("activate", self._view.clearChain, self.chain)



win = MyWindow()
ctrl = PyCalcCtrl(view=win)
#win.show()
Gtk.main()
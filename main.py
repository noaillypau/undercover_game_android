from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
Window.fullscreen = False
Window.size = (360,640)
# screen
from kivy.uix.screenmanager import ScreenManager, Screen
# object
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
# layout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
# prop
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
# python
import json
import numpy as np

ROOT_WIDTH, ROOT_HEIGHT = Window.size

# menu

class MenuWindow(Screen):
    def __init__(self,**kwargs):
        super(MenuWindow,self).__init__(**kwargs)
        self.nbs_players = 4 
        print(ROOT_WIDTH)
        print(ROOT_HEIGHT)
    
    
    def onPushed_NewGame(self):
        sm.current = "gamePrepa"
        
    def onPushed_Words(self):
        sm.current = 'word'
        
    def onPushed_History(self):
        sm.current = 'history'
        
    def onPushed_Stats(self):
        #sm.current = 'stats'
        self.debug()
        
    def debug(self):
        sm.current = 'gameProfile'
        
        
# game
        
        
class GamePrepaWindow(Screen):    
    def onPushed_ReturnMenu(self):
        sm.current = "menu"
        
    def onPushed_LauchGame(self):
        # import default config
        with open('current_game_default.json','r') as f:
            dic_current_game = json.load(f)
            f.close()
        # extract config
        nbs_joueurs = int(self.idInput_nbsMrWhite.text)
        nbs_undercovers = int(self.idInput_nbsUndercovers.text)
        nbs_mrwhite = int(self.idInput_nbsJoueurs.text)
        # edit config
        dic_current_game['game_config']['joueurs'] = nbs_joueurs
        dic_current_game['game_config']['undercovers'] = nbs_undercovers
        dic_current_game['game_config']['mrwhite'] = nbs_mrwhite
        with open('current_game.json','w') as f:
            dic_current_game = json.load(f)
            f.close()        
        sm.current = "gameRound"

class GameRoundWindow(Screen):
    def onPushed_ReturnMenu(self):
        sm.current = "menu"

class GameProfileWindow(Screen):
    def __init__(self,**kwargs):
        super(GameProfileWindow,self).__init__(**kwargs)
        # set name        
        self.name = "gameProfile"
        
    def on_enter(self):
        # import game
        #self.game = self.manager.get_screen("menu").game
        nbs_players = self.manager.get_screen("menu").nbs_players
        # create main layout, boxlayout, and gridlayout
        self.float_layout = FloatLayout()
        self.box_layout = BoxLayout(pos_hint={'x':0.05, 'y':0.1}, 
                                    size_hint=(0.9, 0.6))
        self.grid_layout = GridLayout(cols=2, rows=nbs_players)
        # create main content with text input names
        self.dict_input_text = {}
        for i in range(nbs_players):
            self.dict_input_text[i] = TextInput(text="Nom du joueur")
            self.grid_layout.add_widget(Label(text="Joueur {}".format(i+1)))
            self.grid_layout.add_widget(self.dict_input_text[i])
        # add successive layers of layout
        self.box_layout.add_widget(self.grid_layout)
        self.float_layout.add_widget(self.box_layout)
        self.add_widget(self.float_layout)
        
        # add return to button menu
        button_menu = Button(text='Menu', 
                             pos_hint={"x":0.05,"y":0.85},
                             size_hint= (0.1, 0.1))
        button_menu.bind(on_press=self.onPressed_returnMenu)
        self.add_widget(button_menu)
        
    def onPressed_returnMenu(self,instance):
        sm.current = "menu"
    


# other

class WordWindow(Screen):
    def onPushed_ReturnMenu(self):
        sm.current = "menu"

class HistoryWindow(Screen):
    def onPushed_ReturnMenu(self):
        sm.current = "menu"
        
class StatsWindow(Screen):
    def onPushed_ReturnMenu(self):
        sm.current = "menu"
        
        


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")

sm = WindowManager()
#db = DataBase("users.txt")

screens = [MenuWindow(name="menu"), GamePrepaWindow(name="gamePrepa"),GameRoundWindow(name="gameRound"),GameProfileWindow(name="gameProfile"),WordWindow(name="word"),HistoryWindow(name="history"),StatsWindow(name="stats")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "menu"


class MyMainApp(App):
    def build(self):
        return sm
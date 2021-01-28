import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
# screen
from kivy.uix.screenmanager import ScreenManager, Screen
# object
#from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
#from kivy.uix.image import Image
#from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
# layout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
# prop
#from kivy.properties import ObjectProperty
#from kivy.properties import NumericProperty, StringProperty, ObjectProperty
# python
import json
import numpy as np

class Word(): 
    def words_to_key(word1,word2):
        w1 = "fumée"
        w2 = "vapeur"
        n = min(len(word1),len(word2))
        key = ""
        for i in range(n):
            key += str(ord(word1[i]) + ord(word2[i]))
            if i < n-1:
                key += '_'
        return key

    def add_word(word1, word2):
        with open('game_words.json','r') as f:
            dict_words = json.load(f)
            f.close()

        dict_words[Word.words_to_key(word1,word2)] = [word1, word2]

        with open('game_words.json','w') as f:
            json.dump(dict_words,f,ensure_ascii=False)
            f.close()


import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
# screen
from kivy.uix.screenmanager import ScreenManager, Screen
# object
#from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
#from kivy.uix.image import Image
#from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
# layout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
# prop
#from kivy.properties import ObjectProperty
#from kivy.properties import NumericProperty, StringProperty, ObjectProperty
# python
import json
import numpy as np

#ROOT_WIDTH, ROOT_HEIGHT = Window.size

# menu

class MenuWindow(Screen):
    def __init__(self,**kwargs):
        super(MenuWindow,self).__init__(**kwargs)
        self.nbs_players = 4 
        self.game =  Game()
    
    
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
        self.box_layout = BoxLayout(pos_hint={'x':0.05, 'top':0.8}, 
                                    size_hint=(0.9, 0.3+0.1*nbs_players//2))
        self.grid_layout = GridLayout(cols=2)
        # create main content with text input names
        self.dict_input_text = {}
        for i in range(nbs_players):
            self.dict_input_text[i] = TextInput(text="Nom")
            self.grid_layout.add_widget(Label(text="Joueur {}".format(i+1)))
            self.grid_layout.add_widget(self.dict_input_text[i])
        # add successive layers of layout
        self.box_layout.add_widget(self.grid_layout)
        self.float_layout.add_widget(self.box_layout)
        self.add_widget(self.float_layout)
        
        # add return to button menu
        button_menu = Button(text='Menu', 
                             pos_hint={"x":0.05,"y":0.85},
                             size_hint= (0.1, 0.05))
        button_menu.bind(on_press=self.onPressed_returnMenu)
        self.add_widget(button_menu)
        
        # add Submit button
        button_submit = Button(text='Submit', 
                             pos_hint={"x":0.85,"y":0.05},
                             size_hint= (0.1, 0.05))
        button_submit.bind(on_press=self.onPressed_submit)
        self.add_widget(button_submit)
        
        print(self.width)
        print(self.height)
        
    def onPressed_returnMenu(self,instance):
        sm.current = "menu"
        
    def onPressed_submit(self,instance):
        # for each text_input widget, we add the content(i.e player_name) to the game object stored in menu screen
        for key in self.dict_input_text.keys():
            self.manager.get_screen("menu").game.player_add(self.dict_input_text[key].text)
        # show players
        self.manager.get_screen("menu").game.show_players()
        # we go to next screen
        self.manager.transition.direction = "down"
        sm.current = "gameRound"
    


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

if __name__ == "__main__":    
    Window.fullscreen = False
    Window.size = (412,869)
    import sys
    app = MyMainApp()
    sys.exit(app.run())

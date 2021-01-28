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


class Game():
    def __init__(self):
        with open('game_parameters.json','r') as f:
            dic_game_param = json.load(f)
            f.close()
        # init_self dict
        self.dict = {
            "players": {},
            "current_word":{
                "correct": "",
                "incorrect": ""
            },
            "game_config": {
                "team_composition_mode": "fix",
                "team_composition_qty": {
                    "normal": 0,
                    "undercover": 0,
                    "mrwhite": 0
                },
                "points_won_as": {
                    "normal": 1,
                    "undercover": 2,
                    "mrwhite": 5
                }
            },
            "used_words_id": [],
            "use_IA_for_words": False,
            "round": 1,
            "sub_round": 1
        }
        self.dict['game_config']['points_won_as'] = dic_game_param['points_won_as'].copy()
        
        # list_roles
        self.list_roles = ['normal','undercover','mrwhite']
        self.ROLE_NORMAL = 'normal'
        self.ROLE_UNDERCOVER = 'undercover'
        self.ROLE_MRWHITE = 'mrwhite'
        
    
    ################################ game_config ################################
    
    def config_set_default_team_composition(self):
        # set current game config team composition dict to default
        self.dict['game_config']['team_composition_mode'] = "fix"
        self.dict['game_config']['team_composition_qty'] = {
            "normal": 2,
            "undercover": 2,
            "mrwhite": 0
        }
    
    def config_set_default_point_won(self):
        # set current game config point won dict to default
        self.dict['game_config']['points_won_as'] = {
            "normal": 1,
            "undercover": 2,
            "mrwhite": 5            
        }
        
    def config_set_default(self):
        # set current game config dict to default
        self.config_set_default_team_composition()
        self.config_set_default_point_won()
        
    def config_set_fix_team_composition(self, nbs_normal, nbs_undercover, nbs_mrwhite):
        self.dict['game_config']['team_composition_mode'] = "fix"
        self.dict['game_config']['team_composition_qty'] = {
                    "normal": nbs_normal,
                    "undercover": nbs_undercover,
                    "mrwhite": nbs_mrwhite
        }
        
    def config_set_rdm_team_composition(self):
        nbs_player = self.players_get_nbs()
        nbs_normal = 0
        nbs_mrwhite = 0
        nbs_undercover = 0
        nbs_normal = int((p+1)/2)
        nbs_player = nbs_player - nbs_normal
        while nbs_player > 0:
            rdm = np.random.randint(2)
            if rdm == 0:
                nbs_undercover += 1
            else:
                nbs_mrwhite += 1
            nbs_player -= 1
        self.dict['game_config']['team_composition_qty'] = {
            "normal": nbs_normal,
            "undercover": nbs_undercover,
            "mrwhite": nbs_mrwhite
        }
        self.dict['game_config']['team_composition_mode'] = "rdm"
        
        
        
    ################################ roles ################################
    
    def roles_get_winnables_points(self, role):
        if role in self.list_roles:
            return self.dict['game_config']['points_won_as'][role]
        else:
            return None
        
    def roles_get_list(self):
        return np.concatenate((['normal']*self.dict['game_config']['team_composition_qty']['normal'],
                               ['undercover']*self.dict['game_config']['team_composition_qty']['undercover'],
                               ['mrwhite']*self.dict['game_config']['team_composition_qty']['mrwhite'])).tolist()
        
    def role_set_rdm(self):
        list_player = self.players_get_list()
        list_roles = self.roles_get_list()
        for i in range(len(list_player)):
            rdm_index_role = np.random.randint(len(list_roles))
            rmd_role  = list_roles[rdm_index_role]
            keepLooping = True
            if rmd_role != '':
                self.player_set_role(list_player[i], rmd_role)
                list_roles[rdm_index_role] = ''
                keepLooping = False
            while keepLooping:
                rdm_index_role = np.random.randint(len(list_roles))
                rmd_role  = list_roles[rdm_index_role]
                if rmd_role != '':
                    self.player_set_role(list_player[i], rmd_role)
                    list_roles[rdm_index_role] = ''
                    keepLooping = False
        
    
    
    ################################ players manip ################################
        
    def player_add(self, name):
        # add a new player to the players dict
        if name not in self.dict["players"].keys():
            self.dict["players"][name] = {
                "current_points": 0,
                "current_role": "",
                "still_playing": True
            }
    
    def player_del(self, name):
        # delete a player from the players dict
        if name in self.dict["players"].keys():
            del self.dict["players"][name]
    
    def player_reset(self, name):
        # reset the players dict
        self.dict["players"] = {}
        
    def player_get_role(self, name):
        if name in self.dict['players'].keys():
            return self.dict['players'][name]['current_role']
        else:
            return None
    
    def player_get_point(self, name):
        if name in self.dict['players'].keys():
            return self.dict['players'][name]['current_points']
        else:
            return None
    
    def player_add_point(self, name, qty):
        if name in self.dict['players'].keys():
            self.dict['players'][name]['current_points'] += qty        
        
        
    def player_set_role(self, name, role):
        if name in self.dict['players'].keys() and role in self.list_roles:
            self.dict['players'][name]['current_role'] = role
            
    def players_get_nbs(self):
        return len(self.dict['players'].keys())
    
    def players_get_list(self):
        return list(self.dict['players'].keys())
    
    def players_is_still_playing(self, name):
        return self.dict['players'][name]['still_playing']
    
    
        
    ################################ game rounds ################################
    
    def round_set_roles(self):
        mod_roles = self.dict['game_config']['team_composition_mode']
        if mod_roles == 'fix':
            self.role_set_rdm()
        else:
            self.config_set_rdm_team_composition()
            self.role_set_rdm()
        
        
    def round_update_points(self, winner_role):
        if winner_role in self.list_roles:
            for player in self.dict['players'].keys():
                player_role = self.player_get_role(player)
                if player_role != None and player_role == winner_role:
                    qty = self.roles_get_winnables_points(winner_role)
                    if qty != None:
                        self.player_add_point(player, qty)
        self.dict['round'] += 1
        self.dict['sub_round'] = 1
                        
    def round_generate_word(self):
        with open('game_words.json','r') as f:
            dict_word = json.load(f)
            f.close()
        list_word_key = [key for key in dict_word.keys()]
        wordNotFound = True
        while wordNotFound:
            rdm_index_word = np.random.randint(len(list_word_key))
            key = list_word_key[rdm_index_word]
            if key not in self.dict['used_words_id']:
                rdm_choice = np.random.randint(2)
                if rdm_choice == 0:
                    self.dict['current_word'] = {
                        "correct": dict_word[key][0],
                        "incorrect": dict_word[key][1]                    
                    }
                else:
                    self.dict['current_word'] = {
                        "correct": dict_word[key][1],
                        "incorrect": dict_word[key][0]                    
                    }
                self.dict['used_words_id'].append(key)
                wordNotFound = False
                
    def round_get_label_player(self, player):
        role = self.player_get_role(player)
        if role == 'normal':
            return self.dict['current_word']['correct']
        elif role == 'undercover':
            return self.dict['current_word']['incorrect']
        elif role == 'mrwhite':
            return "Vous êtes Mr.White !"
        else:
            return ''
        
    def round_eliminate_player(self, player):
        print('eliminated {} ({})'.format(player, self.player_get_role(player)))
        self.dict['players'][player]['still_playing'] = False
        # we go to next round
        self.dict['sub_round'] += 1
        
        
    def round_get_nbs_role(self, role):
        nbs_role = 0
        for player in self.dict['players'].keys():
            if self.player_get_role(player) == role and self.players_is_still_playing(player):
                nbs_role += 1
        return nbs_role
        
    def round_is_over(self, guess_mrwhite=''):
        # return 2 elmt: 1 bollean, true if rpund is over, false else. and a string which represent the name of the winning role
        nbs_normal = self.round_get_nbs_role('normal')
        nbs_undercover = self.round_get_nbs_role('undercover')
        nbs_mrwhite = self.round_get_nbs_role('mrwhite')
        if nbs_normal == 1  and nbs_undercover == 1 and nbs_mrwhite == 0:
            return True, 'undercover'
        elif nbs_normal == 0  and nbs_mrwhite == 0:
            return True, 'undercover'
        elif nbs_mrwhite == 0  and nbs_undercover == 0:
            return True, 'normal'
        elif nbs_mrwhite > 0  and guess_mrwhite != '':
            if word_is_correct_guess(guess_mrwhite): 
                return True, 'mrwhite'
            else:
                return False, None
        else:
            return False, None
        
        
        
    def round_reset(self):
        for player in self.dict["players"].keys():
            self.dict["players"][player]["still_playing"] = True
            self.dict["players"][player]["current_role"] = ""
        self.dict['sub_round'] = 1
        
        
    ################################ show ################################
    
    def word_is_correct_guess(guess_word):
        correct_word = self.dict['current_word']['correct']
        if ' ' not in guess_word: # the word only have one word inside
            if guess_word.lower() == correct_word.lower():
                return True
            list_correct_letters = np.array([guess_word[i] in correct_word for i in range(min(len(guess_word),len(correct_word)))])
            if list_correct_letters.sum() / len(list_correct_letters) > 0.85: #85% of letters of word guess are in word correct
                 return True
        else:
            list_words = guess_word.split(' ')
            nbs_word_correct = 0
            for word in list_words:
                if word in correct_word:
                    nbs_word_correct += 1
            if nbs_word_correct / len(list_words) > 0.5:
                return True
        return False
    
    
    ################################ show ################################
    
    def show_players(self):
        print('-------\nPlayers:')
        for player in self.dict['players'].keys():
            print('\n{}:\n  points: {}\n  role: {}'.format(player,self.dict['players'][player]['current_points'],self.dict['players'][player]['current_role']))
    
    def show_word(self):
        print('-------\nWord:')
        print('Correct: {}\nIncorrect: {}'.format(self.dict['current_word']['correct'],self.dict['current_word']['incorrect']))


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
        
        # add title label
        
        self.add_widget(Label(text="w/h {}x{}".format(self.width, self.height), 
                             pos_hint={"x":0.5,"top":0.95},
                             size_hint= (0.1, 0.05)))
        
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
    
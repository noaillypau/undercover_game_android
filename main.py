import json
import numpy as np
from functools import partial

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
            json.dump(dict_words,f,ensure_ascii=True)
            f.close()

    def get_list():
        with open('game_words.json','r') as f:
            dict_words = json.load(f)
            f.close()

        return [dict_words[key] for key in dict_words.keys()]


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
                "nbs_players": 0,
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
        self.dict['game_config']['nbs_players'] = 4
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
        self.dict['game_config']['nbs_players'] = nbs_normal + nbs_undercover + nbs_mrwhite
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
    
    def players_get_word(self, name):
        role = self.player_get_role(name)
        if role == 'normal':
            return self.dict['current_word']['correct']
        elif role == 'undercover':
            return self.dict['current_word']['incorrect']
        elif role == 'mrwhite':
            return ""
        else:
            return ''
    
    
        
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
        elif nbs_mrwhite == 1  and nbs_undercover == 0 and nbs_normal == 1:
            return True, 'mrwhite'
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

    ################################ show ################################
    
    def history_post_game(self):
        with open('game_history.json','r') as f:
            dict_history = json.load(f)
            f.close()
        dict_history[len(dict_history)] = self.dict.copy()
        with open('game_history.json','w') as f:
            json.dump(dict_history,f)
            f.close()











































import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
# screen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
# object
from kivy.uix.popup import Popup
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


class GameProfileWindow(Screen):
    def __init__(self,**kwargs):
        super(GameProfileWindow,self).__init__(**kwargs)
        # set name        
        self.name = "gameProfile"
        
    def on_enter(self):
        # import game
        #self.game = self.manager.get_screen("menu").game
        nbs_players = self.manager.get_screen("menu").game.dict['game_config']['nbs_players']
        # create main layout, boxlayout, and gridlayout
        self.float_layout = FloatLayout()
        self.box_layout = BoxLayout(pos_hint={'x':0.05, 'top':0.8}, 
                                    size_hint=(0.9, 0.3+0.1*nbs_players//2))
        self.grid_layout = GridLayout(cols=2)
        # create main content with text input names
        self.dict_input_text = {}
        self.dict_label_nbs = {}
        for i in range(nbs_players):
            self.dict_input_text[i] = TextInput(text="Nom")
            self.dict_label_nbs[i] = Label(text="Joueur {}".format(i+1))
            self.grid_layout.add_widget(self.dict_label_nbs[i])
            self.grid_layout.add_widget(self.dict_input_text[i])
        # add successive layers of layout
        self.box_layout.add_widget(self.grid_layout)
        self.float_layout.add_widget(self.box_layout)
        self.add_widget(self.float_layout)
        
        # add return to button menu
        button_menu = Button(text='Menu', 
                             pos_hint={"x":0.03,"y":0.85},
                             size_hint= (0.12, 0.05))
        button_menu.bind(on_press=self.onPressed_returnMenu)
        self.add_widget(button_menu)
        
        # add Submit button
        button_submit = Button(text='Submit', 
                             pos_hint={"x":0.85,"y":0.05},
                             size_hint= (0.12, 0.05))
        button_submit.bind(on_press=self.onPressed_submit)
        self.add_widget(button_submit)
        
        # add title label
        
        self.add_widget(Label(text="w/h {}x{}".format(self.width, self.height), 
                             pos_hint={"x":0.5,"top":0.95},
                             size_hint= (0.1, 0.05)))
    def on_leave(self):
        self.clear_widgets()
        
    def onPressed_returnMenu(self,instance):
        self.clear_widgets()
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
        
        
class GamePrepaWindow(Screen):    
    def __init__(self,**kwargs):
        super(GamePrepaWindow,self).__init__(**kwargs)
        # set name        
        self.name = "gamePrepa"
        self.nbs_player = 0
        self.nbs_mrwhite = 0
        self.nbs_undercover = 0

    def on_leave(self):
        self.clear_widgets()
        
    def on_enter(self):
        # create main layout
        self.float_layout = FloatLayout()
        self.add_widget(self.float_layout)

        # create nbs_player input
            # Label
        label_nbs_player = Label(text='Nbs Joueurs:', 
                             pos_hint={"x":0.15,"top":0.75},
                             size_hint= (0.1, 0.05))
        self.float_layout.add_widget(label_nbs_player)
            # button +
        button_add_player = Button(text='+', 
                             pos_hint={"x":0.5,"top":0.75},
                             size_hint= (0.05, 0.05))
        button_add_player.bind(on_press=self.onPressed_addPlayer)
        self.float_layout.add_widget(button_add_player)
            # button -
        button_remove_player = Button(text='-', 
                             pos_hint={"x":0.6,"top":0.75},
                             size_hint= (0.05, 0.05))
        button_remove_player.bind(on_press=self.onPressed_removePlayer)
        self.float_layout.add_widget(button_remove_player)

            # label current nbs player
        self.label_current_nbs_player = Label(text=str(self.nbs_player), 
                             pos_hint={"x":0.7,"top":0.75},
                             size_hint= (0.05, 0.05))
        self.float_layout.add_widget(self.label_current_nbs_player)

        # create nbs_undercover input
            # Label
        label_nbs_undercover = Label(text='Nbs Undercover:', 
                             pos_hint={"x":0.15,"top":0.65},
                             size_hint= (0.1, 0.05))
        self.float_layout.add_widget(label_nbs_undercover)
            # button +
        button_add_undercover = Button(text='+', 
                             pos_hint={"x":0.5,"top":0.65},
                             size_hint= (0.05, 0.05))
        button_add_undercover.bind(on_press=self.onPressed_addUndercover)
        self.float_layout.add_widget(button_add_undercover)
            # button -
        button_remove_undercover = Button(text='-', 
                             pos_hint={"x":0.6,"top":0.65},
                             size_hint= (0.05, 0.05))
        button_remove_undercover.bind(on_press=self.onPressed_removeUndercover)
        self.float_layout.add_widget(button_remove_undercover)

            # label current nbs player
        self.label_current_nbs_undercover = Label(text=str(self.nbs_undercover), 
                             pos_hint={"x":0.7,"top":0.65},
                             size_hint= (0.05, 0.05))
        self.float_layout.add_widget(self.label_current_nbs_undercover)

        # create nbs_mrwhite input
            # Label
        label_nbs_mrwhite = Label(text='Nbs Mr.White:', 
                             pos_hint={"x":0.15,"top":0.55},
                             size_hint= (0.1, 0.05))
        self.float_layout.add_widget(label_nbs_mrwhite)
            # button +
        button_add_mrwhite = Button(text='+', 
                             pos_hint={"x":0.5,"top":0.55},
                             size_hint= (0.05, 0.05))
        button_add_mrwhite.bind(on_press=self.onPressed_addMrwhite)
        self.float_layout.add_widget(button_add_mrwhite)
            # button -
        button_remove_mrwhite = Button(text='-', 
                             pos_hint={"x":0.6,"top":0.55},
                             size_hint= (0.05, 0.05))
        button_remove_mrwhite.bind(on_press=self.onPressed_removeMrwhite)
        self.float_layout.add_widget(button_remove_mrwhite)

            # label current nbs player
        self.label_current_nbs_mrwhite = Label(text=str(self.nbs_mrwhite), 
                             pos_hint={"x":0.7,"top":0.55},
                             size_hint= (0.05, 0.05))
        self.float_layout.add_widget(self.label_current_nbs_mrwhite)

        
        # add return to button menu
        button_menu = Button(text='Menu', 
                             pos_hint={"x":0.03,"y":0.85},
                             size_hint= (0.12, 0.05))
        button_menu.bind(on_press=self.onPressed_returnMenu)
        self.add_widget(button_menu)
        
        # add Submit button
        button_submit = Button(text='Submit', 
                             pos_hint={"x":0.85,"y":0.05},
                             size_hint= (0.12, 0.05))
        button_submit.bind(on_press=self.onPressed_submit)
        self.add_widget(button_submit)
        
        # add title label
        title_game_prepa = 'Préparation du jeu'
        self.add_widget(Label(text=title_game_prepa, 
                             pos_hint={"x":0.5,"top":0.95},
                             size_hint= (0.12, 0.05),
                             font_size= (self.width**2 + self.height**2) / 17**4))
        
    def onPressed_returnMenu(self,instance):
        self.manager.get_screen("gameProfile").grid_layout.clear_widgets()
        self.manager.get_screen("gameProfile").float_layout.clear_widgets()        
        self.float_layout.clear_widgets()
        sm.current = "menu"
        
    def onPressed_submit(self,instance):
        self.manager.get_screen("menu").game.config_set_default_point_won()
        self.manager.get_screen("menu").nbs_player = self.nbs_player
        nbs_normal = self.nbs_player - self.nbs_mrwhite - self.nbs_undercover
        if nbs_normal > 0 and nbs_normal >= self.nbs_mrwhite + self.nbs_undercover:
            self.manager.get_screen("menu").game.config_set_fix_team_composition(nbs_normal,self.nbs_undercover,self.nbs_mrwhite)
            # we go to next screen
            self.manager.transition.direction = "down"
            sm.current = "gameProfile"

    def onPressed_addPlayer(self, instance):
        self.nbs_player += 1
        self.label_current_nbs_player.text = str(self.nbs_player)

    def onPressed_removePlayer(self, instance):
        if self.nbs_player - 1 >= 0:
            self.nbs_player -= 1
            self.label_current_nbs_player.text = str(self.nbs_player)

    def onPressed_addUndercover(self, instance):
        self.nbs_undercover += 1
        self.label_current_nbs_undercover.text = str(self.nbs_undercover)

    def onPressed_removeUndercover(self, instance):
        if self.nbs_undercover - 1 >= 0:
            self.nbs_undercover -= 1
            self.label_current_nbs_undercover.text = str(self.nbs_undercover)

    def onPressed_addMrwhite(self, instance):
        self.nbs_mrwhite += 1
        self.label_current_nbs_mrwhite.text = str(self.nbs_mrwhite)

    def onPressed_removeMrwhite(self, instance):
        if self.nbs_mrwhite - 1 >= 0:
            self.nbs_mrwhite -= 1
            self.label_current_nbs_mrwhite.text = str(self.nbs_mrwhite)





class GameRoundWindow(Screen):
    def __init__(self,**kwargs):
        super(GameRoundWindow,self).__init__(**kwargs)
        # set name        
        self.name = "gameRound"
        
    def on_enter(self):
        self.round = self.manager.get_screen("menu").game.dict['round']
        self.sub_round = self.manager.get_screen("menu").game.dict['sub_round']
        # import game
        #self.game = self.manager.get_screen("menu").game
        dic_players = self.manager.get_screen("menu").game.dict['players']
        # create main layout, boxlayout, and gridlayout
        self.float_layout = FloatLayout()
        self.box_layout = BoxLayout(pos_hint={'x':0.05, 'top':0.8}, 
                                    size_hint=(0.9, 0.3+0.1*len(dic_players)//4))
        self.grid_layout = GridLayout(cols=4,
                                      pos_hint={'top':0.95},
                                      size_hint=(0.9, 0.7))
        
        # add successive layers of layout
        self.box_layout.add_widget(self.grid_layout)
        self.float_layout.add_widget(self.box_layout)
        self.add_widget(self.float_layout)
        
        # add return to button menu
        button_menu = Button(text='Menu', 
                             pos_hint={"x":0.03,"y":0.85},
                             size_hint= (0.12, 0.05))
        button_menu.bind(on_press=self.onPressed_returnMenu)
        self.add_widget(button_menu)

        # add return to button menu
        button_end = Button(text='End game', 
                             pos_hint={"x":0.85,"y":0.85},
                             size_hint= (0.12, 0.05))
        button_end.bind(on_press=self.onPressed_endGame)
        self.add_widget(button_end)

        # add reset round button
        button_resetRoundButton = Button(text='Reset Round', 
                             pos_hint={"x":0.05,"y":0.05},
                             size_hint= (0.12, 0.05))
        button_resetRoundButton.bind(on_press=self.onPressed_resetRoundButton)
        self.add_widget(button_resetRoundButton)
        

        # add Score button
        button_score = Button(text='Score', 
                             pos_hint={"x":0.2,"y":0.05},
                             size_hint= (0.12, 0.05))
        button_score.bind(on_press=self.onPressed_scoreButton)
        self.add_widget(button_score)

        # add text input
        self.textInput_eliminatePlayer = TextInput(text='', 
                             pos_hint={"x":0.40,"y":0.05},
                             size_hint= (0.3, 0.05))
        self.add_widget(self.textInput_eliminatePlayer)

        # add reset round button
        button_eliminatePlayerButton = Button(text='Eliminate player', 
                             pos_hint={"x":0.75,"y":0.05},
                             size_hint= (0.2, 0.05))
        button_eliminatePlayerButton.bind(on_press=self.onPressed_eliminatePlayerButton)
        self.add_widget(button_eliminatePlayerButton)
        
        # add title label
        self.title_label = Label(text="Round {} - {}".format(self.round, self.sub_round), 
                             pos_hint={"x":0.5,"top":0.95},
                             size_hint= (0.1, 0.05))
        self.add_widget(self.title_label)

        self.create_new_round()

    def on_leave(self):
        self.clear_widgets()


        
    def onPressed_returnMenu(self,instance):
        self.clear_widgets()
        sm.current = "menu"

    def onPressed_scoreButton(self,instance):
        summup_content = GridLayout(cols=2)
        summup_content.add_widget(Label(text='Joueur'))
        summup_content.add_widget(Label(text='Score'))
        for player in self.manager.get_screen("menu").game.players_get_list():
            summup_content.add_widget(Label(text='{}'.format(player)))
            summup_content.add_widget(Label(text='{}'.format(self.manager.get_screen("menu").game.player_get_point(player))))


        Popup(title='Score',
              content = summup_content,
              size_hint=(.6, .6)).open()

    def onPressed_resetRoundButton(self,instance):
        self.create_new_round()

    def onPressed_eliminatePlayerButton(self,instance):
        # extract eliminate player
        self.player_to_eliminate = self.textInput_eliminatePlayer.text
        # check if we are allowed to eliminate him
        if self.player_to_eliminate in self.manager.get_screen("menu").game.players_get_list() and self.manager.get_screen("menu").game.players_is_still_playing(self.player_to_eliminate):
            # eliminate player
            self.manager.get_screen("menu").game.round_eliminate_player(self.player_to_eliminate)
            self.guess_mrwhite = ''
            if self.manager.get_screen("menu").game.player_get_role(self.player_to_eliminate) == 'mrwhite':
                print('asking for mrwhite guess')
                self.ask_for_mr_white_guess()
            else:
                isOver, winning_role = self.manager.get_screen("menu").game.round_is_over(self.guess_mrwhite)
                if isOver:
                    # if round is over we end the round by attributing points and we generate a new round
                    self.round_is_over(winning_role)
                    self.next_round()
                else:
                    # if game is not over then we delete the popup of the eliminated player and we go to next sub round
                    self.next_sub_round()
                    Popup(title='Joueur éliminé',
                          content = Label(text='{} était {}'.format(self.player_to_eliminate, self.manager.get_screen("menu").game.player_get_role(self.player_to_eliminate))),
                          size_hint=(.6, .6)).open()
                    self.grid_layout.remove_widget(self.dic_button_popup[self.player_to_eliminate])

    def next_round(self):
        self.round += 1
        self.sub_round = 1
        self.title_label.text = "Round {}-{}".format(self.round, self.sub_round)

    def next_sub_round(self):
        self.sub_round += 1
        self.title_label.text = "Round {}-{}".format(self.round, self.sub_round)


    def create_new_round(self):
        # initialize a new round, set a role to each player, generate word and distribute it, create popup for each player, and set round/sub_round to n+1/1
        self.manager.get_screen("menu").game.round_reset()
        self.manager.get_screen("menu").game.round_set_roles()
        self.manager.get_screen("menu").game.round_generate_word()
        self.manager.get_screen("menu").game.show_players()
        # clear all popups
        self.grid_layout.clear_widgets()
        # create the button and the popups
        dic_players = self.manager.get_screen("menu").game.dict['players']
        self.dic_button_popup = {}
        self.dic_popup = {}
        for key in dic_players.keys():
            if self.manager.get_screen("menu").game.players_is_still_playing(key):                
                self.dic_popup[key] = Popup(title=key,
                                            content=Label(text=self.manager.get_screen("menu").game.round_get_label_player(key)),
                                            size_hint=(.6, .6))
                self.dic_button_popup[key] = Button(text=key)
                self.dic_button_popup[key].bind(on_press=partial(self.onPressed_buttonPopup, key))
                #self.dic_button_popup[key].bind(on_release=lambda instance: self.onPressed_buttonPopup(instance, key))
                self.grid_layout.add_widget(self.dic_button_popup[key])

    def onPressed_buttonPopup(self, *args):
        # this open the popup associated to the player_name
        self.dic_popup[str(args[0])].open()


    def round_is_over(self, winning_role):
        # show a popup to show winning team, point granted, and correct/incorrect words
        # then apply new points
        # then init a new round
        self.manager.get_screen("menu").game.round_update_points(winning_role)
        self.manager.get_screen("menu").game.show_players()


        summup_content = GridLayout(cols=4)
        summup_content.add_widget(Label(text='Joueur'))
        summup_content.add_widget(Label(text='Rôle'))
        summup_content.add_widget(Label(text='Mot'))
        summup_content.add_widget(Label(text='Score'))
        for player in self.manager.get_screen("menu").game.players_get_list():
            role_player = self.manager.get_screen("menu").game.player_get_role(player)
            summup_content.add_widget(Label(text='{}'.format(player)))
            summup_content.add_widget(Label(text='{}'.format(role_player)))
            summup_content.add_widget(Label(text='{}'.format(self.manager.get_screen("menu").game.players_get_word(player))))
            if role_player == winning_role:
                summup_content.add_widget(Label(text='{} (+{})'.format(self.manager.get_screen("menu").game.player_get_point(player),
                                                                       self.manager.get_screen("menu").game.roles_get_winnables_points(winning_role))))
            else:
                summup_content.add_widget(Label(text='{}'.format(self.manager.get_screen("menu").game.player_get_point(player))))


        Popup(title='{} remporte la partie'.format(winning_role),
              content = summup_content,
              size_hint=(.6, .6)).open()
        # create a new round
        self.create_new_round()
        
    def ask_for_mr_white_guess(self):
        self.text_input_guess_mrwhite = TextInput(text='',
                                                 pos_hint={"x":0.40,"y":0.12},
                                                 size_hint= (0.3, 0.05))
        self.add_widget(self.text_input_guess_mrwhite)
        self.button_ask_mrwhite = Button(text='Check guess', 
                                         pos_hint={"x":0.75,"y":0.12},
                                         size_hint= (0.2, 0.05))
        self.button_ask_mrwhite.bind(on_release=self.set_guess_mrwhite)
        self.add_widget(self.button_ask_mrwhite)

    def set_guess_mrwhite(self, instance):
        print('clossing popup ask mrwhite')
        self.guess_mrwhite = self.text_input_guess_mrwhite.text
        self.remove_widget(self.button_ask_mrwhite)
        self.remove_widget(self.text_input_guess_mrwhite)

        isOver, winning_role = self.manager.get_screen("menu").game.round_is_over(self.guess_mrwhite)
        if isOver:
            # if round is over we end the round by attributing points and we generate a new round
            self.round_is_over(winning_role)
            self.next_round()
        else:
            # if game is not over then we delete the popup of the eliminated player and we go to next sub round
            self.next_sub_round()
            Popup(title='Joueur éliminé',
                  content = Label(text='{} était {}'.format(self.player_to_eliminate, self.manager.get_screen("menu").game.player_get_role(self.player_to_eliminate))),
                  size_hint=(.6, .6)).open()
            self.grid_layout.remove_widget(self.dic_button_popup[self.player_to_eliminate])

    def onPressed_endGame(self, instance):
        # button to end game: show a popup that sumup score, and add game to history
        # layout
        content_float_layout = FloatLayout()
        BoxLayout_summup = BoxLayout(pos_hint={'x':0.05, 'top':1}, 
                                    size_hint=(0.9, 0.9))
        BoxLayout_button = BoxLayout(pos_hint={'x':0.05, 'top':0.1}, 
                                    size_hint=(0.9, 0.1))
        # summup grid content
        summup_content = GridLayout(cols=2)
        summup_content.add_widget(Label(text='Joueur'))
        summup_content.add_widget(Label(text='Score'))
        for player in self.manager.get_screen("menu").game.players_get_list():
            summup_content.add_widget(Label(text='{}'.format(player)))
            summup_content.add_widget(Label(text='{}'.format(self.manager.get_screen("menu").game.player_get_point(player))))
        BoxLayout_summup.add_widget(summup_content)
        # button close
        button_close_score_end = Button(text='Close Score',
                                        pos_hint={'x':0.5, 'top':0.5},
                                        size_hint=(0.2, 0.2))
        button_close_score_end.bind(on_press=self.close_score_end_game_popup)
        BoxLayout_button.add_widget(button_close_score_end)
        # compile layout
        content_float_layout.add_widget(BoxLayout_summup)
        content_float_layout.add_widget(BoxLayout_button)
        # create popup and associate layouts
        self.popup_end_game = Popup(title='Score',
                                    content = content_float_layout,
                                    size_hint=(.6, .6))

        self.popup_end_game.open()

    def close_score_end_game_popup(self, instance):
        # close popup
        self.popup_end_game.dismiss()
        # add game to history
        self.manager.get_screen("menu").game.history_post_game()
        # return to menu
        sm.current = "menu"






    


# other

class WordWindow(Screen):
    def __init__(self,**kwargs):
        super(WordWindow,self).__init__(**kwargs)
        # set name        
        self.name = "word"

    def on_leave(self):
        self.clear_widgets()
        
    def on_enter(self):
        # add return to button menu
        button_menu = Button(text='Menu', 
                             pos_hint={"x":0.03,"y":0.9},
                             size_hint= (0.12, 0.05))
        button_menu.bind(on_press=self.onPressed_returnMenu)
        self.add_widget(button_menu)


        # add return to button menu
        button_addWord = Button(text='Add Word', 
                             pos_hint={"x":0.82,"y":0.9},
                             size_hint= (0.12, 0.05))
        button_addWord.bind(on_press=self.onPressed_addWord)
        self.add_widget(button_addWord)

        # add input text
        self.input_text_1 = TextInput(text = '',
                                     pos_hint={"x":0.38,"y":0.9},
                                     size_hint= (0.20, 0.05))    
        self.add_widget(self.input_text_1)    
        self.input_text_2 = TextInput(text = '',
                                     pos_hint={"x":0.60,"y":0.9},
                                     size_hint= (0.20, 0.05))        
        self.add_widget(self.input_text_2)

        self.scrollView = ScrollView(size_hint=(1, 0.87), pos_hint={"top":0.87})
        self.refresh_words()

    def refresh_words(self):
        self.scrollView.clear_widgets()
        list_words = Word.get_list()


        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(len(list_words)):
            label = Label(text=str("{} / {}".format(list_words[i][0],list_words[i][1])), size_hint_y=None, height=120)
            layout.add_widget(label)
        self.scrollView = ScrollView(size_hint=(1, 0.87), pos_hint={"top":0.87})
        self.scrollView.add_widget(layout)
        self.add_widget(self.scrollView)

    def onPressed_returnMenu(self, instance):
        self.clear_widgets()
        sm.current = "menu"

    def onPressed_addWord(self, instance):
        Word.add_word(self.input_text_1.text,self.input_text_2.text)
        self.input_text_1.text = ''
        self.input_text_2.text = ''
        self.refresh_words()

class HistoryWindow(Screen):
    def __init__(self,**kwargs):
        super(HistoryWindow,self).__init__(**kwargs)
        # set name        
        self.name = "history"

    def on_leave(self):
        self.clear_widgets()
        
    def on_enter(self):
        # add return to button menu
        button_menu = Button(text='Menu', 
                             pos_hint={"x":0.03,"y":0.9},
                             size_hint= (0.12, 0.05))
        button_menu.bind(on_press=self.onPressed_returnMenu)
        self.add_widget(button_menu)


        
        
        self.add_widget(Label(text="Historique des parties", 
                             pos_hint={"x":0.5,"top":0.95},
                             size_hint= (0.2, 0.05),                             
                             font_size= (self.width**2 + self.height**2) / 17**4))

        self.scrollView = ScrollView(size_hint=(1, 0.87), pos_hint={"top":0.87})
        self.show_history()

    def show_history(self):
        self.scrollView.clear_widgets()
        
        with open('game_history.json', 'r') as f:
            dic_history = json.load(f)
            f.close()


        layout = GridLayout(cols=1, spacing=40, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(len(dic_history)):
            layout_to_add = self.get_layout_history(str(i), dic_history)
            layout.add_widget(layout_to_add)
        self.scrollView = ScrollView(size_hint=(1, 0.87), pos_hint={"top":0.87})
        self.scrollView.add_widget(layout)
        self.add_widget(self.scrollView)

    def get_layout_history(self, id_history, dic_history):
        layout_to_add = GridLayout(cols=5, spacing=1, size_hint_y=None)
        layout_to_add.add_widget(Label(text='ID: {}'.format(id_history)))
        layout_to_add.add_widget(Label(text='Rounds: {}'.format(dic_history[str(id_history)]["round"])))
        layout_to_add.add_widget(Label(text='Players: {}'.format(len(dic_history[str(id_history)]['players']))))
        layout_to_add.add_widget(Label(text=''))
        layout_to_add.add_widget(Label(text=''))
        for player in dic_history[str(id_history)]['players'].keys():
            layout_to_add.add_widget(Label(text='{}: {}'.format(player,dic_history[str(id_history)]['players'][player]["current_points"])))

        

        return layout_to_add



    def onPressed_returnMenu(self, instance):
        self.clear_widgets()
        sm.current = "menu"
        
class StatsWindow(Screen):
    def onPushed_ReturnMenu(self, instance):
        self.clear_widgets()
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
    Window.size = (1080,2042)
    import sys
    app = MyMainApp()
    sys.exit(app.run())
    
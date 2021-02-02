# undercover_game_android

This is a small and simplistic project that consist on my onw version of the undercover game. \
It is codded in python using kivy and can be deploy on android. \

# deploy

- [ ] install virtualbox and an ubuntu image
  - [ ] go to https://www.virtualbox.org/ for the virtual box
  - [ ] go to https://ubuntu.com/download/desktop for the ubuntu image
- [ ] Open the linux vm
  - [ ] on virtualbox, new > name > next > next > create> next > next > create
  - [ ] double click newly created instance, create disk by openning explorer and selecting the ubuntu image (.iso file) > start > capture
  - [ ]  install ubuntu > then go trhough all the ubuntu settings
- [ ] Setup phone
  - [ ] activate dev mode by clicking 7 times on build version
  - [ ] activate usb debuging
- [ ] Start ubuntu and setup usb
  - [ ] restart ubuntu
  - [ ] on bottom right of vm, if there is a button "no usd device attached", right click > usb setting > usb > device > select your android > ok > return to the righ click > select your android
- [ ] install requierments on vm
  - [ ] open terminal
  - [ ] install git `sudo apt install git`
  - [ ] clone buildozer `git clone https://github.com/kivy/buildozer.git`
  - [ ] install python 3 `sudo apt-get install python3.8`
  - [ ] install setup tools `sudo apt-get install python3-setuptools`
  - [ ] install buildozer `cd buildozer` > `sudo python3 setup.py install` > `cd ..`
  - [ ] clone this repo with the main.py file `git clone https://github.com/noaillypau/undercover_game_android`
- [ ] deploy app
  - [ ] go to the cloned rdirectory `cd undercover_game_android`
  - [ ] init buildozer `buildozer init`
  - [ ] edit the buildozer.spec file, add files needed (ex:json), edit name of app, add python packages req, and uncomment the debugging (line 219)
  - [ ] `sudo apt update`
  - [ ] `sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev`
  - [ ] `pip3 install --user --upgrade cython virtualenv`
  - [ ] `sudo apt-get install cython`
  - [ ] `buildozer android debug deploy run`
  
  
  
# update

```ssh
cd ..
rm -rf undercover_game_android
git clone https://github.com/noaillypau/undercover_game_android
cd undercover_game_android
buildozer init
```

```ssh
buildozer android debug deploy run
```

# Todo List

- [ ] Improve ui design
- [x] add way to not use a word that has been used already in a game
- [x] add way to visualize reccorded words, and a possibility to add new ones
- [x] add way to view history of games
- [ ] Add statistics scrren + calculus
- [x] Implement random role
- [ ] Add random role button on prepaGame screen
- [ ] Add IA player (using gensim api for similar words)
- [ ] Add transalation (eng - fr)
- [ ] Add setting button on main menu screen with options to change language, IA word (couple generated with gensim), and defaults point won per role
- [ ] fix issues when for app deploy when code in splitted in different files
- [ ] Add game icone
- [x] Fix bug that sometimes makes the app close when word menu is openned
  - [x] the probelm was due to game_word.json that had some non utf-8 encoded words. Remade the the json file and added `ensure_ascii=True` in `Word.add_word(word1,word2)`
 
  
 # Debuging
 
 - [x] pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available
   - [x] fix: `sudo apt install libssl-dev` > `buildozer android clean` > delete .buildozer file > `buildozer Android debug` > `buildozer Android debug deploy run`
 
 - [x] lld not installed
   - [x] fix: probably a package problabe, check if you put any package you used to buildozer.spec (warning json and functools packages must not be added in the spec file)






# References

* deploy tutorial with buildozer
https://www.youtube.com/watch?v=EupAeyL8zAo

* official kivy doc
https://kivy.org/doc/stable/

* official kivy api reference
https://kivy.org/doc/stable/api-index.html 

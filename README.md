# undercover_game_android

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
  - [ ] `Sudo apt-get install cython`
  - [ ] `buildozer android debug deploy run`
  
  
  
# update

```ssh
test

```
 
  
 # Debuging
 
 - [ ] pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available
 - [ ] fix: `apt install libssl-dev` > `buildozer android clean`






# References

* deploy tutorial with buildozer
https://www.youtube.com/watch?v=EupAeyL8zAo

* official kivy doc
https://kivy.org/doc/stable/

* official kivy api reference
https://kivy.org/doc/stable/api-index.html

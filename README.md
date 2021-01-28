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
  - [ ] import buildozer `git clone https://github.com/kivy/buildozer.git`
  - [ ] install python 3 `sudo apt-get install python3.8`
  - [ ] install setup tools `sudo apt-get install python3-setuptools`
  
 






# References

* deploy tutorial with buildozer
https://www.youtube.com/watch?v=EupAeyL8zAo

* official kivy doc
https://kivy.org/doc/stable/

* official kivy api reference
https://kivy.org/doc/stable/api-index.html

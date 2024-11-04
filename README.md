
# <p align="center">ArchMonitor</p>

ArchMonitor est un module de gestion autonome de refroidissement liquide haut de gamme. 
Cette premiere version beta fonctionne sur un `Raspberry PI 4B` et prend en charge la configuration suivante :

- Deux pompes
- Deux sondes pour la température de liquide
- Une sonde pour le boitier
- Trois circuits indépendant de cinq ventilateurs
- Un circuit global `ARGB2`
- Un écran tactile de contrôle

Les configurations possibles sous cette version sont de :

- Deux modes de refroidissement configurable
- Trois modes configurable pour le circuit `ARGB2`

Le logiciel ArchMonitor est basé sur la surcouche `ArchGUI` lui-même basé sur `FreeSimpleGUI` et sur `ws2812.py`. 
Ce programme fonctionne sur un `Raspberry PI 4B` avec le dernier `Raspberry Pi OS 64Bits` comme OS.


## 🛠️ Lien externe :

- [`Raspberry Pi OS`](https://www.raspberrypi.com/software/)
- [`ws2812-spi`](https://github.com/joosteto/ws2812-spi)


## 🛠️ Le matériel manufacturé :


| Pièces                  | Aperçu                                         | Achat                                           |
|-------------------------|------------------------------------------------|-------------------------------------------------|
| 1x Raspberry PI 4B      | [`Image`](https://www.amazon.fr/dp/B09TTNF8BT) | [`Amazon`](https://www.amazon.fr/dp/B09TTNF8BT) |
| 1x Dissipateur          | [`Image`](https://www.amazon.fr/dp/B09TTNF8BT) | [`Amazon`](https://www.amazon.fr/dp/B08N617L1J) |
| 1x Ventilateur 120mm    | [`Image`](https://www.amazon.fr/dp/B09TTNF8BT) | [`Amazon`](https://www.amazon.fr/dp/B09RWTCXRR) |
| 1x Contrôleur PCA9685   | [`Image`](https://www.amazon.fr/dp/B09TTNF8BT) | [`Amazon`](https://www.amazon.fr/dp/B072N8G7Y9) |
| 3x Sonde DS18B20        | [`Image`](https://www.amazon.fr/dp/B09TTNF8BT) | [`Amazon`](https://www.amazon.fr/dp/B075FYYLLV) |
| 3x HUBS FAN 4 PINS      | [`Image`](https://www.amazon.fr/dp/B09TTNF8BT) | [`Amazon`](https://www.amazon.fr/dp/B08XWWXBYD) |
| 2x Cables FAN 4 PINS    | [`Image`](https://www.amazon.fr/dp/B09TTNF8BT) | [`Amazon`](https://www.amazon.fr/dp/B01N1Z3FYD) |
| 1x HUB ARGB2 + Cable    | [`Image`](https://www.amazon.fr/dp/B09TTNF8BT) | [`Amazon`](https://www.amazon.fr/dp/B0D2SMNKZY) |
| 1x Écran 800x480        | [`Image`](https://www.amazon.fr/dp/B09TTNF8BT) | [`Amazon`](https://www.amazon.fr/dp/B096ZSZFC8) |
| 1x Cable Micro HDMI     | [`Image`](https://www.amazon.fr/dp/B09TTNF8BT) | [`Amazon`](https://www.amazon.fr/dp/B096ZSZFC8) |
| 3x Cable USB            | [`Image`](https://www.amazon.fr/dp/B09TTNF8BT) | [`Amazon`](https://www.amazon.fr/dp/B096ZSZFC8) |
| 1x Cable extension SATA | [`Image`](https://www.amazon.fr/dp/B09TTNF8BT) | [`Amazon`](https://www.amazon.fr/dp/B07C71J8LL) |


## 🛠️ Impression 3D :

| Pièces                  | Fichiers                                                                                         |
|-------------------------|--------------------------------------------------------------------------------------------------|
| 1x Boitier              | [`Plan PDF`](https://www.amazon.fr/dp/B09TTNF8BT) - [`STL`](https://www.amazon.fr/dp/B09TTNF8BT) |
| 1x Couvercle            | [`Plan PDF`](https://www.amazon.fr/dp/B09TTNF8BT) - [`STL`](https://www.amazon.fr/dp/B09TTNF8BT) |
| 1x Fixation_Cable_2P_4D | [`Plan PDF`](https://www.amazon.fr/dp/B09TTNF8BT) - [`STL`](https://www.amazon.fr/dp/B09TTNF8BT) |
| 3x Fixation_Cable_2P_5D | [`Plan PDF`](https://www.amazon.fr/dp/B09TTNF8BT) - [`STL`](https://www.amazon.fr/dp/B09TTNF8BT) |
| 1x Panneau_Ports_RPI_4B | [`Plan PDF`](https://www.amazon.fr/dp/B09TTNF8BT) - [`STL`](https://www.amazon.fr/dp/B09TTNF8BT) |

Plan de montage général : [`Plan PDF`](https://www.amazon.fr/dp/B09TTNF8BT)


## 🛠️ Schémas de câblage :

| Circuit | Fichiers                                          |
|---------|---------------------------------------------------|
| Général | [`Plan PDF`](https://www.amazon.fr/dp/B09TTNF8BT) |
| RPI     | [`Plan PDF`](https://www.amazon.fr/dp/B09TTNF8BT) |
| Sensors | [`Plan PDF`](https://www.amazon.fr/dp/B09TTNF8BT) |


## 🧑🏻‍💻️ Installation de Raspbian 64 :
 - Configuration l'installation via `Raspberry PI Imager` via Ubuntu au une autre distribution
 - Installation de `Raspberry Pi OS 64Bits` sur la carte SD
 - Démarrage du PI

Pour plus de simplicité j’utilise l’user `archmonitor`, vous le retrouver dans les commandes à venir.


## 🧑🏻‍💻 Mise à jour :
```bash
sudo apt-get update && sudo apt-get upgrade
sudo rpi-update
sudo reboot
```


## 🧑🏻‍💻 Activation des ports :
```bash
sudo raspi-config
```

Puis activer dans `Interface Options` les options suivantes :
- SPI    : Enabled
- 1-Wire : Enabled

```bash
sudo modprobe w1-gpio
sudo modprobe w1-therm
```


## 🧑🏻‍💻 Modification des fichiers boot :

### 📄 `/boot/firmware/cmdline.txt` ➡️ [`cmdline.txt`](https://www.amazon.fr/dp/B09TTNF8BT)<br>
```bash
sudo nano /boot/firmware/cmdline.txt
```
Ajouter à la fin de la ligne :
```bash
consoleblank=0 spidev.bufsiz=250000
```


### 📄 `/boot/firmware/config.txt` ➡️ [`config.txt`](https://www.amazon.fr/dp/B09TTNF8BT)<br>
```bash
sudo nano /boot/firmware/config.txt
```
En dessous de `# Uncomment some or all of these to enable the optional hardware interfaces`<br>
Modifier le fichier pour obtenir :
```bash
# Uncomment some or all of these to enable the optional hardware interfaces
dtparam=spi=on
dtparam=i2c_arm=on
```
À la fin du fichier après `[all]`<br>
Modifier le fichier pour obtenir :
```bash
[all]
dtoverlay=w1-gpio,gpiopin=4,disable-bt
display_auto_detect=1

force_turbo=1
core_freq=500 
core_freq_min=500

hdmi_cvt=800 480 60 3 0 0 0
hdmi_group=1
hdmi_mode=14
hdmi_boost=7

framebufferheight=480
framebufferwidth=800
```


### Redémarrer le PI : <br>
```bash
sudo reboot
```


## 🧑🏻‍💻 Test de détection des sondes :
```bash
cd /sys/bus/w1/devices/
ls
```

 ```
28-xxxxxxxxxxxx  28-xxxxxxxxxxxx  28-xxxxxxxxxxxx  w1_bus_master1
```

Vous devez voir trois devices commençant par `28-xxxxxxxxxxxx`.<br/>
Rentrez dans une de ces devices afficher les données de la sonde :

```bash
cd 28-xxxxxxxxxxxx
cat w1_slave
```

```bash
52 01 55 00 7f ff 0c 10 53 : crc=53 YES
52 01 55 00 7f ff 0c 10 53 t=21125
```

La deuxième ligne vous indiquera la température de la sonde en millième de degré : `t=21125`<br/>
La sonde indique 21 degrés : `21125 / 100 = 21`

## 🧑🏻‍💻 Installation des librairies Python :
```bash
sudo apt-get install pigpio python3-pigpio
sudo systemctl enable pigpiod
sudo systemctl start pigpiod 

sudo pip3 install --break-system-packages FreeSimpleGUI pynput screeninfo gpiozero
sudo pip3 install --break-system-packages adafruit-circuitpython-pca9685

sudo reboot
```


## 🧑🏻‍💻 Téléchargement :
📂 Dans le `home` de votre `user`, ici `/home/archmonitor/` :
```bash
wget https://github.com/archprojectdev/archgui/archive/refs/heads/main.zip
unzip main.zip

mv archmonitor-main archmonitor
cd archmonitor

wget https://github.com/archprojectdev/archgui/archive/refs/heads/main.zip
unzip main.zip

mv archgui-main archgui
```


## 🧑🏻‍💻 Configuration :
📂 Dans le `home` de votre `user`, ici `/home/archmonitor/` :
```bash
cd archmonitor
python sensors.py
```
```bash
----------------------------------------------
/sys/bus/w1/devices/28-7f79541f64ff/w1_slave - 21
/sys/bus/w1/devices/28-837e541f64ff/w1_slave - 25
/sys/bus/w1/devices/28-d97b541f64ff/w1_slave - 21
```
Avec une source de chaleur, 
faites varier la température de chaque sonde pour déterminer quelle sonde correspond à quel ID.<br/>
Une fois déterminé, modifier le fichier `/home/archmonitor/archmonitor/config.json` en conséquence :
```bash
"sensors": {
  "wc_cpu": "/sys/bus/w1/devices/28-7f79541f64ff/w1_slave",
  "wc_gpu": "/sys/bus/w1/devices/28-837e541f64ff/w1_slave",
  "case": "/sys/bus/w1/devices/28-d97b541f64ff/w1_slave"
}
```




## 🧑🏻‍💻 Création des fichiers Xorg :
### 📄 `/etc/X11/xorg.conf.d/10-blanking.conf` ➡️ [`10-blanking.conf`](https://www.amazon.fr/dp/B09TTNF8BT)<br>


```bash
sudo nano /etc/X11/xorg.conf.d/10-blanking.conf
```
```bash
Section "Extensions"
    Option      "DPMS" "Disable"
EndSection

Section "ServerLayout"
    Identifier "ServerLayout0"
    Option "StandbyTime" "0"
    Option "SuspendTime" "0"
    Option "OffTime"     "0"
    Option "BlankTime"   "0"
EndSection
```


### 📄 `/etc/X11/xorg.conf.d/10-monitor.conf` ➡️ [`10-monitor.conf`](https://www.amazon.fr/dp/B09TTNF8BT)<br>
```bash
sudo nano /etc/X11/xorg.conf.d/10-monitor.conf
```
```bash
Section "Monitor"
    Identifier "XWAYLAND0"
    Modeline "800x480_60.00"   29.50  800 824 896 992  480 483 493 500 -hsync +vsync
    Option "PreferredMode" "800x480_60.00"
EndSection

Section "Screen"
    Identifier "HDMI-A-1"
    Monitor "XWAYLAND0"
    DefaultDepth 24
    SubSection "Display"
        Modes "800x480_60.00"
    EndSubSection
EndSection
```


## 🧑🏻‍💻 Création des fichiers de lancement :
### 📄 Créer le fichier : `/home/archmonitor/.bashrc`
```bash
nano .bashrc
>> bash startx.sh
```
### 📄 Créer le fichier : `/home/archmonitor/startx.sh`
```bash
nano startx.sh
>> startx
```
### 📄 Créer le fichier : `/home/archmonitor/.xinitrc`
```bash
nano .xinitrc
>> exec python /home/archmonitor/archmonitor/main.py
```

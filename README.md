
# **WarMAC Beta Version 1.5.6**

**WarMAC** is a command-line Python script that can calculate the average market price of items in Warframe.  
WarMAC compiles seller listings from the fan website *<https://warframe.market/>*, and has the option to target specific platforms, pull data from specific time frames, and find the mean, median, mode, or harmonic mean averages.  

***

## **⚙️To Setup**

### *You will need:*

* Python 3.10.x or 3.11.x
* urllib3 package  

If you already have Python 3.10.x or 3.11.x installed, `git clone` the repo into a directory or download it as a zip. If you're on Windows, run:

```cmd
python .\wfmarket-calc.py
```

If you're on MacOS or Linux, run:

```bash
./wfmarket-calc/warmac.py
```

**WarMAC currently requires end-users to install the dependency library themselves, as this project is not on PyPi.**
If you do not have Python 3.10.x or 3.11.x already on your system, please download it from the following link:  
Python download link: <https://www.python.org/downloads/>.

### 🪟On Windows

After downloading and installing the appropriate Python interpreter for your system, open up `cmd`, `PowerShell`, or `Windows Terminal`, and run the following command:

```PowerShell
python -m pip install urllib3
```

### 🍎On MacOS and 🐧Linux

After downloading and installing the appropriate Python interpreter for your system, open up `Terminal` and run the following command:

```bash
python3 -m pip install urllib3
```

## **⏬Downloading This Program**

### 🎒Downloading as a .zip file

Download this repository as a `.zip` file, and unzip it into a directory of your choosing.

### 🤖Using Git clone

Clone this repository into a directory of your choosing by typing into the command line:

```bash
git clone <this repository URL>.git <your directory>
```

***

## **💽Reporting Issues**

*To report an issue, please open an Issue report on GitHub or GitLab respectively.*  

## **🔮Upcoming/The Future of WarMAC**

This project is currently not available on PyPi. However, I am diligently working on adding functionality before the first official release.  
Upcoming features:  
> Mod rank and Arcane rank handling, show average from buy orders instead of sell orders, add drop sources tag, and deleting lowest/highest sell prices to keep average in line are coming soon. Possibly adding more average types.  

## **⚖️Licensing and Disclaimers**

***This project is NOT affiliated with Warframe, Digital Extremes, or the Warframe Market.***  
*Copyright (c) 2023 Noah Jenner under MIT License*  
*For additional licensing information, please see LICENSE.txt*

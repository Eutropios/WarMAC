
<h1 style="text-align: center;"><b>WarMAC Beta Version 1.5.5</b></h1>

**WarMAC** is a command-line Python script that can calculate the average market price of items in Warframe.  
WarMAC compiles seller listings from the fan website *<https://warframe.market/>*, and has the option to target specific platforms, pull data from specific time frames, and find the mean, median, mode, or harmonic mean averages.  

<hr>
<h2><b>⚙️To Setup</b></h2>

<h3><u><i>You will need:</i></u></h3>

* Python 3.10+ (Python 3.11 recommended)
* urllib3 package  

If you already have Python 3.10.x or 3.11.x installed, `git clone` the repo into a directory or download it as a zip. If you're on Windows, run:

```cmd
python .\wfmarket-calc.py
```

If you're on MacOS or Linux, run:

```bash
./wfmarket-calc/warmac.py
```

<h2><b>🐍Installing Python and urllib3</b></h2>

Please download Python 3.10 or 3.11 for your appropriate CPU and OS.  
Python download link: <https://www.python.org/downloads/>.

<h3>🪟On Windows</h3>

1. After downloading Python, run the installer, making sure `Add to PATH` is selected on the first page.
2. After installing, open up `cmd`, `PowerShell`, or `Windows Terminal`, and type the following line into the text box:

```PowerShell
python -m pip install urllib3
```

<h3>🍎On MacOS and 🐧Linux</h3>

1. After downloading, unpackage the file and run the installer.
2. After installing, open up `Terminal` and run the following command:

```bash
python3 -m pip install urllib3
```

<h2><b>⏬Downloading This Program</b></h2>

<h3>🎒<u>Downloading as a `.zip` file</u></h3>

Donwload this repository as a `.zip` file, and unzip it into a directory of your choosing.

<h3>🤖<u>Using Git clone</u></h3>

Clone this repository into a directory of your choosing by typing into the command line:

```bash
git clone <this repository URL>.git <your directory>
```

<hr>

<h2><b>💽Reporting Issues</b></h2>

*To report an issue, please open an Issue report on GitHub or GitLab respectively.*  

<h2><b>🔮Upcoming/The Future of WarMAC</b></h2>

This project is currently not available on PyPi. However, I am diligently working on adding functionality before the first official release.  
Upcoming features:  
> Mod rank and Arcane rank handling, show average from buy orders instead of sell orders, add drop sources tag, and deleting lowest/highest sell prices to keep average in line are coming soon. Possibly adding more average types.  

<h2><b>⚖️Licensing and Dislcaimers</b></h2>

***This project is NOT affiliated with Warframe, Digital Extremes, or the Warframe Market.***  
*Copyright (c) 2023 Noah Jenner under MIT License*  
*For additional licensing information, please see LICENSE.txt*

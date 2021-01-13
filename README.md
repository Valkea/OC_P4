# Chess Tournament Manager (CTM)

CTM is a Python 3 script created in order to help managing chess tournament without internet connexion

## Installation

In order to use this script, you need to follow the steps below:

### First, 
let's duplicate the project github repository

```bash
>>> git clone https://github.com/Valkea/OC_P4.git
>>> cd OC_P4
```

### Secondly,
let's create a virtual environment and install the required Python libraries

(Linux or Mac)
```bash
>>> python3 -m venv venv
>>> source venv/bin/activate
>>> pip install -r requirements.txt
```

(Windows):
```bash
>>> py -m venv venv
>>> .\venv\Scripts\activate
>>> py -m pip install -r requirements.txt
```

The curses package comes with the Python standard library. In Linux and Mac, the curses dependencies should already be installed so there is no extra steps needed. On Windows, you need to install one special Python package, windows-curses available on PyPI to add support.

#### Needed in Windows only
```bash
>>> py -m pip install windows-curses
```

You can verify everything works by running a Python interpreter and attempting to import curses. If you do not get any errors, you are in good shape.

```bash
>>> import curses
>>>
```
If that doesn't work, you need to visit http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses, download the version of curses that corresponds to your Windows and version of Python, and then pip install the whl file with the python you plan on using.

### Finally,
we can start CTM by using the following command

```bash
>>> python3 CTM.py
```
or by directly calling the controller
```bash
>>> python3 -m controller
```

In Windows you need to use
```bash
>>> py -m controller
```

## Commands

### Menu
You can naviguate in the app using the menu selector with UP, DOWN and ENTER keys.

### Swap between parallel views
The app is split into two main parts; the central part and the menu part.
At some point, you may need to switch between the both parts, and in this case you need to use the 'small 2 above the TAB' key (or £ if you can't get it).

### Bonus
Also, you can hit BACKSPACE to act as the "<< Retour" selection.
And when initializing a new tournament, you can add some extra players by hitting CTRL+F12


## Some screenshots

The following one shows the page on which we can select the current tournament
![alt text](medias/open_tournament.png)

This one is an example of report (showing all the actors of all tournaments)
![alt text](medias/all_actors_report.png)

And finally, this third screenshot shows the interface of a closed tournament
![alt text](medias/closed_tournament.png)

## Simple process example

If you want to run the full tournament process without the Curses interface, you can try the following command

```bash
>>> CTM_algo_demo.py
```

and if you prefer to input the data yourself, you can add the -i or --inputs argument
```bash
>>> CTM_algo_demo.py --inputs
```

## Flake8 / PEP8

If you need to generate a new flake8 report to check the PEP8 compliance of this projet, use the following command
```bash
>>> flake8 --format=html --htmldir=flake8_report
```
and you will find the html report in the 'flake8_report' folder.

## Tests
You can test the modules of the script with pytest.

```bash
>>> python3 -m pytest -s 
```
**Warning**
Don't run `pytest` directly, use `python3 -m pytest`.
Otherwise the test modules won't find the modules.

## Ouputs

### Logs
you can find the logs in the CTM.log file (you can also edit the logging level in the controller/__main__.py file)

### Data
you can find the saved information in the tournament.json


## License
[MIT](https://choosealicense.com/licenses/mit/)

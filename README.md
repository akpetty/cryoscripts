# NASA-Cryo Python home


## Description

This is the home of all things related to the NASA-Cryo Python meetup group. There is information about Python installation and getting started with Python. Also included are some example Python scripts that might be useful for Cryospheric Scientists (especially sea ice scientists interested in IceBridge/CryoSat-2 data, sorry land ice folk). 
More will hopefully be added by me, and hopefully anyone who wants to share a useful function/script over the coming months.

Note that I have included some data so the scripts will run, but contact me if you want more data to play with. None of these datasets are mine, but they are all publically avaiable (mainly through the NSIDC)

### Repo Layout

* *Data*  
Random data used by the example Python scripts

* *Figures*   
Pretty self-explanatory...

* *Notebooks*   
An example iPython notebook that you can view in GitHub or on nbviewer, and run interactively using Jupyter (locally)

* *Scripts*   
The random Python scripts that may be useful to play around with. Mainly plotting up some basic cryo datasets.

* *Slides*    
Slides from the bi-weekly NASA-Cryo Python meetup sessions.

MENTION ISSUES AND WIKI


## Getting Started

### Installation


I've recently becoming a bit obsessed with using [conda][conda] to install/manage Python. I've played around with packages like the [Enthought Python Distribution (EPD)][EPD] and MacPorts together with PIP (a Python package installer), but have found conda to be the easiest and most flexible to use. The NASA IT guys are also familiar with it, which helps a lot!

Conda is just the Python manager, but conda is included with Anaconda (confusing I know) or Miniconda. I recommend Anaconda, for no real reason other than that's what I used. 

*A quick note about Python 2.7/3.5...*  

Python 3 is an upgrade to Python 2. The most stable version of each is 2.7 and 3.5 respectively. When you install Anaconda, it installed Python 2.7, whereas Anaconda3 installs Python 3.5. You can have loads of fun reading all about the differences [here][2735].

I haven't upgraded to Python 3.5 yet, as I can't really be bothered to check if all my scripts produce the same output, and I'm not sure all my libraries have been ported to 3.5. This is probably worth me thinking about some more, so this is something we can discuss in the meetup perhaps. For now I would suggest sticking with 2.7..

*For Mac users...*    
Open Terminal and run this command to check which python install is being used:
  
```
$ which python
```

It should say something like:

```
$ /Applications/anaconda/bin/python
```

You may need to add the link the anaconda install to the start of your PATH (so it loads that version of Python before any other one you may have installed, e.g. the default Mac install or a Macports install:

```
export PATH=/Applications/anaconda/bin/:$PATH
```

[2735]:<https://wiki.python.org/moin/Python2orPython3>  
[EPD]: <https://www.enthought.com/products/epd/>
[conda]:<http://conda.pydata.org/docs/intro.html>
[git-repo-url]: <https://github.com/akpetty/cryoscripts.git>


Alek Petty / www.alekpetty.com / @alekpetty
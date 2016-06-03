# NASA-Cryo Python home

Contact: Alek Petty / www.alekpetty.com / @alekpetty

## Description

This is the home of all things related to the NASA-Cryo Python meetup group. This is in no way affiliated with NASA.

This page includes information about Python installation and getting started with Python. Also included are some example Python scripts that might be useful for Cryospheric Scientists (especially sea ice scientists interested in IceBridge/CryoSat-2 data, sorry land ice folk, but hopefully that will change in time). 
More will hopefully be added by me, and hopefully others, who want to share a useful function/script over the coming months. I f you're familiar with GitHub you can try a push request, or just send me a file to upload. I can add your author info to the script header.

Note that I have included some data so the scripts will run, but contact me if you want more data to play with. None of these datasets are mine, but they are all publicly available (mainly through the NSIDC)

### Layout

* *[Data](Data)*  
Random data used by the example Python scripts

* *[Figures](Figures)*   
Pretty self-explanatory...

* *[Notebooks](Notebooks)*   
An example iPython notebook that you can view in GitHub or on nbviewer, and run interactively using Jupyter (locally)

* *[Scripts](Scripts)*   
The random Python scripts that may be useful to play around with. Mainly plotting up some basic cryosphere datasets.

* *[Slides](Slides)*    
Slides from the bi-weekly NASA-Cryo Python meetup sessions.

Note also that we are currently in the GitHub *code* tab. Issues about the Python code can be raised in the *issues* tab (I included a few test cases).   

There is also a WiKi we can experiment with too. Both require you to have a GitHub account, but that is pretty trivial step, and I recommend you get one anyway!


## Getting Started

### Installation

I've recently becoming a bit obsessed with using [conda][conda] to install/manage Python. I've played around with packages like the [Enthought Python Distribution (EPD)][EPD] and MacPorts together with PIP (a Python package installer), but have found conda to be the easiest and most flexible to use. 

Conda is just the Python library installer, but conda is included with the Anaconda (confusing I know) or Miniconda Python distributions. I recommend Anaconda, for no real reason other than that's what I used. The NASA IT guys are also familiar with it, which helps a lot...

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


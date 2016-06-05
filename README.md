# NASA-Cryo Python home

Contact: Alek Petty / www.alekpetty.com / @alekpetty

## Description

This is the home of all things related to the NASA-Cryo Python meetup group. This is in no way affiliated with NASA.

This repo includes information about Python installation and getting started with Python. Also included are some example Python scripts that might be useful for Cryospheric Scientists (especially sea ice scientists interested in IceBridge/CryoSat-2 data, sorry land ice folk, but hopefully that will change in time). 
More scripts will be added by me, and hopefully others, who want to share a useful function/script over the coming months. If you're familiar with GitHub you can try a push request, or just send me a file to upload. I can add your author info to the script header to credit your efforts.

Note that I have included some data for the scripts to run, but contact me if you want more data to play with. None of these datasets are mine, but they are all publicly available (mainly through the NSIDC)

### Layout

* *[Data](Data)*  
Random data used by the example Python scripts

* *[Figures](Figures)*   
Pretty self-explanatory...

* *[Notebooks](Notebooks)*   
An example iPython notebook that you can view in GitHub or on nbviewer, and run interactively using Jupyter (locally)

* *[Scripts](Scripts)*   
Some Python scripts that may be useful to play around with. Mainly involve plotting up some basic cryosphere datasets.

* *[Slides](Slides)*    
Slides from the bi-weekly NASA-Cryo Python meetup sessions.

Note also that we are currently in the GitHub *code* tab. Issues about the Python code can be raised in the *issues* tab (I included a few test cases).   

There is also a WiKi we can experiment with too. Both require you to have a GitHub account, but that is pretty trivial step, and I recommend you get one anyway!


## Getting Started

### Installation

I've recently becoming a bit obsessed with using [conda][conda] to install/manage Python. I've played around with packages like the [Enthought Python Distribution (EPD)][EPD] and MacPorts together with PIP (a Python package installer), but have found conda to be the easiest and most flexible to use. 

Conda is just the Python library installer, but conda is included with the Anaconda (confusing I know) or Miniconda Python distributions. I recommend Anaconda, for no real reason other than that's what I used. The NASA IT guys are also familiar with it, which helps a lot...

*A quick note about Python 2.7/3.5...*  

Python 3 is an upgrade to Python 2. The most stable version of each is 2.7 and 3.5 respectively. When you install Anaconda, it installs Python 2.7, whereas Anaconda3 installs Python 3.5. You can have loads of fun reading all about the differences [here][2735].

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

You may need to add a link to the anaconda install at the start of your PATH, so it loads that version of Python before any other one you may have installed, e.g. the default Mac install or a Macports install:

```
$ export PATH=/Applications/anaconda/bin/:$PATH
```
So hopefully Python and Conda are now installed. If you try running the plot_CS2.py script you may get the following error:

```
ImportError: No module named netCDF4
```

which implies we're missing a specific Python library (a netcdf reader that is more adbvanced than the built in SciPy reader). This is where conda comes in. Simply run: 

```
$ conda install netCDF4
```

and it should be ready to go. If you have a problem running conda, check you have write permissions in that folder (you may need to ask IT to update this, I did).


### Using Python

There are a crazy number of Python tutorials on the web, and it depends what kind of learner you are/what your needs are. I'm not going to attempt to reinvent this wheel (although I did a couple of years back when I first got in to Python, so you can [check out that tutorial][pettytutor] if you'd like. It may be a bit out-dated).

I have included a Python [cheat sheet](cheat_sheet.py), which was copied from an online [Data Science course][cheat] and seems to cover a lot of the basics in one go. The [iPython notebook Python tutorial](Notebooks/3_Python_Basic_Concepts.ipynb) I found [online][ipynb] also seems pretty useful. Maybe let me know of any other resrouces you found useful and I can list them here

[pettytutor]:<https://alekpetty.wordpress.com/2014/03/13/using-python/>
[ipynb]:<https://github.com/gumption/Python_for_Data_Science>
[cheat]:<https://github.com/justmarkham/python-reference>
[2735]:<https://wiki.python.org/moin/Python2orPython3>  
[EPD]: <https://www.enthought.com/products/epd/>
[conda]:<http://conda.pydata.org/docs/intro.html>
[git-repo-url]: <https://github.com/akpetty/cryoscripts.git>


## Meetup plan

To be updated after the first Meetup...

Thinking something along the lines of a small (~20 minute) tutorial on a given topic, followed by some general Q&A about that or general Python problems. Plan something along the lines of... 

* Meetup 0: Intro to the Meetup

* Meetup 1: Plotting in Python

* Meetup 2: Regression in Python

* Meetup 3: iPython notebooks




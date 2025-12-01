# FMF_Carriage
EPA's Fluid Modeling Facility - Meteorological Wind Tunnel Carriage Controls

## Development

To run these files, you need a Python version that supports Tkinter, such as `python-tk@3.12`.

### Creating an Executable

#### Create a virtual environment

To create a virtual env, run:
```
python -m venv .venv
```

If this doesn't work, try specifying `python3` instead of just `python`.

To activate it on Windows, run:
```
.venv\Scripts\activate
```

For MacOS/Linux:
```
source .venv/bin/activate
```

#### Run `pyinstaller`

After activating the virtual environment, install `pyinstaller` by running `pip install -r requirements.txt` from the root directory of this project.

Then, run:
```
pyinstaller carriage_gui.pyw
```

This will output the executable to the `dist` directory.
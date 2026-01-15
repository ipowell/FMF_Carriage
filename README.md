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

To activate it on Windows, from Command Prompt run:
```
.venv\Scripts\activate
```

Or from PowerShell:
```
.\venv\Scripts\Activate.ps1
```

For MacOS/Linux:
```
source .venv/bin/activate
```

#### Run `pyinstaller`

After activating the virtual environment, install `pyinstaller` by running `pip install -r requirements.txt` from the root directory of this project.

Then, run:
```
pyinstaller --clean --noconfirm carriage_gui.spec
```

This will output the executable to the `dist` directory.

### Runtime configuration
- The app reads settings from `config.yaml` placed next to the executable (bundled by default).
- You can override the config path at runtime (to use a different config file) by setting the `CARRIAGE_CONFIG` environment variable to an absolute or relative path.
  For example, before running the bundled executable:

  On Windows (Command Prompt):
  ```
  set CARRIAGE_CONFIG=C:\path\to\your\custom_config.yaml
  dist\carriage_gui\carriage_gui.exe
  ```

  On MacOS/Linux (bash):
  ```
  export CARRIAGE_CONFIG=/path/to/your/custom_config.yaml
  ./dist/carriage_gui/carriage_gui
  ```

- Relative paths are resolved relative to the app's bundle folder; absolute paths are used as-is.
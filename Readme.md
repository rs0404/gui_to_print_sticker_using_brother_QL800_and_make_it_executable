# Make python file executable using pyinstaller

```Python
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # Running as bundled executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running in development
        base_path = os.path.abspath(os.path.dirname(__file__))
    
    return os.path.join(base_path, relative_path)
```
- need to copy the assets folder to the dist folder.


# Solution available in the internet which take around 5 hours time of mine
```Python
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

```
`print(resource_path(assets/Roboto-Regular.ttf))`
**Output of this statement**
`/var/folders/fj/_76j4pkd56596l4sjxjdvmhw0000gn/T/_MEIw7jggU/assets/Roboto-Regular.ttf`

## Another method:
```Python
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
```
**Output**
`/Users/spark/Downloads/dist/assets/Roboto-Regular.ttf`

Note: 
Do not turn of the terminal mode until you get the desired result. It will help in debugging in case of problem.
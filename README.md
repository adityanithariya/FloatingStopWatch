# Floating StopWatch

## Prerequisites

Be sure you have the following installed on your development machine:

```
1. git
2. python >= 3.10.x
```

## Setup

Clone the repository:

```powershell
git clone https://github.com/adityanithariya/FloatingStopWatch.git StopWatch
cd StopWatch
```

Create a virtual environment and activate it:

```powershell
virtualenv env
.\env\Scripts\activate
```

Then install the dependencies:

```powershell
pip install -r requirements.txt
```

Once `pip` has finished installing dependencies, you're ready to go!

### Starting Floating Stopwatch

Use below command:
```powershell
python StopWatch.py
```

### Shortcuts

You can use shortcuts from the console window, like:<br>
`Ctrl+P` - Play/Pause <br>
`Ctrl+R` - Reset Clock <br>
`Ctrl+X` - Close <br>
`Ctrl+L` - Lap <br>
`Ctrl+T` - Transition <br>
`Ctrl+S` - Split <br>

## Releases

You can access executable for `Windows` in `dist/` and run it directly without the development environment.

HUTIA
==
##### _HUb para la Telerehabilitación con Inteligencia Artificial (Telerehabilitation Hub with Artificial Intelligence)_
## Requeriments:
### Server
- 256 MB of RAM (for each patient connection)
- GNU/Linux, OSX or Windows
- conda (from Anaconda or Miniconda)
### Jitsi
- 3.75 GB of RAM (max of 5 people at same time)
- GNU/Linux
### Patient
- 2 GB of RAM
- GNU/Linux
- GamePad controller SNES with mapping (like QJoyPad)

## Installation
```bash
~$ conda env create -f enviroment.yml
~$ conda activate Hutia
(Hutia) ~$ python app.py
```

*Patients and healthcare staff must be added manually to the SQLite database*
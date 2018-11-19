# Data-Backend

Das *Data-Backend* Modul bietet eine Schnittstelle zum Speichern der gesammelten Daten
aus dem PJET2018 Projekt im Dateisystem.

![UML](doc/uml.png)

## Getting started
Im Folgenden wird die Einbindung und Verwendung des Data-Backends erläutert.

### 1. Voraussetzungen
Das Dataset-Backend ist auf Python 3 ausgelegt. Es wird davon ausgegangen, dass Python 3 auf
dem Zielsystem installiert und lauffähig ist.
Außerdem muss `pip` (Der standard Paketmanager von Python) installiert sein.



Des Weiteren muss das Python-Modul `virtuelenv` installiert werden:
```
pip install virtualenv
```
(evtl. werden Superuser-Rechte benötigt)



### 2. Virtualenv anlegen (optional, aber empfohlen)
Bei größeren Projekten kann es sinnvoll sein eine virtuelle Python Umgebung (*virtualenv*) zu benutzen.
Der Vorteil solcher Umgebungen ist die Isolation des aktuellen Projekts von anderen
Python Projekten und von der globalen Python-Installation. Z.B. werden die in einer
virtualenv installierten Module ausschließlich in das lokale Projektverzeichnis geladen
und "müllen" so nicht die globale Python installation zu.

Zum Anlegen der virtuellen Umgebung muss der folgende Befehl im Stammverzeichnis des
Projektverzeichnisses ausgeführt werden:
```
virtualenv ./
```

Anschließend (und jedesmal wenn man mit einem neuen Terminal auf die virtuelle Umgebung zugreifen möchte) muss die virtuelle Umgebung aktiviert werden..

Unter Linux:
```
source bin/activate
```

Unter Windows:
```
call Scripts/activate
```


### 3. Data-Backend installieren
Das Data-Backend kann nun über folgenden Befehl installiert werden:
```
pip install git+https://dl0ht.fk4.hs-bremen.de/git/jherkenhoff/Data-Backend.git
```
Es wird nach dem Benutzernamen und dem Passwort für das HS-Git gefragt. Anschließend wird das Data-Backend heruntergeladen und (entweder global oder in der virtualenv) installiert.

### 4. Importieren des Data-Backends
Nach der Installation kann das Data-Backend in eigenen Python-Skripten wie gewohnt importiert werden.
Es besteht aus mehreren Klassen, die importiert werden müssen:
```
from data_backend import Dataset, Sample, GPS, Spectrum
```

### 5. Benutzen der Dataset Klasse

Im Folgenden Beispiel wird ein Sample in das dataset geschrieben:

```
# Importieren
from data_backend import Dataset, Sample, GPS, Spectrum
import numpy as np

# Erstellen eines neuen Datasets:
dataset = Dataset("/home/PJET2018/datasets/", "neustadt")

# Schreiben der Device-Metadaten
dataset.device.name = "Raspberry Pi"
dataset.device.version = "1.8"

# Ein erstes Sample in das dataset schreiben:
sample1 = Sample(
    time     = np.datetime64( "now" ), 
    spectrum = Spectrum( freq=[1e6, 2e6, 3e6], mag=[-87.9, -82.6, -93.4] ),
    gps      = GPS( lat = 8.8016937, lat = 53.0792962 )
)

# Und schließlich das Sample in das Dataset schreiben:
dataset.samples.append(sample1)

# Zum Schluss (z.B. wenn die Messfahrt durch Bremen beendet wurde)
# sollte das Dataset wieder geschlossen werden:
dataset.close()
```

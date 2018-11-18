# Data-Backend

Das *Data-Backend* Modul bietet eine Schnittstelle zum Speichern der gesammelten Daten
aus dem PJET2018 Projekt im Dateisystem.


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
Das Data-Backend Modul besitzt mehrere Klassen, wobei jedoch ausschließlich die `Dataset` Klasse für das abspeichern von Daten benötigt wird:
```
from data_backend import Dataset
```

### 5. Benutzen der Dataset Klasse

Im Folgenden Beispiel wird die Benutzung der Dataset Klasse verdeutlicht:

```
from data_backend import Dataset
import numpy as np

# Erstellen eines leeren Datasets:
dataset = Dataset("/home/PJET2018/datasets/", "neustadt", gps=True)

# Schreiben der Device-Metadaten (geht nur solange noch keine Samples ins dataset geschrieben wurden)
dataset.device.name = "Raspberry Pi"
dataset.device.version = "1.8"
dataset.device.method = "FFT"

sample = Sample(time=np.datetime64('now'), gps=, spectrum=)
dataset.samples.append(sample)
```
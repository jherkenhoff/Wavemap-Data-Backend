# Data-Backend

Das *Data-Backend* Modul bietet eine Schnittstelle zum Speichern der gesammelten Daten
aus dem PJET2018 Projekt im Dateisystem. Dabei wird die eigentliche Datenspeicherung (das schreiben in eine Datenbank oder in eine Datei -> hier HDF5) abstrahiert.

In der folgenden Abbildung ist die Klassenhierarchie des Data-Backends dargestellt:

![UML](doc/uml.png)

(Die tatsächliche Implementierung des Data-backends weicht leicht von der Abbildung ab)

## Getting started
Im Folgenden wird die Einbindung und Verwendung des Data-Backends erläutert.

### 1. Voraussetzungen
Das Dataset-Backend ist auf Python 3 ausgelegt. Es wird davon ausgegangen, dass Python 3 auf
dem Zielsystem installiert und lauffähig ist.
Außerdem muss `pip` (Der standard Paketmanager von Python) installiert sein.


### 2. Virtualenv anlegen (optional, aber empfohlen)
Bei größeren Projekten kann es sinnvoll sein eine virtuelle Python Umgebung (*virtualenv*) zu benutzen.
Der Vorteil solcher Umgebungen ist die Isolation des aktuellen Projekts von anderen
Python Projekten und von der globalen Python-Installation. Z.B. werden die in einer
virtualenv installierten Module ausschließlich in das lokale Projektverzeichnis geladen
und "müllen" so nicht die globale Python installation zu.

Zum installieren des Moduls `virtuelenv` muss folgender Befehl ausgeführt werden:
```
pip install virtualenv
```
(evtl. werden Superuser-Rechte benötigt)

Zum Anlegen der virtuellen Umgebung muss der folgende Befehl im Root des
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
Es wird ausschließlich die Dataset Klasse benötigt:
```
from data_backend import Dataset
```

### 5. Benutzen der Dataset Klasse


#### Anlegen und speichern
Im Folgenden Beispiel wird verdeutlicht, wie ein Dataset angelegt wird und ein Sample darin gespeichert wird:

```
# Importieren
from data_backend import Dataset
import numpy as np

# Erstellen eines neuen Datasets:
# Das erste Argument (hier "./") gibt den Pfad an, wo das Dataset gespeichert werden soll.
# Das zweite Argument (hier "neustadt") gibt den Namen des Datasets an.
dataset = Dataset("./", "neustadt")

# Für die spätere Zuordnung des Datasets sollten die Device Metadaten geschrieben werden:
dataset.device.name = "Raspberry Pi"
dataset.device.version = "1.8"

# Ein Dataset kann mehrere Subsets beinhalten. Das ist zum Beispiel dann sinnvoll, wenn die selbe Messung
# Daten in mehreren Varianten abspeichern möchte (z.B. jeweils einmal mit "minhold", "maxhold" und "quasipeak").
# Das erste Argument (hier "maxhold") gibt den Namen des Subsets an. Er kann frei gewählt werden.
# Das zweite Argument (`freq_bins`) gibt die Frequenzen an, bei denen Spektraldaten gemessen werden. (Hier z.B. bei 1kHz, 10kHz und 100kHz)
# Das dritte Argument (gps_support) gibt an, ob in dem Subset GPS Daten gespeichert werden sollen.
dataset.create_subset("maxhold", freq_bins=[1e3, 1e4, 1e5], gps_support=True)

# Mit dem folgenden Befehl können Daten in das Subset geschrieben werden:
# Über den Index ["maxhold"] wird das Subset ausgewählt, in dem gespeichert werden soll.
dataset["maxhold"].append_sample(
        time     = np.datetime64( "now" ),
        spectrum = [-87.3, -91.3, -89.2],
        lat      = 53.073635,
        lon      = 8.806422,
        alt      = 12,
        speed    = 4,
        sats     = 8,
        accuracy = 6
    )

# Zum Schluss (z.B. wenn die Messfahrt durch Bremen beendet wurde)
# sollte das Dataset wieder geschlossen werden:
dataset.close()
```

**ACHTUNG:** Alle Samples die in einem Dataset gespeichert werden, müssen genau die Anzahl an Frequenzstützstellen aufweisen, wie beim erstellen des Subsets ( mit dataset.create_subset ) angegeben wurden.

#### Öffnen und auslesen
Im Folgenden Beispiel wird verdeutlicht, wie ein bestehendes Dataset geöffnet wird und daraus gelesen werden kann:

```python
# Importieren
from data_backend import Dataset
import numpy as np

# Öffnen eines bestehenden Datasets: (Wurde in vorherigem Beispiel angelegt)
# Der Funktionsaufruf unterscheidet nicht zwischen neuem und bestehendem Dataset
dataset = Dataset("./", "neustadt")

# Auslesen des Device Namens
print(dataset.device.name)

# Das erste Sample aus dem "maxhold" Subset lesen:
sample = dataset["maxhold"][0]

# Die Dataset Klasse unterstützt die standard Python slicing Operatoren:
sample = dataset["maxhold"][:]   # Alle Samples
sample = dataset["maxhold"][:5]  # Die ersten 5 Samples
sample = dataset["maxhold"][-5:] # Die letzen 5 Samples

# Um auf einzelne Elemente innerhalb der Samples zuzugreifen wird der Indexing Operator benutzt:
sample = dataset["maxhold"][0]["time"]          # Zeit des ersten Samples
sample = dataset["maxhold"][:][["lat", "lon"]]  # Latitude und longitude Elemente aller Samples

# Auf diese Weise können bereits einfache Verarbeitungsroutinen generiert werden:
spectrum_mean = dataset["maxhold"][0:2]["spectrum"].mean(1)

# Und wieder das Dataset schließen:
dataset.close()
```


#### Ein Sample ohne GPS-Informationen speichern
Sollen Samples ohne GPS-Informationen gespeichert werden (z.B. für Messungen im E-Gebäude) kann dies beim erstellen eines Subsets bekanntgegeben werden:
```
from data_backend import Dataset
import numpy as np

# Neues Dataset für Messung im E-Gebäude:
dataset = Dataset("./", "hs_e_building")

# Neues Subset ohne GPS Informationen:
dataset.create_subset("minhold", freq_bins=[1e3, 1e4, 1e5], gps_support=False)

# Das Speichern eines Sampes ohne GPS Informationen erfolgt analog zu den vorherigen Beispielen.
# Es müssen ausschließlich die GPS-Felder weggelassen werden:
dataset["minhold"].append_sample(
        time     = np.datetime64( "now" ),
        spectrum = [-87.3, -91.3, -89.2]
    )
```


#### Ein Sample mit reduzierten GPS-Informationen speichern
Eventuell stellt der GPS-Receiver nicht alle zusätzlichen Informationen (wie z.B. speed, accuracy etc.) zur Verfügung. Diese können dann beim Abspeichern eines Samples einfach weggelassen werden. Außschließlich die Felder "lat" und "lon" müssen (bei eingeschaltetem gps_support) zwangsläufig vorhanden sein.

```
# Importieren
from data_backend import Dataset
import numpy as np

dataset = Dataset("./", "blockland")
dataset.create_subset("quasipeak", freq_bins=[1e3, 1e4, 1e5], gps_support=True)

dataset["quasipeak"].append_sample(
        time     = np.datetime64( "now" ),
        spectrum = [-87.3, -91.3, -89.2],
        lat      = 53.073635,
        lon      = 8.806422,
        alt      = 12
    )

dataset.close()
```

## Benchmark

Über das Python Skript `test/benchmark.py` kann ein Benchmark des Data-Backends ausgeführt werden.

------ 100.000 freq bins, 10.000 Samples, dtype=uint8, compression=None
1.0 GB
Write: 57.45 s   1.0 MiB
Read: 1.1 s 953.9 MiB
Read Chunked: 1.1 s 95.5 MiB

------ 100.000 freq bins, 10.000 Samples, dtype=float32, compression=None
4.0 GB
Write: 68.1 s   1.0 MiB
Read: 1.8 s 3814.9 MiB
Read Chunked: 1.9 s 381.5 MiB

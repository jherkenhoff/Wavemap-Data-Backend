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
Bei größeren Projekten kann es sinnvoll sein eine virtuelle Python Umgebung (*virtualenv*)zu benutzen.
Der Vorteil solcher Umgebungen ist die Isolation des aktuellen Projekts von anderen
Python Projekten und von der globalen Python-Installation. Z.B. werden die in einer
virtualenv installierten Module ausschließlich in das lokale Projektverzeichnis geladen
und "müllen" so nicht die globale Python installation zu.

Zum Anlegen der virtuellen Umgebung muss der folgende Befehl im Stammverzeichnis des
Projektverzeichnisses ausgeführt werden:
```
virtualenv ./
```

Anschließend muss die virtuelle Umgebung aktiviert werden..
Unter Linux: (immer noch im Projektverzeichnis-Root)
```
source bin/activate
```

Unter Windows:
```
call Scripts/activate
```

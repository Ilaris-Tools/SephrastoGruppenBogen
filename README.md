# SephrastoGruppenBogen
Ein Sephrasto-Plugin, um eine Übersicht der wichtigsten Eigenschaften mehrerer Charaktere zu erstellen.

## Dev Notes
Ich benutz ne seperate Sephrasto-Installation fürs Coden. Und starte die mit `--settingsfile="custom/settings.ini"` (im debugger) um nen eigenen char und plugins ordner anzugeben. Im pluginordner kann dies Repo dann nen unterordner sein. Sephrasto braucht in dem Ordner die `manifest.json` für metadaten und eine `__init__.py` mit der plugin klasse drin. Die Sachen im UI ordner kann man auch mit dem qtcreator (GUI) bearbeiten und dann mit dem build script die python klassen daraus generieren. Die Wrapper enthalten weiteren code, der beim build nicht überschrieben werden soll. So ist der sourcecode von der UI mehr oder weniger getrennt. Die IDs/labels müssen allerdings die selben in python und qtcreator sein.
Mehr infos: https://docs.ilaris-online.de/sephrasto-hilfe/plugin_api/ 
Ich glaub am Kreaturen/Tierbegleiter Plugin können wir uns erstmal orientieren, weil wir ja nicht den Charaktereditor erweitern wollen sondern ein eigenes Fenster.
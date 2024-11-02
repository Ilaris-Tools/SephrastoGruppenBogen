from dataclasses import dataclass
import os
import urllib.parse

@dataclass
class Gruppe:
    name: str = ""
    # charaktere: List[Char]
    path: str = ""
    columns: int = 4

    def add(self, person):
        self.mitglieder.append(person)
    
    def __str__(self):
        return self.name
    
    def char2html(self, char):
        folder = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(folder, "assets", "charakter.html"), "r") as f:
            html = f.read()
        html = html.replace("{name}", char.name)
        html = html.replace("{kurzbeschreibung}", char.kurzbeschreibung)
        rows = []
        # vorteile
        vorteile = ", ".join([v.anzeigenameExt for v in char.vorteile.values()])
        rows.append(f'<div class="row"><b>Vorteile:</b> {vorteile}</div>')
        # fertigkeiten
        fertigkeiten = ", ". join([f"{f.name} ({f.probenwert}/{f.probenwertTalent})" for f in char.fertigkeiten.values()])
        rows.append(f'<div class="row"><b>Fertigkeiten: </b>{fertigkeiten}</div>')
        # close char
        html = html.replace("{rows}", "<hr/>".join(rows))
        return html
    
    def toHtml(self, charaktere=[]):
        folder = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(folder, "assets", "style.css"), "r") as f:
            css = f.read()
        with open(os.path.join(folder, "assets", "template.html"), "r") as f:
            html = f.read()
        chars = [self.char2html(char) for char in charaktere]
        backgroundImg = os.path.join(folder, "assets", "Hintergrund.jpg")
        backgroundImg = backgroundImg.replace("\\", "/")
        html = html.replace("{css}", css)
        html = html.replace("{charaktere}", "".join(chars))
        html = html.replace("{name}", self.name)
        html = html.replace("{backgroundImg}", backgroundImg)
        return html
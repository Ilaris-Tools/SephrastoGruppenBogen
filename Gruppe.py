from dataclasses import dataclass
import os
import urllib.parse

@dataclass
class Gruppe:
    """A group of Charaktere, configuration and logic."""
    name: str = ""
    # charaktere: List[Char]
    path: str = ""
    columns: int = 4
    freiefertigkeiten: bool = True
    eigenheiten: bool = True
    schriftgroesse: int = 12

    def add(self, person):
        self.mitglieder.append(person)
    
    def __str__(self):
        return self.name  # todo (len(chars))
    
    def char2html(self, char):
        folder = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(folder, "assets", "charakter.html"), "r") as f:
            html = f.read()
        html = html.replace("{name}", char.name)
        html = html.replace("{kurzbeschreibung}", char.kurzbeschreibung)
        rows = []
        # werte
        wtab = "<table class='werte'><tr>"
        for a in char.attribute.values():
            wtab += f"<td>{a.name} {a.wert}</td>"
        wtab += "</tr><tr>"
        skipwerte = ["DH", "SB", "SchiP"]
        print(list(char.abgeleiteteWerte.keys()))
        for w in char.abgeleiteteWerte.values():
            if w.name in skipwerte:
                continue
            # if w.name == "WS" and "RS" in char.abgeleiteteWerte:
            #     wtab += f"<td>{w.name} {w.wert}/{w.wert + char.abgeleiteteWerte['RS'].wert} </td>"
            #     continue
            wtab += f"<td>{w.name} {w.wert}</td>"
        wtab += "</tr></table>"
        rows.append(f'<div class="row">{wtab}</div>')
        # fertigkeiten
        ftab = '<table class="fertigkeiten">'
        for fert in char.fertigkeiten.values():
            # tal = ""
            tal = ", ".join(fert.gekaufteTalente)
            if tal:
                tal = f" ({tal})"
            ftab += f"<tr><td class='pw'>{fert.probenwert}</td><td class='pw'>{fert.probenwertTalent}</td>"
            ftab += f"<td class='fertigkeitname'><span class='fertname'>{fert.name}{tal}</span></td></tr>"
        # freie fertigkeiten
        if self.freiefertigkeiten:
            ff = ", ".join([f"{f.name} {f.wert}" for f in char.freieFertigkeiten if f.name])
            ftab += f'<tr class="freiefertigkeiten"><td colspan="3">{ff}</td></tr>'
            # rows.append(f'<div class="row">{ff}</div>')
        ftab += "</table>"
        rows.append(f'<div class="row">{ftab}</div>')
        # eigenheiten
        if self.eigenheiten:
            eigs = "<td></tr><tr><td>".join([e for e in char.eigenheiten if e])
            if eigs:
                eigs = f"<table class='eigenheiten'><tr><td>{eigs}</td></tr></table>"
            rows.append(f'<div class="row">{eigs}</div>')
        # vorteile
        vorteile = ", ".join([v.anzeigenameExt for v in char.vorteile.values()])
        rows.append(f'<div class="row"><b>Vorteile:</b> {vorteile}</div>')
        # close char
        html = html.replace("{rows}", "".join(rows))
        return html
    
    def toHtml(self, charaktere=[]):
        folder = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(folder, "assets", "style.css"), "r") as f:
            css = f.read()
        with open(os.path.join(folder, "assets", "template.html"), "r") as f:
            html = f.read()
        chars = [self.char2html(char) for char in charaktere]
        assets = os.path.join(folder, "assets")
        backgroundImg = os.path.join(folder, "assets", "Hintergrund.jpg")
        backgroundImg = backgroundImg.replace("\\", "/")
        html = html.replace("{css}", css)
        html = html.replace("{charaktere}", "".join(chars))
        html = html.replace("{name}", self.name)
        html = html.replace("{backgroundImg}", backgroundImg)
        html = html.replace("{assets}", assets)
        return html
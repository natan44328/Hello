"""Erzeugt den druckbaren Budgetplaner 2027 (A4, Deutsch) als PDF."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from pathlib import Path

W, H = A4
M = 40  # Rand
SAGE = HexColor("#7A9E87")
SAGE_L = HexColor("#E7F0EA")
INK = HexColor("#2F3B34")
LINE = HexColor("#B9C9BE")
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
          "August", "September", "Oktober", "November", "Dezember"]
OUT = Path(__file__).with_name("Budgetplaner-2027.pdf")


def header(c, title, sub=""):
    c.setFillColor(SAGE)
    c.rect(0, H - 90, W, 90, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, H - 55, title)
    if sub:
        c.setFont("Helvetica", 11)
        c.drawString(M, H - 75, sub)
    c.setFillColor(INK)


def footer(c):
    c.setFont("Helvetica", 8)
    c.setFillColor(LINE)
    c.drawCentredString(W / 2, 20, "Budgetplaner 2027 · nur für den privaten Gebrauch")
    c.setFillColor(INK)


def table(c, x, y, cols, rows, row_h=20, title=None):
    """cols: Liste von (Überschrift, Breite). Gibt neue y-Position zurück."""
    total = sum(w for _, w in cols)
    if title:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y + 6, title)
        y -= 14
    c.setFillColor(SAGE_L)
    c.rect(x, y - row_h, total, row_h, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    cx = x
    for name, w in cols:
        c.drawString(cx + 5, y - row_h + 6, name)
        cx += w
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    for i in range(rows + 1):
        yy = y - row_h * (i + 1)
        c.line(x, yy, x + total, yy)
    cx = x
    for _, w in cols:
        c.line(cx, y - row_h, cx, y - row_h * (rows + 1))
        cx += w
    c.line(x + total, y - row_h, x + total, y - row_h * (rows + 1))
    return y - row_h * (rows + 1) - 24


def cover(c):
    c.setFillColor(SAGE_L)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(SAGE)
    c.circle(W / 2, H / 2 + 60, 150, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(W / 2, H / 2 + 75, "Budgetplaner")
    c.setFont("Helvetica", 30)
    c.drawCentredString(W / 2, H / 2 + 30, "2027")
    c.setFillColor(INK)
    c.setFont("Helvetica", 13)
    c.drawCentredString(W / 2, H / 2 - 140, "Einnahmen · Ausgaben · Sparziele · Schulden")
    c.setFont("Helvetica", 11)
    c.drawCentredString(W / 2, 120, "Name: ________________________________")
    c.showPage()


def anleitung(c):
    header(c, "So nutzt du deinen Planer")
    c.setFont("Helvetica", 11)
    text = [
        "1. Jahresübersicht: Trage am Monatsende Einnahmen, Ausgaben und Ersparnis ein.",
        "2. Fixkosten: Liste alle regelmäßigen Zahlungen (Miete, Handy, Versicherungen).",
        "3. Monatsbudget: Plane zu Monatsbeginn, wie viel du pro Kategorie ausgeben willst.",
        "4. Ausgaben-Tracker: Notiere jede Ausgabe – das ist der wichtigste Schritt.",
        "5. Sparziele & Schulden: Male die Kästchen aus, wenn du einen Betrag erreicht hast.",
        "",
        "Tipp: Die 50/30/20-Regel",
        "   50 % für Bedürfnisse (Miete, Essen, Versicherungen)",
        "   30 % für Wünsche (Freizeit, Shopping, Restaurant)",
        "   20 % zum Sparen und Schulden tilgen",
        "",
        "Druck-Tipp: In A4 drucken, Skalierung 'Tatsächliche Größe'.",
        "Du kannst einzelne Seiten (z. B. Monatsbudget) beliebig oft ausdrucken.",
    ]
    y = H - 130
    for line in text:
        if line.startswith("Tipp"):
            c.setFont("Helvetica-Bold", 12)
        else:
            c.setFont("Helvetica", 11)
        c.drawString(M, y, line)
        y -= 20
    footer(c)
    c.showPage()


def jahresuebersicht(c):
    header(c, "Jahresübersicht 2027")
    cols = [("Monat", 115), ("Einnahmen", 105), ("Ausgaben", 105),
            ("Gespart", 95), ("Notiz", W - 2 * M - 420)]
    y = H - 115
    c.setFillColor(SAGE_L)
    c.rect(M, y - 22, sum(w for _, w in cols), 22, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 10)
    cx = M
    for n, w in cols:
        c.drawString(cx + 5, y - 15, n)
        cx += w
    c.setFont("Helvetica", 10)
    c.setStrokeColor(LINE)
    rh = 40
    for i, m in enumerate(MONATE + ["Gesamt"]):
        yy = y - 22 - rh * (i + 1)
        c.line(M, yy, W - M, yy)
        if m == "Gesamt":
            c.setFont("Helvetica-Bold", 10)
        c.drawString(M + 5, yy + 15, m)
    cx = M
    for _, w in cols:
        c.line(cx, y - 22, cx, y - 22 - rh * 13)
        cx += w
    c.line(W - M, y - 22, W - M, y - 22 - rh * 13)
    footer(c)
    c.showPage()


def fixkosten(c):
    header(c, "Fixkosten", "Alle regelmäßigen Zahlungen auf einen Blick")
    cols = [("Was", 170), ("Betrag", 80), ("Fällig am", 80),
            ("Rhythmus", 90), ("Konto", W - 2 * M - 420)]
    table(c, M, H - 115, cols, 28, row_h=22)
    footer(c)
    c.showPage()


def monat(c, name):
    header(c, f"{name} 2027", "Monatsbudget")
    half = (W - 2 * M - 20) / 2
    y = table(c, M, H - 120, [("Einnahmen", half - 80), ("Betrag", 80)], 5,
              title="Einnahmen")
    table(c, M + half + 20, H - 120, [("Sparen / Tilgen", half - 80), ("Betrag", 80)], 5,
          title="Sparen & Schulden")
    kats = ["Miete / Wohnen", "Strom / Gas", "Lebensmittel", "Transport / Auto",
            "Versicherungen", "Handy / Internet", "Abos", "Kleidung",
            "Freizeit", "Restaurant", "Geschenke", "Gesundheit", "Sonstiges", ""]
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, y + 6, "Ausgaben")
    y -= 14
    cols = [("Kategorie", 200), ("Geplant", 105), ("Tatsächlich", 105),
            ("Differenz", W - 2 * M - 410)]
    rh = 22
    c.setFillColor(SAGE_L)
    c.rect(M, y - rh, W - 2 * M, rh, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    cx = M
    for n, w in cols:
        c.drawString(cx + 5, y - rh + 7, n)
        cx += w
    c.setFont("Helvetica", 9)
    c.setStrokeColor(LINE)
    for i, k in enumerate(kats):
        yy = y - rh * (i + 2)
        c.line(M, yy, W - M, yy)
        c.drawString(M + 5, yy + 7, k)
    cx = M
    for _, w in cols:
        c.line(cx, y - rh, cx, y - rh * (len(kats) + 1))
        cx += w
    c.line(W - M, y - rh, W - M, y - rh * (len(kats) + 1))
    y = y - rh * (len(kats) + 1) - 30
    c.setFont("Helvetica-Bold", 11)
    for label in ["Einnahmen gesamt:", "Ausgaben gesamt:", "Übrig:"]:
        c.drawString(M, y, label)
        c.setStrokeColor(INK)
        c.line(M + 130, y - 2, M + 260, y - 2)
        y -= 24
    footer(c)
    c.showPage()

    header(c, f"{name} 2027", "Ausgaben-Tracker")
    cols = [("Datum", 65), ("Wofür", 210), ("Kategorie", 130),
            ("Betrag", W - 2 * M - 405)]
    table(c, M, H - 115, cols, 30, row_h=22)
    footer(c)
    c.showPage()


def boxes_page(c, title, sub, fields):
    header(c, title, sub)
    y = H - 120
    for _ in range(3):
        c.setFont("Helvetica-Bold", 11)
        for f in fields:
            c.drawString(M, y, f)
            c.setStrokeColor(LINE)
            c.line(M + 110, y - 2, M + 300, y - 2)
            y -= 20
        size = 22
        for row in range(4):
            for col in range(20):
                c.rect(M + col * (size + 3.6), y - 10 - row * (size + 4) - size,
                       size, size, stroke=1, fill=0)
        y -= 4 * (size + 4) + 40
    footer(c)
    c.showPage()


def notizen(c):
    header(c, "Notizen")
    c.setStrokeColor(LINE)
    y = H - 120
    while y > 50:
        c.line(M, y, W - M, y)
        y -= 24
    footer(c)
    c.showPage()


def main():
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("Budgetplaner 2027")
    c.setAuthor("Budgetplaner 2027")
    cover(c)
    anleitung(c)
    jahresuebersicht(c)
    fixkosten(c)
    for m in MONATE:
        monat(c, m)
    boxes_page(c, "Sparziele", "Jedes Kästchen = ein Betrag deiner Wahl (z. B. 10 €)",
               ["Ziel:", "Betrag:", "Bis wann:"])
    boxes_page(c, "Schulden-Tracker", "Jedes Kästchen = ein getilgter Betrag",
               ["Schuld bei:", "Betrag:", "Zinsen:"])
    notizen(c)
    c.save()
    print("geschrieben:", OUT)


if __name__ == "__main__":
    main()

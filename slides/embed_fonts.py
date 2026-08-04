#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Встраивает шрифты Onest / JetBrains Mono в .pptx (OOXML p:embeddedFontLst,
embedTrueTypeFonts="1"). Обе гарнитуры — OFL, лицензия не нужна.

Использование:
    python3 embed_fonts.py <src.pptx> [dst.pptx]
Если dst не задан — пишет <src>_embedded.pptx рядом.
Шрифты берутся из assets/fonts-embed/ генератора брендбука.
"""
import shutil, zipfile, re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get(
    "ALPHYN_FONT_DIR",
    os.path.normpath(os.path.join(HERE, "..", "assets", "fonts-embed")),
)
FONTS = [
    ("Onest",          "OnestEmbedRegular.ttf", "OnestEmbedBold.ttf"),
    ("JetBrains Mono", "JBMonoEmbedRegular.ttf", None),
]
REL_FONT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font"


def embed(src, dst):
    with zipfile.ZipFile(src) as z:
        data = {n: z.read(n) for n in z.namelist()}
    ct   = data["[Content_Types].xml"].decode()
    rels = data["ppt/_rels/presentation.xml.rels"].decode()
    pres = data["ppt/presentation.xml"].decode()

    if 'Extension="fntdata"' not in ct:
        ct = ct.replace('<Default Extension="rels"',
                        '<Default Extension="fntdata" ContentType="application/x-fontdata"/><Default Extension="rels"', 1)

    nid = max([int(m) for m in re.findall(r'Id="rId(\d+)"', rels)]) + 1
    entries, newfiles = [], {}
    for typeface, reg, bold in FONTS:
        inner = []
        for slot, fn in (("regular", reg), ("bold", bold)):
            if not fn:
                continue
            rid = f"rId{nid}"; nid += 1
            fname = f"font{nid}.fntdata"
            newfiles[f"ppt/fonts/{fname}"] = open(os.path.join(FONT_DIR, fn), "rb").read()
            rels = rels.replace("</Relationships>",
                                f'<Relationship Id="{rid}" Type="{REL_FONT}" Target="fonts/{fname}"/></Relationships>')
            tag = "p:regular" if slot == "regular" else "p:bold"
            inner.append(f'<{tag} r:id="{rid}"/>')
        entries.append(f'<p:embeddedFont><p:font typeface="{typeface}"/>{"".join(inner)}</p:embeddedFont>')

    lst = f'<p:embeddedFontLst>{"".join(entries)}</p:embeddedFontLst>'
    if "embedTrueTypeFonts" not in pres:
        pres = pres.replace("<p:presentation ", '<p:presentation embedTrueTypeFonts="1" ', 1)
    # embeddedFontLst — сразу после sldIdLst (порядок по схеме CT_Presentation)
    m = re.search(r'</p:sldIdLst>', pres)
    pres = pres[:m.end()] + lst + pres[m.end():]

    data["[Content_Types].xml"] = ct.encode()
    data["ppt/_rels/presentation.xml.rels"] = rels.encode()
    data["ppt/presentation.xml"] = pres.encode()
    data.update(newfiles)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for n, b in data.items():
            z.writestr(n, b)
    print("embedded", [e for e, *_ in FONTS], "->", dst)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else src.rsplit(".", 1)[0] + "_embedded.pptx"
    embed(src, dst)

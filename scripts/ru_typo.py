#!/usr/bin/env python3
"""Русская микротипографика Alphyn — неразрывные пробелы (висячие предлоги/союзы).

Правило Alphyn (типографика, `manifest.typography.hanging_words_nbsp`): не оставлять
в конце строки короткие служебные слова — приклеивать неразрывным пробелом (\\u00A0).
Применять к любому русскому тексту материалов перед рендером.

    from ru_typo import ru_hang
    nav = ru_hang(nav_html)

Работает по тексту между `>` и `<` (внутри HTML-тегов, атрибутов, CSS/JS не трогает),
в два прохода — чтобы склеить цепочки вида «и в …».
"""
import re

_RU_SHORT = ("в во и а к ко о об от по с со у до за из на не ни но то да для или что как "
             "при про над под без").split()
_RU_RE = re.compile(r'(^|[\s(«"—\xa0])(' + "|".join(_RU_SHORT) + r')\s+', re.IGNORECASE)

def _glue_seg(seg):
    for _ in range(2):
        seg = _RU_RE.sub(lambda m: m.group(1) + m.group(2) + '\xa0', seg)
    return seg

def ru_hang(html: str) -> str:
    """Проставить неразрывные пробелы после висячих предлогов/союзов в HTML-тексте."""
    return re.sub(r'>([^<]+)<', lambda m: '>' + _glue_seg(m.group(1)) + '<', html)

if __name__ == "__main__":
    for t in ["<p>Alphyn — бренд для команд, которые строят продукт на данных</p>",
              "<p>решения в области ML и аналитики для бизнеса</p>"]:
        print(repr(ru_hang(t)))

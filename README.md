# alphyn-brandbook
Alphyn Brandbook

Брендбук: https://TerryAirwalker.github.io/alphyn-brandbook/
Манифест для ИИ-агента: https://TerryAirwalker.github.io/alphyn-brandbook/manifest.json

## Структура
- `index.html` — собранный брендбук (GitHub Pages).
- `manifest.json` — машиночитаемый источник правды для скилла `alphyn-design`.
- `skill/alphyn-design/SKILL.md` — сам скилл (дизайн-агент бренда Alphyn).
- `slides/` — референс-генератор редактируемого `.pptx` (`make_slide.py`, `embed_fonts.py`,
  `README.md`) — Режим A скилла `alphyn-design` (живой текст + встроенные шрифты).
- `assets/logo/` — SVG знак+начертание Alphyn.
- `assets/icons/` — lucide-иконки (`icons.json`) + лицензия.
- `assets/fonts-embed/` — TTF Onest/JetBrains Mono для встраивания в `.pptx`
  (OOXML `p:embeddedFontLst`).

## Чего нет
Исходники генератора брендбука (`build.py`, `chapters.py`, `build_manifest.py`, `publish.py`,
`copy/`, полный `assets/` с рендерами/превью) — приватные, живут в отдельном репозитории
`alphyn-brandbook-generator` и публикуются сюда выборочно тем же `publish.py`.

## Контакт
Маркетинг: ms@datasapience.ru (Марика Саар — руководитель маркетинга).

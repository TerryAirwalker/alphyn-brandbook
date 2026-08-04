# slides/ — сборка редактируемых слайдов Alphyn (референс)

Рабочий, проверенный на манифесте **v1.1** пример Режима A (`manifest.slides.editability`):
редактируемый `.pptx`, где декор — full-bleed PNG, а весь текст — живые надписи python-pptx,
шрифты Onest / JetBrains Mono встроены в файл.

## Файлы
- `make_slide.py` — шаблон слайда типа «Данные» (крупная цифра + вывод + две `icon_card`).
  Тянет lucide-иконки из `../assets/icons/icons.json` и токены из брендбука. Адаптируй тексты/цифры
  под задачу (цифры — только из `products`/alphyn.ai, не выдумывать).
- `embed_fonts.py` — встраивание Onest/JetBrains Mono в любой `.pptx`
  (`p:embeddedFontLst`, `embedTrueTypeFonts="1"`). Обе OFL — лицензия не нужна.

## Пайплайн
```bash
python3 make_slide.py                       # -> out/test_slide.pptx + out/slide_full.png (proof)
python3 embed_fonts.py out/test_slide.pptx  # -> out/test_slide_embedded.pptx
# проверка рендером:
soffice --headless --convert-to pdf --outdir out out/test_slide_embedded.pptx
pdftoppm -png -r 110 -singlefile out/test_slide_embedded.pdf out/render
```

## Что проверять (Шаг 4 скилла alphyn-design)
Холодная палитра · знак не изменён · правило одного упоминания · только Onest+JetBrains Mono (встроены) ·
висячие предлоги приклеены · фон из 6 разрешённых · иконки только из `slides.icons` (lucide, stroke 1.75,
violet-bright на тёмном) внутри карточек/бейджей, не как декор фона.

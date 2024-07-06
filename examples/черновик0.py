from docxtpl import DocxTemplate
import os
# tpl = DocxTemplate("example.docx")

input_path = os.path.normpath("examples/3-ПТ2-1.docx")
output_path = os.path.normpath("examples/output.docx")

tpl = DocxTemplate(input_path)

context = {
    "col_labels": ["fruit", "vegetable", "stone", "thing"],
    "tbl_contents": [
        {"label": "yellow", "cols": ["banana", "capsicum", "pyrite", "taxi"]},
        {"label": "red", "cols": ["apple", "tomato", "cinnabar", "doubledecker"]},
        {"label": "green", "cols": ["guava", "cucumber", "aventurine", "card"]},
    ],
}


data_tag = {
    "кабеля": [{"марка": "ываыа", "длина_всего": "выаыа", "длина_опт": "", "инфо": ""}],
    "общая_физ_длина": "выыа",
    "общая_опт_длина": "ывавыа",
    "год_прокладки_кабеля": None,
    "год_составления_паспорта": "2023",
    "отв_пред_орг_фио": "ыва",
    "название_объекта": "Приозерск",
    "участок": "Рай",
    "название_компании": "АДская контора",
}


tpl.render(data_tag)
tpl.save(output_path)

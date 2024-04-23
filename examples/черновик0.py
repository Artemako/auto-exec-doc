from docxtpl import DocxTemplate
import os
# tpl = DocxTemplate("example.docx")

input_path = os.path.normpath("D:\work\project\AutoExecDoc\examples/2-РД-1.docx")
output_path = os.path.normpath("D:\work\project\AutoExecDoc\examples\output.docx")

tpl = DocxTemplate(input_path)

context = {
    "col_labels": ["fruit", "vegetable", "stone", "thing"],
    "tbl_contents": [
        {"label": "yellow", "cols": ["banana", "capsicum", "pyrite", "taxi"]},
        {"label": "red", "cols": ["apple", "tomato", "cinnabar", "doubledecker"]},
        {"label": "green", "cols": ["guava", "cucumber", "aventurine", "card"]},
    ],
}

data_context = {
    "реестр_ид_паспорт_трассы": {
        "форма": ["1ф", "2ф", "3ф"],
        "наименование_документа": ["1н", "2н", "2н"],
        "кол_листов": ["1к", "2к", ""],
        "номера_стр": ["1н", "", ""],
        "примечание": ["пппппп", "пппп", "пп"],
    },
    "реестр_ид_эл_паспорт_трассы": {
        "форма": [],
        "наименование_документа": [],
        "кол_листов": [],
        "номера_стр": [],
        "примечание": [],
    },
    "рабочая_документация": {
        "форма": [],
        "наименование_документа": [],
        "кол_листов": [],
        "номера_стр": [],
        "примечание": [],
    },
    "название_объекта": "Рощино",
    "участок": "Приозерск",
    "название_компании": "Лампа",
}

tpl.render(data_context)
tpl.save(output_path)



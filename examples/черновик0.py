from docxtpl import DocxTemplate
import os
# tpl = DocxTemplate("example.docx")

input_path = os.path.normpath("D:\work\project\AutoExecDoc\examples/2-РД-1.docx")
output_path = os.path.normpath("D:\work\project\AutoExecDoc\examples\output.docx")

tpl = DocxTemplate(input_path)

# context = {
#     "col_labels": ["fruit", "vegetable", "stone", "thing"],
#     "tbl_contents": [
#         {"label": "yellow", "cols": ["banana", "capsicum", "pyrite", "taxi"]},
#         {"label": "red", "cols": ["apple", "tomato", "cinnabar", "doubledecker"]},
#         {"label": "green", "cols": ["guava", "cucumber", "aventurine", "card"]},
#     ],
# }

data_context = {
    "реестр_ид_паспорт_трассы": {
        
    },
    "реестр_ид_эл_паспорт_трассы": {
        "форма": ["1ф", "2ф", "3ф"],
        "наименование_документа": ["1ф", "2ф", "3ф"],
        "кол_листов": ["1ф", "2ф", "3ф"],
        "номера_стр": ["1ф", "2ф", "3ф"],
        "примечание": ["1ф", "2ф", "3ф"],
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

# data_context = {
#     "кабеля": [
#         {"марка": "", "длина_всего": "", "длина_опт": "", "инфо": ""},
#         {"марка": "", "длина_всего": "", "длина_опт": "", "инфо": ""},
#         {"марка": "", "длина_всего": "", "длина_опт": "", "инфо": ""},
#     ],
#     "общая_физ_длина": None,
#     "общая_опт_длина": None,
#     "год_прокладки_кабеля": None,
#     "год_составления_паспорта": None,
#     "отв_пред_орг_фио": None,
#     "название_объекта": None,
#     "участок": None,
#     "название_компании": None,
# }
try:
    tpl.render(data_context)
    tpl.save(output_path)
except Exception as e:
    print(e)

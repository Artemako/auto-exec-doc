from docxtpl import DocxTemplate, InlineImage
import os
# tpl = DocxTemplate("example.docx")

input_path = os.path.normpath("examples/3-ПТ2-1.docx")
output_path = os.path.normpath("examples/output.docx")

tpl = DocxTemplate(input_path)

context = {
    "col_labels": ["fruit", "vegetable", "stone", "thing"],
    "tbl_tags": [
        {"label": "yellow", "cols": ["banana", "capsicum", "pyrite", "taxi"]},
        {"label": "red", "cols": ["apple", "tomato", "cinnabar", "doubledecker"]},
        {"label": "green", "cols": ["guava", "cucumber", "aventurine", "card"]},
    ],
}


data_tag = {
    "кабеля": [{"марка": "ываыа", "длина_всего": "выаыа", "длина_опт": "", "инфо": ""}],
    "общая_физ_длина": "выыа",
    "общая_опт_длина": "{{ Привет }}",
    "год_прокладки_кабеля": None,
    "год_составления_паспорта": "2023",
    "отв_пред_орг_фио": "ыва",
    "название_объекта": "Приозерск",
    "участок": "Рай \n Привет мой дивный уголок хаха\n ваы а"
}


# set_of_variables = tpl.get_undeclared_template_variables()
# print(set_of_variables)
tpl.render(data_tag)

tpl.save(output_path)

# tpl = DocxTemplate(output_path)

# data_tag = {
#     "кабеля": [{"марка": "ываыа", "длина_всего": "выаыа", "длина_опт": "", "инфо": ""}],
#     "общая_физ_длина": "выыа",
#     "общая_опт_длина": "{{ Привет }}",
#     "год_прокладки_кабеля": None,
#     "год_составления_паспорта": "2023",
#     "отв_пред_орг_фио": "ыва",
#     "название_объекта": "Приозерск",
#     "участок": "Рай"
# }

# tpl.render(data_tag)
# tpl.save(output_path)

from docxtpl import DocxTemplate
import os

input_path = os.path.normpath("examples/parent_child_table.docx")
output_path = os.path.normpath("examples/result_parent_child_table.docx")

tpl = DocxTemplate(input_path)

context = {
    "parent_table": [
        {
            "label": "yellow",
            "child_table": ["child1", "child2"],
        },
        {
            "label": "red",
            "child_table": ["child3", "child4"],
        },
        {
            "label": "green",
            "child_table": ["child5", "child6"],
        },
    ],
}


tpl.render(context)
tpl.save(output_path)

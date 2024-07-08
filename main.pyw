import package.app as app
import os
import sys


def main():
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    app.App(current_directory)


if __name__ == "__main__":
    main()


__sections_info = [
    {
        "type": "page",
        "page": {
            "id_page": 40,
            "id_node_parent": 1202,
            "page_name": "Л.1. Паспорт трассы волоконно-оптической линии связи на участке.",
            "template_name": "3-ПТ2-1",
            "order_page": 0,
            "included": 1,
        },
        "data": [
            {
                "id_pair": 500,
                "id_page": 40,
                "id_tag": 1220,
                "name_tag": "кабеля",
                "value": None,
            },
            {
                "id_pair": 501,
                "id_page": 40,
                "id_tag": 1225,
                "name_tag": "общая_физ_длина",
                "value": None,
            },
            {
                "id_pair": 502,
                "id_page": 40,
                "id_tag": 1226,
                "name_tag": "общая_опт_длина",
                "value": None,
            },
            {
                "id_pair": 503,
                "id_page": 40,
                "id_tag": 1227,
                "name_tag": "год_прокладки_кабеля",
                "value": None,
            },
            {
                "id_pair": 504,
                "id_page": 40,
                "id_tag": 1228,
                "name_tag": "год_составления_паспорта",
                "value": None,
            },
            {
                "id_pair": 505,
                "id_page": 40,
                "id_tag": 1229,
                "name_tag": "отв_пред_орг_фио",
                "value": None,
            },
        ],
    },
    {
        "type": "node",
        "node": {
            "id_node": 12,
            "name_node": "Паспорт трассы",
            "id_parent": 0,
            "order_node": "3",
            "type_node": "GROUP",
            "template_name": None,
            "included": 1,
        },
        "data": [
            {
                "id_pair": 1200,
                "id_node": 12,
                "id_tag": 1101,
                "name_tag": "инж_про_ком_фио",
                "value": None,
            },
            {
                "id_pair": 1201,
                "id_node": 12,
                "id_tag": 1208,
                "name_tag": "дата",
                "value": None,
            },
        ],
    },
    {
        "type": "node",
        "node": {
            "id_node": 0,
            "name_node": "Проект",
            "id_parent": None,
            "order_node": "0",
            "type_node": "PROJECT",
            "template_name": None,
            "included": 1,
        },
        "data": [
            {
                "id_pair": 100,
                "id_node": 0,
                "id_tag": 1003,
                "name_tag": "название_объекта",
                "value": None,
            },
            {
                "id_pair": 101,
                "id_node": 0,
                "id_tag": 1004,
                "name_tag": "участок",
                "value": None,
            },
            {
                "id_pair": 102,
                "id_node": 0,
                "id_tag": 1001,
                "name_tag": "название_компании",
                "value": None,
            },
        ],
    },
]

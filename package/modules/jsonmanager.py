import json

import package.modules.log as log

class JsonManager:

    @staticmethod
    def get_data_from_json_file(filepath) -> dict:
        log.Log.debug_logger(f"IN get_data_from_json_file(filepath) -> dict: filepath = {filepath}")
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
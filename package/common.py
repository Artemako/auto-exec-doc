# Ошибки
class Errors:
    class MsWordError(Exception):
        pass

    class LibreOfficeError(Exception):
        pass

    def __init__(self):
        self.MsWordError = Errors.MsWordError
        self.LibreOfficeError = Errors.LibreOfficeError

# class DefaultValue:

#     def __init__(self):
#         self.default_value = None


class Common:
    def __init__(self):
        self.errors = Errors()
        self.default_value = None


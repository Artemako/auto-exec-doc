
class Errors:
    class MsWordError(Exception):
        pass

    class LibreOfficeError(Exception):
        pass

    def __init__(self):
        self.MsWordError = Errors.MsWordError
        self.LibreOfficeError = Errors.LibreOfficeError

    

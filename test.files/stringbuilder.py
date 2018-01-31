from cStringIO import StringIO

class StringBuilder:
     _file_str = None

     def __init__(self, value=None):
         self._file_str = StringIO()
         if value is not None:
             self.Append(value)

     def Append(self, str):
         self._file_str.write(str)

     def __str__(self):
         return self._file_str.getvalue()
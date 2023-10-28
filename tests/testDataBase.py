import unittest
import controllers
from controllers import demo_backend




class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.title = 'testing'
        self.prompt = 'input anything'
        self.default = 'random shit'
        self.form=demo_backend.MainWindow().input_popup
    def test_something(self):
        ok,text=self.form(self.title,self.prompt,self.default)
        if ok and text:
            print(text)
            return True
        return False
if __name__ == '__main__':
    unittest.main()

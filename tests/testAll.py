import unittest
from controllers import demo_backend,topoSort
from PyQt5.QtWidgets import QApplication


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app=QApplication([])
        self.w=demo_backend.MainWindow()
    # def test_all(self):
    #     self.app.exec_()

    @unittest.skip('skip test_get_course')
    def test_get_course(self):
        self.w.build_courses_graph("计算机")
        res=topoSort.topoSort(self.w.current_course_graph)
        # self.w.current_course_graph.show_ver()
        print("topo result:")
        for ele in res:
            print('list:')
            for el in ele:
                print(el)
    @unittest.skip("skip display_plan")
    def test_display_plan(self):
        self.w.build_courses_graph('计算机')
        res = topoSort.topoSort(self.w.current_course_graph)
        self.w.display_plan(res, 'testing')

    # @unittest.skip("skip test_all")
    def test_all(self):
        self.app.exec_()


        # self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

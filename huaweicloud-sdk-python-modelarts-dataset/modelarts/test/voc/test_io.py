import os
import sys
import unittest

from modelarts.voc.pascal_voc_io import PascalVocReader


class TestPascalVocRW(unittest.TestCase):

  def test_upper(self):
    dir_name = os.path.abspath(os.path.dirname(__file__))
    libs_path = os.path.join(dir_name, '..', 'libs')
    sys.path.insert(0, libs_path)
    from modelarts.voc.pascal_voc_io import PascalVocWriter
    from modelarts.voc.pascal_voc_io import PascalVocReader

    # Test Write/Read
    writer = PascalVocWriter('tests', 'test', (512, 512, 1), localImgPath='tests/test.512.512.bmp')
    difficult = 1
    writer.addBndBox(60, 40, 430, 504, 'person', difficult)
    writer.addBndBox(113, 40, 450, 403, 'face', difficult)
    writer.save('./test.xml')

    reader = PascalVocReader('./test.xml')
    shapes = reader.getShapes()

    personBndBox = shapes[0]
    face = shapes[1]
    self.assertEqual(personBndBox[0], 'person')
    self.assertEqual(personBndBox[1], [(60, 40), (430, 40), (430, 504), (60, 504)])
    self.assertEqual(face[0], 'face')
    self.assertEqual(face[1], [(113, 40), (450, 40), (450, 403), (113, 403)])

  def test_upper2(self):
    path = os.path.abspath('../../../../') + "/resources/VOC/000000023361_1556180702612.xml"
    print(path)

    reader = PascalVocReader(path)
    shapes = reader.getShapes()

    personBndBox = shapes[0]
    self.assertEqual(personBndBox[0], 'trafficlight')
    self.assertEqual(personBndBox[1], [(199, 115), (258, 115), (258, 235), (199, 235)])
    reader.parseXML()


if __name__ == '__main__':
  unittest.main()

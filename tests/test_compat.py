
import os
import shutil
import tempfile
import unittest
from compat import crossPlatformSymlink


class WindowsLinkerTest(unittest.TestCase):

  def setUp(self):
    self._sDir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self._sDir)

  def testCreatesLinks(self):
    afile = open(os.path.join(self._sDir, 'a'), 'w')
    try:
      afile.write('a')
    finally:
      afile.close()

    crossPlatformSymlink(os.path.join(self._sDir, 'a'),
                         os.path.join(self._sDir, 'b'))

    self.assertTrue(os.path.exists(os.path.join(self._sDir, 'b')))


if __name__ == '__main__':
  unittest.main()
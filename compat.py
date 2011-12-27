#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

class WindowsLinker(object):
  """Creates symbolic links under Windows.
  
  Note that only Administrators have the privilege of creating symbolic
  links on Windows, so you'll need to run as an Administrator.
  """

  _binding = None

  def __init__(self):
    if not self._binding:
      self._bind()

  def _bind(self):
    """Binds the C call that creates symbolic links.

    Warning : this call is not thread-safe. But it shouldn't be a big deal for
    now.
    """
    import ctypes
    binding = ctypes.windll.kernel32.CreateSymbolicLinkW
    binding.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
    binding.restype = ctypes.c_ubyte
    WindowsLinker._binding = binding

  def symlink(self, src, dest):
    import ctypes
    flags = 0
    if src is not None and os.path.isdir(src):
      flags = 1
    if self._binding(dest, src, flags) == 0:
      raise ctypes.WinError()


def crossPlatformSymlink(src, dest):
  """Provides the symlink functionality on platforms where it is available.
  
  This wraps os.symlink on Linux (and MacOS), and use a function present
  in Vista and later version of Windows, that creates symlinks. It will 
  raise a NotImplementedError if your version of Windows doesn't support 
  symlinks.
  
  Note that this might be fixed in later versions of python, since a bug seems
  to trace this issue : http://bugs.python.org/issue1578269
  """
  if hasattr(os, 'symlink'):
    return os.symlink(src, dest)

  if sys.platform.startswith('win32'):
    return WindowsLinker().symlink(src, dest)

  raise NotImplementedError()

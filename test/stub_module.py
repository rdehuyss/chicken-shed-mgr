import sys,types

class MockCallable():
  """ Mocks a function, can be enquired on how many calls it received """
  def __init__(self, result):
    self.result  = result
    self._calls  = []

  def __call__(self, *arguments):
    """Mock callable"""
    self._calls.append(arguments)
    return self.result

  def called(self):
    """docstring for called"""
    return self._calls

class StubModule(types.ModuleType, object):
  """ Uses a stub instead of loading libraries """

  def __init__(self, moduleName):
    self.__name__ = moduleName
    sys.modules[moduleName] = self

  def __repr__(self):
    name  = self.__name__
    mocks = ', '.join(set(dir(self)) - set(['__name__']))
    return "<StubModule: %(name)s; mocks: %(mocks)s>" % locals()
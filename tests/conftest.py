import os
from pytest import fixture
from make_runner import InspectableMakeRunner, ToolkitTestRunner, MakeRunner


def pytest_addoption(parser):
    toolkit_path = os.path.abspath('toolkit.mk')
    parser.addoption('--toolkit-path', default=toolkit_path, help='path to gnu make toolkit')


@fixture
def gmake(tmpdir):
    return InspectableMakeRunner(tmpdir)


@fixture
def make(tmpdir, request):
    toolkit_path = request.config.getoption('--toolkit-path')
    return ToolkitTestRunner(tmpdir, toolkit_path=toolkit_path)

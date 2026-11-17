# SPDX-License-Identifier: MIT
def pytest_addoption(parser):
    parser.addoption('--allen-pdf',default=None,help='Optional separately obtained source for a full-source reproduction check')

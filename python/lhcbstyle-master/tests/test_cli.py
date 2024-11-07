###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from pathlib import Path

import pytest

import lhcbstyle.__main__


def test_install_missing_args():
    with pytest.raises(SystemExit) as e:
        lhcbstyle.__main__.parse_args()
    assert e.value.code == 2


def test_install_args(tmpdir, monkeypatch):
    monkeypatch.setattr(
        "sys.argv", ["lhcbstyle", "install", "--macro-dir", str(tmpdir)]
    )
    lhcbstyle.__main__.parse_args()
    assert Path(tmpdir / "lhcbStyle.C").is_file()
    assert "create_lhcbStyle" in Path(tmpdir / "lhcbStyle.C").read_text()


def test_install_env(tmpdir, monkeypatch):
    monkeypatch.setenv("ROOT_MACRO_DIR", str(tmpdir))
    monkeypatch.setattr("sys.argv", ["lhcbstyle", "install"])
    lhcbstyle.__main__.parse_args()
    assert Path(tmpdir / "lhcbStyle.C").is_file()
    assert "create_lhcbStyle" in Path(tmpdir / "lhcbStyle.C").read_text()


def test_install(tmpdir, monkeypatch):
    try:
        monkeypatch.delenv("ROOT_MACRO_DIR")
    except KeyError:
        pass
    monkeypatch.setattr("sys.argv", ["lhcbstyle", "install"])
    lhcbstyle.__main__.parse_args()

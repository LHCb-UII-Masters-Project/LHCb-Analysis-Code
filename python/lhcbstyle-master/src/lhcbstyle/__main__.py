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
import argparse
import importlib.resources
import os
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("--macro-dir", default=None)
    install_parser.set_defaults(func=lambda a: install(a.macro_dir))

    plot_parser = subparsers.add_parser("plot")
    plot_parser.add_argument(
        "filename", help="ROOT file containing the object you want to draw"
    )
    plot_parser.add_argument("object", help="Path to the object within the ROOT file")
    plot_parser.add_argument(
        "output", default="plot", help="Output filename without file extension"
    )
    plot_parser.add_argument(
        "-D", "--draw-style", default="", help="Option string for Draw()"
    )
    plot_parser.add_argument(
        "-F",
        "--formats",
        nargs="+",
        default=["pdf", "png", "eps"],
        help="Output file formats",
    )
    group = plot_parser.add_mutually_exclusive_group()
    group.add_argument(
        "--official",
        action="store_const",
        dest="label",
        const="LHCb",
        help='Draw "LHCb" label',
    )
    group.add_argument(
        "--preliminary",
        action="store_const",
        dest="label",
        const="LHCb Preliminary",
        help='Draw "LHCb Preliminary" label',
    )
    group.add_argument(
        "--simulation",
        action="store_const",
        dest="label",
        const="LHCb Simulation",
        help='Draw "LHCb Simulation" label',
    )
    group.add_argument(
        "--unofficial",
        action="store_const",
        dest="label",
        const="LHCb Unofficial",
        help='Draw "LHCb Unofficial" label',
    )
    group.add_argument(
        "--no-label",
        action="store_const",
        dest="label",
        const=None,
        help="Don't draw any label (default)",
    )
    plot_parser.set_defaults(
        func=lambda a: plot(
            a.filename, a.object, a.output, a.draw_style, a.formats, a.label
        )
    )

    args = parser.parse_args()
    args.func(args)


def install(macro_dir):
    if not macro_dir:
        macro_dir = os.environ.get("ROOT_MACRO_DIR")
    if not macro_dir:
        import ROOT

        macro_dir = str(ROOT.gROOT.GetMacroDir())
    macro_dir = Path(macro_dir)

    print(f"Writing lhcbStyle.C to {macro_dir}")
    macro_dir.mkdir(exist_ok=True, parents=True)
    with importlib.resources.path("lhcbstyle", "lhcbStyle.C") as path:
        (macro_dir / "lhcbStyle.C").write_text(path.read_text())


def plot(filename, objname, output, draw_style, formats, label=None):
    import ROOT

    from .lhcbstyle import LHCbStyle

    with LHCbStyle():
        input_file = ROOT.TFile.Open(filename)
        plotted_obj = input_file.Get(objname)

        plotted_obj.Draw(draw_style)

        if label is not None:
            ROOT.LHCbStyle.create_label(label).Draw("same")

        for ext in formats:
            ROOT.gPad.SaveAs(f"{output}.{ext}")


if __name__ == "__main__":
    parse_args()  # pragma: no cover

# LHCbStyle

[![PyPI version](https://badge.fury.io/py/lhcbstyle.svg)](https://pypi.org/project/lhcbstyle)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/lhcbstyle)](https://github.com/conda-forge/lhcbstyle-feedstock)
[![Python 3.7‒3.9](https://img.shields.io/badge/python-3.7%E2%80%923.9-blue)](https://www.python.org)

Packaged version of the `lhcbStyle.C` macro with a python wrapper and utilities.

👀 **Looking for just the macro itself? See `src/lhcbstyle/lhcbStyle.C`** or [click here](src/lhcbstyle/lhcbStyle.C) if browsing the repository.

🐍 **Using matplotlib? [Check out `mplhep`](https://github.com/scikit-hep/mplhep#getting-started)**

## ⬇️ Installation

✨ *NB: if using `lb-conda default`, this package is already available.*

### 📦 Via package managers

The python module can be installed using `pip`:
```bash
pip install lhcbstyle
```
or `conda` (via `conda-forge`):
```bash
conda install -c conda-forge lhcbstyle
```

### 📜 Installing the macro

✨ *NB: `conda` users can ignore this step. It is done automatically.*

After installing the package with `pip` or from source, there is one last step
to install the `lhcbStyle.C` macro to ROOT's macro path. This is done using the
console command:
```bash
lhcbstyle install
```

The default directory is found using the PyROOT function `gROOT.GetMacroDir()`,
which is typically somewhere like `/usr/share/root/macros` or `$ROOTSYS/macros`.
If you don't have permission to write to this directory, or you want to install
the macro to a different ROOT installation, you can set the destination with an
environment variable:
```bash
ROOT_MACRO_DIR=/path/to/macros lhcbstyle install
```
or use the command-line option `--macro-dir`:
```bash
lhcbstyle install --macro-dir /path/to/macros
```

If your chosen path does not correspond to `$ROOTSYS/macros`, then you can add it
to ROOT's macro paths using your `~/.rootrc` file. For example, if you installed
`lhcbStyle.C` to `~/.local/share/root/macros` then add this line to `~/.rootrc`:
```
Unix.*.Root.MacroPath: .:$(HOME)/.local/share/root/macros:$(ROOTSYS)/macros
```

## ✍️ Usage

### 🌳 In C++

With the macro successfully installed, you can call it in the usual way:
```c++
gROOT->ProcessLine(".L lhcbStyle.C");
lhcbStyle();
```

The function `lhcbStyle()` takes a boolean argument `print_msg` which controls
whether a message is printed to stdout upon setting the style.

The `TPaveText` (`lhcbName`), `TText` (`lhcbLabel`) and `TLatex` (`lhcbLatex`)
objects are now located in the `LHCbStyle` namespace.

For example, to draw the "LHCb" blurb on a plot, using the default position:
```c++
LHCbStyle::lhcbName->Draw("same");
```

The `TStyle` object (`lhcbStyle`) is also available in the same namespace.

For example, to adjust the style before calling `lhcbStyle()`:
```c++
LHCbStyle::lhcbStyle->SetPadLeftMargin(0.16);
```
or after calling `lhcbStyle()`:
```c++
gStyle->SetPadLeftMargin(0.16);
```

### 🐍 In python

Naturally, in PyROOT, you can execute the macro in much the same way as in C++:
```python
ROOT.gROOT.ProcessLine(".L lhcbStyle.C")
ROOT.lhcbStyle()
```

However, the package includes a python class called `LHCbStyle` which adds
context management, allowing the use of the `with` keyword, e.g.:
```python
from lhcbstyle import LHCbStyle

with LHCbStyle() as lbs:
    can = ROOT.TCanvas()
    hist = make_plot()
    hist.Draw("E1")
    lbs.lhcbName.Draw("same")
    can.SaveAs("hist_lhcb.png")
```

### 🖥️ From the command line

There is also a console command `lhcbstyle plot` which draws a plotable object
saved to a ROOT file.

The positional arguments are:

1. the ROOT file to open
1. the name of the `TObject` to draw
1. the output filename, without extension (optional, defaults to "plot")

The optional arguments are:

- `--draw-style`, `-D`: option string to pass to the `Draw()` function
- `--formats`, `-F`: file extensions to save the plot as

Additionally an label can be added to the plot with one of:

- `--official`: draw "LHCb" label
- `--preliminary`: draw "LHCb Preliminary" label
- `--simulation`: draw "LHCb Simulation" label
- `--unofficial`: draw "LHCb Unofficial" label
- `--no-label`: don't draw any label (default)

For example, to open `plot.root`, extract a `TH1D` called `hist` and draw with
error bars and save it as `Fig1.pdf`, `Fig1.eps` and `Fig1.png`:

```bash
lhcbstyle plot plot.root hist Fig1 --draw-style E --formats pdf eps png
```

See the full usage notes using
```bash
lhcbstyle plot -h
```

## 🛠 Contributing

Creating a development environment
```bash
ssh://git@gitlab.cern.ch:7999/lhcb-docs/lhcbstyle.git
cd lhcbstyle
mamba create --name test-env root pytest pip setuptools_scm
pip install -e .[testing]
pre-commit install
curl -o lb-check-copyright "https://gitlab.cern.ch/lhcb-core/LbDevTools/raw/master/LbDevTools/SourceTools.py?inline=false"
chmod +x lb-check-copyright
```

Running the tests:
```bash
pre-commit run --all-files
pytest
```

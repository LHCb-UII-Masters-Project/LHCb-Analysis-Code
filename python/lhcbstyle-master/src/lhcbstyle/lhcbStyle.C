/*****************************************************************************\
* (c) Copyright 2000-2021 CERN for the benefit of the LHCb Collaboration      *
*                                                                             *
* This software is distributed under the terms of the GNU General Public      *
* Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   *
*                                                                             *
* In applying this licence, CERN does not waive the privileges and immunities *
* granted to it by virtue of its status as an Intergovernmental Organization  *
* or submit itself to any jurisdiction.                                       *
\*****************************************************************************/

////////////////////////////////////////////////////////////////////
// PURPOSE:
//
// This macro defines a standard style for (black-and-white)
// "publication quality" LHCb ROOT plots.
//
// USAGE:
//
// Include the lines
//   gROOT->ProcessLine(".L lhcbStyle.C");
//   lhcbStyle();
// at the beginning of your root macro.
//
// Example usage is given in myPlot.C
//
// COMMENTS:
//
// Font:
//
// The font is chosen to be 132, this is Times New Roman (like the text of
//  your document) with precision 2.
//
// "Landscape histograms":
//
// The style here is designed for more or less square plots.
// For longer histograms, or canvas with many pads, adjustements are needed.
// For instance, for a canvas with 1x5 histograms:
//  TCanvas* c1 = new TCanvas("c1", "L0 muons", 600, 800);
//  c1->Divide(1,5);
//  Adaptions like the following will be needed:
//  gStyle->SetTickLength(0.05,"x");
//  gStyle->SetTickLength(0.01,"y");
//  gStyle->SetLabelSize(0.15,"x");
//  gStyle->SetLabelSize(0.1,"y");
//  gStyle->SetStatW(0.15);
//  gStyle->SetStatH(0.5);
//
// Authors: Thomas Schietinger, Andrew Powell, Chris Parkes, Niels Tuning
// Maintained by Editorial board member (currently Niels)
///////////////////////////////////////////////////////////////////

namespace LHCbStyle
{
  // Use times new roman, precision 2
  Int_t lhcbFont        = 132;  // Old LHCb style: 62;
  // Line thickness
  Double_t lhcbWidth    = 2.00; // Old LHCb style: 3.00;
  // Text size
  Double_t lhcbTSize    = 0.06;
}

TStyle* create_lhcbStyle()
{
  using LHCbStyle::lhcbFont;
  using LHCbStyle::lhcbWidth;
  using LHCbStyle::lhcbTSize;
  TStyle* lhcbStyle = new TStyle("lhcbStyle","LHCb plots style");

  //lhcbStyle->SetErrorX(0); //  don't suppress the error bar along X

  lhcbStyle->SetFillColor(kBlack);
  lhcbStyle->SetFillStyle(kFSolid);
  lhcbStyle->SetFrameFillColor(kWhite);
  lhcbStyle->SetFrameBorderMode(0);
  lhcbStyle->SetPadBorderMode(0);
  lhcbStyle->SetPadColor(kWhite);
  lhcbStyle->SetCanvasBorderMode(0);
  lhcbStyle->SetCanvasColor(kWhite);
  lhcbStyle->SetStatColor(kWhite);
  lhcbStyle->SetLegendBorderSize(0);
  lhcbStyle->SetLegendFont(lhcbFont);


  // set the paper & margin sizes
  lhcbStyle->SetPaperSize(20,26);
  lhcbStyle->SetPadTopMargin(lhcbTSize); // Enough space for 10^3 etc
  lhcbStyle->SetPadRightMargin(0.05); // increase for colz plots
  lhcbStyle->SetPadBottomMargin(0.16);
  lhcbStyle->SetPadLeftMargin(0.14);

  // use large fonts
  lhcbStyle->SetTextFont(lhcbFont);
  lhcbStyle->SetTextSize(lhcbTSize);
  lhcbStyle->SetLabelFont(lhcbFont,"x");
  lhcbStyle->SetLabelFont(lhcbFont,"y");
  lhcbStyle->SetLabelFont(lhcbFont,"z");
  lhcbStyle->SetLabelSize(lhcbTSize,"x");
  lhcbStyle->SetLabelSize(lhcbTSize,"y");
  lhcbStyle->SetLabelSize(lhcbTSize,"z");
  lhcbStyle->SetTitleFont(lhcbFont);
  lhcbStyle->SetTitleFont(lhcbFont,"x");
  lhcbStyle->SetTitleFont(lhcbFont,"y");
  lhcbStyle->SetTitleFont(lhcbFont,"z");
  lhcbStyle->SetTitleSize(1.2*lhcbTSize,"x");
  lhcbStyle->SetTitleSize(1.2*lhcbTSize,"y");
  lhcbStyle->SetTitleSize(1.2*lhcbTSize,"z");

  // use medium bold lines and thick markers
  lhcbStyle->SetLineWidth(lhcbWidth);
  lhcbStyle->SetFrameLineWidth(lhcbWidth);
  lhcbStyle->SetHistLineWidth(lhcbWidth);
  lhcbStyle->SetFuncWidth(lhcbWidth);
  lhcbStyle->SetGridWidth(lhcbWidth);
  lhcbStyle->SetLineStyleString(2,"[12 12]"); // postscript dashes
  lhcbStyle->SetMarkerStyle(kFullCircle);
  lhcbStyle->SetMarkerSize(1.0);

  // label offsets
  lhcbStyle->SetLabelOffset(0.010,"X");
  lhcbStyle->SetLabelOffset(0.010,"Y");

  // by default, do not display histogram decorations:
  lhcbStyle->SetOptStat(0);
  //lhcbStyle->SetOptStat("emr");  // show only nent -e , mean - m , rms -r
  // full opts at http://root.cern.ch/root/html/TStyle.html#TStyle:SetOptStat
  lhcbStyle->SetStatFormat("6.3g"); // specified as c printf options
  lhcbStyle->SetOptTitle(0);
  lhcbStyle->SetOptFit(0);
  //lhcbStyle->SetOptFit(1011); // order is probability, Chi2, errors, parameters
  //titles
  lhcbStyle->SetTitleOffset(0.95,"X");
  lhcbStyle->SetTitleOffset(0.95,"Y");
  lhcbStyle->SetTitleOffset(1.2,"Z");
  lhcbStyle->SetTitleFillColor(kWhite);
  lhcbStyle->SetTitleStyle(0);
  lhcbStyle->SetTitleBorderSize(0);
  lhcbStyle->SetTitleFont(lhcbFont,"title");
  lhcbStyle->SetTitleX(0.0);
  lhcbStyle->SetTitleY(1.0);
  lhcbStyle->SetTitleW(1.0);
  lhcbStyle->SetTitleH(0.05);

  // look of the statistics box:
  lhcbStyle->SetStatBorderSize(0);
  lhcbStyle->SetStatFont(lhcbFont);
  lhcbStyle->SetStatFontSize(0.05);
  lhcbStyle->SetStatX(0.9);
  lhcbStyle->SetStatY(0.9);
  lhcbStyle->SetStatW(0.25);
  lhcbStyle->SetStatH(0.15);

  // put tick marks on top and RHS of plots
  lhcbStyle->SetPadTickX(1);
  lhcbStyle->SetPadTickY(1);

  // histogram divisions: only 5 in x to avoid label overlaps
  lhcbStyle->SetNdivisions(505,"x");
  lhcbStyle->SetNdivisions(510,"y");

  return lhcbStyle;
}

namespace LHCbStyle
{
  TPaveText* create_label(const char* label="LHCb Unofficial")
  {
    using LHCbStyle::lhcbFont;
    using LHCbStyle::lhcbTSize;
    TPaveText* paveText = new TPaveText(
        gStyle->GetPadLeftMargin() + 0.10,
        0.87 - gStyle->GetPadTopMargin(),
        gStyle->GetPadLeftMargin() + 0.25,
        0.95 - gStyle->GetPadTopMargin(),
        "BRNDC"
    );
    auto text = paveText->AddText(label);
    paveText->SetTextFont(lhcbFont);
    paveText->SetTextColor(kBlack);
    paveText->SetTextSize(lhcbTSize);
    paveText->SetFillColor(kWhite);
    paveText->SetTextAlign(12);
    paveText->SetBorderSize(0);
    // Fix the width of the bounding box
    auto bbox = text->GetBBox();
    paveText->SetX2(paveText->GetX1() + (6 + bbox.fWidth) / 320.);
    return paveText;
  }
}

TText* create_lhcbLabel()
{
  using LHCbStyle::lhcbFont;
  using LHCbStyle::lhcbTSize;
  TText* lhcbLabel = new TText();
  lhcbLabel->SetTextFont(lhcbFont);
  lhcbLabel->SetTextColor(kBlack);
  lhcbLabel->SetTextSize(lhcbTSize);
  lhcbLabel->SetTextAlign(12);

  return lhcbLabel;
}

TLatex* create_lhcbLatex()
{
  using LHCbStyle::lhcbFont;
  using LHCbStyle::lhcbTSize;
  TLatex* lhcbLatex = new TLatex();
  lhcbLatex->SetTextFont(lhcbFont);
  lhcbLatex->SetTextColor(kBlack);
  lhcbLatex->SetTextSize(lhcbTSize);
  lhcbLatex->SetTextAlign(12);

  return lhcbLatex;
}

namespace LHCbStyle
{
  TStyle* lhcbStyle = create_lhcbStyle();
  TText* lhcbLabel = create_lhcbLabel();
  TLatex* lhcbLatex = create_lhcbLatex();
}

void lhcbStyle(bool print_msg = true)
{
  // use plain black on white colors
  gROOT->SetStyle("Plain");
  gROOT->SetStyle("lhcbStyle");
  gROOT->ForceStyle();
  if(print_msg)
  {
    std::cout << "-------------------------" << std::endl;
    std::cout << "Set LHCb Style - May 2021" << std::endl;
    std::cout << "-------------------------" << std::endl;
  }
}

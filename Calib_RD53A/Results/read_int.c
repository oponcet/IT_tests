#include "TFile.h"
#include "TDirectory.h"

void read_int() {
    TFile* _file0 = new TFile("/home/xtaldaq/IT_Test/Ph2_ACF/Results/Run000073_SCurve.root", "READ");
    if (!_file0 || _file0->IsZombie()) {
        // Handle error opening the file
        return;
    }

    TDirectory* d1 = _file0->GetDirectory("Detector");
    TDirectory* d2 = d1->GetDirectory("Board_0");
    TDirectory* d3 = d2->GetDirectory("OpticalGroup_0");
    TDirectory* d4 = d3->GetDirectory("Hybrid_0");
    TDirectory* d5 = d4->GetDirectory("Chip_0");

    TCanvas* canvas = (TCanvas*)d5->Get("D_B(0)_O(0)_H(0)_SCurves_Chip(0)");

    TH2F* histogram = dynamic_cast<TH2F*>(canvas->FindObject("D_B(0)_O(0)_H(0)_SCurves_Chip(0)"));

    int numBinsX = histogram->GetNbinsX();
    int numBinsY = histogram->GetNbinsY();
    for (int i = 1; i <= numBinsX; i++) {
        double integral = histogram->Integral(i, i, 1, numBinsY);
        printf("Integral of x bin %d: %f\n", i, integral);
    }

    // result = 1623

    _file0->Close();
}
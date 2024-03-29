//
//  main.cpp
//  fxp_direct_form_I
//
//  Created by 何冠勳 on 2021/6/23.
//

// Simulates a realtime system by sending a 12 bit integer ECG
// through a 50Hz fixed point IIR bandstop

// standard I/O stuff
#include <stdio.h>
#include <assert.h>

// includes the 2nd order IIR filter
#include "DirectFormI.h"

// Notch filter, 2nd order bandstop which means 2 biquad filters
// 50Hz notch frequency, sampling rate 1kHz
//
// generated by the Python script gen_coeff with q=14
// [ 15672. -29825.  15672.  16384. -30222.  15624.]
// [ 16384. -31180.  16384.  16384. -30753.  15720.]

// We loop through the ECG file with the 50Hz contamination
// and save a file which has the 50Hz removed!
int main (int,char**)
{
    // generated by the script 'gen_coeff.py' and then
    // copy/pasted in the filter
    DirectFormI biquad1(12210, 0, -12210, -11153, 4173);
    //DirectFormI biquad2(16384,-31180,16384,16384,-30753,15720,14);
    
    FILE *finput = fopen("audio.dat","rt");
    assert(finput != NULL);
    FILE *foutput = fopen("audio_filtered.dat","wt");
    assert(foutput != NULL);
    for(;;)
    {
        // the data file has 3 channels and time
        short x,y;
        int t;
        if (fscanf(finput,"%d %hd\n",&t,&x)<1) break;
        y = biquad1.filter(x);
        //y = biquad2.filter(y);
        fprintf(foutput,"%d %hd\n",t,y);
    }
    fclose(finput);
    fclose(foutput);
    fprintf(stderr,"Done!\n");
    return 0;
}

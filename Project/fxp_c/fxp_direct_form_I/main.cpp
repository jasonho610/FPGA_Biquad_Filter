//
//  main.cpp
//  fxp_direct_form_I
//
//  Created by 何冠勳 on 2021/6/23.
//

#include <stdio.h>
#include <assert.h>
#include "DirectFormI.h"

int main (int,char**)
{
    DirectFormI biquad1(12210, 0, -12210, -11153, 4173);
    
    FILE *finput = fopen("../../audio.dat","rt");
    assert(finput != NULL);
    FILE *foutput = fopen("../../audio_filtered_DI.dat","wt");
    assert(foutput != NULL);
    for(;;)
    {
        short x,y;
        if (fscanf(finput,"%hd\n",&x)<1) break;
        y = biquad1.filter(x);
        fprintf(foutput,"%hd\n",y);
    }
    fclose(finput);
    fclose(foutput);
    fprintf(stderr,"Done!\n");
    return 0;
}

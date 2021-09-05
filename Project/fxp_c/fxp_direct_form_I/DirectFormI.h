//
//  DirectFormI.h
//  fxp_direct_form_I
//
//  Created by 何冠勳 on 2021/6/23.
//
#ifndef DIRECT_FORM_I_H
#define DIRECT_FORM_I_H
#include <iostream>

class DirectFormI
{
public:
    // constructor with the coefficients b0,b1,b2 for the FIR part
        // and a1,a2 for the IIR part. a0 is always one.
    // the coefficients have been scaled up by the factor
    // 2^q which need to scaled down by this factor after every
    // time step which is taken care of.
    DirectFormI(const short int b0, const short int b1, const short int b2,
            const short int a1, const short int a2,
            const short int q = 14)
    {
        // coefficients are scaled by factor 2^q
        q_scaling = q;
        // FIR coefficients
        c_b0 = b0;
        c_b1 = b1;
        c_b2 = b2;
        // IIR coefficients
        c_a1 = a1;
        c_a2 = a2;
        reset();
    }
    
    void reset ()
    {
        m_x1 = 0;
        m_x2 = 0;
        m_y1 = 0;
        m_y2 = 0;
    }

    // filtering operation: one sample in and one out
    inline short int filter(const short int in)
    {
        // calculate the output
        int out_upscaled = (int)c_b0*(int)in
            + (int)c_b1*(int)m_x1
            + (int)c_b2*(int)m_x2
            - (int)c_a1*(int)m_y1
            - (int)c_a2*(int)m_y2;
        
        /*
        std::cout << in << std::endl;
        std::cout << m_x1 << std::endl;
        std::cout << m_x2 << std::endl;
        std::cout << m_y1 << std::endl;
        std::cout << m_y2 << std::endl;*/

        // scale it back from int to short int
        short int out = out_upscaled >> q_scaling;

        // update the delay lines
        m_x2 = m_x1;
        m_y2 = m_y1;
        m_x1 = in;
        m_y1 = out;

        return out;
    }
    
private:
    // delay line
    short int m_x2; // x[n-2]
    short int m_y2; // y[n-2]
    short int m_x1; // x[n-1]
    short int m_y1; // y[n-1]

    // coefficients
    short int c_b0,c_b1,c_b2; // FIR
    short int c_a1,c_a2; // IIR

    // scaling factor
    short int q_scaling; // 2^q_scaling
};

#endif


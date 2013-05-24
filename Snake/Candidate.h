//
//  Candidate.h
//  SNAKE-XXX
//
//  Created by li xiao on 4/13/13.
//
//

#ifndef SNAKE_XXX_Candidate_h
#define SNAKE_XXX_Candidate_h
#include "cocos2d.h"
using namespace cocos2d;

class Candidate : public cocos2d::CCNode{
public:
    int count;
    int dir;
    
    Candidate(int c, int d){
        count = c;
        dir = d;
    }
    
};



#endif

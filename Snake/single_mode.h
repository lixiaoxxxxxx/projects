//
//  single_mode.h
//  SNAKE-XXX
//
//  Created by li xiao on 4/10/13.
//
//

#ifndef __SNAKE_XXX__single_mode__
#define __SNAKE_XXX__single_mode__

#include <iostream>
#include "cocos2d.h"
#include "Game.h"
using namespace cocos2d;

class Single: public cocos2d::CCLayer
{
public:
    Game* game;
    
    // Method 'init' in cocos2d-x returns bool, instead of 'id' in cocos2d-iphone (an object pointer)
    virtual bool init();
    
    // there's no 'id' in cpp, so we recommend to return the class instance pointer
    static cocos2d::CCScene* scene(int mode);
    
    // a selector callback
    void menuCloseCallback(CCObject* pSender);
    void startgame(CCObject* pSender);
    void gameLogic(float dt);
    void ccTouchesBegan(CCSet* touches, cocos2d::CCEvent* event);
    // preprocessor macro for "static create()" constructor ( node() deprecated )
    CREATE_FUNC(Single);
};

#endif /* defined(__SNAKE_XXX__single_mode__) */

#ifndef __HELLOWORLD_SCENE_H__
#define __HELLOWORLD_SCENE_H__

#include "cocos2d.h"
#include "Game.h"
using namespace cocos2d;

class HelloWorld : public cocos2d::CCLayer
{
public:
    
    Game* demo;
    
    // Method 'init' in cocos2d-x returns bool, instead of 'id' in cocos2d-iphone (an object pointer)
    virtual bool init();

    // there's no 'id' in cpp, so we recommend to return the class instance pointer
    static cocos2d::CCScene* scene();
    
    // a selector callback
    void gameLogic(float dt);
    void menuCloseCallback(CCObject* pSender);
    void startgame(CCObject* pSender);
    void ai_mode(CCObject* pSender);
    void normal_mode(CCObject* pSender);
    void single_mode(CCObject* pSender);
    void ccTouchesBegan(CCSet* touches, cocos2d::CCEvent* event);
    void featured_mode(CCObject* pSender);
    // preprocessor macro for "static create()" constructor ( node() deprecated )
    CREATE_FUNC(HelloWorld);
};

#endif // __HELLOWORLD_SCENE_H__

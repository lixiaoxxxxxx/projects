//
//  single_mode.cpp
//  SNAKE-XXX
//
//  Created by li xiao on 4/10/13.
//
//

#include "single_mode.h"

#include "SimpleAudioEngine.h"
#include <string.h>
#include "Snake.h"
#include "Game.h"
#include <sstream>

using namespace cocos2d;
using namespace CocosDenshion;
using namespace std;

CCScene* Single::scene(int mode)
{
    // 'scene' is an autorelease object
    CCScene *scene = CCScene::create();
    //CCDirector::sharedDirector()->runWithScene(s1);
    
    // 'layer' is an autorelease object
    Single*layer = Single::create();
    
    // add layer as a child to scene
    scene->addChild(layer);
    return scene;
}
void Single::gameLogic(float dt)
{
    this->game->act();
}

// on "init" you need to initialize your instance
bool Single::init()
{
    if ( !CCLayer::init() )
    {
        return false;
    }
    this->setTouchEnabled(true);
    CCMenuItemImage *pCloseItem = CCMenuItemImage::create(
                                                          "CloseNormal.png",
                                                          "CloseSelected.png",
                                                          this,
                                                          menu_selector(Single::menuCloseCallback) );
    pCloseItem->setPosition( ccp(CCDirector::sharedDirector()->getWinSize().width - 20, 20) );
    CCSize size = CCDirector::sharedDirector()->getWinSize();
    CCMenu* pMenu = CCMenu::create(pCloseItem, NULL);
    pMenu->setPosition( CCPointZero );
    this->addChild(pMenu, 1);
    CCSprite* pSprite = CCSprite::create("bg.png");
    pSprite->setPosition( ccp(size.width/2, size.height/2) );
    this->addChild(pSprite, 0);
    
    this->game = new Game(2);
    this->addChild(game);
     
    this->schedule( schedule_selector(Single::gameLogic), 0.03);
    
    return true;
}
void Single::ccTouchesBegan(CCSet* touches, CCEvent* event)
{
    CCTouch* touch = (CCTouch*)( touches->anyObject() );
    CCPoint location = touch->getLocationInView();
    location = CCDirector::sharedDirector()->convertToGL(location);
    game->snake1->turn(location);
}

void Single::menuCloseCallback(CCObject* pSender)
{
    CCDirector::sharedDirector()->end();
    
#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS)
    exit(0);
#endif
}


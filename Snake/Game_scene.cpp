//
//  Game_scene.cpp
//  SNAKE-XXX
//
//  Created by li xiao on 4/5/13.
//
//

#include "Game_scene.h"
#include "HelloWorldScene.h"
#include "SimpleAudioEngine.h"
#include <string.h>
#include "Snake.h"
#include "Game.h"
#include <sstream>

using namespace cocos2d;
using namespace CocosDenshion;
using namespace std;

int Game_scene::game_mode = 0;

CCScene* Game_scene::scene(int mode)
{
    Game_scene::game_mode = mode;
    CCScene *scene = CCScene::create();
    Game_scene*layer = Game_scene::create();
    scene->addChild(layer);
    return scene;
}
void Game_scene::gameLogic(float dt)
{
    this->game->act();
    if (this->game->delay == 30){
        CCScene* scene = NULL;
        do{
            scene = HelloWorld::scene();
            //       scene->schedule( schedule_selector(HelloWorld::gameLogic), 0.05);
            CCDirector::sharedDirector()->pushScene(scene);
        }
        while (0);
    }
}

// on "init" you need to initialize your instance
bool Game_scene::init()
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
                                                          menu_selector(Game_scene::menuCloseCallback) );
    pCloseItem->setPosition( ccp(CCDirector::sharedDirector()->getWinSize().width - 20, 20) );
    
    CCSize size = CCDirector::sharedDirector()->getWinSize();
    
    //CCMenu* pMenu = CCMenu::create(pCloseItem, pstartgame, NULL);
    CCMenu* pMenu = CCMenu::create(pCloseItem, NULL);
    pMenu->setPosition( CCPointZero );
    this->addChild(pMenu, 1);
    CCSprite* pSprite = CCSprite::create("bg.png");
    // position the sprite on the center of the screen
    pSprite->setPosition( ccp(size.width/2, size.height/2) );
    
    this->addChild(pSprite, 0);
    
    
    this->game = new Game(Game_scene::game_mode);
    game->setPosition(20, 20);
    this->addChild(game);
     
    this->schedule( schedule_selector(Game_scene::gameLogic), game->mode == 2 ? 0.03 : 0.1);
    
    return true;
}
void Game_scene::ccTouchesBegan(CCSet* touches, CCEvent* event)
{
    CCTouch* touch = (CCTouch*)( touches->anyObject() );
    CCPoint location = touch->getLocationInView();
    location = CCDirector::sharedDirector()->convertToGL(location);
    if (game->snake1 != NULL && game->snake1->alive == 1)
        game->snake1->turn(location);
    if (game->snake2 != NULL && game->snake2->alive == 1)
        game->snake2->turn(location);
}

void Game_scene::menuCloseCallback(CCObject* pSender)
{
    CCScene* scene = NULL;
    do{
        scene = HelloWorld::scene();
 //       scene->schedule( schedule_selector(HelloWorld::gameLogic), 0.05);
        CCDirector::sharedDirector()->pushScene(scene);
    }
    while (0);
    /*
    CCDirector::sharedDirector()->end();
    
#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS)
    exit(0);
#endif
     */
}



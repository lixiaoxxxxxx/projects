#include "HelloWorldScene.h"
#include "SimpleAudioEngine.h"
#include <string.h>
#include "Snake.h"
#include "Game.h"
#include "Game_scene.h"
#include <sstream>

using namespace cocos2d;
using namespace CocosDenshion;
using namespace std;

CCScene* HelloWorld::scene()
{
    CCScene *scene = CCScene::create();
    HelloWorld *layer = HelloWorld::create();
    scene->addChild(layer);
    return scene;
}

void HelloWorld::gameLogic(float dt)
{
    this->demo->act();
}

bool HelloWorld::init()
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
                                                          menu_selector(HelloWorld::menuCloseCallback) );
    pCloseItem->setPosition( ccp(CCDirector::sharedDirector()->getWinSize().width - 20, 20) );
    CCSize size = CCDirector::sharedDirector()->getWinSize();
    
    CCMenuItemFont *game_single = CCMenuItemFont::create(
                                "AI Game",
                                this,
                                                       menu_selector(HelloWorld:: ai_mode));
    
    
    game_single->setPosition(size.width / 2, size.height / 2 - 40);
    
    
    CCMenuItemFont *pstartgame = CCMenuItemFont::create(
                                "Classic Game",
                                this,
                                                       menu_selector(HelloWorld:: startgame));
    
    
    pstartgame->setPosition(size.width / 2, size.height / 2);
    
    CCMenuItemFont *normal = CCMenuItemFont::create(
                                "Normal Game",
                                this,
                                                       menu_selector(HelloWorld:: normal_mode));
    
    
    normal->setPosition(size.width / 2, size.height / 2 - 80);
    CCMenu* pMenu = CCMenu::create(pCloseItem, normal, pstartgame, game_single, NULL);
    pMenu->setPosition( CCPointZero );
    this->addChild(pMenu, 1);
    /*
    CCLabelTTF* pLabel = CCLabelTTF::create("Fuck cocos2d-x", "Thonburi", 34);
    pLabel->setPosition( ccp(size.width / 2, size.height - 20) );
    this->addChild(pLabel, 1);
     */
    CCSprite* pSprite = CCSprite::create("bg.png");
    pSprite->setPosition( ccp(size.width/2, size.height/2) );
    this->addChild(pSprite, 0);
    
    CCSprite* cartoon_snake = CCSprite::create("main_bg.png");
    cartoon_snake->setPosition(ccp(size.width / 2, size.height / 2 + 80));
    this->addChild(cartoon_snake, 0);
    
    this->demo = new Game(0);
    this->demo->setPosition(10, 10);
    this->addChild(demo, 0);
     
    this->schedule( schedule_selector(Game_scene::gameLogic), 0.1);
    return true;
}
void HelloWorld::ccTouchesBegan(CCSet* touches, CCEvent* event)
{
    CCTouch* touch = (CCTouch*)( touches->anyObject() );
    CCPoint location = touch->getLocationInView();
    location = CCDirector::sharedDirector()->convertToGL(location);
    //cout << "x " << location.x << " " << "y " << location.y << endl;
    //game->snake1->turn(location);
}

void HelloWorld::menuCloseCallback(CCObject* pSender)
{
    CCDirector::sharedDirector()->end();
    
#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS)
    exit(0);
#endif
}

void HelloWorld::normal_mode(CCObject* pSender){
    CCScene* scene = NULL;
    do{
        scene = Game_scene::scene(3);
 //       scene->schedule( schedule_selector(HelloWorld::gameLogic), 0.05);
        CCDirector::sharedDirector()->pushScene(scene);
    }
    while (0);
}

void HelloWorld::startgame(CCObject* pSender){
    CCScene* scene = NULL;
    do{
        scene = Game_scene::scene(1);
 //       scene->schedule( schedule_selector(HelloWorld::gameLogic), 0.05);
        CCDirector::sharedDirector()->pushScene(scene);
    }
    while (0);
}
void HelloWorld::ai_mode(CCObject* pSender){
    CCScene* scene = NULL;
    do{
        scene = Game_scene::scene(2);
 //       scene->schedule( schedule_selector(HelloWorld::gameLogic), 0.05);
        CCDirector::sharedDirector()->pushScene(scene);
    }
    while (0);
}

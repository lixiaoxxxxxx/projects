//
//  scoreboard.h
//  SNAKE-XXX
//
//  Created by li xiao on 4/11/13.
//
//

#ifndef SNAKE_XXX_scoreboard_h
#define SNAKE_XXX_scoreboard_h
#include "cocos2d.h"
#include <sstream>

using namespace cocos2d;
using namespace std;

class Scoreboard: public cocos2d::CCNode{
public:
    CCLabelTTF* score_label;
    CCLabelTTF* name;
    int score;
    CCSprite* bg;
    int owner;
    
    Scoreboard(int snake_id, int score){
        if (snake_id == 0){
            bg = CCSprite::create("cartoon_snake.png");
            //bg->setAnchorPoint(ccp(0.5, 0.5));
            this->addChild(bg);
        }
        if (snake_id == 1){
            bg = CCSprite::create("ai_snake.png");
            this->addChild(bg);
        }
        owner = snake_id;
        char temp[10];
        int c = 0;
        while (score){
            temp[c] = (char)((score % 10) + '0');
            c++;
            score = score / 10;
        }
        cout << c << endl;
        char t[10];
        for (int i = 0; i < c; i++){
            t[i] = temp[c - i - 1];
        }
        t[c] = '\0';
        score_label = CCLabelTTF::create(t, "Helvetica", 30);
        score_label->setPosition(ccp(80 , 0));
        this->addChild(score_label, 1);
    }
    void change_image(){
        this->removeChild(bg);
        if (owner == 1){
            bg = CCSprite::create("cartoon_snake_dead.png");
            //bg->setAnchorPoint(ccp(0.5, 0.5));
            this->addChild(bg);
        }
        if (owner == 0){
            bg = CCSprite::create("ai_snake_dead.png");
            this->addChild(bg);
        }
    }
    void update(int score){
        char temp[10];
        int c = 0;
        while (score){
            temp[c] = (char)((score % 10) + '0');
            c++;
            score = score / 10;
        }
        char t[10];
        for (int i = 0; i < c; i++){
            t[i] = temp[c - i - 1];
        }
        t[c] = '\0';
        this->removeChild(score_label);
        score_label = CCLabelTTF::create(t, "Helvetica", 30);
        score_label->setPosition(ccp(80 , 0));
        this->addChild(score_label, 1);
        
    }


};


#endif

//
//  Telegate.h
//  SNAKE-XXX
//
//  Created by li xiao on 4/10/13.
//
//

#ifndef SNAKE_XXX_Telegate_h
#define SNAKE_XXX_Telegate_h
#include "cocos2d.h"
#include "Block.h"
#define SIZE 15

using namespace cocos2d;

class Telegate : public cocos2d::CCNode{
public:
    CCSprite* gate_1;
    CCSprite* gate_2;
    CCPoint pos1;
    CCPoint pos2;
    int x1;
    int y1;
    int x2;
    int y2;
    int duration;
    Telegate(int x1, int y1, int x2, int y2, int duration = 0){
        pos1 = ccp(x1 * SIZE, y1 * SIZE);
        pos2 = ccp(x2 * SIZE, y2 * SIZE);
        this->x1 = x1;
        this->y1 = y1;
        this->x2 = x2;
        this->y2 = y2;
        gate_1 = CCSprite::create("hole.png");
        gate_2 = CCSprite::create("hole.png");
        gate_1->setScale(0.1);
        gate_2->setScale(0.1);
        gate_1->setPosition(pos1);
        gate_2->setPosition(pos2);
        this->addChild(gate_1);
        this->addChild(gate_2);
        cout << "teleport created" << endl;
    }
    void tele(Block& a){
        if (a.pos.equals(this->pos1)){
            a.x = this->x2;
            a.y = this->y2;
        }
        if (a.pos.equals(this->pos2)){
            a.x = this->x1;
            a.y = this->y1;
        }
    }
    ~Telegate(){
        
    }
    
};



#endif

//
//  Block.h
//  SNAKE-x
//
//  Created by li xiao on 3/28/13.
//
//

#ifndef SNAKE_x_Block_h
#define SNAKE_x_Block_h
#include "cocos2d.h"
#include <vector.h>
using namespace cocos2d;
#define SNAKE_SIZE 15


class Block: public cocos2d::CCNode{
public:
    CCSprite* block;
    CCPoint pos;
    int direction;
    int x;
    int y;
    
    Block(int x, int y){
        pos = ccp(x, y);
        this->x = x;
        this->y = y;
        block = CCSprite::create();
        block->setPosition(pos);
        direction = 1;
    }
    
    CCPoint set_pos(){
        pos = ccp(this->x * SNAKE_SIZE, this->y * SNAKE_SIZE);
        return pos;
    }
    
    int get_x(){
        return this->x;
    }
    int get_y(){
        return this->y;
    }
    void move_left(){
        this->y -= 1;
        block->setPosition(set_pos());
    }
    void move_down(){
        this->x += 1;
        block->setPosition(set_pos());
    }
    void move_right(){
        this->y += 1;
        block->setPosition(set_pos());
    }
    void move_up(){
        this->x -= 1;
        block->setPosition(set_pos());
    }
};

#endif

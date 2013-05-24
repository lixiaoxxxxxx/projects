//
//  Snake.h
//  SNAKE-x
//
//  Created by li xiao on 3/21/13.
//
//

#ifndef __SNAKE_x__Snake__
#define __SNAKE_x__Snake__
#define BATTLE_WIDTH 20
#define BATTLE_HEIGHT 20
#include "cocos2d.h"
#include "Block.h"
#include "Telegate.h"
#include "scoreboard.h"
#include <vector.h>
#include <set.h>
using namespace cocos2d;
//using namespace CocosDenshion;
using namespace std;


class Snake : public cocos2d::CCNode{
public:
    vector<Block> blocks;
    vector<CCPoint> next_poses;
    int _id;
    Scoreboard* board;
    Block* temp;
    Block* head;
    Block *tail;
    Block *new_tail;
    int alive;
    int snake_len;
    Snake(int _id, int x, int y){
        alive = 1;
        for (int i = 0; i < 10; i++){
            temp = new Block(x + _id * 5, y + i);
            this->addChild(temp->block, 0);
            blocks.push_back(*temp);
        }
        this->_id = _id;
        snake_len = 10;
        blocks[0].direction = 2;
        head = &blocks[0];
        tail = &blocks[snake_len - 1];
        cout << this->snake_len << endl;
        
        board = new Scoreboard(this->_id, this->blocks.size());
        if (_id == 0)
            board->setPosition(ccp(360, 230 - 150));
        else
            board->setPosition(ccp(360, 230));
        this->addChild(board);
    }
    
    void act(CCPoint food_loc, Snake* other = NULL){
        /*
        if (this->_id == 1){
            this->ai(food_loc, other);
        }
         */
        this->render();
        this->move();
        //this->what_the_fuck();
    }
    
    void render(){
        if (alive == 0)
            return;
        int direction;
        int next_d;
        float degree;
        for (int i = 0; i < blocks.size(); i++){
            direction = blocks[i].direction;
            degree = (direction - 2) * -90.;
            //blocks[i].block->release();
            blocks[i].block->removeFromParentAndCleanup(true);
            //this->removeChild(blocks[i].block);
            if (i < blocks.size() - 1 && i > 0){
                next_d = blocks[i - 1].direction;
                if (direction != next_d){
                    if(direction == 2){
                        degree = (next_d == 1 ? 0. : 90.);
                    }
                    if (direction == 3){
                        degree = (next_d == 2 ? -90.: 0);
                    }
                    if (direction == 4){
                        degree = (next_d == 3 ? 180. : -90.);
                    }
                    if (direction == 1){
                        degree = (next_d == 2 ? 180. : 90);
                    }
                    blocks[i].block = CCSprite::create("turn.png");
                }
                else{
                    blocks[i].block = CCSprite::create("body.png");
                }
            }
            if (i == 0){
                blocks[i].block = CCSprite::create("head.png");
            }
            if (i == blocks.size() - 1){
                degree = (blocks[i - 1].direction - 2) * -90.;
                blocks[i].block = CCSprite::create("tail.png");
            }
            blocks[i].block->setScale(0.1);
            blocks[i].block->setRotation(degree);
            blocks[i].block->setPosition(blocks[i].set_pos());
            this->addChild(blocks[i].block);
        }
    }
    
    void turn_ai(int dir){
        head = &blocks[0];
        head->direction = dir;
    }
    
    void add_all(){
        for (int i = 0; i < blocks.size(); i++){
            this->addChild(blocks[i].block);
        }
    }
    
    
    bool demo_eat(CCPoint food_loc){
        head = &blocks[0];
        if (head->pos.equals(food_loc)){
            return true;
        }
        return false;
    }
    
    void what_the_fuck(){
        this->snake_len = this->blocks.size();
    }
    
    bool eat(CCPoint food_loc){
        head = &blocks[0];
        if (head->pos.equals(food_loc)){
            if (tail->direction == 1){
                new_tail = new Block(tail->x, tail->y + 1);
                new_tail->direction = 1;
                blocks.push_back(*new_tail);
            }
            if (tail->direction == 2){
                new_tail = new Block(tail->x - 1, tail->y);
                new_tail->direction = 2;
                blocks.push_back(*new_tail);
            }
            if (tail->direction == 3){
                new_tail = new Block(tail->x, tail->y - 1);
                new_tail->direction = 3;
                blocks.push_back(*new_tail);
            }
            if (tail->direction == 4){
                new_tail = new Block(tail->x + 1, tail->y);
                new_tail->direction = 4;
                blocks.push_back(*new_tail);
            }
            snake_len = blocks.size();
            if (snake_len != blocks.size()){
                cout << "1!!!!" << endl;
                while (1);
            }
            tail = &blocks[blocks.size()- 1];
            this->board->update(blocks.size());
            return true;
        }
        return false;
    }
    
    CCPoint get_head(){
        return ccp(blocks[0].x, blocks[0].y);
    }
    
    
    void turn(CCPoint tap_pos){
        if (tap_pos.y > 220 && tap_pos.x > 100 && tap_pos.x < 400 && blocks[0].direction != 1){
            blocks[0].direction = 3;
        }
        if (tap_pos.x < 80 && tap_pos.y > 100 && tap_pos.y < 220 && blocks[0].direction != 2){
            blocks[0].direction = 4;
        }
        if (tap_pos.y < 80 && tap_pos.x > 100 && tap_pos.x < 400 && blocks[0].direction != 3){
            blocks[0].direction = 1;
        }
        if (tap_pos.x > 400 && tap_pos.y > 100 && tap_pos.y < 220 && blocks[0].direction != 4){
            blocks[0].direction = 2;
        }
    }
    void move(){
        if (alive == 0)
            return;
        for(int i = 0; i < blocks.size(); i++){
            if (blocks[i].direction == 1){
                blocks[i].move_left();
            }
            if (blocks[i].direction == 2){
                blocks[i].move_down();
            }
            if (blocks[i].direction == 3){
                blocks[i].move_right();
            }
            if (blocks[i].direction == 4){
                blocks[i].move_up();
            }
        }
        for (int i = blocks.size()- 1; i > 0; i--){
            blocks[i].direction = blocks[i - 1].direction;
        }
    }
};



#endif


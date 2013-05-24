//
//  Game.h
//  SNAKE-x
//
//  Created by li xiao on 3/29/13.
//
//
#include "vector.h"
#include <algorithm>
#include "stdlib.h"
#include "Snake.h"
#include "Telegate.h"
#include <iostream>
#include <memory.h>
#include <ctime>
#include "Candidate.h"
#include "HelloWorldScene.h"

#ifndef SNAKE_x_Game_h
#define SNAKE_x_Game_h
#define BATTLE_WIDTH 20
#define BATTLE_HEIGHT 20

using namespace cocos2d;
using namespace std;


class Game : public cocos2d::CCNode{
public:
    Snake* snake1;
    Snake* snake2;
    bool spawned;
    CCPoint food_loc;
    CCSprite* food;
    CCSprite* temp;
    Telegate* gate;
    vector<CCPoint> unvisited;
    vector<CCPoint> way_to_go;
    int food_x, food_y;
    int mode;
    int poses[20][20];
    int depth[20][20];
    int delay;
    int goal;
    vector<int> targets;
    vector<int> searched;
    //vector<Candidate> ccc;
    
    
    
    Game(int mode){
        // new way
        memset(poses, 0, sizeof(poses));
        delay = 0;
        
        this->mode = mode;
        food = CCSprite::create("food.png");
        food->setScale(0.1);
        spawned = false;
        this->addChild(food, 1);
        
        if (mode == 0){
            snake1 = NULL;
            snake2 = new Snake(1, 10, 10);
            snake2->removeChild(snake2->board);
            this->addChild(snake2);
            cout << "demo mode" << endl;
        }
        if (mode == 1){
            this->spawn_tele();
            this->draw_edge();
            snake1 = new Snake(0, 4, 4);
            snake2 = new Snake(1, 10, 10);
            this->addChild(snake1);
            this->addChild(snake2);
            cout << "classic mode " << endl;
        }
        if (mode == 2){
            this->draw_edge();
            snake1 = NULL;
            snake2 = new Snake(1, 10, 10);
            this->addChild(snake2);
            cout << "ai mode " << endl;
            
        }
        if (mode == 3){
            this->spawn_tele();
            this->draw_edge();
            snake1 = new Snake(0, 4, 4);
            snake2 = NULL;
            this->addChild(snake1);
            cout << "single mode " << endl;
            
        }
        cout << "gamed" << endl;
    }
    
    void set_matrix(){
        int x1, x2, y1, y2;
        int x, y;
        memset(poses, 0, sizeof(poses));
        memset(depth, 0, sizeof(depth));
        if (snake1 != NULL){
            for (int i = 0; i < snake1->blocks.size(); i++){
                x = snake1->blocks[i].get_x();
                y = snake1->blocks[i].get_y();
                if (i == 0){
                    x1 = x;
                    y1 = y;
                }
                poses[x][y] = 1;
            }
        }
        if (snake2 != NULL){
            for (int i = 0; i < snake2->blocks.size(); i++){
                x = snake2->blocks[i].get_x();
                y = snake2->blocks[i].get_y();
                poses[x][y] = i + 1;
                if (i == 0){
                    x2 = x;
                    y2 = y;
                }
                if (i == snake2->blocks.size() - 1){
                    goal = i + 1;
                }
            }
            search(x2, y2);
        }
        if (snake1 != NULL)
            check_death(x1, y1, 0);
        if (snake2 != NULL)
            check_death(x2, y2, 1);
    }
    
    void winner(int _id){
        if (_id == 0){
            snake2->board->change_image();
        }
        else{
            snake1->board->change_image();
        }
        
    }
    
    void mark_snake(){
        unvisited.clear();
        for (int i = 0; i < 20; i++){
            for (int j = 0; j < 20; j++){
                if (poses[i][j] == 0){
                    unvisited.push_back(ccp(i, j));
                }
            }
        }
    }
    
    bool within_grid(int x, int y){
        if (x >= 0 && x < 20 && y >= 0 && y < 20){
            return true;
        }
        else
            return false;
    }
    
    bool found(int x, int y, int d){
        int target = goal;
        /*
        if (d <= 2){
            return false;
        }
         */
        int c = 0;
        while (c != 2){
            if ((poses[x - 1][y] == target && within_grid(x - 1, y)) || (poses[x][y - 1] == target && within_grid(x, y - 1))||
                (poses[x + 1][y] == target && within_grid(x + 1, y)) || (poses[x][y + 1] == target && within_grid(x, y + 1))||
                (poses[x][y] == target && within_grid(x, y))){
                return true;
            }
            c++;
            target++;
        }
        return false;
    }
    
    bool ok_point(int x, int y){
        if (x >= 0 && x < 20 && y >= 0 && y < 20 && (poses[x][y] == 0 || poses[x][y] == (snake2 == NULL ? 0 : snake2->blocks.size()))){
            return true;
        }
        else
            return false;
    }
    
    void bfs_set_matrix(){
        int x, y;
        memset(poses, 0, sizeof(poses));
        memset(depth, 0, sizeof(depth));
        if (snake1 != NULL){
            for (int i = 0; i < snake1->blocks.size(); i++){
                x = snake1->blocks[i].get_x();
                y = snake1->blocks[i].get_y();
                poses[x][y] = -3;   // marks the human snake
            }
        }
        if (snake2 != NULL){
            for (int i = 0; i < snake2->blocks.size(); i++){
                x = snake2->blocks[i].get_x();
                y = snake2->blocks[i].get_y();
                poses[x][y] = i + 1;
            }
        }
        
    }
    

    bool BFS(int x, int y, int d){
        vector<CCPoint> loc;
        loc.push_back(ccp(x, y));
        int c = 0;
        bool founded = false;
        while (c != loc.size()){
            int x = loc[c].x;
            int y = loc[c].y;
            int current_depth = depth[x][y];
            if (found(x, y, current_depth)){
                /*(
                cout << "finding " << goal << endl;
                cout << "founded" << endl;
                for (int i = 0; i < 20; i++){
                    for (int j = 0; j < 20; j++){
                        cout << poses[i][j] << '\t';
                    }
                    cout << endl;
                }
                 */
                bfs_set_matrix();
                founded = true;
                return founded;
            }
            if (c != 0)
                poses[x][y] = -2;
            
            if (ok_point(x - 1, y)){
                poses[x - 1][y] = -1;
                depth[x - 1][y] = current_depth + 1;
                loc.push_back(ccp(x - 1, y));
            }
            if (ok_point(x, y - 1)){
                poses[x][y - 1] = -1;
                depth[x][y - 1] = current_depth + 1;
                loc.push_back(ccp(x, y - 1));
            }
            if (ok_point(x + 1, y)){
                poses[x + 1][y] = -1;
                depth[x + 1][y] = current_depth + 1;
                loc.push_back(ccp(x + 1, y));
            }
            if (ok_point(x, y + 1)){
                poses[x][y + 1] = -1;
                depth[x][y + 1] = current_depth + 1;
                loc.push_back(ccp(x, y + 1));
            }
            c++;
            
            if (c == 450){
                for (int i = 0; i < 20; i++){
                    for (int j = 0; j < 20; j++){
                        cout << poses[i][j] << '\t';
                    }
                    cout << endl;
                }
                cout << "error. c reached 400" << endl;
                while(1);
            }
        }
        /*
        if (founded){
            Candidate *t = new Candidate(c, d);
            ccc.push_back(*t);
        }
         */
        cout << "finding " << goal << endl;
        cout << "not founded" << endl;
        for (int i = 0; i < 20; i++){
            for (int j = 0; j < 20; j++){
                cout << poses[i][j] << '\t';
            }
            cout << endl;
        }
        bfs_set_matrix();
        return founded;
    }
    
    int get_direction(int x1, int y1, int x2, int y2){
        if (x1 == x2){
            return (y2 < y1 ? 1 : 3);
        }
        if (y1 == y2){
            return (x1 < x2 ? 2 : 4);
        }
        return -1;
    }
    
    bool right_way(int x, int y, int dir){
        if (x < food_x && dir == 2){
            return true;
        }
        if (x > food_x && dir == 4){
            return true;
        }
        if (y < food_y && dir == 3){
            return true;
        }
        if (y > food_y && dir == 1){
            return true;
        }
        return false;
    }
    
    void check_death(int x1, int y1, int snake_id){
        int next;
        if (snake_id == 0){
            if (snake1->blocks[0].direction == 1){
                next = poses[x1][y1 - 1];
            }
            if (snake1->blocks[0].direction == 2){
                next = poses[x1 + 1][y1];
            }
            if (snake1->blocks[0].direction == 3){
                next = poses[x1][y1 + 1];
            }
            if (snake1->blocks[0].direction == 4){
                next = poses[x1 - 1][y1];
            }
            if ((next > 0 && next < snake2->blocks.size()) || next == -3){
                snake2->board->change_image();
                snake1->alive = 0;
                delay++;
            }
        }
        /*
        if (snake_id == 1){
            if (snake2->blocks[0].direction == 1){
                next = poses[x1][y1 - 1];
            }
            if (snake2->blocks[0].direction == 2){
                next = poses[x1 + 1][y1];
            }
            if (snake2->blocks[0].direction == 3){
                next = poses[x1][y1 + 1];
            }
            if (snake2->blocks[0].direction == 4){
                next = poses[x1 - 1][y1];
            }
            if ((next > 0 && next < snake2->blocks.size()) || next == -3){
                snake2->board->change_image();
                snake2->alive = 0;
                delay++;
            }
        }
         */
        int s = 0;
        if (ok_point(x1 - 1, y1)){
            s++;
        }
        if (ok_point(x1, y1 - 1)){
            s++;
        }
        if (ok_point(x1 + 1, y1)){
            s++;
        }
        if (ok_point(x1, y1 + 1)){
            s++;
        }
        if (s == 0){
            cout << "snake " << snake_id + 1 << " died" << endl;
            if (snake_id == 0){
                snake1->board->change_image();
                snake1->alive = 0;
                delay++;
                cout << delay << endl;
            }
            else{
                while(1);
                snake2->board->change_image();
                snake2->alive = 0;
                delay++;
                cout << delay << endl;
                
            }
        }
        
    }
    
    int cmp(Candidate a, Candidate b){
        return a.count > b.count;
    }
    
    void search(int x1, int y1){
        //ccc.clear();
        int possible[4];
        int subchoice[4];
        int thinkagain[4];
        int t = 0;
        int s = 0;
        int c = 0;
        if (ok_point(x1 - 1, y1)){
            bfs_set_matrix();
            subchoice[s] = 4;
            s++;
            if (poses[x1 - 1][y1] != snake2->blocks.size())
                poses[x1 - 1][y1] = -44;
            depth[x1 - 1][y1] = 1;
            if (BFS(x1 - 1, y1, 4)){
                possible[c] = 4;
                c++;
            }
        }
        if (ok_point(x1, y1 - 1)){
            bfs_set_matrix();
            subchoice[s] = 1;
            s++;
            if (poses[x1][y1 - 1] != snake2->blocks.size())
                poses[x1][y1 - 1] = -11;
            depth[x1][y1 - 1] = 1;
            if (BFS(x1, y1 - 1, 1)){
                possible[c] = 1;
                c++;
            }
        }
        if (ok_point(x1 + 1, y1)){
            bfs_set_matrix();
            if (poses[x1 + 1][y1] != snake2->blocks.size())
                poses[x1 + 1][y1] = -22;
            depth[x1 + 1][y1] = 1;
            subchoice[s] = 2;
            s++;
            if (BFS(x1 + 1, y1, 2)){
                possible[c] = 2;
                c++;
            }
        }
        if (ok_point(x1, y1 + 1)){
            bfs_set_matrix();
            if (poses[x1][y1 + 1] != snake2->blocks.size())
                poses[x1][y1 + 1] = -33;
            depth[x1][y1 + 1] = 1;
            subchoice[s] = 3;
            s++;
            if (BFS(x1, y1 + 1, 3)){
                possible[c] = 3;
                c++;
            }
        }
        if (c){
            int max = 0;
            int togo = 0;
            /*
            for (int i = 0; i < ccc.size(); i++){
                cout << ccc[i].count << "  " << ccc[i].dir << endl;
                if (max < ccc[i].count){
                    max = ccc[i].count;
                    togo = ccc[i].dir;
                }
            }
            cout << endl;
             */
            int temp;
            srand((unsigned) time(0));
            temp = rand() % 100;
            /*
            if (temp < 40){
                snake2->turn_ai(togo);
                return;
            }
            t = 0;
             */
            for (int i = 0; i < c; i++){
                if (temp > 70){
                    snake2->turn_ai(possible[i]);
                    return;
                }
                if (right_way(x1, y1, possible[i])){
                    thinkagain[t] = possible[i];
                    t++;
                }
            }
            if (t){
                srand((unsigned) time(0));
                int temp = rand() % t;
                snake2->turn_ai(thinkagain[temp]);
                return;
            }
            if (!t){
                srand((unsigned) time(0));
                int temp = rand() % c;
                snake2->turn_ai(possible[temp]);
                return;
            }
        }
        if (s){
            /*
            cout << "snake len " << snake2->blocks.size() << endl;
            for (int i = 0; i < 20; i++){
                for (int j = 0; j < 20; j++){
                    cout << poses[i][j] << '\t';
                    
                }
                cout << endl;
            }
            while(1);
             */
            t = 0;
            for (int i = 0; i < s; i++){
                if (right_way(x1, y1, subchoice[i])){
                    thinkagain[t] = subchoice[i];
                    t++;
                }
            }
            if (t){
                srand((unsigned) time(0));
                int temp = rand() % t;
                snake2->turn_ai(thinkagain[temp]);
                return;
            }
            else{
                srand((unsigned) time(0));
                int temp = rand() % s;
                snake2->turn_ai(subchoice[temp]);
                return;
            }
        }
        if (s == 0){
            cout << "snake2 died";
        }
    }

    void spawn_tele(){
        gate = new Telegate(5, 5, 10, 10);
        this->addChild(gate);
    }
    
    void tete_snake(){
        if (snake1 != NULL){
            for (int i = 0; i < snake1->blocks.size(); i++){
                gate->tele(snake1->blocks[i]);
            }
        }
        /*
         for (int i = 0; i < snake2->snake_len; i++){
         gate->tele(snake2->blocks[i]);
         }
         */
    }
    
    void restart(int snake_id){
        if (snake_id == 1){
            this->removeChild(snake1);
            snake1 = new Snake(0, 4, 4);
            this->addChild(snake1);
        }
        else{
            this->removeChild(snake2);
            snake2 = new Snake(1, 10, 10);
            this->addChild(snake2);
        }
    }
    
    void draw_edge(){
        for (int i = 0; i < 30; i++){
            temp = CCSprite::create("edge.png");
            temp->setScale(0.1);
            temp->setPosition(ccp(20 * SNAKE_SIZE, i * 10));
            this->addChild(temp);
            temp = CCSprite::create("edge.png");
            temp->setScale(0.1);
            temp->setPosition(ccp(i * 10, 20 * SNAKE_SIZE));
            this->addChild(temp);
            temp = CCSprite::create("edge.png");
            temp->setScale(0.1);
            temp->setPosition(ccp(0 - SNAKE_SIZE, i * 10));
            this->addChild(temp);
            temp = CCSprite::create("edge.png");
            temp->setScale(0.1);
            temp->setPosition(ccp(i * 10, 0 - SNAKE_SIZE));
            this->addChild(temp);
        }
        temp = CCSprite::create("edge.png");
        temp->setScale(0.1);
        temp->setPosition(ccp(20 * SNAKE_SIZE, 20 * SNAKE_SIZE));
        this->addChild(temp);
    }
    
    
    void act(){
        mark_snake();
        this->set_matrix();
        if (mode == 0){
            this->spawn();
            if (snake1 != NULL){
                if (snake1->demo_eat(food_loc)){
                    this->remove_food();
                    this->spawn();
                }
                snake1->act(food_loc, snake2);
            }
            if (snake2 != NULL){
                if (snake2->demo_eat(food_loc)){
                    this->remove_food();
                    this->spawn();
                }
                snake2->act(food_loc, snake1);
            }
            
        }
        else{
            this->spawn();
            this->tete_snake();
            if (snake1 != NULL){
                if (snake1->eat(food_loc)){
                    this->remove_food();
                    this->spawn();
                }
                snake1->act(food_loc, snake2);
            }
            if (snake2 != NULL){
                if (snake2->eat(food_loc)){
                    this->remove_food();
                    this->spawn();
                }
                snake2->act(food_loc, snake1);
            }
            
        }
        //this->kill_snake();
        
    }
    
    void remove_food(){
        spawned = false;
    }
    
    void spawn(){
        if(!spawned){
            srand((unsigned) time(0));
            int temp = rand() % unvisited.size();
            
            food_x = unvisited[temp].x;
            food_y = unvisited[temp].y;
            food_loc = ccp(food_x * SNAKE_SIZE, food_y * SNAKE_SIZE);
            spawned = true;
            food->setPosition(food_loc);
            //cout << "food spawned" << endl;
        }
    }
    
};


#endif

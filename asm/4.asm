DATAS SEGMENT
STR   DB"please input a string:$"   
BUF   DB 20
      DB ?
      DB 20 DUP (?)
CRLF  DB 0AH,0DH,"$";此处输入数据段代码 
DATAS ENDS
STACKS SEGMENT STACK
       DB      200 DUP(?) ;此处输入堆栈段代码
STACKS ENDS
CODES  SEGMENT
       ASSUME CS:CODES,DS:DATAS,SS:STACKS
START: MOV AX,DATAS
       MOV DS,AX
       LEA DX,STR
       MOV AH,9
       INT 21H
       MOV AH,10
       LEA DX,BUF
       INT 21H
       LEA DX,CRLF
       MOV AH,9
       INT 21H
       MOV CL,BUF+1
       LEA SI,BUF+2
NEXT:  MOV DL,[SI]
       MOV AH,2
       INT 21H
       INC SI
       DEC CL
       JNZ NEXT;此处输入代码段代码 
       MOV AH,4CH
       INT 21H
CODES  ENDS
    END START

STACK  SEGMENT  STACK
	DB  200 DUP(0)
STACK  ENDS

DATA   SEGMENT
	PARM1  	DB 'please input the arithmetic in the form of XXopXXopXX:$'
	PARM2  	DB '=$'
	PARM3 	DB 0DH,0AH,'$'
	PARM4  	DB 0DH,0AH,'error input format!!$'
	A      	DB 4 DUP (?)	; store the first number
	B      	DB 4 DUP (?)	; the second
	AA		DB 4 DUP (?)	; and the third
	M      	DW 2 DUP (?)
DATA   ENDS

CODE   SEGMENT
	ASSUME CS:CODE,DS:DATA,SS:STACK

BEGIN: 
	MOV    AX,DATA
	MOV    DS,AX
	MOV    AX,0
	MOV    BX,0
	MOV    DI,0
	CALL   START

EXIT:  
	MOV    AH,4CH
	INT    21H

START  PROC  
	PUSH   DS
	PUSH   AX
	LEA    DX,PARM1
	MOV    AH,9        
	INT    21H
	MOV    BL,2
	LEA    DI,A       

	F1:    
	MOV    CL,2 

	FIRST: 
	MOV    AH,0
	INT    16H
	CMP    AL,'q'
	JE    EXIT	; q to quit
	CMP    AL,'0'
	JAE    I1	; >=
	JMP    ERROR

	I1:    
	CMP    AL,'9'
	JBE    I2	; <=
	JMP    ERROR

	I2:    
	SUB    AL,30H	;get the value of input

	POS1:  
	MOV    [DI],AL
	PUSH   BX
	PUSH   DI
	ADD    AL,30H
	MOV    AH,14
	INT    10H
	POP    DI
	POP    BX
	INC    DI
	DEC    CL	; previous set CL 2, thus read 2 digis ofr A
	JZ     SEC
	JMP    FIRST

	SEC:   DEC    BL	; init BL with 2
	JZ     THIRD
	MOV    AH,1
	INT    21H 
	MOV    CH,AL
	LEA    DI,B
	JMP    F1

	THIRD: MOV    BX,10
	MOV    AL,A
	MUL    BL
	MOV    BX,AX
	ADD    BL,A+1
	ADC    BH,0	; add carrier
	MOV    WORD PTR A,BX	; store the value of first number into A

	MOV    BL,10
	MOV    AL,B
	MUL    BL
	MOV    BX,AX
	ADD    BL,B+1
	ADC    BH,0            
	MOV    WORD PTR B,BX   

	MOV    AX,WORD PTR A
	MOV    BX,WORD PTR B

	CMP    CH,'+'       
	JNE    LOPA1
	ADD    AX,BX
	MOV    M,AX
	MOV    CL,4
	JMP    cal

	LOPA1: CMP    CH,'-'
	JNE    LOPA2
	SUB    AX,BX       
	MOV    M,AX
	MOV    CL,4
	JMP    cal
	LOPA2: CMP    CH,'*'
	JNE    LOPA3       
	MUL    BX  
	MOV    M,AX
	MOV    CL,4
	JMP    cal
	LOPA3: CMP    CH,'/'
	JNE    ERROR                       
	DIV    BL 
	MOV    AH,0
	MOV    M,AX
	MOV    CL,4


	cal:push AX
	lea DI, AA
	mov AH, 1
	INT 21H
	mov ch, al

	lF1:    MOV    CL,2 

	lFIRST: MOV    AH,0
	INT    16H
	CMP    AL,'q'
	JE    EXIT	; q to quit
	CMP    AL,'0'
	JAE    lI1	; >=
	JMP    ERROR

	lI1:    CMP    AL,'9'
	JBE    lI2	; <=
	JMP    ERROR

	lI2:    SUB    AL,30H	;get the value of input
	lPOS1:  MOV    [DI],AL
	PUSH   BX
	PUSH   DI
	ADD    AL,30H
	MOV    AH,14
	INT    10H
	POP    DI
	POP    BX
	INC    DI
	DEC    CL	; previous set CL 2, thus read 2 digis ofr A
	JZ    lproc 
	JMP    lFIRST

	lproc: MOV    BX,10
	MOV    AL,AA
	MUL    BL
	MOV    BX,AX
	ADD    BL,AA+1
	ADC    BH,0	; add carrier
	MOV    WORD PTR AA,BX	; store the value of first number into A
	pop AX
	mov BX, word ptr AA

	CMP    CH,'+'       
	JNE    lLOPA1
	ADD    AX,BX
	MOV    M,AX
	MOV    CL,4
	JMP    F3

	lLOPA1: CMP    CH,'-'
	JNE    lLOPA2
	SUB    AX,BX       
	MOV    M,AX
	MOV    CL,4
	JMP    F3
	lLOPA2: CMP    CH,'*'
	JNE    lLOPA3       
	MUL    BX  
	MOV    M,AX
	MOV    CL,4
	JMP    F3
	lLOPA3: CMP    CH,'/'
	JNE    ERROR                       
	DIV    BL 
	MOV    AH,0
	MOV    M,AX
	MOV    CL,4

	F3:    MOV    BL,10		; repeadly divide the number in AX with 10 and push the result in stack
	DIV    BL
	MOV    DL,AH
	MOV    DH,0
	PUSH   DX
	MOV    AH,0
	DEC    CL
	JNZ    F3
	LEA    DX,PARM2 
	MOV    AH,9
	INT    21H
	MOV    CL,4 
	F4:    POP    AX
	MOV    AH,14	; use the value in AL to write to the screen
	MOV    BX,0
	ADD    AL,30H
	INT    10H
	DEC    CL
	JNZ    F4
	LEA    DX,PARM3 
	MOV    AH,9
	INT    21H
	JMP    FINISH
	ERROR: LEA    DX,PARM4
	MOV    AH,9
	INT    21H
	LEA    DX,PARM3
	MOV    AH,9
	INT    21H

	FINISH:RET
START  ENDP
CODE   ENDS
END  BEGIN

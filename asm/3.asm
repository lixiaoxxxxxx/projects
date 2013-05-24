stack segment stack
byte 64 dup(0)
stack ends

data segment
	txt_text db "Our super duper cool text here :) $" 
	txt_error db "Wrong key pressed! $"
data ends

code segment
start:

;org 100h
xor ax, ax 
int 16h

xor cx, cx 
mov cl, al 

mov ah, 9
mov dx, offset txt_text 
int 21h

mov ax,4c00h
int 21h

print: 
int 21h 
loopnz print

mov ax, 4c00h
int 21h


code ends

end start

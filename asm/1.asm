stack segment stack
byte 64 dup(0)
stack ends

data segment
msg db 'hello world!$'
data ends

code segment
assume cs:code,ss:stack,ds:data
start:
mov ax,data
mov ds,ax
mov dx,offset msg
mov ah,9
int 21h
mov ax,4c00h
int 21h
code ends

end start

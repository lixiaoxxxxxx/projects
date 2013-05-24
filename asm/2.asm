data segment
notice db 0dh, 0ah,'===proc of number 16 -> 2===', 0dh, 0ah
db '**the Letter only can be: A,B,C,D,E,F**', 0dh, 0ah, '$'
result db 0dh, 0ah,'the result is:$'
errmsg db 'Error: illegal input',0Dh,0Ah,'$'
data ends

code segment
assume cs:code,ds:data
main proc far
start:
push ds
mov ax, data
mov ds, ax 
xor ax, ax
push ax
;显示提示信息
mov ah, 09h
lea dx, notice
int 21h
;循环接受4个16进制字符，存于bx
mov ch, 4 ;接受字符数循环
mov cl, 4 ;移位循环控制数
xor bx, bx
mov ah, 01h
getch: int 21h
sub al, '0'
cmp al, 0
jl error
cmp al, 9
jl next
sub al, 7 ;字母时要再减7
next: rol bx, cl 
or bl, al ;把新数放在最后
dec ch
jnz getch
;显示二进制数 
mov ah, 09h ;提示信息
lea dx, result
int 21h
mov ch, 16d
mov ah, 02h
showN: rol bx, 1
mov dl, bl
and dl, 01h
add dl, '0'
int 21h
dec ch
jnz showN

jmp exit 
;出错处理 
error: mov ah, 09h
lea dx, errmsg
int 21h
mov ah, 02h
mov dl, 07h ;响玲
int 21h
exit: ret
main endp
code ends
end start


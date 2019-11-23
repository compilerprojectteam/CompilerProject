# CompilerProject
Compiler Design course project 

the grammer of language our compiler supports is: 

```
Program -> Declaration-list eof
Declaration-list -> Declaration Declaration-list
Declaration-list -> ε   
Declaration -> Declaration-initial Declaration-prime
Declaration-initial -> Type-specifier id
Declaration-prime -> Fun-declaration-prime
Declaration-prime -> Var-declaration-prime
Var-declaration-prime -> ; 
Var-declaration-prime -> [ num ] ;
Fun-declaration-prime -> ( Params ) Compound-stmt
Type-specifier -> int
Type-specifier -> void
Params -> int id Param-Prime Param-list
Params -> void Param-list-void-abtar
Param-list-void-abtar -> id Param-prime Param-list
Param-list-void-abtar -> ε
Param-list -> , Param Param-list
Param-list -> ε
Param -> Declaration-initial Param-prime
Param-prime -> ε
Param-prime -> [ ]
Compound-stmt -> { Declaration-list Statement-list }
Statement-list -> Statement Statement-list
Statement-list -> ε
Statement -> Expression-stmt
Statement -> Compound-stmt
Statement -> Selection-stmt
Statement -> Iteration-stmt
Statement -> Return-stmt
Statement -> Switch-stmt
Expression-stmt -> Expression ;
Expression-stmt -> continue ;
Expression-stmt -> break ;
Expression-stmt -> ;
Selection-stmt -> if ( Expression ) Statement else Statement
Iteration-stmt -> while ( Expression ) Statement
Return-stmt -> return Return-stmt-prime
Return-stmt-prime -> ; 
Return-stmt-prime -> Expression ;
Switch-stmt -> switch ( Expression ) { Case-stmts Default-stmt }
Case-stmts -> Case-stmt Case-stmts 
Case-stmts -> ε
Case-stmt -> case num : Statement-list
Default-stmt -> default : Statement-list
Default-stmt -> ε

Expression -> id B
Expression -> Simple-expression-zegond

B -> = Expression
B -> [ Expression ] H
B -> Simple-expression-prime

H -> = Expression
H -> G D C

Simple-expression-zegond -> Additive-expression-zegond C
Simple-expression-prime -> Additive-expression-prime C
C -> Relop Additive-expression
C -> ε

Relop -> ==
Relop -> < 
Addop -> +
Addop -> -

Additive-expression -> Term D
Additive-expression-prime -> Term-prime D
Additive-expression-zegond -> Term-zegond D
D -> Addop Term D
D -> ε

Term -> Signed-factor G
Term-prime -> Signed-factor-prime G
Term-zegond -> Signed-factor-zegond G
G -> * Signed-factor G
G -> ε

Signed-factor -> + Factor
Signed-factor -> - Factor
Signed-factor -> Factor
Signed-factor-prime -> Factor-prime
Signed-factor-zegond -> + Factor
Signed-factor-zegond -> - Factor
Signed-factor-zegond -> Factor-zegond

Factor -> ( Expression )
Factor -> num
Factor -> id Var-call-prime

Var-call-prime -> Var-prime 
Var-call-prime -> ( Args ) 
Var-prime -> [ Expression ]
Var-prime -> ε

Factor-prime -> ( Args )
Factor-prime -> ε


Factor-zegond -> ( Expression )
Factor-zegond -> num

Args -> Arg-list
Args -> ε
Arg-list ->  Expression Arg-list-prime
Arg-list-prime -> , Expression Arg-list-prime
Arg-list-prime -> ε
```

## Example Program:

```C
void main(void) {
    int i;
    i = 1;
    while (i < 10) {
        if (i == 5) {
            break;
        } else {
            output(i);
            i = i + 1;
            continue;
        }
    }

    i = 13234123;
    output(i);
}
```

## Generated Code

```
0	(ASSIGN, #77, 1508)
1	(ASSIGN, #0, 1504)
2	(ASSIGN, #2000, 1500)
3	(ASSIGN, 1500, 500)
4	(ADD, 500, #-1992, 500)
5	(ASSIGN, #1, 504)
6	(ASSIGN, 504, @500)
7	(ASSIGN, #60, 500)
8	(ASSIGN, 1500, 504)
9	(ADD, 504, #-1992, 504)
10	(ASSIGN, #10, 508)
11	(LT, @504, 508, 512)
12	(JPF, 512, 60)
13	(ASSIGN, 1500, 504)
14	(ADD, 504, #-1992, 504)
15	(ASSIGN, #5, 508)
16	(EQ, @504, 508, 516)
17	(JPF, 516, 20)
18	(JP, @500)
19	(JP, 59)
20	(ASSIGN, 1500, 504)
21	(SUB, 504, #1000, 504)
22	(ASSIGN, 500, @504)
23	(ASSIGN, 1500, 504)
24	(SUB, 504, #1004, 504)
25	(ASSIGN, 512, @504)
26	(ASSIGN, 1500, 504)
27	(SUB, 504, #1008, 504)
28	(ASSIGN, 516, @504)
29	(ASSIGN, 1500, 504)
30	(ADD, 504, #-1992, 504)
31	(ASSIGN, 1500, 508)
32	(ASSIGN, @504, @508)
33	(ADD, 1500, #2000, 1500)
34	(ASSIGN, 1500, 504)
35	(ADD, 504, #-1996, 504)
36	(ASSIGN, #38, @504)
37	(ASSIGN, 1500, 504)
38	(ADD, 504, #-2000, 504)
39	(PRINT, @504)
40	(ASSIGN, 1504, 504)
41	(SUB, 1500, #2000, 1500)
42	(ASSIGN, 1500, 508)
43	(SUB, 508, #1000, 508)
44	(ASSIGN, @508, 500)
45	(ASSIGN, 1500, 508)
46	(SUB, 508, #1004, 508)
47	(ASSIGN, @508, 512)
48	(ASSIGN, 1500, 508)
49	(SUB, 508, #1008, 508)
50	(ASSIGN, @508, 516)
51	(ASSIGN, 1500, 504)
52	(ADD, 504, #-1992, 504)
53	(ASSIGN, 1500, 508)
54	(ADD, 508, #-1992, 508)
55	(ASSIGN, #1, 520)
56	(ADD, @508, 520, 524)
57	(ASSIGN, 524, @504)
58	(JP, 8)
59	(JP, 8)
60	(ASSIGN, 1500, 500)
61	(ADD, 500, #-1992, 500)
62	(ASSIGN, #13234123, 504)
63	(ASSIGN, 504, @500)
64	(ASSIGN, 1500, 500)
65	(ADD, 500, #-1992, 500)
66	(ASSIGN, 1500, 504)
67	(ASSIGN, @500, @504)
68	(ADD, 1500, #2000, 1500)
69	(ASSIGN, 1500, 500)
70	(ADD, 500, #-1996, 500)
71	(ASSIGN, #73, @500)
72	(ASSIGN, 1500, 500)
73	(ADD, 500, #-2000, 500)
74	(PRINT, @500)
75	(ASSIGN, 1504, 500)
76	(SUB, 1500, #2000, 1500)
77	(ADD, 1500, 1500, 1500)
```

## Execution Outpu

```
PRINT    1
PRINT    2
PRINT    3
PRINT    4
PRINT    13234123
```




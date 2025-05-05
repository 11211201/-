program         → statement* EOF ;
statement       → varAssign | printStmt | ifStmt | whileStmt | funcDecl | returnStmt | exprStmt ;

varAssign       → "set" IDENTIFIER "=" expression ";" ;
printStmt       → "display" "(" expression ")" ";" ;
ifStmt          → "assuming" expression block ;
whileStmt       → "always" expression block ;
funcDecl        → "magic" IDENTIFIER "(" parameters? ")" block ;
returnStmt      → "return" expression ";" ;

parameters      → IDENTIFIER ("," IDENTIFIER)* ;
arguments       → expression ("," expression)* ;

block           → "{" statement* "}" ;
exprStmt        → expression ";" ;

expression      → assignment ;
assignment      → logic_or ( "=" assignment )? ;
logic_or        → logic_and ( "or" logic_and )* ;
logic_and       → equality ( "and" equality )* ;
equality        → comparison ( ( "==" | "!=" ) comparison )* ;
comparison      → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term            → factor ( ( "+" | "-" ) factor )* ;
factor          → unary ( ( "*" | "/" ) unary )* ;
unary           → ( "-" | "!" ) unary | primary ;
primary         → NUMBER | STRING | "true" | "false" | IDENTIFIER | list | functionCall | "(" expression ")" ;

list            → "[" (expression ("," expression)*)? "]" ;
functionCall    → IDENTIFIER "(" arguments? ")" ;

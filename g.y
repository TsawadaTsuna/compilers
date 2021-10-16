%token NUMBER
%%
statemen: NUMBER '+' NUMBER
    | NUMBER '-' NUMBER
    ;

DEFINE TEMP-TABLE user-list NO-UNDO
    FIELD usr-nr       AS INT FORMAT ">>>" LABEL "No"
    FIELD usr-name     AS CHARACTER FORMAT "x(30)" LABEL "User Name"
    FIELD usr-init     AS CHARACTER FORMAT "x(30)" LABEL "User Initials"
    .

DEFINE OUTPUT PARAMETER TABLE FOR user-list.

DEF VAR nr AS INT.

FOR EACH bediener WHERE bediener.flag EQ 0 NO-LOCK BY bediener.username:
    nr = nr + 1.
    CREATE user-list.
    ASSIGN 
    user-list.usr-nr   = nr
    user-list.usr-name = bediener.username
    user-list.usr-init = bediener.userinit
        .
END.

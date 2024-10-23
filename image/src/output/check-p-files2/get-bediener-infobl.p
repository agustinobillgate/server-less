DEFINE TEMP-TABLE bediener-info
    FIELD user-number   AS INT
    FIELD user-init     AS CHAR
    FIELD user-name     AS CHAR
    FIELD dept-number   AS INT
    FIELD dept-name     AS CHAR
    FIELD email         AS CHAR
    FIELD mobile        AS CHAR
    FIELD pager         AS CHAR.

DEFINE INPUT PARAMETER user-name AS CHAR.
DEFINE INPUT PARAMETER user-init AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR bediener-info.

DEFINE BUFFER buser FOR queasy.
DEFINE BUFFER bdept FOR queasy.

FIND FIRST bediener WHERE bediener.userinit EQ user-init AND bediener.username EQ user-name NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN
DO :
    FIND FIRST buser WHERE buser.KEY EQ 134 AND buser.number1 EQ bediener.nr AND buser.betriebsnr EQ 0 AND buser.deci1 EQ 0 AND buser.logi1 EQ NO USE-INDEX b-num_ix NO-LOCK NO-ERROR.
    FIND FIRST bdept WHERE bdept.KEY EQ 19 AND bdept.number1 EQ bediener.user-group NO-LOCK NO-ERROR.
    CREATE bediener-info.
    ASSIGN
        bediener-info.user-number  = bediener.nr
        bediener-info.user-init    = bediener.userinit
        bediener-info.user-name    = bediener.username
        bediener-info.dept-number  = bediener.user-group
        bediener-info.dept-name    = bdept.char3
        bediener-info.email        = buser.char2
        bediener-info.mobile       = buser.char1
        bediener-info.pager        = buser.char3.
END.


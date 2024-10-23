DEFINE TEMP-TABLE payment-gateway-list
    FIELD pg-art-no         AS INT FORMAT ">>>" LABEL "No"
    FIELD pg-art-name       AS CHARACTER FORMAT "x(35)" LABEL "PG Artikel Name"
    FIELD pg-grp-no         AS INT FORMAT ">>>" LABEL "Group No"
    FIELD pg-grp-name       AS CHARACTER FORMAT "x(35)" LABEL "PG Group Name"
    FIELD pg-art-activate   AS LOGICAL LABEL "Active"
    FIELD vhp-art-no        AS INT FORMAT ">>>" LABEL "VHP Article No"
    FIELD vhp-art-name      AS CHARACTER FORMAT "x(35)" LABEL "VHP Artikel Name" 
    FIELD vhp-art-dept      AS INT
    .
/**/

DEFINE INPUT PARAMETER pg-number AS INT.
DEFINE INPUT PARAMETER department AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR payment-gateway-list.

/* DEF VAR pg-number AS INT INIT 1. */

FOR EACH queasy WHERE queasy.KEY EQ 224 
    AND queasy.number2 EQ department
    AND queasy.number1 EQ pg-number 
    AND queasy.logi1 EQ YES NO-LOCK:
    CREATE payment-gateway-list.
    ASSIGN 
        payment-gateway-list.pg-art-no = INT(ENTRY(1,queasy.char1,"-"))
        payment-gateway-list.pg-art-name = ENTRY(2,queasy.char1,"-").
        IF NUM-ENTRIES(queasy.char2,"-") GE 2 THEN
        DO:
            payment-gateway-list.pg-grp-no = INT(ENTRY(1,queasy.char2,"-")).
            payment-gateway-list.pg-grp-name = ENTRY(2,queasy.char2,"-").
        END.
        ELSE payment-gateway-list.pg-grp-name = queasy.char2.

        payment-gateway-list.pg-art-activate = queasy.logi1.
        IF NUM-ENTRIES(queasy.char3,"-") GE 2 THEN
        DO:
            payment-gateway-list.vhp-art-no = INT(ENTRY(1,queasy.char3,"-")).
            payment-gateway-list.vhp-art-name = ENTRY(2,queasy.char3,"-").
        END.
        payment-gateway-list.vhp-art-dept = queasy.number2
        .
END.

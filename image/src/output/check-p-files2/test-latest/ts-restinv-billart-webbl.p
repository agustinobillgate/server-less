/*FDL Jan 31, 2025 => CHG to webBL for ticket 9DB991*/
DEFINE TEMP-TABLE t-request-list
    FIELD billart   AS INTEGER
    FIELD curr-dept AS INTEGER
    FIELD user-init AS CHARACTER
    .

DEFINE TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE tp-bediener  LIKE bediener.
/* FDL Comment
DEFINE INPUT PARAMETER billart AS INT.
DEFINE INPUT PARAMETER curr-dept AS INT.
*/
DEFINE INPUT PARAMETER TABLE FOR t-request-list.    /*FDL Jan 31, 2025: 9DB991*/
DEFINE OUTPUT PARAMETER price AS DECIMAL.
DEFINE OUTPUT PARAMETER error-message AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-h-artikel.

DEFINE VARIABLE perm    AS INTEGER EXTENT 120 FORMAT "9". 
DEFINE VARIABLE loopn   AS INTEGER NO-UNDO.

FIND FIRST t-request-list NO-ERROR.

FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN 
DO:
    CREATE tp-bediener.
    BUFFER-COPY bediener TO tp-bediener.
END.

FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr EQ t-request-list.billart 
    AND vhp.h-artikel.departement EQ t-request-list.curr-dept 
    AND vhp.h-artikel.activeflag AND vhp.h-artikel.artart EQ 0 NO-LOCK NO-ERROR.
IF AVAILABLE vhp.h-artikel THEN 
DO:
    CREATE t-h-artikel.
    BUFFER-COPY h-artikel TO t-h-artikel.
    ASSIGN t-h-artikel.rec-id = RECID(h-artikel).
    RUN get-price.

    /*FDL Jan 31, 2025: 9DB991*/
    FIND FIRST tp-bediener NO-ERROR.
    DO loopn = 1 TO LENGTH(tp-bediener.permissions):   
        perm[loopn] = INTEGER(SUBSTR(tp-bediener.permissions, loopn, 1)).   
    END.

    FIND FIRST wgrpdep WHERE wgrpdep.zknr EQ t-h-artikel.zwkum
        AND wgrpdep.departement EQ t-h-artikel.departement
        AND wgrpdep.bezeich MATCHES "*DISCOUNT*" NO-LOCK NO-ERROR.
    IF AVAILABLE wgrpdep THEN
    DO:
        IF perm[79] LT 2 THEN
        DO:
            error-message = "Sorry, No Access Right. Access Code = 79,2".
            RETURN.
        END.                    
    END.  
END.

/*************************************** PROCEDURES ***************************************/
PROCEDURE get-price: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE tolerance AS INTEGER. 
DEFINE VARIABLE curr-min AS INTEGER. 
    price = vhp.h-artikel.epreis1. 
    IF vhp.h-artikel.epreis2 = 0 THEN RETURN. 
    FIND FIRST vhp.paramtext WHERE vhp.paramtext.txtnr = (10000 + t-request-list.curr-dept) NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.paramtext THEN 
    DO: 
        tolerance = vhp.paramtext.sprachcode. 
        curr-min = INTEGER(SUBSTR(STRING(time, "HH:MM:SS"),4,2)). 
        i = ROUND((time / 3600 - 0.5), 0). 
        IF i LE 0 THEN i = 24. 
        n = INTEGER(SUBSTR(vhp.paramtext.ptexte, i, 1)). 
        IF n = 2 THEN price = vhp.h-artikel.epreis2. 
        ELSE IF tolerance GT 0 THEN 
        DO: 
            IF i = 1 THEN j = 24. 
            ELSE j = i - 1. 
            IF INTEGER(SUBSTR(vhp.paramtext.ptexte, j, 1)) = 2 
                AND curr-min LE tolerance THEN price = vhp.h-artikel.epreis2. 
        END. 
    END. 
END PROCEDURE. 


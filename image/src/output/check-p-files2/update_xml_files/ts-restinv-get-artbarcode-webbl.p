DEFINE TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INTEGER.

DEFINE INPUT PARAMETER barcode      AS CHARACTER.
DEFINE INPUT PARAMETER table-no     AS INTEGER.
DEFINE INPUT PARAMETER dept-no      AS INTEGER.
DEFINE OUTPUT PARAMETER mess-info   AS CHARACTER.
DEFINE OUTPUT PARAMETER price       AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-h-artikel.

DEFINE VARIABLE billart AS INTEGER.

IF table-no EQ 0 THEN
DO:
    mess-info = "Select a table first.".
    RETURN.
END.
IF barcode EQ ? THEN barcode = "".

FIND FIRST queasy WHERE queasy.key EQ 200 AND queasy.char1 EQ barcode NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND FIRST h-artikel WHERE h-artikel.artnr EQ queasy.number2 
        AND h-artikel.departement EQ queasy.number1         
        AND h-artikel.artart EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE h-artikel THEN 
    DO:
        IF h-artikel.activeflag THEN billart = h-artikel.artnr.
        ELSE
        DO:
            mess-info = "Article is no longer active. Choose another barcode.".
            RETURN.
        END.

        CREATE t-h-artikel.
        BUFFER-COPY h-artikel TO t-h-artikel.
        ASSIGN t-h-artikel.rec-id = RECID(h-artikel).

        RUN get-price.
    END.
END.

PROCEDURE get-price: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE tolerance AS INTEGER. 
DEFINE VARIABLE curr-min AS INTEGER. 
    price = h-artikel.epreis1. 
    IF h-artikel.epreis2 EQ 0 THEN RETURN. 
    FIND FIRST paramtext WHERE paramtext.txtnr EQ (10000 + dept-no) NO-LOCK NO-ERROR. 
    IF AVAILABLE paramtext THEN 
    DO: 
        tolerance = paramtext.sprachcode. 
        curr-min = INTEGER(SUBSTR(STRING(time, "HH:MM:SS"),4,2)). 
        i = ROUND((time / 3600 - 0.5), 0). 
        IF i LE 0 THEN i = 24. 
        n = INTEGER(SUBSTR(paramtext.ptexte, i, 1)). 
        IF n = 2 THEN price = h-artikel.epreis2. 
        ELSE IF tolerance GT 0 THEN 
        DO: 
            IF i = 1 THEN j = 24. 
            ELSE j = i - 1. 
            IF INTEGER(SUBSTR(paramtext.ptexte, j, 1)) = 2 
                AND curr-min LE tolerance THEN price = h-artikel.epreis2. 
        END. 
    END. 
END. 

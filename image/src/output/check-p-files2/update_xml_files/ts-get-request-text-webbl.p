DEFINE TEMP-TABLE t-queasy LIKE queasy.

DEFINE TEMP-TABLE rest-maingroup
    FIELD mg-number AS INTEGER.

DEFINE INPUT PARAMETER article-num  AS INTEGER.
DEFINE INPUT PARAMETER dept-num     AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-queasy.

DEFINE VARIABLE art-mgroup  AS INTEGER NO-UNDO.
DEFINE VARIABLE count-i     AS INTEGER NO-UNDO.
DEFINE VARIABLE count-k     AS INTEGER NO-UNDO.
DEFINE VARIABLE param978    AS CHARACTER NO-UNDO.
DEFINE VARIABLE str-tmp     AS CHARACTER NO-UNDO.
DEFINE VARIABLE curr-tmp    AS CHARACTER NO-UNDO.
DEFINE VARIABLE curr-tmp2   AS CHARACTER NO-UNDO.

DEFINE BUFFER b-queasy FOR queasy.

FIND FIRST h-artikel WHERE h-artikel.artnr EQ article-num
    AND h-artikel.departement EQ dept-num NO-LOCK NO-ERROR.
IF AVAILABLE h-artikel THEN
DO:
    FIND FIRST wgrpgen WHERE wgrpgen.eknr EQ h-artikel.endkum NO-LOCK NO-ERROR.
    IF AVAILABLE wgrpgen THEN art-mgroup = h-artikel.endkum.
END.

FIND FIRST queasy WHERE queasy.KEY EQ 12 AND queasy.number2 EQ art-mgroup NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FOR EACH b-queasy WHERE b-queasy.KEY EQ 12 
        AND (b-queasy.number2 EQ art-mgroup OR b-queasy.number2 EQ 0) NO-LOCK:
        CREATE t-queasy.
        BUFFER-COPY b-queasy TO t-queasy.
    END.
END.
ELSE
DO:
    FOR EACH b-queasy WHERE b-queasy.KEY EQ 12 AND b-queasy.number2 EQ 0 NO-LOCK:
        CREATE t-queasy.
        BUFFER-COPY b-queasy TO t-queasy.
    END.
END.

/*
FIND FIRST htparam WHERE htparam.paramnr EQ 978
    AND htparam.bezeich NE "not used" NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN param978 = htparam.fchar.
IF param978 NE "" THEN
DO:
    DO count-i = 1 TO NUM-ENTRIES(param978, ";"):
        str-tmp = ENTRY(count-i, param978, ";").
        curr-tmp = ENTRY(1,str-tmp,":").

        IF INT(SUBSTR(curr-tmp, 2)) EQ dept-num AND NUM-ENTRIES(str-tmp,":") GT 1 THEN
        DO:
            curr-tmp2 = ENTRY(2,str-tmp,":").
            DO count-k = 1 TO NUM-ENTRIES(curr-tmp2, ","):
                CREATE rest-maingroup.
                rest-maingroup.mg-number = INT(ENTRY(count-k,curr-tmp2,",")).
            END.
        END.        
    END.
END.
*/

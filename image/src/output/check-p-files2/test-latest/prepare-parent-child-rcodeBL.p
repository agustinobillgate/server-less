/*Naufal 210920 - extend field length*/
DEFINE TEMP-TABLE tb1 LIKE queasy
    FIELD parent-code  AS CHAR    FORMAT "x(18)" LABEL "Parent"
    FIELD percent-amt  AS CHAR    FORMAT "x(1)"
    FIELD adjust-value AS DECIMAL FORMAT "->>>,>>9.99"
.
DEF TEMP-TABLE tb2 LIKE tb1.

DEF TEMP-TABLE qbuff
    FIELD char3 AS CHAR.

DEF OUTPUT PARAMETER ci-date AS DATE NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR tb1.
DEF OUTPUT PARAMETER TABLE FOR tb2.

DEF VARIABLE in-percent AS LOGICAL NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ASSIGN ci-date = htparam.fdate.

FOR EACH queasy WHERE queasy.KEY = 2 AND NOT queasy.logi2 
    AND NUM-ENTRIES(queasy.char3, ";") GT 2 NO-LOCK:
  CREATE qbuff.
  qbuff.char3 = queasy.char3.
END.

FOR EACH queasy WHERE queasy.KEY = 2 AND NOT queasy.logi2 NO-LOCK:
    IF NUM-ENTRIES(queasy.char3, ";") GT 2 THEN  /* it is a CHILD */
    DO:
        CREATE tb2.
        BUFFER-COPY queasy TO tb2.
        ASSIGN 
            tb2.parent-code  = ENTRY(2, queasy.char3, ";")
            in-percent       = SUBSTR(ENTRY(3, queasy.char3, ";"),1,1) = "%"
            tb2.adjust-value = DECIMAL(SUBSTR(ENTRY(3, queasy.char3, ";"),2)) / 100
        .
        IF in-percent THEN tb2.percent-amt = "%".
    END.
    ELSE
    DO:
        FIND FIRST qbuff WHERE ENTRY(2, qbuff.char3, ";") = queasy.char1 
            NO-ERROR.
        IF AVAILABLE qbuff THEN
        DO:
            CREATE tb1.
            BUFFER-COPY queasy TO tb1.
        END.
    END.
END.



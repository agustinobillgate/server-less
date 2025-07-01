
DEF INPUT  PARAMETER t-resnr          AS INT.
DEF INPUT  PARAMETER t-resline        AS INT.
DEF OUTPUT PARAMETER t-veran-nr       AS INT.
DEF OUTPUT PARAMETER avail-mainres    AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER resv-datum       AS DATE.

DEFINE BUFFER mainres FOR bk-veran.

FIND FIRST mainres WHERE mainres.veran-nr = t-resnr NO-LOCK NO-ERROR. 
IF AVAILABLE mainres THEN 
DO:
    ASSIGN
        avail-mainres = YES
        t-veran-nr = mainres.veran-nr.
END.

FIND FIRST bk-func WHERE bk-func.veran-nr = t-resnr AND bk-func.veran-seite = t-resline NO-LOCK NO-ERROR.
IF AVAILABLE bk-func THEN
DO:
    resv-datum = bk-func.datum.
END.

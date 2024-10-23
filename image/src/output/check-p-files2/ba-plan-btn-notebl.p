
DEF INPUT  PARAMETER t-resnr        AS INT.
DEF OUTPUT PARAMETER t-veran-nr     AS INT.
DEF OUTPUT PARAMETER avail-mainres  AS LOGICAL INIT NO.

DEFINE BUFFER mainres FOR bk-veran.

FIND FIRST mainres WHERE mainres.veran-nr = t-resnr NO-LOCK NO-ERROR. 
IF AVAILABLE mainres THEN 
DO:
    ASSIGN
        avail-mainres = YES
        t-veran-nr = mainres.veran-nr.
END.

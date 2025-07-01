
DEF INPUT  PARAMETER t-resnr            AS INT.
DEF OUTPUT PARAMETER mainres-gastnr     AS INT.
DEF OUTPUT PARAMETER mainres-veran-nr   AS INT.
DEF OUTPUT PARAMETER mainres-resnr      AS INT.
DEF OUTPUT PARAMETER gast-karteityp     AS INT.
DEF OUTPUT PARAMETER avail-mainres      AS LOGICAL INIT NO.

DEFINE BUFFER mainres FOR bk-veran.
DEFINE BUFFER gast    FOR guest. 

FIND FIRST mainres WHERE mainres.veran-nr = t-resnr NO-LOCK NO-ERROR. 
IF AVAILABLE mainres THEN 
DO:
    ASSIGN
        avail-mainres       = YES
        mainres-gastnr      = mainres.gastnr
        mainres-veran-nr    = mainres.veran-nr
        mainres-resnr       = mainres.resnr.

    FIND FIRST gast WHERE gast.gastnr = mainres.gastnr.
    gast-karteityp = gast.karteityp.
END.

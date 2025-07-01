
DEFINE buffer h-rez FOR h-rezept. 

DEF INPUT PARAMETER katnr AS INT.
DEF OUTPUT PARAMETER avail-h-rez AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER o-bezeich AS CHAR.

FIND FIRST h-rez WHERE h-rez.kategorie = katnr NO-LOCK NO-ERROR. 
IF AVAILABLE h-rez THEN 
DO:
    avail-h-rez = YES.
    o-bezeich   = h-rez.bezeich.
END.

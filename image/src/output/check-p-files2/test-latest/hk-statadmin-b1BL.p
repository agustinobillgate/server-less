
DEF INPUT PARAMETER bediener-nr-stat AS INT.
DEF OUTPUT PARAMETER usrinit AS CHAR.
DEF OUTPUT PARAMETER avail-bediener AS LOGICAL INIT NO.

FIND FIRST bediener WHERE bediener.nr = bediener-nr-stat
  NO-LOCK NO-ERROR. 
IF AVAILABLE bediener THEN 
DO:
    avail-bediener = YES.
    usrinit = bediener.userinit.
END.

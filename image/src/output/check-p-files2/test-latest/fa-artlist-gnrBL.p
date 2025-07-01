
DEF INPUT PARAMETER fa-art-gnr AS CHAR.
DEF OUTPUT PARAMETER grp-bez AS CHAR.
DEF OUTPUT PARAMETER avail-fa-grup AS LOGICAL INIT NO.

FIND FIRST fa-grup WHERE fa-grup.gnr = INTEGER(fa-art-gnr)
  AND fa-grup.flag = 0 NO-LOCK NO-ERROR.
IF AVAILABLE fa-grup THEN 
DO:
    avail-fa-grup = YES.
    grp-bez = fa-grup.bezeich.
END.

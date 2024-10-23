
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER r-kellner AS INT.
DEF INPUT PARAMETER r-kellne1 AS INT.
DEF INPUT PARAMETER t-kellner-nr AS INT.
DEF OUTPUT PARAMETER flag AS INT INIT 0.

FIND FIRST h-bill WHERE h-bill.departement = dept 
  AND h-bill.kellner-nr = t-kellner-nr 
  AND h-bill.flag = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE h-bill THEN 
DO: 
  flag = 1.
END. 
ELSE 
DO: 
    FIND FIRST kellner WHERE RECID(kellner) = r-kellner.
    FIND FIRST kellne1 WHERE RECID(kellne1) = r-kellne1.
    FIND CURRENT kellner EXCLUSIVE-LOCK. 
    delete kellner. 
    FIND CURRENT kellne1 EXCLUSIVE-LOCK. 
    delete kellne1. 
END. 

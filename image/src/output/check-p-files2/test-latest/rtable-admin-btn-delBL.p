
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER t-tischnr AS INT.
DEF OUTPUT PARAMETER flag AS INT INIT 0.

FIND FIRST tisch WHERE tisch.departement = dept
    AND tisch.tischnr = t-tischnr.
FIND FIRST h-bill WHERE h-bill.departement = dept
  AND h-bill.tischnr = t-tischnr NO-LOCK NO-ERROR. 
IF AVAILABLE h-bill THEN flag = 1.
ELSE 
DO: 
  FIND CURRENT tisch EXCLUSIVE-LOCK. 
  delete tisch.
END.

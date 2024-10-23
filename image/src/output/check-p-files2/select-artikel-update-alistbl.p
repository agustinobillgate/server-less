
DEF INPUT  PARAMETER veran-nr    AS INT.
DEF INPUT  PARAMETER veran-seite AS INT.
DEF INPUT  PARAMETER curr-date   AS DATE.
DEF OUTPUT PARAMETER from-i      AS INT.
DEF OUTPUT PARAMETER to-i        AS INT.

FIND FIRST bk-reser WHERE bk-reser.veran-nr = veran-nr  /*MU debug*/
    AND bk-reser.veran-resnr = veran-seite
    AND bk-reser.resstatus LE 3 AND bk-reser.datum = curr-date
    USE-INDEX vernr-ix NO-LOCK .
from-i = bk-reser.von-i. 
to-i = bk-reser.bis-i. 

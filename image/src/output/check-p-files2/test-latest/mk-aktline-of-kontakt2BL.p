
DEF INPUT  PARAMETER akt-line1-gastnr AS INT.
DEF INPUT  PARAMETER kontnr           AS INT.
DEF OUTPUT PARAMETER t-kontakt        AS CHAR.

FIND FIRST akt-kont WHERE akt-kont.gastnr = akt-line1-gastnr 
    AND akt-kont.kontakt-nr = kontnr NO-LOCK NO-ERROR. 
t-kontakt = akt-kont.name + ", " + akt-kont.anrede.

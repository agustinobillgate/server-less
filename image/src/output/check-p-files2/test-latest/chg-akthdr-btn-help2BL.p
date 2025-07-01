
DEF INPUT  PARAMETER guest-gastnr   AS INT.
DEF INPUT  PARAMETER kontnr         AS INT.
DEF OUTPUT PARAMETER namekontakt    AS CHAR.

FIND FIRST akt-kont WHERE akt-kont.gastnr = guest-gastnr 
  AND akt-kont.kontakt-nr = kontnr NO-LOCK. 
namekontakt = akt-kont.name + ", " + akt-kont.vorname 
  + " " + akt-kont.anrede. 

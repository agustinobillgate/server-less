
DEF INPUT  PARAMETER rec-id     AS INTEGER.
DEF INPUT  PARAMETER gastnr     AS INTEGER.
DEF OUTPUT PARAMETER main-kont  AS CHAR.

DEF BUFFER akt-kont1 FOR akt-kont.

FIND FIRST akt-kont1 WHERE akt-kont1.gastnr = gastnr AND 
  akt-kont1.hauptkontakt = YES NO-ERROR. 
IF AVAILABLE akt-kont1 THEN 
DO: 
  akt-kont1.hauptkontakt = NO. 
  FIND CURRENT akt-kont1 NO-LOCK. 
END.
FIND FIRST akt-kont WHERE RECID(akt-kont) = rec-id.
FIND CURRENT akt-kont EXCLUSIVE-LOCK. 
akt-kont.hauptkontakt = YES. 
FIND CURRENT akt-kont NO-LOCK. 
main-kont = akt-kont.name + ", " + akt-kont.vorname + " " + akt-kont.anrede. 

DEFINE INPUT PARAMETER curr-gastnr AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER karteityp  AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER gastnr     AS INTEGER NO-UNDO.


FIND FIRST guest WHERE guest.gastnr = curr-gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE guest THEN
    ASSIGN karteityp = guest.karteityp
           gastnr    = guest.gastnr.

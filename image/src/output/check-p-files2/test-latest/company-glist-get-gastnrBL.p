DEFINE INPUT-OUTPUT PARAMETER from-name AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER curr-gastnr AS INTEGER NO-UNDO.

FIND FIRST guest WHERE guest.NAME = from-name AND guest.gastnr GT 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE guest AND from-name NE "" THEN curr-gastnr = 0.
ELSE
DO:
    ASSIGN
        curr-gastnr = guest.gastnr
        from-name   = guest.NAME.
END.
    

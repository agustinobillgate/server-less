DEFINE TEMP-TABLE tb11
    FIELD gastnr    LIKE guest.gastnr
    FIELD NAME      LIKE guest.NAME
    FIELD CODE      LIKE guest-pr.CODE
.

DEF INPUT PARAMETER prcode AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR tb11.

FOR EACH guest-pr WHERE guest-pr.CODE = prcode
    NO-LOCK, 
    FIRST guest WHERE guest.gastnr = guest-pr.gastnr 
    AND guest.karteityp LE 2 NO-LOCK 
    BY guest.NAME:
    CREATE tb11.
    ASSIGN
        tb11.gastnr = guest.gastnr
        tb11.NAME   = guest.NAME
        tb11.CODE   = prcode
    .
END.

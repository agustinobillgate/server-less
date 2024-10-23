DEFINE TEMP-TABLE t-guest-remark LIKE guest-remark.


DEFINE INPUT PARAMETER inp-gastnr   AS INTEGER   NO-UNDO.
DEFINE OUTPUT PARAMETER guest-name  AS CHARACTER NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER TABLE       FOR t-guest-remark.

FIND FIRST guest WHERE guest.gastnr = inp-gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN
    guest-name = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                + " " + guest.anrede1.

FOR EACH guest-remark WHERE guest-remark.gastnr = inp-gastnr NO-LOCK:
    CREATE t-guest-remark.
    BUFFER-COPY guest-remark TO t-guest-remark.
END.

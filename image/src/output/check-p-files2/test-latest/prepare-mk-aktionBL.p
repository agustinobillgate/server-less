
DEFINE TEMP-TABLE t-guest LIKE guest.

DEF INPUT  PARAMETER inp-gastnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-guest.

FIND FIRST guest WHERE guest.gastnr = inp-gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN
DO :
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.
END.


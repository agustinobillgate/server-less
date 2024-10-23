DEF TEMP-TABLE g-list
    FIELD gastnr AS INTEGER
    FIELD gname AS CHAR FORMAT "x(48)"
.

DEF INPUT PARAMETER gastno       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-kontcode  AS CHAR NO-UNDO.
DEF INPUT PARAMETER TABLE FOR g-list.
DEF OUTPUT PARAMETER kontcode-str AS CHAR NO-UNDO INIT "".


FIND FIRST queasy WHERE queasy.KEY = 147
  AND queasy.number1 = gastno
  AND queasy.char1 = inp-kontcode NO-ERROR.
IF AVAILABLE queasy THEN DELETE queasy.

FOR EACH g-list:
    kontcode-str = kontcode-str + STRING(g-list.gastnr) + ",".
END.

CREATE queasy.
ASSIGN
    queasy.KEY      = 147
    queasy.number1  = gastno
    queasy.char1    = inp-kontcode
    queasy.char3    = kontcode-str
.

FOR EACH kontline WHERE kontline.gastnr = gastno
    AND kontline.kontcode = inp-kontcode:
    kontline.pr-code = kontcode-str.
END.

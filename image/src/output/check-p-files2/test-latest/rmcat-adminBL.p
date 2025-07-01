
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER zikatnr AS INT.
DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "rmcat-admin".

FIND FIRST zimmer WHERE zimmer.zikatnr = zikatnr
    NO-LOCK NO-ERROR.
IF AVAILABLE zimmer THEN
DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("Room under this category exists, deleting not possible.",lvCAREA,"").
END.
ELSE
DO:
 FIND FIRST zimkateg WHERE zimkateg.zikatnr = zikatnr EXCLUSIVE-LOCK NO-ERROR.
 IF AVAILABLE zimkateg THEN delete zimkateg.
END.

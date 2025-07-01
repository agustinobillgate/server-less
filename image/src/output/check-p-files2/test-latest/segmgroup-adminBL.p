
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER int1           AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER char3          AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "segmgroup-admin".


FIND FIRST bediener WHERE bediener.user-group = int1
    AND bediener.flag = 0 NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN
DO:
    hide MESSAGE NO-PAUSE.
    MESSAGE translateExtended ("User exists, deletion not possible.",lvCAREA,"") VIEW-AS ALERT-BOX.
END.
ELSE
DO:
    msg-str = msg-str + CHR(2) + "&Q"
            + translateExtended ("REMOVE the Department",lvCAREA,"")
            + CHR(10)
            + STRING(int1) + " - "
            + char3 + " ?".
END.

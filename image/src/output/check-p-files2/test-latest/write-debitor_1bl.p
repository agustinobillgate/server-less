
DEF INPUT PARAMETER tb-recid   AS INTEGER   NO-UNDO.
DEF INPUT PARAMETER remarks    AS CHARACTER NO-UNDO.

DEF OUTPUT PARAMETER successFlag AS LOGICAL INITIAL YES NO-UNDO.

DEF VAR verscod-str AS CHAR EXTENT 5.
DEF VAR new-verscod AS CHAR.
DEF VAR entries     AS INT.
DEF VAR i           AS INT.

FIND FIRST debitor WHERE RECID(debitor) = tb-recid EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE debitor THEN
DO:
    entries = NUM-ENTRIES(debitor.vesrcod,";").

    IF entries GE 1 THEN
    DO:
        DO i = 1 TO entries:
            verscod-str[i] = ENTRY(i, debitor.vesrcod, ";").
        END.
    
        new-verscod = verscod-str[1] + ";" + remarks + ";".
        IF verscod-str[3] NE "" THEN new-verscod = new-verscod + ";" + verscod-str[3] + ";".
        IF verscod-str[4] NE "" THEN new-verscod = new-verscod + ";" + verscod-str[4] + ";".    
        IF verscod-str[5] NE "" THEN new-verscod = new-verscod + ";" + verscod-str[5] + ";".     
    END.
    ELSE new-verscod = remarks.

    ASSIGN
    debitor.vesrcod    = new-verscod.
    FIND CURRENT debitor.
    RELEASE debitor.
    ASSIGN successFlag = YES.
END.


DEFINE TEMP-TABLE history-list
    FIELD datum AS DATE
    FIELD refno AS CHARACTER
    FIELD bezeich AS CHARACTER
    FIELD timestamp AS INTEGER.

DEFINE INPUT PARAMETER from-date AS DATE NO-UNDO.
DEFINE INPUT PARAMETER to-date AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR history-list.

DEFINE BUFFER bqueasy FOR queasy.

EMPTY TEMP-TABLE history-list.

IF from-date EQ ? AND to-date EQ ? THEN
DO:
    ASSIGN
        to-date = TODAY
        from-date = to-date - 7.
END.

IF to-date - from-date GT 30 THEN
DO:
    MESSAGE "The selected date range cannot exceed 30 days."
        VIEW-AS ALERT-BOX INFO BUTTONS OK.
    RETURN.
END.

FOR EACH bqueasy WHERE bqueasy.KEY EQ 345
    AND bqueasy.date1 GE from-date
    AND bqueasy.date1 LE to-date
    AND bqueasy.logi1 EQ NO
    AND bqueasy.logi2 EQ YES
    AND bqueasy.logi3 EQ NO
    NO-LOCK
    BY bqueasy.date1:

    CREATE history-list.
    ASSIGN
        history-list.datum = bqueasy.date1
        history-list.refno = bqueasy.char1
        history-list.timestamp = bqueasy.number2.

    FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno EQ bqueasy.char1 NO-LOCK NO-ERROR.
    IF AVAILABLE gl-jouhdr THEN
    DO:
        ASSIGN history-list.bezeich = gl-jouhdr.bezeich.
    END.
END.

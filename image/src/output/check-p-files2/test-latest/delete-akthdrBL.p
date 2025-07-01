DEFINE INPUT  PARAMETER case-type    AS INT.
DEFINE INPUT  PARAMETER aktNr        AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST akthdr WHERE akthdr.aktnr = aktnr EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
        IF AVAILABLE akthdr THEN
        DO:
            DELETE akthdr.
            RELEASE akthdr.
            ASSIGN success-flag = YES.
        END.
    END.
END CASE.

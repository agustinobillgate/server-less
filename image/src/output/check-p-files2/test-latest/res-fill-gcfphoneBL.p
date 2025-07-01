
DEF INPUT PARAMETER inp-gastnr AS INT.
DEF INPUT PARAMETER phone-str  AS CHAR.

DO TRANSACTION:
    FIND FIRST guest WHERE guest.gastnr = inp-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN DO:
        FIND CURRENT guest EXCLUSIVE-LOCK.
        guest.mobil-telefon = phone-str.
        FIND CURRENT guest NO-LOCK.
    END.
END.

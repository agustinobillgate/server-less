DEFINE TEMP-TABLE bk-list LIKE bk-raum
    FIELD rec-id    AS INTEGER.

DEFINE INPUT PARAMETER curr-select AS CHARACTER.
DEFINE INPUT PARAMETER t-raum AS CHAR.
DEFINE INPUT PARAMETER TABLE FOR bk-list.
DEFINE OUTPUT PARAMETER recid-raum AS INTEGER.

FIND FIRST bk-list.
IF curr-select = "add" THEN
DO:
    CREATE bk-raum. 
    BUFFER-COPY bk-list TO bk-raum.

    FIND FIRST bk-raum WHERE bk-raum.raum EQ bk-list.raum NO-LOCK NO-ERROR.
    IF AVAILABLE bk-raum THEN recid-raum = RECID(bk-raum).
END.
ELSE IF curr-select = "chg" THEN
DO:
    FIND FIRST bk-raum WHERE bk-raum.raum = t-raum NO-LOCK NO-ERROR.
    FIND CURRENT bk-raum EXCLUSIVE-LOCK.
    BUFFER-COPY bk-list TO bk-raum.
    FIND CURRENT bk-raum NO-LOCK.
END.



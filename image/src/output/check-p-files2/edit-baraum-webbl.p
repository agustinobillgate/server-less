DEFINE TEMP-TABLE t-bk-raum LIKE bk-raum.
DEFINE TEMP-TABLE bk-list LIKE bk-raum
    FIELD rec-id    AS INTEGER.

DEFINE INPUT PARAMETER raum AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR bk-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-bk-raum.

FIND FIRST bk-raum WHERE bk-raum.raum = raum NO-LOCK.
CREATE bk-list.
BUFFER-COPY bk-raum TO bk-list.
ASSIGN bk-list.rec-id = RECID(bk-raum).

FOR EACH bk-raum NO-LOCK:
    CREATE t-bk-raum.
    BUFFER-COPY bk-raum TO t-bk-raum.
END.

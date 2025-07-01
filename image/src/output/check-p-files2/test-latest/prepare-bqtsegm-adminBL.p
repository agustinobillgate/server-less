DEFINE TEMP-TABLE q-list LIKE queasy
    FIELD rec-id AS INT.

DEF OUTPUT PARAMETER TABLE FOR q-list.

FOR EACH queasy WHERE queasy.key = 146 NO-LOCK BY queasy.char1:
    CREATE q-list.
    BUFFER-COPY queasy TO q-list.
    ASSIGN q-list.rec-id = RECID(queasy).
END.

DEF TEMP-TABLE t-ba-typ LIKE ba-typ
    FIELD rec-id AS INT.

DEF OUTPUT PARAMETER TABLE FOR t-ba-typ.

FOR EACH ba-typ NO-LOCK BY ba-typ.typ-id:
    CREATE t-ba-typ.
    BUFFER-COPY ba-typ TO t-ba-typ.
    ASSIGN t-ba-typ.rec-id = RECID(ba-typ).
END.

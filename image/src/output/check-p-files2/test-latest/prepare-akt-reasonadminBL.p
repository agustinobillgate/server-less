
DEF TEMP-TABLE t-akt-code LIKE akt-code
    FIELD rec-id AS INT.

DEF OUTPUT PARAMETER TABLE FOR t-akt-code.

FOR EACH akt-code NO-LOCK BY akt-code.aktionscode:
    CREATE t-akt-code.
    BUFFER-COPY akt-code TO t-akt-code.
    ASSIGN t-akt-code.rec-id = RECID(akt-code).
END.

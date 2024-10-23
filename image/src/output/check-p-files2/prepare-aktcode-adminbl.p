DEF TEMP-TABLE t-akt-code LIKE akt-code
    FIELD recid-akt-code AS INT.

DEF OUTPUT PARAMETER TABLE FOR t-akt-code.

FOR EACH akt-code WHERE akt-code.aktiongrup = 1 
    NO-LOCK BY akt-code.aktionscode:
    CREATE t-akt-code.
    BUFFER-COPY akt-code TO t-akt-code.
    t-akt-code.recid-akt-code = RECID(akt-code).
END.

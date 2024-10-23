
DEFINE TEMP-TABLE t-fa-kateg LIKE fa-kateg
    FIELD rec-id AS INT.

DEF OUTPUT PARAMETER TABLE FOR t-fa-kateg.

FOR EACH fa-kateg NO-LOCK BY fa-kateg.katnr:
    CREATE t-fa-kateg.
    BUFFER-COPY fa-kateg TO t-fa-kateg.
    ASSIGN t-fa-kateg.rec-id = RECID(fa-kateg).
END.


DEF TEMP-TABLE t-mhis-line LIKE mhis-line
    FIELD rec-id AS INT.

DEF INPUT PARAMETER curr-nr AS INT.
DEF OUTPUT PARAMETER b-tittle AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-mhis-line.

FIND FIRST mathis WHERE mathis.nr = curr-nr NO-LOCK.
b-tittle = mathis.name + " - " + b-tittle.

FOR EACH mhis-line WHERE mhis-line.nr = curr-nr NO-LOCK:
    CREATE t-mhis-line.
    BUFFER-COPY mhis-line TO t-mhis-line.
    t-mhis-line.rec-id = RECID(mhis-line).
END.

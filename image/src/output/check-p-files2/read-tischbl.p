DEF TEMP-TABLE t-tisch LIKE tisch.

DEF INPUT PARAMETER i-case  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER dept    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER tableNo AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-tisch.

CASE i-case:
    WHEN 1 THEN
    DO:
        IF dept = 0 THEN
        FOR EACH tisch NO-LOCK BY tisch.departement
            BY tisch.tischnr:
            CREATE t-tisch.
            BUFFER-COPY tisch TO t-tisch.
        END.
        ELSE
        FOR EACH tisch WHERE tisch.departement = dept 
            NO-LOCK BY tisch.tischnr:
            CREATE t-tisch.
            BUFFER-COPY tisch TO t-tisch.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST tisch WHERE tisch.departement = dept
            AND tisch.tischnr = tableNo NO-LOCK NO-ERROR.
        IF AVAILABLE tisch THEN
        DO:
            CREATE t-tisch.
            BUFFER-COPY tisch TO t-tisch.
        END.
    END.
END CASE.


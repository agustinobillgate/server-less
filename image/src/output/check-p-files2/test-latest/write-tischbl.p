DEF TEMP-TABLE t-tisch LIKE tisch.

DEF INPUT PARAMETER i-case      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-dept    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-tisch   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER TABLE FOR t-tisch.

FIND FIRST t-tisch NO-ERROR.
IF NOT AVAILABLE t-tisch THEN RETURN.

CASE i-case:
    WHEN 1 THEN
    DO:
        FOR EACH t-tisch:
          FIND FIRST tisch WHERE tisch.departement = t-tisch.departement
            AND tisch.tischnr = t-tisch.tischnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE tisch THEN
          DO:
            CREATE tisch.
            BUFFER-COPY t-tisch TO tisch.
          END.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST tisch WHERE tisch.departement = inp-dept
            AND tisch.tischnr = inp-tisch NO-LOCK NO-ERROR.
        IF AVAILABLE tisch THEN
        DO:
            FIND CURRENT tisch EXCLUSIVE-LOCK.
            BUFFER-COPY t-tisch TO tisch.
            FIND CURRENT tisch NO-LOCK.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST tisch WHERE tisch.departement = inp-dept
            AND tisch.tischnr = inp-tisch NO-LOCK NO-ERROR.
        IF AVAILABLE tisch THEN
        DO:
            FIND CURRENT tisch EXCLUSIVE-LOCK.
            DELETE tisch.
            RELEASE tisch.
        END.
    END.
END CASE.

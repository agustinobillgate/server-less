DEF TEMP-TABLE t-ekum LIKE ekum.

DEF INPUT PARAMETER case-type AS INT. 
DEF INPUT PARAMETER int1 AS INT.
DEF INPUT PARAMETER int2 AS INT.
DEF INPUT PARAMETER char1 AS CHAR.
DEF INPUT PARAMETER char2 AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-ekum.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST ekum WHERE ekum.eknr = int1 NO-LOCK NO-ERROR. 
        IF AVAILABLE ekum THEN RUN assign-it.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH ekum NO-LOCK:
            RUN assign-it.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST ekum WHERE ekum.bezeich = char1
            AND ekum.eknr NE int1 NO-LOCK NO-ERROR.
        IF AVAILABLE ekum THEN RUN assign-it.
    END.
END CASE.


PROCEDURE assign-it:
    CREATE t-ekum.
    BUFFER-COPY ekum TO t-ekum.
END.

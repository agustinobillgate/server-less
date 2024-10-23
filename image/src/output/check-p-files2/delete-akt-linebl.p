DEFINE INPUT  PARAMETER case-type    AS INT.
DEFINE INPUT  PARAMETER aktNr        AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH akt-line WHERE akt-line.aktnr = aktnr:
            DELETE akt-line.
            RELEASE akt-line.
            ASSIGN success-flag = YES.
        END.
    END.
END CASE.

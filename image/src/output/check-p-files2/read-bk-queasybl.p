DEFINE TEMP-TABLE t-bkqueasy LIKE bk-queasy.


DEFINE INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER int-key   AS INTEGER NO-UNDO.

DEFINE OUTPUT PARAMETER TABLE FOR t-bkqueasy.

CASE case-type:
    WHEN 1 THEN DO:
        FOR EACH bk-queasy WHERE bk-queasy.KEY = int-key NO-LOCK:
            CREATE t-bkqueasy.
            BUFFER-COPY bk-queasy TO t-bkqueasy.
        END.
    END.
END CASE.

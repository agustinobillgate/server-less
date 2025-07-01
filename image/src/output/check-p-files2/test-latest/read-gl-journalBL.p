DEF TEMP-TABLE t-gl-journal LIKE gl-journal
    FIELD b-recid AS INTEGER.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER int1 AS INT.
DEF INPUT PARAMETER int2 AS INT.
DEF INPUT PARAMETER int3 AS INT.
DEF INPUT PARAMETER deci1 AS DECIMAL.
DEF INPUT PARAMETER deci2 AS DECIMAL.
DEF INPUT PARAMETER char1 AS CHAR.
DEF INPUT PARAMETER char2 AS CHAR.
DEF INPUT PARAMETER char3 AS CHAR.
DEF INPUT PARAMETER date1 AS DATE.
DEF INPUT PARAMETER date2 AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-gl-journal.

DEFINE VARIABLE rechnr AS CHARACTER.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST gl-journal WHERE gl-journal.jnr = int1
            NO-LOCK NO-ERROR.
        IF AVAILABLE gl-journal THEN
        DO:
            CREATE t-gl-journal.
            BUFFER-COPY gl-journal TO t-gl-journal.
            ASSIGN t-gl-journal.b-recid = RECID(gl-journal).
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST gl-journal WHERE RECID(gl-journal) = int1
            NO-LOCK NO-ERROR.
        IF AVAILABLE gl-journal THEN
        DO:
            CREATE t-gl-journal.
            BUFFER-COPY gl-journal TO t-gl-journal.
            ASSIGN t-gl-journal.b-recid = RECID(gl-journal).
        END.
    END.
    /* Add by Michael @ 25/07/2019 for project VHP Web - moving delete function into AR Debt List */
    WHEN 3 THEN
    DO:
        /* Oscar (04/03/25) - FB3160 - adjust deleting gl-journal with user-remark */
        FIND FIRST gl-journal WHERE (NUM-ENTRIES(gl-journal.bemerk, "-") GT 0 AND TRIM(ENTRY(1, gl-journal.bemerk, "-")) EQ char1)  
            OR (NUM-ENTRIES(gl-journal.bemerk, "-") EQ 0 AND gl-journal.bemerk EQ char1)
            NO-LOCK NO-ERROR.
        IF AVAILABLE gl-journal THEN
        DO:
            CREATE t-gl-journal.
            BUFFER-COPY gl-journal TO t-gl-journal.
            ASSIGN t-gl-journal.b-recid = RECID(gl-journal).
        END.
    END.
    /* End of modify */
END CASE.

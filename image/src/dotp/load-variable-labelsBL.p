/* 
Purpose: To load all or a part of labgels / languages related to 
         one country-id or two country-id for editing purpose
*/

DEFINE TEMP-TABLE country-labels
    FIELD program-variable AS CHAR
    FIELD program-label1   AS CHAR INIT ""
    FIELD program-label2   AS CHAR INIT ""
    FIELD remark           AS CHAR
    FIELD s-recid1         AS INTEGER INIT 0
    FIELD s-recid2         AS INTEGER INIT 0
    FIELD created-id1      AS CHAR INIT ""
    FIELD created-date1    AS DATE
    FIELD created-time1    AS INTEGER INIT 0
    FIELD lastchg-id1      AS CHAR INIT ""
    FIELD lastchg-date1    AS DATE
    FIELD lastchg-time1    AS INTEGER INIT 0
    FIELD created-id2      AS CHAR INIT ""
    FIELD created-date2    AS DATE
    FIELD created-time2    AS INTEGER INIT 0
    FIELD lastchg-id2      AS CHAR INIT ""
    FIELD lastchg-date2    AS DATE
    FIELD lastchg-time2    AS INTEGER INIT 0
    INDEX variable_ix program-variable
.

DEFINE INPUT PARAMETER country-id1  AS CHAR NO-UNDO. /* 1st language  */
DEFINE INPUT PARAMETER country-id2  AS CHAR NO-UNDO. /* 2nd language  */
DEFINE INPUT PARAMETER inp-variable AS CHAR NO-UNDO. 
DEFINE OUTPUT PARAMETER TABLE FOR country-labels.

IF inp-variable NE "" THEN 
DO:
    RUN load-partial-languages.
    RETURN.
END.

FOR EACH countries-lang WHERE countries-lang.country-id EQ country-id1 NO-LOCK:
    FIND FIRST lang-remark WHERE lang-remark.lang-variable EQ countries-lang.lang-variable NO-LOCK NO-ERROR.
    CREATE country-labels.
    ASSIGN
        country-labels.program-variable = countries-lang.lang-variable
        country-labels.program-label1   = countries-lang.lang-value
        country-labels.s-recid1         = RECID(countries-lang)
        country-labels.created-id1      = countries-lang.created-id
        country-labels.created-date1    = countries-lang.created-date
        country-labels.created-time1    = countries-lang.created-time
        country-labels.lastchg-id1      = countries-lang.lastchg-id
        country-labels.lastchg-date1    = countries-lang.lastchg-date
        country-labels.lastchg-time1    = countries-lang.lastchg-time
    .
    IF AVAILABLE lang-remark THEN
    country-labels.remark = lang-remark.remark.
END.

IF country-id2 NE "" THEN
FOR EACH countries-lang WHERE 
    countries-lang.country-id = country-id2 NO-LOCK:
    FIND FIRST country-labels WHERE country-labels.program-variable EQ countries-lang.lang-variable NO-ERROR.
    IF NOT AVAILABLE country-labels THEN
    DO:
        FIND FIRST lang-remark WHERE lang-remark.lang-variable EQ countries-lang.lang-variable NO-LOCK NO-ERROR.
        CREATE country-labels.
        ASSIGN country-labels.program-variable = countries-lang.lang-variable.
        IF AVAILABLE lang-remark THEN country-labels.remark = lang-remark.remark.
    END.
    ASSIGN 
        country-labels.program-label2 = countries-lang.lang-value
        country-labels.s-recid2       = RECID(countries-lang)
        country-labels.created-id2    = countries-lang.created-id
        country-labels.created-date2  = countries-lang.created-date
        country-labels.created-time2  = countries-lang.created-time
        country-labels.lastchg-id2    = countries-lang.lastchg-id
        country-labels.lastchg-date2  = countries-lang.lastchg-date
        country-labels.lastchg-time2  = countries-lang.lastchg-time
    .
END.

PROCEDURE load-partial-languages:
    ASSIGN inp-variable = "*" + inp-variable + "*".
    FOR EACH countries-lang WHERE countries-lang.lang-variable MATCHES inp-variable 
        AND ((countries-lang.country-id = country-id1) OR (countries-lang.country-id = country-id2))
        NO-LOCK BY countries-lang.lang-variable:
        FIND FIRST country-labels WHERE country-labels.program-variable EQ countries-lang.lang-variable NO-ERROR.
        IF NOT AVAILABLE country-labels THEN
        DO:
            FIND FIRST lang-remark WHERE lang-remark.lang-variable EQ countries-lang.lang-variable NO-LOCK NO-ERROR.
            CREATE country-labels.
            ASSIGN country-labels.program-variable = countries-lang.lang-variable.
            IF AVAILABLE lang-remark THEN
            country-labels.remark = lang-remark.remark.
        END.
        IF countries-lang.country-id = country-id1 THEN
        ASSIGN
            country-labels.program-label1 = countries-lang.lang-value
            country-labels.s-recid1       = RECID(countries-lang)
            country-labels.created-id1    = countries-lang.created-id
            country-labels.created-date1  = countries-lang.created-date
            country-labels.created-time1  = countries-lang.created-time
            country-labels.lastchg-id1    = countries-lang.lastchg-id
            country-labels.lastchg-date1  = countries-lang.lastchg-date
            country-labels.lastchg-time1  = countries-lang.lastchg-time
        .
        ELSE
        ASSIGN
            country-labels.program-label2 = countries-lang.lang-value
            country-labels.s-recid1       = RECID(countries-lang)
            country-labels.created-id2    = countries-lang.created-id
            country-labels.created-date2  = countries-lang.created-date
            country-labels.created-time2  = countries-lang.created-time
            country-labels.lastchg-id2    = countries-lang.lastchg-id
            country-labels.lastchg-date2  = countries-lang.lastchg-date
            country-labels.lastchg-time2  = countries-lang.lastchg-time
        .
    END.
END.

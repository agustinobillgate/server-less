DEFINE TEMP-TABLE payload-list
    FIELD dml-no       AS CHARACTER
    FIELD dept-no      AS INTEGER
    FIELD datum        AS CHARACTER
    FIELD remark       AS CHARACTER
.

DEFINE TEMP-TABLE response-list
    FIELD success-flag AS LOGICAL
.

DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR response-list.

DEFINE VARIABLE dml-no     AS CHARACTER.
DEFINE VARIABLE dept-no    AS INTEGER.
DEFINE VARIABLE datum      AS CHARACTER.
DEFINE VARIABLE datum-date AS DATE.
DEFINE VARIABLE remark     AS CHARACTER.

CREATE response-list.

response-list.success-flag = NO.

FIND FIRST payload-list NO-LOCK NO-ERROR.
IF AVAILABLE payload-list THEN
DO:
    ASSIGN
        dml-no  = payload-list.dml-no
        dept-no = payload-list.dept-no
        datum   = payload-list.datum
        remark  = payload-list.remark
    .

    datum-date = DATE(INT(SUBSTR(datum,1,2)), INT(SUBSTR(datum,4,2)), INT(SUBSTR(datum,7,2))).

    IF dml-no EQ "" THEN
        dml-no = "D" + STRING(dept-no, "99") + SUBSTR(datum,7,2) 
               + SUBSTR(datum,1,2) + SUBSTR(datum,4,2) + STRING(1, "999").

    FIND FIRST queasy WHERE queasy.KEY EQ 342
        AND queasy.char1 EQ dml-no
        AND queasy.number1 EQ dept-no NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.

        ASSIGN
            queasy.char1   = dml-no
            queasy.number1 = dept-no
            queasy.date1   = datum-date
            queasy.char2   = remark
        .

        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.

        response-list.success-flag = YES.
    END.
    ElSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY     = 342
            queasy.char1   = dml-no
            queasy.number1 = dept-no
            queasy.date1   = datum-date
            queasy.char2   = remark
        .
        
        response-list.success-flag = YES.
    END.
END.

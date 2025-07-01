DEFINE TEMP-TABLE sduration
    FIELD Duration-nr  AS INTEGER
    FIELD time-str AS CHAR FORMAT "X(100)".

DEFINE TEMP-TABLE duration LIKE eg-Duration.

DEF INPUT PARAMETER TABLE FOR duration.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR sduration.

DEF BUFFER queasy1 FOR eg-Duration.

FIND FIRST duration.
IF case-type = 1 THEN   /*MT add */
DO:
    FIND FIRST queasy1 WHERE queasy1.Duration-nr = duration.Duration-nr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy1 THEN
    DO:
        fl-code = 1.
    END.
    ELSE
    DO:
        /* Malik Serverless 803 change 
        - queasy1.DAY -> queasy1.days 
        - duration.DAY -> duration.days*/
        FIND FIRST queasy1 WHERE queasy1.days = duration.days AND queasy1.hour = duration.hour AND
            queasy1.minute = duration.minute NO-LOCK NO-ERROR.
        IF AVAILABLE queasy1 THEN
        DO:
            fl-code = 2.
        END.
        ELSE
        DO:
            CREATE eg-Duration.  
            RUN fill-new-queasy.  
            RELEASE eg-duration.
            fl-code = 3.
            RUN create-duration.
        END.
    END.   
END.

ELSE IF case-type = 2 THEN   /*MT chg */
DO:
    FIND FIRST eg-Duration WHERE RECID(eg-Duration) = rec-id NO-LOCK NO-ERROR. /* Malik Serverless 803 add if available */
    IF AVAILABLE eg-Duration THEN
    DO:
        FIND FIRST queasy1 WHERE queasy1.Duration-nr = duration.Duration-nr AND ROWID(queasy1) NE ROWID(eg-Duration) NO-LOCK NO-ERROR.
        IF AVAILABLE queasy1 THEN
        DO:
            fl-code = 1.
        END.
        ELSE
        DO:
            FIND FIRST queasy1 WHERE queasy1.days = duration.days AND queasy1.hour = duration.hour AND
                queasy1.minute = duration.minute AND ROWID(queasy1) NE ROWID(eg-Duration) NO-LOCK NO-ERROR.
            IF AVAILABLE queasy1 THEN
            DO:
                fl-code = 2.
            END.
            ELSE
            DO:
                FIND CURRENT eg-Duration EXCLUSIVE-LOCK.  
                eg-Duration.Duration-nr = duration.Duration-nr.
                eg-Duration.days     = duration.days.
                eg-Duration.hour    = duration.hour.
                eg-Duration.minute  = duration.minute.

                FIND CURRENT eg-Duration NO-LOCK . 
                RELEASE eg-Duration.
                fl-code = 3.
                RUN create-duration.
            END.
        END.
    END.
END.


PROCEDURE fill-new-queasy:
        eg-Duration.Duration-nr = duration.duration-nr. /* Malik Serverless 803 change Duration-nr -> duration-nr  */
        eg-Duration.days     = duration.days. /* Malik Serverless 803 DAY -> days  */
        eg-Duration.hour    = duration.hour.
        eg-Duration.minute  = duration.minute.  
END.  


PROCEDURE create-duration:
    DEF BUFFER qbuff FOR eg-Duration.
    DEF VAR str AS CHAR NO-UNDO.
    DEF VAR tmp-days AS INT NO-UNDO.

    FOR EACH sduration:
        DELETE sduration.
    END.
    
    /* Malik Serverless 803 comment 
    FOR EACH qbuff NO-LOCK BY qbuff.Duration-nr:
        IF qbuff.DAY = 0 THEN
        DO:
            str = "".
        END.
        ELSE 
        DO:
            str = string(qbuff.DAY).
            IF qbuff.DAY > 1 THEN str = str + " days ".
            ELSE str = str + " day ".
        END.

        IF qbuff.hour = 0 THEN
        DO:
            str = str.
        END.
        ELSE 
        DO:
            str = str + string(qbuff.hour).
            IF qbuff.hour > 1 THEN str = str + " hrs ".
            ELSE str = str + " hr ".
        END.

        IF qbuff.minute = 0 THEN
        DO:
            str = str .
        END.
        ELSE 
        DO:
            str = str + string(qbuff.minute) + " min ".
        END.

        CREATE sduration.
        ASSIGN sduration.Duration-nr  = qbuff.Duration-nr
               sduration.time-str = str.
    END.*/

    /* Malik Serverless 803 change
    - qbuff.DAY -> qbuff.days'
    - qbuff.Duration-nr -> qbuff.duration-nr  */
    FOR EACH qbuff NO-LOCK BY qbuff.duration-nr:
        tmp-days = INT(qbuff.days). /* Malik Serverless 803 convert to int cause in python the value is string  */
        IF tmp-days = 0 THEN
        DO:
            str = "".
        END.
        ELSE 
        DO:
            str = string(tmp-days).
            IF tmp-days > 1 THEN str = str + " days ".
            ELSE str = str + " day ".
        END.

        IF qbuff.hour = 0 THEN
        DO:
            str = str.
        END.
        ELSE 
        DO:
            str = str + string(qbuff.hour).
            IF qbuff.hour > 1 THEN str = str + " hrs ".
            ELSE str = str + " hr ".
        END.

        IF qbuff.minute = 0 THEN
        DO:
            str = str .
        END.
        ELSE 
        DO:
            str = str + string(qbuff.minute) + " min ".
        END.

        CREATE sduration.
        ASSIGN sduration.Duration-nr  = qbuff.duration-nr
               sduration.time-str = str.
    END.
END.

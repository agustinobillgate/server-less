DEFINE TEMP-TABLE log-list
    FIELD log-recid   AS INT
    FIELD send-date   AS DATE LABEL "Sent Date"
    FIELD report-name AS CHAR FORMAT "x(40)" LABEL "Report Name"
    FIELD send-status AS LOGICAL LABEL "Sent Status"
    FIELD send-result AS CHAR FORMAT "x(30)" LABEL "Sent Result"
    FIELD report-no   AS INT
    .

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER log-recid AS INT.
DEFINE INPUT PARAMETER month-val AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR log-list.

IF case-type EQ 1 THEN /*TRIGGER FOR RESEND DATA*/
DO:
    FIND FIRST queasy WHERE RECID(queasy) EQ log-recid NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN 
            queasy.logi1 = NO.

        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
END.

FOR EACH queasy WHERE queasy.KEY EQ 347 
    AND queasy.betriebsnr EQ 2 
    AND queasy.number1 EQ month-val
    AND queasy.number2 EQ YEAR(TODAY) NO-LOCK:
    CREATE log-list.
    ASSIGN 
        log-list.log-recid   = RECID(queasy)
        log-list.send-date   = queasy.date1  
        log-list.report-name = queasy.char1  
        log-list.send-status = queasy.logi1  
        log-list.send-result = queasy.char2
        log-list.report-no   = queasy.number3
        .
END.

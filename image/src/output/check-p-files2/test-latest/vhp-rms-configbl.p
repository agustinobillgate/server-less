DEFINE TEMP-TABLE report-list
    FIELD nr            AS INT FORMAT ">>>" LABEL "No"
    FIELD report-name   AS CHARACTER FORMAT "x(40)" LABEL "Report Name"
    FIELD activate-flag AS LOGICAL LABEL "Active"
    FIELD activate-date AS DATE LABEL "Active Date".

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR report-list.

DEFINE VARIABLE loop-i AS INT.
DEFINE VARIABLE rpt-list AS CHAR EXTENT 14.
rpt-list[1]  = "Master Data".
rpt-list[2]  = "Room Overview".
rpt-list[3]  = "Room Availability".
rpt-list[4]  = "Monthly Forecast Of Room Occupancy".
rpt-list[5]  = "Forecast Room Production".
rpt-list[6]  = "Future Booking".
rpt-list[7]  = "Reservation By Creation Date".
rpt-list[8]  = "Inhouse Guest List".
rpt-list[9]  = "Cancelled Reservation".
rpt-list[10] = "Room Revenue Breakdown".
rpt-list[11] = "Front Office Turnover Report".
rpt-list[12] = "Company Room Production".
rpt-list[13] = "Travel Agent Room Production".
rpt-list[14] = "Room Recapitulation With Guest Segment".

IF case-type EQ 1 THEN /*LOAD DATA*/
DO:
    DO loop-i = 1 TO 14:
        FIND FIRST queasy WHERE queasy.KEY EQ 347
            AND queasy.betriebsnr EQ 1
            AND queasy.number1 EQ loop-i NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY        = 347
                queasy.betriebsnr = 1
                queasy.number1    = loop-i
                queasy.char1      = rpt-list[loop-i]
                queasy.logi1      = NO
                queasy.date1      = ?.
        END.
    END.
END.
ELSE IF case-type EQ 2 THEN /*UPDATE DATA*/
DO:
    FOR EACH report-list:
        FIND FIRST queasy WHERE queasy.KEY EQ 347
            AND queasy.betriebsnr EQ 1
            AND queasy.number1 EQ report-list.nr NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            IF report-list.activate-flag NE queasy.logi1 THEN
            DO:
                FIND CURRENT queasy EXCLUSIVE-LOCK.
                ASSIGN 
                    queasy.logi1    = report-list.activate-flag
                    queasy.date1    = TODAY.
                    .  
                FIND CURRENT queasy NO-LOCK.
            END.
            RELEASE queasy.
        END.
    END.
END.
EMPTY TEMP-TABLE report-list.
FOR EACH queasy WHERE queasy.KEY EQ 347 AND queasy.betriebsnr EQ 1 NO-LOCK:
    CREATE report-list.
    ASSIGN 
        report-list.nr            = queasy.number1
        report-list.report-name   = queasy.char1  
        report-list.activate-flag = queasy.logi1  
        report-list.activate-date = queasy.date1.  
END.



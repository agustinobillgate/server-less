DEFINE TEMP-TABLE release-table                     
    FIELD dept      AS INT FORMAT "99" LABEL "Dept"
    FIELD tableno   AS INT FORMAT ">>>>" LABEL "Table"
    FIELD pax       AS INT FORMAT ">>>" LABEL "Pax"
    FIELD gname     AS CHAR FORMAT "x(25)" LABEL "Guest Name"
    FIELD occupied  AS LOGICAL LABEL "Occupied"
    FIELD session-parameter AS CHAR
    FIELD gemail    AS CHAR
    FIELD expired-session AS LOGICAL
    FIELD dataQR AS CHAR
    FIELD date-time AS DATETIME FORMAT "99/99/99 HH:MM:SS" LABEL "Picked Datetime"
    .

DEFINE INPUT PARAMETER TABLE FOR release-table.
DEFINE INPUT PARAMETER dynamic-qr AS LOGICAL.
DEFINE INPUT PARAMETER asroom-service AS LOGICAL.
DEFINE OUTPUT PARAMETER error-msg AS CHARACTER INITIAL "".

FIND FIRST release-table.
IF NOT AVAILABLE release-table THEN RETURN.

DEFINE VARIABLE count-i         AS INTEGER.
DEFINE VARIABLE bill-no         AS INTEGER INITIAL 0.
DEFINE VARIABLE dept-no         AS INTEGER.
DEFINE VARIABLE table-no        AS INTEGER.
DEFINE VARIABLE session-params  AS CHARACTER.
DEFINE VARIABLE mess-str        AS CHARACTER.
DEFINE VARIABLE mess-token      AS CHARACTER.
DEFINE VARIABLE mess-keyword    AS CHARACTER.
DEFINE VARIABLE mess-value      AS CHARACTER.
DEFINE VARIABLE date-time       AS DATETIME.

DEFINE BUFFER buff-orderbill FOR queasy.
DEFINE BUFFER pickup-table FOR queasy.
DEFINE BUFFER q-orderbill FOR queasy.
DEFINE BUFFER q-searchbill FOR queasy.
DEFINE BUFFER q-orderbill-line FOR queasy.
DEFINE BUFFER q-search-orderbill-line FOR queasy.

ASSIGN
    dept-no         = release-table.dept   
    table-no        = release-table.tableno
    session-params  = release-table.session-parameter
    date-time       = release-table.date-time
.

IF dynamic-qr THEN
DO:
    RUN dynamic-release.
END.
ELSE    /*STATIC QR*/
DO:
    RUN static-release.    
END.

/*******************************************************************************************************/

PROCEDURE dynamic-release:
    FIND FIRST queasy WHERE queasy.KEY EQ 230
        AND queasy.number1 EQ dept-no
        AND queasy.number2 EQ table-no
        AND queasy.char1 EQ session-params NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        /*Check OrderBill For Posted Cancel Order*/  
        FOR EACH q-searchbill WHERE q-searchbill.KEY EQ 225
            AND q-searchbill.char1 EQ "orderbill"
            AND q-searchbill.number1 EQ dept-no
            AND q-searchbill.number2 EQ table-no
            AND q-searchbill.logi1 EQ YES
            AND q-searchbill.char3 EQ session-params
            AND NUM-ENTRIES(q-searchbill.char2, "|") LE 7 NO-LOCK:

            IF NOT q-searchbill.logi3 THEN
            DO:
                error-msg = "Please make sure ALL Cancel Order is Posted.".
                RETURN.
            END.
        END.

         /*Check All Order Bill, Update Logi1 and Char3*/
        FIND FIRST q-orderbill WHERE q-orderbill.KEY EQ 225
            AND q-orderbill.char1 EQ "orderbill"
            AND q-orderbill.number1 EQ dept-no
            AND q-orderbill.number2 EQ table-no
            AND q-orderbill.logi1 EQ YES
            AND q-orderbill.logi3 EQ YES
            AND q-orderbill.char3 EQ session-params
            AND NUM-ENTRIES(q-orderbill.char2, "|") LE 7 NO-LOCK NO-ERROR.
        IF AVAILABLE q-orderbill THEN
        DO:
            FOR EACH q-orderbill WHERE q-orderbill.KEY EQ 225
                AND q-orderbill.char1 EQ "orderbill"
                AND q-orderbill.number1 EQ dept-no
                AND q-orderbill.number2 EQ table-no
                AND q-orderbill.logi1 EQ YES
                AND q-orderbill.logi3 EQ YES
                AND q-orderbill.char3 EQ session-params
                AND NUM-ENTRIES(q-orderbill.char2, "|") LE 7 EXCLUSIVE-LOCK:
                
                ASSIGN
                    q-orderbill.logi1 = NO
                    q-orderbill.char3 = q-orderbill.char3 + "T" 
                        + REPLACE(STRING(TODAY),"/","") 
                        + REPLACE(STRING(TIME,"HH:MM"),":","")
                        + ";" + "1-GLFT"
                    .                
            END.
        END.        

        /*SEARCH TAKEN TABLE QUEASY AND UPDATE THE FIELDS*/
        FIND FIRST pickup-table WHERE pickup-table.KEY EQ 225
            AND pickup-table.char1 EQ "taken-table"
            AND pickup-table.number1 EQ dept-no
            AND pickup-table.number2 EQ table-no
            AND pickup-table.logi1 EQ YES   
            AND pickup-table.logi2 EQ YES
            AND ENTRY(1, pickup-table.char3, "|") EQ session-params EXCLUSIVE-LOCK.
        IF AVAILABLE pickup-table THEN
        DO:                     
            ASSIGN
                ENTRY(1, pickup-table.char3, "|") = session-params + "T" 
                    + REPLACE(STRING(TODAY),"/","") 
                    + REPLACE(STRING(TIME,"HH:MM"),":","")
                    + ";" + "1-GLFT"
                .                      
        END.         

        FIND CURRENT queasy EXCLUSIVE-LOCK.
        queasy.logi1 = YES.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.

        error-msg = "Table Released.".
    END.
END PROCEDURE.

PROCEDURE static-release:
    FIND FIRST queasy WHERE queasy.KEY EQ 225
        AND queasy.char1 EQ "orderbill"
        AND queasy.number1 EQ dept-no
        AND queasy.number2 EQ table-no
        AND queasy.logi1 EQ YES
        AND queasy.logi3 EQ YES
        AND queasy.char3 EQ session-params
        AND NUM-ENTRIES(queasy.char2, "|") LE 7 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:        
        /*Check OrderBill For Posted Cancel Order*/  
        FOR EACH q-searchbill WHERE q-searchbill.KEY EQ 225
            AND q-searchbill.char1 EQ "orderbill"
            AND q-searchbill.number1 EQ dept-no
            AND q-searchbill.number2 EQ table-no
            AND q-searchbill.logi1 EQ YES
            AND q-searchbill.char3 EQ session-params
            AND NUM-ENTRIES(q-searchbill.char2, "|") LE 7 NO-LOCK:

            IF NOT q-searchbill.logi3 THEN
            DO:
                error-msg = "Please make sure ALL Cancel Order is Posted.".
                RETURN.
            END.
        END.

        /*Check All Order Bill, Update Logi1 and Char3*/
        FOR EACH q-orderbill WHERE q-orderbill.KEY EQ 225
            AND q-orderbill.char1 EQ "orderbill"
            AND q-orderbill.number1 EQ dept-no
            AND q-orderbill.number2 EQ table-no
            AND q-orderbill.logi1 EQ YES
            AND q-orderbill.logi3 EQ YES
            AND q-orderbill.char3 EQ session-params
            AND NUM-ENTRIES(q-orderbill.char2, "|") LE 7 EXCLUSIVE-LOCK:

            /*Check All Order Bill Line, Update Char2*/
            FOR EACH q-orderbill-line WHERE q-orderbill-line.KEY EQ 225
                AND q-orderbill-line.char1 EQ "orderbill-line"
                AND q-orderbill-line.number1 EQ q-orderbill.number3
                AND q-orderbill-line.number2 EQ table-no
                AND INT(ENTRY(1, q-orderbill-line.char2, "|")) EQ dept-no
                AND ENTRY(4, q-orderbill-line.char2, "|") EQ session-params
                AND q-orderbill-line.logi2 EQ NO
                AND q-orderbill-line.logi3 EQ NO EXCLUSIVE-LOCK:

                ASSIGN
                    q-orderbill-line.char2 = ENTRY(1, q-orderbill-line.char2,"|") + "|" 
                        + ENTRY(2, q-orderbill-line.char2,"|") + "|"
                        + ENTRY(3, q-orderbill-line.char2,"|") + "|"
                        + session-params + "T" + REPLACE(STRING(TODAY),"/","") 
                        + REPLACE(STRING(TIME,"HH:MM"),":","")
                        + ";" + "1-GLFT"
                    .                
            END.

            ASSIGN
                q-orderbill.logi1 = NO
                q-orderbill.char3 = q-orderbill.char3 + "T" 
                    + REPLACE(STRING(TODAY),"/","") 
                    + REPLACE(STRING(TIME,"HH:MM"),":","")
                    + ";" + "1-GLFT"
                .            
        END.
        error-msg = "Table Released.".
    END.
    ELSE
    DO:
        error-msg = "Please make sure Cancel Order is Posted.".
        RETURN.
    END.
END PROCEDURE.

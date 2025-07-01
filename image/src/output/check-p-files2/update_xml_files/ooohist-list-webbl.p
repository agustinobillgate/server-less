DEFINE TEMP-TABLE output-list
    FIELD roomno        AS CHARACTER FORMAT "x(6)"       
    FIELD roomtype      AS CHARACTER FORMAT "x(34)"      
    FIELD reason        AS CHARACTER FORMAT "x(80)"      
    FIELD from-date     AS DATE      FORMAT "99/99/9999" 
    FIELD to-date       AS DATE      FORMAT "99/99/9999" 
    FIELD sysdate       AS DATE      FORMAT "99/99/9999" 
    FIELD userinit      AS CHAR 
.
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date AS DATE.
DEFINE INPUT PARAMETER rmNo    AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE curr-date AS DATE.
DEFINE VARIABLE num-day AS INTEGER.
num-day = to-date - from-date.

FOR EACH output-list:
    DELETE output-list.
END.
/* FDL Comment
FOR EACH queasy WHERE queasy.KEY = 900
    AND /*queasy.date1*/ queasy.date3 GE from-date
    AND /*queasy.date1*/ queasy.date3 LE to-date NO-LOCK BY queasy.date1:
    FIND FIRST zimmer WHERE zimmer.zikatnr EQ queasy.number1 NO-LOCK NO-ERROR.
    IF AVAILABLE zimmer THEN
    DO:
        CREATE output-list.
        ASSIGN 
            output-list.roomno     = queasy.char1 
            output-list.roomtype   = zimmer.bezeich
            output-list.reason     = ENTRY(1,queasy.char2,"$")
            output-list.from-date  = queasy.date2  
            output-list.to-date    = queasy.date3  
            output-list.sysdate    = queasy.date1  
            output-list.userinit   = queasy.char3
            .                        
    END.
END.
*/

/* FDL April 06, 2023 => Ticket 2507F0
DO curr-date = from-date TO to-date:
    FOR EACH queasy WHERE queasy.KEY EQ 900
        AND (queasy.date2 GE curr-date AND queasy.date2 LE curr-date) 
        /* OR (queasy.date2 LE curr-date AND queasy.date3 GE curr-date) */ NO-LOCK USE-INDEX queasychr2_ix  BY queasy.date1 /**/:
        IF rmNo NE "" AND rmNo NE ? THEN
        DO:
            FIND FIRST zimmer WHERE zimmer.zikatnr EQ queasy.number1 AND zimmer.zinr = rmNo NO-LOCK NO-ERROR.
        END.
        ELSE
        DO:
            /* Debugging 
            message
                "bukan rmNO"
                view-as alert-box. */
            FIND FIRST zimmer WHERE zimmer.zikatnr EQ queasy.number1 NO-LOCK NO-ERROR.
        END.
        /* Debugging 
        message
            "infoo <<<<"
            view-as alert-box. */
        IF AVAILABLE zimmer THEN
        DO:
            /* Debugging 
            message
                "ada zimmer <<<<<"
                view-as alert-box. */
            FIND FIRST output-list WHERE output-list.roomno EQ queasy.char1
                AND output-list.from-date EQ queasy.date2
                AND output-list.to-date EQ queasy.date3 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE output-list THEN
            DO:
                /* Debugging 
                message
                    "test <<<<<<"
                    view-as alert-box. */
                CREATE output-list.
                ASSIGN 
                    output-list.roomno     = queasy.char1 
                    output-list.roomtype   = zimmer.bezeich
                    output-list.reason     = ENTRY(1,queasy.char2,"$")
                    output-list.from-date  = queasy.date2  
                    output-list.to-date    = queasy.date3  
                    output-list.sysdate    = queasy.date1  
                    output-list.userinit   = queasy.char3
                    . 
            END.                                  
        END.
    END.
END.
*/
IF (rmNo NE "" AND rmNo NE ?) OR num-day GE 730 THEN
DO:
    FOR EACH queasy WHERE queasy.KEY = 900
        AND /*queasy.date1*/ queasy.date3 GE from-date
        AND /*queasy.date1*/ queasy.date3 LE to-date NO-LOCK BY queasy.date1:

            FIND FIRST zimmer WHERE zimmer.zikatnr EQ queasy.number1 NO-LOCK NO-ERROR.

        IF AVAILABLE zimmer THEN
        DO:
            FIND FIRST output-list WHERE output-list.roomno EQ queasy.char1
                AND output-list.from-date EQ queasy.date2
                AND output-list.to-date EQ queasy.date3 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE output-list THEN
            DO:

                CREATE output-list.
                ASSIGN 
                    output-list.roomno     = queasy.char1 
                    output-list.roomtype   = zimmer.bezeich
                    output-list.reason     = ENTRY(1,queasy.char2,"$")
                    output-list.from-date  = queasy.date2  
                    output-list.to-date    = queasy.date3  
                    output-list.sysdate    = queasy.date1  
                    output-list.userinit   = queasy.char3
                    . 
            END.                       
        END.
    END.
    IF rmNo NE "" AND rmNo NE ? THEN
    DO:
        FOR EACH output-list WHERE output-list.roomno NE rmNo:
            DELETE output-list.
        END.
    END.

END.
ELSE
DO:
    /*FDL April 06, 2023 => Ticket 2507F0*/
    DO curr-date = from-date TO to-date:
        FOR EACH queasy WHERE queasy.KEY EQ 900
            AND (queasy.date2 GE curr-date AND queasy.date2 LE curr-date) 
            OR (queasy.date2 LE curr-date AND queasy.date3 GE curr-date) /**/ NO-LOCK  BY queasy.date1:

            FIND FIRST zimmer WHERE zimmer.zikatnr EQ queasy.number1 NO-LOCK NO-ERROR.
            IF AVAILABLE zimmer THEN
            DO:

                FIND FIRST output-list WHERE output-list.roomno EQ queasy.char1
                    AND output-list.from-date EQ queasy.date2
                    AND output-list.to-date EQ queasy.date3 NO-LOCK NO-ERROR.
                IF NOT AVAILABLE output-list THEN
                DO:

                    CREATE output-list.
                    ASSIGN 
                        output-list.roomno     = queasy.char1 
                        output-list.roomtype   = zimmer.bezeich
                        output-list.reason     = ENTRY(1,queasy.char2,"$")
                        output-list.from-date  = queasy.date2  
                        output-list.to-date    = queasy.date3  
                        output-list.sysdate    = queasy.date1  
                        output-list.userinit   = queasy.char3
                        . 
                END.                                  
            END.
        END.
    END.
END.

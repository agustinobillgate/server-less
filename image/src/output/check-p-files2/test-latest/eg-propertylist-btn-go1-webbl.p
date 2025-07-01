DEFINE TEMP-TABLE q1-list
    FIELD nr        LIKE eg-property.nr
    FIELD bezeich   LIKE eg-property.bezeich
    FIELD maintask  LIKE eg-property.maintask /*FD for web*/
    FIELD char3     LIKE eg-property.char3
    FIELD char2     LIKE eg-property.char2
    FIELD zinr      LIKE eg-property.zinr
    FIELD datum     LIKE eg-property.datum
    FIELD brand     LIKE eg-property.brand
    FIELD capacity  LIKE eg-property.capacity
    FIELD dimension LIKE eg-property.dimension
    FIELD TYPE      LIKE eg-property.TYPE
    FIELD price     LIKE eg-property.price
    FIELD Spec      LIKE eg-property.Spec
    FIELD location  LIKE eg-property.location
    FIELD activeflag LIKE eg-property.activeflag.

DEFINE TEMP-TABLE output-list 
    FIELD last-nr AS INT INIT 0
    FIELD all-data AS LOGICAL INIT NO.

DEFINE TEMP-TABLE input-param
    FIELD rmNo       AS CHAR INIT "0"
    FIELD main-nr    AS INT INIT 0
    FIELD sguestflag AS LOGICAL
    FIELD last-nr    AS INT INIT 0
    FIELD item-nr    AS INT.

DEF INPUT-OUTPUT PARAMETER location AS INT.
DEF INPUT PARAMETER TABLE FOR input-param.
DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR output-list.

FIND FIRST input-param NO-LOCK NO-ERROR.

CREATE output-list.

DEFINE VARIABLE counter AS INTEGER.
counter = 0.

IF input-param.sguestflag = YES THEN
DO:
    FIND FIRST eg-location WHERE eg-location.guestflag = YES NO-ERROR.
    IF AVAILABLE eg-location THEN location = eg-location.nr.
    
    IF trim(input-param.rmNo) NE "" AND input-param.main-nr = 0 THEN
    DO:
        IF input-param.item-nr = 0 THEN 
        DO:
            FOR EACH eg-property WHERE eg-property.zinr EQ input-param.rmNo
            AND eg-property.nr GT input-param.last-nr
            NO-LOCK, 
            FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
            FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK:
            counter = counter + 1.
            RUN create-it.
            IF counter EQ 300 THEN
            DO:
                output-list.last-nr = eg-property.nr.
                LEAVE.
            END.
            END.
        END.
        ELSE /* kebutuhan show 1 data ketika selesai*/
        DO:
            FOR EACH eg-property WHERE eg-property.zinr EQ input-param.rmNo
            AND eg-property.nr EQ input-param.item-nr
            NO-LOCK, 
            FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
            FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK:
            counter = counter + 1.
            RUN create-it.
            IF counter EQ 300 THEN
            DO:
                output-list.last-nr = eg-property.nr.
                LEAVE.
            END.
            END. 
        END. 
    END.
        
    ELSE IF trim(input-param.rmNo) NE "" AND input-param.main-nr NE 0 THEN
    DO:
        IF input-param.item-nr = 0 THEN 
        DO:
            FOR EACH eg-property WHERE eg-property.zinr EQ input-param.rmNo 
            AND eg-property.maintask = input-param.main-nr 
            AND eg-property.nr GT input-param.last-nr NO-LOCK, 
            FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
            FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK:
            counter = counter + 1.
            RUN create-it.
            IF counter EQ 300 THEN
            DO:
                output-list.last-nr = eg-property.nr.
                LEAVE.
            END.
            END.
        END.
        ELSE /*kebutuhan show 1 data ketika selesai*/
        DO:
            FOR EACH eg-property WHERE eg-property.zinr EQ input-param.rmNo 
            AND eg-property.maintask = input-param.main-nr 
            AND eg-property.nr EQ input-param.item-nr NO-LOCK, 
            FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
            FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK:
            counter = counter + 1.
            RUN create-it.
            IF counter EQ 300 THEN
            DO:
                output-list.last-nr = eg-property.nr.
                LEAVE.
            END.
            END.
        END.  
    END.
        
    ELSE IF trim(input-param.rmNo) = "" AND input-param.main-nr = 0 THEN
    DO:
        IF input-param.item-nr = 0 THEN 
        DO:
            FOR EACH eg-property WHERE eg-property.location EQ location
            AND eg-property.nr GT input-param.last-nr NO-LOCK, 
            FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
            FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK:
            counter = counter + 1.
            RUN create-it.
            IF counter EQ 300 THEN
            DO:
                output-list.last-nr = eg-property.nr.
                LEAVE.
            END.
            END.
        END.
        ELSE /*kebutuhan show 1 data ketika selesai*/
        DO:
            FOR EACH eg-property WHERE eg-property.location EQ location
            AND eg-property.nr EQ input-param.item-nr NO-LOCK, 
            FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
            FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK:
            counter = counter + 1.
            RUN create-it.
            IF counter EQ 300 THEN
            DO:
                output-list.last-nr = eg-property.nr.
                LEAVE.
            END.
            END.
        END.
        
    END.
        
    ELSE IF trim(input-param.rmNo) = "" AND input-param.main-nr NE 0 THEN
    DO:
        IF input-param.item-nr = 0 THEN 
        DO:
            FOR EACH eg-property WHERE eg-property.location EQ location 
            AND eg-property.maintask = input-param.main-nr
            AND eg-property.nr GT input-param.last-nr NO-LOCK, 
            FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
            FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK:
            counter = counter + 1.
            RUN create-it.
            IF counter EQ 300 THEN
            DO:
                output-list.last-nr = eg-property.nr.
                LEAVE.
            END.
            END.
        END.
        ELSE 
        DO:
            FOR EACH eg-property WHERE eg-property.location EQ location 
            AND eg-property.maintask = input-param.main-nr
            AND eg-property.nr EQ input-param.item-nr NO-LOCK, 
            FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
            FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK:
            counter = counter + 1.
            RUN create-it.
            IF counter EQ 300 THEN
            DO:
                output-list.last-nr = eg-property.nr.
                LEAVE.
            END.
            END.
        END.
        
    END.      
END.
ELSE
DO:
    IF location = 0 THEN
    DO: 
        IF input-param.main-nr = 0 THEN
        DO:
            IF input-param.item-nr = 0 THEN 
            DO:
                FOR EACH eg-property NO-LOCK, 
                FIRST eg-Location WHERE eg-Location.nr EQ eg-property.location
                AND eg-property.nr GT input-param.last-nr NO-LOCK, 
                FIRST queasy WHERE queasy.KEY = 133 
                AND queasy.number1 = eg-property.maintask NO-LOCK:
                counter = counter + 1.
                RUN create-it.
                IF counter EQ 300 THEN
                DO:
                    output-list.last-nr = eg-property.nr.
                    LEAVE.
                END.
                END.
            END.
            ELSE 
            DO:
                FOR EACH eg-property NO-LOCK, 
                FIRST eg-Location WHERE eg-Location.nr EQ eg-property.location
                AND eg-property.nr EQ input-param.item-nr NO-LOCK, 
                FIRST queasy WHERE queasy.KEY = 133 
                AND queasy.number1 = eg-property.maintask NO-LOCK:
                counter = counter + 1.
                RUN create-it.
                IF counter EQ 300 THEN
                DO:
                    output-list.last-nr = eg-property.nr.
                    LEAVE.
                END.
                END.
            END.
            
        END.
            
        ELSE IF input-param.main-nr NE 0 THEN
        DO:
            IF input-param.item-nr = 0 THEN 
            DO:
                FOR EACH eg-property WHERE  eg-property.maintask EQ input-param.main-nr
                AND eg-property.nr GT input-param.last-nr NO-LOCK, 
                FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
                FIRST queasy WHERE queasy.KEY = 133 
                AND queasy.number1 = eg-property.maintask NO-LOCK:
                counter = counter + 1.
                RUN create-it.
                IF counter EQ 300 THEN
                DO:
                    output-list.last-nr = eg-property.nr.
                    LEAVE.
                END.
                END.
            END.
            ELSE 
            DO:
                FOR EACH eg-property WHERE  eg-property.maintask EQ input-param.main-nr
                AND eg-property.nr EQ input-param.item-nr NO-LOCK, 
                FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
                FIRST queasy WHERE queasy.KEY = 133 
                AND queasy.number1 = eg-property.maintask NO-LOCK:
                counter = counter + 1.
                RUN create-it.
                IF counter EQ 300 THEN
                DO:
                    output-list.last-nr = eg-property.nr.
                    LEAVE.
                END.
                END.
            END.
            
        END.      
    END.
    ELSE
    DO: 
        IF  input-param.main-nr = 0 THEN
        DO:
            IF input-param.item-nr = 0 THEN 
            DO:
                FOR EACH eg-property WHERE eg-property.location = location 
                AND eg-property.nr GT input-param.last-nr NO-LOCK, 
                FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
                FIRST queasy WHERE queasy.KEY = 133 
                AND queasy.number1 = eg-property.maintask NO-LOCK:
                counter = counter + 1.
                RUN create-it.
                IF counter EQ 300 THEN
                DO:
                    output-list.last-nr = eg-property.nr.
                    LEAVE.
                END.
                END.
            END.
            ELSE 
            DO:
                FOR EACH eg-property WHERE eg-property.location = location 
                AND eg-property.nr EQ input-param.item-nr NO-LOCK, 
                FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
                FIRST queasy WHERE queasy.KEY = 133 
                AND queasy.number1 = eg-property.maintask NO-LOCK:
                counter = counter + 1.
                RUN create-it.
                IF counter EQ 300 THEN
                DO:
                    output-list.last-nr = eg-property.nr.
                    LEAVE.
                END.
                END.
            END.
            
        END.
            
        ELSE IF input-param.main-nr NE 0 THEN
        DO:
            IF input-param.item-nr = 0 THEN 
            DO:
                FOR EACH eg-property WHERE eg-property.location = location 
                AND eg-property.maintask = input-param.main-nr
                AND eg-property.nr GT input-param.last-nr NO-LOCK, 
                FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
                FIRST queasy WHERE queasy.KEY = 133 
                AND queasy.number1 = eg-property.maintask NO-LOCK:
                counter = counter + 1.
                RUN create-it.
                IF counter EQ 300 THEN
                DO:
                    output-list.last-nr = eg-property.nr.
                    LEAVE.
                END.
                END.
            END.
            ELSE 
            DO:
                FOR EACH eg-property WHERE eg-property.location = location 
                AND eg-property.maintask = input-param.main-nr
                AND eg-property.nr EQ input-param.item-nr NO-LOCK, 
                FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
                FIRST queasy WHERE queasy.KEY = 133 
                AND queasy.number1 = eg-property.maintask NO-LOCK:
                counter = counter + 1.
                RUN create-it.
                IF counter EQ 300 THEN
                DO:
                    output-list.last-nr = eg-property.nr.
                    LEAVE.
                END.
                END.
            END. 
        END.      
    END.
END.

IF counter LT 300 THEN output-list.all-data = YES.

PROCEDURE create-it:
    CREATE q1-list.
    ASSIGN
    q1-list.nr        = eg-property.nr
    q1-list.bezeich   = eg-property.bezeich
    q1-list.maintask  = queasy.number1      /*FD for web*/
    /*FD comment*/
    /*q1-list.char3     = eg-property.char3 
    q1-list.char2     = eg-property.char2*/ 
    q1-list.char3     = queasy.char1        /*FD for web*/
    q1-list.char2     = eg-Location.bezeich /*FD for web*/
    q1-list.zinr      = eg-property.zinr
    q1-list.datum     = eg-property.datum
    q1-list.brand     = eg-property.brand
    q1-list.capacity  = eg-property.capacity
    q1-list.dimension = eg-property.dimension
    q1-list.TYPE      = eg-property.TYPE
    q1-list.price     = eg-property.price
    q1-list.Spec      = eg-property.spec /* Malik Serverless 684 change eg-property.Spec -> eg-property.spec */
    q1-list.location  = eg-property.location
    q1-list.activeflag = eg-property.activeflag.
END.



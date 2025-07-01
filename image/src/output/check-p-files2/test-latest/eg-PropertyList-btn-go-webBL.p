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

DEF INPUT-OUTPUT PARAMETER location AS INT.
DEF INPUT PARAMETER rmNo AS CHAR.
DEF INPUT PARAMETER main-nr AS INT.
DEF INPUT PARAMETER sguestflag AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

IF sguestflag = YES THEN
DO:
    FIND FIRST eg-location WHERE eg-location.guestflag = YES NO-ERROR.
    IF AVAILABLE eg-location THEN location = eg-location.nr.
    
    IF trim(rmNo) NE "" AND main-nr = 0  THEN
        FOR EACH eg-property WHERE eg-property.zinr = rmNo NO-LOCK, 
            FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
            FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK:
            RUN create-it.
        END.
    ELSE IF trim(rmNo) NE "" AND main-nr NE 0 THEN
        FOR EACH eg-property WHERE eg-property.zinr = rmNo 
            AND eg-property.maintask = main-nr NO-LOCK, 
            FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
            FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK:
            RUN create-it.
        END.
    ELSE IF trim(rmNo) = "" AND main-nr = 0 THEN
        FOR EACH eg-property WHERE eg-property.location = location NO-LOCK, 
            FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
            FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK:
            RUN create-it.
        END.
    ELSE IF trim(rmNo) = "" AND main-nr NE 0 THEN
        FOR EACH eg-property WHERE eg-property.location = location 
            AND eg-property.maintask = main-nr NO-LOCK, 
            FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
            FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK:
            RUN create-it.
        END.
END.
ELSE
DO:
    IF location = 0 THEN
    DO:
        
        IF main-nr = 0  THEN
            FOR EACH eg-property NO-LOCK, 
                FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
                FIRST queasy WHERE queasy.KEY = 133 
                AND queasy.number1 = eg-property.maintask NO-LOCK:
                RUN create-it.
            END.
        ELSE IF  main-nr NE 0  THEN
            FOR EACH eg-property WHERE  eg-property.maintask = main-nr NO-LOCK, 
                FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
                FIRST queasy WHERE queasy.KEY = 133 
                AND queasy.number1 = eg-property.maintask NO-LOCK:
                RUN create-it.
            END.
    END.
    ELSE
    DO:
        
        IF  main-nr = 0  THEN
            FOR EACH eg-property WHERE eg-property.location = location NO-LOCK, 
                FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
                FIRST queasy WHERE queasy.KEY = 133 
                AND queasy.number1 = eg-property.maintask NO-LOCK:
                RUN create-it.
            END.
        ELSE IF  main-nr NE 0  THEN
            FOR EACH eg-property WHERE eg-property.location = location 
                AND eg-property.maintask = main-nr NO-LOCK, 
                FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
                FIRST queasy WHERE queasy.KEY = 133 
                AND queasy.number1 = eg-property.maintask NO-LOCK:
                RUN create-it.
            END.
    END.
END.

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

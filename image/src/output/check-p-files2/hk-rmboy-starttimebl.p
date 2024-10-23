DEFINE INPUT PARAMETER userinit AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER zinr AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str AS CHAR NO-UNDO.

DEFINE VARIABLE ci-date AS DATE.
DEFINE VARIABLE do-it AS LOGICAL.
DEFINE VARIABLE room AS CHAR.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate.         /* Rulita 211024 | Fixing for serverless */
do-it   = YES.

FOR EACH queasy WHERE queasy.KEY EQ 196 AND queasy.date1 EQ ci-date AND queasy.char2 EQ userinit NO-LOCK :
    IF queasy.number1 NE 0 AND queasy.number2 EQ 0 THEN 
    DO:
        do-it = NO.
        room = ENTRY(1,queasy.char1,";").
    END.
END.

IF NOT do-it THEN
DO:
    msg-str = "Ongoing Cleaning Room Exist, Start Cleaning Another Room Is Not Allowed!-" + room.
    RETURN.
END.

FIND FIRST queasy WHERE queasy.KEY EQ 196 AND queasy.date1 EQ ci-date AND ENTRY(1,queasy.char1,";") EQ zinr EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    IF queasy.char2 NE "" AND queasy.number1 NE 0 THEN
    DO:
        FIND FIRST bediener WHERE bediener.userinit EQ queasy.char2 NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO: 
            IF queasy.number2 EQ 0 THEN
            DO:
                msg-str = "Room " + zinr + " is being cleaned by " + bediener.username.
                RETURN.
            END.
            ELSE
            DO:
                FIND FIRST zimmer WHERE zimmer.zinr EQ zinr NO-LOCK NO-ERROR.
                IF AVAILABLE zimmer AND zimmer.zistatus LE 1 THEN
                DO:
                    msg-str = "Room " + zinr + " is already cleaned by " + bediener.username.
                    RETURN.
                END.
            END.
        END.
    END.
    queasy.char2   = userinit.
    queasy.number1 = TIME.
    queasy.number2 = 0.
END.
/*ELSE
DO:
    CREATE queasy.
    ASSIGN 
    queasy.KEY     = 196
    queasy.char2   = userinit
    queasy.number1 = TIME
    queasy.number2 = 0
        
    .
END.*/
FIND CURRENT queasy NO-LOCK NO-ERROR.
RELEASE queasy.


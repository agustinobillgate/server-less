
DEFINE TEMP-TABLE maintain LIKE eg-maintain.
DEFINE TEMP-TABLE action LIKE eg-action
    FIELD SELECTED AS LOGICAL INITIAL NO.

DEF INPUT PARAMETER TABLE FOR maintain.
DEF INPUT PARAMETER TABLE FOR action.
DEF INPUT PARAMETER user-init    AS CHAR.
DEF INPUT PARAMETER MainNo       AS INT.
DEF INPUT PARAMETER str-property AS CHAR.

FIND FIRST maintain.
RUN create-log.

FIND FIRST eg-maintain WHERE eg-maintain.maintainnr = maintain.maintainnr
    NO-LOCK NO-ERROR.
IF AVAILABLE eg-maintain THEN
DO:
    FIND CURRENT eg-maintain EXCLUSIVE-LOCK.
    BUFFER-COPY maintain TO eg-maintain.
    FIND CURRENT eg-maintain NO-LOCK.

    /*FD for web*/
    FIND FIRST eg-mdetail WHERE eg-mdetail.KEY EQ 1 
        AND eg-mdetail.maintainnr EQ maintain.maintainnr NO-LOCK NO-ERROR.
    IF AVAILABLE eg-mdetail THEN
    DO:
        FOR EACH eg-mdetail WHERE eg-mdetail.KEY EQ 1 AND eg-mdetail.maintainnr EQ maintain.maintainnr:
            DELETE eg-mdetail.
        END.
    
        FOR EACH action WHERE action.SELECTED EQ YES:
            CREATE eg-mdetail.
            ASSIGN 
                eg-mdetail.KEY = 1
                eg-mdetail.maintainnr = maintain.maintainnr            
                eg-mdetail.nr = action.actionnr
                eg-mdetail.create-date = TODAY
                eg-mdetail.create-time = TIME
                eg-mdetail.create-by   = user-init.
        END. 
    END.     
    /*End FD*/
END.

/*old
DEF VAR fl-daily        AS LOGICAL.
DEF VAR fl-weekly       AS LOGICAL.
DEF VAR fl-monthly      AS LOGICAL.
DEF VAR fl-quarter      AS LOGICAL.
DEF VAR fl-half-yearly  AS LOGICAL.
DEF VAR fl-yearly       AS LOGICAL.

DEF VAR a AS DATE.
DEF VAR tdate AS DATE.
DEF VAR nr AS INT.
FIND FIRST maintain.
IF maintain.typework = 1 THEN
    fl-daily = YES.
ELSE IF maintain.typework = 2 THEN
    fl-weekly = YES.
ELSE IF maintain.typework = 3 THEN
    fl-monthly = YES.
ELSE IF maintain.typework = 4 THEN
    fl-quarter = YES.
ELSE IF maintain.typework = 5 THEN
    fl-half-yearly = YES.
ELSE IF maintain.typework = 6 THEN
    fl-yearly = YES.
RUN create-log.
IF fl-daily THEN
DO:
    a = TODAY.
    tdate = a + 360.
    
    DO WHILE a <= tdate:
        FIND FIRST counters WHERE counters.counter-no = 38 EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE counters THEN
        DO:
            CREATE counters.
            ASSIGN counters.counter-no = 38
                counters.counter-bez = "Counter for maintenance in engineering"
                counters.counter = 0.
        END.
        counters.counter = counters.counter + 1.
        FIND CURRENT counters NO-LOCK.
        nr = counters.counter.

        CREATE eg-maintain.
        BUFFER-COPY maintain EXCEPT maintain.maintainnr 
            maintain.TYPE maintain.created-date maintain.estworkdate 
            TO eg-maintain .
        ASSIGN
            eg-maintain.maintainnr = nr
            eg-maintain.TYPE = 1 /*TYPE*/
            eg-maintain.created-date = TODAY 
            eg-maintain.estworkdate = a 
            .
        a = a + 1.
    END.
END.
ELSE IF fl-weekly THEN
DO:
    a = TODAY.
    tdate = a + 7.
    
    DO WHILE a <= tdate:
        FIND FIRST counters WHERE counters.counter-no = 38 EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE counters THEN
        DO:
            CREATE counters.
            ASSIGN counters.counter-no = 38
                counters.counter-bez = "Counter for maintenance in engineering"
                counters.counter = 0.
        END.
        counters.counter = counters.counter + 1.
        FIND CURRENT counters NO-LOCK.
        nr = counters.counter.

        CREATE eg-maintain.
        BUFFER-COPY maintain EXCEPT maintain.maintainnr 
            maintain.TYPE maintain.created-date maintain.estworkdate 
            TO eg-maintain .
        ASSIGN
            eg-maintain.maintainnr = nr
            eg-maintain.TYPE = 1 /*TYPE*/
            eg-maintain.created-date = TODAY 
            eg-maintain.estworkdate = a 
            .
        a = a + 1.
    END.
END.
ELSE IF fl-monthly THEN
DO:
    a = TODAY.
    tdate = a + 30.
    
    DO WHILE a <= tdate:
        FIND FIRST counters WHERE counters.counter-no = 38 EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE counters THEN
        DO:
            CREATE counters.
            ASSIGN counters.counter-no = 38
                counters.counter-bez = "Counter for maintenance in engineering"
                counters.counter = 0.
        END.
        counters.counter = counters.counter + 1.
        FIND CURRENT counters NO-LOCK.
        nr = counters.counter.

        CREATE eg-maintain.
        BUFFER-COPY maintain EXCEPT maintain.maintainnr 
            maintain.TYPE maintain.created-date maintain.estworkdate 
            TO eg-maintain .
        ASSIGN
            eg-maintain.maintainnr = nr
            eg-maintain.TYPE = 1 /*TYPE*/
            eg-maintain.created-date = TODAY 
            eg-maintain.estworkdate = a 
            .
        a = a + 1.
    END.
END.
ELSE IF fl-quarter THEN
DO:
    a = TODAY.
    tdate = a + 90.
    
    DO WHILE a <= tdate:
        FIND FIRST counters WHERE counters.counter-no = 38 EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE counters THEN
        DO:
            CREATE counters.
            ASSIGN counters.counter-no = 38
                counters.counter-bez = "Counter for maintenance in engineering"
                counters.counter = 0.
        END.
        counters.counter = counters.counter + 1.
        FIND CURRENT counters NO-LOCK.
        nr = counters.counter.

        CREATE eg-maintain.
        BUFFER-COPY maintain EXCEPT maintain.maintainnr 
            maintain.TYPE maintain.created-date maintain.estworkdate 
            TO eg-maintain .
        ASSIGN
            eg-maintain.maintainnr = nr
            eg-maintain.TYPE = 1 /*TYPE*/
            eg-maintain.created-date = TODAY 
            eg-maintain.estworkdate = a 
            .
        a = a + 1.
    END.
END.
ELSE IF fl-half-yearly THEN
DO:
    a = TODAY.
    tdate = a + 180.
    
    DO WHILE a <= tdate:
        FIND FIRST counters WHERE counters.counter-no = 38 EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE counters THEN
        DO:
            CREATE counters.
            ASSIGN counters.counter-no = 38
                counters.counter-bez = "Counter for maintenance in engineering"
                counters.counter = 0.
        END.
        counters.counter = counters.counter + 1.
        FIND CURRENT counters NO-LOCK.
        nr = counters.counter.

        CREATE eg-maintain.
        BUFFER-COPY maintain EXCEPT maintain.maintainnr 
            maintain.TYPE maintain.created-date maintain.estworkdate 
            TO eg-maintain .
        ASSIGN
            eg-maintain.maintainnr = nr
            eg-maintain.TYPE = 1 /*TYPE*/
            eg-maintain.created-date = TODAY 
            eg-maintain.estworkdate = a 
            .
        a = a + 1.
    END.
END.
ELSE IF fl-half-yearly THEN
DO:
    a = TODAY.
    tdate = a + 360.
    
    DO WHILE a <= tdate:
        FIND FIRST counters WHERE counters.counter-no = 38 EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE counters THEN
        DO:
            CREATE counters.
            ASSIGN counters.counter-no = 38
                counters.counter-bez = "Counter for maintenance in engineering"
                counters.counter = 0.
        END.
        counters.counter = counters.counter + 1.
        FIND CURRENT counters NO-LOCK.
        nr = counters.counter.

        CREATE eg-maintain.
        BUFFER-COPY maintain EXCEPT maintain.maintainnr 
            maintain.TYPE maintain.created-date maintain.estworkdate 
            TO eg-maintain .
        ASSIGN
            eg-maintain.maintainnr = nr
            eg-maintain.TYPE = 1 /*TYPE*/
            eg-maintain.created-date = TODAY 
            eg-maintain.estworkdate = a 
            .
        a = a + 1.
    END.
END.
ELSE
DO:
    FIND FIRST eg-maintain WHERE eg-maintain.maintainnr = MainNo.
    BUFFER-COPY maintain TO eg-maintain.
    FOR EACH action WHERE action.SELECTED = YES :
        CREATE eg-mdetail.
        ASSIGN 
            eg-mdetail.KEY = 1
            eg-mdetail.maintainnr = maintain.maintainnr
            eg-mdetail.nr = action.actionnr
            eg-mdetail.create-date = TODAY
            eg-mdetail.create-time = TIME
            eg-mdetail.create-by   = user-init.
    END.
    FIND CURRENT eg-maintain NO-LOCK.
    /*MTFIND CURRENT mbuff NO-LOCK.*/
END.
*/

PROCEDURE create-log:
    DEF BUFFER usr   FOR bediener.
    DEF VAR usrnr    AS INTEGER INITIAL 0  NO-UNDO.
    DEF VAR char1    AS CHAR    INITIAL "" NO-UNDO.
    DEF VAR char2    AS CHAR    INITIAL "" NO-UNDO.
    DEF VAR stStat AS CHAR EXTENT 3 INITIAL ["Scheduled", "Processed", "Done"].
    DEF VAR stType AS CHAR EXTENT 5 INITIAL ["Weekly", "Monthly", "Quarter", "Half Yearly", "Year"].  

    FIND FIRST usr WHERE usr.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE usr THEN usrnr = usr.nr.

    FIND FIRST eg-maintain WHERE eg-maintain.maintainnr = mainNo NO-LOCK NO-ERROR.

    IF eg-maintain.TYPE NE maintain.TYPE THEN
    DO:

        CREATE res-history.
        ASSIGN
            res-history.nr          = usrnr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.Action      = "Engineering"
            res-history.aenderung   = "Change Status maintainNo " + STRING(mainno)
                + ": " + ststat[eg-maintain.TYPE] + " To " + ststat[maintain.TYPE].
    END.
    
    IF eg-maintain.estworkdate NE ? THEN
    DO:
        IF eg-maintain.estworkdate NE maintain.estworkdate THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Change estimate work date maintainNo " + STRING(mainno)
                    + ": " + string(eg-maintain.estworkdate) + " To " + string(maintain.estworkdate).
        END.
    END.

    IF eg-maintain.workdate NE ? THEN
    DO:
        IF eg-maintain.workdate NE maintain.workdate THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Change estimate work date maintainNo " + STRING(mainno)
                    + ": " + string(eg-maintain.workdate) + " To " + string(maintain.workdate).
        END.
    END.

    IF eg-maintain.typework NE maintain.typework THEN
    DO:
        CREATE res-history.
        ASSIGN
            res-history.nr          = usrnr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.Action      = "Engineering"
            res-history.aenderung   = "Change frequency of work maintainNo " + STRING(mainno)
                + ": " + stType[eg-maintain.typework] + " To " + stType[maintain.typework].
    END.
    IF eg-maintain.propertynr NE maintain.propertynr THEN
    DO:
        FIND FIRST eg-property WHERE eg-property.nr = eg-maintain.propertynr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-property THEN char1 = eg-property.bezeich + "(" + string(eg-property.nr) + ")".

        char2 = str-property + "(" + string(maintain.propertynr) + ")".

        CREATE res-history.
        ASSIGN
            res-history.nr          = usrnr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.Action      = "Engineering"
            res-history.aenderung   = "Change Object Item maintainNo " + STRING(mainNo)
                + ": " + char1 + " To " + char2.
    END.

    IF eg-maintain.pic  NE maintain.pic THEN
    DO:
        CREATE res-history.
        ASSIGN
            res-history.nr          = usrnr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.Action      = "Engineering"
            res-history.aenderung   = "Change PIC MaintainNo " + STRING(mainNo)
                    + ": " + string(eg-maintain.pic) + " To " + string(maintain.pic). 
    END.
END.


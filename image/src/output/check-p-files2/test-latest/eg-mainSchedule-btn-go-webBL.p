
DEFINE TEMP-TABLE action LIKE eg-action
    FIELD SELECTED AS LOGICAL INITIAL NO.
DEFINE TEMP-TABLE maintain LIKE eg-maintain.

DEF INPUT-OUTPUT PARAMETER TABLE FOR maintain.
DEF INPUT PARAMETER TABLE FOR action.
DEF INPUT PARAMETER user-init AS CHAR.


DEF VAR fl-daily        AS LOGICAL.
DEF VAR fl-weekly       AS LOGICAL.
DEF VAR fl-monthly      AS LOGICAL.
DEF VAR fl-quarter      AS LOGICAL.
DEF VAR fl-half-yearly  AS LOGICAL.
DEF VAR fl-yearly       AS LOGICAL.

DEF VAR a AS DATE.
DEF VAR b AS DATE.
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

IF fl-daily THEN
DO:
    a = maintain.estworkdate.
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

        /*FD for web*/
        FOR EACH action WHERE action.SELECTED EQ YES :
            CREATE eg-mdetail.
            ASSIGN 
                eg-mdetail.KEY = 1
                eg-mdetail.maintainnr = nr                
                eg-mdetail.nr = action.actionnr
                eg-mdetail.create-date = TODAY
                eg-mdetail.create-time = TIME
                eg-mdetail.create-by   = user-init.
        END.
    END.
END.
ELSE IF fl-weekly THEN
DO:
    a = maintain.estworkdate.
    tdate = a + 365.

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
        a = a + 7.

        /*FD for web*/
        FOR EACH action WHERE action.SELECTED EQ YES :
            CREATE eg-mdetail.
            ASSIGN 
                eg-mdetail.KEY = 1
                eg-mdetail.maintainnr = nr                
                eg-mdetail.nr = action.actionnr
                eg-mdetail.create-date = TODAY
                eg-mdetail.create-time = TIME
                eg-mdetail.create-by   = user-init.
        END.
    END.

    /*
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
    */
END.
ELSE IF fl-monthly THEN
DO:
    a = maintain.estworkdate.
    tdate = a + 365.

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
        a = a + 30.

        /*FD for web*/
        FOR EACH action WHERE action.SELECTED EQ YES :
            CREATE eg-mdetail.
            ASSIGN 
                eg-mdetail.KEY = 1
                eg-mdetail.maintainnr = nr                
                eg-mdetail.nr = action.actionnr
                eg-mdetail.create-date = TODAY
                eg-mdetail.create-time = TIME
                eg-mdetail.create-by   = user-init.
        END.
    END.

    /*
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
    */
END.
ELSE IF fl-quarter THEN
DO:
    a = maintain.estworkdate.
    tdate = a + 365.

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
        /*a = a + 120.*/
        a = a + 90. /*FD*/

        /*FD for web*/
        FOR EACH action WHERE action.SELECTED EQ YES :
            CREATE eg-mdetail.
            ASSIGN 
                eg-mdetail.KEY = 1
                eg-mdetail.maintainnr = nr                
                eg-mdetail.nr = action.actionnr
                eg-mdetail.create-date = TODAY
                eg-mdetail.create-time = TIME
                eg-mdetail.create-by   = user-init.
        END.
    END.

    /*
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
    */
END.
ELSE IF fl-half-yearly THEN
DO:
    a = maintain.estworkdate.
    tdate = a + 365.

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
        a = a + 180.

        /*FD for web*/
        FOR EACH action WHERE action.SELECTED EQ YES :
            CREATE eg-mdetail.
            ASSIGN 
                eg-mdetail.KEY = 1
                eg-mdetail.maintainnr = nr                
                eg-mdetail.nr = action.actionnr
                eg-mdetail.create-date = TODAY
                eg-mdetail.create-time = TIME
                eg-mdetail.create-by   = user-init.
        END.
    END.

    /*
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
    */
END.
ELSE IF fl-yearly THEN
DO:
    a = maintain.estworkdate.
    tdate = a + 365.

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
        a = a + 365.

        /*FD for web*/
        FOR EACH action WHERE action.SELECTED EQ YES :
            CREATE eg-mdetail.
            ASSIGN 
                eg-mdetail.KEY = 1
                eg-mdetail.maintainnr = nr                
                eg-mdetail.nr = action.actionnr
                eg-mdetail.create-date = TODAY
                eg-mdetail.create-time = TIME
                eg-mdetail.create-by   = user-init.
        END.
    END.

    /*
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
    */
END.

/** OLD
FIND FIRST maintain.

FIND FIRST counters WHERE counters.counter-no = 38 EXCLUSIVE-LOCK NO-ERROR.
IF NOT AVAILABLE counters THEN
DO:
    CREATE counters.
    ASSIGN counters.counter-no = 38
        counters.counter-bez = "Counter for maintenance in engineering"
        counters.counter = 0.
END.

ASSIGN counters.counter = counters.counter + 1.

FIND CURRENT counters NO-LOCK.

ASSIGN maintain.maintainnr= counters.counter.

CREATE eg-maintain.
BUFFER-COPY maintain TO eg-maintain.

FOR EACH action WHERE action.SELECTED = YES  :
    CREATE eg-mdetail.
    ASSIGN 
        eg-mdetail.KEY = 1
        eg-mdetail.maintainnr = maintain.maintainnr
        eg-mdetail.nr = action.actionnr
        eg-mdetail.create-date = TODAY
        eg-mdetail.create-time = TIME
        eg-mdetail.create-by   = user-init.
END.
**/

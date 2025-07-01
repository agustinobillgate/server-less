DEFINE TEMP-TABLE tlist
    FIELD nr        AS INTEGER
    FIELD ratecode  AS CHAR
    FIELD bezeich   AS CHAR
    FIELD rm-rev    AS DECIMAL
    FIELD arr       AS DECIMAL
    FIELD rm-sold   AS DECIMAL
    FIELD fbrev     AS DECIMAL
    FIELD proz      AS DECIMAL
    FIELD mrm-rev   AS DECIMAL
    FIELD marr      AS DECIMAL
    FIELD mrm-sold  AS DECIMAL
    FIELD mfbrev    AS DECIMAL
    FIELD mproz     AS DECIMAL
    FIELD yrm-rev   AS DECIMAL
    FIELD yarr      AS DECIMAL
    FIELD yrm-sold  AS DECIMAL
    FIELD yfbrev    AS DECIMAL
    FIELD yproz     AS DECIMAL
.

DEFINE TEMP-TABLE tmp-room
    FIELD gastnr    AS INTEGER
    FIELD zinr      LIKE zimmer.zinr
    FIELD flag      AS INTEGER
    INDEX gstnr gastnr DESC zinr. 

DEFINE INPUT PARAMETER from-date AS DATE NO-UNDO.
DEFINE INPUT PARAMETER to-date AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR tlist.

DEFINE VARIABLE s         AS CHAR    NO-UNDO.
DEFINE VARIABLE curr-code AS CHAR    NO-UNDO.
DEFINE VARIABLE do-it     AS LOGICAL NO-UNDO.
DEFINE VARIABLE counter   AS INTEGER NO-UNDO.

DEFINE VARIABLE tot-rmrev   AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-arr     AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-rmsold  AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-fbrev   AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tot-proz    AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tot-mrmrev  AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-marr    AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tot-mrmsold AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-mfbrev  AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tot-mproz   AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tot-yrmrev  AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-yarr    AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tot-yrmsold AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-yfbrev  AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tot-yproz   AS DECIMAL NO-UNDO. 

DEFINE BUFFER bqueasy FOR queasy.

ASSIGN
    tot-rmrev       = 0
    tot-arr         = 0
    tot-rmsold      = 0
    tot-fbrev       = 0
    tot-proz        = 0
    tot-mrmrev      = 0
    tot-marr        = 0
    tot-mrmsold     = 0
    tot-mfbrev      = 0 
    tot-mproz       = 0
    tot-yrmrev      = 0
    tot-yarr        = 0
    tot-yrmsold     = 0
    tot-yfbrev      = 0
    tot-yproz       = 0
.
   
FOR EACH genstat WHERE genstat.datum GE from-date 
    AND genstat.datum LE to-date 
    AND genstat.resstatus NE 13
    AND genstat.segmentcode NE 0 
    AND genstat.nationnr NE 0
    AND genstat.zinr NE "" 
    AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ 
    USE-INDEX date_ix NO-LOCK,
    FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK BY genstat.gastnr:

    ASSIGN do-it = YES.
        FIND FIRST queasy WHERE queasy.KEY = 212 AND queasy.number3 EQ guest.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN DO:
            FIND FIRST bqueasy WHERE bqueasy.KEY = 211 AND bqueasy.number1 = queasy.number1 NO-LOCK NO-ERROR.
            IF AVAILABLE bqueasy THEN ASSIGN curr-code = bqueasy.char1.
            ELSE curr-code = "UNKNOWN".
        END.
        ELSE curr-code = "UNKNOWN".

    IF do-it = YES THEN DO:                         
        FIND FIRST tlist WHERE tlist.ratecode = curr-code NO-ERROR.
        IF NOT AVAILABLE tlist THEN DO:
            CREATE tlist.
            ASSIGN tlist.ratecode = curr-code
                   tlist.bezeich  = curr-code.                              
        END.
        IF genstat.datum EQ to-date THEN DO:
            ASSIGN 
                   tlist.rm-rev = tlist.rm-rev + genstat.logis
                   tot-rmrev    = tot-rmrev + genstat.logis.

            FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                 AND tmp-room.zinr EQ genstat.zinr 
                 AND tmp-room.flag = 1 NO-ERROR.
            IF NOT AVAILABLE tmp-room THEN
            DO:
                ASSIGN 
                    tlist.rm-sold = tlist.rm-sold + 1
                    tot-rmsold    = tot-rmsold + 1.
                    
                CREATE tmp-room.
                ASSIGN tmp-room.gastnr    = genstat.gastnr
                       tmp-room.zinr      = genstat.zinr
                       tmp-room.flag      = 1.
            END.

            ASSIGN 
                tlist.fbrev  = tlist.fbrev + (genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4])
                tot-fbrev    = tot-fbrev + (genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]).
        END.
        
        IF MONTH(genstat.datum) EQ MONTH(to-date) THEN DO:
        ASSIGN 
            tlist.mrm-rev  = tlist.mrm-rev + genstat.logis
            tlist.mrm-sold = tlist.mrm-sold + 1
            tlist.mfbrev   = tlist.mfbrev + (genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4])
            tot-mrmrev     = tot-mrmrev + genstat.logis
            tot-mrmsold    = tot-mrmsold + 1
            tot-mfbrev     = tot-mfbrev + (genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]).
        END.
  
        ASSIGN 
            tlist.yrm-rev  = tlist.yrm-rev + genstat.logis
            tlist.yrm-sold = tlist.yrm-sold + 1
            tlist.yfbrev   = tlist.yfbrev + (genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4])
            tot-yrmrev     = tot-yrmrev + genstat.logis
            tot-yrmsold    = tot-yrmsold + 1
            tot-yfbrev     = tot-yfbrev + (genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]).
    END.
END.


FOR EACH tlist:
    /* Malik Serverless */
    IF DECIMAL(tlist.rm-sold) NE 0 AND DECIMAL(tlist.rm-sold) NE ? THEN
    DO:
        ASSIGN
            tlist.arr    = tlist.rm-rev / tlist.rm-sold.
    END.
    /* END */
    /* tlist.arr    = tlist.rm-rev / tlist.rm-sold */
    /* Rd, div zero */
    IF tlist.rm-sold = 0 THEN
        tlist.arr = 0.
    ELSE
        tlist.arr = tlist.rm-rev / tlist.rm-sold.
    .
    /* END */
    IF tlist.yrm-sold = 0 THEN
        tlist.yarr = 0.
    ELSE
        tlist.yarr = tlist.yrm-rev / tlist.yrm-sold.
    .
    /* END */  
    /*
    ASSIGN 
        tlist.marr   = tlist.mrm-rev / tlist.mrm-sold
        tlist.yarr   = tlist.yrm-rev / tlist.yrm-sold
    .
    */
    
    IF tlist.arr = ? THEN tlist.arr = 0.
    IF tlist.marr = ? THEN tlist.marr = 0.
    IF tlist.yarr = ? THEN tlist.yarr = 0.

    ASSIGN
        tot-arr      = tot-arr + tlist.arr
        tot-marr     = tot-marr + tlist.marr
        tot-yarr     = tot-yarr + tlist.yarr.

    /* Malik Serverless */
    IF DECIMAL(tot-rmrev) NE 0 AND DECIMAL(tot-rmrev) NE ? THEN
    DO:
        ASSIGN
            tlist.proz   = (tlist.rm-rev / tot-rmrev) * 100.
    END.

    IF DECIMAL(tot-mrmrev) NE 0 AND DECIMAL(tot-mrmrev) NE ? THEN
    DO:
        ASSIGN
            tlist.mproz  = (tlist.mrm-rev / tot-mrmrev) * 100.
    END.

    IF DECIMAL(tot-yrmrev) NE 0 AND DECIMAL(tot-yrmrev) NE ? THEN
    DO:
        ASSIGN
            tlist.yproz  = (tlist.yrm-rev / tot-yrmrev) * 100.
    END.
    /* END */
    
    /* Uncomment for serverless   
    ASSIGN
            tlist.proz   = (tlist.rm-rev / tot-rmrev) * 100
            tlist.mproz  = (tlist.mrm-rev / tot-mrmrev) * 100
            tlist.yproz  = (tlist.yrm-rev / tot-yrmrev) * 100. */
        
    IF tlist.proz = ? THEN tlist.proz = 0.
    IF tlist.mproz = ? THEN tlist.mproz = 0.
    IF tlist.yproz = ? THEN tlist.yproz = 0.
    
    ASSIGN
        tot-proz     = tot-proz + tlist.proz
        tot-mproz    = tot-mproz + tlist.mproz
        tot-yproz    = tot-yproz + tlist.yproz.
END.

FOR EACH tlist BY tlist.bezeich:
    ASSIGN 
        counter  = counter + 1
        tlist.nr = counter.    
END.

CREATE tlist.
ASSIGN
    counter         = counter + 1
    tlist.nr        = counter
    tlist.bezeich   = "TOTAL"
    tlist.rm-rev    = tot-rmrev 
    tlist.arr       = tot-arr  
    tlist.rm-sold   = tot-rmsold 
    tlist.fbrev     = tot-fbrev
    tlist.proz      = tot-proz
    tlist.mrm-rev   = tot-mrmrev
    tlist.marr      = tot-marr
    tlist.mrm-sold  = tot-mrmsold
    tlist.mfbrev    = tot-mfbrev
    tlist.mproz     = tot-mproz
    tlist.yrm-rev   = tot-yrmrev
    tlist.yarr      = tot-yarr
    tlist.yrm-sold  = tot-yrmsold
    tlist.yfbrev    = tot-yfbrev
    tlist.yproz     = tot-yproz.

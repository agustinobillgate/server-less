/*FD Dec 05, 2020 => BL for vhpweb based convert STR to temp-table*/

/********** TEMP TABLE ***********/
DEFINE TEMP-TABLE rmcat-segm-list
    FIELD flag          AS INTEGER
    FIELD segment       AS CHARACTER FORMAT "x(40)"
    FIELD room          AS CHARACTER FORMAT "x(8)"
    FIELD pax           AS CHARACTER FORMAT "x(8)"
    FIELD logis         AS CHARACTER FORMAT "x(19)"
    FIELD proz          AS CHARACTER FORMAT "x(6)"
    FIELD avrgrate      AS CHARACTER FORMAT "x(19)"
    FIELD m-room        AS CHARACTER FORMAT "x(8)"
    FIELD m-pax         AS CHARACTER FORMAT "x(8)"
    FIELD m-logis       AS CHARACTER FORMAT "x(19)"
    FIELD m-proz        AS CHARACTER FORMAT "x(6)"
    FIELD m-avrgrate    AS CHARACTER FORMAT "x(19)"
    FIELD y-room        AS CHARACTER FORMAT "x(8)"
    FIELD y-pax         AS CHARACTER FORMAT "x(8)"
    FIELD y-logis       AS CHARACTER FORMAT "x(19)"
    FIELD y-proz        AS CHARACTER FORMAT "x(6)"
    FIELD y-avrgrate    AS CHARACTER FORMAT "x(19)"
    FIELD rmnite1       AS CHARACTER FORMAT "x(8)"
    FIELD rmrev1        AS CHARACTER FORMAT "x(19)"
    FIELD rmnite        AS CHARACTER FORMAT "x(8)"
    FIELD rmrev         AS CHARACTER FORMAT "x(19)"
    FIELD rmcat         AS CHARACTER FORMAT "x(3)"
    FIELD segm-code     AS INTEGER
.

DEFINE TEMP-TABLE s-list
    FIELD segm-code AS INTEGER
    FIELD segment   AS CHAR FORMAT "x(24)" 
    FIELD catnr     AS INTEGER
    FIELD rmcat     AS CHAR FORMAT "x(3)"
    FIELD cat-bez   AS CHAR FORMAT "x(24)"
    FIELD room      AS INTEGER FORMAT "->>9.99"
    FIELD c-room    AS INTEGER INITIAL 0
    FIELD pax       AS INTEGER FORMAT "->>,>>9"
    FIELD logis     AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0 
    FIELD proz      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
    FIELD avrgrate  AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0 

    FIELD m-room     AS INTEGER FORMAT "->>,>>9" INITIAL 0 
    FIELD mc-room    AS INTEGER                  INITIAL 0
    FIELD m-pax      AS INTEGER FORMAT "->>,>>9" INITIAL 0 
    FIELD m-logis    AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0 
    FIELD m-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0 
    FIELD m-avrgrate AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0 
    
    FIELD y-room     AS INTEGER FORMAT "->>>,>>9" INITIAL 0 
    FIELD yc-room    AS INTEGER                   INITIAL 0
    FIELD y-pax      AS INTEGER FORMAT "->>>,>>9" INITIAL 0 
    FIELD y-logis    AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0 
    FIELD y-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0 
    FIELD y-avrgrate AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0. 
    .                            

DEFINE INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER cardtype    AS INTEGER.
DEFINE INPUT  PARAMETER to-date     AS DATE.
DEFINE INPUT  PARAMETER f-date      AS DATE.
DEFINE INPUT  PARAMETER t-date      AS DATE.
DEFINE INPUT  PARAMETER mi-ftd      AS LOGICAL.
DEFINE INPUT  PARAMETER incl-comp   AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR rmcat-segm-list.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.

/*
DEFINE VARIABLE  pvILanguage    AS INTEGER NO-UNDO INIT 1.
DEFINE VARIABLE  cardtype       AS INTEGER INIT 3.        
DEFINE VARIABLE  to-date        AS DATE INIT 01/14/19.           
DEFINE VARIABLE  f-date         AS DATE INIT ?.           
DEFINE VARIABLE  t-date         AS DATE INIT ?.           
DEFINE VARIABLE  mi-ftd         AS LOGICAL INIT NO.        
DEFINE VARIABLE  incl-comp      AS LOGICAL INIT YES.        
*/

DEFINE VARIABLE room        AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE c-room      AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE pax         AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE logis       AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE avrgrate    AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
dEFINE VARIABLE proz        AS DECIMAL FORMAT "->>9.99" INITIAL 0 .
 
DEFINE VARIABLE m-room      AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE mc-room     AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE m-pax       AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE m-logis     AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE m-avrgrate  AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE m-proz      AS DECIMAL FORMAT "->>9.99" INITIAL 0 .
 
DEFINE VARIABLE y-room      AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE yc-room     AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-pax       AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-logis     AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-avrgrate  AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE y-proz      AS DECIMAL FORMAT "->>9.99" INITIAL 0 .
 
DEFINE VARIABLE st-room     AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stc-room    AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE st-pax      AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE st-logis    AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE st-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE st-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0. 
 
DEFINE VARIABLE stm-room    AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stmc-room   AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stm-pax     AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stm-logis   AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE stm-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9".
DEFINE VARIABLE stm-proz    AS DECIMAL FORMAT "->>9.99" INITIAL 0 .
 
DEFINE VARIABLE sty-room    AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE styc-room   AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sty-pax     AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sty-logis   AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE sty-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE sty-proz    AS DECIMAL FORMAT "->>9.99" INITIAL 0. 
/**/
DEFINE VARIABLE gt-room     AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gtc-room    AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gt-pax      AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gt-logis    AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE gt-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9". 

DEFINE VARIABLE gtm-room    AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gtmc-room   AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gtm-pax     AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gtm-logis   AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE gtm-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9".
DEFINE VARIABLE gtm-proz    AS DECIMAL FORMAT "->>9.99" INITIAL 0 .
 
DEFINE VARIABLE gty-room    AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE gtyc-room   AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE gty-pax     AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE gty-logis   AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE gty-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE gty-proz    AS DECIMAL FORMAT "->>9.99" INITIAL 0. 

DEFINE VARIABLE price-decimal   AS INTEGER.
DEFINE VARIABLE count-i         AS INTEGER.

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "rmcat-segment-web".

/*FDL August 08, 24 => Ticket 48484D*/
FOR EACH queasy WHERE queasy.KEY EQ 285
    AND queasy.number1 EQ 1 NO-LOCK:
    FIND FIRST tqueasy WHERE RECID(tqueasy) EQ RECID(queasy) EXCLUSIVE-LOCK.
    DELETE tqueasy.
    RELEASE tqueasy.
END.

FIND FIRST bqueasy WHERE bqueasy.KEY EQ 285
    AND bqueasy.char1 EQ "Guest Segment By Room Type" NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN 
DO:
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 1.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
END.
ELSE IF NOT AVAILABLE bqueasy THEN 
DO:
    CREATE bqueasy.
    ASSIGN 
        bqueasy.KEY      = 285
        bqueasy.char1    = "Guest Segment By Room Type"
        bqueasy.number1  = 1.
END.

/******************** MAIN LOGIC ********************/
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.
RUN create-umsatz.

/*FDL August 08, 24 => Ticket 48484D*/
FIND FIRST rmcat-segm-list NO-LOCK NO-ERROR.
IF AVAILABLE rmcat-segm-list THEN
DO:
    FOR EACH rmcat-segm-list:
        count-i = count-i + 1.
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 280
            queasy.char1    = "Guest Segment By Room Type"
            queasy.char3    = "PROCESS"
            queasy.number1  = count-i
            queasy.char2    = STRING(rmcat-segm-list.flag)      + "|" +
                            rmcat-segm-list.segment             + "|" +
                            rmcat-segm-list.room                + "|" +
                            rmcat-segm-list.pax                 + "|" +
                            rmcat-segm-list.logis               + "|" +
                            rmcat-segm-list.proz                + "|" +
                            rmcat-segm-list.avrgrate            + "|" +
                            rmcat-segm-list.m-room              + "|" +
                            rmcat-segm-list.m-pax               + "|" +
                            rmcat-segm-list.m-logis             + "|" +
                            rmcat-segm-list.m-proz              + "|" +
                            rmcat-segm-list.m-avrgrate          + "|" +
                            rmcat-segm-list.y-room              + "|" +
                            rmcat-segm-list.y-pax               + "|" +
                            rmcat-segm-list.y-logis             + "|" +
                            rmcat-segm-list.y-proz              + "|" +
                            rmcat-segm-list.y-avrgrate          + "|" +
                            rmcat-segm-list.rmnite              + "|" +
                            rmcat-segm-list.rmrev               + "|" +
                            rmcat-segm-list.rmnite1             + "|" +
                            rmcat-segm-list.rmrev1              + "|" +
                            rmcat-segm-list.rmcat               + "|" +
                            STRING(rmcat-segm-list.segm-code) 
                            .        
    END.
END.

FIND FIRST bqueasy WHERE bqueasy.KEY EQ 285
    AND bqueasy.char1 EQ "Guest Segment By Room Type" NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN 
DO:
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 0.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
END.
/******************** PROCEDURE ********************/
PROCEDURE create-umsatz:
    DEFINE VARIABLE mm          AS INTEGER. 
    DEFINE VARIABLE yy          AS INTEGER. 
    DEFINE VARIABLE from-date   AS DATE. 
    DEFINE VARIABLE datum       AS DATE. 
    DEFINE VARIABLE do-it       AS LOGICAL. 
    DEFINE VARIABLE i           AS INTEGER INITIAL 0.
    DEFINE VARIABLE s           AS CHAR.
    DEFINE VARIABLE curr-code   AS CHAR.

    /*incl-comp = NOT MENU-ITEM mi-comp:CHECKED IN MENU mbar. */

    ASSIGN
      room    = 0     
      c-room  = 0 
      pax     = 0 
      logis   = 0 
    
      m-room  = 0 
      mc-room = 0 
      m-pax   = 0 
      m-logis = 0 
      
      y-room  = 0 
      yc-room = 0 
      y-pax   = 0 
      y-logis = 0

      gt-room       = 0
      gt-pax        = 0
      gt-logis      = 0
      gt-avrgrate   = 0
      gtm-room      = 0
      gtm-pax       = 0
      gtm-logis     = 0
      gtm-avrgrate  = 0
      gtm-room      = 0
      gtm-pax       = 0
      gtm-logis     = 0
      gtm-avrgrate  = 0
      gty-room      = 0
      gty-pax       = 0
      gty-logis     = 0
      gty-avrgrate  = 0
      . 
    FOR EACH rmcat-segm-list:
        DELETE rmcat-segm-list.
    END.

    FOR EACH s-list:
        DELETE s-list.
    END.

    IF mi-ftd = YES THEN 
    DO: 
        from-date = f-date. 
        to-date = t-date. 
        mm = MONTH(to-date). 
        yy = YEAR(to-date). 
    END. 
    ELSE 
    DO: 
        mm = MONTH(to-date). 
        yy = YEAR(to-date). 
        from-date = DATE(1,1,yy). 
    END. 

    FOR EACH genstat WHERE 
        genstat.datum GE from-date 
        AND genstat.datum LE to-date 
        AND genstat.zinr NE ""
        AND genstat.gastnr NE 0 
        AND genstat.resstatus NE 13
        /*MT
        AND genstat.res-int[1] NE 13
        */
        AND genstat.segmentcode NE 0 
        AND genstat.res-logic[2] EQ YES 
        USE-INDEX DATE_ix NO-LOCK,
        FIRST guest WHERE guest.gastnr = genstat.gastnr 
        NO-LOCK BY guest.NAME BY guest.gastnr:
        FIND FIRST zimmer WHERE zimmer.zinr = genstat.zinr 
            NO-LOCK. 
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr
            NO-LOCK.
        FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
            NO-LOCK.
        IF cardtype LT 3 THEN do-it = guest.karteityp = cardtype.
        ELSE do-it = YES.
             
        IF NOT incl-comp AND genstat.zipreis = 0 THEN
        DO:
            IF genstat.gratis GT 0 THEN do-it = NO.
            IF (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis = 0)
                AND genstat.resstatus NE 13 THEN do-it = NO.
        END.
        /*IF NOT incl-comp AND genstat.zipreis = 0 
        AND (genstat.gratis GT 0 OR (genstat.erwachs + genstat.kind1
        + genstat.kind2 + genstat.gratis = 0)) THEN
         do-it = NO.*/
        IF do-it THEN
        DO:
            /*IF genstat.zipreis = 0 AND
            (genstat.gratis GT 0 OR (genstat.erwachs + genstat.kind1
            + genstat.kind2 + genstat.gratis = 0)) THEN 
            DO:
                IF genstat.datum = to-date THEN c-room = c-room + 1.
                IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN 
                   mc-room = mc-room + 1.
                yc-room = yc-room + 1.
            END.
            */
            IF genstat.zipreis = 0 THEN
            DO:
                IF (genstat.gratis GT 0) OR 
                    ((genstat.erwachs + genstat.kind1 + genstat.kind2
                      + genstat.gratis = 0) AND genstat.resstatus NE 13) THEN
                DO:
                    IF genstat.datum = to-date THEN c-room = c-room + 1.
                    IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN 
                       mc-room = mc-room + 1.
                    yc-room = yc-room + 1.
                END.
            END.
            FIND FIRST s-list WHERE s-list.catnr = zimmer.zikatnr 
                AND s-list.segm-code = genstat.segmentcode
                NO-ERROR.
            IF NOT AVAILABLE s-list THEN
            DO:
                CREATE s-list.
                ASSIGN s-list.catnr = zimmer.zikatnr
                    s-list.rmcat    = zimkateg.kurzbez
                    s-list.cat-bez  = zimkateg.bezeich
                    s-list.segm-code = genstat.segmentcode
                    s-list.segment  = segment.bezeich.
            END.
            IF genstat.datum = to-date THEN 
            DO:
                IF genstat.resstatus NE 13 THEN
                    ASSIGN
                        s-list.room   = s-list.room + 1  
                        room          = room + 1.
            
                ASSIGN
                    s-list.pax    = s-list.pax  + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                    s-list.logis  = s-list.logis + genstat.logis
                    pax           = pax + genstat.erwachs
                    logis         = logis + genstat.logis
                    avrgrate      = avrgrate + genstat.ratelocal.
            END.
            IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN 
            DO:
                IF genstat.resstatus NE 13 THEN
                    ASSIGN
                        s-list.m-room      = s-list.m-room  + 1
                        m-room             = m-room  + 1.
                ASSIGN
                  s-list.m-pax       = s-list.m-pax   + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                  s-list.m-logis     = s-list.m-logis + genstat.logis
                  m-pax              = m-pax   + genstat.erwachs
                  m-logis            = m-logis + genstat.logis
                  m-avrgrate         = m-avrgrate + genstat.ratelocal.
            END.
            IF genstat.resstatus NE 13 THEN
                ASSIGN
                s-list.y-room      = s-list.y-room  + 1
                y-room             = y-room  + 1.
            ASSIGN
              s-list.y-pax       = s-list.y-pax   + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
              s-list.y-logis     = s-list.y-logis + genstat.logis
              y-pax              = y-pax   + genstat.erwachs 
              y-logis            = y-logis + genstat.logis
              y-avrgrate         = y-avrgrate + genstat.ratelocal.

            FOR EACH s-list:   
              IF (s-list.room - s-list.c-room) NE 0 THEN 
                s-list.avrgrate = s-list.logis / (s-list.room - s-list.c-room). 
              IF (s-list.m-room - s-list.mc-room) NE 0 THEN 
                s-list.m-avrgrate = s-list.m-logis / (s-list.m-room - s-list.mc-room). 
              IF (s-list.y-room - s-list.yc-room) NE 0 THEN 
                s-list.y-avrgrate = s-list.y-logis / (s-list.y-room - s-list.yc-room). 
              IF logis NE 0 THEN 
                s-list.proz = s-list.logis / logis * 100. 
              IF m-logis NE 0 THEN 
                s-list.m-proz = s-list.m-logis / m-logis * 100. 
              IF y-logis NE 0 THEN 
                s-list.y-proz = s-list.y-logis / y-logis * 100. 
            END.      /* each s-list*/
            
            ASSIGN 
                gt-room   = 0
                gtc-room  = 0
                gt-pax    = 0
                gt-logis  = 0
                gt-avrgrate = 0
                gtm-room  = 0
                gtmc-room = 0
                gtm-pax   = 0
                gtm-logis = 0
                gtm-avrgrate = 0
                gty-room  = 0
                gty-pax   = 0
                gtyc-room = 0
                gty-pax   = 0
                gty-logis = 0
                gty-avrgrate = 0.

            FOR EACH s-list NO-LOCK:
                ASSIGN
                    gt-room       = gt-room + s-list.room
                    gtc-room      = gtc-room + s-list.c-room
                    gt-pax        = gt-pax   + s-list.pax
                    gt-logis      = gt-logis + s-list.logis
                    /*gt-avrgrate   = gt-avrgrate + s-list.avrgrate*/
                    gtm-room      = gtm-room + s-list.m-room
                    gtmc-room     = gtmc-room + s-list.mc-room
                    gtm-pax       = gtm-pax + s-list.m-pax
                    gtm-logis     = gtm-logis + s-list.m-logis
                    /*gtm-avrgrate  = gtm-avrgrate + s-list.m-avrgrate */
                    gty-room      = gty-room + s-list.y-room
                    gtyc-room     = gtyc-room + s-list.yc-room
                    gty-pax       = gty-pax + s-list.y-pax
                    gty-logis     = gty-logis + s-list.y-logis
                    /*gty-avrgrate  = gty-avrgrate + s-list.y-avrgrate.*/
                    .
            END.                   
        END.
    END. /* each genstat*/
    RUN create-output.
END.

PROCEDURE create-output:
    DEFINE VARIABLE tot-room AS INTEGER FORMAT "->>,>>9".
    DEFINE BUFFER sbuff FOR s-list.
    DEFINE VARIABLE i AS INTEGER INITIAL 0.
    DEFINE VARIABLE curr-rmtype AS CHAR INITIAL "".

    FOR EACH s-list NO-LOCK BY s-list.cat-bez BY s-list.segment:
        i = i + 1.
        IF curr-rmtype NE s-list.rmcat AND curr-rmtype NE "" THEN
        DO:
            RUN create-sub.
        END.
        IF curr-rmtype NE s-list.rmcat THEN
        DO:
            FOR EACH sbuff WHERE sbuff.rmcat = s-list.rmcat NO-LOCK:
                tot-room = tot-room + sbuff.room.
            END.

            CREATE rmcat-segm-list.
            ASSIGN
                rmcat-segm-list.flag    = 1
                rmcat-segm-list.segment = s-list.cat-bez 
                rmcat-segm-list.logis   = translateExtended("Total Rooms :", lvCAREA, "") + 
                                        " " + TRIM(STRING(tot-room, "->>9")).
            tot-room = 0.
        END.
        IF price-decimal = 0 THEN
        DO:
            CREATE rmcat-segm-list.
            RUN count-sub1.
        END.
        ELSE
        DO:
            CREATE rmcat-segm-list.
            RUN count-sub2.
        END.
        curr-rmtype = s-list.rmcat.
    END.

    RUN create-sub.
    gt-avrgrate = 0. 
    IF (room - c-room) NE 0 THEN gt-avrgrate = gt-logis / (gt-room - gtc-room). 
    gtm-avrgrate = 0. 
    IF (m-room - mc-room) NE 0 THEN gtm-avrgrate = gtm-logis / (gtm-room - gtmc-room). 
    gty-avrgrate = 0. 
    IF (y-room - yc-room) NE 0 THEN gty-avrgrate = gty-logis / (gty-room - gtyc-room). 
 
    CREATE rmcat-segm-list.
    ASSIGN
        rmcat-segm-list.segment    = translateExtended("T o t a l", lvCAREA, "")
        rmcat-segm-list.room       = STRING(gt-room, "->>>,>>9")                
        rmcat-segm-list.pax        = STRING(gt-pax, "->>>,>>9")                 
        rmcat-segm-list.logis      = STRING(gt-logis, "->>,>>>,>>>,>>>,>>9")    
        rmcat-segm-list.proz       = "100.00"                                   
        rmcat-segm-list.avrgrate   = STRING(gt-avrgrate, "->>,>>>,>>>,>>>,>>9") 
        rmcat-segm-list.m-room     = STRING(gtm-room, "->>>,>>9")               
        rmcat-segm-list.m-pax      = STRING(gtm-pax, "->>>,>>9")                
        rmcat-segm-list.m-logis    = STRING(gtm-logis, "->>,>>>,>>>,>>>,>>9")   
        rmcat-segm-list.m-proz     = "100.00"                                   
        rmcat-segm-list.m-avrgrate = STRING(gtm-avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcat-segm-list.y-room     = STRING(gty-room, "->>>,>>9")               
        rmcat-segm-list.y-pax      = STRING(gty-pax, "->>>,>>9")                
        rmcat-segm-list.y-logis    = STRING(gty-logis, "->>,>>>,>>>,>>>,>>9")   
        rmcat-segm-list.y-proz     = "100.00"                                   
        rmcat-segm-list.y-avrgrate = STRING(gty-avrgrate, "->>,>>>,>>>,>>>,>>9")
    .
END PROCEDURE.

PROCEDURE count-sub1:
    ASSIGN
        rmcat-segm-list.segment    = s-list.segment
        rmcat-segm-list.room       = STRING(s-list.room, "->>>,>>9")              
        rmcat-segm-list.pax        = STRING(s-list.pax, "->>>,>>9")               
        rmcat-segm-list.logis      = STRING(s-list.logis, "->>,>>>,>>>,>>>,>>9")     
        rmcat-segm-list.proz       = STRING(s-list.proz, ">>9.99")              
        rmcat-segm-list.avrgrate   = STRING(s-list.avrgrate, "->>,>>>,>>>,>>>,>>9")   
        rmcat-segm-list.m-room     = STRING(s-list.m-room, "->>>,>>9")            
        rmcat-segm-list.m-pax      = STRING(s-list.m-pax, "->>>,>>9")             
        rmcat-segm-list.m-logis    = STRING(s-list.m-logis, "->>,>>>,>>>,>>>,>>9")   
        rmcat-segm-list.m-proz     = STRING(s-list.m-proz, ">>9.99")            
        rmcat-segm-list.m-avrgrate = STRING(s-list.m-avrgrate, "->>,>>>,>>>,>>>,>>9") 
        rmcat-segm-list.y-room     = STRING(s-list.y-room, "->>>,>>9")           
        rmcat-segm-list.y-pax      = STRING(s-list.y-pax, "->>>,>>9")            
        rmcat-segm-list.y-logis    = STRING(s-list.y-logis, "->>,>>>,>>>,>>>,>>9")
        rmcat-segm-list.y-proz     = STRING(s-list.y-proz, ">>9.99")            
        rmcat-segm-list.y-avrgrate = STRING(s-list.y-avrgrate, "->>,>>>,>>>,>>>,>>9")

        rmcat-segm-list.rmnite     = STRING(s-list.y-room, "->>>,>>9")
        rmcat-segm-list.rmrev      = STRING(s-list.y-logis, "->>,>>>,>>>,>>>,>>9")
        rmcat-segm-list.rmnite1    = STRING(s-list.m-room, "->>>,>>9")
        rmcat-segm-list.rmrev1     = STRING(s-list.m-logis, "->>,>>>,>>>,>>>,>>9")
        rmcat-segm-list.rmcat      = s-list.rmcat
        rmcat-segm-list.segm-code  = s-list.segm-code
    .
    proz = proz + s-list.proz.
    m-proz = m-proz + s-list.m-proz.
    y-proz = y-proz + s-list.y-proz.
    st-room = st-room + s-list.room.
    st-pax = st-pax  + s-list.pax.
    st-proz = st-proz + s-list.proz.
    st-logis = st-logis + s-list.logis.
    /*st-avrgrate = st-avrgrate + s-list.avrgrate.*/
    stm-room = stm-room + s-list.m-room.        
    stm-pax = stm-pax  + s-list.m-pax.
    stm-proz = stm-proz + s-list.m-proz.
    stm-logis = stm-logis + s-list.m-logis.
    /*stm-avrgrate = stm-avrgrate + s-list.m-avrgrate.*/
    sty-room = sty-room + s-list.y-room.        
    sty-pax = sty-pax  + s-list.y-pax.
    sty-proz = sty-proz + s-list.y-proz.
    sty-logis = sty-logis + s-list.y-logis.
    /*sty-avrgrate = sty-avrgrate + s-list.y-avrgrate.*/  
END PROCEDURE.

PROCEDURE create-sub:
    DEF VAR ind AS INTEGER NO-UNDO.
    CREATE rmcat-segm-list. 
    rmcat-segm-list.flag = 1. 
    
    CREATE rmcat-segm-list. 
    rmcat-segm-list.flag = 2. 
    
    st-avrgrate = 0. 
    IF (st-room - stc-room) NE 0 THEN st-avrgrate = st-logis / (st-room - stc-room). 
    stm-avrgrate = 0. 
    IF (stm-room - stmc-room) NE 0 THEN stm-avrgrate = stm-logis / (stm-room - stmc-room). 
    sty-avrgrate = 0. 
    IF (sty-room - styc-room) NE 0 THEN sty-avrgrate = sty-logis / (sty-room - styc-room). 
    
    IF price-decimal = 0 THEN
    DO:
        ASSIGN
            rmcat-segm-list.segment    = translateExtended("S u b T o t a l", lvCAREA, "")
            rmcat-segm-list.room       = STRING(st-room, "->>>,>>9")                
            rmcat-segm-list.pax        = STRING(st-pax, "->>>,>>9")                 
            rmcat-segm-list.logis      = STRING(st-logis, "->>,>>>,>>>,>>>,>>9")    
            rmcat-segm-list.proz       = STRING(st-proz, ">>9.99")                  
            rmcat-segm-list.avrgrate   = STRING(st-avrgrate, "->>,>>>,>>>,>>>,>>9") 
            rmcat-segm-list.m-room     = STRING(stm-room, "->>>,>>9")               
            rmcat-segm-list.m-pax      = STRING(stm-pax, "->>>,>>9")                
            rmcat-segm-list.m-logis    = STRING(stm-logis, "->>,>>>,>>>,>>>,>>9")   
            rmcat-segm-list.m-proz     = STRING(stm-proz, ">>9.99")                 
            rmcat-segm-list.m-avrgrate = STRING(stm-avrgrate, "->>,>>>,>>>,>>>,>>9")
            rmcat-segm-list.y-room     = STRING(sty-room, "->>>,>>9")               
            rmcat-segm-list.y-pax      = STRING(sty-pax, "->>>,>>9")                
            rmcat-segm-list.y-logis    = STRING(sty-logis, "->>,>>>,>>>,>>>,>>9")   
            rmcat-segm-list.y-proz     = STRING(sty-proz, ">>9.99")                 
            rmcat-segm-list.y-avrgrate = STRING(sty-avrgrate, "->>,>>>,>>>,>>>,>>9")
        .
    END.  
    ELSE 
    DO:
        ASSIGN
            rmcat-segm-list.segment    = translateExtended("S u b T o t a l", lvCAREA, "")
            rmcat-segm-list.room       = STRING(st-room, "->>>,>>9")                      
            rmcat-segm-list.pax        = STRING(st-pax, "->>>,>>9")                       
            rmcat-segm-list.logis      = STRING(st-logis, "->>>,>>>,>>>,>>9.99")          
            rmcat-segm-list.proz       = STRING(st-proz, ">>9.99")                        
            rmcat-segm-list.avrgrate   = STRING(st-avrgrate, "->>>,>>>,>>>,>>9.99")       
            rmcat-segm-list.m-room     = STRING(stm-room, "->>>,>>9")                     
            rmcat-segm-list.m-pax      = STRING(stm-pax, "->>>,>>9")                      
            rmcat-segm-list.m-logis    = STRING(stm-logis, "->>>,>>>,>>>,>>9.99")         
            rmcat-segm-list.m-proz     = STRING(stm-proz, ">>9.99")                       
            rmcat-segm-list.m-avrgrate = STRING(stm-avrgrate, "->>>,>>>,>>>,>>9.99")      
            rmcat-segm-list.y-room     = STRING(sty-room, "->>>,>>9")                     
            rmcat-segm-list.y-pax      = STRING(sty-pax, "->>>,>>9")                      
            rmcat-segm-list.y-logis    = STRING(sty-logis, "->>>,>>>,>>>,>>9.99")         
            rmcat-segm-list.y-proz     = STRING(sty-proz, ">>9.99")                       
            rmcat-segm-list.y-avrgrate = STRING(sty-avrgrate, "->>>,>>>,>>>,>>9.99")      
        .    
    END.  

    CREATE rmcat-segm-list. 
    RUN init-val.
END PROCEDURE.

PROCEDURE init-val:
  st-room = 0.
  st-pax = 0.
  st-proz = 0.
  st-logis = 0.
  st-avrgrate = 0.
  stm-room = 0.        
  stm-pax = 0.
  stm-proz = 0.
  stm-logis = 0.
  stm-avrgrate = 0.
  sty-room = 0.   
  sty-pax = 0.
  sty-proz = 0.
  sty-logis = 0.
  sty-avrgrate = 0.
END.

PROCEDURE count-sub2:
    ASSIGN
        rmcat-segm-list.segment    = s-list.segment
        rmcat-segm-list.room       = STRING(s-list.room, "->>>,>>9")                 
        rmcat-segm-list.pax        = STRING(s-list.pax, "->>>,>>9")                  
        rmcat-segm-list.logis      = STRING(s-list.logis, "->>>,>>>,>>>,>>9.99")     
        rmcat-segm-list.proz       = STRING(s-list.proz, ">>9.99")                   
        rmcat-segm-list.avrgrate   = STRING(s-list.avrgrate, "->>>,>>>,>>>,>>9.99")  
        rmcat-segm-list.m-room     = STRING(s-list.m-room, "->>>,>>9")               
        rmcat-segm-list.m-pax      = STRING(s-list.m-pax, "->>>,>>9")                
        rmcat-segm-list.m-logis    = STRING(s-list.m-logis, "->>>,>>>,>>>,>>9.99")   
        rmcat-segm-list.m-proz     = STRING(s-list.m-proz, ">>9.99")                 
        rmcat-segm-list.m-avrgrate = STRING(s-list.m-avrgrate, "->>>,>>>,>>>,>>9.99")
        rmcat-segm-list.y-room     = STRING(s-list.y-room, "->>>,>>9")               
        rmcat-segm-list.y-pax      = STRING(s-list.y-pax, "->>>,>>9")                
        rmcat-segm-list.y-logis    = STRING(s-list.y-logis, "->>>,>>>,>>>,>>9.99")   
        rmcat-segm-list.y-proz     = STRING(s-list.y-proz, ">>9.99")                 
        rmcat-segm-list.y-avrgrate = STRING(s-list.y-avrgrate, "->>>,>>>,>>>,>>9.99")
                                     
        rmcat-segm-list.rmnite     = STRING(s-list.y-room, "->>>,>>9")            
        rmcat-segm-list.rmrev      = STRING(s-list.y-logis, "->>>,>>>,>>>,>>9.99")
        rmcat-segm-list.rmnite1    = STRING(s-list.m-room, "->>>,>>9")            
        rmcat-segm-list.rmrev1     = STRING(s-list.m-logis, "->>>,>>>,>>>,>>9.99")
        rmcat-segm-list.rmcat      = s-list.rmcat                                 
        rmcat-segm-list.segm-code  = s-list.segm-code
    .
    proz = proz + s-list.proz.
    m-proz = m-proz + s-list.m-proz.
    y-proz = y-proz + s-list.y-proz.
    st-room = st-room + s-list.room.
    st-pax = st-pax  + s-list.pax.
    st-proz = st-proz + s-list.proz.
    st-logis = st-logis + s-list.logis.
    st-avrgrate = st-avrgrate + s-list.avrgrate.
    stm-room = stm-room + s-list.m-room.        
    stm-pax = stm-pax  + s-list.m-pax.
    stm-proz = stm-proz + s-list.m-proz.
    stm-logis = stm-logis + s-list.m-logis.
    stm-avrgrate = stm-avrgrate + s-list.m-avrgrate.
    sty-room = sty-room + s-list.y-room.        
    sty-pax = sty-pax  + s-list.y-pax.
    sty-proz = sty-proz + s-list.y-proz.
    sty-logis = sty-logis + s-list.y-logis.
    sty-avrgrate = sty-avrgrate + s-list.y-avrgrate.
END PROCEDURE.

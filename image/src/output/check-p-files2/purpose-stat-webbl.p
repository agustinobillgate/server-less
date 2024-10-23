/*FD Dec 04, 2020 => BL for vhp web baesd STR convert to Temp-Table*/

DEFINE TEMP-TABLE pstay-list
    FIELD flag          AS INTEGER
    FIELD purstr        AS CHARACTER FORMAT "x(24)"
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
    FIELD segment       AS CHARACTER FORMAT "x(10)"
.

DEFINE TEMP-TABLE s-list
    /*FIELD segm-code AS INTEGER
    FIELD segment   AS CHAR FORMAT "x(24)" */
    FIELD catnr     AS INTEGER
    FIELD purnr     AS INTEGER
    FIELD purstr    AS CHAR FORMAT "x(24)"
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

DEFINE TEMP-TABLE t-queasy LIKE queasy. /* gerald */

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER mi-comp1         AS LOGICAL.
DEFINE INPUT PARAMETER mi-ftd1          AS LOGICAL.
DEFINE INPUT PARAMETER f-date           AS DATE.
DEFINE INPUT PARAMETER t-date           AS DATE.
DEFINE INPUT PARAMETER to-date          AS DATE.
DEFINE INPUT PARAMETER cardtype         AS INTEGER.
DEFINE INPUT PARAMETER price-decimal    AS INTEGER.
 
DEFINE OUTPUT PARAMETER TABLE FOR pstay-list. 
DEFINE OUTPUT PARAMETER TABLE FOR t-queasy.

/*
DEFINE VARIABLE  pvILanguage      AS INTEGER NO-UNDO INIT 1.
DEFINE VARIABLE  mi-comp1         AS LOGICAL INIT YES.
DEFINE VARIABLE  mi-ftd1          AS LOGICAL INIT NO.
DEFINE VARIABLE  f-date           AS DATE INIT ?.
DEFINE VARIABLE  t-date           AS DATE INIT ?.
DEFINE VARIABLE  to-date          AS DATE INIT 01/04/19.
DEFINE VARIABLE  cardtype         AS INTEGER INIT 3.
DEFINE VARIABLE  price-decimal    AS INTEGER INIT 0.
*/

DEFINE VARIABLE mm                      AS INTEGER. 
DEFINE VARIABLE yy                      AS INTEGER. 
DEFINE VARIABLE from-date               AS DATE. 
DEFINE VARIABLE datum                   AS DATE. 
DEFINE VARIABLE do-it                   AS LOGICAL. 
DEFINE VARIABLE i                       AS INTEGER INITIAL 0.
DEFINE VARIABLE pur-nr                  AS INTEGER INITIAL 0.
DEFINE VARIABLE num                     AS INTEGER INITIAL 0.
DEFINE VARIABLE s                       AS CHAR INITIAL "".
DEFINE VARIABLE curr-code               AS CHAR.
DEFINE VARIABLE incl-comp               AS LOGICAL INITIAL YES.

DEFINE VARIABLE room                    AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE c-room                  AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE pax                     AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE logis                   AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE avrgrate                AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE proz                    AS DECIMAL FORMAT "->>9.99" INITIAL 0 .

DEFINE VARIABLE m-room                  AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE mc-room                 AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE m-pax                   AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE m-logis                 AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE m-avrgrate              AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE m-proz                  AS DECIMAL FORMAT "->>9.99" INITIAL 0 .

DEFINE VARIABLE y-room                  AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE yc-room                 AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-pax                   AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-logis                 AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-avrgrate              AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE y-proz                  AS DECIMAL FORMAT "->>9.99" INITIAL 0 .

DEFINE VARIABLE st-room                 AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stc-room                AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE st-pax                  AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE st-logis                AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE st-avrgrate             AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE st-proz                 AS DECIMAL FORMAT "->>9.99" INITIAL 0. 

DEFINE VARIABLE stm-room                AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stmc-room               AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stm-pax                 AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stm-logis               AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE stm-avrgrate            AS DECIMAL FORMAT "->,>>>,>>>,>>9".
DEFINE VARIABLE stm-proz                AS DECIMAL FORMAT "->>9.99" INITIAL 0 .
 
DEFINE VARIABLE sty-room                AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE styc-room               AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sty-pax                 AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sty-logis               AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE sty-avrgrate            AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE sty-proz                AS DECIMAL FORMAT "->>9.99" INITIAL 0. 

DEFINE VARIABLE gt-room                 AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gtc-room                AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gt-pax                  AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gt-logis                AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE gt-avrgrate             AS DECIMAL FORMAT "->,>>>,>>>,>>9". 

DEFINE VARIABLE gtm-room                AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gtmc-room               AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gtm-pax                 AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE gtm-logis               AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE gtm-avrgrate            AS DECIMAL FORMAT "->,>>>,>>>,>>9".
DEFINE VARIABLE gtm-proz                AS DECIMAL FORMAT "->>9.99" INITIAL 0 .

DEFINE VARIABLE gty-room                AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE gtyc-room               AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE gty-pax                 AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE gty-logis               AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE gty-avrgrate            AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE gty-proz                AS DECIMAL FORMAT "->>9.99" INITIAL 0. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "purpuse-stat-web". 

incl-comp = NOT mi-comp1. 

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

  gt-room = 0
  gt-pax = 0
  gt-logis = 0
  gt-avrgrate = 0
  gtm-room = 0
  gtm-pax = 0
  gtm-logis = 0
  gtm-avrgrate = 0
  gtm-room = 0
  gtm-pax = 0
  gtm-logis = 0
  gtm-avrgrate = 0
  gty-room = 0
  gty-pax = 0
  gty-logis = 0
  gty-avrgrate = 0
  . 
FOR EACH pstay-list:
    DELETE pstay-list.
END.

FOR EACH s-list:
    DELETE s-list.
END.

IF mi-ftd1 THEN 
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

FOR EACH genstat WHERE genstat.datum GE from-date AND
    genstat.datum LE to-date AND genstat.zinr NE "" AND 
    genstat.res-logic[2] USE-INDEX DATE_ix NO-LOCK,
    FIRST guest WHERE guest.gastnr = genstat.gastnr 
    NO-LOCK BY guest.NAME BY guest.gastnr:
    FIND FIRST zimmer WHERE zimmer.zinr = genstat.zinr 
        NO-LOCK NO-ERROR. 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr
        NO-LOCK.
    FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
        NO-LOCK NO-ERROR.
    IF cardtype LT 3 THEN do-it = guest.karteityp = cardtype.
    ELSE do-it = YES.
         /*
    IF NOT incl-comp AND genstat.zipreis = 0 
    AND (genstat.gratis GT 0 OR (genstat.erwachs + genstat.kind1
    + genstat.kind2 + genstat.gratis = 0)) THEN
     do-it = NO.
     */
    IF NOT incl-comp AND genstat.zipreis = 0 THEN
    DO:
        IF genstat.gratis GT 0 THEN do-it = NO.
        IF (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis = 0)
            AND genstat.resstatus NE 13 THEN do-it = NO.
    END.
    IF do-it THEN
    DO:
        /*IF genstat.zipreis = 0 AND
        (genstat.gratis GT 0 OR (genstat.erwachs + genstat.kind1
        + genstat.kind2 + genstat.gratis = 0)) THEN 
        DO:
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
        /*FIND FIRST s-list WHERE s-list.catnr = zimmer.zikatnr 
            AND s-list.segm-code = genstat.segmentcode
            NO-ERROR.*/
        pur-nr = 0.
        DO num = 1 TO NUM-ENTRIES(genstat.res-char[2], ";"):
            s = ENTRY(num,genstat.res-char[2], ";").
            IF s MATCHES("SEGM_PUR*") THEN
                pur-nr = INTEGER (SUBSTR(s, INDEX(s, "SEGM_PUR") + 8)).
                         
        END.
        FIND FIRST s-list WHERE s-list.purnr = pur-nr NO-ERROR.
        IF NOT AVAILABLE s-list THEN
        DO:
            CREATE s-list.
            ASSIGN 
                s-list.purnr    = pur-nr
                s-list.cat-bez  = zimkateg.bezeich
                /*s-list.segm-code = genstat.segmentcode
                s-list.segment  = segment.bezeich*/ 
                .
            FIND FIRST queasy WHERE queasy.KEY = 143 AND queasy.number1 = pur-nr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                BUFFER-COPY queasy TO t-queasy.
                s-list.purstr = queasy.char3.
            END.
            ELSE 
            DO:
                s-list.purstr = translateExtended("UNKNOWN", lvCAREA, "").
            END.

        END.
        IF genstat.datum = to-date THEN
        DO:
           IF genstat.resstatus NE 13 THEN
                ASSIGN
                    s-list.room   = s-list.room + 1  
                    room          = room + 1.
         /*  DISP genstat.gratis genstat.zinr genstat.datum. PAUSE.*/
             ASSIGN                           
                s-list.pax    = s-list.pax  + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                s-list.logis  = s-list.logis + genstat.logis
                pax           = pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
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
              m-pax              = m-pax   + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
              m-logis            = m-logis + genstat.logis
              m-avrgrate         = m-avrgrate + genstat.rateLocal.
        END.
        IF genstat.resstatus NE 13 THEN
            ASSIGN
            s-list.y-room      = s-list.y-room  + 1
            y-room             = y-room  + 1.
        ASSIGN
          /* s-list.y-room      = s-list.y-room  + 1 */
          s-list.y-pax       = s-list.y-pax   + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
          s-list.y-logis     = s-list.y-logis + genstat.logis
          /* y-room             = y-room  + 1 */
          y-pax              = y-pax   + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
          y-logis            = y-logis + genstat.logis
          y-avrgrate         = y-avrgrate + genstat.rateLocal.

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
              gt-avrgrate   = gt-avrgrate + s-list.avrgrate
              gtm-room      = gtm-room + s-list.m-room
              gtmc-room     = gtmc-room + s-list.mc-room
              gtm-pax       = gtm-pax + s-list.m-pax
              gtm-logis     = gtm-logis + s-list.m-logis
              gtm-avrgrate  = gtm-avrgrate + s-list.m-avrgrate
              gty-room      = gty-room + s-list.y-room
              gtyc-room     = gtyc-room + s-list.yc-room
              gty-pax       = gty-pax + s-list.y-pax
              gty-logis     = gty-logis + s-list.y-logis
              gty-avrgrate  = gty-avrgrate + s-list.y-avrgrate.
      END.
               
    END.
END. /* each genstat*/

RUN create-output.
/*************************************** PROCEDURE *******************************************/

PROCEDURE create-output:
    DEFINE VARIABLE tot-room AS INTEGER FORMAT "->>,>>9".
    DEFINE BUFFER pstay-buff FOR pstay-list.
    DEFINE BUFFER sbuff FOR s-list.
    DEFINE VARIABLE i AS INTEGER INITIAL 0.
    DEFINE VARIABLE curr-rmtype AS CHAR INITIAL "".

    FOR EACH s-list NO-LOCK BY s-list.purstr:
        i = i + 1.
        IF curr-rmtype NE s-list.rmcat AND curr-rmtype NE "" THEN
        DO:
            RUN create-sub.
        END.
       /* IF curr-rmtype NE s-list.rmcat THEN
        DO:
            FOR EACH sbuff WHERE sbuff.rmcat = s-list.rmcat NO-LOCK:
                tot-room = tot-room + sbuff.room.
            END.
            CREATE output-list.
            ASSIGN
            output-list.flag = 1
            output-list.str = STRING(s-list.cat-bez, "x(24)") + 
                FILL(" ", 14) + translateExtended("Total Rooms :", lvCAREA, "") + 
                " " + TRIM(STRING(tot-room, "->>,>>9")).
            tot-room = 0.
        END.
        */
        IF price-decimal = 0 THEN
        DO:
            CREATE pstay-list.
            RUN count-sub1.
        END.
        ELSE
        DO:
            CREATE pstay-list.
            RUN count-sub2.
        END.
        curr-rmtype = s-list.rmcat.
    END.
    RUN create-sub.

    CREATE pstay-list.
    ASSIGN                    
        pstay-list.purstr     = translateExtended("T o t a l", lvCAREA, "")
        pstay-list.room       = STRING(gt-room, "->>>,>>9")             
        pstay-list.pax        = STRING(gt-pax, "->>>,>>9")              
        pstay-list.logis      = STRING(gt-logis, "->>,>>>,>>>,>>>,>>9")    
        pstay-list.proz       = "100.00"                              
        pstay-list.avrgrate   = STRING(gt-avrgrate, "->>,>>>,>>>,>>>,>>9")  
        pstay-list.m-room     = STRING(gtm-room, "->>>,>>9")            
        pstay-list.m-pax      = STRING(gtm-pax, "->>>,>>9")             
        pstay-list.m-logis    = STRING(gtm-logis, "->>,>>>,>>>,>>>,>>9")   
        pstay-list.m-proz     = "100.00"                              
        pstay-list.m-avrgrate = STRING(gtm-avrgrate, "->>,>>>,>>>,>>>,>>9") 
        pstay-list.y-room     = STRING(gty-room, "->>>,>>9")           
        pstay-list.y-pax      = STRING(gty-pax, "->>>,>>9")            
        pstay-list.y-logis    = STRING(gty-logis, "->>,>>>,>>>,>>>,>>9")
        pstay-list.y-proz     = "100.00"                              
        pstay-list.y-avrgrate = STRING(gty-avrgrate, "->>,>>>,>>>,>>>,>>9")
    .
END PROCEDURE.

PROCEDURE count-sub1:
    ASSIGN
        pstay-list.purstr     = s-list.purstr
        pstay-list.room       = STRING(s-list.room, "->>>,>>9")              
        pstay-list.pax        = STRING(s-list.pax, "->>>,>>9")               
        pstay-list.logis      = STRING(s-list.logis, "->>,>>>,>>>,>>>,>>9")     
        pstay-list.proz       = STRING(s-list.proz, ">>9.99")              
        pstay-list.avrgrate   = STRING(s-list.avrgrate, "->>,>>>,>>>,>>>,>>9")   
        pstay-list.m-room     = STRING(s-list.m-room, "->>>,>>9")            
        pstay-list.m-pax      = STRING(s-list.m-pax, "->>>,>>9")             
        pstay-list.m-logis    = STRING(s-list.m-logis, "->>,>>>,>>>,>>>,>>9")   
        pstay-list.m-proz     = STRING(s-list.m-proz, ">>9.99")            
        pstay-list.m-avrgrate = STRING(s-list.m-avrgrate, "->>,>>>,>>>,>>>,>>9") 
        pstay-list.y-room     = STRING(s-list.y-room, "->>>,>>9")           
        pstay-list.y-pax      = STRING(s-list.y-pax, "->>>,>>9")            
        pstay-list.y-logis    = STRING(s-list.y-logis, "->>,>>>,>>>,>>>,>>9")
        pstay-list.y-proz     = STRING(s-list.y-proz, ">>9.99")            
        pstay-list.y-avrgrate = STRING(s-list.y-avrgrate, "->>,>>>,>>>,>>>,>>9")

        pstay-list.rmnite     = STRING(s-list.y-room, "->>>,>>9")
        pstay-list.rmrev      = STRING(s-list.y-logis, "->>,>>>,>>>,>>>,>>9")
        pstay-list.rmnite1    = STRING(s-list.m-room, "->>>,>>9")
        pstay-list.rmrev1     = STRING(s-list.m-logis, "->>,>>>,>>>,>>>,>>9")
        pstay-list.rmcat      = s-list.rmcat
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

PROCEDURE create-sub:
    DEF VAR ind AS INTEGER NO-UNDO.
    
    CREATE pstay-list. 
    pstay-list.flag = 1. 
    
    CREATE pstay-list. 
    pstay-list.flag = 2. 

    st-avrgrate = 0. 
    IF (st-room - stc-room) NE 0 THEN st-avrgrate = st-logis / (st-room - stc-room). 
    stm-avrgrate = 0. 
    IF (stm-room - stmc-room) NE 0 THEN stm-avrgrate = stm-logis / (stm-room - stmc-room). 
    sty-avrgrate = 0. 
    IF (sty-room - styc-room) NE 0 THEN sty-avrgrate = sty-logis / (sty-room - styc-room). 
    
    IF price-decimal = 0 THEN 
    DO:
        ASSIGN
            pstay-list.purstr     = translateExtended("S u b T o t a l", lvCAREA, "")
            pstay-list.room       = STRING(st-room, "->>>,>>9")             
            pstay-list.pax        = STRING(st-pax, "->>>,>>9")              
            pstay-list.logis      = STRING(st-logis, "->>,>>>,>>>,>>>,>>9")    
            pstay-list.proz       = STRING(st-proz, ">>9.99")             
            pstay-list.avrgrate   = STRING(st-avrgrate, "->>,>>>,>>>,>>>,>>9")  
            pstay-list.m-room     = STRING(stm-room, "->>>,>>9")            
            pstay-list.m-pax      = STRING(stm-pax, "->>>,>>9")             
            pstay-list.m-logis    = STRING(stm-logis, "->>,>>>,>>>,>>>,>>9")   
            pstay-list.m-proz     = STRING(stm-proz, ">>9.99")            
            pstay-list.m-avrgrate = STRING(stm-avrgrate, "->>,>>>,>>>,>>>,>>9") 
            pstay-list.y-room     = STRING(sty-room, "->>>,>>9")           
            pstay-list.y-pax      = STRING(sty-pax, "->>>,>>9")            
            pstay-list.y-logis    = STRING(sty-logis, "->>,>>>,>>>,>>>,>>9")
            pstay-list.y-proz     = STRING(sty-proz, ">>9.99")            
            pstay-list.y-avrgrate = STRING(sty-avrgrate, "->>,>>>,>>>,>>>,>>9")
        .   
    END.
    ELSE 
    DO:
        ASSIGN
            pstay-list.purstr     = translateExtended("S u b T o t a l", lvCAREA, "")
            pstay-list.room       = STRING(st-room, "->>>,>>9")                       
            pstay-list.pax        = STRING(st-pax, "->>>,>>9")                        
            pstay-list.logis      = STRING(st-logis, "->>>,>>>,>>>,>>9.99")          
            pstay-list.proz       = STRING(st-proz, ">>9.99")                        
            pstay-list.avrgrate   = STRING(st-avrgrate, "->>>,>>>,>>>,>>9.99")       
            pstay-list.m-room     = STRING(stm-room, "->>>,>>9")                      
            pstay-list.m-pax      = STRING(stm-pax, "->>>,>>9")                       
            pstay-list.m-logis    = STRING(stm-logis, "->>>,>>>,>>>,>>9.99")         
            pstay-list.m-proz     = STRING(stm-proz, ">>9.99")                       
            pstay-list.m-avrgrate = STRING(stm-avrgrate, "->>>,>>>,>>>,>>9.99")      
            pstay-list.y-room     = STRING(sty-room, "->>>,>>9")                     
            pstay-list.y-pax      = STRING(sty-pax, "->>>,>>9")                      
            pstay-list.y-logis    = STRING(sty-logis, "->>>,>>>,>>>,>>9.99")         
            pstay-list.y-proz     = STRING(sty-proz, ">>9.99")                       
            pstay-list.y-avrgrate = STRING(sty-avrgrate, "->>>,>>>,>>>,>>9.99")      
        .
    END.   

    CREATE pstay-list. 
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
END PROCEDURE.

PROCEDURE count-sub2:
    ASSIGN
        pstay-list.purstr     = s-list.purstr                                   
        pstay-list.room       = STRING(s-list.room, "->>>,>>9")                  
        pstay-list.pax        = STRING(s-list.pax, "->>>,>>9")                   
        pstay-list.logis      = STRING(s-list.logis, "->>>,>>>,>>>,>>9.99")     
        pstay-list.proz       = STRING(s-list.proz, ">>9.99")                   
        pstay-list.avrgrate   = STRING(s-list.avrgrate, "->>>,>>>,>>>,>>9.99")  
        pstay-list.m-room     = STRING(s-list.m-room, "->>>,>>9")                
        pstay-list.m-pax      = STRING(s-list.m-pax, "->>>,>>9")                 
        pstay-list.m-logis    = STRING(s-list.m-logis, "->>>,>>>,>>>,>>9.99")   
        pstay-list.m-proz     = STRING(s-list.m-proz, ">>9.99")                 
        pstay-list.m-avrgrate = STRING(s-list.m-avrgrate, "->>>,>>>,>>>,>>9.99")
        pstay-list.y-room     = STRING(s-list.y-room, "->>>,>>9")               
        pstay-list.y-pax      = STRING(s-list.y-pax, "->>>,>>9")                
        pstay-list.y-logis    = STRING(s-list.y-logis, "->>>,>>>,>>>,>>9.99")   
        pstay-list.y-proz     = STRING(s-list.y-proz, ">>9.99")                 
        pstay-list.y-avrgrate = STRING(s-list.y-avrgrate, "->>>,>>>,>>>,>>9.99")
        
        pstay-list.rmnite     = STRING(s-list.y-room, "->>>,>>9")
        pstay-list.rmrev      = STRING(s-list.y-logis, "->>>,>>>,>>>,>>9.99")
        pstay-list.rmnite1    = STRING(s-list.m-room, "->>>,>>9")
        pstay-list.rmrev1     = STRING(s-list.m-logis, "->>>,>>>,>>>,>>9.99")
        pstay-list.rmcat      = s-list.rmcat
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


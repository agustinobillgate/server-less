/* only used in vhp cloud*/

DEFINE TEMP-TABLE output-list 
  FIELD dqty        AS INTEGER FORMAT "->>,>>>" LABEL "ToDate QTY" /* Naufal Afthar - 9513B5*/
  FIELD mqty        AS INTEGER FORMAT "->>,>>>" LABEL "MTD Qty" 
  FIELD yqty        AS INTEGER FORMAT "->>,>>>" LABEL "YTD Qty" /* Dzikri 1160FA - Req shown YTD */
  FIELD bezeich     AS CHAR    FORMAT "x(40)" /* Naufal Afthar - AFB4A4*/
  FIELD STR         AS CHAR. 

DEFINE TEMP-TABLE turn-reportlist /* Dzikri 1160FA - Req shown YTD */ /*william 10/01/24 add format for every field except bezeich*/
    FIELD artno          AS INTEGER   FORMAT ">>>>>>>>>"   
    FIELD descr          AS CHARACTER FORMAT "x(24)"
    FIELD day-net        AS DECIMAL   FORMAT "->>,>>>,>>9.99"
    FIELD day-gros       AS DECIMAL   FORMAT "->>,>>>,>>9.99"
    FIELD day-proz       AS DECIMAL   FORMAT "->>9.99" 
    FIELD todate-mnet    AS DECIMAL   FORMAT "->>,>>>,>>9.99"
    FIELD todate-mgros   AS DECIMAL   FORMAT "->>,>>>,>>9.99"
    FIELD todate-mproz   AS DECIMAL   FORMAT "->>9.99" 
    FIELD todate-ynet    AS DECIMAL   FORMAT "->>,>>>,>>9.99"
    FIELD todate-ygros   AS DECIMAL   FORMAT "->>,>>>,>>9.99"
    FIELD todate-yproz   AS DECIMAL   FORMAT "->>9.99" 
    FIELD dqty           AS INTEGER   FORMAT "->>,>>>" /* Naufal Afthar - 9513B5*/
    FIELD mqty           AS INTEGER   FORMAT "->>,>>>" 
    FIELD yqty           AS INTEGER   FORMAT "->>,>>>" 
    .
DEFINE WORKFILE cl-list 
  FIELD flag       AS CHAR FORMAT "x(2)" INITIAL "" 
  FIELD artnr      AS INTEGER FORMAT ">>>>>>>>>" INITIAL 0 
  FIELD dept       AS INTEGER 
  FIELD bezeich    AS CHAR FORMAT "x(24)" 
  FIELD dnet       AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD proz1      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD dgros      AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD proz2      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD dqty       AS INTEGER FORMAT "->>,>>>" /* Naufal Afthar - 9513B5*/
  FIELD mqty       AS INTEGER FORMAT "->>,>>9" 
  FIELD mnet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz3      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD mgros      AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz4      AS DECIMAL FORMAT "->>9.99" INITIAL 0
  FIELD yqty       AS INTEGER FORMAT "->>,>>9" 
  FIELD ynet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz5      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD ygros      AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz6      AS DECIMAL FORMAT "->>9.99" INITIAL 0
. 


DEF INPUT PARAMETER ldry-flag   AS LOGICAL.
DEF INPUT PARAMETER ldry        AS INT.
DEF INPUT PARAMETER dstore      AS INT.
DEF INPUT PARAMETER from-dept   AS INT.
DEF INPUT PARAMETER to-dept     AS INT.
DEF INPUT PARAMETER from-date   AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER detailed    AS LOGICAL.
DEF INPUT PARAMETER long-digit  AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR turn-reportlist.

/* Dzikri 1160FA - Req shown YTD 
RUN resumz-list-btn-go1-cldbl.p (ldry-flag, ldry, dstore, from-dept, 
                            to-dept, from-date, to-date, detailed, 
                            long-digit, OUTPUT TABLE output-list).*/
    
from-date = DATE(1,1,YEAR(to-date)).

FOR EACH turn-reportlist:
    DELETE turn-reportlist.
END.

RUN create-h-umsatz.

/* 
FOR EACH turn-reportlist:
    DELETE turn-reportlist.
END.

FOR EACH output-list:
    CREATE turn-reportlist.
    ASSIGN 
       turn-reportlist.artno         = INT(SUBSTR(STR, 1, 9)) /* Dzikri 1160FA - Req shown YTD */ /*william 10/01/24 add increase artno substring*/  
       /*turn-reportlist.descr         = SUBSTR(STR, 10, 24) */
       turn-reportlist.descr         = output-list.bezeich /* Naufal Afthar - AFB4A4*/
       turn-reportlist.day-net       = DECIMAL(SUBSTR(STR, 34, 14))
       turn-reportlist.day-gros      = DECIMAL(SUBSTR(STR, 48, 14))
       turn-reportlist.day-proz      = DECIMAL(SUBSTR(STR, 62, 7)) 
       turn-reportlist.todate-mnet   = DECIMAL(SUBSTR(STR, 69, 15))
       turn-reportlist.todate-mgros  = DECIMAL(SUBSTR(STR, 84, 15))
       turn-reportlist.todate-mproz  = DECIMAL(SUBSTR(STR, 99, 7)) 
       turn-reportlist.todate-ynet   = DECIMAL(SUBSTR(STR, 106, 15))
       turn-reportlist.todate-ygros  = DECIMAL(SUBSTR(STR, 121, 15))
       turn-reportlist.todate-yproz  = DECIMAL(SUBSTR(STR, 136, 7)) 
       turn-reportlist.dqty          = output-list.dqty /* Naufal Afthar - 9513B5*/
       turn-reportlist.mqty          = output-list.mqty
       turn-reportlist.yqty          = output-list.yqty
       .
END.*/

PROCEDURE create-h-umsatz: 
  DEFINE VARIABLE dnet AS DECIMAL. 
  DEFINE VARIABLE dgros AS DECIMAL. 
  DEFINE VARIABLE mnet AS DECIMAL. 
  DEFINE VARIABLE mgros AS DECIMAL. 
  DEFINE VARIABLE ynet AS DECIMAL. 
  DEFINE VARIABLE ygros AS DECIMAL.
  DEFINE VARIABLE vat AS DECIMAL. 
  DEFINE VARIABLE serv AS DECIMAL. 
  DEFINE VARIABLE it-exist AS LOGICAL. 
  DEFINE VARIABLE serv-vat AS LOGICAL. 
  DEFINE VARIABLE fact AS DECIMAL. 
 
  DEFINE VARIABLE dqty AS INTEGER INITIAL 0. /* Naufal Afthar - 9513B5*/
  DEFINE VARIABLE mqty AS INTEGER INITIAL 0. 
  DEFINE VARIABLE yqty AS INTEGER INITIAL 0. 
 
  DEFINE VARIABLE curr-ldry AS INTEGER INITIAL 0. 
  DEFINE VARIABLE curr-dstore AS INTEGER INITIAL 0. 
  DEFINE VARIABLE do-it AS LOGICAL. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  IF ldry-flag THEN 
  DO: 
    curr-ldry = ldry. 
    curr-dstore = dstore. 
  END. 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept AND hoteldpt.num NE curr-ldry 
    AND hoteldpt.num NE curr-dstore NO-LOCK BY hoteldpt.num: 
    
    CREATE cl-list. 
    ASSIGN
      cl-list.flag = "*"
      cl-list.bezeich = STRING(hoteldpt.num) + " - " + hoteldpt.depart
      dqty = 0 /* Naufal Afthar - 9513B5*/
      dnet = 0
      dgros = 0 
      mnet = 0 
      mgros = 0 
      mqty = 0
      ynet = 0 
      ygros = 0
      yqty = 0. 
 
    FOR EACH h-artikel WHERE (h-artikel.artart = 0 OR h-artikel.artart = 8) 
      AND h-artikel.departement = hoteldpt.num NO-LOCK BY h-artikel.artnr: 
      it-exist = NO. 
    /*  
     IF h-artikel.service-code NE 0 THEN 
      DO: 
        FIND FIRST htparam WHERE htparam.paramnr = h-artikel.service-code NO-LOCK. 
        IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
          serv = htparam.fdecimal / 100. 
      END. 
      IF h-artikel.mwst-code NE 0 THEN 
      DO: 
        FIND FIRST htparam WHERE htparam.paramnr = h-artikel.mwst-code NO-LOCK. 
        IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
        DO: 
          vat = htparam.fdecimal / 100. 
          IF serv-vat THEN vat = vat + vat * serv. 
          vat = round(vat, 2). 
        END. 
      END. 
 
      fact = 1.00 + serv + vat. 
 */
      serv = 0. 
      vat = 0. 
      FOR EACH h-umsatz WHERE h-umsatz.artnr = h-artikel.artnr 
        AND h-umsatz.departement = h-artikel.departement 
        AND h-umsatz.datum GE from-date AND h-umsatz.datum LE to-date 
        NO-LOCK BY h-umsatz.datum: 
          RUN calc-servvat.p(h-umsatz.departement, h-umsatz.artnr, h-umsatz.datum, h-artikel.service-code, 
             h-artikel.mwst-code, OUTPUT serv, OUTPUT vat).
        fact = 1.00 + serv + vat. 

        IF NOT it-exist THEN 
        DO: 
          it-exist = YES. 
          create cl-list. 
          cl-list.artnr = h-umsatz.artnr. 
          cl-list.dept = h-umsatz.departement. 
          cl-list.bezeich = h-artikel.bezeich. 
        END. 
        IF h-umsatz.datum = to-date THEN 
        DO: 
          cl-list.dqty = h-umsatz.anzahl. /* Naufal Afthar - 9513B5*/
          cl-list.dnet = h-umsatz.betrag / fact. 
          cl-list.dgros = h-umsatz.betrag. 
          dqty = dqty + cl-list.dqty. /* Naufal Afthar - 9513B5*/
          dnet = dnet + cl-list.dnet. 
          dgros = dgros + cl-list.dgros. 
        END. 
        IF MONTH(h-umsatz.datum) EQ MONTH(to-date) AND YEAR(h-umsatz.datum) EQ YEAR(to-date) THEN
        DO:
          cl-list.mnet  = cl-list.mnet  + h-umsatz.betrag / fact. 
          cl-list.mgros = cl-list.mgros + h-umsatz.betrag. 
          cl-list.mqty  = cl-list.mqty  + h-umsatz.anzahl. 
          mnet  = mnet  + h-umsatz.betrag / fact. 
          mgros = mgros + h-umsatz.betrag. 
          mqty  = mqty  + h-umsatz.anzahl. 
        END.
        cl-list.ynet  = cl-list.ynet + h-umsatz.betrag / fact. 
        cl-list.ygros = cl-list.ygros + h-umsatz.betrag. 
        cl-list.yqty  = cl-list.yqty + h-umsatz.anzahl. 
        ynet  = ynet  + h-umsatz.betrag / fact. 
        ygros = ygros + h-umsatz.betrag. 
        yqty  = yqty  + h-umsatz.anzahl. 
      END. 
    END. 
    FOR EACH cl-list WHERE cl-list.dept = hoteldpt.num: 
      IF dnet  NE 0 THEN cl-list.proz1 = cl-list.dnet / dnet * 100. 
      IF dgros NE 0 THEN cl-list.proz2 = cl-list.dgros / dgros * 100. 
      IF mnet  NE 0 THEN cl-list.proz3 = cl-list.mnet / mnet * 100. 
      IF mgros NE 0 THEN cl-list.proz4 = cl-list.mgros / mgros * 100. 
      IF ynet  NE 0 THEN cl-list.proz5 = cl-list.ynet / ynet * 100. 
      IF ygros NE 0 THEN cl-list.proz6 = cl-list.ygros / ygros * 100. 
    END. 
    create cl-list. 
    cl-list.flag = "**". 
    cl-list.bezeich = "T O T A L". 
    cl-list.dnet = dnet. 
    IF dnet NE 0 THEN cl-list.proz1 = 100. 
    cl-list.dgros = dgros. 
    IF dgros NE 0 THEN cl-list.proz2 = 100. 
    cl-list.mnet = mnet. 
    IF mnet NE 0 THEN cl-list.proz3 = 100. 
    cl-list.mgros = mgros. 
    IF mgros NE 0 THEN cl-list.proz4 = 100. 
    cl-list.dqty = dqty. /* Naufal Afthar - 9513B5*/
    cl-list.mqty = mqty. 
    cl-list.ynet = ynet. 
    IF ynet NE 0 THEN cl-list.proz5 = 100. 
    cl-list.ygros = ygros. 
    IF ygros NE 0 THEN cl-list.proz6 = 100. 
    cl-list.yqty = yqty. 
  END. 
 
  FOR EACH cl-list NO-LOCK: 
    IF cl-list.flag = "*" THEN 
    DO: 
      /* Malik Serverless 387 comment    
      create output-list. 
      output-list.str = STRING(cl-list.artnr, ">>>>>>>>>") + STRING(cl-list.bezeich, "x(24)"). */
      CREATE turn-reportlist.
      ASSIGN
        turn-reportlist.artno   = INTEGER(STRING(cl-list.artnr, ">>>>>>>>>")).
        /*turn-reportlist.descr   = STRING(cl-list.bezeich, "x(24)").*/
    END. 
    ELSE IF cl-list.flag = "" THEN 
    DO: 
        do-it = NO. 
        IF detailed OR cl-list.mgros NE 0 THEN do-it = YES. 
        IF do-it THEN 
        DO: 
          /* Malik Serverless 387 comment    
          CREATE output-list. 
          output-list.dqty = cl-list.dqty. /* Naufal Afthar - 9513B5*/
          output-list.mqty = cl-list.mqty. 
          output-list.yqty = cl-list.yqty. */
          CREATE turn-reportlist.
          turn-reportlist.dqty          = cl-list.dqty. 
          turn-reportlist.mqty          = cl-list.mqty.
          turn-reportlist.yqty          = cl-list.yqty.
          IF NOT long-digit THEN 
          DO:
            /* Malik Serverless 378 comment 
            output-list.str = STRING(cl-list.artnr, ">>>>>>>>>") 
                                + STRING(cl-list.bezeich, "x(24)") 
                                + STRING(cl-list.dnet, "->>,>>>,>>9.99") 
                                + STRING(cl-list.dgros, "->>,>>>,>>9.99").
            
            ASSIGN output-list.bezeich = cl-list.bezeich. /* Naufal Afthar - AFB4A4*/
            
            IF cl-list.proz2 GT 999 OR cl-list.proz2 LT -999 THEN
            output-list.str = output-list.str + STRING(cl-list.proz2, "->>,>>9").
            ELSE
            output-list.str = output-list.str + STRING(cl-list.proz2, "->>9.99").                             
            output-list.str = output-list.str
                                + STRING(cl-list.mnet, "->>>,>>>,>>9.99") 
                                + STRING(cl-list.mgros, "->>>,>>>,>>9.99").
            IF cl-list.proz4 GT 999 OR cl-list.proz4 LT -999 THEN
            output-list.str = output-list.str + STRING(cl-list.proz4, "->>,>>9").
            ELSE
            output-list.str = output-list.str + STRING(cl-list.proz4, "->>9.99").                              
            output-list.str = output-list.str
                                + STRING(cl-list.ynet, "->>>,>>>,>>9.99") 
                                + STRING(cl-list.ygros, "->>>,>>>,>>9.99").
            IF cl-list.proz6 GT 999 OR cl-list.proz6 LT -999 THEN
            output-list.str = output-list.str + STRING(cl-list.proz6, "->>,>>9").
            ELSE
            output-list.str = output-list.str + STRING(cl-list.proz6, "->>9.99"). */
            turn-reportlist.artno       = INTEGER(STRING(cl-list.artnr, ">>>>>>>>>")).
            turn-reportlist.day-net     = DECIMAL(STRING(cl-list.dnet, "->>,>>>,>>9.99")).
            turn-reportlist.day-gros    = DECIMAL(STRING(cl-list.dgros, "->>,>>>,>>9.99")).
            turn-reportlist.descr       = cl-list.bezeich.

            IF cl-list.proz2 GT 999 OR cl-list.proz2 LT -999 THEN
            DO:
                /* 
                output-list.str = output-list.str + STRING(cl-list.proz2, "->>,>>9").*/
                turn-reportlist.day-proz      = DECIMAL(STRING(cl-list.proz2, "->>,>>9")).
            END.
            ELSE
            DO:
                /* 
                output-list.str = output-list.str + STRING(cl-list.proz2, "->>9.99").                             
                */
                turn-reportlist.day-proz    = DECIMAL(STRING(cl-list.proz2, "->>9.99")).                
            END.
            turn-reportlist.todate-mnet = DECIMAL(STRING(cl-list.mnet, "->>>,>>>,>>9.99")).
            turn-reportlist.todate-mgros    = DECIMAL(STRING(cl-list.mgros, "->>>,>>>,>>9.99")). 
            IF cl-list.proz4 GT 999 OR cl-list.proz4 LT -999 THEN
            DO:
                /* 
                output-list.str = output-list.str + STRING(cl-list.proz4, "->>,>>9").*/
                turn-reportlist.todate-mproz  = DECIMAL(STRING(cl-list.proz4, "->>,>>9")).
            END.
            ELSE
            DO:
                /* 
                output-list.str = output-list.str + STRING(cl-list.proz4, "->>9.99").*/
                turn-reportlist.todate-mproz    =  DECIMAL(STRING(cl-list.proz4, "->>9.99")).

            END. 
            /*                             
            output-list.str = output-list.str
                                + STRING(cl-list.ynet, "->>>,>>>,>>9.99") 
                                + STRING(cl-list.ygros, "->>>,>>>,>>9.99").*/
            turn-reportlist.todate-ynet   = DECIMAL(STRING(cl-list.ynet, "->>>,>>>,>>9.99")).
            turn-reportlist.todate-ygros  = DECIMAL(STRING(cl-list.ygros, "->>>,>>>,>>9.99")).

            IF cl-list.proz6 GT 999 OR cl-list.proz6 LT -999 THEN
            DO:
                /* 
                output-list.str = output-list.str + STRING(cl-list.proz6, "->>,>>9").*/
                turn-reportlist.todate-yproz  = DECIMAL(STRING(cl-list.proz6, "->>,>>9")).
            END.
            ELSE
            DO:
                /* 
                output-list.str = output-list.str + STRING(cl-list.proz6, "->>9.99"). */
                turn-reportlist.todate-yproz  = DECIMAL(STRING(cl-list.proz6, "->>9.99")).
            END.
          END.
          ELSE
          DO:
              /* Malik Serverless 378 comment 
              output-list.str = STRING(cl-list.artnr, ">>>>>>>>>") 
                                + STRING(cl-list.bezeich, "x(24)") 
                                + STRING(cl-list.dnet, "->,>>>,>>>,>>9") 
                                + STRING(cl-list.dgros, "->,>>>,>>>,>>9")
                                + STRING(cl-list.proz2, "->>9.99") 
                                + STRING(cl-list.mnet, "->>,>>>,>>>,>>9") 
                                + STRING(cl-list.mgros, "->>,>>>,>>>,>>9") 
                                + STRING(cl-list.proz4, "->>9.99")
                                + STRING(cl-list.ynet, "->>,>>>,>>>,>>9") 
                                + STRING(cl-list.ygros, "->>,>>>,>>>,>>9") 
                                + STRING(cl-list.proz6, "->>9.99"). 

              ASSIGN output-list.bezeich = cl-list.bezeich. /* Naufal Afthar - AFB4A4*/*/
              turn-reportlist.artno         = INT(STRING(cl-list.artnr, ">>>>>>>>>")).  
              turn-reportlist.descr         = cl-list.bezeich.
              turn-reportlist.day-net       = DECIMAL(STRING(cl-list.dnet, "->,>>>,>>>,>>9")).
              turn-reportlist.day-gros      = DECIMAL(STRING(cl-list.dgros, "->,>>>,>>>,>>9")).
              turn-reportlist.day-proz      = DECIMAL(STRING(cl-list.proz2, "->>9.99")). 
              turn-reportlist.todate-mnet   = DECIMAL(STRING(cl-list.mnet, "->>,>>>,>>>,>>9")).
              turn-reportlist.todate-mgros  = DECIMAL(STRING(cl-list.mgros, "->>,>>>,>>>,>>9")).
              turn-reportlist.todate-mproz  = DECIMAL(STRING(cl-list.proz4, "->>9.99")). 
              turn-reportlist.todate-ynet   = DECIMAL(STRING(cl-list.ynet, "->>,>>>,>>>,>>9")).
              turn-reportlist.todate-ygros  = DECIMAL(STRING(cl-list.ygros, "->>,>>>,>>>,>>9")).
              turn-reportlist.todate-yproz  = DECIMAL(STRING(cl-list.proz6, "->>9.99")).
          END.
        END. 
    END. 
    ELSE IF cl-list.flag = "**" THEN 
    DO: 
      /* Malik Serverless 378 comment 
      create output-list. 
      output-list.dqty = cl-list.dqty. /* Naufal Afthar - 9513B5*/
      output-list.mqty = cl-list.mqty. 
      output-list.yqty = cl-list.yqty.*/
      CREATE turn-reportlist.
      turn-reportlist.dqty          = cl-list.dqty.
      turn-reportlist.mqty          = cl-list.mqty.
      turn-reportlist.yqty          = cl-list.yqty.

      IF NOT long-digit THEN 
      DO:
        /* 
        output-list.str = STRING(cl-list.artnr, ">>>>>>>>>") 
                                + STRING(cl-list.bezeich, "x(24)") 
                                + STRING(cl-list.dnet, "->>,>>>,>>9.99") 
                                + STRING(cl-list.dgros, "->>,>>>,>>9.99").

        ASSIGN output-list.bezeich = cl-list.bezeich. /* Naufal Afthar - AFB4A4*/ 

        IF cl-list.proz2 GT 999 OR cl-list.proz2 LT -999 THEN
        output-list.str = output-list.str + STRING(cl-list.proz2, "->>,>>9").
        ELSE
        output-list.str = output-list.str + STRING(cl-list.proz2, "->>9.99").                             
        output-list.str = output-list.str
                                + STRING(cl-list.mnet, "->>>,>>>,>>9.99") 
                                + STRING(cl-list.mgros, "->>>,>>>,>>9.99").
        IF cl-list.proz4 GT 999 OR cl-list.proz4 LT -999 THEN
        output-list.str = output-list.str + STRING(cl-list.proz4, "->>,>>9").
        ELSE
        output-list.str = output-list.str + STRING(cl-list.proz4, "->>9.99"). 
        output-list.str = output-list.str
                                + STRING(cl-list.ynet, "->>>,>>>,>>9.99") 
                                + STRING(cl-list.ygros, "->>>,>>>,>>9.99").
        IF cl-list.proz6 GT 999 OR cl-list.proz6 LT -999 THEN
        output-list.str = output-list.str + STRING(cl-list.proz6, "->>,>>9").
        ELSE
        output-list.str = output-list.str + STRING(cl-list.proz6, "->>9.99").*/
        turn-reportlist.artno           = INT(STRING(cl-list.artnr, ">>>>>>>>>")).
        turn-reportlist.day-net         = DECIMAL(STRING(cl-list.dnet, "->>,>>>,>>9.99")).
        turn-reportlist.day-gros        = DECIMAL(STRING(cl-list.dgros, "->>,>>>,>>9.99")).
        turn-reportlist.descr           = cl-list.bezeich.

        IF cl-list.proz2 GT 999 OR cl-list.proz2 LT -999 THEN
        DO:
            /* 
            output-list.str = output-list.str + STRING(cl-list.proz2, "->>,>>9").*/
            turn-reportlist.day-proz      = DECIMAL(STRING(cl-list.proz2, "->>,>>9")).

        END.
        ELSE
        DO:
            /* 
            output-list.str = output-list.str + STRING(cl-list.proz2, "->>9.99").*/
            turn-reportlist.day-proz    = DECIMAL(STRING(cl-list.proz2, "->>9.99")).                
        END.  
        /*                            
        output-list.str = output-list.str
                                + STRING(cl-list.mnet, "->>>,>>>,>>9.99") 
                                + STRING(cl-list.mgros, "->>>,>>>,>>9.99").*/

        turn-reportlist.todate-mnet     = DECIMAL(STRING(cl-list.mnet, "->>>,>>>,>>9.99")).
        turn-reportlist.todate-mgros    = DECIMAL(STRING(cl-list.mgros, "->>>,>>>,>>9.99")). 

        IF cl-list.proz4 GT 999 OR cl-list.proz4 LT -999 THEN
        DO:
            /* 
            output-list.str = output-list.str + STRING(cl-list.proz4, "->>,>>9").*/
            turn-reportlist.todate-mproz  = DECIMAL(STRING(cl-list.proz4, "->>,>>9")).

        END.
        ELSE
        DO:
            /* 
            output-list.str = output-list.str + STRING(cl-list.proz4, "->>9.99"). */
            turn-reportlist.todate-mproz    =  DECIMAL(STRING(cl-list.proz4, "->>9.99")).

        END.
        /* 
        output-list.str = output-list.str
                                + STRING(cl-list.ynet, "->>>,>>>,>>9.99") 
                                + STRING(cl-list.ygros, "->>>,>>>,>>9.99").*/

        turn-reportlist.todate-ynet   = DECIMAL(STRING(cl-list.ynet, "->>>,>>>,>>9.99")).
        turn-reportlist.todate-ygros  = DECIMAL(STRING(cl-list.ygros, "->>>,>>>,>>9.99")).

        IF cl-list.proz6 GT 999 OR cl-list.proz6 LT -999 THEN
        DO:
            /* 
            output-list.str = output-list.str + STRING(cl-list.proz6, "->>,>>9").*/
            turn-reportlist.todate-yproz  = DECIMAL(STRING(cl-list.proz6, "->>,>>9")).

        END.
        ELSE
        DO:
            /* 
            output-list.str = output-list.str + STRING(cl-list.proz6, "->>9.99").*/
            turn-reportlist.todate-yproz  = DECIMAL(STRING(cl-list.proz6, "->>9.99")).
        END.
      END.
      ELSE 
      DO:
          /* 
          output-list.str = STRING(cl-list.artnr, ">>>>>>>>>") 
                                + STRING(cl-list.bezeich, "x(24)") 
                                + STRING(cl-list.dnet, "->,>>>,>>>,>>9") 
                                + STRING(cl-list.dgros, "->,>>>,>>>,>>9") 
                                + STRING(cl-list.proz2, "->>9.99") 
                                + STRING(cl-list.mnet, "->>,>>>,>>>,>>9") 
                                + STRING(cl-list.mgros, "->>,>>>,>>>,>>9") 
                                + STRING(cl-list.proz4, "->>9.99")
                                + STRING(cl-list.ynet, "->>,>>>,>>>,>>9") 
                                + STRING(cl-list.ygros, "->>,>>>,>>>,>>9") 
                                + STRING(cl-list.proz6, "->>9.99"). 
          
          ASSIGN output-list.bezeich = cl-list.bezeich. /* Naufal Afthar - AFB4A4*/*/
          turn-reportlist.artno         = INT(STRING(cl-list.artnr, ">>>>>>>>>")).  
          turn-reportlist.descr         = cl-list.bezeich.
          turn-reportlist.day-net       = DECIMAL(STRING(cl-list.dnet, "->,>>>,>>>,>>9")).
          turn-reportlist.day-gros      = DECIMAL(STRING(cl-list.dgros, "->,>>>,>>>,>>9")).
          turn-reportlist.day-proz      = DECIMAL(STRING(cl-list.proz2, "->>9.99")). 
          turn-reportlist.todate-mnet   = DECIMAL(STRING(cl-list.mnet, "->>,>>>,>>>,>>9")).
          turn-reportlist.todate-mgros  = DECIMAL(STRING(cl-list.mgros, "->>,>>>,>>>,>>9")).
          turn-reportlist.todate-mproz  = DECIMAL(STRING(cl-list.proz4, "->>9.99")). 
          turn-reportlist.todate-ynet   = DECIMAL(STRING(cl-list.ynet, "->>,>>>,>>>,>>9")).
          turn-reportlist.todate-ygros  = DECIMAL(STRING(cl-list.ygros, "->>,>>>,>>>,>>9")).
          turn-reportlist.todate-yproz  = DECIMAL(STRING(cl-list.proz6, "->>9.99")).
      END.
       /*  
       create output-list. */
       CREATE turn-reportlist.
    END. 
  END. 
END. 








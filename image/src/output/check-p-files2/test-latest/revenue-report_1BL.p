
DEFINE TEMP-TABLE output-list 
  FIELD flag       AS CHAR 
  FIELD STR        AS CHAR 
  FIELD bezeich    AS CHAR
  FIELD tnett      AS DECIMAL
  FIELD mtd        AS DECIMAL
  FIELD mtd-budget AS DECIMAL
  FIELD ytd-budget AS DECIMAL
  FIELD lmon-mtd   AS DECIMAL
  FIELD lyear-mtd  AS DECIMAL
  FIELD lyear-ytd  AS DECIMAL
. 

DEFINE TEMP-TABLE cl-list 
  FIELD flag       AS CHAR 
  FIELD artnr      AS INTEGER 
  FIELD kum        AS INTEGER 
  FIELD dept       AS INTEGER 
  FIELD bezeich    AS CHAR 
  FIELD dnet       AS DECIMAL 
  FIELD mnet       AS DECIMAL 
  FIELD mbudget    AS DECIMAL 
  FIELD ynet       AS DECIMAL 
  FIELD lm-mnet    AS DECIMAL 
  FIELD ly-mnet    AS DECIMAL 
  FIELD ly-ynet    AS DECIMAL. 


DEFINE INPUT  PARAMETER sorttype   AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER long-digit AS LOGICAL NO-UNDO.
DEFINE INPUT  PARAMETER short-flag AS LOGICAL NO-UNDO.
DEFINE INPUT  PARAMETER from-date  AS DATE    NO-UNDO.
DEFINE INPUT  PARAMETER to-date    AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.


DEFINE VARIABLE fact1               AS INTEGER              NO-UNDO.
DEFINE VARIABLE price-decimal       AS INTEGER              NO-UNDO.
DEFINE VARIABLE curr-dept           AS CHAR FORMAT "x(20)"  NO-UNDO.
DEFINE VARIABLE curr-art            AS INTEGER              NO-UNDO.
DEFINE VARIABLE bezeich             AS CHAR FORMAT "x(24)"  NO-UNDO.
DEFINE VARIABLE datum               AS DATE                 NO-UNDO.
DEFINE VARIABLE ly-datum            AS DATE                 NO-UNDO.
DEFINE VARIABLE jan1                AS DATE                 NO-UNDO.
DEFINE VARIABLE ly-jan1             AS DATE                 NO-UNDO.
DEFINE VARIABLE lm-fdate            AS DATE                 NO-UNDO.
DEFINE VARIABLE lm-tdate            AS DATE                 NO-UNDO.
DEFINE VARIABLE ly-fdate            AS DATE                 NO-UNDO.
DEFINE VARIABLE ly-tdate            AS DATE                 NO-UNDO.
DEFINE VARIABLE fact                AS DECIMAL              NO-UNDO.
/* DEFINE VARIABLE ekum                AS INTEGER              NO-UNDO. */
DEFINE VARIABLE ekum-serverless     AS INTEGER              NO-UNDO. /* Malik serverless */

 
DEFINE VARIABLE dnet                AS DECIMAL              NO-UNDO.
DEFINE VARIABLE mnet                AS DECIMAL              NO-UNDO.
DEFINE VARIABLE ynet                AS DECIMAL              NO-UNDO.
DEFINE VARIABLE lm-mnet             AS DECIMAL              NO-UNDO.
DEFINE VARIABLE ly-mnet             AS DECIMAL              NO-UNDO.
DEFINE VARIABLE ly-ynet             AS DECIMAL              NO-UNDO.
 
DEFINE VARIABLE tdnet               AS DECIMAL INITIAL 0    NO-UNDO.
DEFINE VARIABLE tmnet               AS DECIMAL INITIAL 0    NO-UNDO.
DEFINE VARIABLE tynet               AS DECIMAL INITIAL 0    NO-UNDO.
DEFINE VARIABLE tlm-mnet            AS DECIMAL INITIAL 0    NO-UNDO.
DEFINE VARIABLE tly-mnet            AS DECIMAL INITIAL 0    NO-UNDO.
DEFINE VARIABLE tly-ynet            AS DECIMAL INITIAL 0    NO-UNDO.
 
DEFINE VARIABLE taxnr               AS INTEGER              NO-UNDO.
DEFINE VARIABLE servnr              AS INTEGER              NO-UNDO.
DEFINE VARIABLE do-it               AS LOGICAL              NO-UNDO.
 
DEFINE VARIABLE vat                 AS DECIMAL              NO-UNDO.
DEFINE VARIABLE serv                AS DECIMAL              NO-UNDO.
DEFINE VARIABLE nett-serv           AS DECIMAL              NO-UNDO.
DEFINE VARIABLE nett-tax            AS DECIMAL              NO-UNDO.
DEFINE VARIABLE nett-amt            AS DECIMAL              NO-UNDO.
DEFINE VARIABLE dept                AS INTEGER INITIAL -1   NO-UNDO.
DEFINE VARIABLE zwkum-serverless    AS INTEGER              NO-UNDO. /* Malik Serverless 129 : zwkum -> zwkum-serverless */
DEFINE VARIABLE serv-vat            AS LOGICAL              NO-UNDO.

DEFINE VARIABLE mbudget             AS DECIMAL              NO-UNDO.
DEFINE VARIABLE t-mbudget           AS DECIMAL              NO-UNDO.
DEFINE VARIABLE tmp-month           AS INTEGER. /* Malik Serverless */
DEFINE VARIABLE year-ly-jan1        AS INTEGER. /* Malik Serverless */
DEFINE VARIABLE num-year-ly-jan1    AS INTEGER. /* Malik Serverless for case 129 */
DEFINE VARIABLE year-ly-fdate       AS INTEGER. /* Malik Serverless */
DEFINE VARIABLE year-ly-tdate       AS INTEGER. /* Malik Serverless */
DEFINE VARIABLE num-year-datum      AS INTEGER. /* Malik Serverless */
DEFINE VARIABLE tmp-day             AS DATE.    /* Malik Serverless */



FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
serv-vat = htparam.flogical. 


ASSIGN
  jan1 = DATE(1, 1, year(from-date))
  num-year-ly-jan1 = year(jan1) - 1       /* Malik Serverless for case 129 */
  ly-jan1 = DATE(1, 1, num-year-ly-jan1).  /* Malik Serverless for case 129 */
  

IF sorttype = 1 THEN
DO:
  IF NOT long-digit OR NOT short-flag THEN fact1 = 1. 
  ELSE fact1 = 1000. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
  FOR EACH cl-list: 
    DELETE cl-list. 
  END. 
  
  FIND FIRST htparam WHERE paramnr = 132 NO-LOCK. 
  taxnr = htparam.finteger.                /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 133 NO-LOCK. 
  servnr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */ 
  
  
  tmp-month = MONTH(from-date) - 1.  /* Malik Serverless */

  IF month(to-date) GE 2 THEN 
  DO: 
    IF day(from-date) = 1 THEN 
      lm-fdate = DATE(tmp-month, 1, year(from-date)). /* Malik serverless : DATE(MONTH(from-date) - 1, 1, year(from-date)) -> DATE(tmp-month, 1, year(from-date)) */
    ELSE lm-fdate = from-date - 30. 
    tmp-day = to-date + 1.        /* Malik Serverless for case 129 */
    IF day(tmp-day) = 1 THEN  /* Malik Serverless for case 129 : day(to-date + 1) -> day(tmp-day) */
      lm-tdate = DATE(month(to-date), 1, year(to-date)) - 1. 
    ELSE lm-tdate = to-date - 30. 
  END. 
  ELSE /** January **/ 
  DO: 
    lm-fdate = from-date - 31. 
    lm-tdate = to-date - 31. 
  END. 
  
  year-ly-tdate = year(to-date) - 1.
  year-ly-fdate = year(from-date) - 1. /* Malik Serverless for case 129 */
                                           
  IF day(from-date) = 29 AND month(from-date) = 2 THEN 
    ly-fdate = DATE(2, 28, year-ly-fdate).                                     /* Malik Serverless for case 129 : year(from-date) - 1 -> year-ly-fdate */
  ELSE ly-fdate = DATE(month(from-date), day(from-date), year-ly-fdate). /* Malik Serverless for case 129 : year(from-date) - 1 -> year-ly-fdate */
  IF day(to-date) = 29 AND month(to-date) = 2 THEN 
    ly-tdate = DATE(2, 28, year-ly-tdate).                           /* Malik serverless 129 : year(to-date) - 1 -> year-ly-tdate */
  ELSE ly-tdate = DATE(month(to-date), day(to-date), year-ly-tdate). /* Malik serverless 129 : year(to-date) - 1 -> year-ly-tdate */
 
  FOR EACH hoteldpt NO-LOCK BY hoteldpt.num: 
    curr-dept = hoteldpt.depart. 
    IF dept = -1 THEN dept = hoteldpt.num. 
    IF dept NE hoteldpt.num THEN 
    DO: 
      CREATE cl-list. 
      ASSIGN 
          cl-list.bezeich   = "T o t a l"
          cl-list.flag      = "**"
          cl-list.dnet      = dnet 
          cl-list.mnet      = mnet 
          cl-list.mbudget   = mbudget
          cl-list.ynet      = ynet 
          cl-list.lm-mnet   = lm-mnet 
          cl-list.ly-mnet   = ly-mnet 
          cl-list.ly-ynet   = ly-ynet. 
      
       CREATE cl-list. 
       ASSIGN 
          dnet    = 0
          mnet    = 0 
          ynet    = 0 
          lm-mnet = 0 
          ly-mnet = 0 
          ly-ynet = 0
          mbudget = 0
          dept = hoteldpt.num. 
    END. 

    create cl-list. 
    cl-list.flag = "*". 
    cl-list.bezeich = hoteldpt.depart. 
    zwkum-serverless = 0. 

    FOR EACH artikel WHERE artikel.departement = hoteldpt.num AND (artikel.artart = 0 OR artikel.artart = 8) NO-LOCK BY artikel.zwkum:
    
      bezeich = STRING(artikel.artnr) + " - " + artikel.bezeich. 
      do-it = YES. 
      IF (artikel.artnr = taxnr OR artikel.artnr = servnr) 
        AND artikel.departement = 0 THEN do-it = NO. 
      IF do-it THEN 
      DO: 
        IF zwkum-serverless NE artikel.zwkum THEN 
        DO: 
          zwkum-serverless = artikel.zwkum. 
          FIND FIRST zwkum WHERE zwkum.zknr = artikel.zwkum 
            AND zwkum.departement = artikel.departement NO-LOCK NO-ERROR. 
        END. 
        
        FIND FIRST cl-list WHERE cl-list.kum = artikel.zwkum 
          AND cl-list.dept = artikel.departement NO-ERROR. 
        IF NOT AVAILABLE cl-list THEN 
        DO: 
          CREATE  cl-list. 
            cl-list.kum       = artikel.zwkum. 
            cl-list.artnr     = artikel.artnr. 
            cl-list.dept      = artikel.departement. 
          IF AVAILABLE zwkum THEN
            cl-list.bezeich   = zwkum.bezeich. 
        END. 

        DO datum = jan1 TO to-date: /* from jan 1 this year TO to-date */ 
          PROCESS EVENTS. 
          
          IF datum GE from-date THEN DO: 
               /*budget*/
            FIND FIRST budget WHERE budget.departement = artikel.departement
              AND budget.artnr = artikel.artnr AND budget.datum = datum NO-LOCK NO-ERROR.
            IF AVAILABLE budget THEN
              ASSIGN 
                cl-list.mbudget = cl-list.mbudget + budget.betrag
                mbudget         = mbudget + budget.betrag
                t-mbudget       = t-mbudget + budget.betrag.
          END.

          FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
            AND umsatz.departement = artikel.departement 
            AND umsatz.datum EQ datum NO-LOCK NO-ERROR. 
          IF AVAILABLE umsatz THEN 
          DO:
            ASSIGN
              fact = 0
              serv = 0
              vat = 0.
              
                /*ITA 020916 */
            RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, 
                               artikel.service-code, artikel.mwst-code, 
                               OUTPUT serv, OUTPUT vat).
            ASSIGN
              fact = 1.00 + serv + vat
              fact = fact * fact1
              nett-amt = umsatz.betrag / fact
              nett-serv = ROUND(nett-amt * serv, price-decimal)
              nett-tax =  ROUND(nett-amt * vat, price-decimal) 
              nett-amt = umsatz.betrag - nett-serv - nett-tax. 
            
            IF umsatz.datum = to-date THEN 
            DO: 
              ASSIGN
                cl-list.dnet = cl-list.dnet + nett-amt
                dnet = dnet + nett-amt
                tdnet = tdnet + nett-amt. 
            END. 
            
            IF datum GE from-date THEN 
            DO: 
              ASSIGN
                cl-list.mnet = cl-list.mnet + nett-amt
                mnet = mnet + nett-amt
                tmnet = tmnet + nett-amt. 
            END. 

            ASSIGN
              cl-list.ynet = cl-list.ynet + nett-amt
              ynet = ynet + nett-amt
              tynet = tynet + nett-amt. 
 
  /* LAST month MTD */ 
            IF datum GE lm-fdate AND datum LE lm-tdate THEN 
            DO: 
              cl-list.lm-mnet = cl-list.lm-mnet + nett-amt. 
              lm-mnet = lm-mnet + nett-amt. 
              tlm-mnet = tlm-mnet + nett-amt. 
            END. 
          END. 

  /* LAST year same DATE */ 
          IF day(datum) = 29 AND month(datum) = 2 THEN. 
          ELSE 
          DO: 
            num-year-datum = year(datum) - 1. /* Malik Serverless 129 */
            ly-datum = DATE(month(datum), day(datum), num-year-datum). /* Malik serverless 129 : year(datum) - 1 -> num-year-datum */
            FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
              AND umsatz.departement = artikel.departement 
              AND umsatz.datum EQ ly-datum NO-LOCK NO-ERROR. 
            IF AVAILABLE umsatz THEN 
            DO: 
              ASSIGN
                fact = 0
                serv = 0
                vat = 0.
                /*ITA 020916 */
              RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, 
                                 artikel.service-code, artikel.mwst-code, 
                                 OUTPUT serv, OUTPUT vat).
              ASSIGN
                fact = 1.00 + serv + vat
                fact = fact * fact1
                nett-amt = umsatz.betrag / fact
                nett-serv = ROUND(nett-amt * serv, price-decimal)
                nett-tax =  ROUND(nett-amt * vat, price-decimal) 
                nett-amt = umsatz.betrag - nett-serv - nett-tax. 

              IF ly-datum GE ly-fdate THEN 
              DO:
                cl-list.ly-mnet = cl-list.ly-mnet + nett-amt. 
                ly-mnet = ly-mnet + nett-amt. 
                tly-mnet = tly-mnet + nett-amt. 
              END. 
              
              ASSIGN
                cl-list.ly-ynet = cl-list.ly-ynet + nett-amt. 
                ly-ynet = ly-ynet + nett-amt. 
                tly-ynet = tly-ynet + nett-amt. 
            END. 
          END.
        END. 
      END. 
    END. 
  END. 
 
  CREATE cl-list. 
  ASSIGN 
      cl-list.kum           = zwkum-serverless
      cl-list.bezeich       = "T o t a l"
      cl-list.flag          = "**" 
      cl-list.dnet          = dnet 
      cl-list.mnet          = mnet
      cl-list.mbudget       = mbudget
      cl-list.ynet          = ynet 
      cl-list.lm-mnet       = lm-mnet
      cl-list.ly-mnet       = ly-mnet 
      cl-list.ly-ynet       = ly-ynet. 
 
  CREATE cl-list. 
  CREATE cl-list. 
  ASSIGN
        cl-list.bezeich = "Grand T o t a l"
        cl-list.flag    = "***" 
        cl-list.dnet    = tdnet 
        cl-list.mnet    = tmnet
        cl-list.mbudget = t-mbudget
        cl-list.ynet    = tynet 
        cl-list.lm-mnet = tlm-mnet
        cl-list.ly-mnet = tly-mnet
        cl-list.ly-ynet = tly-ynet. 
 
  
  FOR EACH cl-list: 
    create output-list. 
    IF cl-list.bezeich NE "" THEN 
    DO: 
      output-list.flag = cl-list.flag. 
      output-list.str = STRING(cl-list.bezeich, "x(24)"). /* Malik Serverless : STR -> str-serverless, rollback jadi output-list.str */
      IF cl-list.flag NE "*" THEN 
      DO: 
        IF price-decimal = 2 THEN
        output-list.str = output-list.str /* Malik Serverless : STR -> output-list.str, rollback dari str-serverless */
          + STRING(cl-list.dnet, "->>>,>>9.99") 
          + STRING(cl-list.mnet, "->>>>,>>9.99") 
          + STRING(cl-list.mbudget, "->,>>>,>>9.99") 
          + STRING(cl-list.ynet, "->>,>>>,>>9.99") 
          + STRING(cl-list.lm-mnet, "->>>>,>>9.99") 
          + STRING(cl-list.ly-mnet, "->>>>,>>9.99") 
          + STRING(cl-list.ly-ynet, "->>,>>>,>>9.99"). 
        ELSE IF NOT long-digit OR (long-digit AND short-flag) THEN      
        output-list.str = output-list.str /* Malik Serverless : STR -> output-list.str, rollback dari str-serverless */
          + STRING(cl-list.dnet, "->>,>>>,>>9") 
          + STRING(cl-list.mnet, "->>>,>>>,>>9") 
          + STRING(cl-list.mbudget, "->>>,>>>,>>9") 
          + STRING(cl-list.ynet, "->,>>>,>>>,>>9") 
          + STRING(cl-list.lm-mnet, "->>>,>>>,>>9") 
          + STRING(cl-list.ly-mnet, "->>>,>>>,>>9") 
          + STRING(cl-list.ly-ynet, "->,>>>,>>>,>>9"). 
        ELSE output-list.str = output-list.str /* Malik Serverless : STR -> output-list.str, rollback dari str-serverless */
          + STRING(cl-list.dnet, "->>>>>>>>>9") 
          + STRING(cl-list.mnet, "->>>>>>>>>>9") 
          + STRING(cl-list.mbudget, "->>>>>>>>>>9") 
          + STRING(cl-list.ynet, "->>>>>>>>>>>>9") 
          + STRING(cl-list.lm-mnet, "->>>>>>>>>>9") 
          + STRING(cl-list.ly-mnet, "->>>>>>>>>>9") 
          + STRING(cl-list.ly-ynet, "->>>>>>>>>>>>9"). 

        ASSIGN 
            output-list.bezeich         = cl-list.bezeich
            output-list.tnett           = cl-list.dnet
            output-list.mtd             = cl-list.mnet
            output-list.mtd-budget      = cl-list.mbudget
            output-list.ytd-budget      = cl-list.ynet
            output-list.lmon-mtd        = cl-list.lm-mnet
            output-list.lyear-mtd       = cl-list.ly-mnet
            output-list.lyear-ytd       = cl-list.ly-ynet
         .
      END. 
    END. 
  END. 
END. 

IF sorttype = 2 THEN
DO:
  IF NOT long-digit OR NOT short-flag THEN fact1 = 1. 
  ELSE fact1 = 1000. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
  
  FIND FIRST htparam WHERE paramnr = 132 NO-LOCK. 
  taxnr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 133 NO-LOCK. 
  servnr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

 
  
  year-ly-fdate = year(from-date) - 1. /* Malik Serverless */
  year-ly-tdate = year(to-date) - 1.
  tmp-day = to-date + 1.
  tmp-month = MONTH(from-date) - 1.  /* Malik Serverless */  
  IF MONTH(to-date) GE 2 THEN 
  DO: 
    IF DAY(from-date) = 1 THEN 
      lm-fdate = DATE(tmp-month, 1, YEAR(from-date)). /* Malik serverless : DATE(MONTH(from-date) - 1, 1, year(from-date)) -> DATE(tmp-month, 1, year(from-date)) */ 
    ELSE lm-fdate = from-date - 30. 
    IF DAY(tmp-day) = 1 THEN /* Malik Serverless : day(to-date + 1) -> day(tmp-day) */
      lm-tdate = DATE(MONTH(to-date), 1, YEAR(to-date)) - 1. 
    ELSE lm-tdate = to-date - 30. 
  END. 
  ELSE /** January **/ 
  DO: 
    lm-fdate = from-date - 31. 
    lm-tdate = to-date - 31. 
  END. 
 
  IF day(from-date) = 29 AND month(from-date) = 2 THEN 
    ly-fdate = DATE(2, 28, year-ly-fdate). /* Malik Serverless : year(from-date) - 1 -> year-ly-fdate */
  ELSE ly-fdate = DATE(month(from-date), day(from-date), year-ly-fdate). /* Malik Serverless : year(from-date) - 1 -> year-ly-fdate */
  IF day(to-date) = 29 AND month(to-date) = 2 THEN 
    ly-tdate = DATE(2, 28, year-ly-tdate). /* Malik Serverless : year(to-date) - 1 -> year-ly-tdate */
  ELSE ly-tdate = DATE(month(to-date), day(to-date), year-ly-tdate). /* Malik Serverless : year(to-date) - 1 -> year-ly-tdate */
 
  ekum-serverless = 0. /* Malik serverless : ekum -> ekum-serverless */
  FOR EACH artikel WHERE (artikel.artart = 0 OR artikel.artart = 8) 
    /* lodging AND artikel.activeflag*/ NO-LOCK 
    BY artikel.endkum BY artikel.bezeich: 
 
 
    FIND FIRST hoteldpt WHERE hoteldpt.num = artikel.departement NO-LOCK NO-ERROR. 
    IF AVAILABLE hoteldpt THEN
    DO:
      curr-dept = hoteldpt.depart. 
      bezeich = STRING(artikel.artnr) + " - " + artikel.bezeich. 
    END.
    
    do-it = YES. 
    
    IF (artikel.artnr = taxnr OR artikel.artnr = servnr) 
      AND artikel.departement = 0 THEN do-it = NO. 
    IF do-it THEN 
    DO: 
      IF ekum-serverless = 0 THEN 
      DO: 
        ekum-serverless = artikel.endkum. 
        FIND FIRST ekum WHERE ekum.eknr = artikel.endkum NO-LOCK NO-ERROR. 
        CREATE cl-list. 
        ASSIGN
          cl-list.flag = "**"
          cl-list.kum = artikel.endkum.
        IF AVAILABLE ekum THEN
          cl-list.bezeich = ekum.bezeich. 
      END. 

      IF ekum-serverless NE artikel.endkum THEN 
      DO:
        ASSIGN
          cl-list.dnet = dnet 
          cl-list.mnet = mnet 
          cl-list.mbudget   = mbudget
          cl-list.ynet = ynet 
          cl-list.lm-mnet = lm-mnet
          cl-list.ly-mnet = ly-mnet 
          cl-list.ly-ynet = ly-ynet 
          ekum-serverless = artikel.endkum. 
        FIND FIRST ekum WHERE ekum.eknr = artikel.endkum NO-LOCK NO-ERROR. 
        CREATE cl-list. 
        ASSIGN
          dnet = 0
          mnet = 0 
          ynet = 0 
          lm-mnet = 0
          ly-mnet = 0 
          ly-ynet = 0
          mbudget = 0.
        CREATE cl-list.
        ASSIGN
          cl-list.flag = "**"
          cl-list.kum = artikel.endkum.
        IF AVAILABLE ekum THEN
          cl-list.bezeich = ekum.bezeich. 
      END. 
      /*RUN calc-servvat.p(artikel.depart, artikel.artnr, to-date, 
          artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
      fact = 1.00 + serv + vat. 
      fact = fact * fact1. */
      
      FIND FIRST cl-list WHERE cl-list.kum = artikel.endkum NO-ERROR. 
      IF NOT AVAILABLE cl-list THEN 
      DO: 
        CREATE cl-list. 
        ASSIGN
          cl-list.kum = artikel.endkum. 
        IF AVAILABLE ekum THEN
          cl-list.bezeich = ekum.bezeich. 
      END. 
      DO datum = jan1 TO to-date: /* from jan 1 this year TO to-date */ 
        
        IF datum GE from-date THEN
        DO: 
            /*budget*/
          FIND FIRST budget WHERE budget.departement = artikel.departement
            AND budget.artnr = artikel.artnr AND budget.datum = datum NO-LOCK NO-ERROR.
          IF AVAILABLE budget THEN
            ASSIGN 
              cl-list.mbudget = cl-list.mbudget + budget.betrag
              mbudget         = mbudget + budget.betrag
              t-mbudget       = t-mbudget + budget.betrag.
        END.

        FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
          AND umsatz.departement = artikel.departement 
          AND umsatz.datum EQ datum NO-LOCK NO-ERROR. 
        IF AVAILABLE umsatz THEN 
        DO: 
          ASSIGN
            fact = 0
            serv = 0
            vat = 0.
                /*ITA 020916 */
          RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, 
                             artikel.service-code, artikel.mwst-code, 
                             OUTPUT serv, OUTPUT vat).
          ASSIGN
            fact = 1.00 + serv + vat
            fact = fact * fact1
            nett-amt = umsatz.betrag / fact 
            nett-serv = ROUND(nett-amt * serv, price-decimal)
            nett-tax =  ROUND(nett-amt * vat, price-decimal) 
            nett-amt = umsatz.betrag - nett-serv - nett-tax. 

          IF umsatz.datum = to-date THEN 
          DO: 
            ASSIGN
              cl-list.dnet = cl-list.dnet + nett-amt
              dnet = dnet + nett-amt
              tdnet = tdnet + nett-amt. 
          END. 

          IF datum GE from-date THEN 
          DO:
            ASSIGN
              cl-list.mnet = cl-list.mnet + nett-amt
              mnet = mnet + nett-amt
              tmnet = tmnet + nett-amt. 
          END.

          ASSIGN
            cl-list.ynet = cl-list.ynet + nett-amt
            ynet = ynet + nett-amt
            tynet = tynet + nett-amt. 
 
/* LAST month MTD */ 
          IF datum GE lm-fdate AND datum LE lm-tdate THEN 
          DO:
            ASSIGN
              cl-list.lm-mnet = cl-list.lm-mnet + nett-amt
              lm-mnet = lm-mnet + nett-amt. 
              tlm-mnet = tlm-mnet + nett-amt. 
          END. 
        END. 
 
/* LAST year same DATE */ 
        IF day(datum) = 29 AND month(datum) = 2 THEN. 
        ELSE 
        DO: 
          num-year-datum = year(datum) - 1. /* Malik Serverless */
          ly-datum = DATE(month(datum), day(datum), num-year-datum). /* Malik serverless : year(datum) - 1 -> num-year-datum */
          FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
            AND umsatz.departement = artikel.departement 
            AND umsatz.datum EQ ly-datum NO-LOCK NO-ERROR. 
          IF AVAILABLE umsatz THEN 
          DO: 
            ASSIGN
              fact = 0
              serv = 0
              vat = 0.
                /*ITA 020916 */
            RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, 
                               artikel.service-code, artikel.mwst-code, 
                               OUTPUT serv, OUTPUT vat).
            ASSIGN
              fact = 1.00 + serv + vat
              fact = fact * fact1
              nett-amt = umsatz.betrag / fact
              nett-serv = ROUND(nett-amt * serv, price-decimal)
              nett-tax =  ROUND(nett-amt * vat, price-decimal)
              nett-amt = umsatz.betrag - nett-serv - nett-tax. 

            IF ly-datum GE ly-fdate THEN 
            DO:
              ASSIGN
                cl-list.ly-mnet = cl-list.ly-mnet + nett-amt
                ly-mnet = ly-mnet + nett-amt
                tly-mnet = tly-mnet + nett-amt. 
            END. 
            ASSIGN
              cl-list.ly-ynet = cl-list.ly-ynet + nett-amt
              ly-ynet = ly-ynet + nett-amt
              tly-ynet = tly-ynet + nett-amt. 
          END. 
        END. 
      END. 
    END. 
  END. 
 
  ASSIGN
    cl-list.dnet = dnet
    cl-list.mnet = mnet 
    cl-list.mbudget  = mbudget
    cl-list.ynet = ynet 
    cl-list.lm-mnet = lm-mnet
    cl-list.ly-mnet = ly-mnet 
    cl-list.ly-ynet = ly-ynet. 
 
  CREATE cl-list. 
  CREATE cl-list. 
  ASSIGN
    cl-list.bezeich = "Grand T o t a l"
    cl-list.flag = "***"
    cl-list.dnet = tdnet 
    cl-list.mnet = tmnet 
    cl-list.mbudget = t-mbudget
    cl-list.ynet = tynet 
    cl-list.lm-mnet = tlm-mnet
    cl-list.ly-mnet = tly-mnet 
    cl-list.ly-ynet = tly-ynet. 
 
  FOR EACH cl-list: 
    create output-list. 
    IF cl-list.bezeich NE "" THEN 
    DO: 
      output-list.flag = cl-list.flag. 
      output-list.str = STRING(cl-list.bezeich, "x(24)"). /* Malik Serverless : STR -> output-list.str, rollback dari str-serverless */
      IF cl-list.flag NE "*" THEN 
      DO: 
        IF price-decimal = 2 THEN
        output-list.str = output-list.str /* Malik Serverless : STR -> output-list.str, rollback dari str-serverless */
          + STRING(cl-list.dnet, "->>>,>>9.99") 
          + STRING(cl-list.mnet, "->>>>,>>9.99") 
          + STRING(cl-list.mbudget, "->,>>>,>>9.99") 
          + STRING(cl-list.ynet, "->>,>>>,>>9.99") 
          + STRING(cl-list.lm-mnet, "->>>>,>>9.99") 
          + STRING(cl-list.ly-mnet, "->>>>,>>9.99") 
          + STRING(cl-list.ly-ynet, "->>,>>>,>>9.99"). 
        ELSE IF NOT long-digit OR (long-digit AND short-flag) THEN 
        output-list.str = output-list.str /* Malik Serverless : STR -> output-list.str, rollback dari str-serverless */
          + STRING(cl-list.dnet, "->>,>>>,>>9") 
          + STRING(cl-list.mnet, "->>>,>>>,>>9") 
          + STRING(cl-list.mbudget, "->>>,>>>,>>9") 
          + STRING(cl-list.ynet, "->,>>>,>>>,>>9") 
          + STRING(cl-list.lm-mnet, "->>>,>>>,>>9") 
          + STRING(cl-list.ly-mnet, "->>>,>>>,>>9") 
          + STRING(cl-list.ly-ynet, "->,>>>,>>>,>>9"). 
        ELSE output-list.str = output-list.str /* Malik Serverless : STR -> output-list.str, rollback dari str-serverless */
          + STRING(cl-list.dnet, "->>>>>>>>>9") 
          + STRING(cl-list.mnet, "->>>>>>>>>>9") 
          + STRING(cl-list.mbudget, "->>>>>>>>>>9") 
          + STRING(cl-list.ynet, "->>>>>>>>>>>>9") 
          + STRING(cl-list.lm-mnet, "->>>>>>>>>>9") 
          + STRING(cl-list.ly-mnet, "->>>>>>>>>>9") 
          + STRING(cl-list.ly-ynet, "->>>>>>>>>>>>9"). 

        ASSIGN 
            output-list.bezeich         = cl-list.bezeich
            output-list.tnett           = cl-list.dnet
            output-list.mtd             = cl-list.mnet
            output-list.mtd-budget      = cl-list.mbudget
            output-list.ytd-budget      = cl-list.ynet
            output-list.lmon-mtd        = cl-list.lm-mnet
            output-list.lyear-mtd       = cl-list.ly-mnet
            output-list.lyear-ytd       = cl-list.ly-ynet
         .
      END. 
    END. 
  END. 
END. 
/*
PROCEDURE cal-tax-service: 
DEFINE OUTPUT PARAMETER fact AS DECIMAL. 
DEFINE OUTPUT PARAMETER vat AS DECIMAL. 
DEFINE OUTPUT PARAMETER serv AS DECIMAL. 
  serv = 0. 
  vat = 0. 
  IF artikel.service-code NE 0 THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code NO-LOCK. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    serv = htparam.fdecimal / 100. 
  END. 
  IF artikel.mwst-code NE 0 THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code NO-LOCK. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    DO: 
      vat = htparam.fdecimal / 100. 
      IF serv-vat THEN vat = vat + vat * serv. 
      vat = round(vat, 2). 
    END. 
  END. 
  fact = 1.00 + serv + vat. 
  fact = fact * fact1. 
END.*/

DEFINE TEMP-TABLE subgr-list 
  FIELD SELECTED   AS LOGICAL INITIAL YES
  FIELD subnr      AS INTEGER 
  FIELD bezeich    AS CHAR    FORMAT "x(24)".
 
DEFINE TEMP-TABLE output-list 
  FIELD flag AS INTEGER 
  FIELD bezeich AS CHAR 
  FIELD s AS CHAR. 

DEFINE TEMP-TABLE h-list 
  FIELD flag       AS CHAR FORMAT "x(2)" INITIAL "" 
  FIELD artnr      AS INTEGER FORMAT ">>>>9" INITIAL 0 
  FIELD dept       AS INTEGER 
  FIELD bezeich    AS CHAR FORMAT "x(24)" INITIAL "" 
  FIELD zknr       AS INTEGER 
  FIELD grpname    AS CHAR FORMAT "x(24)" 
  FIELD anzahl     AS INTEGER FORMAT "->>>>9" INITIAL 0 
  FIELD proz1      AS DECIMAL FORMAT ">>9.99" INITIAL 0 
  FIELD epreis     AS DECIMAL FORMAT ">,>>>,>>9.99" INITIAL 0 
  FIELD cost       AS DECIMAL FORMAT ">,>>>,>>9.99" INITIAL 0 
  FIELD margin     AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD t-sales    AS DECIMAL FORMAT ">>,>>>,>>9.99" INITIAL 0 
  FIELD t-cost     AS DECIMAL FORMAT ">>,>>>,>>9.99" INITIAL 0 
  FIELD t-margin   AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD proz2      AS DECIMAL FORMAT ">>9.99" INITIAL 0.
   

/* Rulita 09/06/22 */
DEFINE TEMP-TABLE fb-cost-analyst 
    FIELD flag                AS INTEGER
    FIELD artnr               AS INTEGER FORMAT ">>>>>>>>9"          INITIAL 0 
    FIELD bezeich             AS CHAR    FORMAT "x(24)"          INITIAL "" 
    FIELD qty                 AS INTEGER FORMAT ">>>>>9"         INITIAL 0
    FIELD proz1               AS DECIMAL FORMAT ">>9.99"         INITIAL 0 
    FIELD epreis              AS DECIMAL FORMAT ">,>>>,>>9.99"   INITIAL 0 
    FIELD cost                AS DECIMAL FORMAT ">,>>>,>>9.99"   INITIAL 0  
    FIELD margin              AS DECIMAL FORMAT "->>>,>>9.99"    INITIAL 0
    FIELD t-sales             AS DECIMAL FORMAT ">>>,>>>,>>9.99" INITIAL 0 
    FIELD t-cost              AS DECIMAL FORMAT ">>>,>>>,>>9.99" INITIAL 0 
    FIELD t-margin            AS DECIMAL FORMAT "->,>>>,>>9.99"  INITIAL 0 
    FIELD proz2               AS DECIMAL FORMAT ">>9.99"         INITIAL 0
    FIELD item-profit         AS DECIMAL FORMAT ">>>,>>>,>>9.99" INITIAL 0 
    FIELD total-profit        AS DECIMAL FORMAT ">>>,>>>,>>9.99" INITIAL 0 
    FIELD profit-category     AS CHAR 
    FIELD popularity-category AS CHAR 
    FIELD menu-item-class     AS CHAR
    .

DEFINE TEMP-TABLE output-list2   /* Rulita 09/06/22 */
  FIELD flag            AS CHAR
  FIELD artnr           AS CHAR 
  FIELD dept            AS CHAR
  FIELD bezeich         AS CHAR 
  FIELD zknr            AS CHAR
  FIELD grpname         AS CHAR
  FIELD anzahl          AS CHAR 
  FIELD proz1           AS CHAR 
  FIELD epreis          AS CHAR 
  FIELD cost            AS CHAR 
  FIELD margin          AS CHAR 
  FIELD item-prof       AS CHAR 
  FIELD t-sales         AS CHAR 
  FIELD t-cost          AS CHAR 
  FIELD t-margin        AS CHAR 
  FIELD profit          AS CHAR 
  FIELD proz2           AS CHAR 
  FIELD profit-cat      AS CHAR 
  FIELD popularity-cat  AS CHAR 
  FIELD menu-item-class AS CHAR 
  FIELD s AS CHAR.

DEFINE INPUT PARAMETER TABLE FOR subgr-list.
DEFINE INPUT PARAMETER sorttype        AS INT.
DEFINE INPUT PARAMETER from-dept       AS INT.
DEFINE INPUT PARAMETER to-dept         AS INT.
DEFINE INPUT PARAMETER dstore          AS INT.
DEFINE INPUT PARAMETER ldry-dept       AS INT.
DEFINE INPUT PARAMETER all-sub         AS LOGICAL.
DEFINE INPUT PARAMETER from-date       AS DATE.
DEFINE INPUT PARAMETER to-date         AS DATE.
DEFINE INPUT PARAMETER fact1           AS INT.
DEFINE INPUT PARAMETER exchg-rate      AS DECIMAL.
DEFINE INPUT PARAMETER vat-included    AS LOGICAL.
DEFINE INPUT PARAMETER mi-subgrp       AS LOGICAL. /*MTMENU-ITEM mi-subgrp:CHECKED IN MENU mbar*/
DEFINE INPUT PARAMETER detailed        AS LOGICAL.
DEFINE INPUT PARAMETER curr-sort       AS INT.
DEFINE INPUT PARAMETER short-flag      AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR output-list2.

DEFINE VARIABLE t-anz     AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-sales   AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-cost    AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-margin  AS DECIMAL INITIAL 0.  
DEFINE VARIABLE st-sales  AS DECIMAL INITIAL 0 FORMAT ">>,>>>,>>9.99".
DEFINE VARIABLE st-cost   AS DECIMAL INITIAL 0 FORMAT ">>,>>>,>>9.99".
DEFINE VARIABLE st-margin AS DECIMAL INITIAL 0 FORMAT "->,>>>,>>9.99". /*Orig ->>9.99*/
DEFINE VARIABLE st-proz2  AS DECIMAL INITIAL 0 FORMAT ">>9.99".
DEFINE VARIABLE s-anzahl  AS INTEGER INITIAL 0 FORMAT "->>>>>9". 
DEFINE VARIABLE s-proz1   AS DECIMAL INITIAL 0 FORMAT ">>9.99". 

/* Rulita 09/06/22 */
DEFINE VARIABLE gtotal-sold      AS DECIMAL.
DEFINE VARIABLE gtotal-sold%     AS DECIMAL.
DEFINE VARIABLE gtotal-cost      AS DECIMAL.
DEFINE VARIABLE gtotal-revenue   AS DECIMAL.
DEFINE VARIABLE gtotal-profit    AS DECIMAL.
DEFINE VARIABLE avrg-item-profit AS DECIMAL.
DEFINE VARIABLE food-cost        AS DECIMAL.
DEFINE VARIABLE menu-pop-factor  AS DECIMAL.
DEFINE VARIABLE count-foodcost   AS DECIMAL.

DEFINE VARIABLE counter   AS INTEGER. /* Debugging */

/* Dzikri E248F5 - wrong cost price, NE recipe */
DEFINE VARIABLE price-type       AS INTEGER.

FIND FIRST htparam WHERE paramnr = 1024 NO-LOCK. 
price-type = htparam.finteger. 
/* Dzikri E248F5 - END */

IF sorttype = 1 THEN RUN create-h-umsatz1. 
ELSE IF sorttype = 2 THEN RUN create-h-umsatz2. 
ELSE IF sorttype = 3 THEN RUN create-h-umsatz3. /* ini yang dijalankan */

/* Rulita 09/06/22 */
FOR EACH output-list:
  counter = counter + 1.
    CREATE fb-cost-analyst.
    ASSIGN             
    fb-cost-analyst.flag         = output-list.flag
    fb-cost-analyst.bezeich      = output-list.bezeich
    fb-cost-analyst.artnr        = INTEGER(SUBSTRING(output-list.s,1,9))
    fb-cost-analyst.qty          = INTEGER(SUBSTRING(output-list.s,10,6)) 
    fb-cost-analyst.proz1        = DECIMAL(SUBSTRING(output-list.s,16,7))
    fb-cost-analyst.epreis       = DECIMAL(SUBSTRING(output-list.s,23,17)) 
    fb-cost-analyst.cost         = DECIMAL(SUBSTRING(output-list.s,40,17))
    fb-cost-analyst.margin       = DECIMAL(SUBSTRING(output-list.s,57,13))
    fb-cost-analyst.t-sales      = DECIMAL(SUBSTRING(output-list.s,70,17))
    fb-cost-analyst.t-cost       = DECIMAL(SUBSTRING(output-list.s,87,17))
    fb-cost-analyst.t-margin     = DECIMAL(SUBSTRING(output-list.s,104,13))
    fb-cost-analyst.proz2        = DECIMAL(SUBSTRING(output-list.s,117,7))
    fb-cost-analyst.item-profit  = fb-cost-analyst.epreis - fb-cost-analyst.cost
    fb-cost-analyst.total-profit = fb-cost-analyst.t-sales - fb-cost-analyst.t-cost
    .

    gtotal-sold    = gtotal-sold    + fb-cost-analyst.qty.
    gtotal-sold%   = gtotal-sold%   + fb-cost-analyst.proz1.
    gtotal-cost    = gtotal-cost    + fb-cost-analyst.t-cost.
    gtotal-revenue = gtotal-revenue + fb-cost-analyst.t-sales.
    gtotal-profit  = gtotal-profit  + fb-cost-analyst.total-profit.

    IF fb-cost-analyst.artnr NE 0 THEN count-foodcost = count-foodcost + 1.
END.
avrg-item-profit = gtotal-profit / gtotal-sold.
menu-pop-factor  = ((1 / count-foodcost) * 0.8 ).

FOR EACH fb-cost-analyst:
    IF fb-cost-analyst.item-profit LT avrg-item-profit THEN fb-cost-analyst.profit-category = "LOW".
    ELSE fb-cost-analyst.profit-category = "HIGH".

    IF fb-cost-analyst.proz1 LT menu-pop-factor THEN fb-cost-analyst.popularity-category = "LOW".
    ELSE fb-cost-analyst.popularity-category = "HIGH".
    
    IF fb-cost-analyst.profit-category EQ "LOW" AND fb-cost-analyst.popularity-category EQ "LOW" THEN fb-cost-analyst.menu-item-class = "DOG".   
    ELSE IF fb-cost-analyst.profit-category EQ "LOW" AND fb-cost-analyst.popularity-category EQ "HIGH" THEN fb-cost-analyst.menu-item-class = "WORKHORSE".
    ELSE IF fb-cost-analyst.profit-category EQ "HIGH" AND fb-cost-analyst.popularity-category EQ "LOW" THEN fb-cost-analyst.menu-item-class = "CHALLENGE".
    ELSE IF fb-cost-analyst.profit-category EQ "HIGH" AND fb-cost-analyst.popularity-category EQ "HIGH" THEN fb-cost-analyst.menu-item-class = "STAR".
END.

/* Rulita 09/06/22 */
FOR EACH fb-cost-analyst:
    CREATE output-list2.
    ASSIGN 
    output-list2.artnr           = STRING(fb-cost-analyst.artnr ,">>>>>>>>9")        
    output-list2.bezeich         = STRING(fb-cost-analyst.bezeich)     
    output-list2.anzahl          = STRING(fb-cost-analyst.qty ,"->>>>9")      
    output-list2.proz1           = STRING(fb-cost-analyst.proz1 ,"->>9.99")                 
    output-list2.epreis          = STRING(fb-cost-analyst.epreis ,"->,>>>,>>>,>>9.99")    
    output-list2.cost            = STRING(fb-cost-analyst.cost ,"->,>>>,>>>,>>9.99")                          
    output-list2.margin          = STRING(fb-cost-analyst.margin ,"->,>>>,>>9.99")                        
    output-list2.item-prof       = STRING(fb-cost-analyst.item-profit ,"->,>>>,>>>,>>9.99")            
    output-list2.t-sales         = STRING(fb-cost-analyst.t-sales ,"->,>>>,>>>,>>9.99")                 
    output-list2.t-cost          = STRING(fb-cost-analyst.t-cost ,"->,>>>,>>>,>>9.99")                   
    output-list2.t-margin        = STRING(fb-cost-analyst.t-margin ,"->,>>>,>>9.99")              
    output-list2.profit          = STRING(fb-cost-analyst.total-profit ,"->,>>>,>>>,>>9.99")          
    output-list2.proz2           = STRING(fb-cost-analyst.proz2 ,"->>9.99")                  
    output-list2.profit-cat      = STRING(fb-cost-analyst.profit-category)               
    output-list2.popularity-cat  = STRING(fb-cost-analyst.popularity-category)   
    output-list2.menu-item-class = STRING(fb-cost-analyst.menu-item-class)       
    .
END.

/* Rulita 09/06/22 */
FOR EACH output-list2:
    IF trim(output-list2.artnr) EQ "0" AND output-list2.bezeich NE "T o t a l"  THEN
    ASSIGN 
    output-list2.artnr           = STRING("")        
    output-list2.bezeich         = output-list2.bezeich     
    output-list2.anzahl          = STRING("")      
    output-list2.proz1           = STRING("")
    output-list2.epreis          = STRING("")    
    output-list2.cost            = STRING("")                        
    output-list2.margin          = STRING("")                      
    output-list2.item-prof       = STRING("")
    output-list2.t-sales         = STRING("")            
    output-list2.t-cost          = STRING("")             
    output-list2.t-margin        = STRING("")        
    output-list2.profit          = STRING("")          
    output-list2.proz2           = STRING("")
    output-list2.profit-cat      = STRING("")               
    output-list2.popularity-cat  = STRING("")   
    output-list2.menu-item-class = STRING("")
    .
    ELSE IF output-list2.bezeich EQ "T o t a l" THEN
    ASSIGN 
    output-list2.artnr           = STRING("")        
    output-list2.bezeich         = output-list2.bezeich
    output-list2.anzahl          = output-list2.anzahl       
    output-list2.proz1           = STRING(100,"->>9.99")                 
    output-list2.epreis          = STRING("")    
    output-list2.cost            = STRING("")                        
    output-list2.margin          = STRING("")                      
    output-list2.item-prof       = STRING("")
    output-list2.t-sales         = output-list2.t-sales                 
    output-list2.t-cost          = output-list2.t-cost                
    output-list2.t-margin        = output-list2.t-margin        
    output-list2.profit          = STRING("")          
    output-list2.proz2           = STRING(100,"->>9.99")                  
    output-list2.profit-cat      = STRING("")               
    output-list2.popularity-cat  = STRING("")   
    output-list2.menu-item-class = STRING("")       
    .
    ELSE IF output-list2.bezeich EQ "" THEN
    ASSIGN 
    output-list2.artnr           = STRING("")        
    output-list2.bezeich         = STRING("")     
    output-list2.anzahl          = STRING("")      
    output-list2.proz1           = STRING("")
    output-list2.epreis          = STRING("")    
    output-list2.cost            = STRING("")                        
    output-list2.margin          = STRING("")                      
    output-list2.item-prof       = STRING("")
    output-list2.t-sales         = STRING("")            
    output-list2.t-cost          = STRING("")             
    output-list2.t-margin        = STRING("")        
    output-list2.profit          = STRING("")          
    output-list2.proz2           = STRING("")
    output-list2.profit-cat      = STRING("")               
    output-list2.popularity-cat  = STRING("")   
    output-list2.menu-item-class = STRING("")
    .
END.

PROCEDURE create-h-umsatz1: 
    DEFINE VARIABLE disc-flag AS LOGICAL. 
    DEFINE VARIABLE disc-nr   AS INTEGER. 
    DEFINE VARIABLE dept      AS INTEGER INITIAL -1. 
    DEFINE VARIABLE pos       AS LOGICAL. 
    DEFINE VARIABLE datum     AS DATE. 
    DEFINE VARIABLE vat       AS DECIMAL. 
    DEFINE VARIABLE serv      AS DECIMAL. 
    DEFINE VARIABLE vat2      AS DECIMAL NO-UNDO.
    DEFINE VARIABLE serv-vat  AS LOGICAL. 
    DEFINE VARIABLE fact      AS DECIMAL.
    DEFINE VARIABLE do-it     AS LOGICAL INITIAL NO.
    DEFINE VARIABLE cost      AS DECIMAL. 
    DEFINE VARIABLE anz       AS INTEGER. 
     
    DEFINE BUFFER h-art   FOR h-artikel. 
    DEFINE BUFFER ph-list FOR h-list. 
     
    EMPTY TEMP-TABLE output-list.
    EMPTY TEMP-TABLE h-list.

    FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
        AND hoteldpt.num LE to-dept 
        AND hoteldpt.num NE dstore 
        AND hoteldpt.num NE ldry-dept NO-LOCK BY hoteldpt.num: 
        FIND FIRST h-artikel WHERE h-artikel.departement = hoteldpt.num NO-LOCK NO-ERROR. 
        IF AVAILABLE h-artikel THEN pos = YES. 
        ELSE pos = NO. 
        IF pos THEN 
        DO: 
            create output-list. 
            output-list.bezeich = STRING(hoteldpt.num,"99 ") + STRING(hoteldpt.depart,"x(21)"). 
        END. 
        dept = hoteldpt.num. 
        FOR EACH h-artikel WHERE h-artikel.artart = 0 
            AND h-artikel.departement = hoteldpt.num NO-LOCK,
            FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
            AND artikel.departement = h-artikel.departement 
            AND (artikel.umsatzart = 3 OR artikel.umsatzart = 5) 
            AND artikel.endkum NE disc-nr NO-LOCK BY h-artikel.bezeich: 
            do-it = NO.
            IF all-sub THEN do-it = YES.
            ELSE
            DO: 
                FIND FIRST subgr-list WHERE subgr-list.subnr = h-artikel.zwkum AND subgr-list.SELECTED NO-LOCK NO-ERROR.
                do-it = AVAILABLE subgr-list.
            END.
            IF do-it THEN
            DO: 
                /* Dzikri E248F5 - wrong cost price, NE recipe
                FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
                    AND h-cost.departement = h-artikel.departement 
                    AND h-cost.datum = to-date 
                    AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
                */
   
                RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,to-date, 
                                       OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
                ASSIGN vat = vat + vat2.
                
                CREATE h-list. 
                h-list.cost = 0.
                RUN fb-cost-count-recipe-costbl.p (h-artikel.artnrrezept, price-type, INPUT-OUTPUT h-list.cost).  
                /* 
                IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN h-list.cost = h-cost.betrag. 
                ELSE h-list.cost = h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                Dzikri E248F5 - END */
                h-list.cost      = h-list.cost / fact1. 
                h-list.dept      = h-artikel.departement. 
                h-list.artnr     = h-artikel.artnr. 
                h-list.dept      = h-artikel.departement. 
                h-list.bezeich   = h-artikel.bezeich. 
                h-list.zknr      = h-artikel.zwkum. 
                
                IF vat-included THEN h-list.epreis = h-artikel.epreis1 * exchg-rate / fact. 
                ELSE h-list.epreis = h-artikel.epreis1 * exchg-rate / fact1. 
                /*
                DO datum = from-date TO to-date: 
                    RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,datum, 
                                           OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
                    ASSIGN vat = vat + vat2.
                    FIND FIRST h-umsatz WHERE h-umsatz.artnr = h-artikel.artnr 
                        AND h-umsatz.departement = h-artikel.departement 
                        AND h-umsatz.datum EQ datum NO-LOCK NO-ERROR. 
                    IF AVAILABLE h-umsatz THEN 
                    DO: 
                        anz  = h-umsatz.anzahl. 
                        cost = 0. 
                        FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
                            AND h-cost.departement = h-artikel.departement 
                            AND h-cost.datum = datum AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
                        IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN
                        DO:
                            cost = anz * h-cost.betrag. 
                            h-list.cost = h-cost.betrag. 
                        END.
                        ELSE 
                        DO: 
                            FIND FIRST h-journal WHERE h-journal.artnr = h-artikel.artnr 
                                AND h-journal.departement = h-artikel.departement 
                                AND h-journal.bill-datum EQ datum NO-LOCK NO-ERROR. 
                            IF AVAILABLE h-journal THEN 
                            cost = anz * h-journal.epreis * h-artikel.prozent / 100. 
                            ELSE cost = anz * h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                            h-list.cost = h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                        END. 
                        cost            = cost / fact1. 
                        h-list.anzahl   = h-list.anzahl + anz. 
                        h-list.t-cost   = h-list.t-cost + cost. 
                        h-list.t-sales  = h-list.t-sales + h-umsatz.betrag / fact. 
                        t-cost          = t-cost + cost. 
                        t-anz           = t-anz + anz. 
                        t-sales         = t-sales + h-umsatz.betrag / fact. 
                    END. 
                END. /* do datum*/
                */
                /*FDL Feb 26, 2024 => Ticket D7BB75*/
                FIND FIRST h-umsatz WHERE h-umsatz.artnr EQ h-artikel.artnr 
                    AND h-umsatz.departement EQ h-artikel.departement 
                    AND h-umsatz.datum GE from-date
                    AND h-umsatz.datum LE to-date USE-INDEX hrartatz_ix NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE h-umsatz:

                    RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,h-umsatz.datum,  /*willi change datum to h-umsatz.datum 14/03/24*/
                                           OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
                    ASSIGN vat = vat + vat2.

                    anz  = h-umsatz.anzahl. 
                    cost = 0. 
                    /* Dzikri E248F5 - wrong cost price, NE recipe
                    FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
                        AND h-cost.departement = h-artikel.departement 
                        AND h-cost.datum = h-umsatz.datum AND h-cost.flag = 1 NO-LOCK NO-ERROR.  /*willi change datum to h-umsatz.datum 14/03/24*/
                    */
                    h-list.cost = 0.
                    RUN fb-cost-count-recipe-costbl.p (h-artikel.artnrrezept, price-type, INPUT-OUTPUT h-list.cost).  

                    /* IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN */
                    IF h-list.cost NE 0 THEN
                    DO:
                        /*
                        cost = anz * h-cost.betrag. 
                        h-list.cost = h-cost.betrag. 
                        */
                        cost = anz * h-list.cost.
                    END.
                    ELSE 
                    DO: 
                        FIND FIRST h-journal WHERE h-journal.artnr = h-artikel.artnr 
                            AND h-journal.departement = h-artikel.departement 
                            AND h-journal.bill-datum EQ h-umsatz.datum NO-LOCK NO-ERROR.  /*willi change datum to h-umsatz.datum 14/03/24*/
                        IF AVAILABLE h-journal THEN 
                        cost = anz * h-journal.epreis * h-artikel.prozent / 100. 
                        ELSE cost = anz * h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                        h-list.cost = h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                    END. 
                    cost            = cost / fact1. 
                    h-list.anzahl   = h-list.anzahl + anz. 
                    h-list.t-cost   = h-list.t-cost + cost. 
                    h-list.t-sales  = h-list.t-sales + h-umsatz.betrag / fact. 
                    t-cost          = t-cost + cost. 
                    t-anz           = t-anz + anz. 
                    t-sales         = t-sales + h-umsatz.betrag / fact. 
                    
                    /* Dzikri D635B2 - CHANGE PRICE TO AVERAGE PRICE */
                    IF vat-included THEN h-list.epreis = (h-list.t-sales / h-list.anzahl) * exchg-rate / fact. 
                    ELSE h-list.epreis = (h-list.t-sales / h-list.anzahl) * exchg-rate / fact1.
                    /* Dzikri D635B2 - END */

                    FIND NEXT h-umsatz WHERE h-umsatz.artnr EQ h-artikel.artnr 
                        AND h-umsatz.departement EQ h-artikel.departement 
                        AND h-umsatz.datum GE from-date
                        AND h-umsatz.datum LE to-date USE-INDEX hrartatz_ix NO-LOCK NO-ERROR.
                END.
                IF h-list.epreis NE 0 THEN h-list.margin = h-list.cost / h-list.epreis * 100. 
            END. /* if do-it*/
        END. 
        RUN create-list(pos). 
        t-anz   = 0. 
        t-sales = 0. 
        t-cost  = 0. 
    END. /*hoteldpt*/
  /*MThide FRAME frame2 NO-PAUSE.*/
END. 
 
PROCEDURE create-h-umsatz2: 
  DEFINE VARIABLE disc-flag AS LOGICAL. 
  DEFINE VARIABLE disc-nr AS INTEGER. 
  DEFINE VARIABLE dept AS INTEGER INITIAL -1. 
  DEFINE VARIABLE pos AS LOGICAL. 
  DEFINE VARIABLE datum AS DATE. 
  DEFINE VARIABLE vat AS DECIMAL. 
  DEFINE VARIABLE serv AS DECIMAL. 
  DEFINE VARIABLE vat2 AS DECIMAL NO-UNDO.
  DEFINE VARIABLE serv-vat AS LOGICAL. 
  DEFINE VARIABLE fact AS DECIMAL. 
  DEFINE VARIABLE do-it AS LOGICAL INITIAL NO.
  
  DEFINE VARIABLE cost AS DECIMAL. 
  DEFINE VARIABLE anz AS INTEGER. 
  
  DEFINE buffer h-art FOR h-artikel. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
  FOR EACH h-list: 
    delete h-list. 
  END. 
  /* 
    from-date = DATE(month(to-date), 1, year(to-date)). 
  */ 
  /*F
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htplogic. 
  FIND FIRST htparam WHERE htparam.paramnr = 555 NO-LOCK. 
  disc-nr = htparam.htpint. 
  F*/
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept AND hoteldpt.num NE dstore 
    AND hoteldpt.num NE ldry-dept NO-LOCK BY hoteldpt.num: 
    FIND FIRST h-artikel WHERE h-artikel.departement = hoteldpt.num 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE h-artikel THEN pos = YES. 
    ELSE pos = NO. 
    IF pos THEN 
    DO: 
      /*MTcurr-dept = STRING(hoteldpt.num,"99") + " - " + hoteldpt.depart. 
      DISP curr-dept WITH FRAME frame2.*/
 
      create output-list. 
      output-list.bezeich = STRING(hoteldpt.num,"99 ") 
        + STRING(hoteldpt.depart,"x(21)").      
    END. 
    dept = hoteldpt.num. 
    FOR EACH h-artikel WHERE h-artikel.artart = 0 
      AND h-artikel.departement = hoteldpt.num NO-LOCK, 
      FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
      AND artikel.departement = h-artikel.departement 
      AND artikel.umsatzart = 6 
      AND artikel.endkum NE disc-nr NO-LOCK BY h-artikel.bezeich: 
      do-it = NO.
      IF all-sub THEN do-it = YES.
      ELSE
      DO:
          FIND FIRST subgr-list WHERE subgr-list.subnr = h-artikel.zwkum
              AND subgr-list.SELECTED NO-LOCK NO-ERROR.
          do-it = AVAILABLE subgr-list.
      END.
      IF do-it THEN
      DO:     
          /* Dzikri E248F5 - wrong cost price, NE recipe
          FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
            AND h-cost.departement = h-artikel.departement 
            AND h-cost.datum = to-date AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
            */
            /*          
              /*RUN calc-servvat.p(h-artikel.departement, h-artikel.artnr, to-date, h-artikel.service-code, 
                                  h-artikel.mwst-code, OUTPUT serv, OUTPUT vat). */
              RUN calc-servvat.p(artikel.departement, artikel.artnr, to-date, artikel.service-code, 
                                artikel.mwst-code, OUTPUT serv, OUTPUT vat).
              fact = (1.00 + serv + vat) * fact1. 
            */     
            /* SY AUG 13 2017 */
          RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
            to-date, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
          ASSIGN vat = vat + vat2.

          CREATE h-list. 
          h-list.cost = 0.
          RUN fb-cost-count-recipe-costbl.p (h-artikel.artnrrezept, price-type, INPUT-OUTPUT h-list.cost).  
          /* 
          IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
            h-list.cost = h-cost.betrag. 
          ELSE h-list.cost = h-artikel.epreis1 * h-artikel.prozent / 100 
            * exchg-rate. 
          Dzikri E248F5 - END */
          h-list.cost = h-list.cost / fact1. 
          h-list.dept = h-artikel.departement. 
          h-list.artnr = h-artikel.artnr. 
          h-list.dept = h-artikel.departement. 
          h-list.bezeich = h-artikel.bezeich. 
          h-list.zknr = h-artikel.zwkum. 
     
          IF vat-included THEN 
            h-list.epreis = h-artikel.epreis1 * exchg-rate / fact. 
          ELSE h-list.epreis = h-artikel.epreis1 * exchg-rate / fact1. 
        
          /*  
          DO datum = from-date TO to-date: 
  /*            
              /*RUN calc-servvat.p(h-artikel.departement, h-artikel.artnr, datum, h-artikel.service-code, 
                                h-artikel.mwst-code, OUTPUT serv, OUTPUT vat).*/
              RUN calc-servvat.p(artikel.departement, artikel.artnr, to-date, artikel.service-code, 
                                artikel.mwst-code, OUTPUT serv, OUTPUT vat).
              fact = (1.00 + serv + vat) * fact1. 
  */
  /* SY AUG 13 2017 */
            RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
                datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
            ASSIGN vat = vat + vat2.

            FIND FIRST h-umsatz WHERE h-umsatz.artnr = h-artikel.artnr 
              AND h-umsatz.departement = h-artikel.departement 
              AND h-umsatz.datum EQ datum NO-LOCK NO-ERROR. 
            IF AVAILABLE h-umsatz THEN 
            DO: 
              anz = h-umsatz.anzahl. 
              cost = 0. 
              FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
                AND h-cost.departement = h-artikel.departement 
                AND h-cost.datum = datum AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
     
              IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN DO:
                  cost = anz * h-cost.betrag. 
                  h-list.cost = h-cost.betrag.
              END.
              ELSE 
              DO: 
                FIND FIRST h-journal WHERE h-journal.artnr = h-artikel.artnr 
                  AND h-journal.departement = h-artikel.departement 
                  AND h-journal.bill-datum EQ datum NO-LOCK NO-ERROR. 
                IF AVAILABLE h-journal THEN 
                  cost = anz * h-journal.epreis * h-artikel.prozent / 100. 
                ELSE cost = anz * h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                h-list.cost = h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
              END. 
              cost = cost / fact1. 
              h-list.anzahl = h-list.anzahl + anz. 
              h-list.t-cost = h-list.t-cost + cost. 
              h-list.t-sales = h-list.t-sales + h-umsatz.betrag / fact. 
              t-cost = t-cost + cost. 
              t-anz = t-anz + anz. 
              t-sales = t-sales + h-umsatz.betrag / fact. 
            END. 
          END.  /* do datum..*/
          */
          /*FDL Feb 26, 2024 => Ticket D7BB75*/
          FIND FIRST h-umsatz WHERE h-umsatz.artnr EQ h-artikel.artnr 
              AND h-umsatz.departement EQ h-artikel.departement 
              AND h-umsatz.datum GE from-date
              AND h-umsatz.datum LE to-date USE-INDEX hrartatz_ix NO-LOCK NO-ERROR.
          DO WHILE AVAILABLE h-umsatz:

              RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
                  datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
              ASSIGN vat = vat + vat2.

              anz = h-umsatz.anzahl. 
              cost = 0. 
              /* Dzikri E248F5 - wrong cost price, NE recipe
              FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
                  AND h-cost.departement = h-artikel.departement 
                  AND h-cost.datum = h-umsatz.datum AND h-cost.flag = 1 NO-LOCK NO-ERROR.    /*willi change datum to h-umsatz.datum 14/03/24*/
              */
              h-list.cost = 0.
              RUN fb-cost-count-recipe-costbl.p (h-artikel.artnrrezept, price-type, INPUT-OUTPUT h-list.cost).  
              /* IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN */
              IF h-list.cost NE 0 THEN
              DO:
                  /*
                  cost = anz * h-cost.betrag. 
                  h-list.cost = h-cost.betrag.
                  */
                  cost = anz * h-list.cost.
              /* Dzikri E248F5 - END */
              END.
              ELSE 
              DO: 
                FIND FIRST h-journal WHERE h-journal.artnr = h-artikel.artnr 
                    AND h-journal.departement = h-artikel.departement 
                    AND h-journal.bill-datum EQ h-umsatz.datum NO-LOCK NO-ERROR.  /*willi change datum to h-umsatz.datum 14/03/24*/
                IF AVAILABLE h-journal THEN 
                    cost = anz * h-journal.epreis * h-artikel.prozent / 100. 
                ELSE cost = anz * h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                h-list.cost = h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
              END. 
              cost = cost / fact1. 
              h-list.anzahl = h-list.anzahl + anz. 
              h-list.t-cost = h-list.t-cost + cost. 
              h-list.t-sales = h-list.t-sales + h-umsatz.betrag / fact. 
              t-cost = t-cost + cost. 
              t-anz = t-anz + anz. 
              t-sales = t-sales + h-umsatz.betrag / fact.

              /* Dzikri D635B2 - CHANGE PRICE TO AVERAGE PRICE */
              IF vat-included THEN h-list.epreis = (h-list.t-sales / h-list.anzahl) * exchg-rate / fact. 
              ELSE h-list.epreis = (h-list.t-sales / h-list.anzahl) * exchg-rate / fact1.
              /* Dzikri D635B2 - END */

              FIND NEXT h-umsatz WHERE h-umsatz.artnr EQ h-artikel.artnr 
                  AND h-umsatz.departement EQ h-artikel.departement 
                  AND h-umsatz.datum GE from-date
                  AND h-umsatz.datum LE to-date USE-INDEX hrartatz_ix NO-LOCK NO-ERROR.
          END.
          IF h-list.epreis NE 0 THEN 
            h-list.margin = h-list.cost / h-list.epreis * 100. 
      END. /*if do-it*/
    END. 
    RUN create-list(pos). 
    t-anz = 0. 
    t-sales = 0. 
    t-cost = 0. 
  END. 
  /*MThide FRAME frame2 NO-PAUSE.*/
END. 

PROCEDURE create-h-umsatz3: 
  DEFINE VARIABLE disc-flag AS LOGICAL. 
  DEFINE VARIABLE disc-nr AS INTEGER. 
  DEFINE VARIABLE dept AS INTEGER INITIAL -1. 
  DEFINE VARIABLE pos AS LOGICAL. 
  DEFINE VARIABLE datum AS DATE. 
  DEFINE VARIABLE vat AS DECIMAL. 
  DEFINE VARIABLE serv AS DECIMAL. 
  DEFINE VARIABLE vat2 AS DECIMAL NO-UNDO.
  DEFINE VARIABLE serv-vat AS LOGICAL. 
  DEFINE VARIABLE fact AS DECIMAL. 
  DEFINE VARIABLE do-it AS LOGICAL INITIAL NO.
  
  DEFINE VARIABLE cost AS DECIMAL. 
  DEFINE VARIABLE anz AS INTEGER. 
  
  DEFINE buffer h-art FOR h-artikel. 

    FOR EACH output-list: 
        DELETE output-list. 
    END. 
    FOR EACH h-list: 
        DELETE h-list. 
    END. 
    /* 
        from-date = DATE(month(to-date), 1, year(to-date)). 
    */ 
    /*F
        FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
        serv-vat = htplogic. 
        FIND FIRST htparam WHERE htparam.paramnr = 555 NO-LOCK. 
        disc-nr = htparam.htpint. 
    F*/
    FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
        AND hoteldpt.num LE to-dept /*AND hoteldpt.num NE dstore 
        AND hoteldpt.num NE ldry-dept*/ NO-LOCK BY hoteldpt.num: 
        FIND FIRST h-artikel WHERE h-artikel.departement = hoteldpt.num 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE h-artikel THEN pos = YES. 
        ELSE pos = NO. 
        IF pos THEN 
        DO: 
            CREATE output-list. 
            output-list.bezeich = STRING(hoteldpt.num,"99 ") 
                + STRING(hoteldpt.depart,"x(21)").             
        END. 
        dept = hoteldpt.num. 

        FOR EACH h-artikel WHERE h-artikel.artart = 0 
            AND h-artikel.departement = hoteldpt.num NO-LOCK, 
            FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
            AND artikel.departement = h-artikel.departement 
            AND artikel.umsatzart = 4 
            AND artikel.endkum NE disc-nr NO-LOCK BY h-artikel.bezeich: 
            do-it = NO.
            IF all-sub THEN do-it = YES.
            ELSE
            DO:
                FIND FIRST subgr-list WHERE subgr-list.subnr = h-artikel.zwkum
                    AND subgr-list.SELECTED NO-LOCK NO-ERROR.
                do-it = AVAILABLE subgr-list.
            END.
            
            IF do-it THEN
            DO:     
                /* Dzikri E248F5 - wrong cost price, NE recipe
                FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
                    AND h-cost.departement = h-artikel.departement 
                    AND h-cost.datum = to-date AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
                  */
                  /*            
                    /*RUN calc-servvat.p(h-artikel.departement, h-artikel.artnr, to-date, h-artikel.service-code, 
                                        h-artikel.mwst-code, OUTPUT serv, OUTPUT vat). */
                    RUN calc-servvat.p(artikel.departement, artikel.artnr, to-date, artikel.service-code, 
                                      artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                    fact = (1.00 + serv + vat) * fact1. 
                  */       
                  /* SY AUG 13 2017 */
                RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
                    to-date, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
                ASSIGN vat = vat + vat2.
            
                CREATE h-list. 
                h-list.cost = 0.
                RUN fb-cost-count-recipe-costbl.p (h-artikel.artnrrezept, price-type, INPUT-OUTPUT h-list.cost).  
                /* 
                IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN h-list.cost = h-cost.betrag. 
                ELSE h-list.cost = h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                Dzikri E248F5 - END */
                h-list.cost = h-list.cost / fact1. 
                h-list.dept = h-artikel.departement. 
                h-list.artnr = h-artikel.artnr. 
                h-list.dept = h-artikel.departement. 
                h-list.bezeich = h-artikel.bezeich. 
                h-list.zknr = h-artikel.zwkum. 
            
                IF vat-included THEN 
                    h-list.epreis = h-artikel.epreis1 * exchg-rate / fact. 
                ELSE h-list.epreis = h-artikel.epreis1 * exchg-rate / fact1. 
            
                
                /*DO datum = from-date TO to-date: 
          /*              
                    /*RUN calc-servvat.p(h-artikel.departement, h-artikel.artnr, datum, h-artikel.service-code, 
                                      h-artikel.mwst-code, OUTPUT serv, OUTPUT vat).*/
                    RUN calc-servvat.p(artikel.departement, artikel.artnr, to-date, artikel.service-code, 
                                      artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                    fact = (1.00 + serv + vat) * fact1. 
          */      
          /* SY AUG 13 2017 */
                    RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
                        datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
                    ASSIGN vat = vat + vat2.
            
                    FIND FIRST h-umsatz WHERE h-umsatz.artnr = h-artikel.artnr 
                        AND h-umsatz.departement = h-artikel.departement 
                        AND h-umsatz.datum EQ datum NO-LOCK NO-ERROR. 
                    IF AVAILABLE h-umsatz THEN 
                    DO: 
                        anz = h-umsatz.anzahl. 
                        cost = 0. 
                        FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
                            AND h-cost.departement = h-artikel.departement 
                            AND h-cost.datum = datum AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
                    
                        IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN DO:
                            cost = anz * h-cost.betrag. 
                            h-list.cost = h-cost.betrag.
                        END.
                        ELSE 
                        DO: 
                            FIND FIRST h-journal WHERE h-journal.artnr = h-artikel.artnr 
                                AND h-journal.departement = h-artikel.departement 
                                AND h-journal.bill-datum EQ datum NO-LOCK NO-ERROR. 
                            IF AVAILABLE h-journal THEN 
                                cost = anz * h-journal.epreis * h-artikel.prozent / 100. 
                            ELSE cost = anz * h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                            h-list.cost = h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                        END. 
                        cost = cost / fact1. 
                        h-list.anzahl = h-list.anzahl + anz. 
                        h-list.t-cost = h-list.t-cost + cost. 
                        h-list.t-sales = h-list.t-sales + h-umsatz.betrag / fact. 
                        t-cost = t-cost + cost. 
                        t-anz = t-anz + anz. 
                        t-sales = t-sales + h-umsatz.betrag / fact. 
                    END. 
                END.  /* do datum..*/*/
                /*ragung*/
                FIND FIRST h-umsatz WHERE h-umsatz.artnr = h-artikel.artnr 
                     AND h-umsatz.departement = h-artikel.departement 
                     AND h-umsatz.datum GE from-date 
                     AND h-umsatz.datum LE to-date USE-INDEX hrartatz_ix NO-LOCK NO-ERROR. 
                DO WHILE AVAILABLE h-umsatz:
                   RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
                         datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
                   ASSIGN vat = vat + vat2.
                   
                   anz = h-umsatz.anzahl. 
                   cost = 0. 
                   /* Dzikri E248F5 - wrong cost price, NE recipe
                   FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
                       AND h-cost.departement = h-artikel.departement 
                       AND h-cost.datum = h-umsatz.datum AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
                   */
                   h-list.cost = 0.
                   RUN fb-cost-count-recipe-costbl.p (h-artikel.artnrrezept, price-type, INPUT-OUTPUT h-list.cost).  
                   
                   /* IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN */
                   IF h-list.cost NE 0 THEN
                   DO:
                       /*
                       cost = anz * h-cost.betrag. 
                       h-list.cost = h-cost.betrag.
                       */
                       cost = anz * h-list.cost.
                   /* Dzikri E248F5 - END */
                   END.
                   ELSE 
                   DO: 
                       FIND FIRST h-journal WHERE h-journal.artnr = h-artikel.artnr 
                           AND h-journal.departement = h-artikel.departement 
                           AND h-journal.bill-datum EQ h-umsatz.datum NO-LOCK NO-ERROR. 
                       IF AVAILABLE h-journal THEN 
                           cost = anz * h-journal.epreis * h-artikel.prozent / 100. 
                       ELSE cost = anz * h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                       h-list.cost = h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                   END. 
                   cost = cost / fact1. 
                   h-list.anzahl = h-list.anzahl + anz. 
                   h-list.t-cost = h-list.t-cost + cost. 
                   h-list.t-sales = h-list.t-sales + h-umsatz.betrag / fact. 
                   t-cost = t-cost + cost. 
                   t-anz = t-anz + anz. 
                   t-sales = t-sales + h-umsatz.betrag / fact. 

                   /* Dzikri D635B2 - CHANGE PRICE TO AVERAGE PRICE */
                   IF vat-included THEN h-list.epreis = (h-list.t-sales / h-list.anzahl) * exchg-rate / fact. 
                   ELSE h-list.epreis = (h-list.t-sales / h-list.anzahl) * exchg-rate / fact1.
                   /* Dzikri D635B2 - END */
                   
                   FIND NEXT h-umsatz WHERE h-umsatz.artnr = h-artikel.artnr 
                      AND h-umsatz.departement = h-artikel.departement 
                      AND h-umsatz.datum GE from-date 
                      AND h-umsatz.datum LE to-date USE-INDEX hrartatz_ix NO-LOCK NO-ERROR. 
                END. /*end*/
                IF h-list.epreis NE 0 THEN 
                    h-list.margin = h-list.cost / h-list.epreis * 100. 
            END. /*if do-it*/
        END. 
    RUN create-list(pos). 
    t-anz = 0. 
    t-sales = 0. 
    t-cost = 0. 
    END. 
  /*MThide FRAME frame2 NO-PAUSE.*/
END. 

PROCEDURE create-list: 
  DEFINE INPUT PARAMETER pos AS LOGICAL. 
  /* Malik Serverless 553 */
  DEFINE VARIABLE h-list-artnr AS CHAR.
  DEFINE VARIABLE h-list-anzahl AS CHAR.
  DEFINE VARIABLE h-list-proz1 AS CHAR.
  DEFINE VARIABLE h-list-epreis AS CHAR.
  DEFINE VARIABLE h-list-cost AS CHAR.
  DEFINE VARIABLE h-list-margin AS CHAR.
  DEFINE VARIABLE h-list-t-sales AS CHAR.
  DEFINE VARIABLE h-list-t-cost AS CHAR.
  DEFINE VARIABLE h-list-t-margin AS CHAR.
  DEFINE VARIABLE h-list-proz2 AS CHAR.
  DEFINE VARIABLE h-list-epreis-non-short-flag AS CHAR.
  DEFINE VARIABLE h-list-cost-non-short-flag AS CHAR.
  DEFINE VARIABLE h-list-t-sales-non-short-flag AS CHAR.
  DEFINE VARIABLE h-list-t-cost-non-short-flag AS CHAR.
  DEFINE VARIABLE t-anz-tot AS CHAR.
  DEFINE VARIABLE hundred-tot AS CHAR.
  DEFINE VARIABLE t-sales-tot AS CHAR.
  DEFINE VARIABLE t-cost-tot AS CHAR.
  DEFINE VARIABLE t-margin-tot AS CHAR.
  DEFINE VARIABLE t-sales-tot-non-short-flag AS CHAR.
  DEFINE VARIABLE t-cost-tot-non-short-flag AS CHAR.


  DO: 
    IF mi-subgrp THEN 
    DO: 
      RUN create-list1(pos). 
      RETURN. 
    END. 
    IF detailed AND curr-sort = 1 THEN 
    FOR EACH h-list WHERE h-list.dept = hoteldpt.num: 
      IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
      IF h-list.t-sales NE 0 THEN 
        h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
      IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

      /* Malik Serverless 553 */
      h-list-artnr = STRING(h-list.artnr, ">>>>>>>>9").
      h-list-anzahl = STRING(h-list.anzahl, "->>>>9").
      h-list-proz1 =  STRING(h-list.proz1, "->>9.99").
      h-list-epreis = STRING(h-list.epreis, "->,>>>,>>>,>>9.99").
      h-list-cost = STRING(h-list.cost, "->,>>>,>>>,>>9.99").
      h-list-margin = STRING(h-list.margin, "->,>>>,>>9.99").
      h-list-t-sales = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99").
      h-list-t-cost = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99").
      h-list-t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99").
      h-list-proz2 = STRING(h-list.proz2, "->>9.99").

      h-list-epreis-non-short-flag = STRING(h-list.epreis, " ->>>,>>>,>>>,>>9"). 
      h-list-cost-non-short-flag = STRING(h-list.cost, " ->>>,>>>,>>>,>>9").
      h-list-t-sales-non-short-flag = STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9").
      h-list-t-cost-non-short-flag = STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9").

      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = h-list.bezeich. 
      IF short-flag THEN output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")            
        + STRING(h-list.epreis, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      ELSE output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")           
        + STRING(h-list.epreis, " ->>>,>>>,>>>,>>9")   
        + STRING(h-list.cost, " ->>>,>>>,>>>,>>9")     
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      */  
      create output-list. 
      output-list.bezeich = h-list.bezeich. 
      IF short-flag THEN output-list.s = STRING(h-list-artnr, "x(9)") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list-anzahl, "x(6)") 
        + STRING(h-list-proz1, "x(7)")            
        + STRING(h-list-epreis, "x(17)") 
        + STRING(h-list-cost, "x(17)")      
        + STRING(h-list-margin, "x(13)") 
        + STRING(h-list-t-sales, "x(17)") 
        + STRING(h-list-t-cost, "x(17)") 
        + STRING(h-list-t-margin, "x(13)") 
        + STRING(h-list-proz2, "x(7)"). 
      ELSE output-list.s = STRING(h-list-artnr, "x(9)") 
      /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list-anzahl, "x(6)") 
        + STRING(h-list-proz1, "x(7)")            
        + STRING(h-list-epreis-non-short-flag, "x(17)") 
        + STRING(h-list-cost-non-short-flag, "x(17)")      
        + STRING(h-list-margin, "x(13)") 
        + STRING(h-list-t-sales-non-short-flag, "x(17)") 
        + STRING(h-list-t-cost-non-short-flag, "x(17)") 
        + STRING(h-list-t-margin, "x(13)") 
        + STRING(h-list-proz2, "x(7)").

    END. 
    ELSE IF detailed AND curr-sort = 2 THEN 
    FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
      BY h-list.anzahl descending BY h-list.t-sales descending 
      BY h-list.bezeich: 
      IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
      IF h-list.t-sales NE 0 THEN 
        h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
      IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

      /* Malik Serverless 553 */
      h-list-artnr = STRING(h-list.artnr, ">>>>>>>>9").
      h-list-anzahl = STRING(h-list.anzahl, "->>>>9").
      h-list-proz1 =  STRING(h-list.proz1, "->>9.99").
      h-list-epreis = STRING(h-list.epreis, "->,>>>,>>>,>>9.99").
      h-list-cost = STRING(h-list.cost, "->,>>>,>>>,>>9.99").
      h-list-margin = STRING(h-list.margin, "->,>>>,>>9.99").
      h-list-t-sales = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99").
      h-list-t-cost = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99").
      h-list-t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99").
      h-list-proz2 = STRING(h-list.proz2, "->>9.99").

      h-list-epreis-non-short-flag = STRING(h-list.epreis, " ->>>,>>>,>>>,>>9").
      h-list-cost-non-short-flag = STRING(h-list.cost, " ->>>,>>>,>>>,>>9").
      h-list-t-sales-non-short-flag = STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9").
      h-list-t-cost-non-short-flag = STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9").
      
      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = h-list.bezeich. 
      IF short-flag THEN output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")            
        + STRING(h-list.epreis, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      ELSE output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")           
        + STRING(h-list.epreis, " ->>>,>>>,>>>,>>9")   
        + STRING(h-list.cost, " ->>>,>>>,>>>,>>9")     
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). */

      create output-list. 
      output-list.bezeich = h-list.bezeich. 
      IF short-flag THEN output-list.s = STRING(h-list-artnr, "x(9)") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list-anzahl, "x(6)") 
        + STRING(h-list-proz1, "x(7)")            
        + STRING(h-list-epreis, "x(17)") 
        + STRING(h-list-cost, "x(17)")      
        + STRING(h-list-margin, "x(13)") 
        + STRING(h-list-t-sales, "x(17)") 
        + STRING(h-list-t-cost, "x(17)") 
        + STRING(h-list-t-margin, "x(13)") 
        + STRING(h-list-proz2, "x(7)"). 
      ELSE output-list.s = STRING(h-list-artnr, "x(9)") 
      /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list-anzahl, "x(6)") 
        + STRING(h-list-proz1, "x(7)")            
        + STRING(h-list-epreis-non-short-flag, "x(17)") 
        + STRING(h-list-cost-non-short-flag, "x(17)")      
        + STRING(h-list-margin, "x(13)") 
        + STRING(h-list-t-sales-non-short-flag, "x(17)") 
        + STRING(h-list-t-cost-non-short-flag, "x(17)") 
        + STRING(h-list-t-margin, "x(13)") 
        + STRING(h-list-proz2, "x(7)").
    END. 
    ELSE IF detailed AND curr-sort = 3 THEN 
    FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
      BY h-list.t-sales descending BY h-list.anzahl descending 
      BY h-list.bezeich: 
      IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
      IF h-list.t-sales NE 0 THEN 
        h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
      IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

      /* Malik Serverless 553 */
      h-list-artnr = STRING(h-list.artnr, ">>>>>>>>9").
      h-list-anzahl = STRING(h-list.anzahl, "->>>>9").
      h-list-proz1 =  STRING(h-list.proz1, "->>9.99").
      h-list-epreis = STRING(h-list.epreis, "->,>>>,>>>,>>9.99").
      h-list-cost = STRING(h-list.cost, "->,>>>,>>>,>>9.99").
      h-list-margin = STRING(h-list.margin, "->,>>>,>>9.99").
      h-list-t-sales = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99").
      h-list-t-cost = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99").
      h-list-t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99").
      h-list-proz2 = STRING(h-list.proz2, "->>9.99").

      h-list-epreis-non-short-flag = STRING(h-list.epreis, " ->>>,>>>,>>>,>>9").
      h-list-cost-non-short-flag = STRING(h-list.cost, " ->>>,>>>,>>>,>>9").
      h-list-t-sales-non-short-flag = STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9").
      h-list-t-cost-non-short-flag = STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9").
      
      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = h-list.bezeich. 
      IF short-flag THEN output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")            
        + STRING(h-list.epreis, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      ELSE output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")           
        + STRING(h-list.epreis, " ->>>,>>>,>>>,>>9")   
        + STRING(h-list.cost, " ->>>,>>>,>>>,>>9")     
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). */
      
        create output-list. 
        output-list.bezeich = h-list.bezeich. 
        IF short-flag THEN output-list.s = STRING(h-list-artnr, "x(9)") 
          /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis, "x(17)") 
          + STRING(h-list-cost, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales, "x(17)") 
          + STRING(h-list-t-cost, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)"). 
        ELSE output-list.s = STRING(h-list-artnr, "x(9)") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis-non-short-flag, "x(17)") 
          + STRING(h-list-cost-non-short-flag, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales-non-short-flag, "x(17)") 
          + STRING(h-list-t-cost-non-short-flag, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)").
    END. 
    ELSE IF NOT detailed AND curr-sort = 1 THEN 
    FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
      AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0): 
      IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
      IF h-list.t-sales NE 0 THEN 
        h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
      IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 
      
      /* Malik Serverless 553 */
      h-list-artnr = STRING(h-list.artnr, ">>>>>>>>9").
      h-list-anzahl = STRING(h-list.anzahl, "->>>>9").
      h-list-proz1 =  STRING(h-list.proz1, "->>9.99").
      h-list-epreis = STRING(h-list.epreis, "->,>>>,>>>,>>9.99").
      h-list-cost = STRING(h-list.cost, "->,>>>,>>>,>>9.99").
      h-list-margin = STRING(h-list.margin, "->,>>>,>>9.99").
      h-list-t-sales = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99").
      h-list-t-cost = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99").
      h-list-t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99").
      h-list-proz2 = STRING(h-list.proz2, "->>9.99").

      h-list-epreis-non-short-flag = STRING(h-list.epreis, " ->>>,>>>,>>>,>>9").
      h-list-cost-non-short-flag = STRING(h-list.cost, " ->>>,>>>,>>>,>>9").
      h-list-t-sales-non-short-flag = STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9").
      h-list-t-cost-non-short-flag = STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9").
      
      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = h-list.bezeich. 
      IF short-flag THEN output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")            
        + STRING(h-list.epreis, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      ELSE output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")           
        + STRING(h-list.epreis, " ->>>,>>>,>>>,>>9")   
        + STRING(h-list.cost, " ->>>,>>>,>>>,>>9")     
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). */
        create output-list. 
        output-list.bezeich = h-list.bezeich. 
        IF short-flag THEN output-list.s = STRING(h-list-artnr, "x(9)") 
          /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis, "x(17)") 
          + STRING(h-list-cost, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales, "x(17)") 
          + STRING(h-list-t-cost, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)"). 
        ELSE output-list.s = STRING(h-list-artnr, "x(9)") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis-non-short-flag, "x(17)") 
          + STRING(h-list-cost-non-short-flag, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales-non-short-flag, "x(17)") 
          + STRING(h-list-t-cost-non-short-flag, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)").
    END. 
    ELSE IF NOT detailed AND curr-sort = 2 THEN 
    FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
      AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) 
      BY h-list.anzahl descending BY h-list.t-sales descending 
      BY h-list.bezeich: 
      IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
      IF h-list.t-sales NE 0 THEN 
        h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
      IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

      /* Malik Serverless 553 */
      h-list-artnr = STRING(h-list.artnr, ">>>>>>>>9").
      h-list-anzahl = STRING(h-list.anzahl, "->>>>9").
      h-list-proz1 =  STRING(h-list.proz1, "->>9.99").
      h-list-epreis = STRING(h-list.epreis, "->,>>>,>>>,>>9.99").
      h-list-cost = STRING(h-list.cost, "->,>>>,>>>,>>9.99").
      h-list-margin = STRING(h-list.margin, "->,>>>,>>9.99").
      h-list-t-sales = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99").
      h-list-t-cost = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99").
      h-list-t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99").
      h-list-proz2 = STRING(h-list.proz2, "->>9.99").

      h-list-epreis-non-short-flag = STRING(h-list.epreis, " ->>>,>>>,>>>,>>9").
      h-list-cost-non-short-flag = STRING(h-list.cost, " ->>>,>>>,>>>,>>9").
      h-list-t-sales-non-short-flag = STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9").
      h-list-t-cost-non-short-flag = STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9").

      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = h-list.bezeich. 
      IF short-flag THEN output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")            
        + STRING(h-list.epreis, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      ELSE output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")           
        + STRING(h-list.epreis, " ->>>,>>>,>>>,>>9")   
        + STRING(h-list.cost, " ->>>,>>>,>>>,>>9")     
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). */
        create output-list. 
        output-list.bezeich = h-list.bezeich. 
        IF short-flag THEN output-list.s = STRING(h-list-artnr, "x(9)") 
          /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis, "x(17)") 
          + STRING(h-list-cost, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales, "x(17)") 
          + STRING(h-list-t-cost, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)"). 
        ELSE output-list.s = STRING(h-list-artnr, "x(9)") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis-non-short-flag, "x(17)") 
          + STRING(h-list-cost-non-short-flag, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales-non-short-flag, "x(17)") 
          + STRING(h-list-t-cost-non-short-flag, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)").

    END. 
    ELSE IF NOT detailed AND curr-sort = 3 THEN 
    FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
      AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) 
      BY h-list.t-sales descending BY h-list.anzahl descending 
      BY h-list.bezeich: 
      IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
      IF h-list.t-sales NE 0 THEN 
        h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
      IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

      /* Malik Serverless 553 */
      h-list-artnr = STRING(h-list.artnr, ">>>>>>>>9").
      h-list-anzahl = STRING(h-list.anzahl, "->>>>9").
      h-list-proz1 =  STRING(h-list.proz1, "->>9.99").
      h-list-epreis = STRING(h-list.epreis, "->,>>>,>>>,>>9.99").
      h-list-cost = STRING(h-list.cost, "->,>>>,>>>,>>9.99").
      h-list-margin = STRING(h-list.margin, "->,>>>,>>9.99").
      h-list-t-sales = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99").
      h-list-t-cost = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99").
      h-list-t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99").
      h-list-proz2 = STRING(h-list.proz2, "->>9.99").

      h-list-epreis-non-short-flag = STRING(h-list.epreis, " ->>>,>>>,>>>,>>9").
      h-list-cost-non-short-flag = STRING(h-list.cost, " ->>>,>>>,>>>,>>9").
      h-list-t-sales-non-short-flag = STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9").
      h-list-t-cost-non-short-flag = STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9").

      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = h-list.bezeich. 
      IF short-flag THEN output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")            
        + STRING(h-list.epreis, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      ELSE output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")           
        + STRING(h-list.epreis, " ->>>,>>>,>>>,>>9")   
        + STRING(h-list.cost, " ->>>,>>>,>>>,>>9")     
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). */
        create output-list. 
        output-list.bezeich = h-list.bezeich. 
        IF short-flag THEN output-list.s = STRING(h-list-artnr, "x(9)") 
          /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis, "x(17)") 
          + STRING(h-list-cost, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales, "x(17)") 
          + STRING(h-list-t-cost, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)"). 
        ELSE output-list.s = STRING(h-list-artnr, "x(9)") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis-non-short-flag, "x(17)") 
          + STRING(h-list-cost-non-short-flag, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales-non-short-flag, "x(17)") 
          + STRING(h-list-t-cost-non-short-flag, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)").

    END. 
    IF pos AND t-sales NE 0 THEN 
    DO: 
      t-margin = 0. 
      IF t-sales NE 0 THEN t-margin = t-cost / t-sales * 100. 

      /* Malik Serverless 553 */
      t-anz-tot = STRING(t-anz, "->>>>9").
      hundred-tot = STRING(100, "->>9.99").
      t-sales-tot = STRING(t-sales, "->,>>>,>>>,>>9.99").
      t-cost-tot = STRING(t-cost, "->,>>>,>>>,>>9.99").
      t-margin-tot = STRING(t-margin, "->,>>>,>>9.99").
      t-sales-tot-non-short-flag = STRING(t-sales, " ->>>,>>>,>>>,>>9").
      t-cost-tot-non-short-flag = STRING(t-cost, " ->>>,>>>,>>>,>>9").

      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = "T o t a l". 
      IF short-flag THEN output-list.s = "         "  
        + STRING(t-anz, "->>>>9") 
        + STRING(100, "->>9.99") 
        + STRING("", "x(47)")
        + STRING(t-sales, "->,>>>,>>>,>>9.99")
        + STRING(t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(t-margin, "->,>>>,>>9.99") 
        + STRING(100, "->>9.99"). 
      ELSE output-list.s = "     " 
        + STRING(t-anz, "->>>>9") 
        + STRING(100, "->>9.99") 
        + STRING("", "x(47)") 
        + STRING(t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(t-margin, "->,>>>,>>9.99") 
        + STRING(100, "->>9.99"). 
      create output-list. */

      create output-list. 
      output-list.bezeich = "T o t a l". 
      IF short-flag THEN output-list.s = STRING(" ", "x(9)")
        + STRING(t-anz-tot, "x(6)") 
        + STRING(hundred-tot, "x(7)") 
        + STRING("", "x(47)")
        + STRING(t-sales-tot, "x(17)")
        + STRING(t-cost-tot, "x(17)") 
        + STRING(t-margin-tot, "x(13)") 
        + STRING(hundred-tot, "x(7)"). 
      ELSE output-list.s = STRING(" ", "x(5)") 
      + STRING(t-anz-tot, "x(6)") 
      + STRING(hundred-tot, "x(7)") 
      + STRING("", "x(47)")
      + STRING(t-sales-tot-non-short-flag, "x(17)")
      + STRING(t-cost-tot-non-short-flag, "x(17)") 
      + STRING(t-margin-tot, "x(13)") 
      + STRING(hundred-tot, "x(7)"). 
      create output-list.
    END. 
  END. 
END. 


PROCEDURE create-list1: 
  DEFINE INPUT PARAMETER pos AS LOGICAL. 
  DEFINE VARIABLE curr-grp AS INTEGER INITIAL 0. 

  /* Malik Serverless 553 */
  DEFINE VARIABLE h-list-artnr AS CHAR.
  DEFINE VARIABLE h-list-anzahl AS CHAR.
  DEFINE VARIABLE h-list-proz1 AS CHAR.
  DEFINE VARIABLE h-list-epreis AS CHAR.
  DEFINE VARIABLE h-list-cost AS CHAR.
  DEFINE VARIABLE h-list-margin AS CHAR.
  DEFINE VARIABLE h-list-t-sales AS CHAR.
  DEFINE VARIABLE h-list-t-cost AS CHAR.
  DEFINE VARIABLE h-list-t-margin AS CHAR.
  DEFINE VARIABLE h-list-proz2 AS CHAR.
  DEFINE VARIABLE h-list-epreis-non-short-flag AS CHAR.
  DEFINE VARIABLE h-list-cost-non-short-flag AS CHAR.
  DEFINE VARIABLE h-list-t-sales-non-short-flag AS CHAR.
  DEFINE VARIABLE h-list-t-cost-non-short-flag AS CHAR.
  DEFINE VARIABLE t-anz-tot AS CHAR.
  DEFINE VARIABLE hundred-tot AS CHAR.
  DEFINE VARIABLE t-sales-tot AS CHAR.
  DEFINE VARIABLE t-cost-tot AS CHAR.
  DEFINE VARIABLE t-margin-tot AS CHAR.
  DEFINE VARIABLE t-sales-tot-non-short-flag AS CHAR.
  DEFINE VARIABLE t-cost-tot-non-short-flag AS CHAR.
  DEFINE VARIABLE wgrpdep-bezeich AS CHAR.


  DO: 
    IF detailed AND curr-sort = 1 THEN 
    FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
      BY h-list.zknr BY h-list.bezeich: 
      IF curr-grp NE h-list.zknr THEN 
      DO: 
        RUN create-sub(curr-grp).
        FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept 
          AND wgrpdep.zknr = h-list.zknr NO-LOCK. 
        curr-grp = h-list.zknr. 
        create output-list. 
        output-list.flag = 1. 
        /* Malik Serverless 553 Comment
        output-list.s = "     " + STRING(wgrpdep.bezeich, "x(24)"). */
        output-list.bezeich = STRING(wgrpdep.bezeich, "x(24)"). 
      END. 
      IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
      IF h-list.t-sales NE 0 THEN 
        h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
      IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 
      
      /* Malik Serverless 553 */
      h-list-artnr = STRING(h-list.artnr, ">>>>>>>>9").
      h-list-anzahl = STRING(h-list.anzahl, "->>>>9").
      h-list-proz1 =  STRING(h-list.proz1, "->>9.99").
      h-list-epreis = STRING(h-list.epreis, "->,>>>,>>>,>>9.99").
      h-list-cost = STRING(h-list.cost, "->,>>>,>>>,>>9.99").
      h-list-margin = STRING(h-list.margin, "->,>>>,>>9.99").
      h-list-t-sales = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99").
      h-list-t-cost = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99").
      h-list-t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99").
      h-list-proz2 = STRING(h-list.proz2, "->>9.99").

      h-list-epreis-non-short-flag = STRING(h-list.epreis, " ->>>,>>>,>>>,>>9"). 
      h-list-cost-non-short-flag = STRING(h-list.cost, " ->>>,>>>,>>>,>>9").
      h-list-t-sales-non-short-flag = STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9").
      h-list-t-cost-non-short-flag = STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9").

      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = h-list.bezeich. 
      IF short-flag THEN output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")            
        + STRING(h-list.epreis, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      ELSE output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")           
        + STRING(h-list.epreis, " ->>>,>>>,>>>,>>9")   
        + STRING(h-list.cost, " ->>>,>>>,>>>,>>9")     
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). */
        create output-list. 
        output-list.bezeich = h-list.bezeich. 
        IF short-flag THEN output-list.s = STRING(h-list-artnr, "x(9)") 
          /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis, "x(17)") 
          + STRING(h-list-cost, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales, "x(17)") 
          + STRING(h-list-t-cost, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)"). 
        ELSE output-list.s = STRING(h-list-artnr, "x(9)") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis-non-short-flag, "x(17)") 
          + STRING(h-list-cost-non-short-flag, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales-non-short-flag, "x(17)") 
          + STRING(h-list-t-cost-non-short-flag, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)").  
        
      RUN add-sub.                        
    END. 
    ELSE IF detailed AND curr-sort = 2 THEN 
    FOR EACH h-list WHERE h-list.dept = hoteldpt.num BY h-list.zknr 
      BY h-list.anzahl descending BY h-list.t-sales descending 
      BY h-list.bezeich: 
      IF curr-grp NE h-list.zknr THEN 
      DO: 
        RUN create-sub(curr-grp).
        FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept 
          AND wgrpdep.zknr = h-list.zknr NO-LOCK NO-ERROR. /* Malik Serverless 553 add if available*/ 
        IF AVAILABLE wgrpdep THEN
        DO:
          wgrpdep-bezeich = wgrpdep.bezeich.
        END.
        ELSE
        DO:
          wgrpdep-bezeich = "".
        END.
        curr-grp = h-list.zknr. 
        create output-list. 
        output-list.flag = 1. 
        /* Malik Serverless 553 Comment 
        output-list.s = "     " + STRING(wgrpdep.bezeich, "x(24)"). */
        output-list.bezeich = STRING(wgrpdep-bezeich, "x(24)"). /* Malik Serverless 553 STRING(wgrpdep.bezeich, "x(24)") -> STRING(wgrpdep-bezeich, "x(24)")*/ 
      END. 
      IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
      IF h-list.t-sales NE 0 THEN 
        h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
      IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

      /* Malik Serverless 553 */
      h-list-artnr = STRING(h-list.artnr, ">>>>>>>>9").
      h-list-anzahl = STRING(h-list.anzahl, "->>>>9").
      h-list-proz1 =  STRING(h-list.proz1, "->>9.99").
      h-list-epreis = STRING(h-list.epreis, "->,>>>,>>>,>>9.99").
      h-list-cost = STRING(h-list.cost, "->,>>>,>>>,>>9.99").
      h-list-margin = STRING(h-list.margin, "->,>>>,>>9.99").
      h-list-t-sales = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99").
      h-list-t-cost = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99").
      h-list-t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99").
      h-list-proz2 = STRING(h-list.proz2, "->>9.99").

      h-list-epreis-non-short-flag = STRING(h-list.epreis, " ->>>,>>>,>>>,>>9"). 
      h-list-cost-non-short-flag = STRING(h-list.cost, " ->>>,>>>,>>>,>>9").
      h-list-t-sales-non-short-flag = STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9").
      h-list-t-cost-non-short-flag = STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9").

      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = STRING(h-list.bezeich, "x(24)"). 
      IF short-flag THEN output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")            
        + STRING(h-list.epreis, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      ELSE output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")           
        + STRING(h-list.epreis, " ->>>,>>>,>>>,>>9")   
        + STRING(h-list.cost, " ->>>,>>>,>>>,>>9")     
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). */ 
        create output-list. 
        output-list.bezeich = h-list.bezeich. 
        IF short-flag THEN output-list.s = STRING(h-list-artnr, "x(9)") 
          /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis, "x(17)") 
          + STRING(h-list-cost, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales, "x(17)") 
          + STRING(h-list-t-cost, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)"). 
        ELSE output-list.s = STRING(h-list-artnr, "x(9)") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis-non-short-flag, "x(17)") 
          + STRING(h-list-cost-non-short-flag, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales-non-short-flag, "x(17)") 
          + STRING(h-list-t-cost-non-short-flag, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)").
       RUN add-sub.
    END. 
    ELSE IF detailed AND curr-sort = 3 THEN 
    FOR EACH h-list WHERE h-list.dept = hoteldpt.num BY h-list.zknr 
      BY h-list.t-sales descending BY h-list.anzahl descending 
      BY h-list.bezeich: 
      IF curr-grp NE h-list.zknr THEN 
      DO: 
        RUN create-sub(curr-grp).
        FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept 
          AND wgrpdep.zknr = h-list.zknr NO-LOCK. 
        curr-grp = h-list.zknr. 
        create output-list. 
        output-list.flag = 1. 
        /* Malik Serverless 553 Comment
        output-list.s = "     " + STRING(wgrpdep.bezeich, "x(24)"). */
        output-list.bezeich = STRING(wgrpdep.bezeich, "x(24)"). 
      END. 
      IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
      IF h-list.t-sales NE 0 THEN 
        h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
      IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 
      /* Malik Serverless 553 */
      h-list-artnr = STRING(h-list.artnr, ">>>>>>>>9").
      h-list-anzahl = STRING(h-list.anzahl, "->>>>9").
      h-list-proz1 =  STRING(h-list.proz1, "->>9.99").
      h-list-epreis = STRING(h-list.epreis, "->,>>>,>>>,>>9.99").
      h-list-cost = STRING(h-list.cost, "->,>>>,>>>,>>9.99").
      h-list-margin = STRING(h-list.margin, "->,>>>,>>9.99").
      h-list-t-sales = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99").
      h-list-t-cost = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99").
      h-list-t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99").
      h-list-proz2 = STRING(h-list.proz2, "->>9.99").

      h-list-epreis-non-short-flag = STRING(h-list.epreis, " ->>>,>>>,>>>,>>9"). 
      h-list-cost-non-short-flag = STRING(h-list.cost, " ->>>,>>>,>>>,>>9").
      h-list-t-sales-non-short-flag = STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9").
      h-list-t-cost-non-short-flag = STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9").

      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = STRING(h-list.bezeich, "x(24)"). 
      IF short-flag THEN output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")            
        + STRING(h-list.epreis, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      ELSE output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")           
        + STRING(h-list.epreis, " ->>>,>>>,>>>,>>9")   
        + STRING(h-list.cost, " ->>>,>>>,>>>,>>9")     
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99").  */

        create output-list. 
        output-list.bezeich = h-list.bezeich. 
        IF short-flag THEN output-list.s = STRING(h-list-artnr, "x(9)") 
          /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis, "x(17)") 
          + STRING(h-list-cost, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales, "x(17)") 
          + STRING(h-list-t-cost, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)"). 
        ELSE output-list.s = STRING(h-list-artnr, "x(9)") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis-non-short-flag, "x(17)") 
          + STRING(h-list-cost-non-short-flag, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales-non-short-flag, "x(17)") 
          + STRING(h-list-t-cost-non-short-flag, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)").

      RUN add-sub.
    END. 
    ELSE IF NOT detailed AND curr-sort = 1 THEN 
    FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
      AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) 
      BY h-list.zknr BY h-list.bezeich: 
      IF curr-grp NE h-list.zknr THEN 
      DO: 
        RUN create-sub(curr-grp).
        FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept 
          AND wgrpdep.zknr = h-list.zknr NO-LOCK. 
        curr-grp = h-list.zknr. 
        create output-list. 
        output-list.flag = 1. 
        output-list.s = "     " + STRING(wgrpdep.bezeich, "x(24)"). 
        output-list.bezeich = STRING(wgrpdep.bezeich, "x(24)"). 
      END. 
      IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
      IF h-list.t-sales NE 0 THEN 
        h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
      IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

      /* Malik Serverless 553 */
      h-list-artnr = STRING(h-list.artnr, ">>>>>>>>9").
      h-list-anzahl = STRING(h-list.anzahl, "->>>>9").
      h-list-proz1 =  STRING(h-list.proz1, "->>9.99").
      h-list-epreis = STRING(h-list.epreis, "->,>>>,>>>,>>9.99").
      h-list-cost = STRING(h-list.cost, "->,>>>,>>>,>>9.99").
      h-list-margin = STRING(h-list.margin, "->,>>>,>>9.99").
      h-list-t-sales = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99").
      h-list-t-cost = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99").
      h-list-t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99").
      h-list-proz2 = STRING(h-list.proz2, "->>9.99").

      h-list-epreis-non-short-flag = STRING(h-list.epreis, " ->>>,>>>,>>>,>>9"). 
      h-list-cost-non-short-flag = STRING(h-list.cost, " ->>>,>>>,>>>,>>9").
      h-list-t-sales-non-short-flag = STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9").
      h-list-t-cost-non-short-flag = STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9").

      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = STRING(h-list.bezeich, "x(24)"). 
      IF short-flag THEN output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")            
        + STRING(h-list.epreis, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      ELSE output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")           
        + STRING(h-list.epreis, " ->>>,>>>,>>>,>>9")   
        + STRING(h-list.cost, " ->>>,>>>,>>>,>>9")     
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99").  */
        create output-list. 
        output-list.bezeich = h-list.bezeich. 
        IF short-flag THEN output-list.s = STRING(h-list-artnr, "x(9)") 
          /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis, "x(17)") 
          + STRING(h-list-cost, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales, "x(17)") 
          + STRING(h-list-t-cost, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)"). 
        ELSE output-list.s = STRING(h-list-artnr, "x(9)") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis-non-short-flag, "x(17)") 
          + STRING(h-list-cost-non-short-flag, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales-non-short-flag, "x(17)") 
          + STRING(h-list-t-cost-non-short-flag, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)").
       RUN add-sub.
    END. 
    ELSE IF NOT detailed AND curr-sort = 2 THEN 
    FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
      AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) BY h-list.zknr 
      BY h-list.anzahl descending BY h-list.t-sales descending 
      BY h-list.bezeich: 
      IF curr-grp NE h-list.zknr THEN 
      DO: 
        RUN create-sub(curr-grp).
        FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept 
          AND wgrpdep.zknr = h-list.zknr NO-LOCK. 
        curr-grp = h-list.zknr. 
        create output-list. 
        output-list.flag = 1. 
        /* Malik Serverless 553 Comment
        output-list.s = "     " + STRING(wgrpdep.bezeich, "x(24)"). */ 
        output-list.bezeich = STRING(wgrpdep.bezeich, "x(24)"). 
      END. 
      IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
      IF h-list.t-sales NE 0 THEN 
        h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
      IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

      /* Malik Serverless 553 */
      h-list-artnr = STRING(h-list.artnr, ">>>>>>>>9").
      h-list-anzahl = STRING(h-list.anzahl, "->>>>9").
      h-list-proz1 =  STRING(h-list.proz1, "->>9.99").
      h-list-epreis = STRING(h-list.epreis, "->,>>>,>>>,>>9.99").
      h-list-cost = STRING(h-list.cost, "->,>>>,>>>,>>9.99").
      h-list-margin = STRING(h-list.margin, "->,>>>,>>9.99").
      h-list-t-sales = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99").
      h-list-t-cost = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99").
      h-list-t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99").
      h-list-proz2 = STRING(h-list.proz2, "->>9.99").

      h-list-epreis-non-short-flag = STRING(h-list.epreis, " ->>>,>>>,>>>,>>9"). 
      h-list-cost-non-short-flag = STRING(h-list.cost, " ->>>,>>>,>>>,>>9").
      h-list-t-sales-non-short-flag = STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9").
      h-list-t-cost-non-short-flag = STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9").

      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = STRING(h-list.bezeich, "x(24)"). 
      IF short-flag THEN output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")            
        + STRING(h-list.epreis, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      ELSE output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")           
        + STRING(h-list.epreis, " ->>>,>>>,>>>,>>9")   
        + STRING(h-list.cost, " ->>>,>>>,>>>,>>9")     
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). */
        create output-list. 
        output-list.bezeich = h-list.bezeich. 
        IF short-flag THEN output-list.s = STRING(h-list-artnr, "x(9)") 
          /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis, "x(17)") 
          + STRING(h-list-cost, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales, "x(17)") 
          + STRING(h-list-t-cost, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)"). 
        ELSE output-list.s = STRING(h-list-artnr, "x(9)") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis-non-short-flag, "x(17)") 
          + STRING(h-list-cost-non-short-flag, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales-non-short-flag, "x(17)") 
          + STRING(h-list-t-cost-non-short-flag, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)").
       RUN add-sub.
    END. 
    ELSE IF NOT detailed AND curr-sort = 3 THEN 
    FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
      AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) BY h-list.zknr 
      BY h-list.t-sales descending BY h-list.anzahl descending 
      BY h-list.bezeich: 
      IF curr-grp NE h-list.zknr THEN 
      DO: 
        RUN create-sub(curr-grp).
        FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept 
          AND wgrpdep.zknr = h-list.zknr NO-LOCK. 
        curr-grp = h-list.zknr. 
        create output-list. 
        output-list.flag = 1. 
        /* Malik Serverless 553 Comment
        output-list.s = "     " + STRING(wgrpdep.bezeich, "x(24)"). */
        output-list.bezeich = STRING(wgrpdep.bezeich, "x(24)"). 
      END. 
      IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
      IF h-list.t-sales NE 0 THEN 
        h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
      IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 
      
      /* Malik Serverless 553 */
      h-list-artnr = STRING(h-list.artnr, ">>>>>>>>9").
      h-list-anzahl = STRING(h-list.anzahl, "->>>>9").
      h-list-proz1 =  STRING(h-list.proz1, "->>9.99").
      h-list-epreis = STRING(h-list.epreis, "->,>>>,>>>,>>9.99").
      h-list-cost = STRING(h-list.cost, "->,>>>,>>>,>>9.99").
      h-list-margin = STRING(h-list.margin, "->,>>>,>>9.99").
      h-list-t-sales = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99").
      h-list-t-cost = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99").
      h-list-t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99").
      h-list-proz2 = STRING(h-list.proz2, "->>9.99").

      h-list-epreis-non-short-flag = STRING(h-list.epreis, " ->>>,>>>,>>>,>>9"). 
      h-list-cost-non-short-flag = STRING(h-list.cost, " ->>>,>>>,>>>,>>9").
      h-list-t-sales-non-short-flag = STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9").
      h-list-t-cost-non-short-flag = STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9").

      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = STRING(h-list.bezeich, "x(24)"). 
      IF short-flag THEN output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")            
        + STRING(h-list.epreis, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). 
      ELSE output-list.s = STRING(h-list.artnr, ">>>>>>>>9") 
        /*+ STRING(h-list.bezeich, "x(24)")*/
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.99")           
        + STRING(h-list.epreis, " ->>>,>>>,>>>,>>9")   
        + STRING(h-list.cost, " ->>>,>>>,>>>,>>9")     
        + STRING(h-list.margin, "->,>>>,>>9.99") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(h-list.t-margin, "->,>>>,>>9.99") 
        + STRING(h-list.proz2, "->>9.99"). */
        create output-list. 
        output-list.bezeich = h-list.bezeich. 
        IF short-flag THEN output-list.s = STRING(h-list-artnr, "x(9)") 
          /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis, "x(17)") 
          + STRING(h-list-cost, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales, "x(17)") 
          + STRING(h-list-t-cost, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)"). 
        ELSE output-list.s = STRING(h-list-artnr, "x(9)") 
        /*+ STRING(h-list.bezeich, "x(24)")*/ 
          + STRING(h-list-anzahl, "x(6)") 
          + STRING(h-list-proz1, "x(7)")            
          + STRING(h-list-epreis-non-short-flag, "x(17)") 
          + STRING(h-list-cost-non-short-flag, "x(17)")      
          + STRING(h-list-margin, "x(13)") 
          + STRING(h-list-t-sales-non-short-flag, "x(17)") 
          + STRING(h-list-t-cost-non-short-flag, "x(17)") 
          + STRING(h-list-t-margin, "x(13)") 
          + STRING(h-list-proz2, "x(7)").
       RUN add-sub.
    END. 
    RUN create-sub(curr-grp).
    IF pos AND t-sales NE 0 THEN 
    DO: 
      
      t-margin = 0. 
      IF t-sales NE 0 THEN t-margin = t-cost / t-sales * 100. 

      /* Malik Serverless 553 */
      t-anz-tot = STRING(t-anz, "->>>>9").
      hundred-tot = STRING(100, "->>9.99").
      t-sales-tot = STRING(t-sales, "->,>>>,>>>,>>9.99").
      t-cost-tot = STRING(t-cost, "->,>>>,>>>,>>9.99").
      t-margin-tot = STRING(t-margin, "->,>>>,>>9.99").
      t-sales-tot-non-short-flag = STRING(t-sales, " ->>>,>>>,>>>,>>9").
      t-cost-tot-non-short-flag = STRING(t-cost, " ->>>,>>>,>>>,>>9").

      /* Malik Serverless 553 Comment 
      create output-list. 
      output-list.bezeich = "T o t a l". 
      IF short-flag THEN output-list.s = "         "  
        + STRING(t-anz, "->>>>9") 
        + STRING(100, "->>9.99") 
        + STRING("", "x(47)")
        + STRING(t-sales, "->,>>>,>>>,>>9.99")
        + STRING(t-cost, "->,>>>,>>>,>>9.99") 
        + STRING(t-margin, "->,>>>,>>9.99") 
        + STRING(100, "->>9.99"). 
      ELSE output-list.s = "     " 
        + STRING(t-anz, "->>>>9") 
        + STRING(100, "->>9.99") 
        + STRING("", "x(47)") 
        + STRING(t-sales, " ->>>,>>>,>>>,>>9") 
        + STRING(t-cost, " ->>>,>>>,>>>,>>9") 
        + STRING(t-margin, "->,>>>,>>9.99") 
        + STRING(100, "->>9.99"). 
      create output-list. */

      create output-list. 
      output-list.bezeich = "T o t a l". 
      IF short-flag THEN output-list.s = STRING(" ", "x(9)")  
        + STRING(t-anz-tot, "x(6)") 
        + STRING(hundred-tot, "x(7)") 
        + STRING("", "x(47)")
        + STRING(t-sales-tot, "x(17)")
        + STRING(t-cost-tot, "x(17)") 
        + STRING(t-margin-tot, "x(13)") 
        + STRING(hundred-tot, "x(7)"). 
      ELSE output-list.s = STRING(" ", "x(5)") /* "     " */ 
      + STRING(t-anz-tot, "x(6)") 
      + STRING(hundred-tot, "x(7)") 
      + STRING("", "x(47)")
      + STRING(t-sales-tot-non-short-flag, "x(17)")
      + STRING(t-cost-tot-non-short-flag, "x(17)") 
      + STRING(t-margin-tot, "x(13)") 
      + STRING(hundred-tot, "x(7)"). 
      create output-list.
    END. 
  END. 
END. 

PROCEDURE create-sub:
    DEFINE INPUT PARAMETER curr-grp AS INTEGER.

    /* Malik Serverless 553 */
    DEFINE VARIABLE s-anzahl-sub-tot AS CHAR.
    DEFINE VARIABLE s-proz1-sub-tot AS CHAR.
    DEFINE VARIABLE st-sales-sub-tot AS CHAR.
    DEFINE VARIABLE st-cost-sub-tot AS CHAR.
    DEFINE VARIABLE st-margin-sub-tot AS CHAR.
    DEFINE VARIABLE st-proz2-sub-tot AS CHAR.
    DEFINE VARIABLE st-sales-sub-tot-non-short-flag AS CHAR.
    DEFINE VARIABLE st-cost-sub-tot-non-short-flag AS CHAR.

    IF curr-grp NE 0 THEN
    DO:
        IF st-sales NE 0 THEN
            st-margin = st-cost / st-sales * 100.

        /* Malik Serverless 553 */
        s-anzahl-sub-tot = STRING(s-anzahl, "->>>>9").
        s-proz1-sub-tot = STRING(s-proz1, "->>9.99").
        st-sales-sub-tot = STRING(st-sales, "->,>>>,>>>,>>9.99").
        st-cost-sub-tot = STRING(st-cost, "->,>>>,>>>,>>9.99").
        st-margin-sub-tot = STRING(st-margin, "->,>>>,>>9.99").
        st-proz2-sub-tot = STRING(st-proz2, "->>9.9").
        st-sales-sub-tot-non-short-flag = STRING(st-sales, " ->>>,>>>,>>>,>>9").
        st-cost-sub-tot-non-short-flag = STRING(st-cost, " ->>>,>>>,>>>,>>9").

        /* Malik Serverless 553 Comment 
        CREATE output-list.
        IF short-flag THEN
        DO:
            ASSIGN
                output-list.flag = 2
                output-list.bezeich = "S u b T o t a l"
                output-list.s = "         " 
                /*+ STRING("S u b T o t a l", "x(24)")*/
                + STRING(s-anzahl, "->>>>9") 
                + STRING(s-proz1, "->>9.99") 
                + STRING(" ", "x(47)")
                + STRING(st-sales, "->,>>>,>>>,>>9.99") 
                + STRING(st-cost, "->,>>>,>>>,>>9.99") 
                + STRING(st-margin, "->,>>>,>>9.99") 
                + STRING(st-proz2, "->>9.9").
        END.        
        ELSE
        DO:
            ASSIGN
                output-list.flag = 2
                output-list.bezeich = "S u b T o t a l"
                output-list.s = "         " 
                /*+ STRING("S u b T o t a l", "x(24)")*/
                + STRING(s-anzahl, "->>>>9") 
                + STRING(s-proz1, "->>9.99") 
                + STRING(" ", "x(47)")
                + STRING(st-sales, " ->>>,>>>,>>>,>>9") 
                + STRING(st-cost, " ->>>,>>>,>>>,>>9") 
                + STRING(st-margin, "->,>>>,>>9.99") 
                + STRING(st-proz2, "->>9.9").
        END. */

        CREATE output-list.
        IF short-flag THEN
        DO:
            ASSIGN
                output-list.flag = 2
                output-list.bezeich = "S u b T o t a l"
                output-list.s = STRING(" ", "x(9)") 
                /*+ STRING("S u b T o t a l", "x(24)")*/
                + STRING(s-anzahl-sub-tot, "x(6)") 
                + STRING(s-proz1-sub-tot, "x(7)") 
                + STRING(" ", "x(47)")
                + STRING(st-sales-sub-tot, "x(17)") 
                + STRING(st-cost-sub-tot, "x(17)") 
                + STRING(st-margin-sub-tot, "x(13)") 
                + STRING(st-proz2-sub-tot, "x(6)").
        END.        
        ELSE
        DO:
          ASSIGN
            output-list.flag = 2
            output-list.bezeich = "S u b T o t a l"
            output-list.s = STRING(" ", "x(9)") 
            /*+ STRING("S u b T o t a l", "x(24)")*/
            + STRING(s-anzahl-sub-tot, "x(6)") 
            + STRING(s-proz1-sub-tot, "x(7)") 
            + STRING(" ", "x(47)")
            + STRING(st-sales-sub-tot-non-short-flag, "x(17)") 
            + STRING(st-cost-sub-tot-non-short-flag, "x(17)") 
            + STRING(st-margin-sub-tot, "x(13)") 
            + STRING(st-proz2-sub-tot, "x(6)").
        END.
        ASSIGN 
            s-anzahl    = 0
            s-proz1     = 0
            st-sales    = 0
            st-cost     = 0
            st-margin   = 0
            st-proz2    = 0.
    END.
END.


PROCEDURE add-sub:
     ASSIGN
        s-anzahl    = s-anzahl + h-list.anzahl
        /*s-epreis    = s-epreis + h-list.epreis
        s-cost      = s-cost   + h-list.cost*/
        st-sales    = st-sales + h-list.t-sales
        st-cost     = st-cost  + h-list.t-cost 
        s-proz1     = s-proz1  + h-list.proz1
        st-proz2    = st-proz2 + h-list.proz2
        .
END.


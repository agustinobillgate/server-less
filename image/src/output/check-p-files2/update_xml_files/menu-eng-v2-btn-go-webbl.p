DEFINE TEMP-TABLE subgr-list 
  FIELD SELECTED   AS LOGICAL INITIAL YES
  FIELD subnr      AS INTEGER 
  FIELD bezeich    AS CHAR    FORMAT "x(75)".
 
DEFINE TEMP-TABLE output-list 
  FIELD flag AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(75)" LABEL "Description" 
  FIELD s AS CHAR. 

DEFINE TEMP-TABLE h-list 
  FIELD flag       AS CHAR FORMAT "x(2)" INITIAL "" 
  FIELD artnr      AS INTEGER FORMAT ">>>>9" INITIAL 0 
  FIELD dept       AS INTEGER 
  FIELD bezeich    AS CHAR FORMAT "x(75)" INITIAL "" 
  FIELD zknr       AS INTEGER 
  FIELD grpname    AS CHAR FORMAT "x(50)" 
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
    FIELD artnr               AS INTEGER FORMAT ">>>>9"          INITIAL 0 
    FIELD bezeich             AS CHAR    FORMAT "x(75)"          INITIAL "" 
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
  FIELD flag            AS INTEGER 
  FIELD artnr           AS INTEGER FORMAT ">>>>9" INITIAL 0
  FIELD dept            AS CHAR
  FIELD bezeich         AS CHAR FORMAT "x(75)" LABEL "Description"
  FIELD zknr            AS INTEGER
  FIELD grpname         AS CHAR FORMAT "x(50)"
  FIELD anzahl          AS INTEGER FORMAT ">>>>>9" INITIAL 0 LABEL "Qty"
  FIELD proz1           AS DECIMAL FORMAT ">>9.99" INITIAL 0 LABEL "(%)"
  FIELD epreis          AS DECIMAL FORMAT ">,>>>,>>9.99" INITIAL 0 LABEL "Unit-Price"
  FIELD cost            AS DECIMAL FORMAT ">,>>>,>>9.99" INITIAL 0 LABEL "Unit-Cost"
  FIELD margin          AS DECIMAL FORMAT "->>>,>>9.99" INITIAL 0 LABEL "Ratio"
  FIELD item-prof       AS DECIMAL FORMAT ">>>,>>>,>>9.99" INITIAL 0 LABEL "Item Profit"
  FIELD t-sales         AS DECIMAL FORMAT ">>>,>>>,>>9.99" INITIAL 0 LABEL "Sales"
  FIELD t-cost          AS DECIMAL FORMAT ">>>,>>>,>>9.99" INITIAL 0 LABEL "Cost"
  FIELD t-margin        AS DECIMAL FORMAT "->,>>>,>>9.99" INITIAL 0 LABEL "Ratio"
  FIELD profit          AS DECIMAL FORMAT ">>>,>>>,>>9.99" INITIAL 0 LABEL "Total Profit"
  FIELD proz2           AS DECIMAL FORMAT ">>9.99" INITIAL 0 LABEL "(%)"
  FIELD profit-cat      AS CHAR FORMAT "x(4)"  LABEL "Profit Category"
  FIELD popularity-cat  AS CHAR FORMAT "x(4)"  LABEL "Popularity Category"
  FIELD menu-item-class AS CHAR FORMAT "x(10)" LABEL "Menu Item Class"
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
DEFINE VARIABLE curr-grp         AS INTEGER INITIAL 0. 
DEFINE VARIABLE grp-bez          AS CHAR.

IF sorttype = 1 THEN RUN create-h-umsatz1. 
ELSE IF sorttype = 2 THEN RUN create-h-umsatz2. 
/*masdod 18122024 rombak struktur coding*/
FOR EACH output-list2:
    gtotal-sold    = gtotal-sold    + output-list2.anzahl.
    gtotal-sold%   = gtotal-sold%   + output-list2.proz1.
    gtotal-cost    = gtotal-cost    + output-list2.t-cost.
    gtotal-revenue = gtotal-revenue + output-list2.t-sales.
    gtotal-profit  = gtotal-profit  + output-list2.profit.

    IF output-list2.artnr NE 0 THEN count-foodcost = count-foodcost + 1.
END.
avrg-item-profit = gtotal-profit / gtotal-sold.
menu-pop-factor  = ((1 / count-foodcost) * 0.8 ).
FOR EACH output-list2:
    IF output-list2.item-prof LT avrg-item-profit THEN output-list2.profit-cat = "LOW".
    ELSE output-list2.profit-cat = "HIGH".

    IF output-list2.proz1 LT menu-pop-factor THEN output-list2.popularity-cat = "LOW".
    ELSE output-list2.popularity-cat = "HIGH".
    
    IF output-list2.profit-cat EQ "LOW" AND output-list2.popularity-cat EQ "LOW" THEN output-list2.menu-item-class = "DOG".   
    ELSE IF output-list2.profit-cat EQ "LOW" AND output-list2.popularity-cat EQ "HIGH" THEN output-list2.menu-item-class = "WORKHORSE".
    ELSE IF output-list2.profit-cat EQ "HIGH" AND output-list2.popularity-cat EQ "LOW" THEN output-list2.menu-item-class = "CHALLENGE".
    ELSE IF output-list2.profit-cat EQ "HIGH" AND output-list2.popularity-cat EQ "HIGH" THEN output-list2.menu-item-class = "STAR".
END.
/*
/* Rulita 09/06/22 */
FOR EACH output-list:
    CREATE fb-cost-analyst.
    ASSIGN             
    fb-cost-analyst.flag         = output-list.flag
    fb-cost-analyst.bezeich      = output-list.bezeich
    fb-cost-analyst.artnr        = INTEGER(SUBSTRING(output-list.s,1,5))
    fb-cost-analyst.qty          = INTEGER(SUBSTRING(output-list.s,30,6)) 
    fb-cost-analyst.proz1        = DECIMAL(SUBSTRING(output-list.s,36,6))
    fb-cost-analyst.epreis       = DECIMAL(SUBSTRING(output-list.s,42,12)) 
    fb-cost-analyst.cost         = DECIMAL(SUBSTRING(output-list.s,54,12))
    fb-cost-analyst.margin       = DECIMAL(SUBSTRING(output-list.s,66,12))
    fb-cost-analyst.t-sales      = DECIMAL(SUBSTRING(output-list.s,78,15))
    fb-cost-analyst.t-cost       = DECIMAL(SUBSTRING(output-list.s,93,15))
    fb-cost-analyst.t-margin     = DECIMAL(SUBSTRING(output-list.s,108,13))
    fb-cost-analyst.proz2        = DECIMAL(SUBSTRING(output-list.s,121,6))
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
    
    IF profit-category EQ "LOW" AND popularity-category EQ "LOW" THEN fb-cost-analyst.menu-item-class = "DOG".   
    ELSE IF profit-category EQ "LOW" AND popularity-category EQ "HIGH" THEN fb-cost-analyst.menu-item-class = "WORKHORSE".
    ELSE IF profit-category EQ "HIGH" AND popularity-category EQ "LOW" THEN fb-cost-analyst.menu-item-class = "CHALLENGE".
    ELSE IF profit-category EQ "HIGH" AND popularity-category EQ "HIGH" THEN fb-cost-analyst.menu-item-class = "STAR".
END.

/* Rulita 09/06/22 */
FOR EACH fb-cost-analyst:
    CREATE output-list2.
    ASSIGN 
    output-list2.artnr           = fb-cost-analyst.artnr
    output-list2.bezeich         = STRING(fb-cost-analyst.bezeich)     
    output-list2.anzahl          = fb-cost-analyst.qty
    output-list2.proz1           = fb-cost-analyst.proz1               
    output-list2.epreis          = fb-cost-analyst.epreis  
    output-list2.cost            = fb-cost-analyst.cost                         
    output-list2.margin          = fb-cost-analyst.margin                      
    output-list2.item-prof       = fb-cost-analyst.item-profit           
    output-list2.t-sales         = fb-cost-analyst.t-sales                 
    output-list2.t-cost          = fb-cost-analyst.t-cost                 
    output-list2.t-margin        = fb-cost-analyst.t-margin              
    output-list2.profit          = fb-cost-analyst.total-profit        
    output-list2.proz2           = fb-cost-analyst.proz2                 
    output-list2.profit-cat      = STRING(fb-cost-analyst.profit-category)               
    output-list2.popularity-cat  = STRING(fb-cost-analyst.popularity-category)   
    output-list2.menu-item-class = STRING(fb-cost-analyst.menu-item-class)       
    .
END.

/* Rulita 09/06/22 */
FOR EACH output-list2:
    IF output-list2.artnr EQ 0 AND output-list2.bezeich NE "T o t a l"  THEN
    ASSIGN 
    output-list2.artnr           = 0      
    output-list2.bezeich         = output-list2.bezeich     
    output-list2.anzahl          = 0      
    output-list2.proz1           = 0
    output-list2.epreis          = 0    
    output-list2.cost            = 0                        
    output-list2.margin          = 0                      
    output-list2.item-prof       = 0
    output-list2.t-sales         = 0            
    output-list2.t-cost          = 0             
    output-list2.t-margin        = 0        
    output-list2.profit          = 0          
    output-list2.proz2           = 0
    output-list2.profit-cat      = STRING("")               
    output-list2.popularity-cat  = STRING("")   
    output-list2.menu-item-class = STRING("")
    .
    ELSE IF output-list2.bezeich EQ "T o t a l" THEN
    ASSIGN 
    output-list2.artnr           = 0        
    output-list2.bezeich         = output-list2.bezeich
    output-list2.anzahl          = output-list2.anzahl       
    output-list2.proz1           = 100                 
    output-list2.epreis          = 0   
    output-list2.cost            = 0                       
    output-list2.margin          = 0                     
    output-list2.item-prof       = 0
    output-list2.t-sales         = output-list2.t-sales                 
    output-list2.t-cost          = output-list2.t-cost                
    output-list2.t-margin        = output-list2.t-margin        
    output-list2.profit          = 0          
    output-list2.proz2           = 100                
    output-list2.profit-cat      = STRING("")               
    output-list2.popularity-cat  = STRING("")   
    output-list2.menu-item-class = STRING("")       
    .
    ELSE IF output-list2.bezeich EQ "" THEN
    ASSIGN 
    output-list2.artnr           = 0        
    output-list2.bezeich         = STRING("")     
    output-list2.anzahl          = 0      
    output-list2.proz1           = 0
    output-list2.epreis          = 0    
    output-list2.cost            = 0                        
    output-list2.margin          = 0                      
    output-list2.item-prof       = 0
    output-list2.t-sales         = 0            
    output-list2.t-cost          = 0             
    output-list2.t-margin        = 0        
    output-list2.profit          = 0          
    output-list2.proz2           = 0
    output-list2.profit-cat      = STRING("")               
    output-list2.popularity-cat  = STRING("")   
    output-list2.menu-item-class = STRING("")
    .
END.
*/
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
            output-list.s = "     " + STRING(hoteldpt.num,"99 ") + STRING(hoteldpt.depart,"x(21)"). 
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
                FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
                    AND h-cost.departement = h-artikel.departement 
                    AND h-cost.datum = to-date 
                    AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
   
                RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,to-date, 
                                       OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
                ASSIGN vat = vat + vat2.
                
                CREATE h-list. 
                IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN h-list.cost = h-cost.betrag. 
                ELSE h-list.cost = h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
                h-list.cost      = h-list.cost / fact1. 
                h-list.dept      = h-artikel.departement. 
                h-list.artnr     = h-artikel.artnr. 
                h-list.dept      = h-artikel.departement. 
                h-list.bezeich   = h-artikel.bezeich. 
                h-list.zknr      = h-artikel.zwkum. 
                
                IF vat-included THEN h-list.epreis = h-artikel.epreis1 * exchg-rate / fact. 
                ELSE h-list.epreis = h-artikel.epreis1 * exchg-rate / fact1. 
                
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
      output-list.s = "     " + STRING(hoteldpt.num,"99 ") 
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
          FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
            AND h-cost.departement = h-artikel.departement 
            AND h-cost.datum = to-date AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
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
          IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
            h-list.cost = h-cost.betrag. 
          ELSE h-list.cost = h-artikel.epreis1 * h-artikel.prozent / 100 
            * exchg-rate. 
          h-list.cost = h-list.cost / fact1. 
          h-list.dept = h-artikel.departement. 
          h-list.artnr = h-artikel.artnr. 
          h-list.dept = h-artikel.departement. 
          h-list.bezeich = h-artikel.bezeich. 
          h-list.zknr = h-artikel.zwkum. 
     
          IF vat-included THEN 
            h-list.epreis = h-artikel.epreis1 * exchg-rate / fact. 
          ELSE h-list.epreis = h-artikel.epreis1 * exchg-rate / fact1. 
     
          
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
    DO: 
        IF mi-subgrp THEN 
        DO: 
            RUN create-list1(pos). 
            RETURN. 
        END. 
        IF detailed AND curr-sort = 1 THEN 
        DO:
            FOR EACH h-list WHERE h-list.dept = hoteldpt.num: 
                RUN do-create-list.          
            END. 
        END.
        ELSE IF detailed AND curr-sort = 2 THEN 
        DO:
            FOR EACH h-list WHERE h-list.dept = hoteldpt.num BY h-list.anzahl descending BY h-list.t-sales descending BY h-list.bezeich: 
                RUN do-create-list.
            END. 
        END.
        ELSE IF detailed AND curr-sort = 3 THEN 
        DO:
            FOR EACH h-list WHERE h-list.dept = hoteldpt.num BY h-list.t-sales descending BY h-list.anzahl descending BY h-list.bezeich: 
                RUN do-create-list.
            END. 
        END.
        ELSE IF NOT detailed AND curr-sort = 1 THEN 
        DO:
            FOR EACH h-list WHERE h-list.dept = hoteldpt.num AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0): 
                RUN do-create-list.
            END. 
        END.
        ELSE IF NOT detailed AND curr-sort = 2 THEN 
        DO:
            FOR EACH h-list WHERE h-list.dept = hoteldpt.num AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) BY h-list.anzahl descending BY h-list.t-sales descending BY h-list.bezeich: 
                RUN do-create-list.
            END.
        END.
        ELSE IF NOT detailed AND curr-sort = 3 THEN 
        DO:
            FOR EACH h-list WHERE h-list.dept = hoteldpt.num AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) BY h-list.t-sales descending BY h-list.anzahl descending BY h-list.bezeich: 
                RUN do-create-list.
            END. 
        END.

        IF pos AND t-sales NE 0 THEN 
        DO: 
            t-margin = 0. 
            IF t-sales NE 0 THEN t-margin = t-cost / t-sales * 100. 
            create output-list. 
            output-list.bezeich = STRING("T o t a l", "x(24)"). 
            IF short-flag THEN output-list.s = "     " + STRING("T o t a l", "x(24)") 
            + STRING(t-anz, ">>,>>9") 
            + STRING(100, ">>9.99") 
            + STRING("", "x(36)") + "  "
            + STRING(t-sales, " ->>>,>>>,>>9") + "  "
            + STRING(t-cost, " ->>>,>>>,>>9") 
            + STRING(t-margin, " ->>>,>>9.99 ") 
            + STRING(100, ">>9.99"). 
            ELSE output-list.s = "     " + STRING("T o t a l", "x(24)") 
            + STRING(t-anz, ">>,>>9") 
            + STRING(100, ">>9.99") 
            + STRING("", "x(36)") + "  "
            + STRING(t-sales, " ->,>>>,>>>,>>9") + "  " 
            + STRING(t-cost, " ->>>,>>>,>>9") 
            + STRING(t-margin, " ->>>,>>9.99 ") 
            + STRING(100, ">>9.99"). 
            create output-list. 

            CREATE output-list2.                                            
            ASSIGN                                                                    
            output-list2.bezeich   = "T o t a l"
            output-list2.anzahl    = t-anz        
            output-list2.proz1     = 100                        
            output-list2.t-sales   = t-sales          
            output-list2.t-cost    = t-cost           
            output-list2.t-margin  = t-margin         
            output-list2.proz2     = 100.
            CREATE output-list2.
        END. 
    END. 
END. 

PROCEDURE create-list1: 
    DEFINE INPUT PARAMETER pos AS LOGICAL. 
    DO: 
        IF detailed AND curr-sort = 1 THEN 
        DO:
            FOR EACH h-list WHERE h-list.dept = hoteldpt.num BY h-list.zknr BY h-list.bezeich: 
                RUN do-create-list1.   
            END. 
        END.
        ELSE IF detailed AND curr-sort = 2 THEN 
        DO:
            FOR EACH h-list WHERE h-list.dept = hoteldpt.num BY h-list.zknr BY h-list.anzahl descending BY h-list.t-sales descending BY h-list.bezeich: 
                RUN do-create-list1. 
            END. 
        END.
        ELSE IF detailed AND curr-sort = 3 THEN 
        DO:
            FOR EACH h-list WHERE h-list.dept = hoteldpt.num BY h-list.zknr BY h-list.t-sales descending BY h-list.anzahl descending BY h-list.bezeich: 
                RUN do-create-list1. 
            END.
        END.
        ELSE IF NOT detailed AND curr-sort = 1 THEN 
        DO:
            FOR EACH h-list WHERE h-list.dept = hoteldpt.num AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) BY h-list.zknr BY h-list.bezeich: 
                RUN do-create-list1. 
            END.
        END.
        ELSE IF NOT detailed AND curr-sort = 2 THEN 
        DO:
            FOR EACH h-list WHERE h-list.dept = hoteldpt.num AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) BY h-list.zknr BY h-list.anzahl descending BY h-list.t-sales descending BY h-list.bezeich: 
                RUN do-create-list1. 
            END. 
        END.
        ELSE IF NOT detailed AND curr-sort = 3 THEN 
        DO:
            FOR EACH h-list WHERE h-list.dept = hoteldpt.num AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) BY h-list.zknr BY h-list.t-sales descending BY h-list.anzahl descending BY h-list.bezeich: 
                RUN do-create-list1. 
            END. 
        END.

        RUN create-sub(curr-grp).
        IF pos AND t-sales NE 0 THEN 
        DO: 
            t-margin = 0. 
            IF t-sales NE 0 THEN t-margin = t-cost / t-sales * 100. 
            create output-list. 
            output-list.bezeich = STRING("T o t a l", "x(24)"). 
            IF short-flag THEN output-list.s = "     " + STRING("T o t a l", "x(24)") 
            + STRING(t-anz, ">>,>>9") 
            + STRING(100, ">>9.99") 
            + STRING("", "x(36)") + "  "
            + STRING(t-sales, " ->>>,>>>,>>9") + "  " 
            + STRING(t-cost, " ->>>,>>>,>>9") 
            + STRING(t-margin, " ->>>,>>9.99 ") 
            + STRING(100, ">>9.99"). 
            ELSE output-list.s = "     " + STRING("T o t a l", "x(24)") 
            + STRING(t-anz, ">>,>>9") 
            + STRING(100, ">>9.99") 
            + STRING("", "x(36)") + "  "
            + STRING(t-sales, " ->,>>>,>>>,>>9") + "  " 
            + STRING(t-cost, " ->>>,>>>,>>9") 
            + STRING(t-margin, " ->>>,>>9.99 ") 
            + STRING(100, ">>9.99"). 
            create output-list. 

            CREATE output-list2.                                            
            ASSIGN                                                                    
            output-list2.bezeich   = "T o t a l"
            output-list2.anzahl    = t-anz        
            output-list2.proz1     = 100                        
            output-list2.t-sales   = t-sales          
            output-list2.t-cost    = t-cost           
            output-list2.t-margin  = t-margin         
            output-list2.proz2     = 100.
            CREATE output-list2.
        END. 
    END. 
END. 

PROCEDURE create-outlist:
    CREATE output-list2.                                            
    ASSIGN                                                          
    output-list2.artnr     = h-list.artnr           
    output-list2.bezeich   = h-list.bezeich
    output-list2.anzahl    = h-list.anzahl         
    output-list2.proz1     = h-list.proz1          
    output-list2.epreis    = h-list.epreis           
    output-list2.cost      = h-list.cost             
    output-list2.margin    = h-list.margin                
    output-list2.t-sales   = h-list.t-sales          
    output-list2.t-cost    = h-list.t-cost           
    output-list2.t-margin  = h-list.t-margin         
    output-list2.proz2     = h-list.proz2  
    output-list2.item-prof = output-list2.epreis - output-list2.cost
    output-list2.profit    = output-list2.t-sales - output-list2.t-cost.

    
END.

PROCEDURE do-create-list:
    IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
    IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
    IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 
    CREATE output-list.   
    output-list.bezeich = STRING(h-list.bezeich, "x(75)"). 
    IF short-flag THEN 
    DO:
        ASSIGN output-list.s = STRING(h-list.artnr, ">>>>9") 
        + STRING(h-list.bezeich, "x(75)") 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.9") 
        + STRING(h-list.epreis, "->,>>>,>>9.9") 
        + STRING(h-list.cost, "->,>>>,>>9.9") 
        + STRING(h-list.margin, "->>>,>>9.99 ") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>9.9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>9.9") 
        + STRING(h-list.t-margin, " ->>>,>>9.99 ") 
        + STRING(h-list.proz2, "->>9.9"). 
    END.
    ELSE 
    DO:
        ASSIGN output-list.s = STRING(h-list.artnr, ">>>>9") 
        + STRING(h-list.bezeich, "x(75)") 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.9") 
        + STRING(h-list.epreis, "->>>,>>>,>>9") 
        + STRING(h-list.cost, "->>>,>>>,>>9") 
        + STRING(h-list.margin, "->>>,>>9.99 ") 
        + STRING(h-list.t-sales, " ->,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>9") 
        + STRING(h-list.t-margin, " ->>>,>>9.99 ") 
        + STRING(h-list.proz2, "->>9.9").                 
    END.
    RUN create-outlist.  
END.

PROCEDURE do-create-list1:
    IF curr-grp NE h-list.zknr THEN 
    DO: 
        RUN create-sub(curr-grp).
        FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept AND wgrpdep.zknr = h-list.zknr NO-LOCK NO-ERROR. 
        IF AVAILABLE wgrpdep THEN grp-bez = wgrpdep.bezeich.
        ELSE grp-bez = "".

        curr-grp = h-list.zknr. 
        CREATE output-list. 
        output-list.flag = 1. 
        output-list.s = "     " + STRING(grp-bez, "x(75)"). 
        output-list.bezeich = STRING(grp-bez, "x(75)"). 
    END. 
    IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
    IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
    IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 
    create output-list. 
    output-list.bezeich = STRING(h-list.bezeich, "x(75)"). 
    IF short-flag THEN
    DO:
        ASSIGN
        output-list.s = STRING(h-list.artnr, ">>>>9") 
        + STRING(h-list.bezeich, "x(75)") 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.9") 
        + STRING(h-list.epreis, "->,>>>,>>9.9") 
        + STRING(h-list.cost, "->,>>>,>>9.9") 
        + STRING(h-list.margin, "->>>,>>9.99 ") 
        + STRING(h-list.t-sales, " ->>>,>>>,>>9.9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>9.9") 
        + STRING(h-list.t-margin, " ->>>,>>9.99 ") 
        + STRING(h-list.proz2, "->>9.9").
    END.
    ELSE 
    DO:
        ASSIGN
        output-list.s = STRING(h-list.artnr, ">>>>9") 
        + STRING(h-list.bezeich, "x(75)") 
        + STRING(h-list.anzahl, "->>>>9") 
        + STRING(h-list.proz1, "->>9.9") 
        + STRING(h-list.epreis, "->>>,>>>,>>9") 
        + STRING(h-list.cost, "->>>,>>>,>>9") 
        + STRING(h-list.margin, "->>>,>>9.99 ") 
        + STRING(h-list.t-sales, " ->,>>>,>>>,>>9") 
        + STRING(h-list.t-cost, " ->>>,>>>,>>9") 
        + STRING(h-list.t-margin, " ->>>,>>9.99 ") 
        + STRING(h-list.proz2, "->>9.9"). 
    END.
    RUN add-sub. 
    RUN create-outlist.
END.

PROCEDURE create-sub:
    DEFINE INPUT PARAMETER curr-grp AS INTEGER.
    IF curr-grp NE 0 THEN
    DO:
        IF st-sales NE 0 THEN st-margin = st-cost / st-sales * 100.
        CREATE output-list.
        ASSIGN
            output-list.flag = 2
            output-list.bezeich = "S u b T o t a l"
            output-list.s = STRING("     ", "x(5)") 
            + STRING("S u b T o t a l", "x(24)")
            + STRING(s-anzahl, "->>>>9") 
            + STRING(s-proz1, "->>9.9") 
            + STRING(" ", "x(36)")
            + STRING(st-sales, " ->,>>>,>>>,>>9") 
            + STRING(st-cost, " ->>>,>>>,>>9") 
            + STRING(st-margin, " ->>>,>>9.99 ") 
            + STRING(st-proz2, "->>9.9").
            
        CREATE output-list2.                                            
        ASSIGN                                                                    
            output-list2.bezeich   = "S u b T o t a l"
            output-list2.anzahl    = s-anzahl        
            output-list2.proz1     = s-proz1                        
            output-list2.t-sales   = st-sales          
            output-list2.t-cost    = st-cost           
            output-list2.t-margin  = st-margin         
            output-list2.proz2     = st-proz2.
            CREATE output-list2.

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


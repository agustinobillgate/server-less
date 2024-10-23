DEFINE TEMP-TABLE subgr-list 
  FIELD SELECTED   AS LOGICAL INITIAL YES
  FIELD subnr      AS INTEGER 
  FIELD bezeich    AS CHAR    FORMAT "x(24)". 

DEFINE WORKFILE h-list 
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
  FIELD margin     AS DECIMAL FORMAT "->>>,>>9.99" INITIAL 0 /*Orig ->>9.99*/
  FIELD t-sales    AS DECIMAL FORMAT ">>,>>>,>>9.99" INITIAL 0 
  FIELD t-cost     AS DECIMAL FORMAT ">>,>>>,>>9.99" INITIAL 0 
  FIELD t-margin   AS DECIMAL FORMAT "->>>,>>9.99" INITIAL 0 /*Orig ->>9.99*/
  FIELD proz2      AS DECIMAL FORMAT ">>9.99" INITIAL 0. 

DEFINE TEMP-TABLE fb-cost-analyst 
    FIELD flag       AS INTEGER
    FIELD artnr      AS CHARACTER FORMAT "x(6)" INITIAL "" 
    FIELD bezeich    AS CHARACTER FORMAT "x(24)" INITIAL "" 
    FIELD qty        AS CHARACTER FORMAT "x(6)" INITIAL ""
    FIELD proz1      AS CHARACTER FORMAT "x(6)" INITIAL "" 
    FIELD epreis     AS CHARACTER FORMAT "x(12)" INITIAL ""
    FIELD cost       AS CHARACTER FORMAT "x(12)" INITIAL "" 
    FIELD margin     AS CHARACTER FORMAT "x(11)" INITIAL "" 
    FIELD t-sales    AS CHARACTER FORMAT "x(14)" INITIAL "" 
    FIELD t-cost     AS CHARACTER FORMAT "x(14)" INITIAL "" 
    FIELD t-margin   AS CHARACTER FORMAT "x(11)" INITIAL ""
    FIELD proz2      AS CHARACTER FORMAT "x(6)" INITIAL ""
.

DEF INPUT PARAMETER TABLE FOR subgr-list.
DEF INPUT PARAMETER sorttype AS INT.
DEF INPUT PARAMETER from-dept AS INT.
DEF INPUT PARAMETER to-dept AS INT.
DEF INPUT PARAMETER dstore AS INT.
DEF INPUT PARAMETER ldry-dept AS INT.
DEF INPUT PARAMETER all-sub AS LOGICAL.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER fact1 AS INT.
DEF INPUT PARAMETER exchg-rate AS DECIMAL.
DEF INPUT PARAMETER vat-included AS LOGICAL.
DEF INPUT PARAMETER mi-subgrp AS LOGICAL. /*MTMENU-ITEM mi-subgrp:CHECKED IN MENU mbar*/
DEF INPUT PARAMETER detailed AS LOGICAL.
DEF INPUT PARAMETER curr-sort AS INT.
DEF INPUT PARAMETER short-flag AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR fb-cost-analyst.

DEFINE VARIABLE t-anz AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-sales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-margin AS DECIMAL INITIAL 0. 

DEFINE VARIABLE st-sales AS DECIMAL INITIAL 0 FORMAT ">>,>>>,>>9.99".
DEFINE VARIABLE st-cost  AS DECIMAL INITIAL 0 FORMAT ">>,>>>,>>9.99".
DEFINE VARIABLE st-margin AS DECIMAL INITIAL 0 FORMAT "->>>,>>9.99". /*Orig ->>9.99*/
DEFINE VARIABLE st-proz2 AS DECIMAL INITIAL 0 FORMAT ">>9.99".

DEFINE VARIABLE s-anzahl AS INTEGER INITIAL 0 FORMAT "->>>>>9". 
DEFINE VARIABLE s-proz1  AS DECIMAL INITIAL 0 FORMAT ">>9.99". 

IF sorttype = 1 THEN RUN create-h-umsatz1. 
ELSE IF sorttype = 2 THEN RUN create-h-umsatz2.
ELSE IF sorttype = 3 THEN RUN create-h-umsatz3.

PROCEDURE create-h-umsatz1: 
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
 
  FOR EACH fb-cost-analyst: 
    DELETE fb-cost-analyst. 
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
 
      CREATE fb-cost-analyst. 
      fb-cost-analyst.bezeich = STRING(hoteldpt.num,"99 ") 
        + STRING(hoteldpt.depart,"x(21)").       
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
          FIND FIRST subgr-list WHERE subgr-list.subnr = h-artikel.zwkum 
              AND subgr-list.SELECTED NO-LOCK NO-ERROR.
          do-it = AVAILABLE subgr-list.
      END.
      IF do-it THEN
      DO:
          /*MTcurr-bezeich = STRING(h-artikel.artnr, ">>>>9") + " " 
            + h-artikel.bezeich. 
          DISP curr-bezeich WITH FRAME frame2.*/
          
          FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
            AND h-cost.departement = h-artikel.departement 
            AND h-cost.datum = to-date AND h-cost.flag = 1 NO-LOCK NO-ERROR. 

/*
          /* ITA
          RUN calc-servvat.p(h-artikel.departement, h-artikel.artnr, to-date, h-artikel.service-code, 
                               h-artikel.mwst-code, OUTPUT serv, OUTPUT vat).*/
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
          ELSE h-list.cost = h-artikel.epreis1 * h-artikel.prozent / 100 * exchg-rate. 
          h-list.cost = h-list.cost / fact1. 
          h-list.dept = h-artikel.departement. 
          h-list.artnr = h-artikel.artnr. 
          h-list.dept = h-artikel.departement. 
          h-list.bezeich = h-artikel.bezeich. 
          h-list.zknr = h-artikel.zwkum. 
     
          IF vat-included THEN 
            h-list.epreis = h-artikel.epreis1 * exchg-rate / fact. 
          ELSE h-list.epreis = h-artikel.epreis1 * exchg-rate / fact1. 
     
          /* FDL Comment
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
          END. /* do datum*/
          */
          /*FDL Feb 26, 2024 => Ticket 385FD3*/
          FIND FIRST h-umsatz WHERE h-umsatz.artnr EQ h-artikel.artnr 
              AND h-umsatz.departement EQ h-artikel.departement 
              AND h-umsatz.datum GE from-date
              AND h-umsatz.datum LE to-date USE-INDEX hrartatz_ix NO-LOCK NO-ERROR.
          DO WHILE AVAILABLE h-umsatz:

              RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
                  h-umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
              ASSIGN vat = vat + vat2.

              anz = h-umsatz.anzahl. 
              cost = 0. 
              FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
                  AND h-cost.departement = h-artikel.departement 
                  AND h-cost.datum = h-umsatz.datum AND h-cost.flag = 1 NO-LOCK NO-ERROR. 

              IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
              DO:
                  cost = anz * h-cost.betrag. 
                  h-list.cost = h-cost.betrag. 
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

              FIND NEXT h-umsatz WHERE h-umsatz.artnr EQ h-artikel.artnr 
                  AND h-umsatz.departement EQ h-artikel.departement 
                  AND h-umsatz.datum GE from-date
                  AND h-umsatz.datum LE to-date USE-INDEX hrartatz_ix NO-LOCK NO-ERROR.
          END.

          IF h-list.epreis NE 0 THEN 
            h-list.margin = h-list.cost / h-list.epreis * 100. 
      END. /* if do-it*/
    END. 
    RUN create-list(pos). 
    t-anz = 0. 
    t-sales = 0. 
    t-cost = 0. 
  END. 
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
 
  FOR EACH fb-cost-analyst: 
    DELETE fb-cost-analyst. 
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
 
      CREATE fb-cost-analyst. 
      fb-cost-analyst.bezeich = STRING(hoteldpt.num,"99 ") 
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
     
          /* FDL Comment
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
          /*FDL Feb 26, 2024 => Ticket 385FD3*/
          FIND FIRST h-umsatz WHERE h-umsatz.artnr EQ h-artikel.artnr 
              AND h-umsatz.departement EQ h-artikel.departement 
              AND h-umsatz.datum GE from-date
              AND h-umsatz.datum LE to-date USE-INDEX hrartatz_ix NO-LOCK NO-ERROR.
          DO WHILE AVAILABLE h-umsatz:
          
              RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
                  h-umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
              ASSIGN vat = vat + vat2.

              anz = h-umsatz.anzahl. 
              cost = 0. 
              FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
                  AND h-cost.departement = h-artikel.departement 
                  AND h-cost.datum = h-umsatz.datum AND h-cost.flag = 1 NO-LOCK NO-ERROR.      
              IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
              DO:
                  cost = anz * h-cost.betrag. 
                  h-list.cost = h-cost.betrag.
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

    FOR EACH fb-cost-analyst: 
        DELETE fb-cost-analyst. 
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
            /*MTcurr-dept = STRING(hoteldpt.num,"99") + " - " + hoteldpt.depart. 
            DISP curr-dept WITH FRAME frame2.*/
            
            create fb-cost-analyst. 
            fb-cost-analyst.bezeich = STRING(hoteldpt.num,"99 ") 
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
                         h-umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
                   ASSIGN vat = vat + vat2.
                   
                   anz = h-umsatz.anzahl. 
                   cost = 0. 
                   FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
                       AND h-cost.departement = h-artikel.departement 
                       AND h-cost.datum = h-umsatz.datum AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
                   
                   IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN DO:
                       cost = anz * h-cost.betrag. 
                       h-list.cost = h-cost.betrag.
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

  DO: 
    IF mi-subgrp THEN 
    DO: 
      RUN create-list1(pos). 
      RETURN. 
    END. 
    IF detailed AND curr-sort = 1 THEN 
    DO:
      FOR EACH h-list WHERE h-list.dept = hoteldpt.num: 
        IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
        IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
        IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 
      
        CREATE fb-cost-analyst. 
        IF short-flag THEN
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->,>>>,>>>,>>9.99")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->,>>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")          
          .
        END.
        ELSE
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->>,>>>,>>>,>>9")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->>,>>>,>>>,>>9")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->>,>>>,>>>,>>9")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->>,>>>,>>>,>>9") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")
          .
        END.
      END. 
    END.    
    ELSE IF detailed AND curr-sort = 2 THEN 
    DO:
      FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
        BY h-list.anzahl DESC BY h-list.t-sales DESC BY h-list.bezeich: 

        IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
        IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
        IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

        CREATE fb-cost-analyst. 
        IF short-flag THEN
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->,>>>,>>>,>>9.99")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->,>>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")          
          .
        END.
        ELSE
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->>,>>>,>>>,>>9")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->>,>>>,>>>,>>9")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->>,>>>,>>>,>>9")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->>,>>>,>>>,>>9") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")
          .
        END. 
      END. 
    END.    
    ELSE IF detailed AND curr-sort = 3 THEN 
    DO:
      FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
        BY h-list.t-sales DESC BY h-list.anzahl DESC BY h-list.bezeich: 

        IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
        IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
        IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

        CREATE fb-cost-analyst. 
        IF short-flag THEN
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->,>>>,>>>,>>9.99")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->,>>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")          
          .
        END.
        ELSE
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->>,>>>,>>>,>>9")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->>,>>>,>>>,>>9")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->>,>>>,>>>,>>9")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->>,>>>,>>>,>>9") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")
          .
        END.
      END. 
    END.
    ELSE IF NOT detailed AND curr-sort = 1 THEN 
    DO:
      FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
        AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0): 

        IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
        IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
        IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

        CREATE fb-cost-analyst. 
        IF short-flag THEN
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->,>>>,>>>,>>9.99")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->,>>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")          
          .
        END.
        ELSE
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->>,>>>,>>>,>>9")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->>,>>>,>>>,>>9")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->>,>>>,>>>,>>9")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->>,>>>,>>>,>>9") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")
          .
        END.
      END. 
    END.
    ELSE IF NOT detailed AND curr-sort = 2 THEN 
    DO:
      FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
        AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) 
        BY h-list.anzahl DESC BY h-list.t-sales DESC BY h-list.bezeich: 

        IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
        IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
        IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

        CREATE fb-cost-analyst. 
        IF short-flag THEN
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->,>>>,>>>,>>9.99")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->,>>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")          
          .
        END.
        ELSE
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->>,>>>,>>>,>>9")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->>,>>>,>>>,>>9")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->>,>>>,>>>,>>9")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->>,>>>,>>>,>>9") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")
          .
        END.
      END. 
    END.
    ELSE IF NOT detailed AND curr-sort = 3 THEN 
    DO:
      FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
        AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) 
        BY h-list.t-sales DESC BY h-list.anzahl DESC BY h-list.bezeich: 

        IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
        IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
        IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

        CREATE fb-cost-analyst. 
        IF short-flag THEN
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->,>>>,>>>,>>9.99")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->,>>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")          
          .
        END.
        ELSE
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->>,>>>,>>>,>>9")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->>,>>>,>>>,>>9")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->>,>>>,>>>,>>9")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->>,>>>,>>>,>>9") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")
          .
        END. 
      END. 
    END.

    IF pos AND t-sales NE 0 THEN 
    DO: 
      t-margin = 0. 
      IF t-sales NE 0 THEN t-margin = t-cost / t-sales * 100. 

      CREATE fb-cost-analyst.
      IF short-flag THEN
      DO:
        ASSIGN
          fb-cost-analyst.artnr    = STRING("")            
          fb-cost-analyst.bezeich  = STRING("T o t a l")          
          fb-cost-analyst.qty      = STRING(t-anz, ">>,>>9")          
          fb-cost-analyst.proz1    = STRING(100, "->>9.99")           
          fb-cost-analyst.epreis   = STRING("")    
          fb-cost-analyst.cost     = STRING("")      
          fb-cost-analyst.margin   = STRING("")    
          fb-cost-analyst.t-sales  = STRING(t-sales, "->>,>>>,>>>,>>9.99")
          fb-cost-analyst.t-cost   = STRING(t-cost, "->>,>>>,>>>,>>9.99") 
          fb-cost-analyst.t-margin = STRING(t-margin, "->>,>>>,>>9.99") 
          fb-cost-analyst.proz2    = STRING(100, "->>9.99")
        .
      END.
      ELSE
      DO:
        ASSIGN
          fb-cost-analyst.artnr    = STRING("")            
          fb-cost-analyst.bezeich  = STRING("T o t a l")          
          fb-cost-analyst.qty      = STRING(t-anz, ">>,>>9")          
          fb-cost-analyst.proz1    = STRING(100, "->>9.99")           
          fb-cost-analyst.epreis   = STRING("")    
          fb-cost-analyst.cost     = STRING("")      
          fb-cost-analyst.margin   = STRING("")    
          fb-cost-analyst.t-sales  = STRING(t-sales, "->>>,>>>,>>>,>>9")
          fb-cost-analyst.t-cost   = STRING(t-cost, "->>>,>>>,>>>,>>9") 
          fb-cost-analyst.t-margin = STRING(t-margin, "->,>>>,>>9.99") 
          fb-cost-analyst.proz2    = STRING(100, "->>9.99")
        .
      END.

      CREATE fb-cost-analyst. 
    END. 
  END. 
END. 

PROCEDURE create-list1: 
DEFINE INPUT PARAMETER pos AS LOGICAL. 
DEFINE VARIABLE curr-grp AS INTEGER INITIAL 0.

  DO: 
    IF detailed AND curr-sort = 1 THEN 
    DO:
      FOR EACH h-list WHERE h-list.dept = hoteldpt.num BY h-list.zknr BY h-list.bezeich: 
        IF curr-grp NE h-list.zknr THEN 
        DO: 
          RUN create-sub(curr-grp).
          FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept 
            AND wgrpdep.zknr = h-list.zknr NO-LOCK. 
          curr-grp = h-list.zknr. 
      
          CREATE fb-cost-analyst. 
          fb-cost-analyst.flag = 1.         
          fb-cost-analyst.bezeich = STRING(wgrpdep.bezeich, "x(24)"). 
        END. 

        IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
        IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
        IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

        CREATE fb-cost-analyst.         
        IF short-flag THEN
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->,>>>,>>>,>>9.99")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->,>>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")          
          .
        END.
        ELSE
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->>,>>>,>>>,>>9")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->>,>>>,>>>,>>9")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->>,>>>,>>>,>>9")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->>,>>>,>>>,>>9") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")
          .
        END.  
        RUN add-sub.                        
      END. 
    END.
    ELSE IF detailed AND curr-sort = 2 THEN 
    DO:
      FOR EACH h-list WHERE h-list.dept = hoteldpt.num BY h-list.zknr 
        BY h-list.anzahl DESC BY h-list.t-sales DESC BY h-list.bezeich: 
      
        IF curr-grp NE h-list.zknr THEN 
        DO: 
          RUN create-sub(curr-grp).
          FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept 
            AND wgrpdep.zknr = h-list.zknr NO-LOCK. 
          curr-grp = h-list.zknr. 

          CREATE fb-cost-analyst. 
          fb-cost-analyst.flag = 1.           
          fb-cost-analyst.bezeich = STRING(wgrpdep.bezeich, "x(24)"). 
        END. 

        IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
        IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
        IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

        CREATE fb-cost-analyst.         
        IF short-flag THEN
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->,>>>,>>>,>>9.99")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->,>>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")          
          .
        END.
        ELSE
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->>,>>>,>>>,>>9")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->>,>>>,>>>,>>9")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->>,>>>,>>>,>>9")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->>,>>>,>>>,>>9") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")
          .
        END.  
        RUN add-sub.
      END. 
    END.
    ELSE IF detailed AND curr-sort = 3 THEN 
    DO:
      FOR EACH h-list WHERE h-list.dept = hoteldpt.num BY h-list.zknr 
        BY h-list.t-sales DESC BY h-list.anzahl DESC BY h-list.bezeich: 

        IF curr-grp NE h-list.zknr THEN 
        DO: 
          RUN create-sub(curr-grp).
          FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept 
            AND wgrpdep.zknr = h-list.zknr NO-LOCK. 
          curr-grp = h-list.zknr.

          CREATE fb-cost-analyst. 
          fb-cost-analyst.flag = 1.           
          fb-cost-analyst.bezeich = STRING(wgrpdep.bezeich, "x(24)"). 
        END. 

        IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
        IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
        IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

        CREATE fb-cost-analyst.         
        IF short-flag THEN
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->,>>>,>>>,>>9.99")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->,>>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")          
          .
        END.
        ELSE
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->>,>>>,>>>,>>9")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->>,>>>,>>>,>>9")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->>,>>>,>>>,>>9")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->>,>>>,>>>,>>9") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")
          .
        END.
        RUN add-sub.
      END. 
    END.
    ELSE IF NOT detailed AND curr-sort = 1 THEN 
    DO:
      FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
        AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) 
        BY h-list.zknr BY h-list.bezeich: 

        IF curr-grp NE h-list.zknr THEN 
        DO: 
          RUN create-sub(curr-grp).
          FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept 
            AND wgrpdep.zknr = h-list.zknr NO-LOCK. 
          curr-grp = h-list.zknr. 

          CREATE fb-cost-analyst. 
          fb-cost-analyst.flag = 1.           
          fb-cost-analyst.bezeich = STRING(wgrpdep.bezeich, "x(24)"). 
        END. 

        IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
        IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
        IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

        CREATE fb-cost-analyst.         
        IF short-flag THEN
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->,>>>,>>>,>>9.99")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->,>>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")          
          .
        END.
        ELSE
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->>,>>>,>>>,>>9")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->>,>>>,>>>,>>9")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->>,>>>,>>>,>>9")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->>,>>>,>>>,>>9") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")
          .
        END.
        RUN add-sub.
      END.
    END.
    ELSE IF NOT detailed AND curr-sort = 2 THEN 
    DO:
      FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
        AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) BY h-list.zknr 
        BY h-list.anzahl DESC BY h-list.t-sales DESC BY h-list.bezeich: 
      
        IF curr-grp NE h-list.zknr THEN 
        DO: 
          RUN create-sub(curr-grp).
          FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept 
            AND wgrpdep.zknr = h-list.zknr NO-LOCK. 
          curr-grp = h-list.zknr. 

          CREATE fb-cost-analyst. 
          fb-cost-analyst.flag = 1.           
          fb-cost-analyst.bezeich = STRING(wgrpdep.bezeich, "x(24)"). 
        END. 

        IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
        IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
        IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

        CREATE fb-cost-analyst.         
        IF short-flag THEN
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->,>>>,>>>,>>9.99")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->,>>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")          
          .
        END.
        ELSE
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->>,>>>,>>>,>>9")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->>,>>>,>>>,>>9")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->>,>>>,>>>,>>9")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->>,>>>,>>>,>>9") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")
          .
        END.
        RUN add-sub.
      END. 
    END.
    ELSE IF NOT detailed AND curr-sort = 3 THEN 
    DO:
      FOR EACH h-list WHERE h-list.dept = hoteldpt.num 
        AND (h-list.t-sales NE 0 OR h-list.anzahl NE 0) BY h-list.zknr 
        BY h-list.t-sales DESC BY h-list.anzahl DESC BY h-list.bezeich: 

        IF curr-grp NE h-list.zknr THEN 
        DO: 
          RUN create-sub(curr-grp).
          FIND FIRST wgrpdep WHERE wgrpdep.departement = h-list.dept 
            AND wgrpdep.zknr = h-list.zknr NO-LOCK. 
          curr-grp = h-list.zknr. 

          CREATE fb-cost-analyst. 
          fb-cost-analyst.flag = 1.           
          fb-cost-analyst.bezeich = STRING(wgrpdep.bezeich, "x(24)"). 
        END. 

        IF t-anz NE 0 THEN h-list.proz1 = h-list.anzahl / t-anz * 100. 
        IF h-list.t-sales NE 0 THEN h-list.t-margin = h-list.t-cost / h-list.t-sales * 100. 
        IF t-sales NE 0 THEN h-list.proz2 = h-list.t-sales / t-sales * 100. 

        CREATE fb-cost-analyst.         
        IF short-flag THEN
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->,>>>,>>>,>>9.99")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->,>>>,>>>,>>9.99")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->,>>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->,>>>,>>>,>>9.99")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->,>>>,>>>,>>9.99") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->,>>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")          
          .
        END.
        ELSE
        DO:
          ASSIGN
            fb-cost-analyst.artnr    = STRING(h-list.artnr, ">>>>>>>>9")            
            fb-cost-analyst.bezeich  = h-list.bezeich         
            fb-cost-analyst.qty      = STRING(h-list.anzahl, "->>>>9")          
            fb-cost-analyst.proz1    = STRING(h-list.proz1, "->>9.99")           
            fb-cost-analyst.epreis   = STRING(h-list.epreis, "->>,>>>,>>>,>>9")    
            fb-cost-analyst.cost     = STRING(h-list.cost, "->>,>>>,>>>,>>9")      
            fb-cost-analyst.margin   = STRING(h-list.margin, "->>>,>>9.99")    
            fb-cost-analyst.t-sales  = STRING(h-list.t-sales, "->>,>>>,>>>,>>9")
            fb-cost-analyst.t-cost   = STRING(h-list.t-cost, "->>,>>>,>>>,>>9") 
            fb-cost-analyst.t-margin = STRING(h-list.t-margin, "->>>,>>9.99") 
            fb-cost-analyst.proz2    = STRING(h-list.proz2, "->>9.99")
          .
        END. 
        RUN add-sub.
      END. 
    END.

    RUN create-sub(curr-grp).
    IF pos AND t-sales NE 0 THEN 
    DO:       
      t-margin = 0. 
      IF t-sales NE 0 THEN t-margin = t-cost / t-sales * 100. 

      CREATE fb-cost-analyst. 
      IF short-flag THEN
      DO:
        ASSIGN
          fb-cost-analyst.artnr    = STRING("")            
          fb-cost-analyst.bezeich  = STRING("T o t a l")          
          fb-cost-analyst.qty      = STRING(t-anz, ">>,>>9")          
          fb-cost-analyst.proz1    = STRING(100, "->>9.99")           
          fb-cost-analyst.epreis   = STRING("")    
          fb-cost-analyst.cost     = STRING("")      
          fb-cost-analyst.margin   = STRING("")    
          fb-cost-analyst.t-sales  = STRING(t-sales, "->>,>>>,>>>,>>9.99")
          fb-cost-analyst.t-cost   = STRING(t-cost, "->>,>>>,>>>,>>9.99") 
          fb-cost-analyst.t-margin = STRING(t-margin, "->>,>>>,>>9.99") 
          fb-cost-analyst.proz2    = STRING(100, "->>9.99")
        .
      END.
      ELSE
      DO:
        ASSIGN
          fb-cost-analyst.artnr    = STRING("")            
          fb-cost-analyst.bezeich  = STRING("T o t a l")          
          fb-cost-analyst.qty      = STRING(t-anz, ">>,>>9")          
          fb-cost-analyst.proz1    = STRING(100, "->>9.99")           
          fb-cost-analyst.epreis   = STRING("")    
          fb-cost-analyst.cost     = STRING("")      
          fb-cost-analyst.margin   = STRING("")    
          fb-cost-analyst.t-sales  = STRING(t-sales, "->,>>>,>>>,>>9")
          fb-cost-analyst.t-cost   = STRING(t-cost, "->,>>>,>>>,>>9") 
          fb-cost-analyst.t-margin = STRING(t-margin, "->,>>>,>>9.99") 
          fb-cost-analyst.proz2    = STRING(100, "->>9.99")
        .
      END.
      
      CREATE fb-cost-analyst. 
    END. 
  END. 
END. 

PROCEDURE create-sub:
DEFINE INPUT PARAMETER curr-grp AS INTEGER.
    IF curr-grp NE 0 THEN
    DO:        
        IF st-sales NE 0 THEN st-margin = st-cost / st-sales * 100.

        IF short-flag THEN
        DO:
            CREATE fb-cost-analyst.
            ASSIGN
                fb-cost-analyst.flag     = 2                        
                fb-cost-analyst.artnr    = STRING("")            
                fb-cost-analyst.bezeich  = STRING("S u b T o t a l")          
                fb-cost-analyst.qty      = STRING(s-anzahl, "->>>>9")          
                fb-cost-analyst.proz1    = STRING(s-proz1, "->>9.99")           
                fb-cost-analyst.epreis   = STRING("")    
                fb-cost-analyst.cost     = STRING("")      
                fb-cost-analyst.margin   = STRING("")    
                fb-cost-analyst.t-sales  = STRING(st-sales, "->,>>>,>>>,>>9.99")
                fb-cost-analyst.t-cost   = STRING(st-cost, "->,>>>,>>>,>>9.99") 
                fb-cost-analyst.t-margin = STRING(st-margin, "->,>>>,>>9.99") 
                fb-cost-analyst.proz2    = STRING(st-proz2, "->>9.9")
            .
        END.
        ELSE
        DO:
            CREATE fb-cost-analyst.
            ASSIGN
                fb-cost-analyst.flag     = 2                        
                fb-cost-analyst.artnr    = STRING("")            
                fb-cost-analyst.bezeich  = STRING("S u b T o t a l")          
                fb-cost-analyst.qty      = STRING(s-anzahl, "->>>>9")          
                fb-cost-analyst.proz1    = STRING(s-proz1, "->>9.99")           
                fb-cost-analyst.epreis   = STRING("")    
                fb-cost-analyst.cost     = STRING("")      
                fb-cost-analyst.margin   = STRING("")    
                fb-cost-analyst.t-sales  = STRING(st-sales, "->,>>>,>>>,>>9")
                fb-cost-analyst.t-cost   = STRING(st-cost, "->,>>>,>>>,>>9") 
                fb-cost-analyst.t-margin = STRING(st-margin, "->>>,>>9.99") 
                fb-cost-analyst.proz2    = STRING(st-proz2, "->>9.9")
            .
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


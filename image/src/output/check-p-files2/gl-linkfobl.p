
DEFINE TEMP-TABLE g-list 
  FIELD  flag   AS INTEGER 
  FIELD  datum  AS DATE 
  FIELD  artnr  AS INTEGER 
  FIELD  dept   AS INTEGER 
  FIELD  jnr        LIKE gl-journal.jnr 
  FIELD  fibukonto  LIKE gl-journal.fibukonto 
  FIELD  debit      LIKE gl-journal.debit   FORMAT ">,>>>,>>>,>>9.99"
  FIELD  credit     LIKE gl-journal.credit FORMAT ">,>>>,>>>,>>9.99"
  FIELD  bemerk     AS CHAR FORMAT "x(32)" 
  FIELD  userinit   LIKE gl-journal.userinit 
  FIELD  sysdate    LIKE gl-journal.sysdate INITIAL today 
  FIELD  zeit       LIKE gl-journal.zeit 
  FIELD  chginit    LIKE gl-journal.chginit 
  FIELD  chgdate    LIKE gl-journal.chgdate INITIAL ? 
  FIELD  duplicate  AS LOGICAL INITIAL YES
  FIELD  acct-fibukonto LIKE gl-acct.fibukonto
  FIELD  bezeich        LIKE gl-acct.bezeich. 

DEFINE TEMP-TABLE buf-g-list LIKE g-list.

DEFINE TEMP-TABLE trans-dept
    FIELD nr AS INTEGER.

DEF INPUT PARAMETER TABLE       FOR trans-dept.
DEF INPUT PARAMETER from-date   AS DATE NO-UNDO.
DEF INPUT PARAMETER to-date     AS DATE NO-UNDO.
DEF INPUT PARAMETER user-init   AS CHAR NO-UNDO.
DEF INPUT PARAMETER refno       AS CHAR NO-UNDO.

DEF INPUT-OUTPUT PARAMETER curr-anz AS INTEGER NO-UNDO.

DEF OUTPUT PARAMETER debits  LIKE gl-acct.actual[1].
DEF OUTPUT PARAMETER credits LIKE gl-acct.actual[1].
DEF OUTPUT PARAMETER acct-error AS INTEGER NO-UNDO INIT 0.
DEF OUTPUT PARAMETER remains    AS DECIMAL NO-UNDO.

DEF OUTPUT PARAMETER art-dpt     AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER art-artnr   AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER art-bezeich AS CHAR    NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR buf-g-list.

DEFINE VARIABLE curr-date       AS DATE. 
DEFINE VARIABLE artart-list     AS INTEGER EXTENT 9 INITIAL [1,9,3,9,9,2,2,4,0]. 
DEFINE VARIABLE price-decimal   AS INTEGER.
DEFINE VARIABLE credit-betrag   AS DECIMAL. 
DEFINE VARIABLE debit-betrag    AS DECIMAL. 
DEFINE VARIABLE serv-acctno     AS CHAR. 
DEFINE VARIABLE vat-acctno      AS CHAR.
DEFINE VARIABLE fibukonto       AS CHAR.
/* Dzikri 15D5B7 & 3337DC - repair remark 
DEFINE VARIABLE lastdate        AS INTEGER. */
DEFINE VARIABLE lastdate        AS DATE.

DEFINE BUFFER gl-acct1          FOR gl-acct. 

FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno = refno 
  AND gl-jouhdr.jtype = 1 NO-LOCK NO-ERROR. 
IF AVAILABLE gl-jouhdr THEN 
DO: 
  acct-error = 1.
  RETURN.
END.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 

/********* default Account Number FOR SERVICE *******/ 
FIND FIRST htparam WHERE paramnr = 133 NO-LOCK. 
FIND FIRST artikel WHERE artikel.artnr = finteger 
  AND artikel.departement = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE artikel THEN serv-acctno = artikel.fibukonto. 

/********* default Account Number FOR VAT *******/ 
FIND FIRST htparam WHERE paramnr = 132 NO-LOCK. 
FIND FIRST artikel WHERE artikel.artnr = finteger 
  AND artikel.departement = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE artikel THEN vat-acctno = artikel.fibukonto. 

RUN check-dept.
RUN step-two. 


PROCEDURE step-two: 
DEFINE buffer art1       FOR artikel. 
DEFINE buffer gl-acc1    FOR gl-acct. 
DEFINE VARIABLE sales    AS DECIMAL INITIAL 0. 

DEFINE VARIABLE service  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tax      AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tax2     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE serv     AS DECIMAL. 

DEFINE VARIABLE vat      AS DECIMAL. 
DEFINE VARIABLE vat2     AS DECIMAL. 
DEFINE VARIABLE fact     AS DECIMAL. 

DEFINE VARIABLE serv-vat AS LOGICAL. 
DEFINE VARIABLE payment  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gledger  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE fibu1    AS CHAR. 
DEFINE VARIABLE vat-fibu  AS CHAR. 
DEFINE VARIABLE vat2-fibu AS CHAR. 
DEFINE VARIABLE serv-fibu AS CHAR. 
DEFINE VARIABLE wert      AS DECIMAL. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  ASSIGN
      debits     = 0
      credits    = 0
  .
  DO curr-date = from-date TO to-date: 
    gledger = 0. 
    FOR EACH hoteldpt NO-LOCK, 
        FIRST trans-dept WHERE trans-dept.nr = hoteldpt.num BY hoteldpt.num: 
      FOR EACH artikel WHERE artikel.departement = hoteldpt.num 
        AND (artart = 0 OR artart = 5 OR artart = 8 
          OR artart = 2 OR artart = 6 OR artart = 7) 
        NO-LOCK BY artart-list[artikel.artart + 1] BY artikel.artnr: 
         
        FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr
          AND umsatz.departement = artikel.departement
          AND umsatz.datum = curr-date NO-LOCK NO-ERROR.
        IF AVAILABLE umsatz THEN
        DO:
          FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = artikel.fibukonto 
            NO-LOCK NO-ERROR.
          IF NOT AVAILABLE gl-acc1 THEN
          DO:
            art-dpt = artikel.departement.
            art-artnr = artikel.artnr.
            art-bezeich = artikel.bezeich.
            acct-error = 2.
            FOR EACH g-list:
              DELETE g-list.
            END.
            RETURN.
          END.
          ELSE 
          DO:
              fibukonto = gl-acc1.fibukonto. 
              fibu1 = fibukonto. 
          END.

          ASSIGN
            serv      = 0 
            vat       = 0
            serv-fibu = ""
            vat-fibu  = ""
          . 
          
/*
          RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, 
                                      artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
          fact = 1.00 + serv + vat. 
*/
/* SY OCT 13 2017: Not needed
          RUN calc-servtaxesbl.p (1, umsatz.artnr, umsatz.departement,
             umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2,
             OUTPUT fact).
*/
          IF artikel.service-code NE 0 THEN 
          DO: 
              FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code NO-LOCK. 
              IF AVAILABLE htparam THEN serv-fibu = ENTRY(1, htparam.fchar, CHR(2)). 
          END. 
          IF artikel.mwst-code NE 0 THEN 
          DO: 
              FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code NO-LOCK. 
              IF AVAILABLE htparam THEN vat-fibu = ENTRY(1, htparam.fchar, CHR(2)). 
          END.            
          IF artikel.prov-code NE 0 THEN 
          DO: 
              FIND FIRST htparam WHERE htparam.paramnr = artikel.prov-code NO-LOCK. 
              IF AVAILABLE htparam THEN 
              DO:    
                  vat2-fibu = ENTRY(1, htparam.fchar, CHR(2)). 
                  IF TRIM(vat2-fibu) = "" THEN
                  DO:
                      acct-error = 3.
                      RETURN.
                  END.
              END.
          END.            
        END.
/* 
        IF artikel.artart = 6 AND artikel.departement = 0 
          AND artikel.pricetab THEN 
        FOR EACH billjournal WHERE billjournal.artnr = artikel.artnr 
          AND billjournal.departement = 0 
          AND billjournal.bill-datum = curr-date 
          AND billjournal.waehrungsnr GT 0 NO-LOCK: 
          RUN money-exchg(billjournal.fremdwaehrng, billjournal.betrag). 
        END. 
*/ 
        FOR EACH umsatz WHERE umsatz.datum EQ curr-date 
          AND umsatz.artnr = artikel.artnr 
          AND umsatz.departement = artikel.departement 
          AND umsatz.betrag NE 0 NO-LOCK: 

/*
          serv = 0. 
          vat = 0. 
          RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, 
                                      artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
          fact = 1.00 + serv + vat. 
*/
          RUN calc-servtaxesbl.p (1, umsatz.artnr, umsatz.departement,
              umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2,
              OUTPUT fact).

          IF NOT AVAILABLE gl-acc1 THEN LEAVE.

          gledger = gledger + umsatz.betrag. 
 
          IF artikel.artart = 0 OR artikel.artart = 5 
            OR artikel.artart = 8 THEN 
          DO: 
            ASSIGN
                wert    = umsatz.betrag / fact
                /*
                service = wert * serv
                tax     = wert * vat
                tax2    = wert * vat2
                */
                
                /*Gerald di comment dulu rounding karna selisih dengan DRR A5D80A*/                
                service = ROUND(wert * serv, price-decimal) 
                tax     = ROUND(wert * vat,  price-decimal)         /*william open gerald's comment - 6856F4 - 07/06/23*/
                tax2    = ROUND(wert * vat2, price-decimal)
                  
                sales   = umsatz.betrag - service - tax - tax2                
            . 
 
            IF service GT 0 THEN 
            DO:
              credit-betrag = service. 
              debit-betrag = 0. 
              IF serv-fibu NE "" THEN fibukonto = serv-fibu. 
              ELSE fibukonto = serv-acctno. 
              FIND FIRST g-list WHERE g-list.fibukonto = fibukonto 
                AND g-list.datum = curr-date /* AND g-list.credit NE 0 */ 
                NO-ERROR. 
              IF NOT AVAILABLE g-list THEN 
                RUN add-list(-2, YES, "", 0, 0). 
              ELSE RUN add-list(-2, NO, "", 0, 0). 
            END. 
            ELSE IF service LT 0 THEN 
            DO: 
              debit-betrag = - service. 
              credit-betrag = 0. 
              IF serv-fibu NE "" THEN fibukonto = serv-fibu. 
              ELSE fibukonto = serv-acctno. 
              FIND FIRST g-list WHERE g-list.fibukonto = fibukonto 
                AND g-list.datum = curr-date /* AND g-list.debit NE 0 */ 
                NO-ERROR. 
              IF NOT AVAILABLE g-list THEN 
                RUN add-list(-2, YES, "", 0, 0). 
              ELSE RUN add-list(-2, NO, "", 0, 0). 
            END. 
 
            IF tax GT 0 THEN 
            DO: 
              credit-betrag = tax. 
              debit-betrag = 0. 
              IF vat-fibu NE "" THEN fibukonto = vat-fibu. 
              ELSE fibukonto = vat-acctno. 
              FIND FIRST g-list WHERE g-list.fibukonto = fibukonto 
                AND g-list.datum = curr-date /* AND g-list.credit NE 0 */ 
                NO-ERROR. 
              IF NOT AVAILABLE g-list THEN 
                RUN add-list(-1, YES, "", 0, 0). 
              ELSE RUN add-list(-1, NO, "", 0, 0). 
            END. 
            ELSE IF tax LT 0 THEN 
            DO: 
              debit-betrag = - tax. 
              credit-betrag = 0. 
              IF vat-fibu NE "" THEN fibukonto = vat-fibu. 
              ELSE fibukonto = vat-acctno. 
              FIND FIRST g-list WHERE g-list.fibukonto = fibukonto 
                AND g-list.datum = curr-date /* AND g-list.debit NE 0 */ 
                NO-ERROR. 
              IF NOT AVAILABLE g-list THEN 
                RUN add-list(-1, YES, "", 0, 0). 
              ELSE RUN add-list(-1, NO, "", 0, 0). 
            END. 
 
            IF tax2 GT 0 THEN 
            DO: 
              ASSIGN
                  credit-betrag = tax2 
                  debit-betrag  = 0 
                  fibukonto     = vat2-fibu
              . 
              FIND FIRST g-list WHERE g-list.fibukonto = fibukonto 
                AND g-list.datum = curr-date /* AND g-list.credit NE 0 */ 
                NO-ERROR. 
              IF NOT AVAILABLE g-list THEN 
                RUN add-list(-1, YES, "", 0, 0). 
              ELSE RUN add-list(-1, NO, "", 0, 0). 
            END. 
            ELSE IF tax2 LT 0 THEN 
            DO: 
              ASSIGN
                  debit-betrag  = - tax2
                  credit-betrag = 0 
                  fibukonto     = vat-fibu
              . 
              FIND FIRST g-list WHERE g-list.fibukonto = fibukonto 
                AND g-list.datum = curr-date /* AND g-list.debit NE 0 */ 
                NO-ERROR. 
              IF NOT AVAILABLE g-list THEN 
                RUN add-list(-1, YES, "", 0, 0). 
              ELSE RUN add-list(-1, NO, "", 0, 0). 
            END. 

            IF sales GT 0 THEN 
            DO: 
              credit-betrag = sales. 
              debit-betrag = 0. 
              fibukonto = gl-acc1.fibukonto. 
              FIND FIRST g-list WHERE g-list.artnr = artikel.artnr 
                AND g-list.dept = artikel.departement 
                AND g-list.fibukonto = fibukonto 
                AND g-list.datum = curr-date /* AND g-list.credit NE 0 */ 
                NO-ERROR. 
 
              IF NOT AVAILABLE g-list THEN RUN add-list(0, YES, 
                (STRING(hoteldpt.num) + " - " + artikel.bezeich 
                 + ";&&;" + STRING(artikel.departement) + ";" 
                 + STRING(artikel.artnr)), artikel.artnr, artikel.departement). 
 
              ELSE RUN add-list(0, NO, 
                (STRING(hoteldpt.num) + " - " + artikel.bezeich), 
                 artikel.artnr, artikel.departement). 
            END. 
            ELSE IF sales LT 0 THEN 
            DO: 
              fibukonto = gl-acc1.fibukonto. 
              debit-betrag = - sales. 
              credit-betrag = 0. 
              FIND FIRST g-list WHERE g-list.artnr = artikel.artnr 
                AND g-list.dept = artikel.departement 
                AND g-list.fibukonto = fibukonto 
                AND g-list.datum = curr-date /* AND g-list.debit NE 0 */ 
                NO-ERROR. 
 
              IF NOT AVAILABLE g-list THEN RUN add-list(0, YES, 
               (STRING(hoteldpt.num) + " - " + artikel.bezeich 
                + ";&&;" + STRING(artikel.departement) + ";" 
                + STRING(artikel.artnr)), artikel.artnr, artikel.departement). 
 
              ELSE RUN add-list(0, NO, 
               (STRING(hoteldpt.num) + " - " + artikel.bezeich 
                + ";&&;" + STRING(artikel.departement) + ";" 
                + STRING(artikel.artnr)), artikel.artnr, artikel.departement). 
            END. 
          END. 
          ELSE /* payment */ 
          DO: 
            IF umsatz.betrag LE 0 THEN 
            DO: 
              fibukonto = gl-acc1.fibukonto. 
              debit-betrag = - umsatz.betrag. 
              credit-betrag = 0. 
              FIND FIRST g-list WHERE g-list.artnr = artikel.artnr 
                AND g-list.dept = artikel.departement 
                AND g-list.fibukonto = fibukonto 
                AND g-list.datum = curr-date /* AND g-list.debit NE 0 */ 
                AND g-list.flag NE 9 NO-ERROR. 
 
              IF NOT AVAILABLE g-list THEN RUN add-list(1, YES, 
                (STRING(hoteldpt.num) + " - " + artikel.bezeich 
                 + ";&&;" + STRING(artikel.departement) + ";" 
                 + STRING(artikel.artnr)), artikel.artnr, artikel.departement). 
 
              ELSE RUN add-list(1, NO, 
               (STRING(hoteldpt.num) + " - " + artikel.bezeich 
                + ";&&;" + STRING(artikel.departement) + ";" 
                + STRING(artikel.artnr)), artikel.artnr, artikel.departement). 
            END. 
            ELSE IF umsatz.betrag GT 0 THEN 
            DO: 
              fibukonto = gl-acc1.fibukonto. 
              credit-betrag = umsatz.betrag. 
              debit-betrag = 0. 
              FIND FIRST g-list WHERE g-list.artnr = artikel.artnr 
                AND g-list.dept = artikel.departement 
                AND g-list.fibukonto = fibukonto 
                AND g-list.datum = curr-date /* AND g-list.credit NE 0 */ 
                AND g-list.flag NE 9 NO-ERROR. 
 
              IF NOT AVAILABLE g-list THEN RUN add-list(1, YES, 
               (STRING(hoteldpt.num) + " - " + artikel.bezeich 
                + ";&&;" + STRING(artikel.departement) + ";" 
                + STRING(artikel.artnr)), artikel.artnr, artikel.departement). 
 
              ELSE RUN add-list(1, NO, 
                (STRING(hoteldpt.num) + " - " + artikel.bezeich 
                 + ";&&;" + STRING(artikel.departement) + ";" 
                 + STRING(artikel.artnr)), artikel.artnr, artikel.departement). 
            END. 
          END. 
        END. 
      END. 
    END. 
 
    FIND FIRST htparam WHERE paramnr = 998 NO-LOCK. 
    fibukonto = htparam.fchar. 
    IF gledger GT 0 THEN 
    DO: 
      debit-betrag = gledger. 
      credit-betrag = 0. 
      FIND FIRST g-list WHERE g-list.fibukonto = fibukonto 
        AND g-list.datum = curr-date /* AND g-list.debit NE 0 */ NO-ERROR. 
      IF NOT AVAILABLE g-list THEN RUN add-list(2, YES, "",0,0). 
      ELSE RUN add-list(2, NO, "",0,0). 
    END. 
    ELSE IF gledger LT 0 THEN 
    DO: 
      credit-betrag = - gledger. 
      debit-betrag = 0. 
      FIND FIRST g-list WHERE g-list.fibukonto = fibukonto 
        AND g-list.datum = curr-date /* AND g-list.credit NE 0 */ NO-ERROR. 
      IF NOT AVAILABLE g-list THEN RUN add-list(2, YES, "",0,0). 
      ELSE RUN add-list(2, NO, "",0,0). 
    END. 
  END. 
 
  IF acct-error GT 0 THEN
  DO:
    FOR EACH g-list:
      DELETE g-list.
    END.
    RETURN.
  END.

  RUN modify-glist. 
 

  FOR EACH g-list NO-LOCK, 
    FIRST gl-acct1 WHERE gl-acct1.fibukonto = g-list.fibukonto NO-LOCK 
      BY g-list.flag BY g-list.sysdate BY g-list.zeit:
      /* Dzikri 15D5B7 & 3337DC - repair remark 
      lastdate = DAY(curr-date) - 1. */
      lastdate = curr-date - 1.
      CREATE buf-g-list.
      BUFFER-COPY g-list TO buf-g-list.
      buf-g-list.acct-fibukonto = gl-acct1.fibukonto.
      buf-g-list.bezeich = gl-acct1.bezeich.
      /*gerald 180520*/
      IF buf-g-list.bemerk = "" AND buf-g-list.acct-fibukonto = gl-acct1.fibukonto THEN
         /* Dzikri 15D5B7 & 3337DC - repair remark 
         buf-g-list.bemerk = gl-acct1.bezeich + " " + STRING(DATE(MONTH(curr-date), lastdate, YEAR(curr-date))).  /*william - 0497D7 add current date*/   */
         buf-g-list.bemerk = gl-acct1.bezeich + " " + STRING(lastdate).   
  END.
END. 
 
PROCEDURE modify-glist: 
    FOR EACH g-list: 
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = g-list.fibukonto NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
            IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN  /* sales OR passive */ 
            DO: 
                IF g-list.debit NE 0 AND g-list.credit GT g-list.debit THEN 
                DO: 
                    /*Gerald rounding karna selisih dengan DRR A5D80A*/
                    g-list.credit = ROUND(g-list.credit - g-list.debit, price-decimal).
                    credits = credits - g-list.debit. 
                    debits = debits - g-list.debit. 
                    g-list.debit = 0.
                END. 
            END. 
            ELSE 
            DO: 
                IF g-list.credit NE 0 AND g-list.debit GT g-list.credit THEN 
                DO: 
                    /*Gerald rounding karna selisih dengan DRR A5D80A*/
                    g-list.debit = ROUND(g-list.debit - g-list.credit, price-decimal). 
                    credits = credits - g-list.credit. 
                    debits = debits - g-list.credit. 
                    g-list.credit = 0.
                END. 
            END.
        END.
    END. 
END. 

PROCEDURE add-list: 
DEFINE INPUT PARAMETER flag AS INTEGER. 
DEFINE INPUT PARAMETER create-it AS LOGICAL. 
DEFINE INPUT PARAMETER bemerk AS CHAR. 
DEFINE INPUT PARAMETER artnr AS INTEGER. 
DEFINE INPUT PARAMETER dept AS INTEGER. 
  curr-anz = curr-anz + 1. 
  IF create-it THEN 
  DO: 
    create g-list. 
    g-list.flag = flag. 
    g-list.fibukonto = fibukonto. 
    g-list.bemerk = "". 
    g-list.datum = curr-date. 
    g-list.artnr = artnr. 
    g-list.dept = dept. 
  END. 
  /*g-list.debit = g-list.debit + debit-betrag. 
  g-list.credit = g-list.credit + credit-betrag.*/
  /*Gerald rounding karna selisih dengan DRR A5D80A*/
  g-list.debit = ROUND(g-list.debit + debit-betrag, price-decimal). 
  g-list.credit = ROUND(g-list.credit + credit-betrag, price-decimal).
  g-list.userinit = user-init. 
  g-list.zeit = time + curr-anz. 
  g-list.duplicate = NO. 
  g-list.bemerk = bemerk. 
  credits = credits + credit-betrag. 
  debits = debits + debit-betrag. 
  remains = debits - credits. 
  debit-betrag = 0. 
  credit-betrag = 0.
END. 


PROCEDURE check-dept:
DEF VAR i AS INTEGER NO-UNDO.

    FOR EACH trans-dept:
        DELETE trans-dept.
    END.

    FIND FIRST htparam WHERE paramnr = 793 NO-LOCK.
    IF htparam.fchar NE "" THEN
    DO:
        DO i = 1 TO NUM-ENTRIES(htparam.fchar, ","):
            FIND FIRST trans-dept WHERE trans-dept.nr = INTEGER(ENTRY(i, htparam.fchar, ",")) 
                NO-ERROR.
            IF NOT AVAILABLE trans-dept THEN
            DO:
                CREATE trans-dept.
                ASSIGN nr = INTEGER(ENTRY(i, htparam.fchar, ",")) .
            END.
        END.
    END.
    ELSE
    DO:
        FOR EACH hoteldpt NO-LOCK:
            CREATE trans-dept.
            ASSIGN nr = hoteldpt.num.
        END.
    END.
END.

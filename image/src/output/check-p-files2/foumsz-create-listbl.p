
DEFINE TEMP-TABLE umsz-list
    FIELD artnr      AS CHARACTER FORMAT "x(4)"
    FIELD bezeich    AS CHARACTER FORMAT "x(24)"
    FIELD day-nett   AS CHARACTER FORMAT "x(19)"
    FIELD day-serv   AS CHARACTER FORMAT "x(19)"
    FIELD day-tax    AS CHARACTER FORMAT "x(19)"
    FIELD day-gros   AS CHARACTER FORMAT "x(19)"
    FIELD day-persen AS CHARACTER FORMAT "x(9)" 
    FIELD mtd-nett   AS CHARACTER FORMAT "x(19)"
    FIELD mtd-serv   AS CHARACTER FORMAT "x(19)"
    FIELD mtd-tax    AS CHARACTER FORMAT "x(19)"
    FIELD mtd-gros   AS CHARACTER FORMAT "x(19)"
    FIELD mtd-persen AS CHARACTER FORMAT "x(9)" 
    FIELD ytd-nett   AS CHARACTER FORMAT "x(19)"     
    FIELD ytd-serv   AS CHARACTER FORMAT "x(19)"    
    FIELD ytd-tax    AS CHARACTER FORMAT "x(19)"     
    FIELD ytd-gros   AS CHARACTER FORMAT "x(19)"    
    FIELD ytd-persen AS CHARACTER FORMAT "x(9)"     
    FIELD month-bud  AS CHARACTER FORMAT "x(21)"  
    FIELD dqty AS CHAR /*FD*/
    FIELD mqty AS CHAR /*FD*/
    FIELD yqty AS CHAR. /*FD*/
    .

DEFINE TEMP-TABLE cl-list 
  FIELD flag       AS CHAR FORMAT "x(2)" INITIAL "" 
  FIELD vat-proz   AS DECIMAL FORMAT ">>9.99"
  FIELD artnr      AS INTEGER FORMAT ">>>9" INITIAL 0 
  FIELD dept       AS INTEGER 
  FIELD bezeich    AS CHAR FORMAT "x(24)" 
  FIELD dnet       AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD proz1      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD dserv      AS DECIMAL FORMAT "->,>>>,>>9.99" INITIAL 0 
  FIELD dtax       AS DECIMAL FORMAT "->,>>>,>>9.99" INITIAL 0 
  FIELD dgros      AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD proz2      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD mnet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD mserv      AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD mtax       AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD mgros      AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz4      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD ynet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz6      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD yserv      AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD ytax       AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD ygros      AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0
  FIELD mbudget    AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" INITIAL 0
  FIELD dqty       AS INTEGER
  FIELD mqty       AS INTEGER
  FIELD yqty       AS INTEGER. 

DEFINE TEMP-TABLE vat-list
  FIELD dptnr      AS INTEGER
  FIELD vat        AS DECIMAL FORMAT ">>9.99"
  FIELD dtax       AS DECIMAL FORMAT "->,>>>,>>9.99"
  FIELD dnet       AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD dgros      AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD dserv      AS DECIMAL FORMAT "->,>>>,>>9.99" INITIAL 0 
  FIELD mtax       AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD mnet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD mserv      AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD mgros      AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD ytax       AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD yserv      AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD ynet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD ygros      AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0. 
  .
 
DEFINE TEMP-TABLE gvat-list
    FIELD dptnr      AS INTEGER
    FIELD vat        AS DECIMAL FORMAT ">>9.99"
    FIELD dtax       AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD dnet       AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
    FIELD dgros      AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
    FIELD dserv      AS DECIMAL FORMAT "->,>>>,>>9.99" INITIAL 0 
    FIELD mtax       AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
    FIELD mnet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
    FIELD mserv      AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
    FIELD mgros      AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
    FIELD ytax       AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
    FIELD yserv      AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
    FIELD ynet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
    FIELD ygros      AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0. 

DEFINE TEMP-TABLE not-avail-umstaz
    FIELD artnr      AS INTEGER 
    FIELD depart     AS INTEGER
    FIELD bezeich    AS CHAR.

DEFINE INPUT  PARAMETER from-dept  AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER to-dept    AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER first-date AS DATE    NO-UNDO.
DEFINE INPUT  PARAMETER from-date  AS DATE    NO-UNDO.
DEFINE INPUT  PARAMETER to-date    AS DATE    NO-UNDO.
DEFINE INPUT  PARAMETER totVatFlag AS LOGICAL NO-UNDO.

DEFINE OUTPUT PARAMETER TABLE FOR umsz-list.
/*
DEFINE VARIABLE from-dept  AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE to-dept    AS INTEGER NO-UNDO INITIAL 20.
DEFINE VARIABLE first-date AS DATE    NO-UNDO INITIAL 01/01/19.
DEFINE VARIABLE from-date  AS DATE    NO-UNDO INITIAL 01/01/19.
DEFINE VARIABLE to-date    AS DATE    NO-UNDO INITIAL 01/14/19.
DEFINE VARIABLE totVatFlag AS LOGICAL NO-UNDO INITIAL NO.
*/

DEF VARIABLE vhp-limited        AS LOGICAL INITIAL NO   NO-UNDO.
DEF VARIABLE vat-str            AS CHAR    INITIAL "" NO-UNDO. 
DEF VARIABLE vat-artnr          AS INTEGER INITIAL 0  NO-UNDO. 
DEF VARIABLE serv-artnr         AS INTEGER INITIAL 0  NO-UNDO. 
DEF VARIABLE price-decimal      AS INTEGER            NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 132 NO-LOCK. 
ASSIGN
  vat-artnr = htparam.finteger
  vat-str   = htparam.fchar.
IF vat-str NE "" THEN
DO:
  IF SUBSTR(vat-str,1,1) NE ";" THEN vat-str = ";" + vat-str.
  IF SUBSTR(vat-str,LENGTH(vat-str),1) NE ";" THEN vat-str = vat-str + ";".
END.

RUN htpint.p (133, OUTPUT serv-artnr).
RUN htpint.p (491, OUTPUT price-decimal).

RUN create-umsatz.

PROCEDURE create-umsatz:
  DEFINE VARIABLE dnet      AS DECIMAL. 
  DEFINE VARIABLE dserv     AS DECIMAL. 
  DEFINE VARIABLE dtax      AS DECIMAL. 
  DEFINE VARIABLE dgros     AS DECIMAL. 
  DEFINE VARIABLE dqty      AS INTEGER.
 
  DEFINE VARIABLE mnet      AS DECIMAL. 
  DEFINE VARIABLE mserv     AS DECIMAL. 
  DEFINE VARIABLE mtax      AS DECIMAL. 
  DEFINE VARIABLE mgros     AS DECIMAL. 
  DEFINE VARIABLE mqty      AS INTEGER.

  DEFINE VARIABLE ynet      AS DECIMAL. 
  DEFINE VARIABLE yserv     AS DECIMAL. 
  DEFINE VARIABLE ytax      AS DECIMAL. 
  DEFINE VARIABLE ygros     AS DECIMAL. 
  DEFINE VARIABLE yqty      AS INTEGER.

  DEFINE VARIABLE t-dnet    AS DECIMAL. 
  DEFINE VARIABLE t-dserv   AS DECIMAL. 
  DEFINE VARIABLE t-dtax    AS DECIMAL. 
  DEFINE VARIABLE t-dgros   AS DECIMAL.
  DEFINE VARIABLE t-dqty    AS INTEGER.
 
  DEFINE VARIABLE t-mnet    AS DECIMAL. 
  DEFINE VARIABLE t-mserv   AS DECIMAL. 
  DEFINE VARIABLE t-mtax    AS DECIMAL. 
  DEFINE VARIABLE t-mgros   AS DECIMAL. 
  DEFINE VARIABLE t-mqty    AS INTEGER.
 
  DEFINE VARIABLE t-ynet    AS DECIMAL. 
  DEFINE VARIABLE t-yserv   AS DECIMAL. 
  DEFINE VARIABLE t-ytax    AS DECIMAL. 
  DEFINE VARIABLE t-ygros   AS DECIMAL. 
  DEFINE VARIABLE t-yqty    AS INTEGER.

  DEFINE VARIABLE vat       AS DECIMAL. 
  /* SY OCT 10 2917 */
  DEFINE VARIABLE vat2      AS DECIMAL. 
  DEFINE VARIABLE all-vat   AS DECIMAL.

  DEFINE VARIABLE serv      AS DECIMAL. 
  DEFINE VARIABLE it-exist  AS LOGICAL. 
  DEFINE VARIABLE serv-vat  AS LOGICAL. 
  DEFINE VARIABLE fact      AS DECIMAL. 
 
  DEFINE VARIABLE nett-amt  AS DECIMAL. 
  DEFINE VARIABLE nett-serv AS DECIMAL. 
  DEFINE VARIABLE nett-tax  AS DECIMAL. 
  DEFINE VARIABLE nett-vat  AS DECIMAL.

  DEFINE VARIABLE mbugdet   AS DECIMAL.
  DEFINE VARIABLE tbudget   AS DECIMAL.
  DEFINE VARIABLE gtbudget  AS DECIMAL.

  DEFINE VARIABLE cr-umsatz        AS LOGICAL.
  DEFINE VARIABLE curr-artnr       AS INTEGER NO-UNDO.
  DEFINE VARIABLE curr-departement AS INTEGER NO-UNDO.
 
  DEFINE VARIABLE fact1     AS DECIMAL INITIAL 1 NO-UNDO.
  DEFINE VARIABLE do-it     AS LOGICAL NO-UNDO INITIAL NO.
  DEFINE VARIABLE counter   AS INTEGER NO-UNDO.
  DEFINE VARIABLE x-sum     AS DECIMAL NO-UNDO.
  DEFINE VARIABLE x-sum2    AS DECIMAL NO-UNDO.
  DEFINE VARIABLE y-sum     AS DECIMAL NO-UNDO.
  DEFINE VARIABLE y-sum2    AS DECIMAL NO-UNDO.
  DEFINE BUFFER bumsz FOR umsatz.

  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH umsz-list: 
    delete umsz-list. 
  END. 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
  FOR EACH vat-list:
      DELETE vat-list.
  END.

  FOR EACH gvat-list:
      DELETE gvat-list.
  END.

  ASSIGN 
      t-dnet    = 0. 
      t-dserv   = 0. 
      t-dtax    = 0. 
      t-dgros   = 0. 
      t-mnet    = 0. 
      t-mserv   = 0. 
      t-mtax    = 0. 
      t-mgros   = 0. 
      t-ynet    = 0. 
      t-yserv   = 0. 
      t-ytax    = 0. 
      t-ygros   = 0. 
      gtbudget  = 0.

 /*ITA*/
  FOR EACH artikel WHERE (artart = 0 OR artart = 8) 
      AND artikel.departement GE from-dept 
      AND artikel.departement LE to-dept NO-LOCK BY artikel.artnr: 
    
       FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
          AND umsatz.departement = artikel.departement 
          AND umsatz.datum GE from-date AND umsatz.datum LE to-date 
          USE-INDEX umdate_index NO-LOCK NO-ERROR. 
       IF NOT AVAILABLE umsatz THEN DO:
           FIND FIRST not-avail-umstaz WHERE not-avail-umstaz.artnr = artikel.artnr
               AND not-avail-umstaz.depart = artikel.departement NO-LOCK NO-ERROR.
           IF AVAILABLE not-avail-umstaz THEN.
           ELSE DO:
               CREATE not-avail-umstaz.
               ASSIGN 
                   not-avail-umstaz.artnr   = artikel.artnr
                   not-avail-umstaz.depart  = artikel.departement
                   not-avail-umstaz.bezeich = artikel.bezeich.
           END.
       END.
  END.

  FOR EACH umsatz WHERE umsatz.departement GE from-dept 
       AND umsatz.departement LE to-dept
       AND umsatz.datum GE from-date 
       AND umsatz.datum LE to-date NO-LOCK
       BY umsatz.departement BY umsatz.artnr BY umsatz.datum :
        
       IF curr-artnr = 0 OR curr-artnr NE umsatz.artnr 
            OR (curr-artnr EQ umsatz.artnr AND curr-departement NE umsatz.departement) THEN 
       DO:
           FIND FIRST artikel WHERE artikel.artnr = umsatz.artnr 
             AND artikel.departement = umsatz.departement
             AND (artikel.artart = 0 OR artikel.artart = 8) NO-LOCK NO-ERROR.
           IF AVAILABLE artikel THEN DO:
               IF curr-artnr NE 0 THEN DO:
                   ASSIGN
                      it-exist  = NO
                      serv      = 0
                      vat       = 0
                      tbudget   = tbudget + mbudget.
               END.
               ASSIGN
                   curr-artnr = umsatz.artnr
                   do-it      = YES.
           END.
           ELSE ASSIGN do-it = NO.
       END.

       IF do-it = YES THEN DO:
             ASSIGN counter = counter + 1.
             IF (curr-departement NE umsatz.departement) OR counter = 1 THEN DO:
                IF counter NE 1 THEN DO:
                  /*cari semua yang tidak ada di umsatz*/ 
                  FOR EACH not-avail-umstaz WHERE not-avail-umstaz.depart = curr-departement NO-LOCK:
                       FIND FIRST budget WHERE MONTH(budget.datum) EQ MONTH(to-date) AND
                                YEAR(budget.datum) EQ YEAR(to-date) AND
                                budget.departement = not-avail-umstaz.depart AND
                                budget.artnr = not-avail-umstaz.artnr NO-LOCK NO-ERROR.
                        IF AVAILABLE budget AND budget.betrag NE 0 THEN
                        DO:  
                                IF NOT it-exist THEN 
                                DO: 
                                    it-exist = YES. 
                                    CREATE  cl-list. 
                                    ASSIGN  cl-list.artnr   = not-avail-umstaz.artnr 
                                            cl-list.dept    = not-avail-umstaz.depart 
                                            cl-list.bezeich = not-avail-umstaz.bezeich
                                            it-exist        = NO.
                                END. 
                                
                               
                                RUN sum-budget(first-date, to-date, not-avail-umstaz.artnr, not-avail-umstaz.depart, 
                                               OUTPUT mbudget).
                                ASSIGN 
                                    mbudget         = ROUND(mbudget, 1)
                                    cl-list.mbudget = mbudget
                                    tbudget         = tbudget + mbudget .
                        END.
                  END.
                  /*end*/
              

                    tbudget = ROUND(tbudget, 1).
                    FOR EACH cl-list WHERE cl-list.dept = hoteldpt.num: 
                      IF dgros NE 0 THEN cl-list.proz2 = cl-list.dgros / dgros * 100. 
                      IF mgros NE 0 THEN cl-list.proz4 = cl-list.mgros / mgros * 100. 
                      IF ygros NE 0 THEN cl-list.proz6 = cl-list.ygros / ygros * 100. 
                    END. 
                
                    IF totVatFlag THEN
                    DO:
                        FOR EACH vat-list WHERE vat-list.vat = 0 OR (vat-list.ytax = 0):
                            DELETE vat-list.
                        END.
                        
                        FOR EACH vat-list WHERE vat-list.dptnr = hoteldpt.num BY vat-list.vat:
                            CREATE cl-list. 
                            ASSIGN
                              cl-list.flag      = "**"
                              cl-list.bezeich   = "TOTAL VAT " + STRING(vat-list.vat * 100, ">>9.99") + " " + "%"
                              cl-list.dnet      = vat-list.dnet
                              cl-list.dserv     = vat-list.dserv 
                              cl-list.dtax      = vat-list.dtax
                              cl-list.dgros     = vat-list.dgros 
                              cl-list.mnet      = vat-list.mnet
                              cl-list.mserv     = vat-list.mserv 
                              cl-list.mtax      = vat-list.mtax
                              cl-list.mgros     = vat-list.mgros 
                              cl-list.ynet      = vat-list.ynet
                              cl-list.yserv     = vat-list.yserv   
                              cl-list.ytax      = vat-list.ytax
                              cl-list.ygros     = vat-list.ygros.
                        END.
                    END.
                    
                    CREATE cl-list. 
                    ASSIGN
                      cl-list.flag      = "**"
                      cl-list.bezeich   = "T O T A L" 
                      cl-list.dnet      = dnet
                      cl-list.dserv     = dserv 
                      cl-list.dtax      = dtax
                      cl-list.dgros     = dgros 
                      cl-list.mnet      = mnet
                      cl-list.mserv     = mserv 
                      cl-list.mtax      = mtax
                      cl-list.mgros     = mgros 
                      cl-list.ynet      = ynet
                      cl-list.yserv     = yserv 
                      cl-list.ytax      = ytax
                      cl-list.ygros     = ygros
                      cl-list.mbudget   = tbudget
                      cl-list.dqty      = dqty
                      cl-list.mqty      = mqty
                      cl-list.yqty      = yqty.
        
                    gtbudget = gtbudget + tbudget.
                    IF dgros NE 0 THEN cl-list.proz2 = 100. 
                    IF mgros NE 0 THEN cl-list.proz4 = 100. 
                    IF ygros NE 0 THEN cl-list.proz6 = 100. 
                END.

                FIND FIRST hoteldpt WHERE hoteldpt.num = umsatz.departement NO-LOCK NO-ERROR.
                IF AVAILABLE hoteldpt THEN DO:
                     CREATE cl-list. 
                     ASSIGN
                        cl-list.flag    = "*" 
                        cl-list.bezeich = STRING(hoteldpt.num) + " - " + hoteldpt.depart 
                        dnet            = 0
                        dserv           = 0
                        dtax            = 0
                        dgros           = 0
                        mnet            = 0
                        mserv           = 0
                        mtax            = 0
                        mgros           = 0
                        ynet            = 0
                        yserv           = 0
                        ytax            = 0
                        ygros           = 0
                        tbudget         = 0
                        dqty            = 0
                        mqty            = 0
                        yqty            = 0.
                END.

                ASSIGN curr-departement = umsatz.departement.
            END.
               
            /*
            RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service-code, 
                              artikel.mwst-code, OUTPUT serv, OUTPUT vat).
            fact = 1.00 + serv + vat. 
            */

            /* SY OCT 10 2917 */
            RUN calc-servtaxesbl.p (1, umsatz.artnr, umsatz.departement,
               umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).

            ASSIGN all-vat = vat + vat2.

            FIND FIRST vat-list WHERE vat-list.vat = vat AND vat-list.dptnr = artikel.departement NO-ERROR.
            IF NOT AVAILABLE vat-list THEN
            DO:
              CREATE vat-list.
              ASSIGN vat-list.vat = all-vat
                     vat-list.dptnr  = artikel.departement.
            END.    
    
            IF NOT it-exist THEN 
            DO: 
                it-exist = YES. 
                CREATE cl-list. 
                ASSIGN
                  cl-list.artnr     = umsatz.artnr 
                  cl-list.dept      = umsatz.departement 
                  cl-list.bezeich   = artikel.bezeich
                  cl-list.vat-proz  = all-vat. 
            END.

              IF vat = 1 OR 
                 (artikel.artnr = vat-artnr AND artikel.departement = 0) THEN 
              ASSIGN 
                nett-amt  = 0 
                nett-serv = 0 
                nett-tax  = umsatz.betrag.
              ELSE IF vat-str MATCHES ("*;" + STRING(artikel.artnr) + ";*")  
                    AND artikel.departement = 0 THEN 
              ASSIGN 
                    nett-amt  = 0 
                    nett-serv = 0 
                    nett-tax  = umsatz.betrag. 
              ELSE IF serv = 1 OR 
                   (artikel.artnr = serv-artnr AND artikel.departement = 0) THEN
              ASSIGN 
                nett-amt  = 0 
                nett-tax  = 0 
                nett-serv = umsatz.betrag. 
              ELSE
              ASSIGN                /*Wenni 12/7/14 */
                nett-amt  =  ROUND(umsatz.betrag / fact, price-decimal) 
                nett-serv =  ROUND(nett-amt * serv, price-decimal) 
                nett-tax  =  ROUND(nett-amt * vat, price-decimal)
                nett-amt  =  ROUND(umsatz.betrag - nett-serv - nett-tax, price-decimal)
              .  
             
              /** for column month budget */
              RUN sum-budget(first-date, to-date, artikel.artnr, artikel.departement, OUTPUT mbudget).
              ASSIGN 
                  mbudget         = ROUND(mbudget, 1)
                  cl-list.mbudget = mbudget.
                  

              IF umsatz.datum = to-date THEN  
              /*DO:
                  IF price-decimal EQ 2 THEN*/
                      ASSIGN
                        cl-list.dnet = ROUND(nett-amt / fact1, price-decimal)
                        cl-list.dgros = ROUND(umsatz.betrag / fact1, price-decimal) 
                        cl-list.dserv = ROUND(nett-serv / fact1, price-decimal)
                        cl-list.dtax = ROUND(nett-tax / fact1, price-decimal)
                        dnet = dnet + cl-list.dnet
                        dserv = dserv + cl-list.dserv 
                        dtax = dtax + cl-list.dtax
                        dgros = dgros + cl-list.dgros 
                        t-dnet = t-dnet + cl-list.dnet 
                        t-dserv = t-dserv + cl-list.dserv 
                        t-dtax = t-dtax + cl-list.dtax
                        t-dgros = t-dgros + cl-list.dgros
                        cl-list.dqty = umsatz.anzahl
                        dqty = dqty + cl-list.dqty
                        t-dqty = t-dqty + cl-list.dqty.
                  /*ELSE
                      ASSIGN
                        cl-list.dnet = TRUNCATE(nett-amt,0) / fact1
                        cl-list.dgros = umsatz.betrag / fact1 
                        cl-list.dserv = TRUNCATE(nett-serv,0) / fact1
                        cl-list.dtax = TRUNCATE(nett-tax,0) / fact1
                        dnet = dnet + cl-list.dnet
                        dserv = dserv + cl-list.dserv 
                        dtax = dtax + cl-list.dtax
                        dgros = dgros + cl-list.dgros 
                        t-dnet = t-dnet + cl-list.dnet 
                        t-dserv = t-dserv + cl-list.dserv 
                        t-dtax = t-dtax + cl-list.dtax
                        t-dgros = t-dgros + cl-list.dgros.
                      /*MESSAGE cl-list.dnet cl-list.dserv cl-list.dtax cl-list.dgros VIEW-AS ALERT-BOX INFO.*/
              END.*/

              IF umsatz.datum = to-date AND AVAILABLE vat-list THEN
              DO:
                  ASSIGN
                      vat-list.dtax = vat-list.dtax + ROUND(nett-tax / fact1, price-decimal)
                      vat-list.dnet = vat-list.dnet + ROUND(nett-amt / fact1, price-decimal) 
                      vat-list.dgros = vat-list.dgros + ROUND(umsatz.betrag / fact1, price-decimal) 
                      vat-list.dserv = vat-list.dserv + ROUND(nett-serv / fact1, price-decimal) 
                   .
              END.
    
              IF umsatz.datum GE first-date AND umsatz.datum LE to-date THEN 
              ASSIGN
                cl-list.mnet = cl-list.mnet + ROUND(nett-amt / fact1, price-decimal)  
                cl-list.mserv = cl-list.mserv + ROUND(nett-serv / fact1, price-decimal)  
                cl-list.mtax = cl-list.mtax + ROUND(nett-tax / fact1, price-decimal) 
                cl-list.mgros = cl-list.mgros + ROUND(umsatz.betrag / fact1, price-decimal)  
                mnet = mnet + ROUND(nett-amt / fact1, price-decimal)  
                mserv = mserv + ROUND(nett-serv / fact1, price-decimal)  
                mtax = mtax + ROUND(nett-tax / fact1, price-decimal) 
                mgros = mgros + ROUND(umsatz.betrag / fact1, price-decimal)  
                t-mnet = t-mnet + ROUND(nett-amt / fact1, price-decimal) 
                t-mserv = t-mserv + ROUND(nett-serv / fact1, price-decimal)  
                t-mtax = t-mtax + ROUND(nett-tax / fact1, price-decimal) 
                t-mgros = t-mgros + ROUND(umsatz.betrag / fact1, price-decimal) 
                cl-list.mqty = cl-list.mqty + umsatz.anzahl
                mqty = mqty + umsatz.anzahl
                t-mqty = t-mqty + umsatz.anzahl
              . 
              IF umsatz.datum GE first-date AND umsatz.datum LE to-date
                  AND AVAILABLE vat-list THEN 
                  ASSIGN
                  vat-list.mtax = vat-list.mtax + ROUND(nett-tax / fact1, price-decimal) 
                  vat-list.mnet = vat-list.mnet + ROUND(nett-amt / fact1, price-decimal) 
                  vat-list.mserv = vat-list.mserv + ROUND(nett-serv / fact1, price-decimal) 
                  vat-list.mgros = vat-list.mgros + ROUND(umsatz.betrag / fact1, price-decimal) .
     
              ASSIGN
                cl-list.ynet = cl-list.ynet + ROUND(nett-amt / fact1, price-decimal) 
                cl-list.yserv = cl-list.yserv + ROUND(nett-serv / fact1, price-decimal)  
                cl-list.ytax = cl-list.ytax + ROUND(nett-tax / fact1, price-decimal) 
                cl-list.ygros = cl-list.ygros + ROUND(umsatz.betrag / fact1, price-decimal)  
                ynet = ynet + ROUND(nett-amt / fact1, price-decimal) 
                yserv = yserv + ROUND(nett-serv / fact1, price-decimal)  
                ytax = ytax + ROUND(nett-tax / fact1, price-decimal) 
                ygros = ygros + ROUND(umsatz.betrag / fact1, price-decimal)  
                t-ynet = t-ynet + ROUND(nett-amt / fact1, price-decimal) 
                t-yserv = t-yserv + ROUND(nett-serv / fact1, price-decimal)  
                t-ytax = t-ytax + ROUND(nett-tax / fact1, price-decimal) 
                t-ygros = t-ygros + ROUND(umsatz.betrag / fact1, price-decimal) 
                cl-list.yqty = cl-list.yqty + umsatz.anzahl
                yqty = yqty + umsatz.anzahl
                t-yqty = t-yqty + umsatz.anzahl.

              IF AVAILABLE vat-list THEN
                  ASSIGN
                      vat-list.ytax = vat-list.ytax + ROUND(nett-tax / fact1, price-decimal) 
                      vat-list.ynet = vat-list.ynet + ROUND(nett-amt / fact1, price-decimal) 
                      vat-list.yserv = vat-list.yserv + ROUND(nett-serv / fact1, price-decimal) 
                      vat-list.ygros = vat-list.ygros + ROUND(umsatz.betrag / fact1, price-decimal) 
                      .              
       END. /*end do-it*/
  END.   /*end umsatz*/
  /*end ita*/

  /*field terakhir*/
  IF counter NE 1 THEN DO:
        /*cari semua yang tidak ada di umsatz*/ 
        FOR EACH not-avail-umstaz WHERE not-avail-umstaz.depart = curr-departement NO-LOCK:
             FIND FIRST budget WHERE MONTH(budget.datum) EQ MONTH(to-date) AND
                      YEAR(budget.datum) EQ YEAR(to-date) AND
                      budget.departement = not-avail-umstaz.depart AND
                      budget.artnr = not-avail-umstaz.artnr NO-LOCK NO-ERROR.
              IF AVAILABLE budget AND budget.betrag NE 0 THEN
              DO:  
                      IF NOT it-exist THEN 
                      DO: 
                          it-exist = YES. 
                          CREATE  cl-list. 
                          ASSIGN  cl-list.artnr   = not-avail-umstaz.artnr 
                                  cl-list.dept    = not-avail-umstaz.depart 
                                  cl-list.bezeich = not-avail-umstaz.bezeich
                                  it-exist        = NO.
                      END. 
                      
                     
                      RUN sum-budget(first-date, to-date, not-avail-umstaz.artnr, not-avail-umstaz.depart, 
                                     OUTPUT mbudget).
                      ASSIGN 
                          mbudget         = ROUND(mbudget, 1)
                          cl-list.mbudget = mbudget
                          tbudget         = tbudget + mbudget .
              END.
        END.
        /*end*/
  

      tbudget = ROUND(tbudget, 1).
      FOR EACH cl-list WHERE cl-list.dept = hoteldpt.num: 
        IF dgros NE 0 THEN cl-list.proz2 = cl-list.dgros / dgros * 100. 
        IF mgros NE 0 THEN cl-list.proz4 = cl-list.mgros / mgros * 100. 
        IF ygros NE 0 THEN cl-list.proz6 = cl-list.ygros / ygros * 100. 
      END. 
  
      IF totVatFlag THEN
      DO:
          FOR EACH vat-list WHERE vat-list.vat = 0 OR (vat-list.ytax = 0):
              DELETE vat-list.
          END.
          
          FOR EACH vat-list WHERE vat-list.dptnr = hoteldpt.num BY vat-list.vat:
              CREATE cl-list. 
              ASSIGN
                cl-list.flag      = "**"
                cl-list.bezeich   = "TOTAL VAT " + STRING(vat-list.vat * 100, ">>9.99") + " " + "%"
                cl-list.dnet      = vat-list.dnet
                cl-list.dserv     = vat-list.dserv 
                cl-list.dtax      = vat-list.dtax
                cl-list.dgros     = vat-list.dgros 
                cl-list.mnet      = vat-list.mnet
                cl-list.mserv     = vat-list.mserv 
                cl-list.mtax      = vat-list.mtax
                cl-list.mgros     = vat-list.mgros 
                cl-list.ynet      = vat-list.ynet
                cl-list.yserv     = vat-list.yserv   
                cl-list.ytax      = vat-list.ytax
                cl-list.ygros     = vat-list.ygros.
          END.
      END.
      
      CREATE cl-list. 
      ASSIGN
        cl-list.flag      = "**"
        cl-list.bezeich   = "T O T A L" 
        cl-list.dnet      = dnet
        cl-list.dserv     = dserv
        cl-list.dtax      = dtax
        cl-list.dgros     = dgros 
        cl-list.mnet      = mnet
        cl-list.mserv     = mserv 
        cl-list.mtax      = mtax
        cl-list.mgros     = mgros 
        cl-list.ynet      = ynet
        cl-list.yserv     = yserv 
        cl-list.ytax      = ytax
        cl-list.ygros     = ygros
        cl-list.mbudget   = tbudget
        cl-list.dqty      = dqty
        cl-list.mqty      = mqty
        cl-list.yqty      = yqty.

      gtbudget = gtbudget + tbudget.
      IF dgros NE 0 THEN cl-list.proz2 = 100. 
      IF mgros NE 0 THEN cl-list.proz4 = 100. 
      IF ygros NE 0 THEN cl-list.proz6 = 100. 
  END.
  /*end*/

  FOR EACH cl-list:
    IF cl-list.flag = "*" THEN
    DO:
      CREATE umsz-list.
      ASSIGN
        umsz-list.artnr   = STRING(cl-list.artnr, ">>>>")
        umsz-list.bezeich = cl-list.bezeich
      .
    END.
    ELSE
    DO:
      IF price-decimal = 2 THEN
      DO:
        CREATE umsz-list.
        ASSIGN
          umsz-list.artnr       = STRING(cl-list.artnr, ">>>>")  
          umsz-list.bezeich     = cl-list.bezeich
          umsz-list.day-nett    = STRING(cl-list.dnet, "->>>,>>>,>>>,>>9.99")
          umsz-list.day-serv    = STRING(cl-list.dserv, "->>>,>>>,>>>,>>9.99")
          umsz-list.day-tax     = STRING(cl-list.dtax, "->>>,>>>,>>>,>>9.99")
          umsz-list.day-gros    = STRING(cl-list.dgros, "->>>,>>>,>>>,>>9.99")
          umsz-list.day-persen  = STRING(cl-list.proz2, "->>>>9.99")
          umsz-list.mtd-nett    = STRING(cl-list.mnet, "->>>,>>>,>>>,>>9.99")
          umsz-list.mtd-serv    = STRING(cl-list.mserv, "->>>,>>>,>>>,>>9.99")
          umsz-list.mtd-tax     = STRING(cl-list.mtax, "->>>,>>>,>>>,>>9.99")
          umsz-list.mtd-gros    = STRING(cl-list.mgros, "->>>,>>>,>>>,>>9.99")
          umsz-list.mtd-persen  = STRING(cl-list.proz4, "->>>>9.99")
          umsz-list.ytd-nett    = STRING(cl-list.ynet, "->>>,>>>,>>>,>>9.99")
          umsz-list.ytd-serv    = STRING(cl-list.yserv, "->>>,>>>,>>>,>>9.99")
          umsz-list.ytd-tax     = STRING(cl-list.ytax, "->>>,>>>,>>>,>>9.99")
          umsz-list.ytd-gros    = STRING(cl-list.ygros, "->>>,>>>,>>>,>>9.99")
          umsz-list.ytd-persen  = STRING(cl-list.proz6, "->>>>9.99")
          umsz-list.month-bud   = STRING(cl-list.mbudget, "->,>>>,>>>,>>>,>>9.99")
        .
      END.
      ELSE
      DO:
        CREATE umsz-list.
        ASSIGN
          umsz-list.artnr       = STRING(cl-list.artnr, ">>>>")  
          umsz-list.bezeich     = cl-list.bezeich
          umsz-list.day-nett    = STRING(cl-list.dnet, "->>,>>>,>>>,>>>,>>9") 
          umsz-list.day-serv    = STRING(cl-list.dserv, "->>,>>>,>>>,>>>,>>9") 
          umsz-list.day-tax     = STRING(cl-list.dtax, "->>,>>>,>>>,>>>,>>9")  
          umsz-list.day-gros    = STRING(cl-list.dgros, "->>,>>>,>>>,>>>,>>9")
          umsz-list.day-persen  = STRING(cl-list.proz2, "->>>>9.99")     
          umsz-list.mtd-nett    = STRING(cl-list.mnet, "->>,>>>,>>>,>>>,>>9") 
          umsz-list.mtd-serv    = STRING(cl-list.mserv, "->>,>>>,>>>,>>>,>>9")  
          umsz-list.mtd-tax     = STRING(cl-list.mtax, "->>,>>>,>>>,>>>,>>9")   
          umsz-list.mtd-gros    = STRING(cl-list.mgros, "->>,>>>,>>>,>>>,>>9")
          umsz-list.mtd-persen  = STRING(cl-list.proz4, "->>>>9.99")        
          umsz-list.ytd-nett    = STRING(cl-list.ynet, "->>,>>>,>>>,>>>,>>9")      
          umsz-list.ytd-serv    = STRING(cl-list.yserv, "->>,>>>,>>>,>>>,>>9")      
          umsz-list.ytd-tax     = STRING(cl-list.ytax, "->>,>>>,>>>,>>>,>>9")       
          umsz-list.ytd-gros    = STRING(cl-list.ygros, "->>,>>>,>>>,>>>,>>9")     
          umsz-list.ytd-persen  = STRING(cl-list.proz6, "->>>>9.99")              
          umsz-list.month-bud   = STRING(cl-list.mbudget, "->,>>>,>>>,>>>,>>9.99")
        .
      END.  

      umsz-list.dqty        = STRING(cl-list.dqty, "->>>>>>9").
      umsz-list.mqty        = STRING(cl-list.mqty, "->>>>>>9").
      umsz-list.yqty        = STRING(cl-list.yqty, "->>>>>>9").
    END.
  END. /*end for each*/

  IF totVatFlag THEN
  DO: 
      FOR EACH vat-list BY vat-list.vat:
          FIND FIRST gvat-list WHERE gvat-list.vat = vat-list.vat NO-ERROR.
          IF NOT AVAILABLE gvat-list THEN
          DO:
              CREATE gvat-list.
              ASSIGN
                  gvat-list.vat = vat-list.vat.
          END.
          ASSIGN
              gvat-list.dnet      = gvat-list.dnet + vat-list.dnet
              gvat-list.dserv     = gvat-list.dserv + vat-list.dserv 
              gvat-list.dtax      = gvat-list.dtax + vat-list.dtax
              gvat-list.dgros     = gvat-list.dgros + vat-list.dgros 
              gvat-list.mnet      = gvat-list.mnet + vat-list.mnet
              gvat-list.mserv     = gvat-list.mserv + vat-list.mserv 
              gvat-list.mtax      = gvat-list.mtax + vat-list.mtax
              gvat-list.mgros     = gvat-list.mgros + vat-list.mgros 
              gvat-list.ynet      = gvat-list.ynet + vat-list.ynet
              gvat-list.yserv     = gvat-list.yserv + vat-list.yserv   
              gvat-list.ytax      = gvat-list.ytax + vat-list.ytax
              gvat-list.ygros     = gvat-list.ygros + vat-list.ygros.
      END.

      FOR EACH gvat-list BY gvat-list.vat:
          CREATE cl-list. 
          ASSIGN
              cl-list.flag      = "**"
              cl-list.bezeich   = "GTOTAL VAT " + STRING(gvat-list.vat * 100, ">>9.99") + " " + "%"
              cl-list.dnet      = gvat-list.dnet
              cl-list.dserv     = gvat-list.dserv 
              cl-list.dtax      = gvat-list.dtax
              cl-list.dgros     = gvat-list.dgros 
              cl-list.mnet      = gvat-list.mnet
              cl-list.mserv     = gvat-list.mserv 
              cl-list.mtax      = gvat-list.mtax
              cl-list.mgros     = gvat-list.mgros 
              cl-list.ynet      = gvat-list.ynet
              cl-list.yserv     = gvat-list.yserv   
              cl-list.ytax      = gvat-list.ytax
              cl-list.ygros     = gvat-list.ygros.

          CREATE umsz-list.
          IF price-decimal = 2 THEN 
          DO:
            ASSIGN                    
              umsz-list.artnr       = STRING(cl-list.artnr, ">>>>")                   
              umsz-list.bezeich     = cl-list.bezeich                                 
              umsz-list.day-nett    = STRING(cl-list.dnet, "->>>,>>>,>>>,>>9.99")     
              umsz-list.day-serv    = STRING(cl-list.dserv, "->>>,>>>,>>>,>>9.99")    
              umsz-list.day-tax     = STRING(cl-list.dtax, "->>>,>>>,>>>,>>9.99")     
              umsz-list.day-gros    = STRING(cl-list.dgros, "->>>,>>>,>>>,>>9.99")    
              umsz-list.day-persen  = STRING(cl-list.proz2, "->>>>9.99")              
              umsz-list.mtd-nett    = STRING(cl-list.mnet, "->>>,>>>,>>>,>>9.99")     
              umsz-list.mtd-serv    = STRING(cl-list.mserv, "->>>,>>>,>>>,>>9.99")    
              umsz-list.mtd-tax     = STRING(cl-list.mtax, "->>>,>>>,>>>,>>9.99")     
              umsz-list.mtd-gros    = STRING(cl-list.mgros, "->>>,>>>,>>>,>>9.99")    
              umsz-list.mtd-persen  = STRING(cl-list.proz4, "->>>>9.99")              
              umsz-list.ytd-nett    = STRING(cl-list.ynet, "->>>,>>>,>>>,>>9.99")     
              umsz-list.ytd-serv    = STRING(cl-list.yserv, "->>>,>>>,>>>,>>9.99")    
              umsz-list.ytd-tax     = STRING(cl-list.ytax, "->>>,>>>,>>>,>>9.99")     
              umsz-list.ytd-gros    = STRING(cl-list.ygros, "->>>,>>>,>>>,>>9.99")    
              umsz-list.ytd-persen  = STRING(cl-list.proz6, "->>>>9.99")              
              umsz-list.month-bud   = STRING(cl-list.mbudget, "->,>>>,>>>,>>>,>>9.99")
            .
          END.               
          ELSE 
          DO: 
            ASSIGN
              umsz-list.artnr       = STRING(cl-list.artnr, ">>>>")                                      
              umsz-list.bezeich     = cl-list.bezeich                                                    
              umsz-list.day-nett    = STRING(cl-list.dnet, "->>,>>>,>>>,>>>,>>9")      
              umsz-list.day-serv    = STRING(cl-list.dserv, "->>,>>>,>>>,>>>,>>9")     
              umsz-list.day-tax     = STRING(cl-list.dtax, "->>,>>>,>>>,>>>,>>9")      
              umsz-list.day-gros    = STRING(cl-list.dgros, "->>,>>>,>>>,>>>,>>9")     
              umsz-list.day-persen  = STRING(cl-list.proz2, "->>>>9.99")               
              umsz-list.mtd-nett    = STRING(cl-list.mnet, "->>,>>>,>>>,>>>,>>9")      
              umsz-list.mtd-serv    = STRING(cl-list.mserv, "->>,>>>,>>>,>>>,>>9")     
              umsz-list.mtd-tax     = STRING(cl-list.mtax, "->>,>>>,>>>,>>>,>>9")      
              umsz-list.mtd-gros    = STRING(cl-list.mgros, "->>,>>>,>>>,>>>,>>9")     
              umsz-list.mtd-persen  = STRING(cl-list.proz4, "->>>>9.99")               
              umsz-list.ytd-nett    = STRING(cl-list.ynet, "->>,>>>,>>>,>>>,>>9")      
              umsz-list.ytd-serv    = STRING(cl-list.yserv, "->>,>>>,>>>,>>>,>>9")     
              umsz-list.ytd-tax     = STRING(cl-list.ytax, "->>,>>>,>>>,>>>,>>9")      
              umsz-list.ytd-gros    = STRING(cl-list.ygros, "->>,>>>,>>>,>>>,>>9")     
              umsz-list.ytd-persen  = STRING(cl-list.proz6, "->>>>9.99")               
              umsz-list.month-bud   = STRING(cl-list.mbudget, "->,>>>,>>>,>>>,>>9.99") 
            .
          END. 
      END. /*end for each*/
  END. /*end totVatFlag*/

  CREATE cl-list. 
  ASSIGN
    cl-list.flag    = "***"
    cl-list.bezeich = "GRAND TOTAL" 
    cl-list.dnet    = t-dnet
    cl-list.dserv   = t-dserv 
    cl-list.dtax    = t-dtax
    cl-list.dgros   = t-dgros 
    cl-list.mnet    = t-mnet
    cl-list.mserv   = t-mserv 
    cl-list.mtax    = t-mtax
    cl-list.mgros   = t-mgros 
    cl-list.ynet    = t-ynet
    cl-list.yserv   = t-yserv 
    cl-list.ytax    = t-ytax
    cl-list.ygros   = t-ygros
    cl-list.mbudget = gtbudget
    cl-list.dqty    = t-dqty
    cl-list.mqty    = t-mqty  
    cl-list.yqty    = t-yqty.

  IF t-dgros NE 0 THEN cl-list.proz2 = 100. 
  IF t-mgros NE 0 THEN cl-list.proz4 = 100. 
  IF t-ygros NE 0 THEN cl-list.proz6 = 100.

  CREATE umsz-list.
  IF price-decimal = 2 THEN
  DO:
    ASSIGN                                                                    
      umsz-list.artnr       = STRING(cl-list.artnr, ">>>>")                   
      umsz-list.bezeich     = cl-list.bezeich                                 
      umsz-list.day-nett    = STRING(cl-list.dnet, "->>>,>>>,>>>,>>9.99")     
      umsz-list.day-serv    = STRING(cl-list.dserv, "->>>,>>>,>>>,>>9.99")    
      umsz-list.day-tax     = STRING(cl-list.dtax, "->>>,>>>,>>>,>>9.99")     
      umsz-list.day-gros    = STRING(cl-list.dgros, "->>>,>>>,>>>,>>9.99")    
      umsz-list.day-persen  = STRING(cl-list.proz2, "->>>>9.99")              
      umsz-list.mtd-nett    = STRING(cl-list.mnet, "->>>,>>>,>>>,>>9.99")     
      umsz-list.mtd-serv    = STRING(cl-list.mserv, "->>>,>>>,>>>,>>9.99")    
      umsz-list.mtd-tax     = STRING(cl-list.mtax, "->>>,>>>,>>>,>>9.99")     
      umsz-list.mtd-gros    = STRING(cl-list.mgros, "->>>,>>>,>>>,>>9.99")    
      umsz-list.mtd-persen  = STRING(cl-list.proz4, "->>>>9.99")              
      umsz-list.ytd-nett    = STRING(cl-list.ynet, "->>>,>>>,>>>,>>9.99")     
      umsz-list.ytd-serv    = STRING(cl-list.yserv, "->>>,>>>,>>>,>>9.99")    
      umsz-list.ytd-tax     = STRING(cl-list.ytax, "->>>,>>>,>>>,>>9.99")     
      umsz-list.ytd-gros    = STRING(cl-list.ygros, "->>>,>>>,>>>,>>9.99")    
      umsz-list.ytd-persen  = STRING(cl-list.proz6, "->>>>9.99")              
      umsz-list.month-bud   = STRING(cl-list.mbudget, "->,>>>,>>>,>>>,>>9.99")
    .                                                                         
  END.
  ELSE
  DO:
    ASSIGN
      umsz-list.artnr       = STRING(cl-list.artnr, ">>>>")                     
      umsz-list.bezeich     = cl-list.bezeich                                   
      umsz-list.day-nett    = STRING(cl-list.dnet, "->>,>>>,>>>,>>>,>>9")       
      umsz-list.day-serv    = STRING(cl-list.dserv, "->>,>>>,>>>,>>>,>>9")      
      umsz-list.day-tax     = STRING(cl-list.dtax, "->>,>>>,>>>,>>>,>>9")       
      umsz-list.day-gros    = STRING(cl-list.dgros, "->>,>>>,>>>,>>>,>>9")      
      umsz-list.day-persen  = STRING(cl-list.proz2, "->>>>9.99")                
      umsz-list.mtd-nett    = STRING(cl-list.mnet, "->>,>>>,>>>,>>>,>>9")       
      umsz-list.mtd-serv    = STRING(cl-list.mserv, "->>,>>>,>>>,>>>,>>9")      
      umsz-list.mtd-tax     = STRING(cl-list.mtax, "->>,>>>,>>>,>>>,>>9")       
      umsz-list.mtd-gros    = STRING(cl-list.mgros, "->>,>>>,>>>,>>>,>>9")      
      umsz-list.mtd-persen  = STRING(cl-list.proz4, "->>>>9.99")                
      umsz-list.ytd-nett    = STRING(cl-list.ynet, "->>,>>>,>>>,>>>,>>9")       
      umsz-list.ytd-serv    = STRING(cl-list.yserv, "->>,>>>,>>>,>>>,>>9")      
      umsz-list.ytd-tax     = STRING(cl-list.ytax, "->>,>>>,>>>,>>>,>>9")       
      umsz-list.ytd-gros    = STRING(cl-list.ygros, "->>,>>>,>>>,>>>,>>9")      
      umsz-list.ytd-persen  = STRING(cl-list.proz6, "->>>>9.99")                
      umsz-list.month-bud   = STRING(cl-list.mbudget, "->,>>>,>>>,>>>,>>9.99")  
    .
  END.

  umsz-list.dqty = STRING(cl-list.dqty, "->>>>>>9").
  umsz-list.mqty = STRING(cl-list.mqty, "->>>>>>9").
  umsz-list.yqty = STRING(cl-list.yqty, "->>>>>>9").

END PROCEDURE.

PROCEDURE sum-budget :
    DEFINE INPUT PARAMETER from-date    AS DATE.
    DEFINE INPUT PARAMETER to-date      AS DATE.
    DEFINE INPUT PARAMETER artnr        AS INTEGER.
    DEFINE INPUT PARAMETER deptno       AS INTEGER.
    DEFINE OUTPUT PARAMETER mbudget     AS DECIMAL INITIAL 0.
    /*DEFINE OUTPUT PARAMETER tbudget     AS DECIMAL INITIAL 0.*/

    IF MONTH(from-date) EQ MONTH(to-date) THEN
    DO:
        FOR EACH budget WHERE MONTH(budget.datum) EQ MONTH(to-date) AND
            YEAR(budget.datum) EQ YEAR(to-date) AND
            budget.departement = deptno AND
            budget.artnr = artnr NO-LOCK:
            mbudget = mbudget + budget.betrag.
        END.
    END.
END.

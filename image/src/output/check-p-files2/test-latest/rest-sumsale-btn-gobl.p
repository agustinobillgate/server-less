
DEFINE TEMP-TABLE outstand-list 
  FIELD deptname AS CHAR FORMAT "x(24)" 
  FIELD name     AS CHAR FORMAT "x(16)" 
  FIELD rechnr   AS INTEGER FORMAT " >,>>>,>>9" 
  FIELD foreign  AS DECIMAL FORMAT "->>>,>>9.99" 
  FIELD saldo    AS DECIMAL FORMAT "->>,>>>,>>9.99". 

DEFINE TEMP-TABLE pay-list 
  FIELD flag    AS INTEGER /* 1 cash  2 room  3 CC  4 EL  5 CL  6 Comp  */ 
  FIELD bezeich AS CHAR FORMAT "x(24)" 
  FIELD artnr   AS INTEGER FORMAT ">>>>9 " 
  FIELD rechnr  AS INTEGER FORMAT ">>>>>>9 " 
  FIELD foreign AS DECIMAL FORMAT "->>>,>>9.99" 
  FIELD saldo   AS DECIMAL FORMAT "->>,>>>,>>9.99". 

DEFINE TEMP-TABLE comp-list
    FIELD rechnr AS INTEGER FORMAT ">>>>>>9 ". 

DEFINE TEMP-TABLE turnover 
  FIELD compli          AS LOGICAL INITIAL NO 
  FIELD compli-amt      AS DECIMAL 
  FIELD departement     LIKE h-bill.departement 
  FIELD kellner-nr      LIKE h-bill.kellner-nr 
  FIELD name            AS CHAR FORMAT "x(24)" LABEL "Department" 
  FIELD tischnr         LIKE h-bill.tischnr COLUMN-LABEL "Tbl" 
  FIELD rechnr          AS CHAR FORMAT "x(7)" COLUMN-LABEL "Bill-No     " 
  FIELD belegung        AS INTEGER FORMAT ">>>>9" COLUMN-LABEL "Pax" 
  FIELD artnr           LIKE h-bill-line.artnr 
  FIELD info           AS CHAR FORMAT "x(4)"        LABEL "Info" 
  FIELD food            AS DECIMAL FORMAT "->>,>>>,>>9" 
  FIELD beverage        AS DECIMAL FORMAT "->>,>>>,>>9" 
  FIELD misc            AS DECIMAL FORMAT "->>>,>>9" 
  FIELD cigarette       AS DECIMAL FORMAT "->>>,>>9" 
  FIELD discount        AS DECIMAL FORMAT "->>>,>>9" 
  FIELD t-service       AS DECIMAL FORMAT "->,>>>,>>9" 
                          COLUMN-LABEL "Service" 
  FIELD t-tax           AS DECIMAL FORMAT "->,>>>,>>9" 
                          COLUMN-LABEL "Tax" 
  FIELD t-debit         AS DECIMAL FORMAT "->>,>>>,>>9" LABEL "Total" 
  FIELD t-credit        AS DECIMAL FORMAT "->>,>>>,>>9" 
  FIELD p-cash          AS DECIMAL FORMAT "->>,>>>,>>9" 
  FIELD p-cash1         AS DECIMAL FORMAT "->,>>9.99" 
  FIELD r-transfer      AS DECIMAL FORMAT "->>,>>>,>>9" LABEL "Transfer" 
  FIELD c-ledger        AS DECIMAL FORMAT "->>,>>>,>>9" LABEL "CC / CL". 

DEF TEMP-TABLE tt-artnr
    FIELD curr-i AS INTEGER
    FIELD artnr  AS INTEGER
.

DEF INPUT-OUTPUT PARAMETER curr-dept AS INT.
DEF INPUT-OUTPUT PARAMETER dept-name AS CHAR.
DEF INPUT-OUTPUT PARAMETER exchg-rate AS DECIMAL.

DEF INPUT PARAMETER TABLE FOR tt-artnr.

DEF INPUT PARAMETER ldry AS INT.
DEF INPUT PARAMETER dstore AS INT.
DEF INPUT PARAMETER clb AS INT.
DEF INPUT PARAMETER zeit2 AS INT.
DEF INPUT PARAMETER zeit1 AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER t-betrag AS DECIMAL FORMAT "->>,>>>,>>9.99". 
DEF OUTPUT PARAMETER t-foreign AS DECIMAL FORMAT "->>>,>>9.99". 
DEF OUTPUT PARAMETER TABLE FOR turnover.
DEF OUTPUT PARAMETER TABLE FOR outstand-list.
DEF OUTPUT PARAMETER TABLE FOR pay-list.


DEFINE VARIABLE artnr-list  AS INTEGER EXTENT 5 NO-UNDO.
DEFINE VARIABLE curr-rechnr AS INTEGER NO-UNDO INIT -1.
DEFINE VARIABLE new-dept AS INTEGER NO-UNDO INIT -1.

DEFINE VARIABLE tot-food     AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-beverage AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-misc     AS DECIMAL FORMAT "->>>,>>9". 
DEFINE VARIABLE tot-cigar    AS DECIMAL FORMAT "->>>,>>9". 
DEFINE VARIABLE tot-disc     AS DECIMAL FORMAT "->>>,>>9". 
DEFINE VARIABLE tot-serv     AS DECIMAL FORMAT "->,>>>,>>9". 
DEFINE VARIABLE tot-tax      AS DECIMAL FORMAT "->,>>>,>>9". 
DEFINE VARIABLE tot-debit    AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-cash     AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-cash1    AS DECIMAL FORMAT "->,>>9.99". 
DEFINE VARIABLE tot-trans    AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-ledger   AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-cover    AS INTEGER FORMAT ">>>9". 

DEFINE VARIABLE t-food      AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE t-beverage  AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE t-misc      AS DECIMAL FORMAT "->>>,>>9". 
DEFINE VARIABLE t-cigar     AS DECIMAL FORMAT "->>>,>>9". 
DEFINE VARIABLE t-disc      AS DECIMAL FORMAT "->>>,>>9". 
DEFINE VARIABLE t-serv      AS DECIMAL FORMAT "->,>>>,>>9". 
DEFINE VARIABLE t-tax       AS DECIMAL FORMAT "->,>>>,>>9". 
DEFINE VARIABLE t-debit     AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE t-cash      AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE t-cash1     AS DECIMAL FORMAT "->,>>9.99". 
DEFINE VARIABLE t-trans     AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE t-ledger    AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE t-cover     AS INTEGER FORMAT ">>>9". 
                             
DEFINE VARIABLE anz-comp    AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE val-comp    AS DECIMAL FORMAT "->,>>>,>>9.99". 
DEFINE VARIABLE anz-coup    AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE val-coup    AS DECIMAL FORMAT "->,>>>,>>9.99". 
 
DEFINE VARIABLE return-debit    AS DECIMAL FORMAT "->>,>>>,>>9".
DEFINE VARIABLE return-cash1    AS DECIMAL FORMAT "->>,>>>,>>9".
DEFINE VARIABLE return-cash     AS DECIMAL FORMAT "->>,>>>,>>9".
DEFINE VARIABLE return-trans    AS DECIMAL FORMAT "->>,>>>,>>9".
DEFINE VARIABLE return-ledger   AS DECIMAL FORMAT "->>,>>>,>>9".

DEFINE VARIABLE compli-flag     AS LOGICAL. 

DEF BUFFER bh-bill-line FOR h-bill-line.
DEF BUFFER bh-artikel FOR h-artikel.

RUN daysale-list. 

PROCEDURE daysale-list: 
DEFINE VARIABLE from-dept AS INTEGER NO-UNDO.
DEFINE VARIABLE to-dept AS INTEGER NO-UNDO.
DEFINE VARIABLE ft-dept AS INTEGER NO-UNDO.
 
  FOR EACH tt-artnr:
      ASSIGN artnr-list[tt-artnr.curr-i] = tt-artnr.artnr.
  END.

  ASSIGN
    t-betrag  = 0 
    t-foreign = 0
  . 
 
  FOR EACH turnover: 
    DELETE turnover. 
  END. 
  FOR EACH pay-list: 
    DELETE pay-list. 
  END. 
  FOR EACH outstand-list: 
    DELETE outstand-list. 
  END. 
 
  tot-cover = 0. 
  tot-food = 0. 
  tot-beverage = 0. 
  tot-misc = 0. 
  tot-disc = 0. 
  tot-serv = 0. 
  tot-tax = 0. 
  tot-debit = 0. 
  tot-cash1 = 0. 
  tot-cash = 0. 
  tot-trans = 0. 
  tot-ledger = 0. 

  /*
  FIND FIRST hoteldpt WHERE hoteldpt.num GE 1 
      AND hoteldpt.num NE ldry AND hoteldpt.num NE dstore
      AND hoteldpt.num NE clb NO-LOCK NO-ERROR.
  IF AVAILABLE hoteldpt THEN from-dept = hoteldpt.num.

  FOR EACH hoteldpt WHERE hoteldpt.num GE 1 
      AND hoteldpt.num NE ldry AND hoteldpt.num NE dstore
      AND hoteldpt.num NE clb NO-LOCK BY hoteldpt.num DESC:

      to-dept = hoteldpt.num.
  END.
  */

  /*Create Outstanding*/
  FOR EACH hoteldpt WHERE hoteldpt.num GE 1 
      AND hoteldpt.num NE ldry AND hoteldpt.num NE dstore
      AND hoteldpt.num NE clb NO-LOCK BY hoteldpt.num DESC:

      curr-dept = hoteldpt.num. 
      dept-name = hoteldpt.depart.

      FOR EACH h-bill WHERE h-bill.flag EQ 0 AND h-bill.saldo NE 0 
          AND h-bill.departement EQ curr-dept NO-LOCK USE-INDEX dept_ix, 
          FIRST kellner WHERE kellner.kellner-nr EQ h-bill.kellner-nr NO-LOCK
          BY h-bill.rechnr: 
          
          CREATE outstand-list. 
          ASSIGN
              outstand-list.deptname = STRING(curr-dept,"99") + " - " + dept-name 
              outstand-list.rechnr = h-bill.rechnr 
              outstand-list.name = kellner.kellnername              
          .
    
          FOR EACH h-bill-line WHERE h-bill-line.rechnr EQ h-bill.rechnr 
              AND h-bill-line.departement EQ curr-dept NO-LOCK: 
    
              ASSIGN
                  outstand-list.saldo = outstand-list.saldo + h-bill-line.betrag 
                  outstand-list.foreign = outstand-list.foreign + h-bill-line.fremdwbetrag
              .
          END. 
      END.
  END.  

  FOR EACH hoteldpt WHERE hoteldpt.num GE 1 
      AND hoteldpt.num NE ldry AND hoteldpt.num NE dstore
      AND hoteldpt.num NE clb NO-LOCK: 
      curr-dept = hoteldpt.num. 
      dept-name = hoteldpt.depart.             

      CREATE turnover. 
      turnover.departement = curr-dept. 
      turnover.name = STRING(curr-dept,"99") + " - " + dept-name. 
      
      IF (zeit2 - zeit1) GE (24 * 3600 - 60) THEN 
      DO:
          FOR EACH h-bill-line WHERE h-bill-line.bill-datum EQ from-date
              AND h-bill-line.departement EQ curr-dept NO-LOCK USE-INDEX bildat_index,
              FIRST h-bill WHERE h-bill.rechnr EQ h-bill-line.rechnr
                  AND h-bill.departement EQ h-bill-line.departement 
                  AND h-bill.flag EQ 1 NO-LOCK 
              BY h-bill-line.rechnr:

              RUN create-turnover.
          END.
      END.          
      ELSE IF zeit1 GT zeit2 THEN
      DO:
          FOR EACH h-bill-line WHERE h-bill-line.bill-datum EQ from-date
              AND h-bill-line.departement EQ curr-dept 
              AND h-bill-line.zeit GE zeit1 NO-LOCK USE-INDEX bildat_index,
              FIRST h-bill WHERE h-bill.rechnr EQ h-bill-line.rechnr
                  AND h-bill.departement EQ h-bill-line.departement 
                  AND h-bill.flag EQ 1 NO-LOCK
              BY h-bill-line.rechnr:

              RUN create-turnover.
          END.
      END.
      ELSE
      DO:
          FOR EACH h-bill-line WHERE h-bill-line.bill-datum EQ from-date
              AND h-bill-line.departement EQ curr-dept 
              AND h-bill-line.zeit GE zeit1 
              AND h-bill-line.zeit LE zeit2 NO-LOCK USE-INDEX bildat_index,
              FIRST h-bill WHERE h-bill.rechnr EQ h-bill-line.rechnr
                  AND h-bill.departement EQ h-bill-line.departement 
                  AND h-bill.flag EQ 1 NO-LOCK
              BY h-bill-line.rechnr:

              RUN create-turnover.
          END.
      END.
  END.
 
  FOR EACH turnover WHERE turnover.compli-amt NE 0: 
      turnover.compli = YES. 
      /*tot-food = tot-food - turnover.food. /*william 556A23 25/01/24*/
      tot-beverage = tot-beverage - turnover.beverage. 
      tot-misc = tot-misc - turnover.misc. 
      tot-disc = tot-disc - turnover.discount. 
      tot-serv = tot-serv - turnover.t-service. 
      tot-tax  = tot-tax  - turnover.t-tax. 
      tot-cover = tot-cover - turnover.belegung.
      /*tot-debit = tot-debit - turnover.compli-amt.*/ /*FD Comment Sept 22, 2021*/
      
      /*FD Sept 22, 2021 => For balancing total value when compli = YES*/
      return-debit    = return-debit  + turnover.t-debit.
      return-cash1    = return-cash1  + turnover.p-cash1.
      return-cash     = return-cash   + turnover.p-cash.
      return-trans    = return-trans  + turnover.r-transfer.
      return-ledger   = return-ledger + turnover.c-ledger.*/    

  END. 

 
  CREATE turnover. 
  turnover.name = "TOTAL". 
  turnover.belegung =  tot-cover. 
  turnover.food = tot-food. 
  turnover.beverage = tot-beverage. 
  turnover.misc = tot-misc. 
  turnover.discount = tot-disc. 
  turnover.t-service = tot-serv. 
  turnover.t-tax = tot-tax. 
  turnover.t-debit = tot-debit - return-debit. 
  turnover.p-cash = tot-cash - return-cash. 
  turnover.p-cash1 = tot-cash1 - return-cash1. 
  turnover.r-transfer = tot-trans - return-trans. 
  turnover.c-ledger = tot-ledger - return-ledger. 
END PROCEDURE. 

PROCEDURE create-turnover:
DEFINE VARIABLE dept    AS INTEGER FORMAT ">>9" INITIAL 1. 
DEFINE VARIABLE i       AS INTEGER. 
DEFINE VARIABLE curr-s  AS INTEGER. 
DEFINE VARIABLE billnr  AS INTEGER. 
DEFINE VARIABLE d-name  AS CHARACTER FORMAT "x(24)". 
DEFINE VARIABLE usr-nr  AS INTEGER. 
DEFINE VARIABLE d-found AS LOGICAL INITIAL "no". 
DEFINE VARIABLE c-found AS LOGICAL INITIAL "no". 
DEFINE VARIABLE vat     AS DECIMAL. 
DEFINE VARIABLE service AS DECIMAL. 
DEFINE VARIABLE netto   AS DECIMAL. 
DEFINE VARIABLE found   AS LOGICAL INITIAL NO. 
DEFINE VARIABLE vat2    AS DECIMAL NO-UNDO.
DEFINE VARIABLE fact    AS DECIMAL NO-UNDO.

    IF curr-rechnr NE h-bill.rechnr THEN
    DO:
        ASSIGN
            turnover.belegung = turnover.belegung + h-bill.belegung. 
            tot-cover = tot-cover + h-bill.belegung
        .       

        curr-rechnr = h-bill.rechnr.        
    END.
   
    IF h-bill-line.artnr EQ 0 THEN    /* room OR bill transfer */ 
    DO: 
        FIND FIRST pay-list WHERE pay-list.flag EQ 2 NO-ERROR. 
        IF NOT AVAILABLE pay-list THEN 
        DO: 
            CREATE pay-list. 
            pay-list.flag = 2. 
            pay-list.bezeich = "Room / Bill Transfer". 
        END. 
        pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 
        t-betrag = t-betrag - h-bill-line.betrag. 
        turnover.r-transfer = turnover.r-transfer - h-bill-line.betrag. 

        i = 0. 
        found = NO. 
        /* FD comment => this syntax can be stuck
        DO WHILE NOT found: 
          i = i + 1. 
          IF SUBSTR(h-bill-line.bezeich, i, 1) EQ "*" THEN found = YES. 
        END. 
        */
        turnover.t-credit = turnover.t-credit - h-bill-line.betrag. 
        tot-trans = tot-trans - h-bill-line.betrag. 
    END. 
    ELSE
    DO:
        ASSIGN compli-flag = NO. /*william 556A23 25/01/24*/
          FOR EACH bh-bill-line WHERE bh-bill-line.rechnr = h-bill-line.rechnr AND bh-bill-line.departement = h-bill-line.departement NO-LOCK ,
             FIRST bh-artikel WHERE bh-artikel.artnr = bh-bill-line.artnr AND bh-artikel.departement = bh-bill-line.departement 
             AND bh-artikel.artart GE 11 AND bh-artikel.artart LE 12 NO-LOCK BY bh-artikel.artart DESC:
             ASSIGN compli-flag = YES.
             LEAVE.
          END.
       
        FIND FIRST h-artikel WHERE h-artikel.artnr EQ h-bill-line.artnr 
            AND h-artikel.departement EQ h-bill-line.departement NO-LOCK NO-ERROR.
        IF AVAILABLE h-artikel THEN
        DO:
            IF h-artikel.artart EQ 11 OR h-artikel.artart EQ 12 THEN /* complimentary OR meal coupon */              
            DO:                 
                /*tot-cover = tot-cover + h-bill.belegung. 
                t-cover = t-cover + h-bill.belegung.*/ 
                
                IF h-artikel.artart = 11 THEN 
                DO: 
                    FIND FIRST pay-list WHERE pay-list.flag EQ 6 
                        AND pay-list.bezeich EQ h-artikel.bezeich NO-ERROR. 
                    IF NOT AVAILABLE pay-list THEN 
                    DO: 
                        CREATE pay-list. 
                        pay-list.flag = 6. 
                        pay-list.bezeich = h-artikel.bezeich. 
                    END. 
                    pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 
                    IF h-bill-line.betrag LT 0 THEN anz-comp = anz-comp + 1. 
                    ELSE IF h-bill-line.betrag GT 0 THEN anz-comp = anz-comp - 1. 
                    turnover.compli-amt = turnover.compli-amt - h-bill-line.betrag. 
                    val-comp = val-comp - h-bill-line.betrag. 
                END. 
                ELSE IF h-artikel.artart = 12 THEN 
                DO: 
                    FIND FIRST pay-list WHERE pay-list.flag EQ 7 NO-ERROR. 
                    IF NOT AVAILABLE pay-list THEN 
                    DO: 
                        CREATE pay-list. 
                        pay-list.flag = 7. 
                        pay-list.bezeich = "Meal Coupon". 
                    END. 
                    pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 
                    IF h-bill-line.betrag LT 0 THEN anz-coup = anz-coup + 1. 
                    ELSE IF h-bill-line.betrag GT 0 THEN anz-coup = anz-coup - 1. 
                    turnover.compli-amt = turnover.compli-amt - h-bill-line.betrag. 
                    val-coup = val-coup - h-bill-line.betrag. 
                END. 
                
                turnover.r-transfer = turnover.r-transfer - h-bill-line.betrag. 
                IF h-artikel.artart = 11 THEN turnover.info = "Comp". 
                ELSE IF h-artikel.artart = 12 THEN turnover.info = "Cpon". 
                tot-trans = tot-trans - h-bill-line.betrag. 

            END.
            ELSE
            DO: 
                /*IF compli-flag THEN . /*william 556A23 25/01/24*/ /* Naufal Afthar - 129749 -> comment to include complimnent*/
                ELSE
                DO:*/
                    IF h-artikel.artart EQ 0 THEN /* sales articles */ 
                    DO:
                        FIND FIRST artikel WHERE artikel.departement EQ curr-dept 
                            AND artikel.artnr EQ h-artikel.artnrfront NO-LOCK NO-ERROR.
                    END.                     
                    ELSE /* city ledger */ 
                    DO:
                        FIND FIRST artikel WHERE artikel.departement EQ 0 
                            AND artikel.artnr EQ h-artikel.artnrfront NO-ERROR.
                    END.
                    
                    IF h-artikel.artart EQ 0 THEN    /* turnover articles */ 
                    DO:
                        /*service = 0. 
                        vat = 0. 
                        FIND FIRST htparam WHERE htparam.paramnr EQ h-artikel.service-code NO-LOCK NO-ERROR. 
                        IF AVAILABLE htparam THEN service = 0.01 * htparam.fdecimal. 
                    
                        FIND FIRST htparam WHERE htparam.paramnr EQ h-artikel.mwst-code NO-LOCK NO-ERROR. 
                        IF AVAILABLE htparam THEN vat = 0.01 * htparam.fdecimal * (1 + service). */

                        /*start bernatd E3673E*/
                        service = 0. 
                        vat = 0. 
                        vat2 = 0.
                        RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
                                        h-bill-line.bill-datum, OUTPUT service, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
                        
                        netto = h-bill-line.betrag / (1 + vat + vat2 + service). 
                        /*end bernatd E3673E*/

                        /* Naufal Afthar - 129749*/
                        IF NOT compli-flag THEN
                        DO:
                            turnover.t-service = turnover.t-service + netto * service. 
                            turnover.t-tax = turnover.t-tax + netto * vat. 
                            turnover.t-debit = turnover.t-debit + h-bill-line.betrag.
                            tot-serv = tot-serv + netto * service. 
                            tot-tax = tot-tax + netto * vat. 
                            tot-debit = tot-debit + h-bill-line.betrag.
                        END.
                        ELSE
                        DO:
                            turnover.r-transfer = turnover.r-transfer - netto * service - netto * vat.
                            tot-trans = tot-trans -  netto * service - netto * vat.
                            turnover.t-debit = turnover.t-debit + netto.
                            tot-debit = tot-debit + netto.
                        END.
                        /* end Naufal Afthar*/

                        IF h-bill-line.fremdwbetrag NE 0 THEN 
                            exchg-rate = h-bill-line.betrag / h-bill-line.fremdwbetrag. 
                    
                        IF artikel.artnr EQ artnr-list[1] THEN 
                        DO: 
                            turnover.food = turnover.food + netto. 
                            tot-food = tot-food + netto. 
                        END. 
                        ELSE IF artikel.artnr EQ artnr-list[2] THEN 
                        DO: 
                            turnover.beverage = turnover.beverage + netto. 
                            tot-beverage = tot-beverage + netto. 
                        END. 
                        ELSE IF artikel.artnr EQ artnr-list[3] THEN 
                        DO: 
                            turnover.misc = turnover.misc + netto. 
                            tot-misc = tot-misc + netto. 
                        END. 
                        ELSE IF artikel.artnr EQ artnr-list[4] THEN 
                        DO: 
                            turnover.cigarette = turnover.cigarette + netto. 
                            tot-cigar = tot-cigar + netto. 
                        END. 
                        ELSE IF artikel.artnr EQ artnr-list[5] THEN 
                        DO: 
                            turnover.discount = turnover.discount + netto. 
                            tot-disc = tot-disc + netto. 
                        END.
                    END.
                    ELSE IF h-artikel.artart EQ 6 THEN   /* cash */
                    DO:
                        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
                            AND artikel.departement = 0 NO-LOCK. 
                    
                        FIND FIRST pay-list WHERE pay-list.flag EQ 1 NO-ERROR. 
                        IF NOT AVAILABLE pay-list THEN 
                        DO: 
                            CREATE pay-list. 
                            pay-list.flag = 1. 
                            pay-list.bezeich = "Cash". 
                        END. 
                    
                        IF artikel.pricetab THEN 
                        DO: 
                            pay-list.foreign = pay-list.foreign - h-bill-line.fremdwbetrag. 
                            t-foreign = t-foreign - h-bill-line.fremdwbetrag. 
                        END. 
                        ELSE 
                        DO: 
                            pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 
                            t-betrag = t-betrag - h-bill-line.betrag. 
                        END. 
                    
                        IF artikel.pricetab THEN 
                        DO: 
                            turnover.p-cash1 = turnover.p-cash1 - h-bill-line.fremdwbetrag. 
                            tot-cash1 = tot-cash1 - h-bill-line.fremdwbetrag. 
                        END. 
                        ELSE 
                        DO: 
                            turnover.p-cash = turnover.p-cash - h-bill-line.betrag. 
                            tot-cash = tot-cash - h-bill-line.betrag. 
                        END. 
                    
                        turnover.t-credit = turnover.t-credit - h-bill-line.betrag.
                    END.
                    ELSE IF h-artikel.artart EQ 7 OR h-artikel.artart EQ 2 THEN   /* city ledger */
                    DO:
                        IF h-artikel.artart EQ 7 THEN 
                        DO: 
                            FIND FIRST pay-list WHERE pay-list.flag EQ 3 NO-ERROR. 
                            IF NOT AVAILABLE pay-list THEN 
                            DO: 
                                CREATE pay-list. 
                                pay-list.flag = 3. 
                                pay-list.bezeich = "Credit Card". 
                            END. 
                        END. 
                        ELSE IF h-artikel.artart EQ 2 THEN 
                        DO: 
                            FIND FIRST pay-list WHERE pay-list.flag EQ 5 NO-ERROR. 
                            IF NOT AVAILABLE pay-list THEN 
                            DO: 
                                CREATE pay-list. 
                                pay-list.flag = 5. 
                                pay-list.bezeich = "City- & Employee Ledger". 
                            END. 
                        END. 
                    
                        pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 
                        t-betrag = t-betrag - h-bill-line.betrag. 
                        turnover.c-ledger = turnover.c-ledger - h-bill-line.betrag. 
                        turnover.t-credit = turnover.t-credit - h-bill-line.betrag. 
                        tot-ledger = tot-ledger - h-bill-line.betrag.
                    END.
                /*END.*/
            END.
        END.
    END.
END PROCEDURE.
 

DEFINE TEMP-TABLE cash-art
    FIELD sortnr        AS INTEGER
    FIELD usrnr         LIKE bediener.nr
    FIELD usrnm         LIKE bediener.username
    FIELD artnr         LIKE artikel.artnr
    FIELD bezeich       LIKE artikel.bezeich
    FIELD amount        AS DECIMAL FORMAT "->>>,>>>,>>9.99".

DEFINE TEMP-TABLE bline-list 
  FIELD selected AS LOGICAL INITIAL NO
  FIELD NAME     LIKE kellner.kellnername
  FIELD depart   AS CHAR 
  FIELD dept     AS INTEGER 
  FIELD knr      AS INTEGER 
  FIELD bl-recid AS INTEGER. 

DEFINE TEMP-TABLE outstand-list 
  FIELD name    AS CHAR FORMAT "x(16)" 
  FIELD rechnr  AS INTEGER FORMAT " >,>>>,>>9" 
  FIELD foreign AS DECIMAL FORMAT "->>>,>>9.99" 
  FIELD saldo   AS DECIMAL FORMAT "->>,>>>,>>9.99". 

DEFINE TEMP-TABLE pay-list 
  FIELD compli  AS LOGICAL INITIAL no 
  FIELD person  AS INTEGER 
  FIELD flag    AS INTEGER /* 1 cash  2 room  3 CC  4 EL  5 CL  6 Comp  */ 
  FIELD bezeich AS CHAR FORMAT "x(24)" 
  FIELD artnr   AS INTEGER FORMAT ">>>>9 " 
  FIELD rechnr  AS INTEGER FORMAT ">>>>>>9 " 
  FIELD foreign AS DECIMAL FORMAT "->>>,>>9.99" 
  FIELD saldo   AS DECIMAL FORMAT "->>,>>>,>>9.99". 

DEFINE TEMP-TABLE turnover 
  FIELD departement     LIKE h-bill.departement 
  FIELD deptname        LIKE hoteldpt.depart
  FIELD kellner-nr      LIKE h-bill.kellner-nr 
  FIELD name            LIKE kellner.kellnername 
  FIELD tischnr         LIKE h-bill.tischnr         COLUMN-LABEL "Tbl" 
  FIELD rechnr          AS CHAR FORMAT "x(16)"      COLUMN-LABEL "Bill-No" 
  FIELD belegung        AS INTEGER FORMAT "->>9"    COLUMN-LABEL "Pax" 
  FIELD artnr           LIKE h-bill-line.artnr 
  FIELD info            AS CHAR    FORMAT "x(48)"           LABEL "Info" 
  FIELD t-debit         AS DECIMAL FORMAT "->>,>>>,>>9"     label "Total" 
  FIELD t-credit        AS DECIMAL FORMAT "->>,>>>,>>9"  
  FIELD p-cash          AS DECIMAL FORMAT "->>>,>>>,>>9.99"  
  FIELD p-cash1         AS DECIMAL FORMAT "->>>,>>>,>>9.99"         /*ger 59EED2 before >,>>9.99*/
  FIELD r-transfer      AS DECIMAL FORMAT "->>>,>>>,>>9.99" LABEL "Transfer" 
  FIELD c-ledger        AS DECIMAL FORMAT "->>>,>>>,>>9.99" LABEL "CreditCard / CL"
  FIELD compli          AS LOGICAL INITIAL NO COLUMN-LABEL "Comp" FORMAT "Yes/No"
  FIELD flag            AS INTEGER INITIAL 0
  FIELD coupon          AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" LABEL "Coupon"
  FIELD comp            AS DECIMAL FORMAT "->>>,>>>,>>9.99" LABEL "Compliment"
  FIELD gname           AS CHAR FORMAT "x(16)" COLUMN-LABEL "Guest Name".

DEFINE VARIABLE tot-debit       AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
/*DEFINE VARIABLE tot-cash1       AS DECIMAL FORMAT "->,>>9.99".*/ /*william*/
DEFINE VARIABLE tot-cover       AS INTEGER FORMAT ">>>9". 
DEFINE VARIABLE nt-debit        AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
/*DEFINE VARIABLE nt-cash1        AS DECIMAL FORMAT "->,>>9.99".*/ /*william*/ 
DEFINE VARIABLE nt-cover        AS INTEGER FORMAT ">>>9". 

DEFINE VARIABLE t-debit         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 
DEFINE VARIABLE t-cash          AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 
DEFINE VARIABLE t-cash1         AS DECIMAL FORMAT "->,>>9.99". 
DEFINE VARIABLE t-trans         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 
DEFINE VARIABLE t-ledger        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 
DEFINE VARIABLE t-coupon        AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE t-compli        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 
DEFINE VARIABLE t-cover         AS INTEGER FORMAT ">>>9". 

DEFINE VARIABLE anz-comp        AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE val-comp        AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE anz-coup        AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE val-coup        AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE serv-taxable    AS LOGICAL INITIAL NO. 

DEFINE BUFFER bufparam FOR htparam.
FIND FIRST bufparam WHERE bufparam.paramnr = 1001 NO-LOCK NO-ERROR.

DEF INPUT PARAMETER TABLE FOR bline-list.
DEF INPUT PARAMETER shift AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER exchg-rate AS DECIMAL.
DEF OUTPUT PARAMETER tot-cash        AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEF OUTPUT PARAMETER tot-cash1       AS DECIMAL FORMAT "->>>,>>>,>>9.99". /*william*/
DEF OUTPUT PARAMETER tot-ledger      AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER tot-trans       AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER tot-compli      AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER tot-coupon      AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER nt-cash         AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEF OUTPUT PARAMETER nt-cash1        AS DECIMAL FORMAT "->>>,>>>,>>9.99". /*william*/
DEF OUTPUT PARAMETER nt-ledger       AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER nt-trans        AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER nt-compli       AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER nt-coupon       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER t-betrag        AS DECIMAL  FORMAT "->>,>>>,>>9.99". 
DEF OUTPUT PARAMETER t-foreign       AS DECIMAL  FORMAT "->>>,>>9.99". 
DEF OUTPUT PARAMETER TABLE FOR turnover.

RUN daysale-list.

procedure daysale-list: 
DEFINE VARIABLE curr-s      AS INTEGER. 
DEFINE VARIABLE billnr      AS INTEGER. 
DEFINE VARIABLE dept        AS INTEGER FORMAT ">>9" INITIAL 1. 
DEFINE VARIABLE d-name      AS CHARACTER FORMAT "x(24)". 
DEFINE VARIABLE usr-nr      AS INTEGER. 
DEFINE VARIABLE d-found     AS LOGICAL INITIAL "no". 
DEFINE VARIABLE c-found     AS LOGICAL INITIAL "no". 
DEFINE VARIABLE vat         AS DECIMAL. 
DEFINE VARIABLE service     AS DECIMAL. 
DEFINE VARIABLE netto       AS DECIMAL. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE found       AS LOGICAL INITIAL no. 
DEFINE VARIABLE compli      AS LOGICAL.  
DEFINE VARIABLE guestname   AS CHAR. 
DEFINE VARIABLE bill-no     AS INTEGER.
DEFINE VARIABLE pos         AS INTEGER.
DEFINE BUFFER kellner1 FOR kellner. 
DEF BUFFER tlist FOR turnover.
DEF BUFFER h-bline FOR h-bill-line.

  FOR EACH turnover: 
    delete turnover. 
  END. 
  FOR EACH pay-list: 
    delete pay-list. 
  END. 
  FOR EACH outstand-list: 
    delete outstand-list. 
  END. 
 
  t-betrag = 0. 
  t-foreign = 0. 
 
  ASSIGN
      tot-cover = 0
      tot-debit = 0
      tot-cash1 = 0
      tot-cash  = 0
      tot-trans = 0
      tot-ledger = 0
      tot-compli = 0
      tot-coupon = 0
      nt-cover  = 0
      nt-debit  = 0
      nt-cash1  = 0
      nt-cash   = 0
      nt-trans  = 0
      nt-compli = 0
      nt-coupon = 0.


  FOR EACH bline-list WHERE bline-list.selected = yes, 
    first kellner WHERE recid(kellner) = bline-list.bl-recid 
    /*AND kellner.departement = curr-dept*/
    by kellner.departement by kellner.kellnername: 
    
    t-cover     = 0. 
    t-debit     = 0. 
    t-cash1     = 0. 
    t-cash      = 0. 
    t-trans     = 0. 
    t-ledger    = 0. 
    t-compli    = 0.
    t-coupon    = 0.
                
    FOR EACH h-bill WHERE h-bill.flag EQ 0 and h-bill.saldo NE 0 
      and h-bill.departement = bline-list.dept  
  /*  and h-bill.kellner-nr = kellner.kellner-nr */  
      NO-LOCK use-index dept1_ix by h-bill.rechnr: 
      CREATE outstand-list. 
      FIND FIRST kellner1 WHERE kellner1.kellner-nr = h-bill.kellner-nr 
        and kellner1.departement = h-bill.departement NO-LOCK NO-ERROR. 
      outstand-list.rechnr = h-bill.rechnr. 
      IF AVAILABLE kellner1 THEN  
        outstand-list.name = kellner1.kellnername. 
      ELSE outstand-list.name = string(h-bill.kellner-nr). 
      FOR EACH h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
        and h-bill-line.departement = /*curr-dept*/ bline-list.dept NO-LOCK: 
        outstand-list.saldo = outstand-list.saldo + h-bill-line.betrag. 
        outstand-list.foreign = outstand-list.foreign  
          + h-bill-line.fremdwbetrag. 
      END. 
    END. 
             
    FOR EACH h-bill WHERE h-bill.flag EQ 1 
      and h-bill.departement = bline-list.dept  
      and h-bill.kellner-nr = kellner.kellner-nr  
      NO-LOCK use-index dept1_ix by h-bill.rechnr: 
      
      IF shift = 0 THEN
        FIND FIRST h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
        AND h-bill-line.bill-datum = from-date  
        AND /*h-bill-line.departement = curr-dept*/ 
          h-bill-line.departement = bline-list.dept NO-LOCK NO-ERROR. 
      ELSE
        FIND first h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
        AND h-bill-line.bill-datum = from-date  
        AND h-bill-line.departement = bline-list.dept
        /*AND h-bill-line.departement = curr-dept*/
        AND h-bill-line.betriebsnr = shift NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE h-bill-line THEN found = NO.
      ELSE found = YES.
      DO WHILE AVAILABLE h-bill-line:  
          found = YES.
        FIND FIRST turnover WHERE turnover.departement = /*curr-dept*/ 
          bline-list.dept AND 
          turnover.kellner-nr = kellner.kellner-nr AND 
          turnover.rechnr = STRING(h-bill.rechnr) NO-ERROR. 
        IF NOT AVAILABLE turnover THEN 
        DO:            
          pos = 0.
          bill-no = 0.
          guestname = "".
          IF shift = 0 THEN
            FIND FIRST h-bline WHERE h-bline.rechnr = h-bill.rechnr 
            AND h-bline.bill-datum = from-date  
            /*AND h-bline.departement = curr-dept */
            AND h-bline.departement = bline-list.dept
            AND h-bline.artnr = 0 NO-LOCK NO-ERROR. 
          ELSE
            FIND first h-bline WHERE h-bline.rechnr = h-bill.rechnr 
            AND h-bline.bill-datum = from-date  
            /*AND h-bline.departement = curr-dept*/
            AND h-bline.departement = bline-list.dept
            AND h-bline.betriebsnr = shift 
            AND h-bline.artnr = 0 NO-LOCK NO-ERROR. 
          IF AVAILABLE h-bline THEN
          DO: 
              pos = INDEX( h-bline.bezeich, "*").
              IF pos NE 0 THEN
                  bill-no = INTEGER(SUBSTR(h-bline.bezeich, pos,
                                           (LENGTH(h-bline.bezeich) - pos + 1))).
              IF bill-no NE 0 THEN
              DO:
                  FIND FIRST bill WHERE bill.rechnr = bill-no NO-LOCK NO-ERROR.
                  IF AVAILABLE bill THEN
                  DO:
                      FIND FIRST res-line WHERE res-line.resnr = bill.resnr AND 
                          res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
                      IF AVAILABLE res-line THEN
                          guestname = res-line.NAME.
                  END.
              END.
          END.
          CREATE turnover. 
          turnover.departement = kellner.departement. 
          turnover.deptname   = bline-list.depart.
          turnover.kellner-nr = kellner.kellner-nr. 
          turnover.name = kellner.kellnername. 
          turnover.tischnr = h-bill.tischnr. 
          turnover.belegung = h-bill.belegung. 
          turnover.rechnr = string(h-bill.rechnr).
          turnover.gname = guestname.
          tot-cover = tot-cover + h-bill.belegung. 
          t-cover = t-cover + h-bill.belegung. 
        END. 
        
        IF h-bill-line.artnr = 0 THEN    /* room or bill transfer */ 
        DO:                       
          turnover.r-transfer = turnover.r-transfer - h-bill-line.betrag. 
          turnover.compli = NO.
          
          FIND FIRST pay-list WHERE pay-list.flag = 2 NO-ERROR. 
          IF not AVAILABLE pay-list THEN 
          DO: 
            CREATE pay-list. 
            pay-list.flag = 2. 
            pay-list.bezeich = "Room / Bill Transfer". 
          END. 
          pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 
          t-betrag = t-betrag - h-bill-line.betrag.  
          i = 0. 
         
          /* FDL Comment => Can not responding server if generate many bills
          found = no. 
          do while not found: 
            i = i + 1. 
            IF substr(h-bill-line.bezeich, i, 1) = "*" THEN found = yes. 
          END. 
          */                    
          /*
          billnr = INTEGER(substr(h-bill-line.bezeich, i + 1,  
            length(h-bill-line.bezeich) - i)).
          */  
          /*FDL June 06, 2023 - Ticket E782C4*/
          IF h-bill-line.bezeich MATCHES "*RmNo*" THEN
          DO:
              IF NUM-ENTRIES(h-bill-line.bezeich,"*") GT 1 THEN
              DO:
                  billnr = INT(ENTRY(2,h-bill-line.bezeich,"*")).
              END.
          END.

          FIND FIRST bill WHERE bill.rechnr = billnr NO-LOCK NO-ERROR.           
          IF AVAILABLE bill THEN turnover.info = bill.zinr. 

          turnover.t-credit = turnover.t-credit - h-bill-line.betrag. 
          t-trans = t-trans - h-bill-line.betrag. 
          tot-trans = tot-trans - h-bill-line.betrag.           
        END. 
        ELSE 
        DO:    /* i.e h-bill-line.artnr NE 0  */                
          FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr 
            AND h-artikel.departement = /*curr-dept*/ bline-list.dept NO-LOCK NO-ERROR. 
          IF AVAILABLE h-artikel THEN
          DO:                       
            IF h-artikel.artart = 11 or h-artikel.artart = 12 THEN  /* complimentary or meal coupon */       
            DO:                     
              IF h-artikel.artart = 11 THEN 
              DO:                        
                FIND FIRST pay-list WHERE pay-list.flag = 6 NO-ERROR. 
                IF not AVAILABLE pay-list THEN 
                DO: 
                  CREATE pay-list. 
                  pay-list.flag = 6. 
                  pay-list.compli = yes. 
                  pay-list.bezeich = "Compliment". 
                END. 
                pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 
                IF h-bill-line.betrag LT 0 THEN 
                  pay-list.person = pay-list.person + h-bill.belegung. 
                ELSE IF h-bill-line.betrag GT 0 THEN 
                DO:
                  IF h-bill.belegung > 0 THEN
                      pay-list.person = pay-list.person - h-bill.belegung. 
                  ELSE pay-list.person = pay-list.person + h-bill.belegung. 
                END.
                t-betrag = t-betrag - h-bill-line.betrag. 
/*              t-foreign = t-foreign - h-bill-line.fremwbetrag. */
                t-compli = t-compli - h-bill-line.betrag.
                tot-compli = tot-compli - h-bill-line.betrag.
                anz-comp = anz-comp + 1. 
                val-comp = val-comp - h-bill-line.betrag. 
                turnover.comp = turnover.comp - h-bill-line.betrag.
              END. 
              ELSE IF h-artikel.artart = 12 THEN 
              DO:                              
                FIND FIRST pay-list WHERE pay-list.flag = 7  
                  and pay-list.bezeich = h-artikel.bezeich NO-ERROR. 
                IF not AVAILABLE pay-list THEN 
                DO: 
                  CREATE pay-list. 
                  pay-list.flag = 7. 
                  pay-list.compli = yes. 
                  pay-list.bezeich = h-artikel.bezeich. 
                END. 
/*              pay-list.foreign = pay-list.foreign - h-bill-line.fremdwbetrag. */ 
                pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 
                IF h-bill-line.betrag LT 0 THEN 
                  pay-list.person = pay-list.person + h-bill.belegung. 
                ELSE IF h-bill-line.betrag GT 0 THEN 
                DO:
                  IF h-bill.belegung > 0 THEN
                      pay-list.person = pay-list.person - h-bill.belegung. 
                  ELSE pay-list.person = pay-list.person + h-bill.belegung. 
                END.
            
                t-betrag = t-betrag - h-bill-line.betrag. 
/*              t-foreign = t-foreign - h-bill-line.fremwbetrag.  */ 
                t-coupon = t-coupon - h-bill-line.betrag.
                tot-coupon = tot-coupon - h-bill-line.betrag.
                anz-coup = anz-coup + 1. 
                val-coup = val-coup - h-bill-line.betrag. 
                turnover.coupon = turnover.coupon - h-bill-line.betrag.
              END. 
                          
              turnover.compli = NOT turnover.compli.
              turnover.info = h-bill.bilname. 
            END. 
            ELSE IF h-artikel.artart = 0 THEN /* sales articles */  
            DO:                    
              service = 0. 
              vat = 0.

              FIND FIRST artikel WHERE artikel.departement = /*curr-dept */ bline-list.dept
                AND artikel.artnr = h-artikel.artnrfront NO-LOCK NO-ERROR.              
              IF AVAILABLE artikel THEN DO: /*Eko 30 mar 2016 Error Not available artikel*/                  
                  FIND FIRST htparam WHERE  
                    paramnr = artikel.service-code NO-LOCK NO-ERROR. 
                  IF AVAILABLE htparam THEN service = 0.01 * htparam.fDECIMAL. 
                  FIND FIRST htparam WHERE  
                    paramnr = artikel.mwst-code NO-LOCK NO-ERROR. 
                  IF AVAILABLE htparam THEN  
                  DO: 
                    IF serv-taxable THEN 
                      vat = 0.01 * htparam.fDECIMAL * (1 + service). 
                    ELSE vat = 0.01 * htparam.fDECIMAL. 
                  END. 
              END.              
              
              netto = h-bill-line.betrag / (1 + vat + service). 
              IF h-bill-line.fremdwbetrag NE 0 THEN 
                exchg-rate = h-bill-line.betrag / h-bill-line.fremdwbetrag. 
              END.  
              IF h-artikel.artart = 6 THEN    /* cash */ 
              DO:                           
                FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
                  and artikel.departement = 0 NO-LOCK NO-ERROR. 
                IF AVAILABLE artikel THEN DO: /*Eko 30 mar 2016*/
                  FIND FIRST pay-list WHERE pay-list.flag = 1 
                       AND pay-list.bezeich = artikel.bezeich NO-ERROR. 
                  IF not AVAILABLE pay-list THEN 
                  DO: 
                    CREATE pay-list. 
                    pay-list.flag = 1. 
                    pay-list.bezeich = artikel.bezeich. 
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
            
                  IF h-artikel.artnr = bufparam.finteger THEN  
                  DO: 
                    turnover.p-cash1 = turnover.p-cash1 - h-bill-line.betrag. /*william change fremdwbetrag to betrag 2438D5*/ 
                    t-cash1 = t-cash1 - h-bill-line.betrag. /*william change fremdwbetrag to betrag 2438D5*/ 
                    tot-cash1 = tot-cash1 - h-bill-line.betrag. /*william change fremdwbetrag to betrag 2438D5*/ 
                  END. 
                  ELSE  
                  DO:                     
                    turnover.p-cash = turnover.p-cash - h-bill-line.betrag. 
                    t-cash = t-cash - h-bill-line.betrag. 
                    tot-cash = tot-cash - h-bill-line.betrag.                     
                  END. 
                  turnover.t-credit = turnover.t-credit - h-bill-line.betrag. 
                  FIND FIRST cash-art WHERE cash-art.artnr = artikel.artnr
                        AND cash-art.usrnr = kellner.kellner-nr NO-ERROR.
                    IF NOT AVAILABLE cash-art THEN
                    DO:
                        CREATE cash-art.
                        ASSIGN cash-art.artnr = artikel.artnr
                            cash-art.usrnr    = kellner.kellner-nr
                            cash-art.usrnm    = kellner.kellnername
                            cash-art.bezeich  = artikel.bezeich.
                    END.
                    cash-art.amount = cash-art.amount - h-bill-line.betrag.
                END.                
              END.
            
              /*wen*/
              IF h-artikel.artart = 6 AND h-artikel.artart = 7 THEN    /* cash */ 
              DO: 
                FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
                  and artikel.departement = 0 NO-LOCK NO-ERROR. 
                IF AVAILABLE artikel THEN DO: /*Eko 30 mar 2016*/
                  FIND FIRST pay-list WHERE pay-list.flag = 1 
                       AND pay-list.bezeich = artikel.bezeich NO-ERROR. 
                  IF not AVAILABLE pay-list THEN 
                  DO: 
                    CREATE pay-list. 
                    pay-list.flag = 1 . 
                    pay-list.bezeich = artikel.bezeich. 
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
            
                  IF h-artikel.artnr = bufparam.finteger THEN  
                  DO: 
                    turnover.p-cash1 = turnover.p-cash1 - h-bill-line.betrag. /*william change fremdwbetrag to betrag 2438D5*/ 
                    t-cash1 = t-cash1 - h-bill-line.betrag. /*william change fremdwbetrag to betrag 2438D5*/ 
                    tot-cash1 = tot-cash1 - h-bill-line.betrag. /*william change fremdwbetrag to betrag 2438D5*/ 
                  END. 
                  ELSE  
                  DO: 
                    turnover.p-cash = turnover.p-cash - h-bill-line.betrag. 
                    t-cash = t-cash - h-bill-line.betrag. 
                    tot-cash = tot-cash - h-bill-line.betrag. 
                  END. 
                  turnover.t-credit = turnover.t-credit - h-bill-line.betrag. 
                  FIND FIRST cash-art WHERE cash-art.artnr = artikel.artnr
                        AND cash-art.usrnr = kellner.kellner-nr NO-ERROR.
                    IF NOT AVAILABLE cash-art THEN
                    DO:
                        CREATE cash-art.
                        ASSIGN cash-art.artnr = artikel.artnr
                            cash-art.usrnr    = kellner.kellner-nr
                            cash-art.usrnm    = kellner.kellnername
                            cash-art.bezeich  = artikel.bezeich.
                    END.
                    cash-art.amount = cash-art.amount - h-bill-line.betrag.
                END.
              END.
            
              ELSE IF h-artikel.artart = 7  /* credit card */ 
              or      h-artikel.artart = 2  /* city ledger */  THEN 
              DO: 
                FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
                  and artikel.departement = 0 NO-LOCK NO-ERROR.  /*FD September 08, 2021*/
                IF AVAILABLE artikel THEN
                DO:
                  IF h-artikel.artart = 7 THEN 
                  DO:                               
                    FIND FIRST pay-list WHERE pay-list.flag = 3 NO-ERROR. 
                    IF not AVAILABLE pay-list THEN 
                    DO: 
                      CREATE pay-list. 
                      pay-list.flag = 3. 
                      pay-list.bezeich = "Credit Card". 
                    END.                                                                                         
                  END. 
                  ELSE IF h-artikel.artart = 2 THEN 
                  DO: 
                    FIND FIRST pay-list WHERE pay-list.flag = 5 NO-ERROR. 
                    IF not AVAILABLE pay-list THEN 
                    DO: 
                      CREATE pay-list. 
                      pay-list.flag = 5. 
                      pay-list.bezeich = "City- & Employee Ledger". 
                    END.                                       
                  END. 
              
/*                pay-list.foreign = pay-list.foreign - h-bill-line.fremdwbetrag. */ 
                   pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 
                   t-betrag = t-betrag - h-bill-line.betrag. 
/*                t-foreign = t-foreign - h-bill-line.fremwbetrag.  */ 
            
                  IF LENGTH(h-bill-line.bezeich) GT LENGTH(h-artikel.bezeich) THEN
                     turnover.info = SUBSTR(h-bill-line.bezeich, (LENGTH(h-artikel.bezeich) + 1),
                                               (LENGTH(h-bill-line.bezeich) - LENGTH(h-artikel.bezeich))). 
                  ELSE
                  turnover.INFO      = h-bill.bilname.
                  turnover.artnr     = artikel.artnr. 
                  turnover.c-ledger  = turnover.c-ledger - h-bill-line.betrag. 
                  turnover.t-credit  = turnover.t-credit - h-bill-line.betrag. 
                  t-ledger           = t-ledger - h-bill-line.betrag. 
                  tot-ledger         = tot-ledger - h-bill-line.betrag. 
                END.                
            END. 
          END.          
        END.  

        IF shift = 0 THEN
          FIND NEXT h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
          AND h-bill-line.bill-datum = from-date  
          /*AND h-bill-line.departement = curr-dept*/
            AND h-bill-line.departement = bline-list.dept NO-LOCK NO-ERROR. 
        ELSE
          FIND NEXT h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
          AND h-bill-line.bill-datum = from-date  
          /*AND h-bill-line.departement = curr-dept*/
           AND h-bill-line.departement = bline-list.dept
          AND h-bill-line.betriebsnr = shift NO-LOCK NO-ERROR. 
      END. /*do while*/
    END. /*each h-bill*/
    FIND FIRST tlist WHERE tlist.NAME = kellner.kellnername 
        AND tlist.departement = bline-list.dept NO-LOCK NO-ERROR.
    IF AVAILABLE tlist THEN
    DO:
        CREATE turnover. 
        turnover.departement = bline-list.dept.
        turnover.deptname    = bline-list.depart.
        turnover.name        = kellner.kellnername. 
        turnover.rechnr      = kellner.kellnername + " TOTAL". 
        turnover.belegung    =  t-cover. 
        turnover.t-debit     = t-debit. 
        turnover.p-cash      = t-cash.  
        turnover.p-cash1     = t-cash1.  
        turnover.r-transfer  = t-trans. 
        turnover.c-ledger    = t-ledger.  
        turnover.comp        = t-compli.
        turnover.coupon      = t-coupon.
        turnover.flag        = 1.
    END.
  END. /*each bline-list*/
  CREATE turnover. 
  turnover.rechnr           = "G-TOTAL". 
  turnover.NAME             = "ZZZ".
  turnover.belegung         =  tot-cover. 
  turnover.t-debit          = tot-debit. 
  turnover.p-cash           = tot-cash.  
  turnover.p-cash1          = tot-cash1.  
  turnover.r-transfer       = tot-trans. 
  turnover.c-ledger         = tot-ledger.  
  turnover.comp             = tot-compli.
  turnover.coupon           = tot-coupon.
  turnover.flag             = 2.
 
  CREATE turnover. 
  turnover.NAME   = "ZZZ".
  turnover.rechnr = "R-TOTAL".
  turnover.flag = 3.
  
  FOR EACH tlist WHERE tlist.flag = 0:
      turnover.belegung     = turnover.belegung + tlist.belegung. 
      turnover.comp         = turnover.comp + tlist.comp.
      turnover.coupon       = turnover.coupon + tlist.coupon.
      turnover.t-debit      = turnover.t-debit + tlist.t-debit. 
      turnover.p-cash       = turnover.p-cash + tlist.p-cash.  
      turnover.p-cash1      = turnover.p-cash1 + tlist.p-cash1.  
      turnover.r-transfer   = turnover.r-transfer + tlist.r-transfer. 
      turnover.c-ledger     = turnover.c-ledger + tlist.c-ledger.  
  END.

  nt-cover  = turnover.belegung.
  nt-compli = turnover.comp.
  nt-coupon = turnover.coupon.
  nt-debit  = turnover.t-debit.
  nt-cash   = turnover.p-cash.
  nt-cash1  = turnover.p-cash1.
  nt-trans  = turnover.r-transfer.
  nt-ledger = turnover.c-ledger.
END.  

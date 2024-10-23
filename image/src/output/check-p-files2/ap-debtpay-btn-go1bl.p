DEFINE TEMP-TABLE age-list 
    FIELD selected        AS LOGICAL INITIAL NO 
    FIELD ap-recid        AS INTEGER 
    FIELD counter         AS INTEGER 
    FIELD docu-nr         AS CHAR FORMAT "x(10)" 
    FIELD rechnr          AS INTEGER 
    FIELD lief-nr         AS INTEGER 
    FIELD lscheinnr       AS CHAR FORMAT "x(23)" 
    FIELD supplier        AS CHAR FORMAT "x(24)" 
    FIELD rgdatum         AS DATE 
    FIELD rabatt          AS DECIMAL FORMAT ">9.99" 
    FIELD rabattbetrag    AS DECIMAL FORMAT "->,>>>,>>9.99" 
    FIELD ziel            AS DATE 
    FIELD netto           AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
    FIELD user-init       AS CHAR FORMAT "x(2)" 
    FIELD debt            AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0 
    FIELD credit          AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0 
    FIELD bemerk          AS CHAR 
    FIELD tot-debt        AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0
    FIELD rec-id          AS INT
    FIELD resname         AS CHAR
    FIELD comments        AS CHAR
    /*gerald 210920 Tauzia LnL*/   
    FIELD fibukonto       LIKE gl-journal.fibukonto     
    FIELD t-bezeich       LIKE gl-acct.bezeich          
    FIELD debt2           AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0
    FIELD recv-date       AS DATE
    .

DEFINE TEMP-TABLE t-l-lieferant 
    FIELD telefon   LIKE l-lieferant.telefon
    FIELD fax       LIKE l-lieferant.fax
    FIELD adresse1  LIKE l-lieferant.adresse1
    FIELD notizen-1 AS CHAR
    FIELD lief-nr   LIKE l-lieferant.lief-nr
    .

DEF INPUT-OUTPUT PARAMETER art-selected AS INT.
DEF INPUT  PARAMETER bill-name AS CHAR.
DEF INPUT  PARAMETER bill-date AS DATE.
DEF OUTPUT PARAMETER outstand AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR age-list.
DEF OUTPUT PARAMETER TABLE FOR t-l-lieferant.

IF bill-name = "" THEN RUN create-age-list. 
ELSE RUN create-age-list1.

FOR EACH age-list NO-LOCK:
    FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = age-list.lief-nr 
        NO-LOCK NO-ERROR.
    IF AVAILABLE l-lieferant THEN
    DO: 
        FIND FIRST t-l-lieferant WHERE t-l-lieferant.lief-nr = l-lieferant.lief-nr
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-l-lieferant THEN
        DO:
            CREATE t-l-lieferant.
            ASSIGN
                t-l-lieferant.telefon       = l-lieferant.telefon
                t-l-lieferant.fax           = l-lieferant.fax
                t-l-lieferant.adresse1      = l-lieferant.adresse1
                t-l-lieferant.notizen-1     = l-lieferant.notizen[1]
                t-l-lieferant.lief-nr       = l-lieferant.lief-nr.
        END.
    END.
END.

PROCEDURE create-age-list: 
DEFINE buffer artikel1      FOR artikel. 
DEFINE VARIABLE curr-rechnr AS INTEGER. 
DEFINE VARIABLE curr-saldo  AS DECIMAL. 
DEFINE VARIABLE opart       AS INTEGER INITIAL 1. 
DEFINE VARIABLE create-it   AS LOGICAL. 
  
    DO: 
      FOR EACH age-list: 
        delete age-list. 
      END. 
      curr-rechnr = 0. 
     
      outstand = 0. 
      
      FOR EACH l-kredit WHERE 
        l-kredit.rgdatum LE bill-date AND l-kredit.opart LT 2 
        AND l-kredit.counter GE 0 
        /*and l-kredit.name GE bill-nr*/ NO-LOCK, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
        BY l-lieferant.firma BY l-kredit.counter 
        BY l-kredit.rgdatum BY l-kredit.zahlkonto: 
        create-it = NO. 
        IF l-kredit.counter = 0 THEN create-it = YES. 
        ELSE 
        DO: 
          FIND FIRST age-list WHERE age-list.counter = l-kredit.counter NO-ERROR. 
          IF NOT AVAILABLE age-list THEN create-it = YES. 
        END. 
        IF create-it THEN 
        DO: 
          create age-list. 
          age-list.counter   = l-kredit.counter. 
          age-list.docu-nr   = l-kredit.name.        /* PO number */ 
          age-list.rechnr    = l-kredit.rechnr. 
          age-list.lief-nr   = l-kredit.lief-nr. 
          age-list.supplier  = l-lieferant.firma + ", " + l-lieferant.anredefirma.
          age-list.rec-id    = RECID(l-kredit).
        END. 
        IF l-kredit.zahlkonto = 0 THEN 
        DO: 
          FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
              NO-LOCK NO-ERROR. 
          IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit. 
          age-list.ap-recid   = RECID(l-kredit). 
          age-list.rgdatum    = l-kredit.rgdatum. 
          age-list.debt       = l-kredit.saldo. 
          age-list.rabatt     = l-kredit.rabatt. 
          age-list.rabattbetrag = l-kredit.rabattbetrag. 
          age-list.netto      = l-kredit.netto. 
          age-list.ziel       = l-kredit.rgdatum + l-kredit.ziel. 
          age-list.lscheinnr  = l-kredit.lscheinnr. 
          age-list.bemerk     = l-kredit.bemerk. 
          age-list.tot-debt   = age-list.tot-debt + l-kredit.netto.
       
          FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.char1 = l-kredit.NAME NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
              ASSIGN
                  age-list.recv-date = queasy.date1.
          END.
        END. 
        ELSE 
        DO: 
          age-list.credit   = age-list.credit - l-kredit.saldo. 
          age-list.tot-debt = age-list.tot-debt + l-kredit.saldo. 
        END. 
       
        RUN disp-l-lieferant-debt.
       
        FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno = l-kredit.NAME NO-LOCK NO-ERROR.
        IF AVAILABLE gl-jouhdr THEN
        DO:
          FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr NO-LOCK,
              EACH gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto
              AND (gl-acct.acc-type = 2  OR gl-acct.acc-type = 3 OR gl-acct.acc-type = 5):
              age-list.comment = age-list.comment + ";" + 
                                 string(gl-journal.fibukonto) + ";" + string(l-kredit.steuercode).
              /*gerald 210920 Tauzia LnL*/   
              age-list.fibukonto = gl-journal.fibukonto.
              age-list.t-bezeich = gl-acct.bezeich.
       
              IF gl-journal.debit GT 0 THEN
              DO:
                age-list.debt2     = gl-journal.debit.
              END.
              ELSE IF gl-journal.credit GT 0 THEN
              DO:
                age-list.debt2    = -(gl-journal.credit).
              END.
              /*end gerald*/
          END.
        END.
      END.  
      art-selected = 1. 
    END. 
END.     

PROCEDURE create-age-list1: 
DEFINE buffer artikel1 FOR artikel. 
DEFINE VARIABLE curr-rechnr AS INTEGER. 
DEFINE VARIABLE curr-saldo AS DECIMAL. 
DEFINE VARIABLE opart AS INTEGER INITIAL 1. 
DEFINE VARIABLE create-it AS LOGICAL. 
    
    DO: 
        FOR EACH age-list: 
          delete age-list. 
        END. 
        curr-rechnr = 0. 
        outstand = 0. 
        FIND FIRST l-lieferant WHERE l-lieferant.firma = bill-name NO-LOCK NO-ERROR. 
        IF AVAILABLE l-lieferant THEN 
        FOR EACH l-kredit WHERE 
            l-kredit.rgdatum LE bill-date AND l-kredit.opart LT 2 
            AND l-kredit.lief-nr = l-lieferant.lief-nr NO-LOCK 
            BY l-kredit.counter BY l-kredit.rgdatum BY l-kredit.zahlkonto: 
            create-it = NO. 
            IF l-kredit.counter = 0 THEN create-it = YES. 
            ELSE 
            DO: 
                FIND FIRST age-list WHERE age-list.counter = l-kredit.counter NO-ERROR. 
                IF NOT AVAILABLE age-list THEN create-it = YES. 
            END. 
            IF create-it THEN 
            DO: 
                create age-list. 
                age-list.counter   = l-kredit.counter. 
                age-list.docu-nr   = l-kredit.name. 
                age-list.rechnr    = l-kredit.rechnr. 
                age-list.lief-nr   = l-kredit.lief-nr. 
                age-list.supplier  = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
                age-list.rec-id    = RECID(l-kredit).
            END. 
            IF l-kredit.zahlkonto = 0 THEN 
            DO: 
                FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
                  NO-LOCK NO-ERROR. 
                IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit. 
                ASSIGN
                    age-list.ap-recid   = RECID(l-kredit)
                    age-list.rgdatum    = l-kredit.rgdatum 
                    age-list.debt       = l-kredit.saldo 
                    /* SY 30/14/14
                    age-list.rabatt = l-kredit.rabatt
                    age-list.rabattbetrag = l-kredit.rabattbetrag*/        
                    age-list.netto      = l-kredit.netto
                    age-list.ziel       = l-kredit.rgdatum + l-kredit.ziel
                    age-list.lscheinnr  = l-kredit.lscheinnr 
                    age-list.bemerk     = l-kredit.bemerk 
                    age-list.tot-debt   = age-list.tot-debt + l-kredit.netto
                .
                IF l-kredit.NAME NE l-kredit.lscheinnr THEN
                DO:
                    FIND FIRST l-order WHERE l-order.lief-nr = l-kredit.lief-nr
                        AND l-order.docu-nr = l-kredit.NAME
                        AND l-order.pos = 0 NO-LOCK NO-ERROR.
                    IF AVAILABLE l-order THEN
                    ASSIGN age-list.rabattbetrag = l-order.warenwert.
                END.

                FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.char1 = l-kredit.NAME NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    ASSIGN
                        age-list.recv-date = queasy.date1.
                END.
            END. 
            ELSE 
            DO: 
                age-list.credit = age-list.credit - l-kredit.saldo. 
                age-list.tot-debt = age-list.tot-debt + l-kredit.saldo. 
            END. 
    
            RUN disp-l-lieferant-debt.
    
            FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno = l-kredit.NAME NO-LOCK NO-ERROR.
            IF AVAIL gl-jouhdr THEN
            DO:
                FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr NO-LOCK,
                    EACH gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto
                    AND (gl-acct.acc-type = 2  OR gl-acct.acc-type = 3 OR gl-acct.acc-type = 5):
                    age-list.comment = age-list.comment + ";" + 
                                       string(gl-journal.fibukonto) + ";" + string(l-kredit.steuercode).
                    /*gerald 210920 Tauzia LnL*/   
                    age-list.fibukonto = gl-journal.fibukonto.
                    age-list.t-bezeich = gl-acct.bezeich.

                    IF gl-journal.debit GT 0 THEN
                    DO:
                      age-list.debt2     = gl-journal.debit.
                    END.
                    ELSE IF gl-journal.credit GT 0 THEN
                    DO:
                      age-list.debt2    = -(gl-journal.credit).
                    END.
                    /*end gerald*/
                END.
            END.
        END. 
        art-selected = 1. 
    END. 
END. 



PROCEDURE disp-l-lieferant-debt: 
DEFINE VARIABLE lief-nr AS INTEGER.
    IF AVAILABLE age-list THEN 
    DO: 
        lief-nr = age-list.lief-nr. 
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK.
        ASSIGN
            age-list.resname  = l-lieferant.firma + ", " + l-lieferant.anredefirma + chr(10) + 
                                l-lieferant.adresse1 + chr(10) +  l-lieferant.wohnort + " " + l-lieferant.plz
            age-list.comments = age-list.bemerk.
    END. 
END. 

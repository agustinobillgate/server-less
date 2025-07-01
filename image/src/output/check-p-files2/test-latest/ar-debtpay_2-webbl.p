DEFINE TEMP-TABLE t-debt
    FIELD t-debt-recid  AS INT
    FIELD rgdatum       AS DATE.

DEFINE TEMP-TABLE age-list 
  FIELD selected        AS LOGICAL INITIAL NO 
  FIELD ar-recid        AS INTEGER 
  FIELD rechnr          AS INTEGER FORMAT ">>>>>>>>9" 
  FIELD refno           AS INTEGER FORMAT ">>>>>>>>>" 
  FIELD counter         AS INTEGER 
  FIELD gastnr          AS INTEGER 
  FIELD billname        AS CHAR FORMAT "x(36)" 
  FIELD gastnrmember    AS INTEGER 
  FIELD gastname        AS CHAR FORMAT "x(36)" 
  FIELD zinr            AS CHAR format "x(9)" /* change by damen 29/03/23 B05088 */
  FIELD rgdatum         AS DATE 
  FIELD user-init       AS CHAR FORMAT "x(2)" 
  FIELD debt            AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" /* INITIAL 0 */
  FIELD debt-foreign    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD currency        AS CHAR FORMAT "x(4)" 
  FIELD credit          AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0
  FIELD vouc-nr         AS CHAR   FORMAT "x(24)"
  FIELD prevdate        AS DATE 
  FIELD remarks         AS CHAR   FORMAT "x(50)" /*ITA 121213*/
  FIELD b-resname       AS CHAR
  FIELD ci-date         AS DATE /*sis 300414 add ci-date*/
  FIELD co-date         AS DATE /*sis 300414 add co-date*/
  FIELD resnr           AS INTEGER
  FIELD mbill           AS CHAR
  /* Naufal Afthar - 992296*/
  FIELD dptNo           AS INTEGER.


DEFINE TEMP-TABLE input-payload
    FIELD artnr         AS INTEGER
    FIELD userinit      AS CHARACTER
    FIELD bill-nr       AS INTEGER
    FIELD temp-art2     AS INTEGER
    FIELD from-date     AS DATE /*bernatd 4ACE13*/
    FIELD to-date       AS DATE /*bernatd 4ACE13*/
    FIELD bill-name     AS CHARACTER
    FIELD to-name       AS CHARACTER
    FIELD bill-saldo    AS DECIMAL
    /* Naufal Afthar - 992296*/
    FIELD period-flag   AS LOGICAL 
    FIELD remark-str    AS CHARACTER
    FIELD from-dpt      AS INTEGER
    FIELD to-dpt        AS INTEGER
    .


DEFINE INPUT PARAMETER TABLE FOR input-payload.
DEFINE INPUT-OUTPUT PARAMETER art-selected  AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER foutstand     AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER outstand      AS DECIMAL.
DEFINE OUTPUT PARAMETER curr-art            AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR age-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-debt.

DEFINE BUFFER abuff  FOR age-list.
DEFINE BUFFER debt   FOR debitor.
DEFINE BUFFER t-pay  FOR debitor. /* Naufal Afthar - C596AF*/
DEF VAR t-resnr AS INT.
DEF VAR t-name  AS CHAR.


FIND FIRST input-payload NO-LOCK NO-ERROR.

/* Naufal Afthar - 992296*/
IF input-payload.period-flag THEN 
DO: 
    RUN create-age-list1.

    /* Naufal Afthar - C596AF -> get saldo and credit outside of from-date to-date period*/
    FOR EACH age-list:
        FOR EACH t-pay WHERE t-pay.artnr EQ input-payload.temp-art2
            AND t-pay.rechnr EQ age-list.rechnr
            AND t-pay.counter EQ age-list.counter
            AND t-pay.counter NE 0
            AND t-pay.opart LT 2
            AND (t-pay.rgdatum LT input-payload.from-date OR t-pay.rgdatum GT input-payload.to-date)
            USE-INDEX rechnr_ix NO-LOCK
            BY t-pay.zahlkonto BY t-pay.rgdatum:
    
            IF t-pay.zahlkonto GT 0 THEN
            ASSIGN age-list.credit = age-list.credit - t-pay.saldo.
    
            age-list.tot-debt = age-list.tot-debt + t-pay.saldo.
        END.
        
        /* Naufal Afthar - 992296 -> search by remark & outlet no*/
        IF (input-payload.remark-str NE ? AND input-payload.remark-str NE "" AND input-payload.remark-str NE " ")
            AND NOT age-list.remarks MATCHES("*" + input-payload.remark-str + "*") THEN
        DO:
            DELETE age-list.
        END.

        IF age-list.dptNo LT input-payload.from-dpt OR age-list.dptNo GT input-payload.to-dpt THEN
        DO:
            DELETE age-list.
        END.
    END.
END.
ELSE 
DO: 
    RUN create-age-list.

    /* Naufal Afthar - C596AF -> get debit and credit after bill-date*/
    FOR EACH age-list:
        FOR EACH t-pay WHERE t-pay.artnr EQ input-payload.temp-art2
            AND t-pay.rechnr EQ age-list.rechnr
            AND t-pay.counter EQ age-list.counter
            AND t-pay.counter NE 0
            AND t-pay.opart LT 2
            AND t-pay.rgdatum GT input-payload.from-date
            USE-INDEX rechnr_ix NO-LOCK
            BY t-pay.zahlkonto BY t-pay.rgdatum :
            
            IF t-pay.zahlkonto GT 0 THEN
            ASSIGN age-list.credit = age-list.credit - t-pay.saldo.
            
            age-list.tot-debt = age-list.tot-debt + t-pay.saldo.
        END.

        /* Naufal Afthar - 992296 -> search by remark & outlet no*/
        IF (input-payload.remark-str NE ? AND input-payload.remark-str NE "" AND input-payload.remark-str NE " ")
            AND NOT age-list.remarks MATCHES("*" + input-payload.remark-str + "*") THEN
        DO:
            DELETE age-list.
        END.

        IF age-list.dptNo LT input-payload.from-dpt OR age-list.dptNo GT input-payload.to-dpt THEN
        DO:
            DELETE age-list.
        END.
    END.
END.

FOR EACH abuff,
    FIRST debt WHERE RECID(debt) = abuff.ar-recid NO-LOCK:
    CREATE t-debt.
    ASSIGN t-debt.t-debt-recid = RECID(debt)
           t-debt.rgdatum = debt.rgdatum.
END.


PROCEDURE create-age-list: 
  DEFINE BUFFER artikel1 FOR artikel. 
  DEFINE VARIABLE curr-rechnr AS INTEGER. 
  DEFINE VARIABLE curr-saldo AS DECIMAL. 
  DEFINE VARIABLE opart AS INTEGER INITIAL 1. 
  DEFINE VARIABLE i AS INTEGER NO-UNDO.
  DEFINE VARIABLE bill-date AS DATE.
  /* IF curr-art NE artikel.artnr THEN */ 
 
  bill-date = input-payload.from-date.

  DO: 
    curr-art = input-payload.artnr. 
    FOR EACH age-list: 
      delete age-list. 
    END. 
    ASSIGN
        curr-rechnr = 0
        outstand = 0
        foutstand = 0.
    IF input-payload.bill-nr NE 0 THEN 
    DO:
      FOR EACH debitor WHERE debitor.artnr = /*artikel.artnr */ input-payload.temp-art2
        AND debitor.rechnr EQ input-payload.bill-nr 
        AND debitor.rgdatum LE bill-date AND debitor.opart LT 2 NO-LOCK 
        USE-INDEX rechnr_ix BY debitor.zahlkonto BY debitor.rgdatum: 
        IF debitor.counter NE 0 THEN FIND FIRST age-list 
          WHERE age-list.counter = debitor.counter NO-ERROR. 
        IF NOT AVAILABLE age-list OR debitor.counter = 0 THEN 
        DO: 
          CREATE age-list. 
          age-list.ar-recid     = RECID(debitor). 
          age-list.rgdatum      = debitor.rgdatum. 
          age-list.counter      = debitor.counter. 
          age-list.rechnr       = debitor.rechnr. 
          age-list.refno        = debitor.debref. 
          age-list.gastnr       = debitor.gastnr. 
          age-list.gastnrmember = debitor.gastnrmember. 
          age-list.zinr         = debitor.zinr. 
          age-list.dptNo        = debitor.betriebsnr. /* Naufal Afthar - 992296*/
          
          RUN disp-guest-debt.
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
          age-list.billname = guest.name + ", " + guest.vorname1 
            + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnrmember 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE guest THEN age-list.gastname = guest.name + ", " 
            + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
              AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
              (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.TRANSzeit + 2))
              NO-LOCK NO-ERROR.
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
             IF bill.reslinnr = 0 THEN 
                 ASSIGN age-list.resnr = bill.resnr
                        age-list.mbill = "*".
          END.
        END. 
        IF debitor.zahlkonto = 0 THEN 
        DO: 
          /*ITA age-list.user-init = userinit. */
          FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr NO-LOCK NO-ERROR.
          IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit.
          age-list.rgdatum = debitor.rgdatum. 
          age-list.debt = age-list.debt + debitor.saldo. 
          age-list.debt-foreign = age-list.debt-foreign + debitor.vesrdep. 
          IF debitor.betrieb-gastmem NE 0 THEN 
          DO: 
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
              debitor.betrieb-gastmem NO-LOCK NO-ERROR. 
            IF AVAILABLE waehrung THEN age-list.currency = waehrung.wabkurz. 
          END. 
        END. 
        ELSE 
        DO: 
          age-list.credit = age-list.credit - debitor.saldo. 
        END. 
        age-list.tot-debt = age-list.tot-debt + debitor.saldo. 
      END. 
    END. 
    ELSE IF (input-payload.bill-name NE "") AND (SUBSTR(input-payload.bill-name,1,1) NE "*") THEN 
    DO:
      FOR EACH debitor WHERE debitor.artnr = /*artikel.artnr */ input-payload.temp-art2
        AND debitor.name /*GE*/ MATCHES("*" + input-payload.bill-name + "*") /*AND debitor.name LE input-payload.to-name) */
        AND debitor.rgdatum LE bill-date AND debitor.opart LT 2 
        NO-LOCK BY debitor.zahlkonto BY debitor.debref BY debitor.rgdatum: 
        IF debitor.counter NE 0 THEN FIND FIRST age-list 
          WHERE age-list.counter = debitor.counter NO-ERROR. 
        IF NOT AVAILABLE age-list OR debitor.counter = 0 THEN 
        DO: 
          create age-list. 
          age-list.ar-recid     = RECID(debitor). 
          age-list.rgdatum      = debitor.rgdatum. 
          age-list.counter      = debitor.counter. 
          age-list.rechnr       = debitor.rechnr. 
          age-list.refno        = debitor.debref. 
          age-list.gastnr       = debitor.gastnr. 
          age-list.gastnrmember = debitor.gastnrmember. 
          age-list.zinr         = debitor.zinr.
          age-list.dptNo        = debitor.betriebsnr. /* Naufal Afthar - 992296*/
          
          RUN disp-guest-debt.
          
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
          age-list.billname = guest.name + ", " + guest.vorname1 
            + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnrmember 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE guest THEN age-list.gastname = guest.name + ", " 
            + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
              AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
              (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.TRANSzeit + 2))
              NO-LOCK NO-ERROR.
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
             IF bill.reslinnr = 0 THEN 
                 ASSIGN age-list.resnr = bill.resnr
                        age-list.mbill = "*".
          END.
          /*ITA 121213*/
          IF debitor.vesrcod MATCHES "*resno:*" THEN
          DO:
                /*IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                t-resnr = INT(SUBSTR(debitor.vesrcod, 26, LENGTH(debitor.vesrcod) - 1)).
                ELSE
                    ASSIGN
                        t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                        t-resnr = INT(SUBSTR(t-name, 26, LENGTH(t-name) - 1)).
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.*/
                
                /*ITA 121016*/
                IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                      ASSIGN t-resnr = INT(TRIM(ENTRY(2, ENTRY(1, debitor.vesrcod, ";"), ":"))).
                ELSE
                    ASSIGN
                        t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                        t-resnr = INT(TRIM(ENTRY(2, t-name, ":"))).
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.
          END.
          
          IF(debitor.vesrcod MATCHES "*;*") THEN
          ASSIGN
              age-list.vouc-nr = TRIM(ENTRY(2, debitor.vesrcod, ";"))
              age-list.remarks = TRIM(ENTRY(1, debitor.vesrcod, ";")).
          ELSE
          DO:
            age-list.remarks = debitor.vesrcod.
            FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
              AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
              (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.TRANSzeit + 2))
              NO-LOCK NO-ERROR.
            IF AVAILABLE bill-line THEN
            DO:
              DO i = 1 TO (LENGTH(bill-line.bezeich)):
                  IF SUBSTR(bill-line.bezeich, i, 1) = "/"   THEN
                  DO:
                      age-list.vouc-nr = SUBSTR(bill-line.bezeich, (i + 1), 
                                                (LENGTH(bill-line.bezeich) - i)).
                      i = LENGTH(bill-line.bezeich).
                  END.
              END.
              /*age-list.vouc-nr = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
            END.
          END.
        END. 
          /*IF AVAILABLE bill-line THEN
          DO:
              DO i = 1 TO (LENGTH(bill-line.bezeich)):
                  IF SUBSTR(bill-line.bezeich, i, 1) = "/"   THEN
                  DO:
                      age-list.vouc-nr = SUBSTR(bill-line.bezeich, (i + 1), 
                                                (LENGTH(bill-line.bezeich) - i)).
                      i = LENGTH(bill-line.bezeich).
                  END.
              END.
              /*age-list.vouc-nr = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
          END.
        END.*/ 
        IF debitor.zahlkonto = 0 THEN 
        DO: 
          /*ITA age-list.user-init = userinit.*/
          FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr NO-LOCK NO-ERROR.
          IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit.
          age-list.rgdatum = debitor.rgdatum. 
          age-list.debt = age-list.debt + debitor.saldo. 
          age-list.debt-foreign = age-list.debt-foreign + debitor.vesrdep. 
          IF debitor.betrieb-gastmem NE 0 THEN 
          DO: 
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
              debitor.betrieb-gastmem NO-LOCK NO-ERROR. 
            IF AVAILABLE waehrung THEN age-list.currency = waehrung.wabkurz. 
          END. 
        END. 
        ELSE 
        DO: 
          age-list.credit = age-list.credit - debitor.saldo. 
        END. 
        age-list.tot-debt = age-list.tot-debt + debitor.saldo. 
      END. 
    END. 
    ELSE IF (input-payload.bill-name NE "") AND (SUBSTR(input-payload.bill-name,1,1) EQ "*") THEN 
    DO: 
      FOR EACH debitor WHERE debitor.artnr = /*artikel.artnr */ input-payload.temp-art2
        AND debitor.name  MATCHES("*" + input-payload.bill-name + "*") 
        AND debitor.rgdatum LE bill-date AND debitor.opart LT 2 
        NO-LOCK BY debitor.zahlkonto BY debitor.debref BY debitor.rgdatum: 
        IF debitor.counter NE 0 THEN FIND FIRST age-list 
          WHERE age-list.counter = debitor.counter NO-ERROR. 
        IF NOT AVAILABLE age-list OR debitor.counter = 0 THEN 
        DO: 
          create age-list. 
          age-list.ar-recid     = RECID(debitor). 
          age-list.rgdatum      = debitor.rgdatum. 
          age-list.counter      = debitor.counter. 
          age-list.rechnr       = debitor.rechnr. 
          age-list.refno        = debitor.debref. 
          age-list.gastnr       = debitor.gastnr. 
          age-list.gastnrmember = debitor.gastnrmember. 
          age-list.zinr         = debitor.zinr.
          age-list.dptNo        = debitor.betriebsnr. /* Naufal Afthar - 992296*/
          
          RUN disp-guest-debt.
         
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
          age-list.billname = guest.name + ", " + guest.vorname1 
            + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnrmember 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE guest THEN age-list.gastname = guest.name + ", " 
            + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
              AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
              (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.transzeit + 2))
              NO-LOCK NO-ERROR.
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
             IF bill.reslinnr = 0 THEN 
                 ASSIGN age-list.resnr = bill.resnr
                        age-list.mbill = "*".
          END.
          /*ITA 121213*/
          IF debitor.vesrcod MATCHES "*resno:*" THEN
          DO:
                /*IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                t-resnr = INT(SUBSTR(debitor.vesrcod, 26, LENGTH(debitor.vesrcod) - 1)).
                ELSE
                    ASSIGN
                        t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                        t-resnr = INT(SUBSTR(t-name, 26, LENGTH(t-name) - 1)).
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.*/
              /*ITA 121016*/
                IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                      ASSIGN t-resnr = INT(TRIM(ENTRY(2, ENTRY(1, debitor.vesrcod, ";"), ":"))).
                ELSE
                    ASSIGN
                        t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                        t-resnr = INT(TRIM(ENTRY(2, t-name, ":"))).
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.
          END.
          IF(debitor.vesrcod MATCHES "*;*") THEN
          ASSIGN
              age-list.vouc-nr = TRIM(ENTRY(2, debitor.vesrcod, ";"))
              age-list.remarks = TRIM(ENTRY(1, debitor.vesrcod, ";")).
          ELSE
          DO:
              age-list.remarks = debitor.vesrcod.
              FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
                  AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
                  (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.transzeit + 2))
                  NO-LOCK NO-ERROR.
              IF AVAILABLE bill-line THEN
              DO:
                   DO i = 1 TO (LENGTH(bill-line.bezeich)):
                      IF SUBSTR(bill-line.bezeich, i, 1) = "/"   THEN
                      DO:
                          age-list.vouc-nr = SUBSTR(bill-line.bezeich, (i + 1), 
                                                    (LENGTH(bill-line.bezeich) - i)).
                          i = LENGTH(bill-line.bezeich).
                      END.
                  END.
                  /*age-list.vouc-nr = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
              END.
          END.
          /*IF AVAILABLE bill-line THEN
          DO:
               DO i = 1 TO (LENGTH(bill-line.bezeich)):
                  IF SUBSTR(bill-line.bezeich, i, 1) = "/"   THEN
                  DO:
                      age-list.vouc-nr = SUBSTR(bill-line.bezeich, (i + 1), 
                                                (LENGTH(bill-line.bezeich) - i)).
                      i = LENGTH(bill-line.bezeich).
                  END.
              END.
              /*age-list.vouc-nr = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
          END.*/
        END. 
        IF debitor.zahlkonto = 0 THEN 
        DO:
          /*ITA age-list.user-init = userinit. */
          FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr NO-LOCK NO-ERROR.
          IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit.
          age-list.rgdatum = debitor.rgdatum. 
          age-list.debt = age-list.debt + debitor.saldo.   
          age-list.debt-foreign = age-list.debt-foreign + debitor.vesrdep. 
          IF debitor.betrieb-gastmem NE 0 THEN 
          DO: 
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
              debitor.betrieb-gastmem NO-LOCK NO-ERROR. 
            IF AVAILABLE waehrung THEN age-list.currency = waehrung.wabkurz. 
          END. 
        END. 
        ELSE 
        DO: 
          age-list.credit = age-list.credit - debitor.saldo. 
        END. 
        age-list.tot-debt = age-list.tot-debt + debitor.saldo. 
      END. 
    END. 
    ELSE IF input-payload.bill-name = "" THEN 
    DO:
        FOR EACH debitor WHERE debitor.artnr =/* artikel.artnr */ input-payload.temp-art2
            AND debitor.rgdatum LE bill-date AND debitor.opart LT 2 NO-LOCK BY debitor.zahlkonto BY debitor.rgdatum: 
            IF debitor.counter NE 0 THEN FIND FIRST age-list WHERE age-list.counter = debitor.counter NO-ERROR. 
            IF NOT AVAILABLE age-list OR debitor.counter = 0 THEN 
        DO: 
          create age-list. 
          age-list.ar-recid     = RECID(debitor). 
          age-list.rgdatum      = debitor.rgdatum. 
          age-list.counter      = debitor.counter. 
          age-list.rechnr       = debitor.rechnr. 
          age-list.refno        = debitor.debref. 
          age-list.gastnr       = debitor.gastnr. 
          age-list.gastnrmember = debitor.gastnrmember. 
          age-list.zinr         = debitor.zinr.
          age-list.dptNo        = debitor.betriebsnr. /* Naufal Afthar - 992296*/

          
          MESSAGE "TRAPLOG: start: " + STRING(TIME,"hh:mm:ss") VIEW-AS ALERT-BOX INFO BUTTONS OK.
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK NO-ERROR. 
          age-list.billname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR. 
          IF AVAILABLE guest THEN age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
            AND bill-line.betrag = (- debitor.saldo) 
            AND (bill-line.zeit GE (debitor.transzeit - 2) 
            AND (bill-line.zeit LE debitor.transzeit + 2)) NO-LOCK NO-ERROR.
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
             IF bill.reslinnr = 0 THEN 
                 ASSIGN age-list.resnr = bill.resnr
                        age-list.mbill = "*".
          END.
          MESSAGE "TRAPLOG: end: " + STRING(TIME,"hh:mm:ss") VIEW-AS ALERT-BOX INFO BUTTONS OK.
          /*ITA 121213*/
          IF debitor.vesrcod MATCHES "*resno:*" THEN
          DO:
                /*IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                t-resnr = INT(SUBSTR(debitor.vesrcod, 26, LENGTH(debitor.vesrcod) - 1))
                  NO-ERROR.
                ELSE
                ASSIGN
                    t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                    t-resnr = INT(SUBSTR(t-name, 26, LENGTH(t-name) - 1)) NO-ERROR
                .
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.*/
              /*ITA 121016*/
                IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                      ASSIGN t-resnr = INT(TRIM(ENTRY(2, ENTRY(1, debitor.vesrcod, ";"), ":"))).
                ELSE
                    ASSIGN
                        t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                        t-resnr = INT(TRIM(ENTRY(2, t-name, ":"))).
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.
          END.
          IF(debitor.vesrcod MATCHES "*;*") THEN
          ASSIGN
              age-list.vouc-nr = TRIM(ENTRY(2, debitor.vesrcod, ";"))
              age-list.remarks = TRIM(ENTRY(1, debitor.vesrcod, ";")).
          ELSE
          DO:
              age-list.remarks = debitor.vesrcod.
              FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
                  AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
                  (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.transzeit + 2))
                  NO-LOCK NO-ERROR.
              IF AVAILABLE bill-line THEN
              DO:
                   DO i = 1 TO (LENGTH(bill-line.bezeich)):
                      IF SUBSTR(bill-line.bezeich, i, 1) = "/"   THEN
                      DO:
                          age-list.vouc-nr = SUBSTR(bill-line.bezeich, (i + 1), 
                                                    (LENGTH(bill-line.bezeich) - i )).
                          i = LENGTH(bill-line.bezeich).
                      END.
                  END.
                  /*age-list.vouc-nr = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
              END.
          END.
          
          /*IF AVAILABLE bill-line THEN
          DO:
               DO i = 1 TO (LENGTH(bill-line.bezeich)):
                  IF SUBSTR(bill-line.bezeich, i, 1) = "/"   THEN
                  DO:
                      age-list.vouc-nr = SUBSTR(bill-line.bezeich, (i + 1), 
                                                (LENGTH(bill-line.bezeich) - i )).
                      i = LENGTH(bill-line.bezeich).
                  END.
              END.
              /*age-list.vouc-nr = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
          END.*/
        END. 
        IF debitor.zahlkonto = 0 THEN 
        DO: 
          /*ITA age-list.user-init = userinit. */
          FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr NO-LOCK NO-ERROR.
          IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit.
          age-list.rgdatum = debitor.rgdatum. 
          age-list.debt = age-list.debt + debitor.saldo. 
          age-list.debt-foreign = age-list.debt-foreign + debitor.vesrdep. 
          
          RUN disp-guest-debt.
          
          IF debitor.betrieb-gastmem NE 0 THEN 
          DO: 
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
              debitor.betrieb-gastmem NO-LOCK NO-ERROR. 
            IF AVAILABLE waehrung THEN age-list.currency = waehrung.wabkurz. 
          END. 
        END. 
        ELSE 
        DO: 
          age-list.credit = age-list.credit - debitor.saldo. 
        END. 
        age-list.tot-debt = age-list.tot-debt + debitor.saldo. 
      END. 
    END. 
    art-selected = 1. 
    IF input-payload.bill-saldo NE 0 THEN 
    FOR EACH age-list WHERE age-list.tot-debt NE input-payload.bill-saldo: 
        DELETE age-list. 
    END. 
  END. 
  RELEASE abuff.
END. 

PROCEDURE create-age-list1: 
  DEFINE BUFFER artikel1 FOR artikel. 
  DEFINE VARIABLE curr-rechnr AS INTEGER. 
  DEFINE VARIABLE curr-saldo AS DECIMAL. 
  DEFINE VARIABLE opart AS INTEGER INITIAL 1. 
  DEFINE VARIABLE i AS INTEGER NO-UNDO.
  DEFINE VARIABLE from-date AS DATE.
  DEFINE VARIABLE to-date AS DATE.
  /* IF curr-art NE artikel.artnr THEN */ 
 
  DO: 
    from-date = input-payload.from-date.
    to-date   = input-payload.to-date.
    curr-art = input-payload.artnr. 

    FOR EACH age-list: 
      delete age-list. 
    END. 
    ASSIGN
        curr-rechnr = 0
        outstand = 0
        foutstand = 0.

    IF input-payload.bill-nr NE 0 THEN 
    DO:
      FOR EACH debitor WHERE debitor.artnr = /*artikel.artnr */ input-payload.temp-art2
        AND debitor.rechnr EQ input-payload.bill-nr 
        AND debitor.rgdatum GE from-date 
        AND debitor.rgdatum LE to-date AND debitor.opart LT 2 NO-LOCK 
        USE-INDEX rechnr_ix BY debitor.zahlkonto BY debitor.rgdatum: 
        IF debitor.counter NE 0 THEN FIND FIRST age-list 
          WHERE age-list.counter = debitor.counter NO-ERROR. 
        IF NOT AVAILABLE age-list OR debitor.counter = 0 THEN 
        DO: 
          CREATE age-list. 
          age-list.ar-recid     = RECID(debitor). 
          age-list.rgdatum      = debitor.rgdatum. 
          age-list.counter      = debitor.counter. 
          age-list.rechnr       = debitor.rechnr. 
          age-list.refno        = debitor.debref. 
          age-list.gastnr       = debitor.gastnr. 
          age-list.gastnrmember = debitor.gastnrmember. 
          age-list.zinr         = debitor.zinr. 
          age-list.dptNo        = debitor.betriebsnr. /* Naufal Afthar - 992296*/
          
          RUN disp-guest-debt.

          FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
          age-list.billname = guest.name + ", " + guest.vorname1 
            + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnrmember 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE guest THEN age-list.gastname = guest.name + ", " 
            + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
              AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
              (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.TRANSzeit + 2))
              NO-LOCK NO-ERROR.


          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
             IF bill.reslinnr = 0 THEN 
                 ASSIGN age-list.resnr = bill.resnr
                        age-list.mbill = "*".
          END.
        END. 
        IF debitor.zahlkonto = 0 THEN 
        DO: 
          /*ITA age-list.user-init = userinit. */
          FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr NO-LOCK NO-ERROR.
          IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit.
          age-list.rgdatum = debitor.rgdatum. 
          age-list.debt = age-list.debt + debitor.saldo. 
          age-list.debt-foreign = age-list.debt-foreign + debitor.vesrdep. 
          IF debitor.betrieb-gastmem NE 0 THEN 
          DO: 
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
              debitor.betrieb-gastmem NO-LOCK NO-ERROR. 
            IF AVAILABLE waehrung THEN age-list.currency = waehrung.wabkurz. 
          END. 
        END. 
        ELSE 
        DO: 
          age-list.credit = age-list.credit - debitor.saldo. 
        END. 
        age-list.tot-debt = age-list.tot-debt + debitor.saldo. 
      END. 
    END. 
    ELSE IF (input-payload.bill-name NE "") AND (SUBSTR(input-payload.bill-name,1,1) NE "*") THEN 
    DO:
      FOR EACH debitor WHERE debitor.artnr = /*artikel.artnr */ input-payload.temp-art2
        AND debitor.name /*GE*/ MATCHES("*" + input-payload.bill-name + "*") /*AND debitor.name LE input-payload.to-name)*/
        AND debitor.rgdatum GE from-date 
        AND debitor.rgdatum LE to-date AND debitor.opart LT 2 
        NO-LOCK BY debitor.zahlkonto BY debitor.debref BY debitor.rgdatum: 
        IF debitor.counter NE 0 THEN FIND FIRST age-list 
          WHERE age-list.counter = debitor.counter NO-ERROR. 
        IF NOT AVAILABLE age-list OR debitor.counter = 0 THEN 
        DO: 
          create age-list. 
          age-list.ar-recid     = RECID(debitor). 
          age-list.rgdatum      = debitor.rgdatum. 
          age-list.counter      = debitor.counter. 
          age-list.rechnr       = debitor.rechnr. 
          age-list.refno        = debitor.debref. 
          age-list.gastnr       = debitor.gastnr. 
          age-list.gastnrmember = debitor.gastnrmember. 
          age-list.zinr         = debitor.zinr.
          age-list.dptNo        = debitor.betriebsnr. /* Naufal Afthar - 992296*/
          
          RUN disp-guest-debt.
          
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
          age-list.billname = guest.name + ", " + guest.vorname1 
            + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnrmember 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE guest THEN age-list.gastname = guest.name + ", " 
            + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
              AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
              (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.TRANSzeit + 2))
              NO-LOCK NO-ERROR.

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
             IF bill.reslinnr = 0 THEN 
                 ASSIGN age-list.resnr = bill.resnr
                        age-list.mbill = "*".
          END.

          /*ITA 121213*/
          IF debitor.vesrcod MATCHES "*resno:*" THEN
          DO:
                /*IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                t-resnr = INT(SUBSTR(debitor.vesrcod, 26, LENGTH(debitor.vesrcod) - 1)).
                ELSE
                    ASSIGN
                        t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                        t-resnr = INT(SUBSTR(t-name, 26, LENGTH(t-name) - 1)).
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.*/
                
                /*ITA 121016*/
                IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                      ASSIGN t-resnr = INT(TRIM(ENTRY(2, ENTRY(1, debitor.vesrcod, ";"), ":"))).
                ELSE
                    ASSIGN
                        t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                        t-resnr = INT(TRIM(ENTRY(2, t-name, ":"))).
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.
          END.
          
          IF(debitor.vesrcod MATCHES "*;*") THEN
          ASSIGN
              age-list.vouc-nr = TRIM(ENTRY(2, debitor.vesrcod, ";"))
              age-list.remarks = TRIM(ENTRY(1, debitor.vesrcod, ";")).
          ELSE
          DO:
            age-list.remarks = debitor.vesrcod.
            FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
              AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
              (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.TRANSzeit + 2))
              NO-LOCK NO-ERROR.
            IF AVAILABLE bill-line THEN
            DO:
              DO i = 1 TO (LENGTH(bill-line.bezeich)):
                  IF SUBSTR(bill-line.bezeich, i, 1) = "/"   THEN
                  DO:
                      age-list.vouc-nr = SUBSTR(bill-line.bezeich, (i + 1), 
                                                (LENGTH(bill-line.bezeich) - i)).
                      i = LENGTH(bill-line.bezeich).
                  END.
              END.
              /*age-list.vouc-nr = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
            END.
          END.
        END. 
          /*IF AVAILABLE bill-line THEN
          DO:
              DO i = 1 TO (LENGTH(bill-line.bezeich)):
                  IF SUBSTR(bill-line.bezeich, i, 1) = "/"   THEN
                  DO:
                      age-list.vouc-nr = SUBSTR(bill-line.bezeich, (i + 1), 
                                                (LENGTH(bill-line.bezeich) - i)).
                      i = LENGTH(bill-line.bezeich).
                  END.
              END.
              /*age-list.vouc-nr = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
          END.
        END.*/ 
        IF debitor.zahlkonto = 0 THEN 
        DO: 
          /*ITA age-list.user-init = userinit.*/
          FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr NO-LOCK NO-ERROR.
          IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit.
          age-list.rgdatum = debitor.rgdatum. 
          age-list.debt = age-list.debt + debitor.saldo. 
          age-list.debt-foreign = age-list.debt-foreign + debitor.vesrdep. 
          IF debitor.betrieb-gastmem NE 0 THEN 
          DO: 
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
              debitor.betrieb-gastmem NO-LOCK NO-ERROR. 
            IF AVAILABLE waehrung THEN age-list.currency = waehrung.wabkurz. 
          END. 
        END. 
        ELSE 
        DO: 
          age-list.credit = age-list.credit - debitor.saldo. 
        END. 
        age-list.tot-debt = age-list.tot-debt + debitor.saldo. 
      END. 
    END. 
    ELSE IF (input-payload.bill-name NE "") AND (SUBSTR(input-payload.bill-name,1,1) EQ "*") THEN 
    DO: 
      FOR EACH debitor WHERE debitor.artnr = /*artikel.artnr */ input-payload.temp-art2
        AND debitor.name  MATCHES("*" + input-payload.bill-name + "*") 
        AND debitor.rgdatum GE from-date
        AND debitor.rgdatum LE to-date AND debitor.opart LT 2 
        NO-LOCK BY debitor.zahlkonto BY debitor.debref BY debitor.rgdatum: 
        IF debitor.counter NE 0 THEN FIND FIRST age-list 
          WHERE age-list.counter = debitor.counter NO-ERROR. 
        IF NOT AVAILABLE age-list OR debitor.counter = 0 THEN 
        DO: 
          create age-list. 
          age-list.ar-recid     = RECID(debitor). 
          age-list.rgdatum      = debitor.rgdatum. 
          age-list.counter      = debitor.counter. 
          age-list.rechnr       = debitor.rechnr. 
          age-list.refno        = debitor.debref. 
          age-list.gastnr       = debitor.gastnr. 
          age-list.gastnrmember = debitor.gastnrmember. 
          age-list.zinr         = debitor.zinr. 
          age-list.dptNo        = debitor.betriebsnr. /* Naufal Afthar - 992296*/
          
          RUN disp-guest-debt.
         
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
          age-list.billname = guest.name + ", " + guest.vorname1 
            + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnrmember 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE guest THEN age-list.gastname = guest.name + ", " 
            + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
              AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
              (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.transzeit + 2))
              NO-LOCK NO-ERROR.

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
             IF bill.reslinnr = 0 THEN 
                 ASSIGN age-list.resnr = bill.resnr
                        age-list.mbill = "*".
          END.
          /*ITA 121213*/
          IF debitor.vesrcod MATCHES "*resno:*" THEN
          DO:
                /*IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                t-resnr = INT(SUBSTR(debitor.vesrcod, 26, LENGTH(debitor.vesrcod) - 1)).
                ELSE
                    ASSIGN
                        t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                        t-resnr = INT(SUBSTR(t-name, 26, LENGTH(t-name) - 1)).
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.*/

              /*ITA 121016*/
                IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                      ASSIGN t-resnr = INT(TRIM(ENTRY(2, ENTRY(1, debitor.vesrcod, ";"), ":"))).
                ELSE
                    ASSIGN
                        t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                        t-resnr = INT(TRIM(ENTRY(2, t-name, ":"))).
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.
          END.

          IF(debitor.vesrcod MATCHES "*;*") THEN
          ASSIGN
              age-list.vouc-nr = TRIM(ENTRY(2, debitor.vesrcod, ";"))
              age-list.remarks = TRIM(ENTRY(1, debitor.vesrcod, ";")).
          ELSE
          DO:
              age-list.remarks = debitor.vesrcod.
              FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
                  AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
                  (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.transzeit + 2))
                  NO-LOCK NO-ERROR.
              IF AVAILABLE bill-line THEN
              DO:
                   DO i = 1 TO (LENGTH(bill-line.bezeich)):
                      IF SUBSTR(bill-line.bezeich, i, 1) = "/"   THEN
                      DO:
                          age-list.vouc-nr = SUBSTR(bill-line.bezeich, (i + 1), 
                                                    (LENGTH(bill-line.bezeich) - i)).
                          i = LENGTH(bill-line.bezeich).
                      END.
                  END.
                  /*age-list.vouc-nr = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
              END.
          END.

          /*IF AVAILABLE bill-line THEN
          DO:
               DO i = 1 TO (LENGTH(bill-line.bezeich)):
                  IF SUBSTR(bill-line.bezeich, i, 1) = "/"   THEN
                  DO:
                      age-list.vouc-nr = SUBSTR(bill-line.bezeich, (i + 1), 
                                                (LENGTH(bill-line.bezeich) - i)).
                      i = LENGTH(bill-line.bezeich).
                  END.
              END.
              /*age-list.vouc-nr = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
          END.*/
        END. 
        IF debitor.zahlkonto = 0 THEN 
        DO:
          /*ITA age-list.user-init = userinit. */
          FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr NO-LOCK NO-ERROR.
          IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit.
          age-list.rgdatum = debitor.rgdatum. 
          age-list.debt = age-list.debt + debitor.saldo.   
          age-list.debt-foreign = age-list.debt-foreign + debitor.vesrdep. 
          IF debitor.betrieb-gastmem NE 0 THEN 
          DO: 
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
              debitor.betrieb-gastmem NO-LOCK NO-ERROR. 
            IF AVAILABLE waehrung THEN age-list.currency = waehrung.wabkurz. 
          END. 
        END. 
        ELSE 
        DO: 
          age-list.credit = age-list.credit - debitor.saldo. 
        END. 
        age-list.tot-debt = age-list.tot-debt + debitor.saldo. 
      END. 
    END. 
    ELSE IF input-payload.bill-name = "" THEN 
    DO:
      FOR EACH debitor WHERE debitor.artnr =/* artikel.artnr */ input-payload.temp-art2
        AND debitor.rgdatum GE from-date
        AND debitor.rgdatum LE to-date AND debitor.opart LT 2 
        NO-LOCK BY debitor.zahlkonto BY debitor.rgdatum: 
        IF debitor.counter NE 0 THEN FIND FIRST age-list 
          WHERE age-list.counter = debitor.counter NO-ERROR. 
        IF NOT AVAILABLE age-list OR debitor.counter = 0 THEN 
        DO: 
          create age-list. 
          age-list.ar-recid     = RECID(debitor). 
          age-list.rgdatum      = debitor.rgdatum. 
          age-list.counter      = debitor.counter. 
          age-list.rechnr       = debitor.rechnr. 
          age-list.refno        = debitor.debref. 
          age-list.gastnr       = debitor.gastnr. 
          age-list.gastnrmember = debitor.gastnrmember. 
          age-list.zinr         = debitor.zinr. 
          age-list.dptNo        = debitor.betriebsnr. /* Naufal Afthar - 992296*/
          
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
          age-list.billname = guest.name + ", " + guest.vorname1 
            + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnrmember 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE guest THEN age-list.gastname = guest.name + ", " 
            + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
          FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
              AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
              (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.transzeit + 2))
              NO-LOCK NO-ERROR.

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
             IF bill.reslinnr = 0 THEN 
                 ASSIGN age-list.resnr = bill.resnr
                        age-list.mbill = "*".
          END.

          /*ITA 121213*/
          IF debitor.vesrcod MATCHES "*resno:*" THEN
          DO:
                /*IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                t-resnr = INT(SUBSTR(debitor.vesrcod, 26, LENGTH(debitor.vesrcod) - 1))
                  NO-ERROR.
                ELSE
                ASSIGN
                    t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                    t-resnr = INT(SUBSTR(t-name, 26, LENGTH(t-name) - 1)) NO-ERROR
                .
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.*/

              /*ITA 121016*/
                IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                      ASSIGN t-resnr = INT(TRIM(ENTRY(2, ENTRY(1, debitor.vesrcod, ";"), ":"))).
                ELSE
                    ASSIGN
                        t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                        t-resnr = INT(TRIM(ENTRY(2, t-name, ":"))).
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    age-list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.
          END.

          IF(debitor.vesrcod MATCHES "*;*") THEN
          ASSIGN
              age-list.vouc-nr = TRIM(ENTRY(2, debitor.vesrcod, ";"))
              age-list.remarks = TRIM(ENTRY(1, debitor.vesrcod, ";")).
          ELSE
          DO:
              age-list.remarks = debitor.vesrcod.
              FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr
                  AND bill-line.betrag = (- debitor.saldo) AND (bill-line.zeit GE 
                  (debitor.transzeit - 2) AND (bill-line.zeit LE debitor.transzeit + 2))
                  NO-LOCK NO-ERROR.
              IF AVAILABLE bill-line THEN
              DO:
                   DO i = 1 TO (LENGTH(bill-line.bezeich)):
                      IF SUBSTR(bill-line.bezeich, i, 1) = "/"   THEN
                      DO:
                          age-list.vouc-nr = SUBSTR(bill-line.bezeich, (i + 1), 
                                                    (LENGTH(bill-line.bezeich) - i )).
                          i = LENGTH(bill-line.bezeich).
                      END.
                  END.
                  /*age-list.vouc-nr = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
              END.
          END.
          
          /*IF AVAILABLE bill-line THEN
          DO:
               DO i = 1 TO (LENGTH(bill-line.bezeich)):
                  IF SUBSTR(bill-line.bezeich, i, 1) = "/"   THEN
                  DO:
                      age-list.vouc-nr = SUBSTR(bill-line.bezeich, (i + 1), 
                                                (LENGTH(bill-line.bezeich) - i )).
                      i = LENGTH(bill-line.bezeich).
                  END.
              END.
              /*age-list.vouc-nr = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
          END.*/
        END. 
        IF debitor.zahlkonto = 0 THEN 
        DO: 
          /*ITA age-list.user-init = userinit. */
          FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr NO-LOCK NO-ERROR.
          IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit.
          age-list.rgdatum = debitor.rgdatum. 
          age-list.debt = age-list.debt + debitor.saldo. 
          age-list.debt-foreign = age-list.debt-foreign + debitor.vesrdep. 
          
          RUN disp-guest-debt.
          
          IF debitor.betrieb-gastmem NE 0 THEN 
          DO: 
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
              debitor.betrieb-gastmem NO-LOCK NO-ERROR. 
            IF AVAILABLE waehrung THEN age-list.currency = waehrung.wabkurz. 
          END. 
        END. 
        ELSE 
        DO: 
          age-list.credit = age-list.credit - debitor.saldo. 
        END. 
        age-list.tot-debt = age-list.tot-debt + debitor.saldo. 
      END. 
    END. 
    art-selected = 1. 
    IF input-payload.bill-saldo NE 0 THEN 
    FOR EACH age-list WHERE age-list.tot-debt NE input-payload.bill-saldo: 
        DELETE age-list. 
    END. 
  END. 
  RELEASE abuff.
END. 


PROCEDURE disp-guest-debt: 
DEFINE VARIABLE gastnr AS INTEGER. 
DEFINE BUFFER age-list1 FOR age-list. 
  DEFINE BUFFER debt FOR debitor. 
  ASSIGN age-list.b-resname = "Previous Payment Remark:". 
    IF debitor.counter NE 0 THEN 
    DO: 
      age-list.b-resname = "Payment Remark:". 
      FOR EACH debt WHERE debt.counter = debitor.counter 
        AND debt.opart = 1 NO-LOCK: 
        IF debt.vesrcod NE "" THEN 
        age-list.b-resname = age-list.b-resname + chr(10) + STRING(debt.rgdatum) + " " 
        + TRIM(STRING(debt.saldo,"->>>,>>>,>>9.99")) + ": " + debt.vesrcod. 
      END. 
    END.
 
    IF age-list.b-resname = "Payment Remark:" THEN age-list.b-resname = "". 
    ELSE age-list.b-resname = age-list.b-resname + chr(10) + chr(10). 
 
    FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
    age-list.b-resname = age-list.b-resname + guest.name + ", " + guest.vorname1 + guest.anredefirma 
            + " " + guest.anrede1 
            + chr(10) + guest.adresse1 
            + chr(10) + guest.wohnort + " " + guest.plz. 
END. 

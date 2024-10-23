
DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF INPUT-OUTPUT PARAMETER pax       AS INT.
DEF INPUT PARAMETER curr-tischnr     AS INTEGER. 
DEF INPUT PARAMETER rec-id           AS INT.
DEF INPUT PARAMETER curr-dept        AS INT.
DEF INPUT PARAMETER tischnr          AS INT.
DEF INPUT PARAMETER bilrecid         AS INT.
DEF INPUT PARAMETER rechnr           AS INT.
DEF INPUT PARAMETER curr-waiter      AS INT.
DEF INPUT PARAMETER new-waiter       AS INT.

DEF OUTPUT PARAMETER bill-date       AS DATE.
DEF OUTPUT PARAMETER printed         AS CHAR.
DEF OUTPUT PARAMETER balance         AS DECIMAL.
DEF OUTPUT PARAMETER balance-foreign AS DECIMAL.
DEF OUTPUT PARAMETER fl-code         AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code1        AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code2        AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

DEFINE BUFFER buf-bill FOR h-bill.
DEFINE BUFFER buffq251 FOR queasy.
DEFINE BUFFER buffq33  FOR queasy.

/*FD August 02, 2022*/
DEFINE VARIABLE flag-move AS LOGICAL INITIAL NO.
DEFINE VARIABLE old-billno AS INTEGER.
DEFINE VARIABLE curr-recid AS INTEGER.
DEFINE VARIABLE active-deposit AS LOGICAL INITIAL NO.

FIND FIRST htparam WHERE htparam.paramnr EQ 588 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN active-deposit = htparam.flogical.

/*ITA add validasi when user transfer one more time.*/
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN DO:
    old-billno = h-bill.rechnr.
    FIND FIRST buf-bill WHERE buf-bill.rechnr = rechnr
        AND buf-bill.departement = curr-dept
        AND buf-bill.tischnr = curr-tischnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE buf-bill THEN DO: 
        ASSIGN fl-code = 2.
        RETURN.
    END.
END.

RUN move-table.
FIND CURRENT h-bill NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill.
    ASSIGN t-h-bill.rec-id = RECID(h-bill).
END.

/*FD August 02, 2022*/
IF flag-move THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 230 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        IF bilrecid NE 0 THEN RUN selforder-moveto-occtable. /*Occupied Table*/
        ELSE RUN selforder-moveto-emptytable. /*Empty Table*/
    END.

    /*FD Dec 05, 2022 => Feature Deposit Resto*/
    IF active-deposit THEN
    DO:
        IF bilrecid NE 0 THEN curr-recid = bilrecid.
        ELSE curr-recid = rec-id.
    
        FIND FIRST buffq251 WHERE buffq251.KEY EQ 251
            AND buffq251.number1 EQ curr-recid NO-LOCK NO-ERROR.
        IF AVAILABLE buffq251 THEN
        DO:
            FIND FIRST buffq33 WHERE RECID(buffq33) EQ buffq251.number2 NO-LOCK NO-ERROR.
            IF AVAILABLE buffq33 THEN
            DO:
                FIND CURRENT buffq33 EXCLUSIVE-LOCK.
                buffq33.number2 = tischnr.
                IF NUM-ENTRIES(buffq33.char3, ";") LE 3 THEN
                DO:
                    buffq33.char3 = buffq33.char3 + "Move Table From " + STRING(curr-tischnr) + " to " 
                        + STRING(tischnr) + " - UserID " + STRING(curr-waiter).
                END.
    
                FIND CURRENT buffq33 NO-LOCK.
                RELEASE buffq33.
            END.  
    
            IF bilrecid NE 0 THEN 
            DO:
                FIND CURRENT buffq251 EXCLUSIVE-LOCK.
                buffq251.number1 = curr-recid.
                FIND CURRENT buffq251 NO-LOCK.
                RELEASE buffq251.
            END.
        END.  
    END.    
END.    

/****************************************** PROCEDURE *******************************************/
PROCEDURE move-table:
  DEFINE VARIABLE new-rechnr            AS INTEGER. 
  DEFINE VARIABLE curr-saldo            AS DECIMAL. 
  DEFINE BUFFER h-bill1                 FOR vhp.h-bill. 
  DEFINE BUFFER qbuff                   FOR vhp.queasy. 
  DEFINE BUFFER hbline                  FOR vhp.h-bill-line.

  new-rechnr = vhp.h-bill.rechnr. 
  
  DO TRANSACTION: 
    
    FIND FIRST vhp.queasy WHERE vhp.queasy.KEY = 31 
      AND vhp.queasy.number1 = curr-dept
      AND vhp.queasy.number2 = curr-tischnr /*EXCLUSIVE-LOCK*/ NO-LOCK NO-ERROR.
    FIND FIRST qbuff WHERE qbuff.KEY = 31 
      AND qbuff.number1 = curr-dept
      AND qbuff.number2 = tischnr /*EXCLUSIVE-LOCK*/ NO-LOCK NO-ERROR.
    IF AVAILABLE qbuff AND qbuff.date1 = ? THEN
    DO:
      FIND CURRENT qbuff EXCLUSIVE-LOCK.
      IF AVAILABLE vhp.queasy THEN
      ASSIGN
        qbuff.number3 = vhp.queasy.number3
        qbuff.date1   = vhp.queasy.date1
      .
      ELSE
      ASSIGN
        qbuff.number3 = TIME
        qbuff.date1   = TODAY
      .
    END.
    IF AVAILABLE qbuff THEN FIND CURRENT qbuff NO-LOCK.
    RELEASE qbuff.
    
    FIND FIRST vhp.tisch WHERE vhp.tisch.tischnr =  tischnr 
      AND vhp.tisch.departement = curr-dept NO-LOCK NO-ERROR. 
    IF bilrecid = 0 THEN 
    DO: 
      curr-tischnr = vhp.h-bill.tischnr. 
      curr-saldo = vhp.h-bill.saldo. 
      FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
      vhp.h-bill.tischnr =  tischnr. 
      vhp.h-bill.rgdruck = 0. 
      FIND CURRENT vhp.h-bill NO-LOCK. 
    END. 
    ELSE 
    DO: 
      curr-tischnr = vhp.h-bill.tischnr. 
      curr-saldo = vhp.h-bill.saldo. 
      FIND FIRST h-bill1 WHERE RECID(vhp.h-bill1) = bilrecid EXCLUSIVE-LOCK. 
      ASSIGN
        h-bill1.saldo    = h-bill1.saldo + curr-saldo
        h-bill1.mwst[99] = h-bill1.mwst[99] + vhp.h-bill.mwst[99]
        h-bill1.tischnr  = tischnr 
        new-rechnr       = h-bill1.rechnr 
        h-bill1.rgdruck  = 0
        h-bill1.belegung = h-bill1.belegung + vhp.h-bill.belegung
        pax              = h-bill1.belegung
      . 
      FIND CURRENT h-bill1 NO-LOCK.
      fl-code = 1.
      FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
      ASSIGN
        vhp.h-bill.saldo    = 0 
        vhp.h-bill.mwst[99] = 0 
        vhp.h-bill.flag     = 1
      . 
      FIND CURRENT vhp.h-bill NO-LOCK. 
    END. 
 
    IF AVAILABLE vhp.queasy THEN
    DO:
      FIND CURRENT vhp.queasy EXCLUSIVE-LOCK.
      ASSIGN vhp.queasy.number3 = 0
             vhp.queasy.date1 = ?.
      FIND CURRENT vhp.queasy NO-LOCK.
      RELEASE vhp.queasy.
    END.
    
    FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = rechnr 
        AND vhp.h-bill-line.departement = curr-dept NO-LOCK:
        FIND FIRST hbline WHERE RECID(hbline) = RECID(vhp.h-bill-line) NO-LOCK NO-ERROR.
        FIND CURRENT hbline EXCLUSIVE-LOCK.
        ASSIGN
            bill-date = vhp.h-bill-line.bill-datum
            hbline.tischnr =  tischnr
            hbline.rechnr = new-rechnr
            hbline.waehrungsnr = 0 
        .
        FIND CURRENT hbline NO-LOCK.
        RELEASE hbline.
    END. 
 
    FOR EACH vhp.h-journal WHERE vhp.h-journal.rechnr = rechnr 
      AND vhp.h-journal.departement = curr-dept
      AND vhp.h-journal.bill-datum = bill-date:
      ASSIGN
          vhp.h-journal.tischnr =  tischnr
          vhp.h-journal.rechnr = new-rechnr
      .
    END. 

    CREATE vhp.h-journal. 
    vhp.h-journal.rechnr = vhp.h-bill.rechnr. 
    IF bilrecid NE 0 THEN 
      vhp.h-journal.bezeich = "To Table " + STRING(vhp.h-bill1.tischnr) 
      + " *" + STRING(vhp.h-bill1.rechnr). 
    ELSE 
    vhp.h-journal.bezeich = "To Table " + STRING(tischnr) 
      + " *" + STRING(vhp.h-bill.rechnr). 
    ASSIGN
      vhp.h-journal.tischnr = curr-tischnr  /* table# TO be transferred */ 
      vhp.h-journal.departement = vhp.h-bill.departement
      vhp.h-journal.zeit = TIME
      vhp.h-journal.kellner-nr = curr-waiter
      vhp.h-journal.bill-datum = bill-date
      vhp.h-journal.artnrfront = 0
      vhp.h-journal.aendertext = "" 
      vhp.h-journal.betrag = - curr-saldo
    . 
    FIND CURRENT vhp.h-journal NO-LOCK. 
 
    CREATE vhp.h-journal. 
    IF bilrecid NE 0 THEN vhp.h-journal.rechnr = h-bill1.rechnr. 
    ELSE vhp.h-journal.rechnr = vhp.h-bill.rechnr. 
    vhp.h-journal.bezeich = "From Table " + STRING(curr-tischnr) 
      + " *" + STRING(vhp.h-bill.rechnr). 
    vhp.h-journal.tischnr =  tischnr.  /* Transfer TO this table# */ 
    vhp.h-journal.departement = vhp.h-bill.departement. 
    vhp.h-journal.zeit = time. 
    vhp.h-journal.kellner-nr = curr-waiter. 
    vhp.h-journal.bill-datum = bill-date. 
    vhp.h-journal.artnrfront = 0. 
    vhp.h-journal.aendertext = "". 
    vhp.h-journal.betrag = curr-saldo. 
    FIND CURRENT vhp.h-journal NO-LOCK. 
  END. 
 
  IF curr-waiter = new-waiter THEN 
  DO: 
    rechnr = new-rechnr. 
    FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr =  tischnr 
      AND vhp.h-bill.departement = curr-dept NO-LOCK. 
    printed = "". 
    balance = vhp.h-bill.saldo. 
    balance-foreign = vhp.h-bill.mwst[99].
    fl-code1 = 1.
  END. 
  ELSE fl-code2 = 1.

  flag-move = YES.
END. 

/*********************************************************************************
                               SELFORDER MOVE TABLE
*********************************************************************************/
PROCEDURE selforder-moveto-emptytable:
DEFINE BUFFER pickup-table          FOR queasy.
DEFINE BUFFER orderbill             FOR queasy.
DEFINE BUFFER b-orderbill           FOR queasy.
DEFINE BUFFER orderbill-line        FOR queasy.
DEFINE BUFFER b-orderbill-line      FOR queasy.
DEFINE BUFFER paygateway-session    FOR queasy.
DEFINE BUFFER b-pg-session          FOR queasy.
DEFINE BUFFER selforder-session     FOR queasy.
DEFINE BUFFER genparamso            FOR queasy.
DEFINE BUFFER buff-hbill            FOR h-bill.

DEFINE VARIABLE sessionID-one       AS CHARACTER.
DEFINE VARIABLE sessionID-two       AS CHARACTER.
DEFINE VARIABLE mess-str            AS CHARACTER.
DEFINE VARIABLE mess-token          AS CHARACTER.
DEFINE VARIABLE mess-keyword        AS CHARACTER.
DEFINE VARIABLE mess-value          AS CHARACTER.
DEFINE VARIABLE guest-name          AS CHARACTER.
DEFINE VARIABLE i-str               AS INTEGER.
DEFINE VARIABLE validate-rechnr     AS INTEGER.
DEFINE VARIABLE bill-no             AS INTEGER.
DEFINE VARIABLE dynamic-qr          AS LOGICAL.
DEFINE VARIABLE room-serviceflag    AS LOGICAL.
DEFINE VARIABLE hbill-date          AS DATE.
                
    /*SEARCH EVERY VALUE IN GENPARAM FOR SELFORDER*/
    FOR EACH genparamso WHERE genparamso.KEY EQ 222 
        AND genparamso.number1 EQ 1 
        AND genparamso.betriebsnr EQ curr-dept NO-LOCK:
        IF genparamso.number2 EQ 14 THEN dynamic-qr = genparamso.logi1.
        IF genparamso.number2 EQ 21 THEN room-serviceflag = genparamso.logi1.
    END.

    IF NOT dynamic-qr THEN /*STATIC QR*/
    DO:
        /*SEARCH SESSION OLD TABLE*/
        FIND FIRST pickup-table WHERE pickup-table.key EQ 225
            AND pickup-table.char1 EQ "taken-table"
            AND pickup-table.logi1 EQ YES
            AND pickup-table.logi2 EQ NO
            AND pickup-table.number1 EQ curr-dept
            AND pickup-table.number2 EQ curr-tischnr NO-LOCK NO-ERROR.
        IF AVAILABLE pickup-table THEN
        DO:
            sessionID-one = ENTRY(1, pickup-table.char3, "|").
        END.
    
        /*SEARCH SESSION NEW TABLE*/
        FIND FIRST pickup-table WHERE pickup-table.key EQ 225
            AND pickup-table.char1 EQ "taken-table"
            AND pickup-table.logi1 EQ YES
            AND pickup-table.logi2 EQ NO
            AND pickup-table.number1 EQ curr-dept
            AND pickup-table.number2 EQ tischnr NO-LOCK NO-ERROR.
        IF AVAILABLE pickup-table THEN
        DO:
            sessionID-two = ENTRY(1, pickup-table.char3, "|").                      
        END.
    END.
    ELSE /*DYANMIC QR*/
    DO:
        /*SEARCH SESSION OLD TABLE*/
        FIND FIRST pickup-table WHERE pickup-table.key EQ 225
            AND pickup-table.char1 EQ "taken-table"
            AND pickup-table.logi1 EQ YES
            AND pickup-table.logi2 EQ YES
            AND pickup-table.number1 EQ curr-dept
            AND pickup-table.number2 EQ curr-tischnr
            AND LENGTH(ENTRY(1, pickup-table.char3, "|")) LE 20 NO-LOCK NO-ERROR.
        IF AVAILABLE pickup-table THEN
        DO:             
            sessionID-one = ENTRY(1, pickup-table.char3, "|").                           
        END.
    
        /*SEARCH SESSION NEW TABLE*/
        FIND FIRST pickup-table WHERE pickup-table.key EQ 225
            AND pickup-table.char1 EQ "taken-table"
            AND pickup-table.logi1 EQ YES
            AND pickup-table.logi2 EQ YES
            AND pickup-table.number1 EQ curr-dept
            AND pickup-table.number2 EQ tischnr 
            AND LENGTH(ENTRY(1, pickup-table.char3, "|")) LE 20 NO-LOCK NO-ERROR.
        IF AVAILABLE pickup-table THEN
        DO:            
            sessionID-two = ENTRY(1, pickup-table.char3, "|"). 

            mess-str = pickup-table.char2.
            DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
                mess-token   = ENTRY(i-str,mess-str,"|").
                mess-keyword = ENTRY(1,mess-token,"=").
                mess-value   = ENTRY(2,mess-token,"=").

                IF mess-keyword EQ "NM" THEN guest-name = mess-value.  
                IF guest-name NE "" THEN LEAVE.
            END.                               
        END.
    END.
           
    FIND FIRST h-bill-line WHERE h-bill-line.rechnr EQ rechnr
        AND h-bill-line.departement EQ curr-dept NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill-line THEN
    DO:
        hbill-date = h-bill-line.bill-datum.
    END.
    
    /*CHECK IF ORDER NOT FROM SELFORDER, RETURN IT*/
    FIND FIRST orderbill WHERE orderbill.key EQ 225
        AND orderbill.char1 EQ "orderbill"
        AND orderbill.number1 EQ curr-dept
        AND orderbill.number2 EQ curr-tischnr
        AND orderbill.char3 EQ sessionID-one        
        AND orderbill.logi1 EQ YES
        /*AND orderbill.logi3 EQ YES*/ NO-LOCK NO-ERROR.
    IF NOT AVAILABLE orderbill THEN
    DO:
        RETURN.
    END.

    /*UPDATE SESSION FROM OLD TABLE TO NEW TABLE*/
    DO TRANSACTION:
        FIND FIRST selforder-session WHERE selforder-session.key EQ 230
            AND selforder-session.number1 EQ curr-dept
            AND selforder-session.number2 EQ curr-tischnr
            AND selforder-session.char1 EQ sessionID-one
            AND selforder-session.logi1 EQ NO /*EXCLUSIVE-LOCK*/ NO-LOCK NO-ERROR.
        IF AVAILABLE selforder-session THEN
        DO:
            FOR EACH orderbill WHERE orderbill.key EQ 225
                AND orderbill.char1 EQ "orderbill"
                AND orderbill.number1 EQ curr-dept
                AND orderbill.number2 EQ curr-tischnr
                AND orderbill.char3 EQ sessionID-one
                AND orderbill.logi1 EQ YES
                AND orderbill.logi3 EQ YES
                NO-LOCK BY orderbill.number3:
        
                mess-str = orderbill.char2.
                DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
                    mess-token   = ENTRY(i-str,mess-str,"|").
                    mess-keyword = ENTRY(1,mess-token,"=").
                    mess-value   = ENTRY(2,mess-token,"=").

                    IF mess-keyword EQ "BL" THEN validate-rechnr = INT(mess-value).                    
                    IF validate-rechnr NE 0 THEN LEAVE.
                END.
                
                /*UPDATE ORDERBILL*/
                FIND FIRST b-orderbill WHERE RECID(b-orderbill) EQ RECID(orderbill) NO-LOCK NO-ERROR.
                IF AVAILABLE b-orderbill THEN
                DO:
                    FIND CURRENT b-orderbill EXCLUSIVE-LOCK.
                    ASSIGN
                        b-orderbill.number1 = curr-dept
                        b-orderbill.number2 = tischnr     
                        b-orderbill.char3   = sessionID-two                        
                    .                                     

                    IF NOT dynamic-qr THEN /*STATIC QR*/
                    DO:
                        ENTRY(2, b-orderbill.char2, "|") = "NM=GuestTable" + STRING(tischnr).
                    END.
                    ELSE /*DYANMIC QR*/
                    DO:
                        ENTRY(2, b-orderbill.char2, "|") = "NM=" + guest-name.
                    END.
                    FIND CURRENT b-orderbill NO-LOCK.
                    RELEASE b-orderbill.
                END.
            END.
                      
            /*UPDATE ORDERBILL-LINE*/
            FOR EACH orderbill-line WHERE orderbill-line.key EQ 225
                AND orderbill-line.char1 EQ "orderbill-line"
                AND orderbill-line.number2 EQ curr-tischnr
                AND ENTRY(1, orderbill-line.char2, "|") EQ STRING(curr-dept)
                AND ENTRY(4, orderbill-line.char2, "|") EQ sessionID-one
                AND orderbill-line.logi2
                AND orderbill-line.logi3 NO-LOCK:
                
                FIND FIRST b-orderbill-line WHERE RECID(b-orderbill-line) EQ RECID(orderbill-line) NO-LOCK NO-ERROR.
                IF AVAILABLE b-orderbill-line THEN
                DO:
                    FIND CURRENT b-orderbill-line EXCLUSIVE-LOCK.
                    ASSIGN                        
                        b-orderbill-line.number2 = tischnr
                        ENTRY(1, b-orderbill-line.char2, "|") = STRING(curr-dept)
                        ENTRY(2, b-orderbill-line.char2, "|") = STRING(tischnr)
                        ENTRY(4, b-orderbill-line.char2, "|") = sessionID-two
                    .
                    FIND CURRENT b-orderbill-line NO-LOCK.
                    RELEASE b-orderbill-line.
                END.
            END.          
            
            IF dynamic-qr THEN
            DO:
                FIND CURRENT selforder-session EXCLUSIVE-LOCK.
                selforder-session.logi1 = YES.
                FIND CURRENT selforder-session NO-LOCK.

                /*EXPIRATION SESSION OLD PICKUP TABLE*/
                FIND FIRST pickup-table WHERE pickup-table.key EQ 225
                    AND pickup-table.char1 EQ "taken-table"
                    AND pickup-table.logi1 EQ YES
                    AND pickup-table.logi2 EQ YES
                    AND pickup-table.number1 EQ curr-dept
                    AND pickup-table.number2 EQ curr-tischnr                   
                    AND ENTRY(1, pickup-table.char3, "|") EQ sessionID-one NO-LOCK NO-ERROR.
                IF AVAILABLE pickup-table THEN
                DO:             
                    FIND CURRENT pickup-table EXCLUSIVE-LOCK.
                    ENTRY(1, pickup-table.char3, "|") = sessionID-one + "T" 
                        + REPLACE(STRING(TODAY),"/","") 
                        + REPLACE(STRING(TIME,"HH:MM"),":","").
                    FIND CURRENT pickup-table NO-LOCK.
                    RELEASE pickup-table.
                END.
            END.
                
            FIND FIRST paygateway-session WHERE paygateway-session.key EQ 223
                AND paygateway-session.number1 EQ curr-dept
                AND paygateway-session.char3 EQ sessionID-one 
                AND paygateway-session.betriebsnr EQ rechnr NO-LOCK NO-ERROR.
            IF AVAILABLE paygateway-session THEN
            DO:
                bill-no = paygateway-session.betriebsnr.
                FIND FIRST b-pg-session WHERE b-pg-session.key EQ 223
                    AND b-pg-session.number1 EQ curr-dept
                    AND b-pg-session.char3 EQ sessionID-two  NO-LOCK NO-ERROR.
                IF AVAILABLE b-pg-session THEN
                DO:
                    FIND CURRENT b-pg-session EXCLUSIVE-LOCK.
                    b-pg-session.betriebsnr = bill-no.
                    FIND CURRENT b-pg-session NO-LOCK.
                    RELEASE b-pg-session.
                END.

                FIND CURRENT paygateway-session EXCLUSIVE-LOCK.
                paygateway-session.betriebsnr = 0.
                FIND CURRENT paygateway-session NO-LOCK.
                RELEASE paygateway-session.
            END.
            
            RELEASE selforder-session.
        END.            
    END.
END PROCEDURE.

PROCEDURE selforder-moveto-occtable:
DEFINE BUFFER pickup-table          FOR queasy.
DEFINE BUFFER orderbill             FOR queasy.
DEFINE BUFFER b-orderbill           FOR queasy.
DEFINE BUFFER orderbill-line        FOR queasy.
DEFINE BUFFER b-orderbill-line      FOR queasy.
DEFINE BUFFER paygateway-session    FOR queasy.
DEFINE BUFFER b-pg-session          FOR queasy.
DEFINE BUFFER selforder-session     FOR queasy.
DEFINE BUFFER genparamso            FOR queasy.
DEFINE BUFFER buff-hbill            FOR h-bill.

DEFINE VARIABLE sessionID-one       AS CHARACTER.
DEFINE VARIABLE sessionID-two       AS CHARACTER.
DEFINE VARIABLE mess-str            AS CHARACTER.
DEFINE VARIABLE mess-token          AS CHARACTER.
DEFINE VARIABLE mess-keyword        AS CHARACTER.
DEFINE VARIABLE mess-value          AS CHARACTER.
DEFINE VARIABLE guest-name          AS CHARACTER.
DEFINE VARIABLE i-str               AS INTEGER.
DEFINE VARIABLE validate-rechnr     AS INTEGER.
DEFINE VARIABLE bill-no             AS INTEGER.
DEFINE VARIABLE new-billno          AS INTEGER.
DEFINE VARIABLE orderbill-counter   AS INTEGER.
DEFINE VARIABLE orderbill-count     AS INTEGER.
DEFINE VARIABLE orderbill-line-count AS INTEGER.
DEFINE VARIABLE dynamic-qr          AS LOGICAL.
DEFINE VARIABLE room-serviceflag    AS LOGICAL.
DEFINE VARIABLE hbill-date          AS DATE.

    /*SEARCH EVERY VALUE IN GENPARAM FOR SELFORDER*/
    FOR EACH genparamso WHERE genparamso.KEY EQ 222 
        AND genparamso.number1 EQ 1 
        AND genparamso.betriebsnr EQ curr-dept NO-LOCK:
        IF genparamso.number2 EQ 14 THEN dynamic-qr = genparamso.logi1.
        IF genparamso.number2 EQ 21 THEN room-serviceflag = genparamso.logi1.
    END.

    IF NOT dynamic-qr THEN /*STATIC QR*/
    DO:
        /*SEARCH SESSION OLD TABLE*/
        FIND FIRST pickup-table WHERE pickup-table.key EQ 225
            AND pickup-table.char1 EQ "taken-table"
            AND pickup-table.logi1 EQ YES
            AND pickup-table.logi2 EQ NO
            AND pickup-table.number1 EQ curr-dept
            AND pickup-table.number2 EQ curr-tischnr NO-LOCK NO-ERROR.
        IF AVAILABLE pickup-table THEN
        DO:
            sessionID-one = ENTRY(1, pickup-table.char3, "|").
        END.
    
        /*SEARCH SESSION NEW TABLE*/
        FIND FIRST pickup-table WHERE pickup-table.key EQ 225
            AND pickup-table.char1 EQ "taken-table"
            AND pickup-table.logi1 EQ YES
            AND pickup-table.logi2 EQ NO
            AND pickup-table.number1 EQ curr-dept
            AND pickup-table.number2 EQ tischnr NO-LOCK NO-ERROR.
        IF AVAILABLE pickup-table THEN
        DO:
            sessionID-two = ENTRY(1, pickup-table.char3, "|").                      
        END.
    END.
    ELSE /*DYANMIC QR*/
    DO:
        /*SEARCH SESSION OLD TABLE*/
        FIND FIRST pickup-table WHERE pickup-table.key EQ 225
            AND pickup-table.char1 EQ "taken-table"
            AND pickup-table.logi1 EQ YES
            AND pickup-table.logi2 EQ YES
            AND pickup-table.number1 EQ curr-dept
            AND pickup-table.number2 EQ curr-tischnr
            AND LENGTH(ENTRY(1, pickup-table.char3, "|")) LE 20 NO-LOCK NO-ERROR.
        IF AVAILABLE pickup-table THEN
        DO:             
            sessionID-one = ENTRY(1, pickup-table.char3, "|").                           
        END.
    
        /*SEARCH SESSION NEW TABLE*/
        FIND FIRST pickup-table WHERE pickup-table.key EQ 225
            AND pickup-table.char1 EQ "taken-table"
            AND pickup-table.logi1 EQ YES
            AND pickup-table.logi2 EQ YES
            AND pickup-table.number1 EQ curr-dept
            AND pickup-table.number2 EQ tischnr 
            AND LENGTH(ENTRY(1, pickup-table.char3, "|")) LE 20 NO-LOCK NO-ERROR.
        IF AVAILABLE pickup-table THEN
        DO:            
            sessionID-two = ENTRY(1, pickup-table.char3, "|"). 

            mess-str = pickup-table.char2.
            DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
                mess-token   = ENTRY(i-str,mess-str,"|").
                mess-keyword = ENTRY(1,mess-token,"=").
                mess-value   = ENTRY(2,mess-token,"=").

                IF mess-keyword EQ "NM" THEN guest-name = mess-value.  
                IF guest-name NE "" THEN LEAVE.
            END.                               
        END.
    END.
    
    FIND FIRST h-bill WHERE RECID(h-bill) EQ bilrecid NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN
    DO:
        FIND FIRST h-bill-line WHERE h-bill-line.rechnr EQ rechnr
            AND h-bill-line.departement EQ curr-dept NO-LOCK NO-ERROR.
        IF AVAILABLE h-bill-line THEN
        DO:
            hbill-date = h-bill-line.bill-datum.
        END.
    END.
        
    /*CHECK IF ORDER NOT FROM SELFORDER, RETURN IT*/
    FIND FIRST orderbill WHERE orderbill.key EQ 225
        AND orderbill.char1 EQ "orderbill"
        AND orderbill.number1 EQ curr-dept
        AND orderbill.number2 EQ curr-tischnr
        AND orderbill.char3 EQ sessionID-one        
        AND orderbill.logi1 EQ YES
        /*AND orderbill.logi3 EQ YES*/ NO-LOCK NO-ERROR.
    IF NOT AVAILABLE orderbill THEN
    DO:
        RETURN.
    END.

    /*UPDATE SESSION FROM OLD TABLE TO NEW TABLE*/
    DO TRANSACTION:
        FIND FIRST selforder-session WHERE selforder-session.key EQ 230
            AND selforder-session.number1 EQ curr-dept
            AND selforder-session.number2 EQ curr-tischnr
            AND selforder-session.char1 EQ sessionID-one
            AND selforder-session.logi1 EQ NO /*EXCLUSIVE-LOCK*/ NO-LOCK NO-ERROR.
        IF AVAILABLE selforder-session THEN
        DO:
            /*GET BILL NUMBER NEW TABLE*/
            FIND FIRST buff-hbill WHERE RECID(buff-hbill) EQ bilrecid NO-LOCK NO-ERROR.
            IF AVAILABLE buff-hbill THEN new-billno = buff-hbill.rechnr.

            /*GET ORDERBILL COUNTER*/
            FOR EACH orderbill WHERE orderbill.key EQ 225
                AND orderbill.char1 EQ "orderbill"
                AND orderbill.number1 EQ curr-dept
                AND orderbill.number2 EQ tischnr
                AND orderbill.char3 EQ sessionID-two
                AND orderbill.logi1 EQ YES
                AND orderbill.logi3 EQ YES
                NO-LOCK BY orderbill.number3 DESC:
                
                orderbill-counter = orderbill.number3.                
                LEAVE.
            END.                      

            FOR EACH orderbill WHERE orderbill.key EQ 225
                AND orderbill.char1 EQ "orderbill"
                AND orderbill.number1 EQ curr-dept
                AND orderbill.number2 EQ curr-tischnr
                AND orderbill.char3 EQ sessionID-one
                AND orderbill.logi1 EQ YES
                AND orderbill.logi3 EQ YES
                NO-LOCK BY orderbill.number3:
                
                orderbill-counter = orderbill-counter + 1.                         

                mess-str = orderbill.char2.
                DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
                    mess-token   = ENTRY(i-str,mess-str,"|").
                    mess-keyword = ENTRY(1,mess-token,"=").
                    mess-value   = ENTRY(2,mess-token,"=").

                    IF mess-keyword EQ "BL" THEN validate-rechnr = INT(mess-value).                    
                    IF validate-rechnr NE 0 THEN LEAVE.
                END.
                
                /*UPDATE ORDERBILL-LINE*/
                FOR EACH orderbill-line WHERE orderbill-line.key EQ 225
                    AND orderbill-line.char1 EQ "orderbill-line"
                    AND orderbill-line.number1 EQ orderbill.number3
                    AND orderbill-line.number2 EQ curr-tischnr
                    AND ENTRY(1, orderbill-line.char2, "|") EQ STRING(curr-dept)
                    AND ENTRY(4, orderbill-line.char2, "|") EQ sessionID-one
                    AND orderbill-line.logi2
                    AND orderbill-line.logi3 NO-LOCK:                                               
    
                    FIND FIRST b-orderbill-line WHERE RECID(b-orderbill-line) EQ RECID(orderbill-line) NO-LOCK NO-ERROR.
                    IF AVAILABLE b-orderbill-line THEN
                    DO:
                        FIND CURRENT b-orderbill-line EXCLUSIVE-LOCK.
                        ASSIGN
                            b-orderbill-line.number1 = orderbill-counter
                            b-orderbill-line.number2 = tischnr                                
                            ENTRY(1, b-orderbill-line.char2, "|") = STRING(curr-dept)
                            ENTRY(2, b-orderbill-line.char2, "|") = STRING(tischnr)
                            ENTRY(4, b-orderbill-line.char2, "|") = sessionID-two
                        .
                        FIND CURRENT b-orderbill-line NO-LOCK.
                        RELEASE b-orderbill-line.
                    END.
                END.      

                /*UPDATE ORDERBILL*/
                FIND FIRST b-orderbill WHERE RECID(b-orderbill) EQ RECID(orderbill) NO-LOCK NO-ERROR.
                IF AVAILABLE b-orderbill THEN
                DO:
                    FIND CURRENT b-orderbill EXCLUSIVE-LOCK.
                    ASSIGN
                        b-orderbill.number1 = curr-dept
                        b-orderbill.number2 = tischnr  
                        b-orderbill.number3 = orderbill-counter
                        b-orderbill.char3   = sessionID-two                        
                    .                   

                    IF NUM-ENTRIES(b-orderbill.char2, "|") GE 8 THEN
                    DO:
                        ASSIGN
                            b-orderbill.betriebsnr = bilrecid
                            ENTRY(8, b-orderbill.char2, "|") = "BL=" + STRING(new-billno)
                        .
                    END.

                    IF NOT dynamic-qr THEN /*STATIC QR*/
                    DO:
                        ENTRY(2, b-orderbill.char2, "|") = "NM=GuestTable" + STRING(tischnr).
                    END.
                    ELSE /*DYANMIC QR*/
                    DO:
                        ENTRY(2, b-orderbill.char2, "|") = "NM=" + guest-name.
                    END.
                    FIND CURRENT b-orderbill NO-LOCK.
                    RELEASE b-orderbill.
                END.
            END.                                  
            
            IF dynamic-qr THEN
            DO:
                FIND CURRENT selforder-session EXCLUSIVE-LOCK.
                selforder-session.logi1 = YES.
                FIND CURRENT selforder-session NO-LOCK.

                /*EXPIRATION SESSION OLD PICKUP TABLE*/
                FIND FIRST pickup-table WHERE pickup-table.key EQ 225
                    AND pickup-table.char1 EQ "taken-table"
                    AND pickup-table.logi1 EQ YES
                    AND pickup-table.logi2 EQ YES
                    AND pickup-table.number1 EQ curr-dept
                    AND pickup-table.number2 EQ curr-tischnr                   
                    AND ENTRY(1, pickup-table.char3, "|") EQ sessionID-one NO-LOCK NO-ERROR.
                IF AVAILABLE pickup-table THEN
                DO:             
                    FIND CURRENT pickup-table EXCLUSIVE-LOCK.
                    ENTRY(1, pickup-table.char3, "|") = sessionID-one + "T" 
                        + REPLACE(STRING(TODAY),"/","") 
                        + REPLACE(STRING(TIME,"HH:MM"),":","").
                    FIND CURRENT pickup-table NO-LOCK.
                    RELEASE pickup-table.
                END.
            END.
                
            FIND FIRST paygateway-session WHERE paygateway-session.key EQ 223
                AND paygateway-session.number1 EQ curr-dept
                AND paygateway-session.char3 EQ sessionID-one 
                AND paygateway-session.betriebsnr EQ old-billno NO-LOCK NO-ERROR.
            IF AVAILABLE paygateway-session THEN
            DO:                
                FIND CURRENT paygateway-session EXCLUSIVE-LOCK.
                paygateway-session.betriebsnr = 0.
                FIND CURRENT paygateway-session NO-LOCK.
                RELEASE paygateway-session.
            END.
            
            RELEASE selforder-session.
        END.  
    END.
END PROCEDURE.

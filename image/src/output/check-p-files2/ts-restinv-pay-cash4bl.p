
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER transdate AS DATE.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER disc-art1 AS INT.
DEF INPUT PARAMETER disc-art2 AS INT.
DEF INPUT PARAMETER disc-art3 AS INT.

DEF OUTPUT PARAMETER bill-date AS DATE.

DEF VARIABLE get-rechnr  AS INTEGER NO-UNDO.
DEF VARIABLE get-amount  AS DECIMAL NO-UNDO.
DEF VARIABLE active-deposit AS LOGICAL.
DEF VARIABLE recid-hbill AS INTEGER. /*FD*/

/*FD Nov 30, 2022 => Feature Deposit Resto*/
FIND FIRST htparam WHERE htparam.paramnr EQ 588 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN active-deposit = htparam.flogical.

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.

/*FD March 14, 2022 => UPDATE ALL QUEASY RELATED ON SELF ORDER*/
DO TRANSACTION:
    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
    ASSIGN vhp.h-bill.flag = 1.
    /************************online tax vanguard (pengiriman realtime)*****************/
    CREATE INTERFACE.
    ASSIGN
    INTERFACE.KEY         = 38
    INTERFACE.action      = YES
    INTERFACE.nebenstelle = ""
    INTERFACE.parameters = "close-bill"
    INTERFACE.intfield    = h-bill.rechnr
    INTERFACE.decfield    = h-bill.departement
    INTERFACE.int-time    = TIME
    INTERFACE.intdate     = TODAY
    INTERFACE.resnr       = h-bill.resnr
    INTERFACE.reslinnr    = h-bill.reslinnr
    .
    FIND CURRENT INTERFACE NO-LOCK.
    RELEASE INTERFACE.

    FIND CURRENT vhp.h-bill NO-LOCK. 
 
    get-rechnr = vhp.h-bill.rechnr.
    FOR EACH h-bill-line WHERE h-bill-line.departement EQ h-bill.departement 
        AND h-bill-line.rechnr EQ h-bill.rechnr
        AND h-bill-line.betrag LT 0 NO-LOCK:
        FIND FIRST h-artikel WHERE h-artikel.departement EQ h-bill-line.departement
            AND h-artikel.artnr EQ h-bill-line.artnr
            AND h-artikel.artart NE 0 NO-LOCK NO-ERROR.
        IF AVAILABLE h-artikel THEN get-amount = get-amount + h-bill-line.betrag.
    END.
    FIND FIRST queasy WHERE queasy.KEY EQ 230 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        RUN update-selforder.
    END.

    /*FD Nov 30, 2022 => Feature Deposit Resto*/
    recid-hbill = RECID(vhp.h-bill).
    IF active-deposit THEN
    DO:
        RUN remove-rsv-table.
    END.
END.

RUN fill-cover.

PROCEDURE fill-cover: 
  DEF VAR f-pax  AS INTEGER INITIAL 0   NO-UNDO. 
  DEF VAR b-pax  AS INTEGER INITIAL 0   NO-UNDO.
  DEF VAR str     AS CHAR               NO-UNDO.
  DEF BUFFER h-art1 FOR vhp.h-artikel. 
  DEF BUFFER tbuff  FOR vhp.tisch.

  DO TRANSACTION: 
    
    FIND FIRST tbuff WHERE tbuff.tischnr = vhp.h-bill.tischnr 
        AND tbuff.departement = vhp.h-bill.departement NO-LOCK NO-ERROR.
    IF AVAILABLE tbuff AND tbuff.roomcharge AND tbuff.kellner-nr NE 0 THEN
    DO:
        FIND CURRENT tbuff EXCLUSIVE-LOCK.
        ASSIGN tbuff.kellner-nr = 0.
        FIND CURRENT tbuff NO-LOCK.
    END.
    RUN release-TBplan.

    IF vhp.h-bill.resnr GT 0 THEN 
    RUN rest-addgastinfo.p(vhp.h-bill.departement, vhp.h-bill.rechnr,
      vhp.h-bill.resnr, vhp.h-bill.reslinnr, 0, transdate).

    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
    ASSIGN vhp.h-bill.kellner-nr = vhp.kellner.kellner-nr NO-ERROR.
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 739 NO-LOCK.
    IF vhp.htparam.flogical THEN 
    DO:
      RUN TS-voucherUI.p(OUTPUT str).
      IF str NE "" THEN ASSIGN vhp.h-bill.service[5] = DECIMAL(str).
    END.
    FIND CURRENT vhp.h-bill NO-LOCK.

    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
    /* vhp.bill DATE */ 
    bill-date = vhp.htparam.fdate. 
    IF transdate NE ? THEN bill-date = transdate. 
    ELSE 
    DO: 
      FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */ 
      IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
    END. 
 
    FIND FIRST vhp.h-umsatz WHERE vhp.h-umsatz.artnr = 0 
      AND vhp.h-umsatz.departement = curr-dept AND 
      vhp.h-umsatz.betriebsnr = curr-dept 
      AND vhp.h-umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE vhp.h-umsatz THEN 
    DO: 
      create vhp.h-umsatz. 
      vhp.h-umsatz.artnr = 0. 
      vhp.h-umsatz.departement = curr-dept. 
      vhp.h-umsatz.betriebsnr = curr-dept. 
      vhp.h-umsatz.datum = bill-date. 
    END. 
    vhp.h-umsatz.anzahl = vhp.h-umsatz.anzahl + vhp.h-bill.belegung. 
 
    IF vhp.h-bill.belegung NE 0 THEN 
    FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
        AND vhp.h-bill-line.departement = vhp.h-bill.departement 
        AND vhp.h-bill-line.artnr NE disc-art1 
        AND vhp.h-bill-line.artnr NE disc-art2 
        AND vhp.h-bill-line.artnr NE disc-art3 NO-LOCK, 
        FIRST h-art1 WHERE h-art1.artnr = vhp.h-bill-line.artnr 
        AND h-art1.departement = vhp.h-bill-line.departement 
        AND h-art1.artart = 0 NO-LOCK, 
        FIRST vhp.artikel WHERE vhp.artikel.artnr = h-art1.artnrfront 
        AND vhp.artikel.departement = h-art1.departement NO-LOCK: 
        IF vhp.artikel.umsatzart = 3 OR vhp.artikel.umsatzart = 5 THEN 
            f-pax = f-pax + h-bill-line.anzahl. 
        ELSE IF vhp.artikel.umsatzart = 6 THEN 
            b-pax = b-pax + h-bill-line.anzahl. 
    END. 
 
    IF vhp.h-bill.belegung > 0 THEN 
    DO: 
        IF f-pax > vhp.h-bill.belegung THEN f-pax = vhp.h-bill.belegung. 
        IF b-pax > vhp.h-bill.belegung THEN b-pax = vhp.h-bill.belegung. 
    END. 
    ELSE IF vhp.h-bill.belegung < 0 THEN 
    DO: 
        IF f-pax < vhp.h-bill.belegung THEN f-pax = vhp.h-bill.belegung. 
        IF b-pax < vhp.h-bill.belegung THEN b-pax = vhp.h-bill.belegung. 
    END. 
    vhp.h-umsatz.betrag = vhp.h-umsatz.betrag + f-pax. 
    vhp.h-umsatz.nettobetrag = vhp.h-umsatz.nettobetrag + b-pax. 
 
    FIND CURRENT vhp.h-umsatz NO-LOCK. 
    RELEASE vhp.h-umsatz. 
  END. 
END. 

PROCEDURE release-TBplan:
    FIND FIRST vhp.queasy WHERE vhp.queasy.KEY = 31 
      AND vhp.queasy.number1 = vhp.h-bill.departement
      AND vhp.queasy.number2 = vhp.h-bill.tischnr NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.queasy THEN
    DO TRANSACTION:
      FIND CURRENT vhp.queasy EXCLUSIVE-LOCK.
      ASSIGN vhp.queasy.number3 = 0
             vhp.queasy.date1 = ?.
      FIND CURRENT vhp.queasy NO-LOCK.
      RELEASE vhp.queasy.
    END.
END.

PROCEDURE update-selforder:
    DEFINE BUFFER paramqsy FOR queasy.
    DEFINE BUFFER searchbill FOR queasy.
    DEFINE BUFFER genparamso FOR queasy.
    DEFINE BUFFER orderbill FOR queasy.
    DEFINE BUFFER orderbilline FOR queasy.
    DEFINE BUFFER orderbill-close FOR queasy.
    DEFINE BUFFER pickup-table FOR queasy.
    DEFINE BUFFER qpayment-gateway FOR queasy.

    DEFINE VARIABLE found-bill AS INT.
    DEFINE VARIABLE session-parameter AS CHAR.
    
    DEFINE VARIABLE mess-str AS CHAR.
    DEFINE VARIABLE i-str AS INT.
    DEFINE VARIABLE mess-token AS CHAR.
    DEFINE VARIABLE mess-keyword AS CHAR.
    DEFINE VARIABLE mess-value AS CHAR.

    DEFINE VARIABLE dynamic-qr AS LOGICAL.
    DEFINE VARIABLE room-serviceflag AS LOGICAL.

    /*SEARCH EVERY VALUE IN GENPARAM FOR SELFORDER*/
    FOR EACH genparamso WHERE genparamso.KEY EQ 222 
        AND genparamso.number1 EQ 1 
        AND genparamso.betriebsnr EQ curr-dept NO-LOCK:
        IF genparamso.number2 EQ 14 THEN dynamic-qr = genparamso.logi1.
        IF genparamso.number2 EQ 21 THEN room-serviceflag = genparamso.logi1.
    END.
    
    /*SEARCH SESSION PARAMETER BASED ON BILL NUMBER*/
    FOR EACH searchbill WHERE searchbill.KEY EQ 225 
        AND searchbill.number1 EQ curr-dept 
        AND searchbill.char1 EQ "orderbill" NO-LOCK:

        mess-str = searchbill.char2.
        DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
            mess-token = ENTRY(i-str,mess-str,"|").
            mess-keyword = ENTRY(1,mess-token,"=").
            mess-value = ENTRY(2,mess-token,"=").
            IF mess-keyword EQ "BL" THEN
            DO: 
                found-bill = INT(mess-value).
                LEAVE.
            END.
        END.
        IF found-bill EQ get-rechnr THEN
        DO: 
            session-parameter = searchbill.char3.
            LEAVE.
        END.
    END.
    
    /*UPDATE SESSION FROM ACTIVE TO EXPIRED*/
    DO TRANSACTION:
        FIND FIRST paramqsy WHERE paramqsy.KEY EQ 230 AND paramqsy.char1 EQ session-parameter EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE paramqsy THEN
        DO:            
            paramqsy.betriebsnr = get-rechnr.

            IF dynamic-qr THEN
            DO:
                /*SEARCH TAKEN TABLE QUEASY AND UPDATE THE FIELDS*/
                FIND FIRST pickup-table WHERE pickup-table.KEY = 225
                    AND pickup-table.char1 EQ "taken-table"
                    AND pickup-table.number1 EQ curr-dept
                    AND pickup-table.logi1 EQ YES
                    AND pickup-table.logi2 EQ YES
                    AND pickup-table.number2 EQ paramqsy.number2
                    AND ENTRY(1, pickup-table.char3, "|") EQ session-parameter EXCLUSIVE-LOCK NO-ERROR.
                IF AVAILABLE pickup-table THEN
                DO:
                    ASSIGN
                        ENTRY(1, pickup-table.char3, "|") = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").

                    FIND CURRENT pickup-table NO-LOCK.
                END.
            END.
            
            FIND FIRST orderbill WHERE orderbill.KEY EQ 225 AND orderbill.char1 EQ "orderbill" 
                AND orderbill.char3 EQ session-parameter
                AND orderbill.logi1 EQ YES
                AND orderbill.logi3 EQ YES EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE orderbill THEN 
            DO:                
                orderbill.deci1 = get-amount.
                orderbill.logi2 = NO.
                orderbill.char3 = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").
                orderbill.logi1 = NO.

                FOR EACH orderbill-close WHERE orderbill-close.KEY EQ 225
                    AND orderbill-close.char1 EQ "orderbill"
                    AND orderbill-close.char3 EQ session-parameter 
                    AND orderbill-close.logi1 EQ YES
                    AND orderbill-close.logi3 EQ YES EXCLUSIVE-LOCK:
                    orderbill-close.char3 = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").
                    ASSIGN orderbill-close.logi1 = NO.
                END.
            END.            

            IF dynamic-qr THEN paramqsy.logi1 = YES.
            ELSE
            DO:
                IF room-serviceflag THEN
                DO:
                    ASSIGN
                    paramqsy.char1      = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","")
                    paramqsy.char3      = paramqsy.char3 + "|BL=" + STRING(get-rechnr)
                    paramqsy.logi1      = YES.
                   
                END.
                ELSE
                DO:
                    CREATE queasy.
                    BUFFER-COPY paramqsy TO queasy.
                    ASSIGN 
                    queasy.char1      = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","")
                    queasy.betriebsnr = 1
                    queasy.logi1      = YES.
                END.

                /*SEARCH ORDERBILL-LINE QUEASY AND UPDATE THE FIELDS CHAR2*/
                FOR EACH orderbilline WHERE orderbilline.KEY EQ 225 
                    AND orderbilline.char1 EQ "orderbill-line"
                    AND ENTRY(4,orderbilline.char2,"|") EQ session-parameter EXCLUSIVE-LOCK:                    
                   
                    IF orderbilline.logi2 AND orderbilline.logi3 THEN /*Posting to Bill*/
                    DO:
                        orderbilline.char2 = ENTRY(1,orderbilline.char2,"|") + "|" + 
                            ENTRY(2,orderbilline.char2,"|") + "|" + 
                            ENTRY(3,orderbilline.char2,"|") + "|" + 
                            session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").
                    END.
                    ELSE /*Cancel from seflorder dashboard*/
                    DO:
                        IF NUM-ENTRIES(orderbilline.char3,"|") GT 8
                            AND ENTRY(9, orderbilline.char3, "|") NE "" THEN
                        DO:
                            orderbilline.char2 = ENTRY(1,orderbilline.char2,"|") + "|" + 
                                ENTRY(2,orderbilline.char2,"|") + "|" + 
                                ENTRY(3,orderbilline.char2,"|") + "|" + 
                                session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").
                        END.
                    END.
                END.
            END.

            /*FD June 21, 2022 => For issue payment gateway can't posting, release betriebsnr 223 to 0*/
            FIND FIRST qpayment-gateway WHERE qpayment-gateway.KEY EQ 223
                AND qpayment-gateway.char3 EQ session-parameter
                AND qpayment-gateway.betriebsnr EQ get-rechnr EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE qpayment-gateway THEN
            DO:
                qpayment-gateway.betriebsnr = 0.
                FIND CURRENT qpayment-gateway NO-LOCK.
            END.

            FIND CURRENT paramqsy NO-LOCK.
        END.        
    END.
END PROCEDURE.

PROCEDURE remove-rsv-table:
    DEFINE VARIABLE recid-q33 AS INTEGER.

    DEFINE BUFFER buffq33 FOR queasy.

    FIND FIRST queasy WHERE queasy.KEY EQ 251 AND queasy.number1 EQ recid-hbill NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        recid-q33 = queasy.number2.

        FIND FIRST buffq33 WHERE RECID(buffq33) EQ recid-q33 NO-LOCK NO-ERROR.
        IF AVAILABLE buffq33 THEN
        DO:
            FIND CURRENT buffq33 EXCLUSIVE-LOCK.
            ASSIGN
                buffq33.betriebsnr = 1      /*FD Dec 13, 2022 => betriebsnr = 1 (Closed)*/
            .
            FIND CURRENT buffq33 NO-LOCK.
            RELEASE buffq33.
        END.
    END.
END PROCEDURE.

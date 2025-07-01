
DEFINE INPUT PARAMETER guestno LIKE guest.gastnr NO-UNDO.
DEFINE INPUT PARAMETER init-fee   AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" LABEL "INITIAL Fee".
DEFINE INPUT PARAMETER mber-fee   AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" LABEL "Membership Fee".
DEFINE INPUT PARAMETER user-init  AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str AS CHARACTER NO-UNDO.

/*
DEFINE VARIABLE guestno AS INTEGER INITIAL 22450.
DEFINE VARIABLE init-fee AS DECIMAL NO-UNDO.
DEFINE VARIABLE mber-fee AS DECIMAL INITIAL 1057320.
DEFINE VARIABLE msg-str AS CHARACTER.
DEFINE VARIABLE user-init AS CHARACTER INITIAL "99".
*/


DEFINE VARIABLE art-init    AS INTEGER      NO-UNDO.
DEFINE VARIABLE artnr1      AS INTEGER      NO-UNDO.
DEFINE VARIABLE art-disc    AS INTEGER      NO-UNDO.
DEFINE VARIABLE art-disc1   AS INTEGER      NO-UNDO.
DEFINE VARIABLE art-tax     AS INTEGER      NO-UNDO.
DEFINE VARIABLE art-ccard   AS INTEGER      NO-UNDO.
DEFINE VARIABLE pay-art     AS INTEGER      NO-UNDO.
DEFINE VARIABLE str-art     AS CHARACTER    NO-UNDO.
DEFINE VARIABLE billdate    AS DATE         NO-UNDO.
DEFINE VARIABLE dept        AS INTEGER      NO-UNDO.

DEFINE VARIABLE member-code AS CHARACTER    NO-UNDO.

DEFINE VARIABLE i AS INTEGER    NO-UNDO.
DEFINE VARIABLE s AS CHARACTER  NO-UNDO.

DEFINE VARIABLE from-date AS DATE NO-UNDO.
DEFINE VARIABLE to-date AS DATE NO-UNDO.
DEFINE VARIABLE billname AS CHARACTER NO-UNDO.

DEFINE BUFFER mbuff FOR cl-member.
DEFINE BUFFER gbuff FOR guest.
DEFINE BUFFER gbuff1 FOR guest.
DEFINE BUFFER artikel1 FOR artikel.
DEFINE BUFFER fbuff FOR mc-fee.
DEFINE BUFFER tbuff FOR cl-memtype.


FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
billdate = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr = 1045 NO-LOCK.
dept = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 1046 NO-LOCK.
str-art = htparam.fchar.

DO i = 1 TO NUM-ENTRIES(str-art, ";"):
    s = ENTRY(1, ENTRY(i, str-art, ";"), ",").
    CASE s:
        WHEN "IF" THEN 
            art-init = INTEGER(ENTRY(2, ENTRY(i, str-art, ";"), ",")).
        WHEN "MF" THEN
            artnr1   = INTEGER(ENTRY(2, ENTRY(i, str-art, ";"), ",")).  /*art for membership fee*/
        WHEN "IFD" THEN
            art-disc = INTEGER(ENTRY(2, ENTRY(i, str-art, ";"), ",")).
        WHEN "MFD" THEN
            art-disc1 = INTEGER(ENTRY(2, ENTRY(i, str-art, ";"), ",")).
        WHEN "TX" THEN
            art-tax = INTEGER(ENTRY(2, ENTRY(i, str-art, ";"), ",")).
        WHEN "CC" THEN
            art-ccard = INTEGER(ENTRY(2, ENTRY(i, str-art, ";"), ",")).
    END CASE.

    /*hardcode*/
    ASSIGN
        art-init    = 3
        artnr1      = 2
        art-tax     = 5
        pay-art     = 30.
    /*end hardcoded*/

    /*tambah param untuk automatic active the member*/
    DEFINE VARIABLE active-flag AS LOGICAL INITIAL YES.
END.

DEFINE VARIABLE validity    AS INTEGER      NO-UNDO.
DEFINE VARIABLE memname     AS CHARACTER    NO-UNDO.
DEFINE VARIABLE betrag      AS DECIMAL      NO-UNDO.
DEFINE VARIABLE paid-amt    AS DECIMAL      NO-UNDO.
DEFINE VARIABLE paid-flag   AS LOGICAL      NO-UNDO.
DEFINE VARIABLE typenr      AS INTEGER      NO-UNDO.
DEFINE VARIABLE membertype  AS CHARACTER    NO-UNDO.
DEFINE VARIABLE payment     AS DECIMAL      NO-UNDO.
DEFINE VARIABLE curr-time   AS INTEGER      NO-UNDO.
DEFINE VARIABLE billgastnr  AS INTEGER      NO-UNDO.
     
RUN init-display.
RUN validation.
RUN create-bill.

PROCEDURE init-display:
    FIND FIRST gbuff WHERE gbuff.gastnr = guestno USE-INDEX gastnr_index 
        NO-LOCK NO-ERROR.
    IF AVAILABLE gbuff THEN memname = gbuff.NAME + ", " + gbuff.vorname1 + " " + gbuff.anrede1.
    
    FIND FIRST mbuff WHERE mbuff.gastnr = guestno
        AND mbuff.memstatus LE 2 USE-INDEX gastnr_ix NO-LOCK.
    FIND FIRST mc-fee WHERE mc-fee.KEY = 2
        AND mc-fee.nr = mbuff.membertype
        AND mc-fee.gastnr = mbuff.gastnr
        AND mc-fee.activeflag = 0
        NO-LOCK.

    ASSIGN
        billgastnr  = mbuff.billgastnr
        from-date   = mc-fee.von-datum
        to-date     = mc-fee.bis-datum
        validity    = mbuff.num1
        member-code = mbuff.codenum
    .

    FIND FIRST gbuff1 WHERE gbuff1.gastnr = mbuff.billgastnr USE-INDEX gastnr_index
        NO-LOCK NO-ERROR.
    IF AVAILABLE gbuff1 THEN
    DO:
        IF gbuff1.karteityp = 0 THEN
            ASSIGN billname = gbuff1.NAME + ", " + gbuff1.vorname1 + " " 
                + gbuff.anrede1.
        ELSE ASSIGN billname = gbuff1.NAME + ", " + gbuff1.anredefirma.
    END.
    ELSE
    DO:
        IF gbuff.karteityp = 0 THEN
            ASSIGN billname = gbuff.NAME + ", " + gbuff.vorname1 + " " 
                + gbuff.anrede1.
        ELSE ASSIGN billname = gbuff.NAME + ", " + gbuff.anredefirma.
    END.

    FIND FIRST fbuff WHERE fbuff.gastnr = guestno AND fbuff.activeflag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE fbuff THEN 
    DO:
        ASSIGN 
            betrag      = fbuff.betrag
            paid-amt    = fbuff.bezahlt
            .
        IF fbuff.bezahlt = 0 THEN paid-flag = NO.
    END.

    FIND FIRST tbuff WHERE tbuff.nr = fbuff.nr NO-LOCK NO-ERROR.
    IF AVAILABLE tbuff THEN
    DO:
        ASSIGN
            membertype = tbuff.DESCRIPT
            typenr     = tbuff.nr.
        IF validity = 0 THEN
            validity   = tbuff.dauer.
    END.                         

    payment = init-fee + mber-fee.
END.

PROCEDURE validation:
    /*validation*/
    FIND FIRST artikel1 WHERE artikel1.artnr = artnr1 AND
        artikel1.departement = dept NO-LOCK NO-ERROR.
    IF NOT AVAILABLE artikel1 THEN msg-str = "F/O artNo for membership fee not yet been setup.".


    IF init-fee NE 0 THEN
    DO:
        FIND FIRST artikel1 WHERE artikel1.artnr = art-init AND
            artikel1.departement = dept NO-LOCK NO-ERROR.
        IF NOT AVAILABLE artikel1 THEN msg-str = msg-str + CHR(13) + "F/O artNo for INITIAL fee not yet been setup.".
    END.
END.

PROCEDURE create-bill:
    FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK.
    counters.counter = counters.counter + 1.
    FIND CURRENT counters NO-LOCK.
    CREATE bill.
    ASSIGN
        bill.gastnr     = guestno
        bill.rechnr     = counters.counter
        bill.datum      = billdate
        bill.billtyp    = dept
        bill.NAME       = billname
        bill.bilname    = memname
        bill.reslinnr   = 1
        bill.rgdruck    = 0
        bill.saldo      = 0
        .
    FIND CURRENT bill NO-LOCK.

    curr-time = TIME.

    IF init-fee NE 0 THEN
    DO:
        RUN create-bill-line(art-init, init-fee, "", curr-time, dept).
    END.

    IF mber-fee NE 0 THEN
    DO:
        RUN create-bill-line(artnr1, mber-fee, "", curr-time, dept).
    END.

    curr-time = curr-time + 1.

    RUN create-bill-line(pay-art, - payment, "", curr-time, 0).

    FIND FIRST artikel WHERE artikel.artnr = pay-art
        AND artikel.departement = 0 NO-LOCK.
    IF artikel.artart = 2 OR artikel.artart = 7 THEN
        RUN inv-ar(pay-art, " " , billgastnr, guestno, bill.rechnr,
                   - betrag, 0, billdate, billname, user-init).

    FIND CURRENT mc-fee EXCLUSIVE-LOCK.
    ASSIGN
        mc-fee.activeflag = 1
        mc-fee.bezahlt    = betrag
        mc-fee.bez-datum  = billdate
        mc-fee.usr-init   = user-init
        mc-fee.artnr      = pay-art.
    FIND CURRENT mc-fee NO-LOCK.

    RUN create-history.

    IF active-flag THEN RUN update-membership.
    ELSE RUN update-joindate.
END.


PROCEDURE create-bill-line:
    DEF INPUT PARAMETER artnr       AS INTEGER NO-UNDO.
    DEF INPUT PARAMETER amt         AS DECIMAL NO-UNDO.
    DEF INPUT PARAMETER voucher     AS CHAR NO-UNDO.
    DEF INPUT PARAMETER curr-time   AS INTEGER NO-UNDO.
    DEF INPUT PARAMETER deptnr      AS INTEGER NO-UNDO.
    DEF BUFFER artikel1 FOR artikel.


        DEF VAR do-it AS LOGICAL INITIAL YES.
        FIND FIRST artikel1 WHERE artikel1.artnr = artnr
            AND artikel1.departement = deptnr NO-LOCK NO-ERROR.

        CREATE bill-line.
        ASSIGN
            bill-line.rechnr = bill.rechnr
            bill-line.artnr = artnr
            bill-line.anzahl = 1
            bill-line.betrag = amt
            bill-line.bezeich = artikel1.bezeich
            bill-line.departement = deptnr
            bill-line.zeit = curr-time
            bill-line.userinit = user-init
            bill-line.bill-datum = billdate
            .
        IF voucher NE "" THEN bill-line.bezeich = bill-line.bezeich + 
            "/" + voucher.
        FIND CURRENT bill-line NO-LOCK.

        CREATE billjournal.
         ASSIGN
              billjournal.rechnr = bill.rechnr
              billjournal.artnr = artnr
              billjournal.betrag = amt
              billjournal.anzahl = 1
              billjournal.bezeich = bill-line.bezeich
              billjournal.departement = deptnr
              billjournal.zeit = curr-time
              billjournal.userinit = user-init
              billjournal.bill-datum = billdate
         .

        
          FIND FIRST umsatz WHERE umsatz.artnr = artnr AND umsatz.departement = deptnr
                AND umsatz.datum = billdate EXCLUSIVE-LOCK NO-ERROR.
          IF NOT AVAILABLE umsatz THEN
          DO:
                CREATE umsatz.
                ASSIGN 
                    umsatz.artnr = artnr
                    umsatz.departement = deptnr
                    umsatz.datum = billdate
                    .
          END.
          umsatz.betrag = umsatz.betrag + amt.
          FIND CURRENT umsatz NO-LOCK.
END.


PROCEDURE inv-ar:
    DEFINE INPUT PARAMETER curr-art       AS INTEGER.
    DEFINE INPUT PARAMETER zinr           AS CHAR FORMAT "x(4)".
    DEFINE INPUT PARAMETER gastnr         AS INTEGER.
    DEFINE INPUT PARAMETER gastnrmember   AS INTEGER.
    DEFINE INPUT PARAMETER rechnr         AS INTEGER.
    DEFINE INPUT PARAMETER saldo          AS DECIMAL.
    DEFINE INPUT PARAMETER saldo-foreign  AS DECIMAL.
    DEFINE INPUT PARAMETER bill-date      AS DATE.
    DEFINE INPUT PARAMETER billname       AS CHAR.
    DEFINE INPUT PARAMETER userinit       AS CHAR FORMAT "x(2)".


  DEFINE BUFFER debt        FOR debitor.
  DEFINE BUFFER bill1       FOR bill.

  DEFINE VARIABLE comment       AS CHAR INITIAL "".
  DEFINE VARIABLE verstat       AS INTEGER INITIAL 0.
  DEFINE VARIABLE fsaldo        AS DECIMAL INITIAL 0.
  DEFINE VARIABLE lsaldo        AS DECIMAL INITIAL 0.
  DEFINE VARIABLE foreign-rate  AS LOGICAL.  
  DEFINE VARIABLE currency-nr   AS INTEGER INITIAL 0 NO-UNDO.
  DEFINE VARIABLE double-currency AS LOGICAL.  

  FIND FIRST htparam WHERE paramnr = 143 NO-LOCK.
  foreign-rate = htparam.flogical.

  FIND FIRST htparam WHERE paramnr = 240 NO-LOCK.
  double-currency = htparam.flogical.

  FIND FIRST bediener WHERE bediener.userinit = userinit NO-LOCK.
  
  FIND FIRST htparam WHERE paramnr = 997 NO-LOCK.
  if NOT htparam.flogical THEN RETURN.

  FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK.
  billname = guest.name + ", " + guest.vorname1 + " " 
    + guest.anrede1 + guest.anredefirma.
      
  FIND FIRST debt WHERE debt.artnr = curr-art
    AND debt.rechnr = rechnr and debt.opart = 0 
    AND debt.rgdatum = bill-date and debt.counter = 0 
    AND debt.saldo = saldo NO-LOCK NO-ERROR.

  IF AVAILABLE debt THEN
  do:
    FIND CURRENT debt EXCLUSIVE-LOCK.
    DELETE debt.
    RETURN.
  END.

  IF gastnr NE gastnrmember THEN
  DO:
    FIND FIRST guest WHERE guest.gastnr = gastnrmember NO-LOCK.
    comment = guest.name + ", " + guest.vorname1 + " " 
      + guest.anrede1 + guest.anredefirma.
  END.
  
  comment = comment + " Membership Fee - " + member-code.

  CREATE debitor.
  ASSIGN
    debitor.artnr           = curr-art
    debitor.betrieb-gastmem = currency-nr
    debitor.zinr            = zinr
    debitor.gastnr          = gastnr
    debitor.gastnrmember    = gastnrmember
    debitor.rechnr          = rechnr
    debitor.saldo           = - saldo
    debitor.transzeit       = time
    debitor.rgdatum         = bill-date
    debitor.bediener-nr     = bediener.nr
    debitor.name            = billname
    debitor.vesrcod         = comment
    debitor.verstat         = verstat.

    IF double-currency OR foreign-rate THEN 
      debitor.vesrdep    = - saldo-foreign.

  RELEASE debitor.
END.

PROCEDURE create-history:
    DEF BUFFER Mber  FOR cl-member.
    DEF BUFFER sbuff FOR bediener.
    CREATE cl-histpay.
    ASSIGN
        cl-histpay.KEY      = 1
        cl-histpay.datum    = billdate
        cl-histpay.datum1   = from-date
        cl-histpay.datum2   = to-date
        cl-histpay.gastnr   = guestno
        cl-histpay.amount   = mber-fee
        cl-histpay.paid     = payment
        cl-histpay.balance  = 0
        cl-histpay.remarks  = user-init + " - " + "Payment History"
        cl-histpay.deci1    = init-fee
        cl-histpay.char2    = remarks
        .

    IF AVAILABLE bill THEN cl-histpay.rechnr   = bill.rechnr.

    FIND FIRST mber WHERE mber.gastnr = guestno
      AND mber.memstatus LE 2 NO-LOCK.
    FIND FIRST sbuff WHERE sbuff.userinit = mber.salesID NO-LOCK NO-ERROR.
    ASSIGN 
        cl-histpay.codenum      = mber.codenum
        cl-histpay.billgastnr   = mber.gastnr
        cl-histpay.memtype      = mber.membertype
    .
    IF AVAILABLE sbuff THEN cl-histpay.number1 = sbuff.nr.
    FIND CURRENT cl-histpay NO-LOCK.
    
END.


PROCEDURE update-membership:
    DEF BUFFER mbuff   FOR cl-member.
    DEF BUFFER mbuff1  FOR cl-member.
    DEF BUFFER mbuff2  FOR cl-member.
    DEF BUFFER mcbuff  FOR mc-fee.
    DEF BUFFER guest1  FOR guest.
    DEF BUFFER guest2  FOR guest.
    DEF VAR    do-it   AS LOGICAL NO-UNDO.

    DO:
        FIND FIRST mbuff WHERE mbuff.gastnr = guestno
          AND mbuff.memstatus LE 2 USE-INDEX gastnr_ix
            EXCLUSIVE-LOCK.
        DO:
            FIND FIRST guest1 WHERE guest1.gastnr = mbuff.gastnr NO-LOCK.
            DO:                         
                CREATE cl-log.
                ASSIGN 
                    cl-log.codenum = mbuff.codenum
                    cl-log.datum = TODAY
                    cl-log.zeit = TIME
                    cl-log.user-init = user-init
                    cl-log.CHAR1 = string(mbuff.membertype) + " ; " + string(mbuff.membertype) 
                    + " ; " + STRING(mbuff.memstatus) + " ; " + STRING(1) 
                    + " ; " + mbuff.pict-file + " ; " + mbuff.pict-file
                    + " ; " + mbuff.load-by + " ; " + mbuff.load-by
                    + " ; " + STRING(mbuff.billgastnr, ">,>>9") + " ; " + STRING(mbuff.billgastnr, ">,>>9") 
                    + " ; " + STRING(guest1.kreditlimit, ">>,>>>,>>>,>>9") + " ; " + STRING(guest1.kreditlimit, ">>,>>>,>>>,>>9")
                    + " ; " + STRING(mbuff.paysched) + " ; " + STRING(mbuff.paysched)
                    + " ; " + STRING(mbuff.billcycle) + " ; " + STRING(mbuff.billcycle)
                    + " ; " + STRING(mbuff.expired) + " ; " + STRING(mc-fee.bis-datum)
                    + " ; " + mbuff.user-init1 + " ; " + user-init
                    .
                FIND CURRENT cl-log NO-LOCK.
            END.

            IF mbuff.lastbill EQ ? THEN
            ASSIGN mbuff.last-renewed = ?. 
            ELSE mbuff.last-renewed = mbuff.expired-date. 
            
            IF mbuff.memstatus = 0 THEN
            ASSIGN
              mbuff.memstatus    = 1
              mbuff.nextbill     = mc-fee.bis-datum
              mbuff.lastbill     = billdate
              mbuff.expired-date = mc-fee.bis-datum
            . 
            ELSE
            ASSIGN
              mbuff.memstatus    = 1
              mbuff.nextbill     = mc-fee.bis-datum
              mbuff.lastbill     = billdate
              mbuff.join-date    = mc-fee.von-datum
              mbuff.expired-date = mc-fee.bis-datum
            .

            FIND CURRENT mbuff NO-LOCK.
            CREATE cl-histstat.
            ASSIGN cl-histstat.datum = TODAY
                cl-histstat.codenum =  mbuff.codenum
                cl-histstat.memstatus = mbuff.memstatus
                cl-histstat.remark = "Membership fee had been paid"
                cl-histstat.user-init = user-init
                cl-histstat.zeit = TIME
            .
            FIND CURRENT cl-histstat NO-LOCK.
        END.                       

        FIND CURRENT mbuff NO-LOCK.
        FIND FIRST cl-memtype WHERE cl-memtype.nr = mbuff.membertype NO-LOCK.

        IF mbuff.gastnr = mbuff.main-gastnr THEN
        FOR EACH mbuff2 NO-LOCK WHERE 
            mbuff2.main-gastnr = mbuff.main-gastnr AND 
            mbuff2.gastnr NE mbuff.gastnr AND 
            mbuff2.memstatus LE 1:  /* changed by SY 14Jul2007 */

            FIND FIRST mcbuff NO-LOCK WHERE 
                mcbuff.activeflag = 0 AND 
                mcbuff.KEY = 2 AND
                mcbuff.gastnr = mbuff2.gastnr AND
                mcbuff.betrag = 0 NO-ERROR.

            IF AVAILABLE mcbuff THEN
            DO:
              FIND CURRENT mcbuff EXCLUSIVE-LOCK.
              ASSIGN mcbuff.activeflag = 1.
              FIND CURRENT mcbuff NO-LOCK.

              FIND FIRST mbuff1 WHERE RECID(mbuff1) = RECID(mbuff2) EXCLUSIVE-LOCK.
              FIND FIRST guest2 WHERE guest2.gastnr = mbuff2.gastnr NO-LOCK NO-ERROR.
              IF AVAILABLE guest2 THEN
              DO: 
                CREATE cl-log.
                ASSIGN 
                    cl-log.codenum = mbuff1.codenum
                    cl-log.datum = TODAY
                    cl-log.zeit = TIME
                    cl-log.user-init = user-init
                    cl-log.CHAR1 = string(mbuff1.membertype) + " ; " + string(mbuff1.membertype) 
                    + " ; " + STRING(mbuff1.memstatus) + " ; " + STRING(1) 
                    + " ; " + mbuff1.pict-file + " ; " + mbuff1.pict-file
                    + " ; " + mbuff1.load-by + " ; " + mbuff1.load-by
                    + " ; " + STRING(mbuff1.billgastnr, ">,>>9") + " ; " + STRING(mbuff1.billgastnr, ">,>>9") 
                    + " ; " + STRING(guest2.kreditlimit, ">>,>>>,>>>,>>9") + " ; " + STRING(guest2.kreditlimit, ">>,>>>,>>>,>>9")
                    + " ; " + STRING(mbuff1.paysched) + " ; " + STRING(mbuff1.paysched)
                    + " ; " + STRING(mbuff1.billcycle) + " ; " + STRING(mbuff1.billcycle)
                    + " ; " + STRING(mbuff1.expired) + " ; " + STRING(mc-fee.bis-datum)
                    + " ; " + mbuff1.user-init1 + " ; " + user-init
                    .
                FIND CURRENT cl-log NO-LOCK.
              END.

              IF mbuff1.lastbill EQ ? THEN 
              DO:
                mbuff1.last-renewed = ?.
                mbuff1.join-date = from-date.
              END.
              ELSE mbuff1.last-renewed = mbuff.expired-date.
              
              IF mbuff1.memstatus = 0 THEN
              ASSIGN
                mbuff1.memstatus = 1
                mbuff1.nextbill = mc-fee.bis-datum
                mbuff1.lastbill = billdate
              .
              ELSE
              ASSIGN
                mbuff1.nextbill     = mc-fee.bis-datum
                mbuff1.lastbill     = billdate
                mbuff1.join-date    = mc-fee.von-datum
                mbuff1.expired-date = mc-fee.bis-datum
              .
              
              CREATE cl-histstat.
              ASSIGN cl-histstat.datum = TODAY
                cl-histstat.codenum =  mbuff1.codenum
                cl-histstat.memstatus = mbuff1.memstatus
                cl-histstat.remark = "Membership fee had been paid"
                cl-histstat.user-init = user-init
                cl-histstat.zeit = TIME
              .
              FIND CURRENT cl-histstat NO-LOCK.
              FIND CURRENT mbuff1 NO-LOCK.
            END. /* if available mcbuff */
        END. 
    END.
END.


PROCEDURE update-joindate:
    DEF BUFFER mbuff FOR cl-member.
    DEF BUFFER mbuff1 FOR cl-member.
    DEF BUFFER mbuff2 FOR cl-member.
    DEF BUFFER guest1 FOR guest.
    DEF BUFFER guest2 FOR guest.

    DO:
        FIND FIRST mbuff WHERE mbuff.gastnr = guestno
            AND mbuff.memstatus LE 2 USE-INDEX gastnr_ix
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE mbuff THEN 
        DO:
            FIND FIRST guest1 WHERE guest1.gastnr = mbuff.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest1 THEN
            DO:   
                IF mc-fee.bis-datum NE mbuff.expired THEN
                DO:
                    CREATE cl-log.
                    ASSIGN 
                        cl-log.codenum = mbuff.codenum
                        cl-log.datum = TODAY
                        cl-log.zeit = TIME
                        cl-log.user-init = user-init
                        cl-log.CHAR1 = string(mbuff.membertype) + " ; " + string(mbuff.membertype) 
                        + " ; " + STRING(mbuff.memstatus) + " ; " + STRING(mbuff.memstatus) 
                        + " ; " + mbuff.pict-file + " ; " + mbuff.pict-file
                        + " ; " + mbuff.load-by + " ; " + mbuff.load-by
                        + " ; " + STRING(mbuff.billgastnr, ">,>>9") + " ; " + STRING(mbuff.billgastnr, ">,>>9") 
                        + " ; " + STRING(guest1.kreditlimit, ">>,>>>,>>>,>>9") + " ; " + STRING(guest1.kreditlimit, ">>,>>>,>>>,>>9")
                        + " ; " + STRING(mbuff.paysched) + " ; " + STRING(mbuff.paysched)
                        + " ; " + STRING(mbuff.billcycle) + " ; " + STRING(mbuff.billcycle)
                        + " ; " + STRING(mbuff.expired) + " ; " + STRING(mc-fee.bis-datum)
                        + " ; " + mbuff.user-init1 + " ; " + user-init
                        .
                    FIND CURRENT cl-log NO-LOCK.
                END.
            END.
            /*
            IF mbuff.lastbill EQ ? THEN
            DO:
                mbuff.last-renewed = ?.
                mbuff.join-date = mc-fee.von-datum.
            END.                                   
            ELSE mbuff.last-renewed = mc-fee.von-datum.
            */
            IF mbuff.last-renewed = ? THEN
            DO:
                mbuff.join-date = mc-fee.von-datum.
            END.
            ELSE mbuff.last-renewed = billdate.
            mbuff.nextbill = mc-fee.bis-datum.
            mbuff.lastbill = billdate.
            mbuff.expired-date = mc-fee.bis-datum.
            FIND CURRENT mbuff NO-LOCK.
        END.          

        IF mbuff.gastnr = mbuff.main-gastnr THEN
        FOR EACH mbuff2 NO-LOCK WHERE mbuff2.main-gastnr = guestno AND 
          mbuff2.gastnr NE mbuff.gastnr AND
          mbuff2.memstatus LE 1:
          FIND FIRST mc-fee WHERE mc-fee.activeflag = 0 AND mc-fee.KEY = 2 
            AND mc-fee.gastnr = mbuff2.gastnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE mc-fee THEN
          DO:
            FIND FIRST mbuff1 WHERE RECID(mbuff1) = RECID(mbuff2) EXCLUSIVE-LOCK.
            FIND FIRST guest2 WHERE guest2.gastnr = mbuff2.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest2 THEN
            DO:         
              CREATE cl-log.
              ASSIGN 
                  cl-log.codenum = mbuff1.codenum
                  cl-log.datum = TODAY
                  cl-log.zeit = TIME
                  cl-log.user-init = user-init
                  cl-log.CHAR1 = string(mbuff1.membertype) + " ; " + string(mbuff1.membertype) 
                        + " ; " + STRING(mbuff1.memstatus) + " ; " + STRING(mbuff1.memstatus) 
                        + " ; " + mbuff1.pict-file + " ; " + mbuff1.pict-file
                        + " ; " + mbuff1.load-by + " ; " + mbuff1.load-by
                        + " ; " + STRING(mbuff1.billgastnr, ">,>>9") + " ; " + STRING(mbuff1.billgastnr, ">,>>9") 
                        + " ; " + STRING(guest2.kreditlimit, ">>,>>>,>>>,>>9") + " ; " + STRING(guest2.kreditlimit, ">>,>>>,>>>,>>9")
                        + " ; " + STRING(mbuff1.paysched) + " ; " + STRING(mbuff1.paysched)
                        + " ; " + STRING(mbuff1.billcycle) + " ; " + STRING(mbuff1.billcycle)
                        + " ; " + STRING(mbuff1.expired) + " ; " + STRING(mc-fee.bis-datum)
                        + " ; " + mbuff1.user-init1 + " ; " + user-init
              .
              FIND CURRENT cl-log NO-LOCK.
            END.
            IF mbuff1.lastbill EQ ? THEN 
            DO:
                mbuff1.last-renewed = ?.
                mbuff1.join-date = mbuff.join-date.
            END.
            ELSE mbuff1.last-renewed = mbuff.last-renewed.
            ASSIGN
              mbuff1.nextbill = mbuff.nextbill
              mbuff1.lastbill = billdate
              mbuff1.expired-date = mbuff.expired-date
            .
            FIND CURRENT mbuff1 NO-LOCK NO-ERROR.
          END.
        END.
    END. /*Transaction */
END.


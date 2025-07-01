/*Eko 25062015 Add some keyword on output-list*/
DEFINE TEMP-TABLE s-list 
  FIELD artnr       AS INTEGER 
  FIELD bezeich     AS CHAR FORMAT "x(36)" 
  FIELD betrag      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 


DEF TEMP-TABLE t-list 
    FIELD artnr     AS INTEGER 
    FIELD bezeich   AS CHAR FORMAT "x(36)" 
    FIELD betrag    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 


DEFINE TEMP-TABLE output-list 
  FIELD artnr        AS INTEGER 
  FIELD pay-count    AS INTEGER INITIAL 0 
  FIELD flag         AS INTEGER INITIAL 0 
  FIELD pay-amt      AS DECIMAL 
  FIELD dbetrag      AS DECIMAL 
  FIELD sbetrag      AS CHAR 
  FIELD inv-no       AS CHAR FORMAT "x(9)"
  FIELD STR          AS CHAR
  FIELD bill-art     AS INTEGER
  FIELD debt-counter AS INTEGER
  /*MG For Selected Print WEB DF2D4B*/
  FIELD art-bezeich  AS CHAR
  FIELD tbetrag      AS DECIMAL
  FIELD gastname     AS CHAR 
  FIELD soa-inv      AS CHARACTER
  FIELD famt         AS CHARACTER 
  FIELD bill-num     AS INT
  FIELD pay-famt     AS DECIMAL. /* Naufal Afthar - D7F30E*/

DEFINE TEMP-TABLE t-ar-paylist
  FIELD bill-date     AS CHARACTER
  FIELD bill-num      AS CHARACTER
  FIELD inv-num       AS CHARACTER
  FIELD bill-rcv      AS CHARACTER
  FIELD debt-amt      AS CHARACTER
  FIELD pay-amt       AS CHARACTER
  FIELD pay-famt      AS CHARACTER
  FIELD curr          AS CHARACTER
  FIELD pay-art       AS CHARACTER
  FIELD pay-date      AS CHARACTER
  FIELD uid           AS CHARACTER
  FIELD pay-comment   AS CHARACTER
  FIELD tot-pay       AS CHARACTER
  FIELD artno         AS CHARACTER
  FIELD debt-counter  AS CHARACTER
  /*MG For Selected Print WEB DF2D4B*/
  FIELD art-bezeich   AS CHARACTER
  FIELD tbetrag       AS CHARACTER
  FIELD gastname      AS CHARACTER
  FIELD soa-inv       AS CHARACTER
  FIELD famt          AS CHARACTER
  FIELD bill-num2     AS CHARACTER.

DEFINE INPUT  PARAMETER  comment     AS CHAR      NO-UNDO.
DEFINE INPUT  PARAMETER  cledger     AS LOGICAL   NO-UNDO.
DEFINE INPUT  PARAMETER  ccard       AS LOGICAL   NO-UNDO.
DEFINE INPUT  PARAMETER  last-sort   AS INTEGER   NO-UNDO.
DEFINE INPUT  PARAMETER  from-date   AS DATE      NO-UNDO.
DEFINE INPUT  PARAMETER  to-date     AS DATE      NO-UNDO.
DEFINE INPUT  PARAMETER  from-art    AS INTEGER   NO-UNDO.
DEFINE INPUT  PARAMETER  to-art      AS INTEGER   NO-UNDO.
DEFINE INPUT  PARAMETER  mi-payment  AS LOGICAL   NO-UNDO.
DEFINE INPUT  PARAMETER  mi-transfer AS LOGICAL   NO-UNDO.
DEFINE INPUT  PARAMETER  show-inv    AS LOGICAL   NO-UNDO.
DEFINE INPUT  PARAMETER  bill-name   AS CHARACTER NO-UNDO.  /*MG 5E0DCF*/
DEFINE INPUT  PARAMETER  bill-nr     AS INTEGER NO-UNDO.  /*bernatd 2025 D5C323*/
DEFINE OUTPUT PARAMETER  r-no        AS INTEGER   NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-ar-paylist.

/*
DEFINE VARIABLE bill-name AS CHARACTER   NO-UNDO INIT "".
DEFINE VARIABLE bill-nr AS INTEGER     NO-UNDO INIT ?.
DEFINE VARIABLE ccard AS LOGICAL     NO-UNDO INIT YES.
DEFINE VARIABLE cledger AS LOGICAL     NO-UNDO INIT YES.
DEFINE VARIABLE comment AS CHARACTER   NO-UNDO INIT " ".
DEFINE VARIABLE from-art AS INTEGER     NO-UNDO INIT 1.
DEFINE VARIABLE from-date AS DATE        NO-UNDO INIT 05/01/25.
DEFINE VARIABLE mi-payment AS LOGICAL     NO-UNDO INIT NO.
DEFINE VARIABLE mi-transfer AS LOGICAL     NO-UNDO INIT NO.
DEFINE VARIABLE last-sort AS INTEGER     NO-UNDO INIT 1.
DEFINE VARIABLE show-inv AS LOGICAL     NO-UNDO INIT NO.
DEFINE VARIABLE to-art AS INTEGER     NO-UNDO INIT 31.
DEFINE VARIABLE to-date AS DATE        NO-UNDO INIT 05/22/25.
*/

DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

DEFINE BUFFER bguest FOR guest.
DEFINE BUFFER bdebitor FOR debitor.

RUN create-list.

FOR EACH t-ar-paylist:
    DELETE t-ar-paylist.
END.

/*FIND FIRST output-list WHERE SUBSTR(output-list.STR, 9, 11) EQ "    147,068" NO-LOCK NO-ERROR.
IF AVAILABLE output-list THEN
DO:
  MESSAGE output-list.STR VIEW-AS ALERT-BOX.
END.FT serverless*/

FOR EACH output-list :
    CREATE t-ar-paylist.
    ASSIGN
        t-ar-paylist.bill-date      = SUBSTR(output-list.STR, 1, 8)   
        t-ar-paylist.bill-num       = SUBSTR(output-list.STR, 9, 11)  
        t-ar-paylist.inv-num        = output-list.inv-no              
        t-ar-paylist.bill-rcv       = SUBSTR(output-list.STR, 20, 32) 
        t-ar-paylist.debt-amt       = SUBSTR(output-list.STR, 52, 17) 
        /* t-ar-paylist.pay-amt        = SUBSTR(output-list.STR, 69, 17) 
        t-ar-paylist.pay-famt       = SUBSTR(output-list.str, 165, 18) */
        t-ar-paylist.curr           = SUBSTR(output-list.str, 183, 4) 
        t-ar-paylist.pay-art        = SUBSTR(output-list.STR, 86, 34) 
        t-ar-paylist.pay-date       = SUBSTR(output-list.STR, 120, 8) 
        t-ar-paylist.uid            = SUBSTR(output-list.STR, 128, 3) 
        t-ar-paylist.pay-comment    = SUBSTR(output-list.STR, 131, 34)
        t-ar-paylist.tot-pay        = output-list.sbetrag 
        t-ar-paylist.artno          = STRING(output-list.bill-art) /*FD Dec 08, 2021*/
        t-ar-paylist.debt-counter   = STRING(output-list.debt-counter) /*MG 2ADD13*/
        t-ar-paylist.art-bezeich    = output-list.art-bezeich
        t-ar-paylist.tbetrag        = STRING(output-list.tbetrag, "->>>,>>>,>>>,>>9.99") 
        t-ar-paylist.gastname       = output-list.gastname
        t-ar-paylist.soa-inv        = output-list.soa-inv 
        t-ar-paylist.famt           = output-list.famt 
        t-ar-paylist.bill-num2      = STRING(output-list.bill-num)
    .

    IF t-ar-paylist.pay-comment MATCHES("*?*") THEN
        ASSIGN t-ar-paylist.pay-comment = "".

    /* Naufal Afthar - D7F30E*/
    IF NOT long-digit THEN
        ASSIGN
          t-ar-paylist.pay-amt        = STRING(output-list.pay-amt, "->,>>>,>>>,>>>,>>9.99")
          t-ar-paylist.pay-famt       = STRING(output-list.pay-famt, "->,>>>,>>>,>>>,>>>,>>9.99").
    ELSE
        ASSIGN
          t-ar-paylist.pay-amt        = STRING(output-list.pay-amt, "->>>,>>>,>>>,>>>,>>9")
          t-ar-paylist.pay-famt       = STRING(output-list.pay-famt, "->>>,>>>,>>>,>>>,>>>,>>9").
END.

 
/*************** PROCEDURES ***************/
PROCEDURE create-list: 

  FOR EACH s-list: 
    DELETE s-list. 
  END. 
  FOR EACH t-list: 
      DELETE t-list. 
  END. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  IF comment = "" THEN 
  DO: 
    IF cledger AND ccard THEN 
    DO: 
      IF last-sort = 1 THEN RUN create-list1. 
      ELSE IF last-sort = 2 THEN RUN create-list1A.
      ELSE IF last-sort = 3 THEN RUN create-list1B.
      ELSE IF last-sort = 4 THEN RUN create-list1C.
      ELSE IF last-sort = 5 THEN RUN create-list1D.
      ELSE IF last-sort = 6 THEN RUN create-list1E. /* Oscar (16/12/2024) - E0A590 - add new sorting by Payment Date */
      
      /*bernatd 2025 D5C323*/
      ELSE IF last-sort = 7 THEN
      DO:
        IF bill-nr NE ? THEN
        DO: 
            RUN create-list1F. 
        END.
        ELSE 
        DO: 
            RUN create-list1FS.
        END.
      END. 
      /*end bernatd D5C323*/
    END. 
    ELSE IF cledger AND NOT ccard THEN 
    DO: 
      IF last-sort = 1 THEN RUN create-list2. 
      ELSE IF last-sort = 2 THEN RUN create-list2A.
      ELSE IF last-sort = 3 THEN RUN create-list2B.
      ELSE IF last-sort = 4 THEN RUN create-list2C.
      ELSE IF last-sort = 5 THEN RUN create-list2D.       
      ELSE IF last-sort = 6 THEN RUN create-list2E. /* Oscar (16/12/2024) - E0A590 - add new sorting by Payment Date */
    
      /*bernatd 2025 D5C323*/
      ELSE IF last-sort = 7 THEN
      DO:
        IF bill-nr NE ? THEN
        DO: 
            RUN create-list2F. 
        END.
        ELSE 
        DO: 
            RUN create-list2FS.
        END.
      END. 
      /*end bernatd D5C323*/
    END. 
    ELSE IF ccard AND NOT cledger THEN 
    DO: 
      IF last-sort = 1 THEN RUN create-list3. 
      ELSE IF last-sort = 2 THEN RUN create-list3A. 
      ELSE IF last-sort = 3 THEN RUN create-list3B. 
      ELSE IF last-sort = 4 THEN RUN create-list3C. 
      ELSE IF last-sort = 5 THEN RUN create-list3D. 
      ELSE IF last-sort = 6 THEN RUN create-list3E. /* Oscar (16/12/2024) - E0A590 - add new sorting by Payment Date */

      /*bernatd 2025 D5C323*/
      ELSE IF last-sort = 7 THEN
      DO:
        IF bill-nr NE ? THEN
        DO: 
            RUN create-list3F. 
        END.
        ELSE 
        DO: 
            RUN create-list3FS.
        END.
      END. 
      /*end bernatd D5C323*/

    END. 
  END. 
  ELSE IF comment NE "" THEN 
  DO: 
    IF cledger AND ccard THEN RUN create-list11. 
    ELSE IF cledger AND NOT ccard THEN RUN create-list21. 
    ELSE IF ccard AND NOT cledger THEN RUN create-list31. 
  END. 
END. 

 
PROCEDURE create-tot-payment: 
  DEF VAR curr-artno AS INTEGER INITIAL 0. 
  DEF VAR tbetrag AS DECIMAL INITIAL 0. 
  DEF VAR curr-count AS INTEGER. 
  DEF BUFFER tbuff FOR output-list. 
  DEF BUFFER bQ FOR output-list. 

  FIND FIRST bQ WHERE bQ.pay-count NE 0 NO-ERROR. 
  IF NOT AVAILABLE bQ THEN RETURN. 
 
  FOR EACH bQ WHERE bQ.flag EQ 1 AND bQ.pay-count NE 0 BY bQ.pay-count: 
    IF curr-count = 0 THEN curr-count = bQ.pay-count. 
    IF (curr-count NE bQ.pay-count) THEN 
    DO: 
      FOR EACH tbuff WHERE tbuff.pay-count EQ curr-count: 
        IF NOT long-digit THEN tbuff.sbetrag = STRING(tbetrag, "->,>>>,>>>,>>9.99"). 
        ELSE tbuff.sbetrag = STRING(tbetrag, " ->>>,>>>,>>>,>>9"). 
        tbuff.dbetrag = tbetrag. 
      END. 
      tbetrag = 0. 
    END. 
    curr-count = bQ.pay-count. 
    tbetrag = tbetrag + bQ.pay-amt. 
  END.

  FOR EACH tbuff WHERE tbuff.pay-count EQ curr-count: 
    IF NOT long-digit THEN tbuff.sbetrag = STRING(tbetrag, "->,>>>,>>>,>>9.99"). 
    ELSE tbuff.sbetrag = STRING(tbetrag, " ->>>,>>>,>>>,>>9"). 
    tbuff.dbetrag = tbetrag. 
  END. 
END. 
 
PROCEDURE create-list1: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel.
  DEFINE BUFFER t-guest       FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.NAME BY debitor.gastnr
    BY debitor.rgdatum BY debitor.zahlkonto BY debitor.betriebsnr 
    BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr.
          
          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END.

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo.
          output-list.pay-famt = tot-foreign.

          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9").

          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 

        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
            t-list.artnr = artikel.artnr 
            t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            /*gerald gastnr yg sama terhitung di beda artikel 250820*/
            IF tot-saldo NE 0 THEN
            DO:
              CREATE output-list. 
              DO i = 1 TO 58: 
                output-list.str = output-list.str + " ". 
              END. 

              /* Naufal Afthar - D7F30E*/
              output-list.pay-amt = tot-saldo. 
              output-list.pay-famt = tot-foreign.
              
              IF NOT long-digit THEN 
                output-list.str = output-list.str + "T O T A L " 
                                + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                                + FILL(" ", 78)
                                + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
              ELSE 
                output-list.str = output-list.str + "T O T A L " 
                                + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                                + FILL(" ", 78)
                                + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
              
              CREATE output-list. 
              tot-saldo = 0. 
              tot-foreign = 0.
            END.
            /*end*/

            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit.
            output-list.pay-famt = t-famt.

            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0.
            tot-saldo = 0. /*gerald 250820*/
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  
        
        CREATE output-list. 
        ASSIGN 
          output-list.flag = 1 
          output-list.artnr = debitor.zahlkonto 
          output-list.pay-amt = debitor.saldo 
          output-list.pay-count = debitor.betriebsnr 
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99") /* Oscar - 188F7D - add AR Foreign column */
          output-list.pay-famt = debt.vesrdep. /* Naufal Afthar - D7F30E*/
        
        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.
  
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)")     /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") /*Debt*/
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") /*Payment*/
                          + STRING(art.bezeich, "x(34)") /*34*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 
      
        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        output-list.str = output-list.str + STRING(debitor.vesrdep, "->>,>>>,>>>,>>9.99").
        
        FIND FIRST waehrung WHERE waehrung.waehrungsnr EQ debitor.betrieb-gastmem NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
        DO:
            output-list.str = output-list.str + STRING(waehrung.wabkurz, "x(4)").
        END.
        ELSE output-list.str = output-list.str + "    ".

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        s-list.betrag = s-list.betrag + debitor.saldo.
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit.
  output-list.pay-famt = t-famt.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
 
  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END.

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit.
  output-list.pay-famt = tot-famt.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
 
  RUN create-tot-payment. 
END. 


PROCEDURE create-list1A:
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel.
  DEFINE BUFFER t-guest       FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.zahlkonto 
    BY debitor.name BY debitor.rgdatum BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.zahlkonto. 
        IF curr-gastnr NE debitor.zahlkonto THEN 
        DO: 
          curr-gastnr = debitor.zahlkonto.

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99"). 
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9").

          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
            t-list.artnr = artikel.artnr 
            t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit.
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9"). 

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). /*24*/
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list.
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo.
        output-list.pay-famt = debitor.vesrdep.

        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/ 
                          + STRING(debitor.rgdatum). 

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)").
        output-list.str = output-list.str + STRING(" ", "x(22)").

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo.
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
      output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit.
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "->>,>>>,>>>,>>9.99"). 
END. 

PROCEDURE create-list1B: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel.
  DEFINE BUFFER t-guest       FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debt.rgdatum  BY debitor.name BY debitor.zahlkonto 
    BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
            t-list.artnr = artikel.artnr 
            t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit.
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0.
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  
        
        CREATE output-list. 
        ASSIGN 
          output-list.flag = 1 
          output-list.artnr = debitor.zahlkonto 
          output-list.pay-amt = debitor.saldo 
          output-list.pay-count = debitor.betriebsnr
          output-list.bill-art = artikel.artnr 
          output-list.debt-counter = debitor.Counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99") /* Oscar - 188F7D - add AR Foreign column */
          output-list.pay-famt = debt.vesrdep. /* Naufal Afthar - D7F30E*/

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.
  
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)")     /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") /*Debt*/
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") /*Payment*/
                          + STRING(art.bezeich, "x(34)") /*34*/
                          + STRING(debitor.rgdatum). 
      
        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        output-list.str = output-list.str + STRING(debitor.vesrdep, "->>,>>>,>>>,>>9.99").

        FIND FIRST waehrung WHERE waehrung.waehrungsnr EQ debitor.betrieb-gastmem NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            output-list.str = output-list.str + STRING(waehrung.wabkurz, "x(4)").
        ELSE output-list.str = output-list.str + "    ".

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        s-list.betrag = s-list.betrag + debitor.saldo.
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo.
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit.
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit.
  output-list.pay-famt = tot-famt.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 

  RUN create-tot-payment. 
END. 

PROCEDURE create-list1C: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel.
  DEFINE BUFFER t-guest       FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.rechnr 
    BY debitor.NAME BY debitor.rgdatum BY debitor.zahlkonto: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
              t-list.artnr = artikel.artnr 
              t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            create output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END.

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit.
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0.
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END.

          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  
        
        CREATE output-list. 
        ASSIGN 
          output-list.flag = 1 
          output-list.artnr = debitor.zahlkonto 
          output-list.pay-amt = debitor.saldo 
          output-list.pay-count = debitor.betriebsnr
          output-list.bill-art = artikel.artnr 
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99") /* Oscar - 188F7D - add AR Foreign column */
          output-list.pay-famt = debt.vesrdep. /* Naufal Afthar - D7F30E*/

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.
  
        IF NOT long-digit THEN
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)")     /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") /*Debt*/
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") /*Payment*/
                          + STRING(art.bezeich, "x(34)") /*34*/
                          + STRING(debitor.rgdatum). 
      
        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        output-list.str = output-list.str + STRING(debitor.vesrdep, "->>,>>>,>>>,>>9.99").

        FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            output-list.str = output-list.str + STRING(waehrung.wabkurz, "x(4)").
        ELSE output-list.str = output-list.str + "    ".

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        s-list.betrag = s-list.betrag + debitor.saldo.
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo.
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 

  RUN create-tot-payment. 
END. 


PROCEDURE create-list1D:
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel.
  DEFINE BUFFER t-guest       FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date 
    AND rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.vesrcod 
    BY debitor.NAME BY debitor.rgdatum BY debitor.zahlkonto BY debitor.rechnr :
 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.

          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
              t-list.artnr = artikel.artnr 
              t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit.
            output-list.pay-famt = t-famt.

            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0.
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  
        
        CREATE output-list. 
        ASSIGN 
          output-list.flag = 1 
          output-list.artnr = debitor.zahlkonto 
          output-list.pay-amt = debitor.saldo 
          output-list.pay-count = debitor.betriebsnr
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99") /* Oscar - 188F7D - add AR Foreign column */
          output-list.pay-famt = debt.vesrdep. /* Naufal Afthar - D7F30E*/

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.
  
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)")     /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") /*Debt*/
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") /*Payment*/
                          + STRING(art.bezeich, "x(34)") /*34*/
                          + STRING(debitor.rgdatum). 
      
        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        output-list.str = output-list.str + STRING(debitor.vesrdep, "->>,>>>,>>>,>>9.99").

        FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            output-list.str = output-list.str + STRING(waehrung.wabkurz, "x(4)").
        ELSE output-list.str = output-list.str + "    ".

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        s-list.betrag = s-list.betrag + debitor.saldo.
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit.
  output-list.pay-famt = t-famt.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 

  RUN create-tot-payment.  
END. 

/* Oscar (16/12/2024) - E0A590 - add new sorting by Payment Date */
PROCEDURE create-list1E:
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-date   AS DATE INITIAL ?. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel.
  DEFINE BUFFER t-guest       FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date 
    AND rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.rgdatum BY debitor.rgdatum BY debitor.vesrcod 
    BY debitor.NAME BY debitor.zahlkonto BY debitor.rechnr :
 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-date = ? THEN curr-date = debitor.rgdatum. 
        IF curr-date NE debitor.rgdatum THEN
        DO: 
          curr-date = debitor.rgdatum.  

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
              t-list.artnr = artikel.artnr 
              t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0.
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  
        
        CREATE output-list. 
        ASSIGN 
          output-list.flag = 1 
          output-list.artnr = debitor.zahlkonto 
          output-list.pay-amt = debitor.saldo 
          output-list.pay-count = debitor.betriebsnr
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99") /* Oscar - 188F7D - add AR Foreign column */
          output-list.pay-famt = debt.vesrdep. /* Naufal Afthar - D7F30E*/

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.
  
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)")     /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") /*Debt*/
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") /*Payment*/
                          + STRING(art.bezeich, "x(34)") /*34*/
                          + STRING(debitor.rgdatum). 
      
        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        output-list.str = output-list.str + STRING(debitor.vesrdep, "->>,>>>,>>>,>>9.99").

        FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            output-list.str = output-list.str + STRING(waehrung.wabkurz, "x(4)").
        ELSE output-list.str = output-list.str + "    ".

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        s-list.betrag = s-list.betrag + debitor.saldo.
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit.
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 

  RUN create-tot-payment.  
END.

PROCEDURE create-list1F: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel.
  DEFINE BUFFER t-guest       FOR guest.

  FOR EACH debitor WHERE /*rgdatum GE from-date AND 
    rgdatum LE to-date AND*/ debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0
    AND debitor.rechnr EQ bill-nr NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.NAME BY debitor.gastnr
    BY debitor.rgdatum BY debitor.zahlkonto BY debitor.betriebsnr 
    BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr.
          
          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END.

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo.
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
            
          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 

        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
            t-list.artnr = artikel.artnr 
            t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            /*gerald gastnr yg sama terhitung di beda artikel 250820*/
            IF tot-saldo NE 0 THEN
            DO:
              CREATE output-list. 
              DO i = 1 TO 58: 
                output-list.str = output-list.str + " ". 
              END. 

              /* Naufal Afthar - D7F30E*/
              output-list.pay-amt = tot-saldo.
              output-list.pay-famt = tot-foreign.
              
              IF NOT long-digit THEN 
                output-list.str = output-list.str + "T O T A L " 
                                + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                                + FILL(" ", 78)
                                + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
              ELSE 
                output-list.str = output-list.str + "T O T A L " 
                                + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                                + FILL(" ", 78)
                                + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
              
              CREATE output-list. 
              tot-saldo = 0. 
              tot-foreign = 0.
            END.
            /*end*/

            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0.
            tot-saldo = 0. /*gerald 250820*/
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  
        
        CREATE output-list. 
        ASSIGN 
          output-list.flag = 1 
          output-list.artnr = debitor.zahlkonto 
          output-list.pay-amt = debitor.saldo 
          output-list.pay-count = debitor.betriebsnr 
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99") /* Oscar - 188F7D - add AR Foreign column */
          output-list.pay-famt = debt.vesrdep. /* Naufal Afthar - D7F30E*/

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.
  
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)")     /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") /*Debt*/
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") /*Payment*/
                          + STRING(art.bezeich, "x(34)") /*34*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 
      
        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        output-list.str = output-list.str + STRING(debitor.vesrdep, "->>,>>>,>>>,>>9.99").
        
        FIND FIRST waehrung WHERE waehrung.waehrungsnr EQ debitor.betrieb-gastmem NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
        DO:
            output-list.str = output-list.str + STRING(waehrung.wabkurz, "x(4)").
        END.
        ELSE output-list.str = output-list.str + "    ".

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        s-list.betrag = s-list.betrag + debitor.saldo.
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo.
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
 
  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
 
  RUN create-tot-payment. 
END. 

PROCEDURE create-list1FS: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel.
  DEFINE BUFFER t-guest       FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.NAME BY debitor.gastnr
    BY debitor.rgdatum BY debitor.zahlkonto BY debitor.betriebsnr 
    BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr.
          
          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END.

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.

          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
            
          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 

        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
            t-list.artnr = artikel.artnr 
            t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            /*gerald gastnr yg sama terhitung di beda artikel 250820*/
            IF tot-saldo NE 0 THEN
            DO:
              CREATE output-list. 
              DO i = 1 TO 58: 
                output-list.str = output-list.str + " ". 
              END. 

              /* Naufal Afthar - D7F30E*/
              output-list.pay-amt = tot-saldo. 
              output-list.pay-famt = tot-foreign.
              
              IF NOT long-digit THEN 
                output-list.str = output-list.str + "T O T A L " 
                                + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                                + FILL(" ", 78)
                                + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
              ELSE 
                output-list.str = output-list.str + "T O T A L " 
                                + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                                + FILL(" ", 78)
                                + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
              
              CREATE output-list. 
              tot-saldo = 0. 
              tot-foreign = 0.
            END.
            /*end*/

            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.

            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0.
            tot-saldo = 0. /*gerald 250820*/
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  
        
        CREATE output-list. 
        ASSIGN 
          output-list.flag = 1 
          output-list.artnr = debitor.zahlkonto 
          output-list.pay-amt = debitor.saldo 
          output-list.pay-count = debitor.betriebsnr 
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99") /* Oscar - 188F7D - add AR Foreign column */
          output-list.pay-famt = debt.vesrdep. /* Naufal Afthar - D7F30E*/

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.
  
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)")     /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") /*Debt*/
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") /*Payment*/
                          + STRING(art.bezeich, "x(34)") /*34*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 
      
        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        output-list.str = output-list.str + STRING(debitor.vesrdep, "->>,>>>,>>>,>>9.99").
        
        FIND FIRST waehrung WHERE waehrung.waehrungsnr EQ debitor.betrieb-gastmem NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
        DO:
            output-list.str = output-list.str + STRING(waehrung.wabkurz, "x(4)").
        END.
        ELSE output-list.str = output-list.str + "    ".

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        s-list.betrag = s-list.betrag + debitor.saldo.
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
 
  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
 
  RUN create-tot-payment. 
END. 

PROCEDURE create-list2: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt FOR debitor. 
  DEFINE BUFFER art FOR artikel. 
  DEFINE BUFFER t-guest FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 2 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
      AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr 
    BY debitor.rgdatum BY debitor.zahlkonto BY debitor.betriebsnr 
    BY debitor.rechnr: 
 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99") .
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

          CREATE output-list. 
          tot-saldo = 0.
          tot-foreign = 0. 
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
                t-list.artnr = artikel.artnr 
                t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN
          DO:
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99").  
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9").

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 

        t-list.betrag = t-list.betrag - debitor.saldo. 

        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.
        
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 
        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)").
        output-list.str = output-list.str + STRING(" ", "x(22)").
        
        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo.
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 

  RUN create-tot-payment. 
END. 
 
PROCEDURE create-list2A: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel. 
  DEFINE BUFFER t-guest       FOR guest.
  
  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 2 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
      AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.zahlkonto 
    BY debitor.name BY debitor.rgdatum BY debitor.rechnr: 
 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.zahlkonto. 
        IF curr-gastnr NE debitor.zahlkonto THEN 
        DO: 
          curr-gastnr = debitor.zahlkonto. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.

          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99"). 
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9").

          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
              t-list.artnr = artikel.artnr 
              t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9"). 

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.

        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)").
        output-list.str = output-list.str + STRING(" ", "x(22)").

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list3: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel. 
  DEFINE BUFFER t-guest       FOR guest.
  
  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 7 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr 
    BY debitor.rgdatum BY debitor.zahlkonto BY debitor.betriebsnr 
    BY debitor.rechnr: 
 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.

          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99"). 
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
              t-list.artnr = artikel.artnr 
              t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            /*gerald gastnr yg sama terhitung di beda artikel 250820*/
            IF tot-saldo NE 0 THEN
            DO:
              CREATE output-list. 
              DO i = 1 TO 58: 
                output-list.str = output-list.str + " ". 
              END. 

              /* Naufal Afthar - D7F30E*/
              output-list.pay-amt = tot-saldo. 
              output-list.pay-famt = tot-foreign.

              IF NOT long-digit THEN 
                output-list.str = output-list.str + "T O T A L " 
                                + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                                + FILL(" ", 78)
                                + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
              ELSE 
                output-list.str = output-list.str + "T O T A L " 
                                + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                                + FILL(" ", 78)
                                + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

              CREATE output-list. 
              tot-saldo = 0. 
              tot-foreign = 0.
            END.
            /*end*/

            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.

            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0.
            tot-saldo = 0. /*gerald 250820*/
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo.
        output-list.pay-famt = debitor.vesrdep.

        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        output-list.str = output-list.str + STRING(" ", "x(22)").
        
        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
                     
  RUN create-tot-payment. 
END. 
 
PROCEDURE create-list3A: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel. 
  DEFINE BUFFER t-guest       FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 7 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.zahlkonto 
    BY debitor.name BY debitor.rgdatum BY debitor.rechnr: 

      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.zahlkonto. 
        IF curr-gastnr NE debitor.zahlkonto THEN 
        DO: 
          curr-gastnr = debitor.zahlkonto. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99"). 
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo,   " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

          CREATE output-list. 
          tot-saldo = 0. 
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
              t-list.artnr = artikel.artnr 
              t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN
          DO:
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9"). 
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list.
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.
        
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)")  /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        output-list.str = output-list.str + STRING(" ", "x(22)").

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
 
  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list11: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel.
  DEFINE BUFFER t-guest       FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.vesrcod = comment
    /*AND debitor.vesrcod MATCHES ("*" + comment + "*")*/
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr 
    BY debitor.rgdatum BY debitor.rechnr: 

      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.
    
      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 
          
          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo.
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
          output-list.str = output-list.str + "T O T A L " 
            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
            + FILL(" ", 78)
            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  
          ELSE output-list.str = output-list.str + "T O T A L " 
            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
            + FILL(" ", 78)
            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
              t-list.artnr = artikel.artnr 
              t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 
            
            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
            output-list.str = output-list.str + "Sub-Total " 
              + STRING(t-credit, "->,>>>,>>>,>>9.99")
              + FILL(" ", 78)
              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
            ELSE output-list.str = output-list.str + "Sub-Total " 
              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
              + FILL(" ", 78)
              + STRING(t-famt, "  ->>>,>>>,>>>,>>9").
            create output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
            + STRING(artikel.artnr, ">>>>9") + " - " 
            + STRING(artikel.bezeich, "x(34)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list.
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.
        
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") 
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        output-list.str = output-list.str + STRING(" ", "x(22)").

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
 
  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list21: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel.
  DEFINE BUFFER t-guest       FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 AND debitor.vesrcod = comment
    /*AND debitor.vesrcod MATCHES ("*" + comment + "*")*/ NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 2 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr 
    BY debitor.rgdatum BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr.

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.

          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99") . 
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
          
          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
              t-list.artnr = artikel.artnr 
              t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN
          DO:
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9"). 
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list.
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo.
        output-list.pay-famt = debitor.vesrdep.

        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)")  /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*34*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        output-list.str = output-list.str + STRING(" ", "x(22)").

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit.
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
 
  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit.
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list31: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel. 
  DEFINE BUFFER t-guest       FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 AND debitor.vesrcod = comment 
    /*AND debitor.vesrcod MATCHES ("*" + comment + "*")*/ NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 7 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr 
    BY debitor.rgdatum BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99"). 
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
          
          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
              t-list.artnr = artikel.artnr 
              t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN
          DO:
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9"). 
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 
          
        t-list.betrag = t-list.betrag - debitor.saldo. 

        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.
        
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
                
        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        output-list.str = output-list.str + STRING(" ", "x(22)").

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
 
  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
END. 


PROCEDURE create-list2B: 
  DEFINE VARIABLE artnr           AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i               AS INTEGER. 
  DEFINE VARIABLE curr-gastnr     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit        AS DECIMAL. 
  DEFINE VARIABLE tot-credit      AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo       AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign       AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver        AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it           AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt FOR debitor. 
  DEFINE BUFFER art FOR artikel. 
  DEFINE BUFFER t-guest FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 2 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debt.rgdatum BY debitor.name BY debitor.zahlkonto 
    BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr.

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99") .
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
          
          CREATE output-list. 
          tot-saldo = 0.
          tot-foreign = 0. 
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
                t-list.artnr = artikel.artnr 
                t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN
          DO:
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit.
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99").  
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9").
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 

        t-list.betrag = t-list.betrag - debitor.saldo. 

        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.

        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)").
        output-list.str = output-list.str + STRING(" ", "x(22)").
        
        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
 
  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
 
  RUN create-tot-payment. 
END. 

PROCEDURE create-list2C: 
  DEFINE VARIABLE artnr           AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i               AS INTEGER. 
  DEFINE VARIABLE curr-gastnr     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit        AS DECIMAL. 
  DEFINE VARIABLE tot-credit      AS DECIMAL. 
  DEFINE VARIABLE t-famt          AS DECIMAL. 
  DEFINE VARIABLE tot-famt        AS DECIMAL. 
  DEFINE VARIABLE tot-saldo       AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign       AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver        AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it           AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt FOR debitor. 
  DEFINE BUFFER art FOR artikel. 
  DEFINE BUFFER t-guest FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 2 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.rechnr 
    BY debitor.NAME BY debitor.rgdatum BY debitor.zahlkonto: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99") .
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
          
          CREATE output-list. 
          tot-saldo = 0.
          tot-foreign = 0. 
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
                t-list.artnr = artikel.artnr 
                t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN
          DO:
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99").  
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9").
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 

        t-list.betrag = t-list.betrag - debitor.saldo. 

        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.
        
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ".

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)").
        output-list.str = output-list.str + STRING(" ", "x(22)").
        
        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
 
  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
 
  RUN create-tot-payment. 
END. 

PROCEDURE create-list2D: 
  DEFINE VARIABLE artnr           AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i               AS INTEGER. 
  DEFINE VARIABLE curr-gastnr     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit        AS DECIMAL. 
  DEFINE VARIABLE tot-credit      AS DECIMAL. 
  DEFINE VARIABLE t-famt          AS DECIMAL. 
  DEFINE VARIABLE tot-famt        AS DECIMAL. 
  DEFINE VARIABLE tot-saldo       AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign       AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver        AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it           AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt FOR debitor. 
  DEFINE BUFFER art FOR artikel. 
  DEFINE BUFFER t-guest FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 2 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.vesrcod
    BY debitor.NAME BY debitor.rgdatum BY debitor.zahlkonto BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99") .
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
          
          CREATE output-list. 
          tot-saldo = 0.
          tot-foreign = 0. 
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
                t-list.artnr = artikel.artnr 
                t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN
          DO:
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99").  
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9").
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). /*24*/
          artnr = artikel.artnr.
        END.

        t-list.betrag = t-list.betrag - debitor.saldo. 

        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.

        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)").
        output-list.str = output-list.str + STRING(" ", "x(22)").
        
        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
      output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "->>,>>>,>>>,>>9.99"). 
 
  RUN create-tot-payment. 
END.

/* Oscar (16/12/2024) - E0A590 - add new sorting by Payment Date */
PROCEDURE create-list2E: 
  DEFINE VARIABLE artnr           AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i               AS INTEGER. 
  DEFINE VARIABLE curr-date       AS DATE INITIAL ?. 
  DEFINE VARIABLE t-credit        AS DECIMAL. 
  DEFINE VARIABLE tot-credit      AS DECIMAL. 
  DEFINE VARIABLE t-famt          AS DECIMAL. 
  DEFINE VARIABLE tot-famt        AS DECIMAL. 
  DEFINE VARIABLE tot-saldo       AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign       AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver        AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it           AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt FOR debitor. 
  DEFINE BUFFER art FOR artikel. 
  DEFINE BUFFER t-guest FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 2 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.rgdatum BY debitor.vesrcod
    BY debitor.NAME BY debitor.zahlkonto BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-date = ? THEN curr-date = debitor.rgdatum. 
        IF curr-date NE debitor.rgdatum THEN
        DO: 
          curr-date = debitor.rgdatum.  

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99") .
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
          
          CREATE output-list. 
          tot-saldo = 0.
          tot-foreign = 0. 
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
                t-list.artnr = artikel.artnr 
                t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN
          DO:
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = tot-saldo. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99").  
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9").
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). /*24*/
          artnr = artikel.artnr.
        END.

        t-list.betrag = t-list.betrag - debitor.saldo. 

        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo.
        output-list.pay-famt = debitor.vesrdep.
        
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)").
        output-list.str = output-list.str + STRING(" ", "x(22)").
        
        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
      output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "->>,>>>,>>>,>>9.99"). 
 
  RUN create-tot-payment. 
END.

PROCEDURE create-list2F: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt FOR debitor. 
  DEFINE BUFFER art FOR artikel. 
  DEFINE BUFFER t-guest FOR guest.

  FOR EACH debitor WHERE /*rgdatum GE from-date AND 
    rgdatum LE to-date AND*/ debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0
    AND debitor.rechnr EQ bill-nr NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 2 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
      AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr 
    BY debitor.rgdatum BY debitor.zahlkonto BY debitor.betriebsnr 
    BY debitor.rechnr: 
 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99") .
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

          CREATE output-list. 
          tot-saldo = 0.
          tot-foreign = 0. 
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
                t-list.artnr = artikel.artnr 
                t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN
          DO:
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99").  
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9").

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 

        t-list.betrag = t-list.betrag - debitor.saldo. 

        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.
        
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 
        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)").
        output-list.str = output-list.str + STRING(" ", "x(22)").
        
        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 

  RUN create-tot-payment. 
END. 

PROCEDURE create-list2FS: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt FOR debitor. 
  DEFINE BUFFER art FOR artikel. 
  DEFINE BUFFER t-guest FOR guest.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 2 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
      AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr 
    BY debitor.rgdatum BY debitor.zahlkonto BY debitor.betriebsnr 
    BY debitor.rechnr: 
 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99") .
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

          CREATE output-list. 
          tot-saldo = 0.
          tot-foreign = 0. 
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
                t-list.artnr = artikel.artnr 
                t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN
          DO:
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit.
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99").  
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9").

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(24)"). 
          artnr = artikel.artnr. 
        END. 

        t-list.betrag = t-list.betrag - debitor.saldo. 

        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.

        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 
        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)").
        output-list.str = output-list.str + STRING(" ", "x(22)").
        
        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 

  RUN create-tot-payment. 
END. 

PROCEDURE create-list3B: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel. 
  DEFINE BUFFER t-guest       FOR guest.
 
  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 7 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debt.rgdatum BY debitor.name BY debitor.zahlkonto 
    BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99"). 
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
          
          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
            t-list.artnr = artikel.artnr 
            t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9"). 
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list.
        ASSIGN 
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.

        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025 1A8DDE*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        output-list.str = output-list.str + STRING(" ", "x(22)").
        
        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep. 

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
 
  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
 
  RUN create-tot-payment. 
END. 


PROCEDURE create-list3C: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel. 
  DEFINE BUFFER t-guest       FOR guest.
 
  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 7 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.rechnr 
    BY debitor.NAME BY debitor.rgdatum BY debitor.zahlkonto: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.
  
      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99"). 
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9").
          
          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 

        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
              t-list.artnr = artikel.artnr 
              t-list.bezeich = artikel.bezeich. 

          IF artnr NE 0 THEN 
          DO: 
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9"). 
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 

          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). 
          artnr = artikel.artnr. 
        END. 

        t-list.betrag = t-list.betrag - debitor.saldo. 

        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".
        
        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/
        
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.

        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.
        
        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        output-list.str = output-list.str + STRING(" ", "x(22)").

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .
 
  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 

  RUN create-tot-payment. 
END. 


PROCEDURE create-list3D: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel. 
  DEFINE BUFFER t-guest       FOR guest.
 
  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 7 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
      AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.vesrcod 
    BY debitor.NAME BY debitor.rgdatum BY debitor.zahlkonto BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.
  
      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END.

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.

          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99"). 
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9").
          
          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 

        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
            t-list.artnr = artikel.artnr 
            t-list.bezeich = artikel.bezeich. 

          IF artnr NE 0 THEN 
          DO: 
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = tot-saldo. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9"). 
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 

          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). 
          artnr = artikel.artnr. 
        END. 

        t-list.betrag = t-list.betrag - debitor.saldo. 

        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".
        
        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.   

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/
  
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.

        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.
        
        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "  ".

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        output-list.str = output-list.str + STRING(" ", "x(22)").

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.
        
        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 

  RUN create-tot-payment. 
END. 
 
/* Oscar (16/12/2024) - E0A590 - add new sorting by Payment Date */
PROCEDURE create-list3E: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-date   AS DATE INITIAL ?. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel. 
  DEFINE BUFFER t-guest       FOR guest.
 
  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 7 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.rgdatum BY debitor.vesrcod 
    BY debitor.NAME BY debitor.zahlkonto BY debitor.rechnr: 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) NE "*") THEN
      DO:
        IF NOT guest.NAME MATCHES ("*" + bill-name + "*") THEN do-it = NO.
      END.
  
      IF do-it AND (bill-name NE "") AND (SUBSTR(bill-name,1,1) EQ "*") THEN
      DO:
        IF NOT guest.NAME MATCHES bill-name THEN do-it = NO.  
      END.

      IF do-it THEN
      DO:
        IF curr-date = ? THEN curr-date = debitor.rgdatum. 
        IF curr-date NE debitor.rgdatum THEN
        DO: 
          curr-date = debitor.rgdatum. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END.

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.

          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99"). 
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9").
          
          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 

        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
            t-list.artnr = artikel.artnr 
            t-list.bezeich = artikel.bezeich. 

          IF artnr NE 0 THEN 
          DO: 
            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9"). 
            
            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0. 
          END. 

          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). 
          artnr = artikel.artnr. 
        END. 

        t-list.betrag = t-list.betrag - debitor.saldo. 

        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".
        
        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.   

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/
  
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.

        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        
        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.
        
        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "  ".

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        output-list.str = output-list.str + STRING(" ", "x(22)").

        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/

        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.
        
        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit.
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 

  RUN create-tot-payment. 
END.

PROCEDURE create-list3F: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel. 
  DEFINE BUFFER t-guest       FOR guest.
  
  FOR EACH debitor WHERE /*rgdatum GE from-date AND 
    rgdatum LE to-date AND*/ debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0
    AND debitor.rechnr EQ bill-nr NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 7 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr 
    BY debitor.rgdatum BY debitor.zahlkonto BY debitor.betriebsnr 
    BY debitor.rechnr: 
 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99"). 
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
              t-list.artnr = artikel.artnr 
              t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            /*gerald gastnr yg sama terhitung di beda artikel 250820*/
            IF tot-saldo NE 0 THEN
            DO:
              CREATE output-list. 
              DO i = 1 TO 58: 
                output-list.str = output-list.str + " ". 
              END. 

              /* Naufal Afthar - D7F30E*/
              output-list.pay-amt = tot-saldo.
              output-list.pay-famt = tot-foreign.
              
              IF NOT long-digit THEN 
                output-list.str = output-list.str + "T O T A L " 
                                + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                                + FILL(" ", 78)
                                + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
              ELSE 
                output-list.str = output-list.str + "T O T A L " 
                                + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                                + FILL(" ", 78)
                                + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

              CREATE output-list. 
              tot-saldo = 0. 
              tot-foreign = 0.
            END.
            /*end*/

            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0.
            tot-saldo = 0. /*gerald 250820*/
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.

        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        output-list.str = output-list.str + STRING(" ", "x(22)").
        
        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.

  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
                     
  RUN create-tot-payment. 
END. 

PROCEDURE create-list3FS: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL. 
  DEFINE VARIABLE tot-credit  AS DECIMAL. 
  DEFINE VARIABLE t-famt      AS DECIMAL. 
  DEFINE VARIABLE tot-famt    AS DECIMAL. 
  DEFINE VARIABLE tot-saldo   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-foreign   AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  DEFINE VARIABLE temp-name        AS CHAR.
  DEFINE VARIABLE temp-vorname1    AS CHAR.
  DEFINE VARIABLE temp-anredefirma AS CHAR.
  DEFINE VARIABLE temp-anrede1     AS CHAR.

  DEFINE BUFFER debt          FOR debitor. 
  DEFINE BUFFER art           FOR artikel. 
  DEFINE BUFFER t-guest       FOR guest.
  
  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto GT 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.counter GT 0 AND debitor.opart GT 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = debitor.counter 
    AND debt.zahlkonto = 0 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 AND artikel.artart = 7 NO-LOCK, 
    FIRST art WHERE art.artnr = debitor.zahlkonto 
    AND art.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr 
    BY debitor.rgdatum BY debitor.zahlkonto BY debitor.betriebsnr 
    BY debitor.rechnr: 
 
      do-it = YES.
      IF mi-payment THEN 
      DO:    
        IF artikel.artart = 2 AND art.artart NE 4 AND art.artart NE 7
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart NE 4 THEN do-it = NO.
      END.
      ELSE IF mi-transfer THEN
      DO:
        IF artikel.artart = 2 AND (art.artart EQ 4 OR art.artart EQ 7)
          THEN do-it = NO.
        ELSE IF artikel.artart = 7 AND art.artart EQ 4 THEN do-it = NO.
      END.

      IF do-it THEN
      DO:
        IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
        IF curr-gastnr NE debitor.gastnr THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 

          CREATE output-list. 
          DO i = 1 TO 58: 
            output-list.str = output-list.str + " ". 
          END. 

          /* Naufal Afthar - D7F30E*/
          output-list.pay-amt = tot-saldo. 
          output-list.pay-famt = tot-foreign.
          
          IF NOT long-digit THEN 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99"). 
          ELSE 
            output-list.str = output-list.str + "T O T A L " 
                            + STRING(tot-saldo, " ->>>,>>>,>>>,>>9")
                            + FILL(" ", 78)
                            + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

          CREATE output-list. 
          tot-saldo = 0. 
          tot-foreign = 0.
        END. 
  
        IF artnr NE artikel.artnr THEN 
        DO: 
          CREATE t-list. 
          ASSIGN 
              t-list.artnr = artikel.artnr 
              t-list.bezeich = artikel.bezeich. 
  
          IF artnr NE 0 THEN 
          DO: 
            /*gerald gastnr yg sama terhitung di beda artikel 250820*/
            IF tot-saldo NE 0 THEN
            DO:
              CREATE output-list. 
              DO i = 1 TO 58: 
                output-list.str = output-list.str + " ". 
              END. 

              /* Naufal Afthar - D7F30E*/
              output-list.pay-amt = tot-saldo. 
              output-list.pay-famt = tot-foreign.
              
              IF NOT long-digit THEN 
                output-list.str = output-list.str + "T O T A L " 
                                + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                                + FILL(" ", 78)
                                + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
              ELSE 
                output-list.str = output-list.str + "T O T A L " 
                                + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                                + FILL(" ", 78)
                                + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 

              CREATE output-list. 
              tot-saldo = 0. 
              tot-foreign = 0.
            END.
            /*end*/

            CREATE output-list. 
            DO i = 1 TO 58: 
              output-list.str = output-list.str + " ". 
            END. 

            /* Naufal Afthar - D7F30E*/
            output-list.pay-amt = t-credit. 
            output-list.pay-famt = t-famt.
            
            IF NOT long-digit THEN 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, "->,>>>,>>>,>>9.99")
                              + FILL(" ", 78)
                              + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
            ELSE 
              output-list.str = output-list.str + "Sub-Total " 
                              + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                              + FILL(" ", 78)
                              + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

            CREATE output-list. 
            t-credit = 0. 
            t-famt = 0.
            tot-saldo = 0. /*gerald 250820*/
          END. 
  
          CREATE output-list. 
          DO i = 1 TO 19: 
            output-list.str = output-list.str + " ". 
          END. 
          output-list.str = output-list.str 
                          + STRING(artikel.artnr, ">>>>9") + " - " 
                          + STRING(artikel.bezeich, "x(34)"). 
          artnr = artikel.artnr. 
        END. 
  
        t-list.betrag = t-list.betrag - debitor.saldo. 
  
        /*MG tiket 023181*/
        IF guest.NAME NE ? THEN ASSIGN temp-name = guest.NAME.
        ELSE temp-name = "".
        IF guest.vorname1 NE ? THEN ASSIGN temp-vorname1 = guest.vorname1.
        ELSE temp-vorname1 = "".
        IF guest.anredefirma NE ? THEN ASSIGN temp-anredefirma = guest.anredefirma.
        ELSE temp-anredefirma = "".
        IF guest.anrede1 NE ? THEN ASSIGN temp-anrede1 = guest.anrede1.
        ELSE temp-anrede1 = "".

        /*receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
          + guest.anrede1.*/
        receiver = temp-name + ", " + temp-vorname1 + " " + temp-anredefirma 
                 + temp-anrede1.  

        CREATE output-list. 
        ASSIGN
          output-list.bill-art = artikel.artnr
          output-list.debt-counter = debitor.counter
          output-list.famt = STRING(debt.vesrdep, "->>,>>>,>>>,>>9.99"). /* Oscar - 188F7D - add AR Foreign column */

        IF show-inv THEN
        DO:
          /*FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE bill THEN
          DO:
              r-no = debitor.rechnr.
          END.
          ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").*/

          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
            output-list.inv-no  = STRING(bill.rechnr2, ">>>>>>>>>").
          
            IF bill.billref NE 0 THEN output-list.soa-inv = "INV" + STRING(bill.billref, "9999999"). /*gerald D8F0E0*/
          END.
          ELSE 
          DO:
            FIND FIRST bdebitor WHERE bdebitor.rechnr = debitor.rechnr AND bdebitor.debref GT 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bdebitor THEN ASSIGN output-list.soa-inv  = "INV" + STRING(debitor.debref, "9999999").  /*gerald D8F0E0*/
          END.
        END.

        /* Naufal Afthar - D7F30E*/
        output-list.pay-amt = debitor.saldo. 
        output-list.pay-famt = debitor.vesrdep.
        
        IF NOT long-digit THEN 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(debitor.saldo, "->,>>>,>>>,>>9.99") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 
        ELSE 
          output-list.str = STRING(debt.rgdatum) 
                          + STRING(debitor.rechnr, ">>>,>>>,>>9") 
                          + STRING(receiver, "x(32)") 
                          + STRING(debt.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(debitor.saldo, " ->>>,>>>,>>>,>>9") 
                          + STRING(art.bezeich, "x(34)") /*24*/
                          + STRING(debitor.rgdatum). 

        /*bernatd 2025*/
        output-list.bill-num = debitor.rechnr.
        /*MG For Selected Print WEB DF2D4B*/
        output-list.art-bezeich   = artikel.bezeich.
        output-list.tbetrag       = output-list.tbetrag - debitor.saldo.

        FIND FIRST bguest WHERE bguest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN 
          output-list.gastname = bguest.name + ", " 
                               + bguest.vorname1 + bguest.anredefirma + " " + bguest.anrede1. 

        FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
          output-list.str = output-list.str + STRING(bediener.userinit, "x(3)"). 
        ELSE output-list.str = output-list.str + "   ". 

        output-list.str = output-list.str + STRING(debitor.vesrcod, "x(34)"). 
        output-list.str = output-list.str + STRING(" ", "x(22)").
        
        /*Eko 25062015*/
        DEFINE VARIABLE tStr AS CHARACTER NO-UNDO.
        FIND FIRST t-guest WHERE t-guest.gastnr = debt.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE t-guest THEN tStr = t-guest.NAME + "," + t-guest.vorname1 + " " + t-guest.anrede1.
        ELSE tStr = " ".
        ASSIGN
            output-list.str = output-list.str + STRING(tStr,"x(50)")
            output-list.str = output-list.str + STRING(debit.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + string(debitor.zahlkonto,">>>>9")
            output-list.str = output-list.str + string(debitor.vesrdep,"->,>>>,>>>,>>9.99")
            output-list.str = output-list.str + STRING(artikel.bezeich,"x(40)").
        /*Eko 25062015*/
        
        t-credit = t-credit + debitor.saldo. 
        t-famt = t-famt + debitor.vesrdep. 
        tot-credit = tot-credit + debitor.saldo. 
        tot-saldo = tot-saldo + debitor.saldo. 
        tot-foreign = tot-foreign + debitor.vesrdep.
        tot-famt = tot-famt + debitor.vesrdep.

        FIND FIRST s-list WHERE s-list.artnr = art.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.artnr = art.artnr. 
          s-list.bezeich = art.bezeich. 
        END. 
        s-list.betrag = s-list.betrag + debitor.saldo. 
      END. 
  END.

  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-saldo. 
  output-list.pay-famt = tot-foreign.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, " ->>,>>>,>>>,>>9.99").  /*ITA*/
  ELSE 
    output-list.str = output-list.str + "T O T A L " 
                    + STRING(tot-saldo,  " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-foreign, "   ->>>,>>>,>>>,>>9"). 
  
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 58: 
    output-list.str = output-list.str + " ". 
  END. 

  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = t-credit. 
  output-list.pay-famt = t-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(t-famt, "->>,>>>,>>>,>>9.99"). /*ITA*/ 
  ELSE 
    output-list.str = output-list.str + "Sub-Total " 
                    + STRING(t-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(t-famt, "  ->>>,>>>,>>>,>>9") .

  CREATE output-list.
  CREATE output-list. 
  DO i = 1 TO 56: 
      output-list.str = output-list.str + " ". 
  END. 
  
  /* Naufal Afthar - D7F30E*/
  output-list.pay-amt = tot-credit. 
  output-list.pay-famt = tot-famt.
  
  IF NOT long-digit THEN 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, "->,>>>,>>>,>>9.99")
                    + FILL(" ", 78)
                    + STRING(tot-famt,  "->>,>>>,>>>,>>9.99"). 
  ELSE 
    output-list.str = output-list.str + "Grand TOTAL " 
                    + STRING(tot-credit, " ->>>,>>>,>>>,>>9")
                    + FILL(" ", 78)
                    + STRING(tot-famt, "  ->>>,>>>,>>>,>>9"). 
                     
  RUN create-tot-payment. 
END. 






DEFINE TEMP-TABLE output-list 
    FIELD ar-recid AS INTEGER 
    FIELD info AS CHAR 
    FIELD wabkurz AS CHAR FORMAT "x(4)" 
    FIELD maildate AS DATE LABEL "MailDate" INITIAL ? 
    FIELD inv-no AS CHAR FORMAT "x(9)"
    /*Naufal - CHG From STR*/
    FIELD datum     AS DATE     FORMAT "99/99/99"               LABEL "Date"
    FIELD mflag     AS CHAR     FORMAT "x(1)"                   LABEL " "
    FIELD bill-no   AS CHARACTER                                LABEL "Bill-No"
    FIELD rm-no     AS CHAR     FORMAT "x(6)"                   LABEL "RmNo"
    FIELD receiver  AS CHAR     FORMAT "x(38)"                  LABEL "Bill Receiver"
    FIELD saldo     AS CHARACTER                                LABEL "Debt Amount"
    FIELD fsaldo    AS CHARACTER                                LABEL "Foreign Amt"
    FIELD userinit  AS CHAR     FORMAT "x(4)"                   LABEL "ID"
    FIELD vesrcod   AS CHAR     FORMAT "x(38)"                  LABEL "Additional Info"
    /*END*/
    FIELD ref-no1   AS CHARACTER                    LABEL "Comp-No"
    FIELD ref-no2   AS CHAR    FORMAT "x(32)"       LABEL "Ref-No"
    FIELD ci-date   AS DATE    FORMAT "99/99/99"    LABEL "C/I Date"
    FIELD co-date   AS DATE    FORMAT "99/99/99"    LABEL "C/O Date"
    FIELD nights    AS CHARACTER                    LABEL "Nights"
    FIELD verstat   AS INTEGER /* Add by Michael @ 14/08/2019 for add delete journal feature */
    FIELD selected  AS LOGICAL  INITIAL NO
    FIELD ref-no3   AS INTEGER FORMAT ">>>>>>>>>"  /*refno ar-payment gerald 100620*/
    . 

DEFINE TEMP-TABLE edit-list
    FIELD rechnr    AS INTEGER FORMAT ">>>>>>>>>9"
    FIELD datum     AS DATE FORMAT "99/99/99"
    FIELD zinr      LIKE zimmer.zinr
    FIELD billname  AS CHAR FORMAT "x(32)"
    FIELD lamt      AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD famt      AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD fcurr     AS CHAR FORMAT "x(4)"
    FIELD ar-recid  AS INTEGER
    FIELD amt-change AS LOGICAL INITIAL NO
    FIELD curr-change AS LOGICAL INITIAL NO
    FIELD curr-nr   AS INTEGER
    .

DEFINE INPUT PARAMETER  from-name   AS CHAR.
DEFINE INPUT PARAMETER  to-name     AS CHAR.
DEFINE INPUT PARAMETER  from-date   AS DATE.
DEFINE INPUT PARAMETER  to-date     AS DATE.
DEFINE INPUT PARAMETER  from-art    AS INTEGER.
DEFINE INPUT PARAMETER  to-art      AS INTEGER.
DEFINE INPUT PARAMETER  tot-flag    AS LOGICAL.
DEFINE INPUT PARAMETER  lesspay     AS LOGICAL.
DEFINE INPUT PARAMETER  show-inv    AS LOGICAL.
DEFINE INPUT PARAMETER  case-type   AS INTEGER.
DEFINE OUTPUT PARAMETER d-rechnr    AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.
DEFINE OUTPUT PARAMETER TABLE FOR edit-list.

CASE case-type:
    WHEN 0 THEN
    DO:
        IF SUBSTR(to-name,1,2) = "zz" THEN
        DO:
            RUN create-listA. /*DONE 060520*/
        END.    
        ELSE
        DO:
            RUN create-list. /*DONE 080520*/
        END.  
    END.
    WHEN 1 THEN
    DO:
        IF SUBSTR(to-name,1,2) = "zz" THEN
        DO:
            RUN create-list1A. /*DONE 080520*/
        END.   
        ELSE 
        DO:
            RUN create-list1.   /*DONE 110520*/
        END.   
    END.
    WHEN 2 THEN
    DO:
        IF SUBSTR(to-name,1,2) = "zz" THEN 
        DO:
            RUN create-list2A.  /*DONE 110520*/
        END.    
        ELSE 
        DO:
            RUN create-list2.   /*DONE 110520*/
        END.    
    END.
END CASE.

PROCEDURE create-list: 
DEFINE VARIABLE artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-debit AS DECIMAL. 
DEFINE VARIABLE tot-debit AS DECIMAL. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE receiver AS CHAR FORMAT "x(38)". 
DEFINE VARIABLE saldo AS DECIMAL. 
DEFINE VARIABLE bill-str AS CHAR FORMAT "x(11)". 
DEFINE buffer debt FOR debitor. 
DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-saldo AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-saldo AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-debit AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-debit AS DECIMAL INITIAL 0. 
DEFINE VARIABLE fsaldo AS DECIMAL INITIAL 0.
DEFINE VARIABLE fcurr  AS CHAR FORMAT "x(4)".
  
  FOR EACH output-list: 
    delete output-list. 
  END. 

  FOR EACH edit-list:
      DELETE edit-list.
  END.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto = 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr 
    AND guest.name GE from-name AND guest.name LE to-name NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr BY debitor.rgdatum: 
 
    IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
    IF curr-gastnr NE debitor.gastnr THEN 
    DO: 
      curr-gastnr = debitor.gastnr. 
      IF tot-saldo NE 0 AND tot-flag THEN 
      DO: 
        create output-list. 
        /*DO i = 1 TO 49: 
          output-list.str = output-list.str + " ". 
        END. 
        /*output-list.str = output-list.str + "   T O T A L"*/
        output-list.str = output-list.str + "   Sub-Total"
          + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
          + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
        /*Naufal 080520 - adjust from str to field*/
        DO i = 1 TO 29:
            output-list.receiver = output-list.receiver + " ".
        END.
        ASSIGN
            output-list.receiver = output-list.receiver + "Sub-Total"
            output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
            output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
        /*end*/
        create output-list. 
        tot-saldo = 0. 
        tf-saldo = 0. 
      END. 
    END. 

    saldo = debitor.saldo. 
    fsaldo = debitor.vesrdep.
    
    IF debitor.counter GT 0 AND lesspay THEN 
    FOR EACH debt WHERE debt.counter = debitor.counter 
      AND debt.opart GE 1 AND debt.zahlkonto GT 0 
      AND debt.rgdatum GE from-date AND debt.rgdatum LE to-date NO-LOCK: 
      saldo = saldo + debt.saldo. 
      fsaldo = fsaldo + debt.vesrdep.
    END. 
    IF (saldo GE -0.05) AND (saldo LE 0.05) THEN saldo = 0. 
    IF saldo NE 0 THEN 
    DO: 
      IF artnr NE artikel.artnr THEN 
      DO: 
        IF artnr NE 0 THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 
          IF tot-saldo NE 0 AND tot-flag THEN 
          DO: 
            create output-list. 
            /*DO i = 1 TO 49: 
              output-list.str = output-list.str + " ". 
            END. 
            /*output-list.str = output-list.str + "   T O T A L"*/
            output-list.str = output-list.str + "   Sub-Total"
              + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
              + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */

            /*Naufal 080520 - adjust from str to field*/
            DO i = 1 TO 29:
                output-list.receiver = output-list.receiver + " ".
            END.
            ASSIGN
                output-list.receiver = output-list.receiver + "Sub-Total"
                output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") 
                output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99"). 
            /*end*/
            tot-saldo = 0. 
            tf-saldo = 0. 
            create output-list. 
          END. 
          create output-list. 
          /*DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END. 
          /*output-list.str = output-list.str + "   Sub-Total"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/ 
          IF tot-flag THEN
            output-list.str = output-list.str + "   T O T A L"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
          ELSE
            output-list.str = output-list.str + "   Sub-Total"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). */

          /*Naufal 050520 - adjust from str to field*/
          DO i = 1 TO 29:
              output-list.receiver = output-list.receiver + " ".
          END.
          IF tot-flag THEN
          DO:
              ASSIGN
                  output-list.receiver = output-list.receiver + "T O T A L"
                  output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
                  output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
          END.
          ELSE
          DO:
              ASSIGN
                  output-list.receiver = output-list.receiver + "Sub-Total"
                  output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")  
                  output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
          END.
          /*end*/
          create output-list. 
          t-debit = 0. 
          tf-debit = 0. 
          tot-saldo = 0. 
          tf-saldo = 0. 
        END. 
        create output-list. 
        /*DO i = 1 TO 21: 
          output-list.str = output-list.str + " ". 
        END. 
        output-list.str = output-list.str 
          + STRING(artikel.artnr, ">>>>>9") + " - " 
          + STRING(artikel.bezeich, "x(30)"). */

        /*Naufal 080520 - adjust from str to field*/
        output-list.receiver = STRING(artikel.artnr, ">>>>>9") + " - "
                             + STRING(artikel.bezeich, "x(30)").
        /*end*/
        artnr = artikel.artnr. 
      END. 
      receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
        + guest.anrede1. 
      create output-list. 
      ASSIGN 
          output-list.ref-no1 = STRING(guest.firmen-nr)
          output-list.ref-no2 = guest.steuernr
          output-list.ref-no3 = debitor.debref. /*ref no. ar-peyment gerald 100620*/
      /*IF show-inv THEN
      DO:*/
            FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bill THEN
            DO:
                d-rechnr = debitor.rechnr.
            END.
            ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").
      /*END.*/
      IF debitor.verstat = 1 THEN bill-str = 
        "M" + STRING(debitor.rechnr, ">>,>>>,>>9"). 
      ELSE bill-str = STRING(debitor.rechnr, ">>>,>>>,>>9"). 
      /*output-list.str = STRING(debitor.rgdatum) 
        + bill-str 
        + STRING(debitor.zinr, "x(6)") 
        + STRING(receiver, "x(38)") 
        + STRING(saldo, "->,>>>,>>>,>>>,>>9.99").*/ /*sis 020915*/
      /*Naufal 060520*/
      ASSIGN
          output-list.datum     = debitor.rgdatum
          output-list.mflag     = SUBSTR(bill-str,1,1)
          output-list.bill-no   = STRING(debitor.rechnr, ">>>,>>>,>>9")
          output-list.rm-no     = debitor.zinr
          output-list.receiver  = receiver
          output-list.saldo     = STRING(saldo, "->,>>>,>>>,>>>,>>9.99").
      FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
        NO-LOCK NO-ERROR. 
      /*IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(4)"). 
      ELSE output-list.str = output-list.str + "  ". */
      /*Naufal 080520*/
      IF AVAILABLE bediener THEN
          output-list.userinit = bediener.userinit.
      ELSE
          output-list.userinit = "  ".
      /*output-list.str = output-list.str + "  " 
        + STRING(fsaldo, "->>>,>>>,>>>,>>9.99").*/
      output-list.fsaldo  = STRING(fsaldo, "->,>>>,>>>,>>>,>>9.99").
      /*end*/
      output-list.verstat = debitor.verstat. /* Add by Michael @ 14/08/2019 for add delete journal feature */
      /*DO j = 1 TO 38: 
        IF SUBSTR(debitor.vesrcod,j,1) EQ chr(10) THEN 
          output-list.str = output-list.str + " ". 
        ELSE output-list.str = output-list.str + SUBSTR(debitor.vesrcod,j,1). 
      END. */
      /*Naufal 060520*/
      DO j = 1 TO 38:
          IF SUBSTR(debitor.vesrcod,j,1) EQ CHR(10) THEN
              output-list.vesrcod = " ".
          ELSE
              output-list.vesrcod = output-list.vesrcod + SUBSTR(debitor.vesrcod,j,1).
      END.
      /*end*/
      output-list.ar-recid = RECID(debitor). 
      output-list.info = debitor.vesrcod. 
      IF debitor.versanddat NE ? THEN output-list.maildate = debitor.versanddat. 
 
      IF debitor.betrieb-gastmem NE 0 THEN 
      DO: 
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN 
            output-list.wabkurz = waehrung.wabkurz. 
      END. 
      
      /*M additional column : ci-date, co-date, nights  */
      IF debitor.betriebsnr EQ 0 THEN  /*M from departmen FO */
      DO:
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.resnr GT 0
              AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
              IF bill.reslinnr EQ 0 THEN  /*M master bill */
              DO:
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.resstatus = 8 NO-LOCK NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9")
                          .
                  END.  
              END.
              ELSE
              DO: 
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9")
                          .
                  END.  
              END.
          END.
          ELSE DO:   /*ITA*/
              DEFINE VARIABLE resnr AS INTEGER NO-UNDO.
              IF debitor.vesrcod NE " " AND debitor.vesrcod MATCHES "*Deposit Payment*" THEN DO:
                    ASSIGN resnr = INTEGER(ENTRY(2, ENTRY(1,debitor.vesrcod, ";"), ":")).
                    FIND FIRST res-line WHERE res-line.resnr = resnr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                             ASSIGN  
                              output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9").
                    END.
              END.
          END.
      END.

      CREATE edit-list.
      ASSIGN 
          edit-list.rechnr   = debitor.rechnr
          edit-list.ar-recid = RECID(debitor)
          edit-list.datum    = debitor.rgdatum
          edit-list.zinr     = debitor.zinr
          edit-list.billname = receiver
          edit-list.famt     = debitor.vesrdep
          edit-list.fcurr    = output-list.wabkurz
          edit-list.curr-nr  = debitor.betrieb-gastmem.
      
 
      t-debit = t-debit + saldo. 
      tot-debit = tot-debit + saldo. 
      tot-saldo = tot-saldo + saldo. 
      tf-debit = tf-debit + fsaldo. 
      ttf-debit = ttf-debit + fsaldo. 
      tf-saldo = tf-saldo + fsaldo. 
    END. 
  END. 
 
  IF tot-saldo NE 0 AND tot-flag THEN 
  DO: 
    create output-list. 
    /*DO i = 1 TO 49: 
      output-list.str = output-list.str + " ". 
    END. 
    /*output-list.str = output-list.str + "   T O T A L"*/
    output-list.str = output-list.str + "   Sub-Total"
      + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
      + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
    /*Naufal 080520*/
    DO i = 1 TO 29:
        output-list.receiver = output-list.receiver + " ".
    END.
    ASSIGN
        output-list.receiver = output-list.receiver + "Sub-Total"
        output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
        output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
    /*end*/
    create output-list. 
  END. 
  create output-list. 
  /*DO i = 1 TO 49: 
      output-list.str = output-list.str + " ". 
  END. 
  /*output-list.str = output-list.str + "   Sub-Total"
       + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
       + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/ 
  IF tot-flag THEN
    output-list.str = output-list.str + "   T O T A L"
    + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
    + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
  ELSE
    output-list.str = output-list.str + "   Sub-Total"
    + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
    + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). */
  /*Naufal 080520*/
  DO i = 1 TO 29:
      output-list.receiver = output-list.receiver + " ".
  END.
  IF tot-flag THEN
      ASSIGN
          output-list.receiver = output-list.receiver + "T O T A L"
          output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
          output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
  ELSE
      ASSIGN
          output-list.receiver = output-list.receiver + "Sub-Total"
          output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")  
          output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
  /*end*/
  create output-list. 
  create output-list. 
  /*DO i = 1 TO 47: 
      output-list.str = output-list.str + " ". 
  END. 
  output-list.str = output-list.str + "   Grand TOTAL" 
       + STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
       + STRING(ttf-debit, "->,>>>,>>>,>>>,>>9.99"). */
  /*Naufal 080520*/
  DO i = 1 TO 27:
      output-list.receiver = output-list.receiver + " ".
  END.
  ASSIGN
      output-list.receiver = output-list.receiver + "Grand TOTAL"
      output-list.saldo    = STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99")
      output-list.fsaldo   = STRING(ttf-debit, "->,>>>,>>>,>>>,>>9.99").
  /*end*/
END. 
 
PROCEDURE create-listA: 
DEFINE VARIABLE artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-debit AS DECIMAL. 
DEFINE VARIABLE tot-debit AS DECIMAL. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE receiver AS CHAR FORMAT "x(38)". 
DEFINE VARIABLE saldo AS DECIMAL. 
DEFINE VARIABLE bill-str AS CHAR FORMAT "x(11)". 
DEFINE buffer debt FOR debitor. 
DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-saldo AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-saldo AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-debit AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-debit AS DECIMAL INITIAL 0. 
DEFINE VARIABLE fsaldo AS DECIMAL INITIAL 0.
  
  FOR EACH output-list: 
    delete output-list. 
  END. 

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto = 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr 
    AND guest.name GE from-name NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr BY debitor.rgdatum: 
 
    IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
    IF curr-gastnr NE debitor.gastnr THEN 
    DO:
      curr-gastnr = debitor.gastnr. 
      IF tot-saldo NE 0 AND tot-flag THEN 
      DO:
        /*Tidak masuk kesini saat pertama execute*/                         
        create output-list.                                                 
        /*DO i = 1 TO 49:                                                   
          output-list.str = output-list.str + " ".                          
        END.                                                                
        /*output-list.str = output-list.str + "   T O T A L"*/              
        output-list.str = output-list.str + "   Sub-Total"                  
          + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
          + STRING(tf-saldo,    "->>>,>>>,>>>,>>9.99").*/

        /*Naufal 050520 - adjust from str to field*/
        DO i = 1 TO 29:
            output-list.receiver = output-list.receiver + " ".
        END.
        ASSIGN
            output-list.receiver = output-list.receiver + "Sub-Total"
            output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
            output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
        /*end*/
        create output-list.                                         
        tot-saldo = 0.                                              
        tf-saldo = 0.                                               
      END.                                                          
    END.                                                            
    saldo = debitor.saldo.                                          
    fsaldo = debitor.vesrdep .
    IF debitor.counter GT 0 AND lesspay THEN 
    FOR EACH debt WHERE debt.counter = debitor.counter 
      AND debt.opart GE 1 AND debt.zahlkonto GT 0 
      AND debt.rgdatum GE from-date AND debt.rgdatum LE to-date NO-LOCK: 
      saldo = saldo + debt.saldo. 
      fsaldo = fsaldo + debt.vesrdep.
    END. 
    IF (saldo GE -0.05) AND (saldo LE 0.05) THEN saldo = 0. 
 
    IF saldo NE 0 THEN 
    DO: 
      IF artnr NE artikel.artnr THEN 
      DO: 
        IF artnr NE 0 THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 
          IF tot-saldo NE 0 AND tot-flag THEN 
          DO: 
            create output-list. 
            /*DO i = 1 TO 49: 
              output-list.str = output-list.str + " ". 
            END. 
            /*output-list.str = output-list.str + "   T O T A L"*/ 
            output-list.str = output-list.str + "   Sub-Total"
              + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
              + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99").*/

            /*Naufal 050520 - adjust from str to field*/
            DO i = 1 TO 29:
                output-list.receiver = output-list.receiver + " ".
            END.
            ASSIGN
                output-list.receiver = output-list.receiver + "Sub-Total"
                output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
                output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
            /*end*/
            tot-saldo = 0. 
            tf-saldo = 0. 
            create output-list. 
          END. 
          create output-list. 
          /*DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END.*/
          /*output-list.str = output-list.str + "   Sub-Total" 
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/ 
          /*IF tot-flag THEN
            output-list.str = output-list.str + "   T O T A L"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
          ELSE
            output-list.str = output-list.str + "   Sub-Total"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/

          /*Naufal 050520 - adjust from str to field*/
          DO i = 1 TO 29:
              output-list.receiver = output-list.receiver + " ".
          END.
          IF tot-flag THEN
          DO:
              ASSIGN
                  output-list.receiver = output-list.receiver + "T O T A L"
                  output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
                  output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
          END.
          ELSE
          DO:
              ASSIGN
                  output-list.receiver = output-list.receiver + "Sub-Total"
                  output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")  
                  output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
          END.
          /*end*/
          create output-list. 
          t-debit = 0. 
          tf-debit = 0. 
          tot-saldo = 0. 
          tf-saldo = 0. 
        END. 
        create output-list.
        /*
        DO i = 1 TO 21: 
          output-list.str = output-list.str + " ". 
        END. 
        output-list.str = output-list.str 
          + STRING(artikel.artnr, ">>>>>9") + " - " 
          + STRING(artikel.bezeich, "x(30)").*/

        /*Naufal 050520 - adjust from str to field*/
        output-list.receiver = STRING(artikel.artnr, ">>>>>9") + " - "
                             + STRING(artikel.bezeich, "x(30)").
        /*end*/
        artnr = artikel.artnr. 
      END. 
      receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
        + guest.anrede1. 
      create output-list. 
      ASSIGN 
          output-list.ref-no1 = STRING(guest.firmen-nr)
          output-list.ref-no2 = guest.steuernr
          output-list.ref-no3 = debitor.debref. /*ref no. ar-peyment gerald 100620*/
      /*IF show-inv THEN
        DO:*/
            FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bill THEN
            DO:
                d-rechnr = debitor.rechnr.
            END.
            ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").
        /*END.*/
      IF debitor.verstat = 1 THEN bill-str = 
        "M" + STRING(debitor.rechnr, ">>,>>>,>>9"). 
      ELSE bill-str = STRING(debitor.rechnr, ">>>,>>>,>>9").
      /*output-list.str = STRING(debitor.rgdatum) 
        + bill-str 
        + STRING(debitor.zinr, "x(6)") 
        + STRING(receiver, "x(38)") 
        + STRING(saldo, "->,>>>,>>>,>>>,>>9.99").*/  /*sis 020915*/
      /*Naufal 060520*/
      ASSIGN
          output-list.datum     = debitor.rgdatum
          output-list.mflag     = SUBSTR(bill-str,1,1)
          output-list.bill-no   = STRING(debitor.rechnr, ">>>,>>>,>>9")
          output-list.rm-no     = debitor.zinr
          output-list.receiver  = receiver
          output-list.saldo     = STRING(saldo, "->,>>>,>>>,>>>,>>9.99").
      FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
        NO-LOCK NO-ERROR. 
      /*IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit, "x(4)"). 
      ELSE output-list.str = output-list.str + "  ".*/
      IF AVAILABLE bediener THEN
          output-list.userinit = bediener.userinit.
      ELSE
          output-list.userinit = "  ".
      /*output-list.str = output-list.str 
        + STRING(fsaldo, "->>>,>>>,>>>,>>9.99").*/
    /*Naufal 060520*/
      output-list.fsaldo = STRING(fsaldo, "->,>>>,>>>,>>>,>>9.99").
      output-list.verstat = debitor.verstat. /* Add by Michael @ 14/08/2019 for add delete journal feature */
      /*DO j = 1 TO 38: 
        IF SUBSTR(debitor.vesrcod,j,1) EQ chr(10) THEN 
          output-list.str = output-list.str + " ". 
        ELSE output-list.str = output-list.str + SUBSTR(debitor.vesrcod,j,1). 
      END.*/
    /*end*/
    /*Naufal 060520*/
      DO j = 1 TO 38:
          IF SUBSTR(debitor.vesrcod,j,1) EQ CHR(10) THEN
              output-list.vesrcod = " ".
          ELSE
              output-list.vesrcod = output-list.vesrcod + SUBSTR(debitor.vesrcod,j,1).
      END.
    /*end*/
      output-list.ar-recid = RECID(debitor). 
      output-list.info = debitor.vesrcod. 
      IF debitor.versanddat NE ? THEN output-list.maildate = debitor.versanddat. 
 
      IF debitor.betrieb-gastmem NE 0 THEN 
      DO: 
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN output-list.wabkurz = waehrung.wabkurz. 
      END. 

      /*M additional column : ci-date, co-date, nights  */
      IF debitor.betriebsnr EQ 0 THEN  /*M from departmen FO */
      DO:
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.resnr GT 0
              AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
              IF bill.reslinnr EQ 0 THEN  /*M master bill */
              DO:
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.resstatus = 8 NO-LOCK NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9")
                          .
                  END.  
              END.
              ELSE
              DO:
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9")
                          .
                  END.  
              END.
          END.
          ELSE DO: /*ITA*/
              DEFINE VARIABLE resnr AS INTEGER NO-UNDO.
              IF debitor.vesrcod NE " " AND debitor.vesrcod MATCHES "*Deposit Payment*" THEN DO:
                    ASSIGN resnr = INTEGER(ENTRY(2, ENTRY(1,debitor.vesrcod, ";"), ":")).
                    FIND FIRST res-line WHERE res-line.resnr = resnr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                             ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9").
                    END.
              END.          
          END.
      END.

      CREATE edit-list.
      ASSIGN 
          edit-list.rechnr   = debitor.rechnr
          edit-list.ar-recid = RECID(debitor)
          edit-list.datum    = debitor.rgdatum
          edit-list.zinr     = debitor.zinr
          edit-list.billname = receiver
          edit-list.famt     = debitor.vesrdep
          edit-list.fcurr    = output-list.wabkurz
          edit-list.curr-nr  = debitor.betrieb-gastmem.
      
 
      t-debit = t-debit + saldo. 
      tot-debit = tot-debit + saldo. 
      tot-saldo = tot-saldo + saldo. 
      tf-debit = tf-debit + fsaldo. 
      ttf-debit = ttf-debit + fsaldo. 
      tf-saldo = tf-saldo + fsaldo. 
    END. 
  END. 
 
  IF tot-saldo NE 0 AND tot-flag THEN 
  DO: 
    create output-list. 
    /*DO i = 1 TO 49: 
      output-list.str = output-list.str + " ". 
    END. 
    /*output-list.str = output-list.str + "   T O T A L"*/
    output-list.str = output-list.str + "   Sub-Total"
      + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
      + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99").*/
    /*Naufal 060520*/
    DO i = 1 TO 29:
        output-list.receiver = output-list.receiver + " ".
    END.
    ASSIGN
        output-list.receiver = output-list.receiver + "Sub-Total"
        output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
        output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
    /*end*/
    create output-list. 
  END. 
  create output-list. 
  /*DO i = 1 TO 49: 
      output-list.str = output-list.str + " ". 
  END. 
  /*output-list.str = output-list.str + "   Sub-Total"
       + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
       + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/ 
  IF tot-flag THEN
    output-list.str = output-list.str + "   T O T A L"
    + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
    + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
  ELSE
    output-list.str = output-list.str + "   Sub-Total"
    + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
    + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/
  /*Naufal 060520*/
  DO i = 1 TO 29:
      output-list.receiver = output-list.receiver + " ".
  END.
  IF tot-flag THEN
      ASSIGN
          output-list.receiver = output-list.receiver + "T O T A L"
          output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
          output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
  ELSE
      ASSIGN
          output-list.receiver = output-list.receiver + "Sub-Total"
          output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")   
          output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
  /*end*/
  create output-list. 
  create output-list. 
  /*DO i = 1 TO 47: 
      output-list.str = output-list.str + " ". 
  END. 
  output-list.str = output-list.str + "   Grand TOTAL" 
       + STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
       + STRING(ttf-debit, "->,>>>,>>>,>>>,>>9.99"). */
  /*Naufal 060520*/
  DO i = 1 TO 27:
      output-list.receiver = output-list.receiver + " ".
  END.
  ASSIGN
      output-list.receiver = output-list.receiver + "Grand TOTAL"
      output-list.saldo    = STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99")
      output-list.fsaldo   = STRING(ttf-debit, "->,>>>,>>>,>>>,>>9.99").
  /*end*/
END. 

PROCEDURE create-list1: 
DEFINE VARIABLE artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-debit AS DECIMAL. 
DEFINE VARIABLE tot-debit AS DECIMAL. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE receiver AS CHAR FORMAT "x(38)". 
DEFINE VARIABLE saldo AS DECIMAL. 
DEFINE VARIABLE bill-str AS CHAR FORMAT "x(11)". 
DEFINE buffer debt FOR debitor. 
DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-saldo AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-saldo AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-debit AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-debit AS DECIMAL INITIAL 0. 
DEFINE VARIABLE fsaldo AS DECIMAL INITIAL 0.
DEFINE VARIABLE fcurr  AS CHAR FORMAT "x(4)".
  
  FOR EACH output-list: 
    delete output-list. 
  END. 

  FOR EACH edit-list:
      DELETE edit-list.
  END.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto = 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.verstat EQ 9 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr 
    AND guest.name GE from-name AND guest.name LE to-name NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr BY debitor.rgdatum: 
 
    IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
    IF curr-gastnr NE debitor.gastnr THEN 
    DO: 
      curr-gastnr = debitor.gastnr. 
      IF tot-saldo NE 0 AND tot-flag THEN 
      DO: 
        create output-list. 
        /*DO i = 1 TO 49: 
          output-list.str = output-list.str + " ". 
        END. 
        /*output-list.str = output-list.str + "   T O T A L"*/
        output-list.str = output-list.str + "   Sub-Total"
          + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
          + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
        /*Naufal 080520 - adjust from str to field*/
        DO i = 1 TO 29:
            output-list.receiver = output-list.receiver + " ".
        END.
        ASSIGN
            output-list.receiver = output-list.receiver + "Sub-Total"
            output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
            output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
        /*end*/
        create output-list. 
        tot-saldo = 0. 
        tf-saldo = 0. 
      END. 
    END. 

    saldo = debitor.saldo. 
    fsaldo = debitor.vesrdep.
    
    IF debitor.counter GT 0 AND lesspay THEN 
    FOR EACH debt WHERE debt.counter = debitor.counter 
      AND debt.opart GE 1 AND debt.zahlkonto GT 0 
      AND debt.rgdatum GE from-date AND debt.rgdatum LE to-date NO-LOCK: 
      saldo = saldo + debt.saldo. 
      fsaldo = fsaldo + debt.vesrdep.
    END. 
    IF (saldo GE -0.05) AND (saldo LE 0.05) THEN saldo = 0. 
    IF saldo NE 0 THEN 
    DO: 
      IF artnr NE artikel.artnr THEN 
      DO: 
        IF artnr NE 0 THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 
          IF tot-saldo NE 0 AND tot-flag THEN 
          DO: 
            create output-list. 
            /*DO i = 1 TO 49: 
              output-list.str = output-list.str + " ". 
            END. 
            /*output-list.str = output-list.str + "   T O T A L"*/
            output-list.str = output-list.str + "   Sub-Total"
              + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
              + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
            /*Naufal 080520 - adjust from str to field*/
            DO i = 1 TO 29:
                output-list.receiver = output-list.receiver + " ".
            END.
            ASSIGN
                output-list.receiver = output-list.receiver + "Sub-Total"
                output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") 
                output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99"). 
            /*end*/
            tot-saldo = 0. 
            tf-saldo = 0. 
            create output-list. 
          END. 
          create output-list. 
          /*DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END. 
          /*output-list.str = output-list.str + "   Sub-Total"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/ 
          IF tot-flag THEN
            output-list.str = output-list.str + "   T O T A L"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
          ELSE
            output-list.str = output-list.str + "   Sub-Total"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). */
          /*Naufal 080520 - adjust from str to field*/
          DO i = 1 TO 29:
              output-list.receiver = output-list.receiver + " ".
          END.
          IF tot-flag THEN
          DO:
              ASSIGN
                  output-list.receiver = output-list.receiver + "T O T A L"
                  output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
                  output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
          END.
          ELSE
          DO:
              ASSIGN
                  output-list.receiver = output-list.receiver + "Sub-Total"
                  output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")  
                  output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
          END.
          /*end*/
          create output-list. 
          t-debit = 0. 
          tf-debit = 0. 
          tot-saldo = 0. 
          tf-saldo = 0. 
        END. 
        create output-list. 
        /*DO i = 1 TO 21: 
          output-list.str = output-list.str + " ". 
        END. 
        output-list.str = output-list.str 
          + STRING(artikel.artnr, ">>>>>9") + " - " 
          + STRING(artikel.bezeich, "x(30)"). */
        /*Naufal 110520*/
        output-list.receiver = STRING(artikel.artnr, ">>>>>9") + " - "
                             + STRING(artikel.bezeich, "x(30)").
        /*end*/
        artnr = artikel.artnr. 
      END. 
      receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
        + guest.anrede1. 
      create output-list. 
      ASSIGN 
          output-list.ref-no1 = STRING(guest.firmen-nr)
          output-list.ref-no2 = guest.steuernr
          output-list.ref-no3 = debitor.debref. /*ref no. ar-peyment gerald 100620*/
      /*IF show-inv THEN
      DO:*/
            FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bill THEN
            DO:
                d-rechnr = debitor.rechnr.
            END.
            ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").
      /*END.*/
      IF debitor.verstat = 1 THEN bill-str = 
        "M" + STRING(debitor.rechnr, ">>,>>>,>>9"). 
      ELSE bill-str = STRING(debitor.rechnr, ">>>,>>>,>>9"). 
      /*output-list.str = STRING(debitor.rgdatum) 
        + bill-str 
        + STRING(debitor.zinr, "x(6)") 
        + STRING(receiver, "x(38)") 
        + STRING(saldo, "->,>>>,>>>,>>>,>>9.99"). */ /*sis 020915*/
      /*Naufal 110520*/
      ASSIGN
          output-list.datum     = debitor.rgdatum
          output-list.mflag     = SUBSTR(bill-str,1,1)
          output-list.bill-no   = STRING(debitor.rechnr, ">>>,>>>,>>9")
          output-list.rm-no     = debitor.zinr
          output-list.receiver  = receiver
          output-list.saldo     = STRING(saldo, "->,>>>,>>>,>>>,>>9.99").
      FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
        NO-LOCK NO-ERROR. 
      /*IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(4)"). 
      ELSE output-list.str = output-list.str + "  ". */
      IF AVAILABLE bediener THEN
          output-list.userinit = bediener.userinit.
      ELSE
          output-list.userinit = "  ".
      /*output-list.str = output-list.str + "  " 
        + STRING(fsaldo, "->>>,>>>,>>>,>>9.99"). */
      output-list.fsaldo = STRING(fsaldo, "->,>>>,>>>,>>>,>>9.99").
      /*end*/
      output-list.verstat = debitor.verstat. /* Add by Michael @ 14/08/2019 for add delete journal feature */
      /*DO j = 1 TO 38: 
        IF SUBSTR(debitor.vesrcod,j,1) EQ chr(10) THEN 
          output-list.str = output-list.str + " ". 
        ELSE output-list.str = output-list.str + SUBSTR(debitor.vesrcod,j,1). 
      END. */
      /*Naufal 110520*/
      DO j = 1 TO 38:
          IF SUBSTR(debitor.vesrcod,j,1) EQ CHR(10) THEN
              output-list.vesrcod = " ".
          ELSE
              output-list.vesrcod = output-list.vesrcod + SUBSTR(debitor.vesrcod,j,1).
      END.
      /*end*/
      output-list.ar-recid = RECID(debitor). 
      output-list.info = debitor.vesrcod. 
      IF debitor.versanddat NE ? THEN output-list.maildate = debitor.versanddat. 
 
      IF debitor.betrieb-gastmem NE 0 THEN 
      DO: 
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN 
            output-list.wabkurz = waehrung.wabkurz. 
      END. 
      
      /*M additional column : ci-date, co-date, nights  */
      IF debitor.betriebsnr EQ 0 THEN  /*M from departmen FO */
      DO:
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.resnr GT 0
              AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
              IF bill.reslinnr EQ 0 THEN  /*M master bill */
              DO:
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.resstatus = 8 NO-LOCK NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9")
                          .
                  END.  
              END.
              ELSE
              DO: 
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9")
                          .
                  END.  
              END.
          END.
          ELSE DO:   /*ITA*/
              DEFINE VARIABLE resnr AS INTEGER NO-UNDO.
              IF debitor.vesrcod NE " " AND debitor.vesrcod MATCHES "*Deposit Payment*" THEN DO:
                    ASSIGN resnr = INTEGER(ENTRY(2, ENTRY(1,debitor.vesrcod, ";"), ":")).
                    FIND FIRST res-line WHERE res-line.resnr = resnr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                             ASSIGN  
                              output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9").
                    END.
              END.
          END.
      END.

      CREATE edit-list.
      ASSIGN 
          edit-list.rechnr   = debitor.rechnr
          edit-list.ar-recid = RECID(debitor)
          edit-list.datum    = debitor.rgdatum
          edit-list.zinr     = debitor.zinr
          edit-list.billname = receiver
          edit-list.famt     = debitor.vesrdep
          edit-list.fcurr    = output-list.wabkurz
          edit-list.curr-nr  = debitor.betrieb-gastmem.
      
 
      t-debit = t-debit + saldo. 
      tot-debit = tot-debit + saldo. 
      tot-saldo = tot-saldo + saldo. 
      tf-debit = tf-debit + fsaldo. 
      ttf-debit = ttf-debit + fsaldo. 
      tf-saldo = tf-saldo + fsaldo. 
    END. 
  END. 
 
  IF tot-saldo NE 0 AND tot-flag THEN 
  DO: 
    create output-list. 
    /*DO i = 1 TO 49: 
      output-list.str = output-list.str + " ". 
    END. 
    /*output-list.str = output-list.str + "   T O T A L"*/ 
    output-list.str = output-list.str + "   Sub-Total"
      + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
      + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
    /*Naufal 110520*/
    DO i = 1 TO 29:
        output-list.receiver = output-list.receiver + " ".
    END.
    ASSIGN
        output-list.receiver = output-list.receiver + "Sub-Total"
        output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
        output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
    /*end*/
    create output-list. 
  END. 
  create output-list. 
  /*DO i = 1 TO 49: 
      output-list.str = output-list.str + " ". 
  END. 
  /*output-list.str = output-list.str + "   Sub-Total" 
       + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
       + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/ 
  IF tot-flag THEN
    output-list.str = output-list.str + "   T O T A L"
    + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
    + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
  ELSE
    output-list.str = output-list.str + "   Sub-Total"
    + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
    + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). */
  /*Naufal 110520*/
  DO i = 1 TO 29:
      output-list.receiver = output-list.receiver + " ".
  END.
  IF tot-flag THEN
      ASSIGN
          output-list.receiver = output-list.receiver + "T O T A L"
          output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
          output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
  ELSE
      ASSIGN
          output-list.receiver = output-list.receiver + "Sub-Total"
          output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")   
          output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
  /*end*/
  create output-list. 
  create output-list. 
  /*DO i = 1 TO 47: 
      output-list.str = output-list.str + " ". 
  END. 
  output-list.str = output-list.str + "   Grand TOTAL" 
       + STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
       + STRING(ttf-debit, "->,>>>,>>>,>>>,>>9.99"). */
  /*Naufal 110520*/
  DO i = 1 TO 27:
      output-list.receiver = output-list.receiver + " ".
  END.
  ASSIGN
      output-list.receiver = output-list.receiver + "Grand TOTAL"
      output-list.saldo    = STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99")
      output-list.fsaldo   = STRING(ttf-debit, "->,>>>,>>>,>>>,>>9.99").
  /*end*/
END. 
 
PROCEDURE create-list1A: 
DEFINE VARIABLE artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-debit AS DECIMAL. 
DEFINE VARIABLE tot-debit AS DECIMAL. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE receiver AS CHAR FORMAT "x(38)". 
DEFINE VARIABLE saldo AS DECIMAL. 
DEFINE VARIABLE bill-str AS CHAR FORMAT "x(11)". 
DEFINE buffer debt FOR debitor. 
DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-saldo AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-saldo AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-debit AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-debit AS DECIMAL INITIAL 0. 
DEFINE VARIABLE fsaldo AS DECIMAL INITIAL 0.
  
  FOR EACH output-list: 
    delete output-list. 
  END. 

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto = 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.verstat EQ 9 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr 
    AND guest.name GE from-name NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr BY debitor.rgdatum: 
 
    IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
    IF curr-gastnr NE debitor.gastnr THEN 
    DO: 
      curr-gastnr = debitor.gastnr. 
      IF tot-saldo NE 0 AND tot-flag THEN 
      DO: 
        create output-list. 
        /*DO i = 1 TO 49: 
          output-list.str = output-list.str + " ". 
        END. 
        /*output-list.str = output-list.str + "   T O T A L"*/ 
        output-list.str = output-list.str + "   Sub-Total"
          + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
          + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
        /*Naufal 080520 - adjust from str to field*/
        DO i = 1 TO 29:
            output-list.receiver = output-list.receiver + " ".
        END.
        ASSIGN
            output-list.receiver = output-list.receiver + "Sub-Total"
            output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
            output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
        /*end*/
        create output-list. 
        tot-saldo = 0. 
        tf-saldo = 0. 
      END. 
    END. 
    saldo = debitor.saldo. 
    fsaldo = debitor.vesrdep .
    IF debitor.counter GT 0 AND lesspay THEN 
    FOR EACH debt WHERE debt.counter = debitor.counter 
      AND debt.opart GE 1 AND debt.zahlkonto GT 0 
      AND debt.rgdatum GE from-date AND debt.rgdatum LE to-date NO-LOCK: 
      saldo = saldo + debt.saldo. 
      fsaldo = fsaldo + debt.vesrdep.
    END. 
    IF (saldo GE -0.05) AND (saldo LE 0.05) THEN saldo = 0. 
 
    IF saldo NE 0 THEN 
    DO: 
      IF artnr NE artikel.artnr THEN 
      DO: 
        IF artnr NE 0 THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 
          IF tot-saldo NE 0 AND tot-flag THEN 
          DO: 
            create output-list. 
            /*DO i = 1 TO 49: 
              output-list.str = output-list.str + " ". 
            END. 
            /*output-list.str = output-list.str + "   T O T A L"*/
            output-list.str = output-list.str + "   Sub-Total"
              + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
              + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
            /*Naufal 080520 - adjust from str to field*/
            DO i = 1 TO 29:
                output-list.receiver = output-list.receiver + " ".
            END.
            ASSIGN
                output-list.receiver = output-list.receiver + "Sub-Total"
                output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
                output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
            /*end*/
            tot-saldo = 0. 
            tf-saldo = 0. 
            create output-list. 
          END. 
          create output-list. 
          /*DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END. 
          /*output-list.str = output-list.str + "   Sub-Total"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/ 
          IF tot-flag THEN
            output-list.str = output-list.str + "   T O T A L"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
          ELSE
            output-list.str = output-list.str + "   Sub-Total"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). */
          /*Naufal 080520 - adjust from str to field*/
          DO i = 1 TO 29:
              output-list.receiver = output-list.receiver + " ".
          END.
          IF tot-flag THEN
          DO:
              ASSIGN
                  output-list.receiver = output-list.receiver + "T O T A L"
                  output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
                  output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
          END.
          ELSE
          DO:
              ASSIGN
                  output-list.receiver = output-list.receiver + "Sub-Total"
                  output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")  
                  output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
          END.
          /*end*/
          create output-list. 
          t-debit = 0. 
          tf-debit = 0. 
          tot-saldo = 0. 
          tf-saldo = 0. 
        END. 
        create output-list. 
        /*DO i = 1 TO 21: 
          output-list.str = output-list.str + " ". 
        END. 
        output-list.str = output-list.str 
          + STRING(artikel.artnr, ">>>>>9") + " - " 
          + STRING(artikel.bezeich, "x(30)"). */
        /*Naufal 080520 - adjust from str to field*/
        output-list.receiver = STRING(artikel.artnr, ">>>>>9") + " - "
                             + STRING(artikel.bezeich, "x(30)").
        /*end*/
        artnr = artikel.artnr. 
      END. 
      receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
        + guest.anrede1. 
      create output-list. 
      ASSIGN 
          output-list.ref-no1 = STRING(guest.firmen-nr)
          output-list.ref-no2 = guest.steuernr
          output-list.ref-no3 = debitor.debref. /*ref no. ar-peyment gerald 100620*/
      /*IF show-inv THEN
        DO:*/
            FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bill THEN
            DO:
                d-rechnr = debitor.rechnr.
            END.
            ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").
        /*END.*/
      IF debitor.verstat = 1 THEN bill-str = 
        "M" + STRING(debitor.rechnr, ">>,>>>,>>9"). 
      ELSE bill-str = STRING(debitor.rechnr, ">>>,>>>,>>9"). 
      /*output-list.str = STRING(debitor.rgdatum) 
        + bill-str 
        + STRING(debitor.zinr, "x(6)") 
        + STRING(receiver, "x(38)") 
        + STRING(saldo, "->,>>>,>>>,>>>,>>9.99"). */ /*sis 020915*/
      /*Naufal 080520*/
      ASSIGN
          output-list.datum     = debitor.rgdatum
          output-list.mflag     = SUBSTR(bill-str,1,1)
          output-list.bill-no   = STRING(debitor.rechnr, ">>>,>>>,>>9")
          output-list.rm-no     = debitor.zinr
          output-list.receiver  = receiver
          output-list.saldo     = STRING(saldo, "->,>>>,>>>,>>>,>>9.99").
      FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
        NO-LOCK NO-ERROR. 
      /*IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit, "x(4)"). 
      ELSE output-list.str = output-list.str + "  ". */
      IF AVAILABLE bediener THEN
          output-list.userinit = bediener.userinit.
      ELSE
          output-list.userinit = "  ".
      /*output-list.str = output-list.str 
        + STRING(fsaldo, "->>>,>>>,>>>,>>9.99"). */
      output-list.fsaldo = STRING(fsaldo, "->,>>>,>>>,>>>,>>9.99").
      /*end*/
      output-list.verstat = debitor.verstat. /* Add by Michael @ 14/08/2019 for add delete journal feature */
      /*DO j = 1 TO 38: 
        IF SUBSTR(debitor.vesrcod,j,1) EQ chr(10) THEN 
          output-list.str = output-list.str + " ". 
        ELSE output-list.str = output-list.str + SUBSTR(debitor.vesrcod,j,1). 
      END. */
      /*Naufal 080520*/
      DO j = 1 TO 38:
          IF SUBSTR(debitor.vesrcod,j,1) EQ CHR(10) THEN
              output-list.vesrcod = " ".
          ELSE
              output-list.vesrcod = output-list.vesrcod + SUBSTR(debitor.vesrcod,j,1).
      END.
      /*end*/
      output-list.ar-recid = RECID(debitor). 
      output-list.info = debitor.vesrcod. 
      IF debitor.versanddat NE ? THEN output-list.maildate = debitor.versanddat. 
 
      IF debitor.betrieb-gastmem NE 0 THEN 
      DO: 
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN output-list.wabkurz = waehrung.wabkurz. 
      END. 

      /*M additional column : ci-date, co-date, nights  */
      IF debitor.betriebsnr EQ 0 THEN  /*M from departmen FO */
      DO:
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.resnr GT 0
              AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
              IF bill.reslinnr EQ 0 THEN  /*M master bill */
              DO:
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.resstatus = 8 NO-LOCK NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9")
                          .
                  END.  
              END.
              ELSE
              DO:
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9")
                          .
                  END.  
              END.
          END.
          ELSE DO: /*ITA*/
              DEFINE VARIABLE resnr AS INTEGER NO-UNDO.
              IF debitor.vesrcod NE " " AND debitor.vesrcod MATCHES "*Deposit Payment*" THEN DO:
                    ASSIGN resnr = INTEGER(ENTRY(2, ENTRY(1,debitor.vesrcod, ";"), ":")).
                    FIND FIRST res-line WHERE res-line.resnr = resnr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                             ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9").
                    END.
              END.          
          END.
      END.

      CREATE edit-list.
      ASSIGN 
          edit-list.rechnr   = debitor.rechnr
          edit-list.ar-recid = RECID(debitor)
          edit-list.datum    = debitor.rgdatum
          edit-list.zinr     = debitor.zinr
          edit-list.billname = receiver
          edit-list.famt     = debitor.vesrdep
          edit-list.fcurr    = output-list.wabkurz
          edit-list.curr-nr  = debitor.betrieb-gastmem.
      
 
      t-debit = t-debit + saldo. 
      tot-debit = tot-debit + saldo. 
      tot-saldo = tot-saldo + saldo. 
      tf-debit = tf-debit + fsaldo. 
      ttf-debit = ttf-debit + fsaldo. 
      tf-saldo = tf-saldo + fsaldo. 
    END. 
  END. 
 
  IF tot-saldo NE 0 AND tot-flag THEN 
  DO: 
    create output-list. 
    /*DO i = 1 TO 49: 
      output-list.str = output-list.str + " ". 
    END. 
    /*output-list.str = output-list.str + "   T O T A L"*/ 
    output-list.str = output-list.str + "   Sub-Total"
      + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
      + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
    /*Naufal 080520*/
    DO i = 1 TO 29:
        output-list.receiver = output-list.receiver + " ".
    END.
    ASSIGN
        output-list.receiver = output-list.receiver + "Sub-Total"
        output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
        output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
    /*end*/
    create output-list. 
  END. 
  create output-list. 
  /*DO i = 1 TO 49: 
      output-list.str = output-list.str + " ". 
  END. 
  /*output-list.str = output-list.str + "   Sub-Total"
       + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
       + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/ 
  IF tot-flag THEN
    output-list.str = output-list.str + "   T O T A L"
    + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
    + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
  ELSE
    output-list.str = output-list.str + "   Sub-Total"
    + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
    + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). */
  /*Naufal 080520*/
  DO i = 1 TO 29:
      output-list.receiver = output-list.receiver + " ".
  END.
  IF tot-flag THEN
      ASSIGN
          output-list.receiver = output-list.receiver + "T O T A L"
          output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
          output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
  ELSE
      ASSIGN
          output-list.receiver = output-list.receiver + "Sub-Total"
          output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")  
          output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
  /*end*/
  create output-list. 
  create output-list. 
  /*DO i = 1 TO 47: 
      output-list.str = output-list.str + " ". 
  END. 
  output-list.str = output-list.str + "   Grand TOTAL" 
       + STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
       + STRING(ttf-debit, "->,>>>,>>>,>>>,>>9.99"). */
  /*Naufal 080520*/
  DO i = 1 TO 27:
      output-list.receiver = output-list.receiver + " ".
  END.
  ASSIGN
      output-list.receiver = output-list.receiver + "Grand TOTAL"
      output-list.saldo    = STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99")
      output-list.fsaldo   = STRING(ttf-debit, "->,>>>,>>>,>>>,>>9.99").
  /*end*/
END. 

PROCEDURE create-list2: 
DEFINE VARIABLE artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-debit AS DECIMAL. 
DEFINE VARIABLE tot-debit AS DECIMAL. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE receiver AS CHAR FORMAT "x(38)". 
DEFINE VARIABLE saldo AS DECIMAL. 
DEFINE VARIABLE bill-str AS CHAR FORMAT "x(11)". 
DEFINE buffer debt FOR debitor. 
DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-saldo AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-saldo AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-debit AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-debit AS DECIMAL INITIAL 0. 
DEFINE VARIABLE fsaldo AS DECIMAL INITIAL 0.
DEFINE VARIABLE fcurr  AS CHAR FORMAT "x(4)".
  
  FOR EACH output-list: 
    delete output-list. 
  END. 

  FOR EACH edit-list:
      DELETE edit-list.
  END.

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto = 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.verstat NE 9 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr 
    AND guest.name GE from-name AND guest.name LE to-name NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr BY debitor.rgdatum: 
 
    IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
    IF curr-gastnr NE debitor.gastnr THEN 
    DO: 
      curr-gastnr = debitor.gastnr. 
      IF tot-saldo NE 0 AND tot-flag THEN 
      DO: 
        create output-list. 
        /*DO i = 1 TO 49: 
          output-list.str = output-list.str + " ". 
        END. 
        /*output-list.str = output-list.str + "   T O T A L"*/ 
        output-list.str = output-list.str + "   Sub-Total"
          + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
          + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
        /*Naufal 110520 - adjust from str to field*/
        DO i = 1 TO 29:
            output-list.receiver = output-list.receiver + " ".
        END.
        ASSIGN
            output-list.receiver = output-list.receiver + "Sub-Total"
            output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
            output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
        /*end*/
        create output-list. 
        tot-saldo = 0. 
        tf-saldo = 0. 
      END. 
    END. 

    saldo = debitor.saldo. 
    fsaldo = debitor.vesrdep.
    
    IF debitor.counter GT 0 AND lesspay THEN 
    FOR EACH debt WHERE debt.counter = debitor.counter 
      AND debt.opart GE 1 AND debt.zahlkonto GT 0 
      AND debt.rgdatum GE from-date AND debt.rgdatum LE to-date NO-LOCK: 
      saldo = saldo + debt.saldo. 
      fsaldo = fsaldo + debt.vesrdep.
    END. 
    IF (saldo GE -0.05) AND (saldo LE 0.05) THEN saldo = 0. 
    IF saldo NE 0 THEN 
    DO: 
      IF artnr NE artikel.artnr THEN 
      DO: 
        IF artnr NE 0 THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 
          IF tot-saldo NE 0 AND tot-flag THEN 
          DO: 
            create output-list. 
            /*DO i = 1 TO 49: 
              output-list.str = output-list.str + " ". 
            END. 
            /*output-list.str = output-list.str + "   T O T A L"*/ 
            output-list.str = output-list.str + "   Sub-Total"
              + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
              + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
            /*Naufal 110520 - adjust from str to field*/
            DO i = 1 TO 29:
                output-list.receiver = output-list.receiver + " ".
            END.
            ASSIGN
                output-list.receiver = output-list.receiver + "Sub-Total"
                output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
                output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
            /*end*/
            tot-saldo = 0. 
            tf-saldo = 0. 
            create output-list. 
          END. 
          create output-list. 
          /*DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END. 
          /*output-list.str = output-list.str + "   Sub-Total"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/ 
          IF tot-flag THEN
            output-list.str = output-list.str + "   T O T A L"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
          ELSE
            output-list.str = output-list.str + "   Sub-Total"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). */
          /*Naufal 110520 - adjust from str to field*/
          DO i = 1 TO 29:
              output-list.receiver = output-list.receiver + " ".
          END.
          IF tot-flag THEN
          DO:
              ASSIGN
                  output-list.receiver = output-list.receiver + "T O T A L"
                  output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
                  output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
          END.
          ELSE
          DO:
              ASSIGN
                  output-list.receiver = output-list.receiver + "Sub-Total"
                  output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")  
                  output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
          END.
          /*end*/
          create output-list. 
          t-debit = 0. 
          tf-debit = 0. 
          tot-saldo = 0. 
          tf-saldo = 0. 
        END. 
        create output-list. 
        /*DO i = 1 TO 21: 
          output-list.str = output-list.str + " ". 
        END. 
        output-list.str = output-list.str 
          + STRING(artikel.artnr, ">>>>>9") + " - " 
          + STRING(artikel.bezeich, "x(30)"). */
        /*Naufal 110520 - adjust from str to field*/
        output-list.receiver = STRING(artikel.artnr, ">>>>>9") + " - "
                             + STRING(artikel.bezeich, "x(30)").
        /*end*/
        artnr = artikel.artnr. 
      END. 
      receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
        + guest.anrede1. 
      create output-list. 
      ASSIGN 
          output-list.ref-no1 = STRING(guest.firmen-nr)
          output-list.ref-no2 = guest.steuernr
          output-list.ref-no3 = debitor.debref. /*ref no. ar-peyment gerald 100620*/
      /*IF show-inv THEN
      DO:*/
            FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bill THEN
            DO:
                d-rechnr = debitor.rechnr.
            END.
            ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").
      /*END.*/
      IF debitor.verstat = 1 THEN bill-str = 
        "M" + STRING(debitor.rechnr, ">>,>>>,>>9"). 
      ELSE bill-str = STRING(debitor.rechnr, ">>>,>>>,>>9"). 
      /*output-list.str = STRING(debitor.rgdatum) 
        + bill-str 
        + STRING(debitor.zinr, "x(6)") 
        + STRING(receiver, "x(38)") 
        + STRING(saldo, "->,>>>,>>>,>>>,>>9.99").*/ /*sis 020915*/
      /*Naufal 110520*/
      ASSIGN
          output-list.datum     = debitor.rgdatum
          output-list.mflag     = SUBSTR(bill-str,1,1)
          output-list.bill-no   = STRING(debitor.rechnr, ">>>,>>>,>>9")
          output-list.rm-no     = debitor.zinr
          output-list.receiver  = receiver
          output-list.saldo     = STRING(saldo, "->,>>>,>>>,>>>,>>9.99").
      FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
        NO-LOCK NO-ERROR. 
      /*IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(4)"). 
      ELSE output-list.str = output-list.str + "  ". */
      IF AVAILABLE bediener THEN
          output-list.userinit = bediener.userinit.
      ELSE
          output-list.userinit = "  ".
      /*output-list.str = output-list.str + "  " 
        + STRING(fsaldo, "->>>,>>>,>>>,>>9.99"). */
      output-list.fsaldo = STRING(fsaldo, "->,>>>,>>>,>>>,>>9.99").
      /*end*/
      output-list.verstat = debitor.verstat. /* Add by Michael @ 14/08/2019 for add delete journal feature */
      /*DO j = 1 TO 38: 
        IF SUBSTR(debitor.vesrcod,j,1) EQ chr(10) THEN 
          output-list.str = output-list.str + " ". 
        ELSE output-list.str = output-list.str + SUBSTR(debitor.vesrcod,j,1). 
      END. */
      /*Naufal 110520*/
      DO j = 1 TO 38:
          IF SUBSTR(debitor.vesrcod,j,1) EQ CHR(10) THEN
              output-list.vesrcod = " ".
          ELSE
              output-list.vesrcod = output-list.vesrcod + SUBSTR(debitor.vesrcod,j,1).
      END.
      /*end*/
      output-list.ar-recid = RECID(debitor). 
      output-list.info = debitor.vesrcod. 
      IF debitor.versanddat NE ? THEN output-list.maildate = debitor.versanddat. 
 
      IF debitor.betrieb-gastmem NE 0 THEN 
      DO: 
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN 
            output-list.wabkurz = waehrung.wabkurz. 
      END. 
      
      /*M additional column : ci-date, co-date, nights  */
      IF debitor.betriebsnr EQ 0 THEN  /*M from departmen FO */
      DO:
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.resnr GT 0
              AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
              IF bill.reslinnr EQ 0 THEN  /*M master bill */
              DO:
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.resstatus = 8 NO-LOCK NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9")
                          .
                  END.  
              END.
              ELSE
              DO: 
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9")
                          .
                  END.  
              END.
          END.
          ELSE DO:   /*ITA*/
              DEFINE VARIABLE resnr AS INTEGER NO-UNDO.
              IF debitor.vesrcod NE " " AND debitor.vesrcod MATCHES "*Deposit Payment*" THEN DO:
                    ASSIGN resnr = INTEGER(ENTRY(2, ENTRY(1,debitor.vesrcod, ";"), ":")).
                    FIND FIRST res-line WHERE res-line.resnr = resnr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                             ASSIGN  
                              output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9").
                    END.
              END.
          END.
      END.

      CREATE edit-list.
      ASSIGN 
          edit-list.rechnr   = debitor.rechnr
          edit-list.ar-recid = RECID(debitor)
          edit-list.datum    = debitor.rgdatum
          edit-list.zinr     = debitor.zinr
          edit-list.billname = receiver
          edit-list.famt     = debitor.vesrdep
          edit-list.fcurr    = output-list.wabkurz
          edit-list.curr-nr  = debitor.betrieb-gastmem.
      
 
      t-debit = t-debit + saldo. 
      tot-debit = tot-debit + saldo. 
      tot-saldo = tot-saldo + saldo. 
      tf-debit = tf-debit + fsaldo. 
      ttf-debit = ttf-debit + fsaldo. 
      tf-saldo = tf-saldo + fsaldo. 
    END. 
  END. 
 
  IF tot-saldo NE 0 AND tot-flag THEN 
  DO: 
    create output-list. 
    /*DO i = 1 TO 49: 
      output-list.str = output-list.str + " ". 
    END. 
    /*output-list.str = output-list.str + "   T O T A L"*/ 
    output-list.str = output-list.str + "   Sub-Total"
      + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
      + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
    /*Naufal 110520*/
    DO i = 1 TO 29:
        output-list.receiver = output-list.receiver + " ".
    END.
    ASSIGN
        output-list.receiver = output-list.receiver + "Sub-Total"
        output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
        output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
    /*end*/
    create output-list. 
  END. 
  create output-list. 
  /*DO i = 1 TO 49: 
      output-list.str = output-list.str + " ". 
  END. 
  /*output-list.str = output-list.str + "   Sub-Total"
       + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
       + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/ 
  IF tot-flag THEN
    output-list.str = output-list.str + "   T O T A L"
    + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
    + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
  ELSE
    output-list.str = output-list.str + "   Sub-Total"
    + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
    + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). */
  /*Naufal 110520*/
  DO i = 1 TO 29:
      output-list.receiver = output-list.receiver + " ".
  END.
  IF tot-flag THEN
      ASSIGN
          output-list.receiver = output-list.receiver + "T O T A L"
          output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
          output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
  ELSE
      ASSIGN
          output-list.receiver = output-list.receiver + "Sub-Total"
          output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
          output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
  /*end*/
  create output-list. 
  create output-list. 
  /*DO i = 1 TO 47: 
      output-list.str = output-list.str + " ". 
  END. 
  output-list.str = output-list.str + "   Grand TOTAL" 
       + STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
       + STRING(ttf-debit, "->,>>>,>>>,>>>,>>9.99"). */
  /*Naufal 110520*/
  DO i = 1 TO 27:
      output-list.receiver = output-list.receiver + " ".
  END.
  ASSIGN
      output-list.receiver = output-list.receiver + "Grand TOTAL"
      output-list.saldo    = STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99")
      output-list.fsaldo   = STRING(ttf-debit, "->,>>>,>>>,>>>,>>9.99").
  /*end*/
END. 
 
PROCEDURE create-list2A: 
DEFINE VARIABLE artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-debit AS DECIMAL. 
DEFINE VARIABLE tot-debit AS DECIMAL. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE receiver AS CHAR FORMAT "x(38)". 
DEFINE VARIABLE saldo AS DECIMAL. 
DEFINE VARIABLE bill-str AS CHAR FORMAT "x(11)". 
DEFINE buffer debt FOR debitor. 
DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-saldo AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-saldo AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-debit AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-debit AS DECIMAL INITIAL 0. 
DEFINE VARIABLE fsaldo AS DECIMAL INITIAL 0.
  
  FOR EACH output-list: 
    delete output-list. 
  END. 

  FOR EACH debitor WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND debitor.zahlkonto = 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.verstat NE 9 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr 
    AND guest.name GE from-name NO-LOCK 
    BY artikel.artnr BY debitor.name BY debitor.gastnr BY debitor.rgdatum: 
 
    IF curr-gastnr = 0 THEN curr-gastnr = debitor.gastnr. 
    IF curr-gastnr NE debitor.gastnr THEN 
    DO: 
      curr-gastnr = debitor.gastnr. 
      IF tot-saldo NE 0 AND tot-flag THEN 
      DO: 
        create output-list. 
        /*DO i = 1 TO 49: 
          output-list.str = output-list.str + " ". 
        END. 
        /*output-list.str = output-list.str + "   T O T A L"*/ 
        output-list.str = output-list.str + "   Sub-Total"
          + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
          + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
        /*Naufal 110520 - adjust from str to field*/
        DO i = 1 TO 29:
            output-list.receiver = output-list.receiver + " ".
        END.
        ASSIGN
            output-list.receiver = output-list.receiver + "Sub-Total"
            output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
            output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
        /*end*/
        create output-list. 
        tot-saldo = 0. 
        tf-saldo = 0. 
      END. 
    END. 
    saldo = debitor.saldo. 
    fsaldo = debitor.vesrdep .
    IF debitor.counter GT 0 AND lesspay THEN 
    FOR EACH debt WHERE debt.counter = debitor.counter 
      AND debt.opart GE 1 AND debt.zahlkonto GT 0 
      AND debt.rgdatum GE from-date AND debt.rgdatum LE to-date NO-LOCK: 
      saldo = saldo + debt.saldo. 
      fsaldo = fsaldo + debt.vesrdep.
    END. 
    IF (saldo GE -0.05) AND (saldo LE 0.05) THEN saldo = 0. 
 
    IF saldo NE 0 THEN 
    DO: 
      IF artnr NE artikel.artnr THEN 
      DO: 
        IF artnr NE 0 THEN 
        DO: 
          curr-gastnr = debitor.gastnr. 
          IF tot-saldo NE 0 AND tot-flag THEN 
          DO: 
            create output-list. 
            /*DO i = 1 TO 49: 
              output-list.str = output-list.str + " ". 
            END. 
            /*output-list.str = output-list.str + "   T O T A L"*/ 
            output-list.str = output-list.str + "   Sub-Total"
              + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
              + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
            /*Naufal 110520 - adjust from str to field*/
            DO i = 1 TO 29:
                output-list.receiver = output-list.receiver + " ".
            END.
            ASSIGN
                output-list.receiver = output-list.receiver + "Sub-Total"
                output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") 
                output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99"). 
            /*end*/
            tot-saldo = 0. 
            tf-saldo = 0. 
            create output-list. 
          END. 
          create output-list. 
          /*DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END. 
          /*output-list.str = output-list.str + "   Sub-Total" 
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/ 
          IF tot-flag THEN
            output-list.str = output-list.str + "   T O T A L"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
          ELSE
            output-list.str = output-list.str + "   Sub-Total"
            + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
            + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). */
          /*Naufal 110520 - adjust from str to field*/
          DO i = 1 TO 29:
              output-list.receiver = output-list.receiver + " ".
          END.
          IF tot-flag THEN
          DO:
              ASSIGN
                  output-list.receiver = output-list.receiver + "T O T A L"
                  output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
                  output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
          END.
          ELSE
          DO:
              ASSIGN
                  output-list.receiver = output-list.receiver + "Sub-Total"
                  output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")  
                  output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
          END.
          /*end*/
          create output-list. 
          t-debit = 0. 
          tf-debit = 0. 
          tot-saldo = 0. 
          tf-saldo = 0. 
        END. 
        create output-list. 
        /*DO i = 1 TO 21: 
          output-list.str = output-list.str + " ". 
        END. 
        output-list.str = output-list.str 
          + STRING(artikel.artnr, ">>>>>9") + " - " 
          + STRING(artikel.bezeich, "x(30)"). */
        /*Naufal 110520 - adjust from str to field*/
        output-list.receiver = STRING(artikel.artnr, ">>>>>9") + " - "
                             + STRING(artikel.bezeich, "x(30)").
        /*end*/
        artnr = artikel.artnr. 
      END. 
      receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma 
        + guest.anrede1. 
      create output-list. 
      ASSIGN 
          output-list.ref-no1 = STRING(guest.firmen-nr)
          output-list.ref-no2 = guest.steuernr
          output-list.ref-no3 = debitor.debref. /*ref no. ar-peyment gerald 100620*/
      /*IF show-inv THEN
        DO:*/
            FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bill THEN
            DO:
                d-rechnr = debitor.rechnr.
            END.
            ELSE output-list.inv-no = STRING(bill.rechnr2, ">>>>>>>>>").
        /*END.*/
      IF debitor.verstat = 1 THEN bill-str = 
        "M" + STRING(debitor.rechnr, ">>,>>>,>>9"). 
      ELSE bill-str = STRING(debitor.rechnr, ">>>,>>>,>>9"). 
      /*output-list.str = STRING(debitor.rgdatum) 
        + bill-str 
        + STRING(debitor.zinr, "x(6)") 
        + STRING(receiver, "x(38)") 
        + STRING(saldo, "->,>>>,>>>,>>>,>>9.99"). */ /*sis 020915*/
      /*Naufal 110520*/
      ASSIGN
          output-list.datum     = debitor.rgdatum
          output-list.mflag     = SUBSTR(bill-str,1,1)
          output-list.bill-no   = STRING(debitor.rechnr, ">>>,>>>,>>9")
          output-list.rm-no     = debitor.zinr
          output-list.receiver  = receiver
          output-list.saldo     = STRING(saldo, "->,>>>,>>>,>>>,>>9.99").
      FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
        NO-LOCK NO-ERROR. 
      /*IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit, "x(4)"). 
      ELSE output-list.str = output-list.str + "  ". */
      IF AVAILABLE bediener THEN
          output-list.userinit = bediener.userinit.
      ELSE
          output-list.userinit = "  ".
      /*output-list.str = output-list.str 
        + STRING(fsaldo, "->>>,>>>,>>>,>>9.99"). */
      output-list.fsaldo = STRING(fsaldo, "->,>>>,>>>,>>>,>>9.99").
      /*end*/
      output-list.verstat = debitor.verstat. /* Add by Michael @ 14/08/2019 for add delete journal feature */
      /*DO j = 1 TO 38: 
        IF SUBSTR(debitor.vesrcod,j,1) EQ chr(10) THEN 
          output-list.str = output-list.str + " ". 
        ELSE output-list.str = output-list.str + SUBSTR(debitor.vesrcod,j,1). 
      END. */
      /*Naufal 110520*/
      DO j = 1 TO 38:
          IF SUBSTR(debitor.vesrcod,j,1) EQ CHR(10) THEN
              output-list.vesrcod = " ".
          ELSE
              output-list.vesrcod = output-list.vesrcod + SUBSTR(debitor.vesrcod,j,1).
      END.
      /*end*/
      output-list.ar-recid = RECID(debitor). 
      output-list.info = debitor.vesrcod. 
      IF debitor.versanddat NE ? THEN output-list.maildate = debitor.versanddat. 
 
      IF debitor.betrieb-gastmem NE 0 THEN 
      DO: 
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN output-list.wabkurz = waehrung.wabkurz. 
      END. 

      /*M additional column : ci-date, co-date, nights  */
      IF debitor.betriebsnr EQ 0 THEN  /*M from departmen FO */
      DO:
          FIND FIRST bill WHERE bill.rechnr = debitor.rechnr AND bill.resnr GT 0
              AND bill.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE bill THEN
          DO:
              IF bill.reslinnr EQ 0 THEN  /*M master bill */
              DO:
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.resstatus = 8 NO-LOCK NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9")
                          .
                  END.  
              END.
              ELSE
              DO:
                  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                      AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
                  IF AVAILABLE res-line THEN
                  DO:
                      ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9")
                          .
                  END.  
              END.
          END.
          ELSE DO: /*ITA*/
              DEFINE VARIABLE resnr AS INTEGER NO-UNDO.
              IF debitor.vesrcod NE " " AND debitor.vesrcod MATCHES "*Deposit Payment*" THEN DO:
                    ASSIGN resnr = INTEGER(ENTRY(2, ENTRY(1,debitor.vesrcod, ";"), ":")).
                    FIND FIRST res-line WHERE res-line.resnr = resnr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                             ASSIGN  output-list.ci-date = res-line.ankunft
                              output-list.co-date = res-line.abreise
                              output-list.nights  = STRING(INT(res-line.abreise - res-line.ankunft), ">>9").
                    END.
              END.          
          END.
      END.

      CREATE edit-list.
      ASSIGN 
          edit-list.rechnr   = debitor.rechnr
          edit-list.ar-recid = RECID(debitor)
          edit-list.datum    = debitor.rgdatum
          edit-list.zinr     = debitor.zinr
          edit-list.billname = receiver
          edit-list.famt     = debitor.vesrdep
          edit-list.fcurr    = output-list.wabkurz
          edit-list.curr-nr  = debitor.betrieb-gastmem.
      
 
      t-debit = t-debit + saldo. 
      tot-debit = tot-debit + saldo. 
      tot-saldo = tot-saldo + saldo. 
      tf-debit = tf-debit + fsaldo. 
      ttf-debit = ttf-debit + fsaldo. 
      tf-saldo = tf-saldo + fsaldo. 
    END. 
  END. 
 
  IF tot-saldo NE 0 AND tot-flag THEN 
  DO: 
    create output-list. 
    /*DO i = 1 TO 49: 
      output-list.str = output-list.str + " ". 
    END. 
    /*output-list.str = output-list.str + "   T O T A L"*/
    output-list.str = output-list.str + "   Sub-Total"
      + STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99") + "  " /*sis 020915*/
      + STRING(tf-saldo, "->>>,>>>,>>>,>>9.99"). */
    /*Naufal 110520*/
    DO i = 1 TO 29:
        output-list.receiver = output-list.receiver + " ".
    END.
    ASSIGN
        output-list.receiver = output-list.receiver + "Sub-Total"
        output-list.saldo    = STRING(tot-saldo, "->,>>>,>>>,>>>,>>9.99")
        output-list.fsaldo   = STRING(tf-saldo, "->,>>>,>>>,>>>,>>9.99").
    /*end*/
    create output-list. 
  END. 
  create output-list. 
  /*DO i = 1 TO 49: 
      output-list.str = output-list.str + " ". 
  END. 
  /*output-list.str = output-list.str + "   Sub-Total" 
       + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
       + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").*/ 
  IF tot-flag THEN
    output-list.str = output-list.str + "   T O T A L"
    + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
    + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). 
  ELSE
    output-list.str = output-list.str + "   Sub-Total"
    + STRING(t-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
    + STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99"). */
  /*Naufal 110520*/
  DO i = 1 TO 29:
      output-list.receiver = output-list.receiver + " ".
  END.
  IF tot-flag THEN
      ASSIGN
          output-list.receiver = output-list.receiver + "T O T A L"
          output-list.saldo    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")
          output-list.fsaldo   = STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
  ELSE
      ASSIGN
          output-list.receiver = output-list.receiver + "Sub-Total"
          output-list.saldo    =STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")  
          output-list.fsaldo   =STRING(tf-debit, "->,>>>,>>>,>>>,>>9.99").
  /*end*/
  create output-list. 
  create output-list. 
  /*DO i = 1 TO 47: 
      output-list.str = output-list.str + " ". 
  END. 
  output-list.str = output-list.str + "   Grand TOTAL" 
       + STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99") + "  " 
       + STRING(ttf-debit, "->,>>>,>>>,>>>,>>9.99").*/
  /*Naufal 110520*/
  DO i = 1 TO 27:
      output-list.receiver = output-list.receiver + " ".
  END.
  ASSIGN
      output-list.receiver = output-list.receiver + "Grand TOTAL"
      output-list.saldo    = STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99")
      output-list.fsaldo   = STRING(ttf-debit, "->,>>>,>>>,>>>,>>9.99").
  /*end*/
END. 

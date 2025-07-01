/*Eko 1 Januari 2015 Penambahan sorting by subGroup ** JIKA DATA TIDAK MUNCUL, PASTIKAN BL SUDAH TERUPDATE YANG PALING TERAKHIR ****/
/*MCH Oct 31, 2024 => Ticket 956248 - Add Cost Center and Unit*/
/*MCH Nov 18, 2024 => Ticket BF65B1 - Add GL Department*/

DEFINE TEMP-TABLE str-list 
  FIELD billdate AS DATE 
  FIELD fibu AS CHAR 
  FIELD other-fibu AS LOGICAL 
  FIELD op-recid AS INTEGER 
  FIELD lscheinnr AS CHAR 
  FIELD s AS CHAR FORMAT "x(153)"
  FIELD ID AS CHAR FORMAT "x(4)"
  FIELD masseinheit AS CHAR FORMAT "x(3)"
  FIELD gldept AS CHAR
  FIELD amount      AS DECIMAL
  FIELD avrg-price  AS DECIMAL

  /* Oscar (12/02/25) - DDB12D - show remark in outgoing report */
  FIELD remark-artikel AS CHARACTER.

DEFINE WORKFILE s-list 
  FIELD fibu AS CHAR 
  FIELD cost-center AS CHAR FORMAT "x(24)" 
  FIELD bezeich AS CHAR 
  FIELD cost AS DECIMAL
  FIELD subgroup AS CHARACTER
  FIELD anzahl AS DECIMAL. 

DEF INPUT PARAMETER trans-code AS CHAR.
DEF INPUT PARAMETER from-grp   AS INT.
DEF INPUT PARAMETER mi-alloc   AS LOGICAL.
DEF INPUT PARAMETER mi-article AS LOGICAL.
DEF INPUT PARAMETER mi-docu    AS LOGICAL.
DEF INPUT PARAMETER mi-date    AS LOGICAL.
DEF INPUT PARAMETER mattype     AS INT.

DEF INPUT PARAMETER from-lager AS INT.
DEF INPUT PARAMETER to-lager AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER from-art AS INT.
DEF INPUT PARAMETER to-art AS INT.
DEF INPUT PARAMETER show-price AS LOGICAL.
DEF INPUT PARAMETER cost-acct AS CHAR.
DEF INPUT PARAMETER deptNo AS INT.

DEF OUTPUT PARAMETER it-exist AS LOGICAL.
DEF OUTPUT PARAMETER tot-anz AS DECIMAL. 
DEF OUTPUT PARAMETER tot-amount AS DECIMAL. 
DEF OUTPUT PARAMETER TABLE FOR str-list.

DEFINE VARIABLE preis       AS DECIMAL INITIAL 0.
DEFINE VARIABLE wert        AS DECIMAL INITIAL 0.
DEFINE VARIABLE i AS INT.
DEFINE VARIABLE do-it AS LOGICAL.

DEF VAR mi-subgroup AS LOGICAL INITIAL NO NO-UNDO.

/*Eko*/
IF NUM-ENTRIES(trans-code,";") GT 1 THEN DO:
    mi-subgroup = LOGICAL(ENTRY(2,trans-code,";")).
    trans-code = ENTRY(1,trans-code,";").
END.
trans-code = REPLACE(trans-code,";","").
/*End Eko*/

IF trans-code NE "" THEN RUN create-list-trans.
ELSE
DO:
  IF from-grp = 0 THEN 
  DO: 
    IF mi-alloc = YES THEN RUN create-list. 
    ELSE IF mi-article = YES 
      THEN RUN create-listA. 
    ELSE IF mi-docu = YES 
      THEN RUN create-listB. 
    ELSE IF mi-date = YES 
      THEN RUN create-listC.
    ELSE IF mi-subgroup = YES /*Eko*/
      THEN RUN create-listD.
  END. 
  ELSE 
  DO: 
    IF mi-alloc = YES THEN RUN create-list1. 
    ELSE IF mi-article = YES 
      THEN RUN create-list1A. 
    ELSE IF mi-docu = YES 
      THEN RUN create-list1B. 
    ELSE IF mi-date = YES 
      THEN RUN create-list1C. 
    ELSE IF mi-date = YES  /*Eko*/
      THEN RUN create-list1D. 
  END. 
END.


PROCEDURE create-list-trans: 
  DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
  DEFINE VARIABLE t-val AS DECIMAL. 
  DEFINE VARIABLE lschein AS CHAR INITIAL "". 
  DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(24)". 
  DEFINE VARIABLE fibukonto AS CHAR. 
  DEFINE VARIABLE do-it AS LOGICAL. 
  DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
  DEFINE VARIABLE other-fibu AS LOGICAL. 
  DEFINE buffer gl-acct1 FOR gl-acct. 
  DEFINE VARIABLE create-it AS LOGICAL. 
  DEFINE VARIABLE curr-fibu AS CHAR INITIAL "". 

  status default "Processing...". 
 
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
  
  tot-anz = 0. 
  tot-amount = 0. 
  do-it = YES. 

  FOR EACH l-lager NO-LOCK:  
    t-anz = 0.

    /* Oscar (18/12/2024) - 989732 - fix some article seperated */
    CREATE str-list. 
    str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
    
    CREATE str-list.

    curr-fibu = "".
    
    /*  calculate the outgoing stocks within the given periods */ 
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.anzahl NE 0 AND l-op.op-art = 3 
      AND l-op.lscheinnr = trans-code
      AND l-op.loeschflag LE 1  NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
      AND l-ophdr.lscheinnr = l-op.lscheinnr 
      AND l-ophdr.fibukonto NE "" NO-LOCK, 
      FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund NO-LOCK,
      FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK 
      BY l-op.stornogrund BY l-ophdr.fibukonto /*BY l-artikel.bezeich*/ 
      BY l-op.datum BY l-op.artnr: 
 
        IF show-price THEN 
        DO: 
          preis = l-op.einzelpreis. 
          wert = l-op.warenwert. 
        END. 
  
        it-exist = YES. 
        other-fibu = NO. 
        IF l-op.stornogrund NE "" THEN 
        DO: 
          FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
        END. 
        IF other-fibu THEN 
          RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
        ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
  
        IF lschein = "" THEN lschein = l-op.lscheinnr. 
  
        IF other-fibu THEN 
        DO: 
          fibukonto = gl-acct1.fibukonto. 
          cost-bezeich = gl-acct1.bezeich. 
          IF cost-acct = "" THEN create-it = YES. 
          ELSE create-it = (cost-acct = fibukonto). 
        END. 
        ELSE 
        DO: 
          fibukonto = gl-acct.fibukonto. 
          cost-bezeich = gl-acct.bezeich. 
          IF cost-acct = "" THEN create-it = YES. 
          ELSE create-it = (cost-acct = fibukonto). 
        END. 
  
        IF create-it AND deptNo NE 0 THEN
        DO:
          FIND FIRST parameters NO-LOCK WHERE 
            parameters.progname = "CostCenter"  AND
            parameters.section = "alloc"        AND
            parameters.varname = STRING(deptNo) AND
            parameters.vstring = fibukonto NO-ERROR.
          create-it = AVAILABLE parameters.
        END.

        /* Oscar (18/12/2024) - 989732 - fix some article seperated */
        /* IF curr-fibu = "" THEN curr-fibu = fibukonto. 
        IF curr-fibu NE fibukonto AND t-anz NE 0 THEN 
        /* IF (lschein NE l-op.lscheinnr) AND t-anz NE 0 THEN */ 
        DO: 
          create str-list. 
          DO i = 1 TO 45: 
            str-list.s = str-list.s + " ". 
          END. 
          str-list.s = str-list.s + "Subtotal ". 
          DO i = 1 TO 41: /*ragung*/
            str-list.s = str-list.s + " ". 
          END. 
          str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
          DO i = 1 TO 14: 
            str-list.s = str-list.s + " ". 
          END. 
          /*MTIF NOT long-digit THEN*/
          str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
          /*MTELSE 
          str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
          t-anz = 0. 
          t-val = 0. 
          create str-list. 
          lschein = l-op.lscheinnr. 
          curr-fibu = fibukonto. 
        END.*/
  
        /* IF do-it THEN 
        DO: 
          create str-list. 
          str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
          create str-list. 
          do-it = NO. 
        END. */ 
  
        IF create-it THEN 
        DO: 
          /* Oscar (18/12/2024) - 989732 - fix some article seperated */
          IF curr-fibu = "" THEN curr-fibu = fibukonto. 
          IF curr-fibu NE fibukonto AND t-anz NE 0 THEN 
          /* IF (lschein NE l-op.lscheinnr) AND t-anz NE 0 THEN */ 
          DO: 
            CREATE str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 

            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 41: /*ragung*/   
              str-list.s = str-list.s + " ". 
            END.

            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 14: 
              str-list.s = str-list.s + " ". 
            END. 

            /*MTIF NOT long-digit THEN */
            /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
            str-list.amount = t-val.
            str-list.avrg-price = 0. 
            /*MTELSE 
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
            t-anz = 0. 
            t-val = 0. 

            CREATE str-list. 
            lschein = l-op.lscheinnr. 
            curr-fibu = fibukonto.
          END.

          FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.fibu = fibukonto. 
            s-list.bezeich = cost-bezeich.

            IF cc-code NE 0 THEN 
              s-list.bezeich = STRING(cc-code,"9999 ") + s-list.bezeich. 
          END. 

          s-list.cost = s-list.cost + wert.
          s-list.anzahl = s-list.anzahl + l-op.anzahl.
          t-anz = t-anz + l-op.anzahl. 
          t-val = t-val + wert. 
          tot-anz = tot-anz + l-op.anzahl. 
          tot-amount = tot-amount + wert. 

          CREATE str-list. 
          RUN add-id.

          str-list.lscheinnr = l-op.lscheinnr. 
          str-list.fibu = fibukonto. 
          str-list.other-fibu = other-fibu. 
          str-list.op-recid = RECID(l-op). 
          str-list.masseinheit = l-artikel.masseinheit.
          str-list.gldept = STRING(gl-department.nr) + " - " + gl-department.bezeich.

          /* Oscar (12/02/25) - DDB12D - show remark in outgoing report */
          FIND FIRST queasy WHERE queasy.KEY EQ 340 
            AND queasy.char1 EQ l-op.lscheinnr
            AND queasy.number1 EQ l-op.artnr
            AND queasy.deci1 EQ l-op.einzelpreis NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
            str-list.remark-artikel = queasy.char2.
          END.
          ELSE
          DO:
            str-list.remark-artikel = "".
          END.

          /*MTIF NOT long-digit THEN*/
          str-list.s = STRING(l-op.datum) 
                  + STRING(s-list.bezeich, "x(30)") 
                  + STRING(l-artikel.artnr, "9999999") 
                  + STRING(l-artikel.bezeich, "x(50)") 
                  + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                  /* + STRING(preis, ">>>,>>>,>>9.99") 
                  + STRING(wert, "->,>>>,>>>,>>9.99")  */
                  + STRING(l-op.lscheinnr, "x(12)"). 
          /*MTELSE str-list.s = STRING(l-op.datum) 
                  + STRING(s-list.bezeich, "x(30)") 
                  + STRING(l-artikel.artnr, "9999999") 
                  + STRING(l-artikel.bezeich, "x(32)") 
                  + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                  + STRING(preis, ">>>>,>>>,>>9") 
                  + STRING(wert, "->,>>>,>>>,>>9") 
                  + STRING(l-op.lscheinnr, "x(12)").*/
          str-list.billdate = l-op.datum.
          str-list.avrg-price = preis.
          str-list.amount = wert.
        END. 
    END. 

    IF t-anz NE 0 THEN 
    DO: 
      CREATE str-list. 
      DO i = 1 TO 45: 
        str-list.s = str-list.s + " ". 
      END. 

      str-list.s = str-list.s + "Subtotal ". 
      DO i = 1 TO 41: /*ragung*/
        str-list.s = str-list.s + " ". 
      END. 

      str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
      DO i = 1 TO 14: 
        str-list.s = str-list.s + " ". 
      END. 
      
      /*MTIF NOT long-digit THEN*/
      /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */ 
      str-list.amount = t-val.
      str-list.avrg-price = 0.
      /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
      t-anz = 0. 
      t-val = 0.

      CREATE str-list. 
    END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 41: /*ragung*/
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    
    /*MTIF NOT long-digit THEN*/
    /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */ 
    str-list.amount = t-val.
    str-list.avrg-price = 0.
    /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
    CREATE str-list. 
  END.  
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 14: 
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */ 
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  str-list.s = STRING("","x(8)") + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  tot-anz = 0.

  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    /*MTIF NOT long-digit THEN*/
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(50)") 
      + STRING(s-list.anzahl, "->>>>>>>>>>>>>").
      /* + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). */ 
    /*MTELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9").*/
    str-list.amount = s-list.cost.
    str-list.avrg-price = 0.

    tot-amount = tot-amount + s-list.cost. 
    tot-anz = tot-anz + s-list.anzahl.
  END. 

  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->>>>>>>>>>>>>").
  DO i = 1 TO 12:
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
END. 
 
PROCEDURE create-list: 
  DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
  DEFINE VARIABLE t-val AS DECIMAL. 
  DEFINE VARIABLE lschein AS CHAR INITIAL "". 
  DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(24)". 
  DEFINE VARIABLE fibukonto AS CHAR. 
  DEFINE VARIABLE do-it AS LOGICAL. 
  DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
  DEFINE VARIABLE other-fibu AS LOGICAL. 
  DEFINE buffer gl-acct1 FOR gl-acct. 
  DEFINE VARIABLE create-it AS LOGICAL. 
  DEFINE VARIABLE curr-fibu AS CHAR INITIAL "". 
  
  status default "Processing...". 
  
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  do-it = YES. 
  
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
      
      t-anz = 0.

      /* Oscar (18/12/2024) - 989732 - fix some article seperated */
      CREATE str-list. 
      str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
      
      CREATE str-list.

      curr-fibu = "".

      /*  calculate the outgoing stocks within the given periods */ 
      FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.anzahl NE 0 AND l-op.op-art = 3 
        AND l-op.loeschflag LE 1  NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
        AND l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund NO-LOCK, 
        FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK 
        BY l-op.stornogrund BY l-ophdr.fibukonto /*BY l-artikel.bezeich*/ 
        BY l-op.datum BY l-op.artnr: 
  
          IF show-price THEN 
          DO: 
            preis = l-op.einzelpreis. 
            wert = l-op.warenwert. 
          END. 
    
          it-exist = YES. 
          other-fibu = NO. 
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
    
          IF lschein = "" THEN lschein = l-op.lscheinnr. 
    
          IF other-fibu THEN 
          DO: 
            fibukonto = gl-acct1.fibukonto. 
            cost-bezeich = gl-acct1.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
          ELSE 
          DO: 
            fibukonto = gl-acct.fibukonto. 
            cost-bezeich = gl-acct.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
    
          IF create-it AND deptNo NE 0 THEN
          DO:
            FIND FIRST parameters NO-LOCK WHERE 
              parameters.progname = "CostCenter"  AND
              parameters.section = "alloc"        AND
              parameters.varname = STRING(deptNo) AND
              parameters.vstring = fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.

          /* Oscar (18/12/2024) - 989732 - fix some article seperated */
          /* IF curr-fibu = "" THEN curr-fibu = fibukonto. 
          IF curr-fibu NE fibukonto AND t-anz NE 0 THEN 
          /* IF (lschein NE l-op.lscheinnr) AND t-anz NE 0 THEN */ 
          DO: 
            create str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 41: /*ragung*/
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 14: 
              str-list.s = str-list.s + " ". 
            END. 
            /*MTIF NOT long-digit THEN */
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            /*MTELSE 
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
            t-anz = 0. 
            t-val = 0. 
            create str-list. 
            lschein = l-op.lscheinnr. 
            curr-fibu = fibukonto. 
          END. */
    
          /* IF do-it THEN 
          DO:  
            create str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
            create str-list. 
            do-it = NO. 
          END.  */
    
          IF create-it THEN 
          DO: 
            /* Oscar (18/12/2024) - 989732 - fix some article seperated */
            IF curr-fibu = "" THEN curr-fibu = fibukonto. 
            IF curr-fibu NE fibukonto AND t-anz NE 0 THEN 
            /* IF (lschein NE l-op.lscheinnr) AND t-anz NE 0 THEN */ 
            DO: 
              CREATE str-list. 
              DO i = 1 TO 45: 
                str-list.s = str-list.s + " ". 
              END. 

              str-list.s = str-list.s + "Subtotal ". 
              DO i = 1 TO 41: /*ragung*/   
                str-list.s = str-list.s + " ". 
              END.

              str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
              DO i = 1 TO 14: 
                str-list.s = str-list.s + " ". 
              END. 

              /*MTIF NOT long-digit THEN */
              /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
              str-list.amount = t-val.
              str-list.avrg-price = 0. 
              /*MTELSE 
              str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
              t-anz = 0. 
              t-val = 0. 

              CREATE str-list. 
              lschein = l-op.lscheinnr. 
              curr-fibu = fibukonto. 
            END.
            
            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich.

              IF cc-code NE 0 THEN 
                s-list.bezeich = STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 

            s-list.cost = s-list.cost + wert.
            s-list.anzahl = s-list.anzahl + l-op.anzahl.
            t-anz = t-anz + l-op.anzahl. 
            t-val = t-val + wert. 
            tot-anz = tot-anz + l-op.anzahl. 
            tot-amount = tot-amount + wert. 

            CREATE str-list. 
            RUN add-id.

            str-list.lscheinnr = l-op.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            str-list.masseinheit = l-artikel.masseinheit.
            str-list.gldept = STRING(gl-department.nr) + " - " + gl-department.bezeich.

            /* Oscar (12/02/25) - DDB12D - show remark in outgoing report */
            FIND FIRST queasy WHERE queasy.KEY EQ 340 
              AND queasy.char1 EQ l-op.lscheinnr
              AND queasy.number1 EQ l-op.artnr
              AND queasy.deci1 EQ l-op.einzelpreis NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
              str-list.remark-artikel = queasy.char2.
            END.
            ELSE
            DO:
              str-list.remark-artikel = "".
            END.
            
            /*MTIF NOT long-digit THEN*/
            str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(50)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    /* + STRING(preis, ">>>,>>>,>>9.99") 
                    + STRING(wert, "->,>>>,>>>,>>9.99")  */
                    + STRING(l-op.lscheinnr, "x(12)"). 
            /*MTELSE str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(32)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    + STRING(preis, ">>>>,>>>,>>9") 
                    + STRING(wert, "->,>>>,>>>,>>9") 
                    + STRING(l-op.lscheinnr, "x(12)").*/
            str-list.billdate = l-op.datum.
            str-list.avrg-price = preis.
            str-list.amount = wert.
          END. 
      END. 

      IF t-anz NE 0 THEN 
      DO: 
        CREATE str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 

        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 41: /*ragung*/   
          str-list.s = str-list.s + " ". 
        END.

        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 

        /*MTIF NOT long-digit THEN */
        /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
        str-list.amount = t-val.
        str-list.avrg-price = 0. 
        /*MTELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
        t-anz = 0. 
        t-val = 0. 

        CREATE str-list.
      END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 41: /*ragung*/
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    
    /*MTIF NOT long-digit THEN*/
    /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */ 
    str-list.amount = t-val.
    str-list.avrg-price = 0.
    /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 14: 
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */ 
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  str-list.s = STRING("","x(8)") + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  tot-anz = 0.

  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    /*MTIF NOT long-digit THEN*/
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(50)") 
      + STRING(s-list.anzahl, "->>>>>>>>>>>>>").
      /* + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). */ 
    /*MTELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9").*/
    str-list.amount = s-list.cost.
    str-list.avrg-price = 0.

    tot-amount = tot-amount + s-list.cost. 
    tot-anz = tot-anz + s-list.anzahl.
  END. 

  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->>>>>>>>>>>>>").
  DO i = 1 TO 12:
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
END. 
 
PROCEDURE create-list1: 
  DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
  DEFINE VARIABLE t-val AS DECIMAL. 
  DEFINE VARIABLE lschein AS CHAR INITIAL "". 
  DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(30)". 
  DEFINE VARIABLE fibukonto AS CHAR. 
  DEFINE VARIABLE do-it AS LOGICAL. 
  DEFINE VARIABLE create-it AS LOGICAL. 
  DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
  DEFINE VARIABLE other-fibu AS LOGICAL. 
  DEFINE VARIABLE grp1 AS INTEGER INITIAL 0. 
  DEFINE VARIABLE grp2 AS INTEGER INITIAL 1. 
  DEFINE VARIABLE curr-fibu AS CHAR INITIAL "". 
  DEFINE buffer gl-acct1 FOR gl-acct. 
  
  status default "Processing...". 
 
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  do-it = YES.

  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 

      t-anz = 0.

      /* Oscar (18/12/2024) - 989732 - fix some article seperated */
      CREATE str-list. 
      str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
      
      CREATE str-list.

      curr-fibu = "".
      
      /*  calculate the outgoing stocks within the given periods */ 
      FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.anzahl NE 0 AND l-op.op-art = 3 
        AND l-op.loeschflag LE 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
        AND l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund NO-LOCK, 
        FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum EQ from-grp NO-LOCK, 
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
        AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
        NO-LOCK BY l-op.stornogrund BY l-ophdr.fibukonto 
        BY l-op.datum /*BY l-artikel.bezeich*/ BY l-op.artnr: 
  
          IF show-price THEN 
          DO: 
            preis = l-op.einzelpreis. 
            wert = l-op.warenwert. 
          END. 
    
          it-exist = YES. 
          other-fibu = NO. 
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
    
          IF lschein = "" THEN lschein = l-op.lscheinnr. 
    
          IF other-fibu THEN 
          DO: 
            fibukonto = gl-acct1.fibukonto. 
            cost-bezeich = gl-acct1.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
          ELSE 
          DO: 
            fibukonto = gl-acct.fibukonto. 
            cost-bezeich = gl-acct.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
    
          IF create-it AND deptNo NE 0 THEN
          DO:
            FIND FIRST parameters NO-LOCK WHERE 
              parameters.progname = "CostCenter"  AND
              parameters.section = "alloc"        AND
              parameters.varname = STRING(deptNo) AND
              parameters.vstring = fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.

          /* Oscar (18/12/2024) - 989732 - fix some article seperated */
          /* IF curr-fibu = "" THEN curr-fibu = fibukonto. 
          IF curr-fibu NE fibukonto AND t-anz NE 0 THEN 
          /* IF (lschein NE l-op.lscheinnr) AND t-anz NE 0 THEN */ 
          DO: 
            create str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 41: /*ragung*/
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 14: 
              str-list.s = str-list.s + " ". 
            END. 
            /*MTIF NOT long-digit THEN*/
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
            t-anz = 0. 
            t-val = 0. 
            create str-list. 
            lschein = l-op.lscheinnr. 
            curr-fibu = fibukonto. 
          END.  */
    
          /* IF do-it THEN 
          DO: 
            create str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
            create str-list. 
            do-it = NO. 
          END. */ 
    
          IF create-it THEN 
          DO: 
            /* Oscar (18/12/2024) - 989732 - fix some article seperated */
            IF curr-fibu = "" THEN curr-fibu = fibukonto. 
            IF curr-fibu NE fibukonto AND t-anz NE 0 THEN 
            /* IF (lschein NE l-op.lscheinnr) AND t-anz NE 0 THEN */ 
            DO: 
              CREATE str-list. 
              DO i = 1 TO 45: 
                str-list.s = str-list.s + " ". 
              END. 

              str-list.s = str-list.s + "Subtotal ". 
              DO i = 1 TO 41: /*ragung*/   
                str-list.s = str-list.s + " ". 
              END.

              str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
              DO i = 1 TO 14: 
                str-list.s = str-list.s + " ". 
              END. 

              /*MTIF NOT long-digit THEN */
              /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
              str-list.amount = t-val.
              str-list.avrg-price = 0. 
              /*MTELSE 
              str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
              t-anz = 0. 
              t-val = 0.

              CREATE str-list. 
              lschein = l-op.lscheinnr. 
              curr-fibu = fibukonto. 
            END. 
            
            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich.

              IF cc-code NE 0 THEN 
                s-list.bezeich = STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 

            s-list.cost = s-list.cost + wert.
            s-list.anzahl = s-list.anzahl + l-op.anzahl.
            t-anz = t-anz + l-op.anzahl. 
            t-val = t-val + wert. 
            tot-anz = tot-anz + l-op.anzahl. 
            tot-amount = tot-amount + wert. 

            CREATE str-list. 
            RUN add-id.

            str-list.lscheinnr = l-op.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            str-list.masseinheit = l-artikel.masseinheit.
            str-list.gldept = STRING(gl-department.nr) + " - " + gl-department.bezeich.

            /* Oscar (12/02/25) - DDB12D - show remark in outgoing report */
            FIND FIRST queasy WHERE queasy.KEY EQ 340 
              AND queasy.char1 EQ l-op.lscheinnr
              AND queasy.number1 EQ l-op.artnr
              AND queasy.deci1 EQ l-op.einzelpreis NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
              str-list.remark-artikel = queasy.char2.
            END.
            ELSE
            DO:
              str-list.remark-artikel = "".
            END.

            /*MTIF NOT long-digit THEN*/
            str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(50)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    /* + STRING(preis, ">>>,>>>,>>9.99") 
                    + STRING(wert, "->,>>>,>>>,>>9.99")  */
                    + STRING(l-op.lscheinnr, "x(12)"). 
            /*MTELSE str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(32)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    + STRING(preis, ">>>>,>>>,>>9") 
                    + STRING(wert, "->,>>>,>>>,>>9") 
                    + STRING(l-op.lscheinnr, "x(12)").*/
            str-list.billdate = l-op.datum.
            str-list.avrg-price = preis.
            str-list.amount = wert.
          END. 
      END.
      
      IF t-anz NE 0 THEN 
      DO: 
        CREATE str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 

        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 41: /*ragung*/   
          str-list.s = str-list.s + " ". 
        END.

        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 

        /*MTIF NOT long-digit THEN */
        /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
        str-list.amount = t-val.
        str-list.avrg-price = 0. 
        /*MTELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
        t-anz = 0. 
        t-val = 0. 

        CREATE str-list.
      END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 41: /*ragung*/
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    
    /*MTIF NOT long-digit THEN*/
    /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */ 
    str-list.amount = t-val.
    str-list.avrg-price = 0.
    /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 14: 
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */ 
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  str-list.s = STRING("","x(8)") + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  tot-anz = 0.

  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    /*MTIF NOT long-digit THEN*/
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(50)") 
      + STRING(s-list.anzahl, "->>>>>>>>>>>>>").
      /* + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). */ 
    /*MTELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9").*/
    str-list.amount = s-list.cost.
    str-list.avrg-price = 0.

    tot-amount = tot-amount + s-list.cost. 
    tot-anz = tot-anz + s-list.anzahl.
  END. 

  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->>>>>>>>>>>>>").
  DO i = 1 TO 12:
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
END. 
 
PROCEDURE create-list1A: 
  DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
  DEFINE VARIABLE t-val AS DECIMAL. 
  DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE lschein AS CHAR INITIAL "". 
  DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(30)". 
  DEFINE VARIABLE fibukonto AS CHAR. 
  DEFINE VARIABLE do-it AS LOGICAL. 
  DEFINE VARIABLE create-it AS LOGICAL. 
  DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
  DEFINE VARIABLE other-fibu AS LOGICAL. 
  DEFINE VARIABLE grp1 AS INTEGER INITIAL 0. 
  DEFINE VARIABLE grp2 AS INTEGER INITIAL 1. 
  DEFINE buffer gl-acct1 FOR gl-acct. 
  
  status default "Processing...". 
  
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  do-it = YES.

  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 

      curr-artnr = 0. 
      t-anz = 0.

      /* Oscar (18/12/2024) - 989732 - fix some article seperated */
      CREATE str-list. 
      str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
      
      CREATE str-list.

      curr-artnr = 0.

      /*  calculate the outgoing stocks within the given periods */ 
      FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.anzahl NE 0 AND l-op.op-art = 3 
        AND l-op.loeschflag LE 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum EQ from-grp NO-LOCK, 
        FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
        AND l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund NO-LOCK, 
        FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
        AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
        NO-LOCK BY l-op.datum /*BY l-artikel.bezeich */
        BY l-op.lscheinnr BY l-op.artnr: 
  
          IF show-price THEN 
          DO: 
            preis = l-op.einzelpreis. 
            wert = l-op.warenwert. 
          END. 
    
          it-exist = YES. 
          other-fibu = NO. 
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
    
          IF lschein = "" THEN lschein = l-op.lscheinnr. 
    
          IF other-fibu THEN 
          DO: 
            fibukonto = gl-acct1.fibukonto. 
            cost-bezeich = gl-acct1.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
          ELSE 
          DO: 
            fibukonto = gl-acct.fibukonto. 
            cost-bezeich = gl-acct.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
    
          IF create-it AND deptNo NE 0 THEN
          DO:
            FIND FIRST parameters NO-LOCK WHERE 
              parameters.progname = "CostCenter"  AND
              parameters.section = "alloc"        AND
              parameters.varname = STRING(deptNo) AND
              parameters.vstring = fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.

          /* Oscar (18/12/2024) - 989732 - fix some article seperated */
          /* IF curr-artnr = 0 THEN curr-artnr = l-op.artnr. 
          IF curr-artnr NE l-op.artnr AND t-anz NE 0 THEN 
          DO: 
            create str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 41: /*ragung*/
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 14: 
              str-list.s = str-list.s + " ". 
            END. 
            /*MTIF NOT long-digit THEN*/
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
            t-anz = 0. 
            t-val = 0. 
            create str-list. 
            lschein = l-op.lscheinnr. 
            curr-artnr = l-op.artnr. 
          END.  */
    
          /* IF do-it THEN 
          DO:  
            create str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
            create str-list. 
            do-it = NO. 
          END. */ 
    
          IF create-it THEN 
          DO: 
            /* Oscar (18/12/2024) - 989732 - fix some article seperated */
            IF curr-artnr = 0 THEN curr-artnr = l-op.artnr. 
            IF curr-artnr NE l-op.artnr AND t-anz NE 0 THEN 
            DO: 
              CREATE str-list. 
              DO i = 1 TO 45: 
                str-list.s = str-list.s + " ". 
              END. 

              str-list.s = str-list.s + "Subtotal ". 
              DO i = 1 TO 41: /*ragung*/   
                str-list.s = str-list.s + " ". 
              END.

              str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
              DO i = 1 TO 14: 
                str-list.s = str-list.s + " ". 
              END. 

              /*MTIF NOT long-digit THEN */
              /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
              str-list.amount = t-val.
              str-list.avrg-price = 0. 
              /*MTELSE 
              str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
              t-anz = 0. 
              t-val = 0. 

              CREATE str-list. 
              lschein = l-op.lscheinnr. 
              curr-artnr = l-op.artnr. 
            END. 

            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich.

              IF cc-code NE 0 THEN 
                s-list.bezeich = STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 

            s-list.cost = s-list.cost + wert.
            s-list.anzahl = s-list.anzahl + l-op.anzahl.
            t-anz = t-anz + l-op.anzahl. 
            t-val = t-val + wert. 
            tot-anz = tot-anz + l-op.anzahl. 
            tot-amount = tot-amount + wert. 

            CREATE str-list. 
            RUN add-id.

            str-list.lscheinnr = l-op.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            str-list.masseinheit = l-artikel.masseinheit.
            str-list.gldept = STRING(gl-department.nr) + " - " + gl-department.bezeich.

            /* Oscar (12/02/25) - DDB12D - show remark in outgoing report */
            FIND FIRST queasy WHERE queasy.KEY EQ 340 
              AND queasy.char1 EQ l-op.lscheinnr
              AND queasy.number1 EQ l-op.artnr
              AND queasy.deci1 EQ l-op.einzelpreis NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
              str-list.remark-artikel = queasy.char2.
            END.
            ELSE
            DO:
              str-list.remark-artikel = "".
            END.

            /*MTIF NOT long-digit THEN*/
            str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(50)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    /* + STRING(preis, ">>>,>>>,>>9.99") 
                    + STRING(wert, "->,>>>,>>>,>>9.99")  */
                    + STRING(l-op.lscheinnr, "x(12)"). 
            /*MTELSE str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(32)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    + STRING(preis, ">>>>,>>>,>>9") 
                    + STRING(wert, "->,>>>,>>>,>>9") 
                    + STRING(l-op.lscheinnr, "x(12)").*/
            str-list.billdate = l-op.datum.
            str-list.avrg-price = preis.
            str-list.amount = wert.
          END. 
      END. 

      IF t-anz NE 0 THEN 
      DO: 
        CREATE str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 

        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 41: /*ragung*/   
          str-list.s = str-list.s + " ". 
        END.

        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 

        /*MTIF NOT long-digit THEN */
        /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
        str-list.amount = t-val.
        str-list.avrg-price = 0. 
        /*MTELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
        t-anz = 0. 
        t-val = 0. 

        CREATE str-list.
      END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 41: /*ragung*/
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    
    /*MTIF NOT long-digit THEN*/
    /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */ 
    str-list.amount = t-val.
    str-list.avrg-price = 0.
    /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 14: 
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */ 
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  str-list.s = STRING("","x(8)") + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  tot-anz = 0.

  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    /*MTIF NOT long-digit THEN*/
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(50)") 
      + STRING(s-list.anzahl, "->>>>>>>>>>>>>").
      /* + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). */ 
    /*MTELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9").*/
    str-list.amount = s-list.cost.
    str-list.avrg-price = 0.

    tot-amount = tot-amount + s-list.cost. 
    tot-anz = tot-anz + s-list.anzahl.
  END. 

  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->>>>>>>>>>>>>").
  DO i = 1 TO 12:
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
END. 
 
PROCEDURE create-list1B: 
  DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
  DEFINE VARIABLE t-val AS DECIMAL. 
  DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE lschein AS CHAR INITIAL "". 
  DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(30)". 
  DEFINE VARIABLE fibukonto AS CHAR. 
  DEFINE VARIABLE do-it AS LOGICAL. 
  DEFINE VARIABLE create-it AS LOGICAL. 
  DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
  DEFINE VARIABLE other-fibu AS LOGICAL. 
  DEFINE VARIABLE grp1 AS INTEGER INITIAL 0. 
  DEFINE VARIABLE grp2 AS INTEGER INITIAL 1. 
  DEFINE buffer gl-acct1 FOR gl-acct. 
  
  status default "Processing...".

  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  do-it = YES. 

  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
 
      curr-artnr = 0. 
      t-anz = 0.

      /* Oscar (18/12/2024) - 989732 - fix some article seperated */
      CREATE str-list. 
      str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
      
      CREATE str-list.

      lschein = "".

      /* calculate the outgoing stocks within the given periods */ 
      FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.anzahl NE 0 AND l-op.op-art = 3 
        AND l-op.loeschflag LE 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum EQ from-grp NO-LOCK, 
        FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
        AND l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund NO-LOCK, 
        FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
        AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
        BY l-op.lscheinnr /*BY l-artikel.bezeich*/ BY l-op.artnr: 
  
          IF show-price THEN 
          DO: 
            preis = l-op.einzelpreis. 
            wert = l-op.warenwert. 
          END. 
    
          it-exist = YES. 
          other-fibu = NO. 
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
    
          IF other-fibu THEN 
          DO: 
            fibukonto = gl-acct1.fibukonto. 
            cost-bezeich = gl-acct1.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
          ELSE 
          DO: 
            fibukonto = gl-acct.fibukonto. 
            cost-bezeich = gl-acct.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
    
          IF create-it AND deptNo NE 0 THEN
          DO:
            FIND FIRST parameters NO-LOCK WHERE 
              parameters.progname = "CostCenter"  AND
              parameters.section = "alloc"        AND
              parameters.varname = STRING(deptNo) AND
              parameters.vstring = fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.

          /* Oscar (18/12/2024) - 989732 - fix some article seperated */
          /* IF lschein = "" THEN lschein = l-op.lscheinnr. 
          IF lschein NE l-op.lscheinnr AND t-anz NE 0 THEN 
          DO: 
            create str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 41: /*ragung*/
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 14: 
              str-list.s = str-list.s + " ". 
            END. 
            /*MTIF NOT long-digit THEN*/
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
            t-anz = 0. 
            t-val = 0. 
            create str-list. 
            lschein = l-op.lscheinnr. 
            curr-artnr = l-op.artnr. 
          END.  */
    
          /* IF do-it THEN 
          DO:  
            create str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
            create str-list. 
            do-it = NO. 
          END.  */
    
          IF create-it THEN 
          DO: 
            /* Oscar (18/12/2024) - 989732 - fix some article seperated */
            IF lschein = "" THEN lschein = l-op.lscheinnr. 
            IF (lschein NE l-op.lscheinnr) AND t-anz NE 0 THEN 
            DO: 
              CREATE str-list. 
              DO i = 1 TO 45: 
                str-list.s = str-list.s + " ". 
              END. 

              str-list.s = str-list.s + "Subtotal ". 
              DO i = 1 TO 41: /*ragung*/   
                str-list.s = str-list.s + " ". 
              END.

              str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
              DO i = 1 TO 14: 
                str-list.s = str-list.s + " ". 
              END. 

              /*MTIF NOT long-digit THEN */
              /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
              str-list.amount = t-val.
              str-list.avrg-price = 0. 
              /*MTELSE 
              str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
              t-anz = 0. 
              t-val = 0. 

              CREATE str-list. 
              lschein = l-op.lscheinnr. 
              curr-artnr = l-op.artnr. 
            END.

            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich.

              IF cc-code NE 0 THEN 
                s-list.bezeich = STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 

            s-list.cost = s-list.cost + wert.
            s-list.anzahl = s-list.anzahl + l-op.anzahl.
            t-anz = t-anz + l-op.anzahl. 
            t-val = t-val + wert. 
            tot-anz = tot-anz + l-op.anzahl. 
            tot-amount = tot-amount + wert. 

            CREATE str-list. 
            RUN add-id.

            str-list.lscheinnr = l-op.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            str-list.masseinheit = l-artikel.masseinheit.
            str-list.gldept = STRING(gl-department.nr) + " - " + gl-department.bezeich.

            /* Oscar (12/02/25) - DDB12D - show remark in outgoing report */
            FIND FIRST queasy WHERE queasy.KEY EQ 340 
              AND queasy.char1 EQ l-op.lscheinnr
              AND queasy.number1 EQ l-op.artnr
              AND queasy.deci1 EQ l-op.einzelpreis NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
              str-list.remark-artikel = queasy.char2.
            END.
            ELSE
            DO:
              str-list.remark-artikel = "".
            END.

            /*MTIF NOT long-digit THEN*/
            str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(50)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    /* + STRING(preis, ">>>,>>>,>>9.99") 
                    + STRING(wert, "->,>>>,>>>,>>9.99")  */
                    + STRING(l-op.lscheinnr, "x(12)"). 
            /*MTELSE str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(32)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    + STRING(preis, ">>>>,>>>,>>9") 
                    + STRING(wert, "->,>>>,>>>,>>9") 
                    + STRING(l-op.lscheinnr, "x(12)").*/
            str-list.billdate = l-op.datum.
            str-list.avrg-price = preis.
            str-list.amount = wert.
          END. 
      END. 

      IF t-anz NE 0 THEN 
      DO: 
        CREATE str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 

        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 41: /*ragung*/   
          str-list.s = str-list.s + " ". 
        END.

        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 

        /*MTIF NOT long-digit THEN */
        /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
        str-list.amount = t-val.
        str-list.avrg-price = 0. 
        /*MTELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
        t-anz = 0. 
        t-val = 0. 

        CREATE str-list.
      END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 41: /*ragung*/
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    
    /*MTIF NOT long-digit THEN*/
    /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */ 
    str-list.amount = t-val.
    str-list.avrg-price = 0.
    /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 14: 
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */ 
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  str-list.s = STRING("","x(8)") + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  tot-anz = 0.

  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    /*MTIF NOT long-digit THEN*/
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(50)") 
      + STRING(s-list.anzahl, "->>>>>>>>>>>>>").
      /* + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). */ 
    /*MTELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9").*/
    str-list.amount = s-list.cost.
    str-list.avrg-price = 0.

    tot-amount = tot-amount + s-list.cost. 
    tot-anz = tot-anz + s-list.anzahl.
  END. 

  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->>>>>>>>>>>>>").
  DO i = 1 TO 12:
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
END. 
 
PROCEDURE create-list1C: 
  DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
  DEFINE VARIABLE t-val AS DECIMAL. 
  DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE lschein AS CHAR INITIAL "". 
  DEFINE VARIABLE datum AS DATE INITIAL ?. 
  DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(30)". 
  DEFINE VARIABLE fibukonto AS CHAR. 
  DEFINE VARIABLE do-it AS LOGICAL. 
  DEFINE VARIABLE create-it AS LOGICAL. 
  DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
  DEFINE VARIABLE other-fibu AS LOGICAL. 
  DEFINE VARIABLE grp1 AS INTEGER INITIAL 0. 
  DEFINE VARIABLE grp2 AS INTEGER INITIAL 1. 
  DEFINE buffer gl-acct1 FOR gl-acct. 
  
  status default "Processing...".
   
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  do-it = YES. 

  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
 
      curr-artnr = 0. 
      t-anz = 0.

      /* Oscar (18/12/2024) - 989732 - fix some article seperated */
      CREATE str-list. 
      str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
      
      CREATE str-list.

      datum = ?.
      
      /* calculate the outgoing stocks within the given periods */ 
      FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.anzahl NE 0 AND l-op.op-art = 3 
        AND l-op.loeschflag LE 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum EQ from-grp NO-LOCK, 
        FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
        AND l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund NO-LOCK, 
        FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
        AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
        BY l-op.datum /*BY l-artikel.bezeich*/ BY l-op.artnr: 
  
          IF show-price THEN 
          DO: 
            preis = l-op.einzelpreis. 
            wert = l-op.warenwert. 
          END. 
    
          it-exist = YES. 
          other-fibu = NO. 
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
    
          IF other-fibu THEN 
          DO: 
            fibukonto = gl-acct1.fibukonto. 
            cost-bezeich = gl-acct1.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
          ELSE 
          DO: 
            fibukonto = gl-acct.fibukonto. 
            cost-bezeich = gl-acct.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
    
          IF create-it AND deptNo NE 0 THEN
          DO:
            FIND FIRST parameters NO-LOCK WHERE 
              parameters.progname = "CostCenter"  AND
              parameters.section = "alloc"        AND
              parameters.varname = STRING(deptNo) AND
              parameters.vstring = fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.

          /* Oscar (18/12/2024) - 989732 - fix some article seperated */
          /* IF datum = ? THEN datum = l-op.datum. 
          IF datum NE l-op.datum AND t-anz NE 0 THEN 
          DO: 
            create str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 41: /*ragung*/ 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 14: 
              str-list.s = str-list.s + " ". 
            END. 
            /*MTIF NOT long-digit THEN */
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
            t-anz = 0. 
            t-val = 0. 
            create str-list. 
            lschein = l-op.lscheinnr. 
            datum = l-op.datum. 
            curr-artnr = l-op.artnr. 
          END. */ 
    
          /* IF do-it THEN 
          DO:  
            create str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
            create str-list. 
            do-it = NO. 
          END.  */
    
          IF create-it THEN 
          DO: 
            /* Oscar (18/12/2024) - 989732 - fix some article seperated */
            IF datum = ? THEN datum = l-op.datum. 
            IF datum NE l-op.datum AND t-anz NE 0 THEN 
            DO: 
              CREATE str-list. 
              DO i = 1 TO 45: 
                str-list.s = str-list.s + " ". 
              END. 

              str-list.s = str-list.s + "Subtotal ". 
              DO i = 1 TO 41: /*ragung*/   
                str-list.s = str-list.s + " ". 
              END.

              str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
              DO i = 1 TO 14: 
                str-list.s = str-list.s + " ". 
              END. 

              /*MTIF NOT long-digit THEN */
              /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
              str-list.amount = t-val.
              str-list.avrg-price = 0. 
              /*MTELSE 
              str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
              t-anz = 0. 
              t-val = 0. 

              CREATE str-list. 
              lschein = l-op.lscheinnr. 
              datum = l-op.datum. 
              curr-artnr = l-op.artnr. 
            END.
            
            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich.

              IF cc-code NE 0 THEN 
                s-list.bezeich = STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 

            s-list.cost = s-list.cost + wert.
            s-list.anzahl = s-list.anzahl + l-op.anzahl.
            t-anz = t-anz + l-op.anzahl. 
            t-val = t-val + wert. 
            tot-anz = tot-anz + l-op.anzahl. 
            tot-amount = tot-amount + wert. 

            CREATE str-list. 
            RUN add-id.

            str-list.lscheinnr = l-op.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            str-list.masseinheit = l-artikel.masseinheit.
            str-list.gldept = STRING(gl-department.nr) + " - " + gl-department.bezeich.

            /* Oscar (12/02/25) - DDB12D - show remark in outgoing report */
            FIND FIRST queasy WHERE queasy.KEY EQ 340 
              AND queasy.char1 EQ l-op.lscheinnr
              AND queasy.number1 EQ l-op.artnr
              AND queasy.deci1 EQ l-op.einzelpreis NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
              str-list.remark-artikel = queasy.char2.
            END.
            ELSE
            DO:
              str-list.remark-artikel = "".
            END.

            /*MTIF NOT long-digit THEN*/
            str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(50)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    /* + STRING(preis, ">>>,>>>,>>9.99") 
                    + STRING(wert, "->,>>>,>>>,>>9.99")  */
                    + STRING(l-op.lscheinnr, "x(12)"). 
            /*MTELSE str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(32)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    + STRING(preis, ">>>>,>>>,>>9") 
                    + STRING(wert, "->,>>>,>>>,>>9") 
                    + STRING(l-op.lscheinnr, "x(12)").*/
            str-list.billdate = l-op.datum.
            str-list.avrg-price = preis.
            str-list.amount = wert.
          END. 
      END. 

      IF t-anz NE 0 THEN 
      DO: 
        CREATE str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 

        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 41: /*ragung*/   
          str-list.s = str-list.s + " ". 
        END.

        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 

        /*MTIF NOT long-digit THEN */
        /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
        str-list.amount = t-val.
        str-list.avrg-price = 0. 
        /*MTELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
        t-anz = 0. 
        t-val = 0. 

        CREATE str-list.
      END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 41: /*ragung*/
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    
    /*MTIF NOT long-digit THEN*/
    /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */ 
    str-list.amount = t-val.
    str-list.avrg-price = 0.
    /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 14: 
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */ 
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  str-list.s = STRING("","x(8)") + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  tot-anz = 0.

  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    /*MTIF NOT long-digit THEN*/
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(50)") 
      + STRING(s-list.anzahl, "->>>>>>>>>>>>>").
      /* + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). */ 
    /*MTELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9").*/
    str-list.amount = s-list.cost.
    str-list.avrg-price = 0.

    tot-amount = tot-amount + s-list.cost. 
    tot-anz = tot-anz + s-list.anzahl.
  END. 

  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->>>>>>>>>>>>>").
  DO i = 1 TO 12:
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
END. 

PROCEDURE create-listB: 
  DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
  DEFINE VARIABLE t-val AS DECIMAL. 
  DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE lschein AS CHAR INITIAL "". 
  DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(24)". 
  DEFINE VARIABLE fibukonto AS CHAR. 
  DEFINE VARIABLE do-it AS LOGICAL. 
  DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
  DEFINE VARIABLE other-fibu AS LOGICAL. 
  DEFINE buffer gl-acct1 FOR gl-acct. 
  DEFINE VARIABLE create-it AS LOGICAL. 
  
  status default "Processing...". 
  
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  do-it = YES. 

  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 

      curr-artnr = 0. 
      t-anz = 0.

      /* Oscar (18/12/2024) - 989732 - fix some article seperated */
      CREATE str-list. 
      str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
      
      CREATE str-list.

      lschein = "".

      FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.anzahl NE 0 AND l-op.op-art = 3 
        AND l-op.loeschflag LE 1  NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
        AND l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund NO-LOCK, 
        FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK 
        /*BY SUBSTR(l-op.lscheinnr,4,12) BY l-artikel.bezeich*/ 
        BY l-op.lscheinnr BY l-op.artnr: 
  
          IF show-price THEN 
          DO: 
            preis = l-op.einzelpreis. 
            wert = l-op.warenwert. 
          END. 
    
          it-exist = YES. 
          other-fibu = NO. 
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
    
          IF other-fibu THEN 
          DO: 
            fibukonto = gl-acct1.fibukonto. 
            cost-bezeich = gl-acct1.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
          ELSE 
          DO: 
            fibukonto = gl-acct.fibukonto. 
            cost-bezeich = gl-acct.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
    
          IF create-it AND deptNo NE 0 THEN
          DO:
            FIND FIRST parameters NO-LOCK WHERE 
              parameters.progname = "CostCenter"  AND
              parameters.section = "alloc"        AND
              parameters.varname = STRING(deptNo) AND
              parameters.vstring = fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END. 

          /* Oscar (18/12/2024) - 989732 - fix some article seperated */
          /* IF lschein = "" THEN lschein = l-op.lscheinnr. 
          IF (lschein NE l-op.lscheinnr) AND t-anz NE 0 THEN 
          DO: 
            CREATE str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 

            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 41: /*ragung*/   
              str-list.s = str-list.s + " ". 
            END.

            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 14: 
              str-list.s = str-list.s + " ". 
            END. 

            /*MTIF NOT long-digit THEN */
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            /*MTELSE 
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
            t-anz = 0. 
            t-val = 0. 

            CREATE str-list. 
            lschein = l-op.lscheinnr. 
            curr-artnr = l-op.artnr. 
          END. */

          /* IF do-it THEN 
          DO: 
            create str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
            create str-list. 
            do-it = NO. 
          END. */

          IF create-it THEN 
          DO: 
            /* Oscar (18/12/2024) - 989732 - fix some article seperated */
            IF lschein = "" THEN lschein = l-op.lscheinnr. 
            IF (lschein NE l-op.lscheinnr) AND t-anz NE 0 THEN 
            DO: 
              CREATE str-list. 
              DO i = 1 TO 45: 
                str-list.s = str-list.s + " ". 
              END. 

              str-list.s = str-list.s + "Subtotal ". 
              DO i = 1 TO 41: /*ragung*/   
                str-list.s = str-list.s + " ". 
              END.

              str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
              DO i = 1 TO 14: 
                str-list.s = str-list.s + " ". 
              END. 

              /*MTIF NOT long-digit THEN */
              /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
              str-list.amount = t-val.
              str-list.avrg-price = 0. 
              /*MTELSE 
              str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
              t-anz = 0. 
              t-val = 0. 

              CREATE str-list. 
              lschein = l-op.lscheinnr. 
              curr-artnr = l-op.artnr. 
            END.

            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich.

              IF cc-code NE 0 THEN 
                s-list.bezeich = STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 

            s-list.cost = s-list.cost + wert.
            s-list.anzahl = s-list.anzahl + l-op.anzahl.
            t-anz = t-anz + l-op.anzahl. 
            t-val = t-val + wert. 
            tot-anz = tot-anz + l-op.anzahl. 
            tot-amount = tot-amount + wert. 

            CREATE str-list. 
            RUN add-id.

            str-list.lscheinnr = l-op.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            str-list.masseinheit = l-artikel.masseinheit.
            str-list.gldept = STRING(gl-department.nr) + " - " + gl-department.bezeich.

            /* Oscar (12/02/25) - DDB12D - show remark in outgoing report */
            FIND FIRST queasy WHERE queasy.KEY EQ 340 
              AND queasy.char1 EQ l-op.lscheinnr
              AND queasy.number1 EQ l-op.artnr
              AND queasy.deci1 EQ l-op.einzelpreis NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
              str-list.remark-artikel = queasy.char2.
            END.
            ELSE
            DO:
              str-list.remark-artikel = "".
            END.

            /*MTIF NOT long-digit THEN*/
            str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(50)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    /* + STRING(preis, ">>>,>>>,>>9.99") 
                    + STRING(wert, "->,>>>,>>>,>>9.99")  */
                    + STRING(l-op.lscheinnr, "x(12)"). 
            /*MTELSE str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(32)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    + STRING(preis, ">>>>,>>>,>>9") 
                    + STRING(wert, "->,>>>,>>>,>>9") 
                    + STRING(l-op.lscheinnr, "x(12)").*/
            str-list.billdate = l-op.datum.
            str-list.avrg-price = preis.
            str-list.amount = wert.
          END. 
      END. 

      IF t-anz NE 0 THEN 
      DO: 
        CREATE str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 

        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 41: /*ragung*/   
          str-list.s = str-list.s + " ". 
        END.

        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 

        /*MTIF NOT long-digit THEN */
        /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
        str-list.amount = t-val.
        str-list.avrg-price = 0. 
        /*MTELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
        t-anz = 0. 
        t-val = 0. 

        CREATE str-list.
      END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 41: /*ragung*/
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    
    /*MTIF NOT long-digit THEN*/
    /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */ 
    str-list.amount = t-val.
    str-list.avrg-price = 0.
    /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 14: 
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */ 
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  str-list.s = STRING("","x(8)") + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  tot-anz = 0.

  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    /*MTIF NOT long-digit THEN*/
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(50)") 
      + STRING(s-list.anzahl, "->>>>>>>>>>>>>").
      /* + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). */ 
    /*MTELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9").*/
    str-list.amount = s-list.cost.
    str-list.avrg-price = 0.

    tot-amount = tot-amount + s-list.cost. 
    tot-anz = tot-anz + s-list.anzahl.
  END. 

  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->>>>>>>>>>>>>").
  DO i = 1 TO 12:
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
END. 
 
PROCEDURE create-listC: 
  DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
  DEFINE VARIABLE t-val AS DECIMAL. 
  DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE lschein AS CHAR INITIAL "". 
  DEFINE VARIABLE datum AS DATE INITIAL ?. 
  DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(24)". 
  DEFINE VARIABLE fibukonto AS CHAR. 
  DEFINE VARIABLE do-it AS LOGICAL. 
  DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
  DEFINE VARIABLE other-fibu AS LOGICAL. 
  DEFINE buffer gl-acct1 FOR gl-acct. 
  DEFINE VARIABLE create-it AS LOGICAL. 
  
  status default "Processing...". 
  
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  do-it = YES. 

  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 

      curr-artnr = 0. 
      t-anz = 0.

      /* Oscar (18/12/2024) - 989732 - fix some article seperated */
      CREATE str-list. 
      str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
      
      CREATE str-list.

      datum = ?.

      FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.anzahl NE 0 AND l-op.op-art = 3 
        AND l-op.loeschflag LE 1  NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
        AND l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund NO-LOCK, 
        FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK 
        BY l-op.datum /*BY l-artikel.bezeich*/ BY l-op.artnr: 
  
          IF show-price THEN 
          DO: 
            preis = l-op.einzelpreis. 
            wert = l-op.warenwert. 
          END. 
    
          it-exist = YES. 
          other-fibu = NO. 
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
    
          IF other-fibu THEN 
          DO: 
            fibukonto = gl-acct1.fibukonto. 
            cost-bezeich = gl-acct1.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
          ELSE 
          DO: 
            fibukonto = gl-acct.fibukonto. 
            cost-bezeich = gl-acct.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
    
          IF create-it AND deptNo NE 0 THEN
          DO:
            FIND FIRST parameters NO-LOCK WHERE 
              parameters.progname = "CostCenter"  AND
              parameters.section = "alloc"        AND
              parameters.varname = STRING(deptNo) AND
              parameters.vstring = fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.

          /* Oscar (18/12/2024) - 989732 - fix some article seperated */
          /* IF datum = ? THEN datum = l-op.datum. 
          IF (datum NE l-op.datum) AND t-anz NE 0 THEN 
          DO: 
            create str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 41:  /*ragung*/
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 14: 
              str-list.s = str-list.s + " ". 
            END. 
            /*MTIF NOT long-digit THEN*/
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            /*MTELSE 
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
            t-anz = 0. 
            t-val = 0. 
            create str-list. 
            lschein = l-op.lscheinnr. 
            datum = l-op.datum. 
            curr-artnr = l-op.artnr. 
          END.  */
          
          /* IF do-it THEN 
          DO: 
            create str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
            create str-list. 
            do-it = NO. 
          END. */ 
    
          IF create-it THEN 
          DO: 
            /* Oscar (18/12/2024) - 989732 - fix some article seperated */
            IF datum = ? THEN datum = l-op.datum. 
            IF (datum NE l-op.datum) AND t-anz NE 0 THEN 
            DO: 
              CREATE str-list. 
              DO i = 1 TO 45: 
                str-list.s = str-list.s + " ". 
              END. 

              str-list.s = str-list.s + "Subtotal ". 
              DO i = 1 TO 41: /*ragung*/   
                str-list.s = str-list.s + " ". 
              END.

              str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
              DO i = 1 TO 14: 
                str-list.s = str-list.s + " ". 
              END. 

              /*MTIF NOT long-digit THEN */
              /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
              str-list.amount = t-val.
              str-list.avrg-price = 0. 
              /*MTELSE 
              str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
              t-anz = 0. 
              t-val = 0. 

              CREATE str-list. 
              lschein = l-op.lscheinnr. 
              datum = l-op.datum. 
              curr-artnr = l-op.artnr. 
            END. 

            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich.

              IF cc-code NE 0 THEN 
                s-list.bezeich = STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 

            s-list.cost = s-list.cost + wert.
            s-list.anzahl = s-list.anzahl + l-op.anzahl.
            t-anz = t-anz + l-op.anzahl. 
            t-val = t-val + wert. 
            tot-anz = tot-anz + l-op.anzahl. 
            tot-amount = tot-amount + wert. 

            CREATE str-list. 
            RUN add-id.

            str-list.lscheinnr = l-op.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            str-list.masseinheit = l-artikel.masseinheit.
            str-list.gldept = STRING(gl-department.nr) + " - " + gl-department.bezeich.

            /* Oscar (12/02/25) - DDB12D - show remark in outgoing report */
            FIND FIRST queasy WHERE queasy.KEY EQ 340 
              AND queasy.char1 EQ l-op.lscheinnr
              AND queasy.number1 EQ l-op.artnr
              AND queasy.deci1 EQ l-op.einzelpreis NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
              str-list.remark-artikel = queasy.char2.
            END.
            ELSE
            DO:
              str-list.remark-artikel = "".
            END.

            /*MTIF NOT long-digit THEN*/
            str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(50)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    /* + STRING(preis, ">>>,>>>,>>9.99") 
                    + STRING(wert, "->,>>>,>>>,>>9.99")  */
                    + STRING(l-op.lscheinnr, "x(12)"). 
            /*MTELSE str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(32)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    + STRING(preis, ">>>>,>>>,>>9") 
                    + STRING(wert, "->,>>>,>>>,>>9") 
                    + STRING(l-op.lscheinnr, "x(12)").*/
            str-list.billdate = l-op.datum.
            str-list.avrg-price = preis.
            str-list.amount = wert.
          END. 
      END. 

      IF t-anz NE 0 THEN 
      DO: 
        CREATE str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 

        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 41: /*ragung*/   
          str-list.s = str-list.s + " ". 
        END.

        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 

        /*MTIF NOT long-digit THEN */
        /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
        str-list.amount = t-val.
        str-list.avrg-price = 0. 
        /*MTELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
        t-anz = 0. 
        t-val = 0. 

        CREATE str-list.
      END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 41: /*ragung*/
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    
    /*MTIF NOT long-digit THEN*/
    /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */ 
    str-list.amount = t-val.
    str-list.avrg-price = 0.
    /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 14: 
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */ 
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  str-list.s = STRING("","x(8)") + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  tot-anz = 0.

  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    /*MTIF NOT long-digit THEN*/
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(50)") 
      + STRING(s-list.anzahl, "->>>>>>>>>>>>>").
      /* + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). */ 
    /*MTELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9").*/
    str-list.amount = s-list.cost.
    str-list.avrg-price = 0.

    tot-amount = tot-amount + s-list.cost. 
    tot-anz = tot-anz + s-list.anzahl.
  END. 

  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->>>>>>>>>>>>>").
  DO i = 1 TO 12:
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
END. 


PROCEDURE add-id:
  DEFINE BUFFER usr FOR bediener.

  FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
  IF AVAILABLE usr THEN str-list.id = usr.userinit.
  ELSE IF l-op.fuellflag = 0 THEN ASSIGN str-list.id = "**".
  ELSE str-list.id = "??".
END.

PROCEDURE get-costcenter-code: 
  DEFINE INPUT PARAMETER fibukonto AS CHAR. 
  DEFINE OUTPUT PARAMETER cc-code AS INTEGER INITIAL 0. 
  FIND FIRST parameters WHERE progname = "CostCenter" 
    AND section = "Alloc" AND varname GT "" 
    AND parameters.vstring = fibukonto NO-LOCK NO-ERROR. 
  IF AVAILABLE parameters THEN cc-code = INTEGER(parameters.varname). 
END. 

PROCEDURE create-listA: 
  DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
  DEFINE VARIABLE t-val AS DECIMAL. 
  DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE lschein AS CHAR INITIAL "". 
  DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(24)". 
  DEFINE VARIABLE fibukonto AS CHAR. 
  DEFINE VARIABLE do-it AS LOGICAL. 
  DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
  DEFINE VARIABLE other-fibu AS LOGICAL. 
  DEFINE buffer gl-acct1 FOR gl-acct. 
  DEFINE VARIABLE create-it AS LOGICAL. 
  
  status default "Processing...". 
  
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  do-it = YES. 

  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 

      curr-artnr = 0. 
      t-anz = 0.

      /* Oscar (18/12/2024) - 989732 - fix some article seperated */
      CREATE str-list. 
      str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
      
      CREATE str-list.

      curr-artnr = 0.

      FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.anzahl NE 0 AND l-op.op-art = 3 
        AND l-op.loeschflag LE 1  NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
        AND l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund NO-LOCK, 
        FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK 
        /*BY l-artikel.bezeich*/ BY l-op.datum 
        BY l-op.lscheinnr BY l-op.artnr: 
  
          IF show-price THEN 
          DO: 
            preis = l-op.einzelpreis. 
            wert = l-op.warenwert. 
          END. 
    
          it-exist = YES. 
          other-fibu = NO. 
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
    
          IF lschein = "" THEN lschein = l-op.lscheinnr. 
    
          IF other-fibu THEN 
          DO: 
            fibukonto = gl-acct1.fibukonto. 
            cost-bezeich = gl-acct1.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
          ELSE 
          DO: 
            fibukonto = gl-acct.fibukonto. 
            cost-bezeich = gl-acct.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
    
          IF create-it AND deptNo NE 0 THEN
          DO:
            FIND FIRST parameters NO-LOCK WHERE 
              parameters.progname = "CostCenter"  AND
              parameters.section = "alloc"        AND
              parameters.varname = STRING(deptNo) AND
              parameters.vstring = fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.

          /* Oscar (18/12/2024) - 989732 - fix some article seperated */
          /* IF curr-artnr = 0 THEN curr-artnr = l-op.artnr. 
          IF (curr-artnr NE l-op.artnr) AND t-anz NE 0 THEN 
          DO: 
            create str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 41: /*ragung*/
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 14: 
              str-list.s = str-list.s + " ". 
            END. 
            /*MTIF NOT long-digit THEN*/
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            /*MTELSE 
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
            t-anz = 0. 
            t-val = 0. 
            create str-list. 
            lschein = l-op.lscheinnr. 
            curr-artnr = l-op.artnr. 
          END. */ 

          /* IF do-it THEN 
          DO:  
            create str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
            create str-list. 
            do-it = NO. 
          END. */ 
    
          IF create-it THEN 
          DO: 
            /* Oscar (18/12/2024) - 989732 - fix some article seperated */
            IF curr-artnr = 0 THEN curr-artnr = l-op.artnr. 
            IF (curr-artnr NE l-op.artnr) AND t-anz NE 0 THEN 
            DO: 
              CREATE str-list. 
              DO i = 1 TO 45: 
                str-list.s = str-list.s + " ". 
              END. 

              str-list.s = str-list.s + "Subtotal ". 
              DO i = 1 TO 41: /*ragung*/   
                str-list.s = str-list.s + " ". 
              END.

              str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
              DO i = 1 TO 14: 
                str-list.s = str-list.s + " ". 
              END. 

              /*MTIF NOT long-digit THEN */
              /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
              str-list.amount = t-val.
              str-list.avrg-price = 0. 
              /*MTELSE 
              str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
              t-anz = 0. 
              t-val = 0.

              CREATE str-list. 
              lschein = l-op.lscheinnr. 
              curr-artnr = l-op.artnr. 
            END.
            
            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich.

              IF cc-code NE 0 THEN 
                s-list.bezeich = STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 

            s-list.cost = s-list.cost + wert.
            s-list.anzahl = s-list.anzahl + l-op.anzahl.
            t-anz = t-anz + l-op.anzahl. 
            t-val = t-val + wert. 
            tot-anz = tot-anz + l-op.anzahl. 
            tot-amount = tot-amount + wert. 

            CREATE str-list. 
            RUN add-id.

            str-list.lscheinnr = l-op.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            str-list.masseinheit = l-artikel.masseinheit.
            str-list.gldept = STRING(gl-department.nr) + " - " + gl-department.bezeich.

            /* Oscar (12/02/25) - DDB12D - show remark in outgoing report */
            FIND FIRST queasy WHERE queasy.KEY EQ 340 
              AND queasy.char1 EQ l-op.lscheinnr
              AND queasy.number1 EQ l-op.artnr
              AND queasy.deci1 EQ l-op.einzelpreis NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
              str-list.remark-artikel = queasy.char2.
            END.
            ELSE
            DO:
              str-list.remark-artikel = "".
            END.

            /*MTIF NOT long-digit THEN*/
            str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(50)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    /* + STRING(preis, ">>>,>>>,>>9.99") 
                    + STRING(wert, "->,>>>,>>>,>>9.99")  */
                    + STRING(l-op.lscheinnr, "x(12)"). 
            /*MTELSE str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(32)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    + STRING(preis, ">>>>,>>>,>>9") 
                    + STRING(wert, "->,>>>,>>>,>>9") 
                    + STRING(l-op.lscheinnr, "x(12)").*/
            str-list.billdate = l-op.datum.
            str-list.avrg-price = preis.
            str-list.amount = wert.
          END. 
      END.
      
      IF t-anz NE 0 THEN 
      DO: 
        CREATE str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 

        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 41: /*ragung*/   
          str-list.s = str-list.s + " ". 
        END.

        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 

        /*MTIF NOT long-digit THEN */
        /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
        str-list.amount = t-val.
        str-list.avrg-price = 0. 
        /*MTELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
        t-anz = 0. 
        t-val = 0. 

        CREATE str-list.
      END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 41: /*ragung*/
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    
    /*MTIF NOT long-digit THEN*/
    /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */ 
    str-list.amount = t-val.
    str-list.avrg-price = 0.
    /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 14: 
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */ 
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  str-list.s = STRING("","x(8)") + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  tot-anz = 0.

  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    /*MTIF NOT long-digit THEN*/
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(50)") 
      + STRING(s-list.anzahl, "->>>>>>>>>>>>>").
      /* + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). */ 
    /*MTELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9").*/
    str-list.amount = s-list.cost.
    str-list.avrg-price = 0.

    tot-amount = tot-amount + s-list.cost. 
    tot-anz = tot-anz + s-list.anzahl.
  END. 

  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->>>>>>>>>>>>>").
  DO i = 1 TO 12:
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
END. 


PROCEDURE create-listD: 
  DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
  DEFINE VARIABLE t-val AS DECIMAL. 
  DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE lschein AS CHAR INITIAL "". 
  DEFINE VARIABLE datum AS DATE INITIAL ?. 
  DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(24)". 
  DEFINE VARIABLE fibukonto AS CHAR. 
  DEFINE VARIABLE do-it AS LOGICAL. 
  DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
  DEFINE VARIABLE other-fibu AS LOGICAL. 
  DEFINE buffer gl-acct1 FOR gl-acct. 
  DEFINE VARIABLE create-it AS LOGICAL. 
  DEF VAR curr-zwkum AS CHARACTER INIT "". 
  DEF VAR create-sub-group AS LOGICAL INITIAL YES.
  
  status default "Processing...". 
  
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  do-it = YES.

  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK:  

      curr-artnr = 0. 
      t-anz = 0.

      /* Oscar (18/12/2024) - 989732 - fix some article seperated */
      CREATE str-list. 
      str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
      
      CREATE str-list.

      curr-zwkum = "".

      FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.anzahl NE 0 AND l-op.op-art = 3 
        AND l-op.loeschflag LE 1  NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
        AND l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK, 
        FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK
        BY l-untergrup.bezeich BY l-op.datum /*BY l-artikel.bezeich*/ BY l-op.artnr: 
        
          IF show-price THEN 
          DO: 
            preis = l-op.einzelpreis. 
            wert = l-op.warenwert. 
          END. 
    
          it-exist = YES. 
          other-fibu = NO. 
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
    
          IF other-fibu THEN 
          DO: 
            fibukonto = gl-acct1.fibukonto. 
            cost-bezeich = gl-acct1.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
          ELSE 
          DO: 
            fibukonto = gl-acct.fibukonto. 
            cost-bezeich = gl-acct.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
    
          IF create-it AND deptNo NE 0 THEN
          DO:
            FIND FIRST parameters NO-LOCK WHERE 
              parameters.progname = "CostCenter"  AND
              parameters.section = "alloc"        AND
              parameters.varname = STRING(deptNo) AND
              parameters.vstring = fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.

          /* Oscar (18/12/2024) - 989732 - fix some article seperated */
          /* IF datum = ? THEN datum = l-op.datum. 
          IF (datum NE l-op.datum) AND t-anz NE 0 THEN 
          DO: 
            create str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 41: /*ragung*/ 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 14: 
              str-list.s = str-list.s + " ". 
            END. 
            /*EKOIF NOT long-digit THEN*/ 
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            /*EKOELSE 
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/ 
            t-anz = 0. 
            t-val = 0. 
            create str-list. 
            lschein = l-op.lscheinnr. 
            datum = l-op.datum. 
            curr-artnr = l-op.artnr. 
          END. */ 
    
          /* IF do-it THEN 
          DO: 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
            create str-list.
            do-it = NO. 
          END. */ 

          /* IF curr-zwkum NE l-untergrup.zwkum THEN
          DO:
            curr-zwkum = l-untergrup.zwkum.
            create str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-untergrup.bezeich, "x(24)"). 
          END. */
          
          IF create-it THEN 
          DO: 
            /* Oscar (18/12/2024) - 989732 - fix some article seperated */
            IF curr-zwkum = "" THEN curr-zwkum = l-untergrup.bezeich. 
            IF (curr-zwkum NE l-untergrup.bezeich) AND t-anz NE 0 THEN 
            DO: 
              CREATE str-list. 
              DO i = 1 TO 45: 
                str-list.s = str-list.s + " ". 
              END. 

              str-list.s = str-list.s + "Subtotal ". 
              DO i = 1 TO 41: /*ragung*/   
                str-list.s = str-list.s + " ". 
              END.

              str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
              DO i = 1 TO 14: 
                str-list.s = str-list.s + " ". 
              END. 

              /*MTIF NOT long-digit THEN */
              /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
              str-list.amount = t-val.
              str-list.avrg-price = 0. 
              /*MTELSE 
              str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
              t-anz = 0. 
              t-val = 0. 

              CREATE str-list. 
              lschein = l-op.lscheinnr. 
              datum = l-op.datum. 
              curr-artnr = l-op.artnr. 
              curr-zwkum = l-untergrup.bezeich.

              create-sub-group = YES.
            END.

            IF create-sub-group THEN
            DO:
              CREATE str-list. 
              str-list.s = STRING("", "x(8)") + "SUB: " + STRING(l-untergrup.bezeich, "x(19)").
              CREATE str-list.
              create-sub-group = NO.
            END.

            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich.

              IF cc-code NE 0 THEN 
                s-list.bezeich = STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 

            s-list.cost = s-list.cost + wert.
            s-list.anzahl = s-list.anzahl + l-op.anzahl.
            t-anz = t-anz + l-op.anzahl. 
            t-val = t-val + wert. 
            tot-anz = tot-anz + l-op.anzahl. 
            tot-amount = tot-amount + wert. 

            CREATE str-list. 
            RUN add-id.

            str-list.lscheinnr = l-op.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            str-list.masseinheit = l-artikel.masseinheit.
            str-list.gldept = STRING(gl-department.nr) + " - " + gl-department.bezeich.

            /* Oscar (12/02/25) - DDB12D - show remark in outgoing report */
            FIND FIRST queasy WHERE queasy.KEY EQ 340 
              AND queasy.char1 EQ l-op.lscheinnr
              AND queasy.number1 EQ l-op.artnr
              AND queasy.deci1 EQ l-op.einzelpreis NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
              str-list.remark-artikel = queasy.char2.
            END.
            ELSE
            DO:
              str-list.remark-artikel = "".
            END.

            /*MTIF NOT long-digit THEN*/
            str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(50)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    /* + STRING(preis, ">>>,>>>,>>9.99") 
                    + STRING(wert, "->,>>>,>>>,>>9.99")  */
                    + STRING(l-op.lscheinnr, "x(12)"). 
            /*MTELSE str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(32)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    + STRING(preis, ">>>>,>>>,>>9") 
                    + STRING(wert, "->,>>>,>>>,>>9") 
                    + STRING(l-op.lscheinnr, "x(12)").*/
            str-list.billdate = l-op.datum.
            str-list.avrg-price = preis.
            str-list.amount = wert.
          END. 
      END. 

      IF t-anz NE 0 THEN 
      DO: 
        CREATE str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 

        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 41: /*ragung*/   
          str-list.s = str-list.s + " ". 
        END.

        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 

        /*MTIF NOT long-digit THEN */
        /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
        str-list.amount = t-val.
        str-list.avrg-price = 0. 
        /*MTELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
        t-anz = 0. 
        t-val = 0. 

        CREATE str-list.
        create-sub-group = YES.
      END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 41: /*ragung*/
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    
    /*MTIF NOT long-digit THEN*/
    /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */ 
    str-list.amount = t-val.
    str-list.avrg-price = 0.
    /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 14: 
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */ 
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  str-list.s = STRING("","x(8)") + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  tot-anz = 0.

  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    /*MTIF NOT long-digit THEN*/
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(50)") 
      + STRING(s-list.anzahl, "->>>>>>>>>>>>>").
      /* + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). */ 
    /*MTELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9").*/
    str-list.amount = s-list.cost.
    str-list.avrg-price = 0.

    tot-amount = tot-amount + s-list.cost. 
    tot-anz = tot-anz + s-list.anzahl.
  END. 

  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->>>>>>>>>>>>>").
  DO i = 1 TO 12:
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
END. 


PROCEDURE create-list1D: 
  DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
  DEFINE VARIABLE t-val AS DECIMAL. 
  DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE lschein AS CHAR INITIAL "". 
  DEFINE VARIABLE datum AS DATE INITIAL ?. 
  DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(30)". 
  DEFINE VARIABLE fibukonto AS CHAR. 
  DEFINE VARIABLE do-it AS LOGICAL. 
  DEFINE VARIABLE create-it AS LOGICAL. 
  DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
  DEFINE VARIABLE other-fibu AS LOGICAL. 
  DEFINE VARIABLE grp1 AS INTEGER INITIAL 0. 
  DEFINE VARIABLE grp2 AS INTEGER INITIAL 1. 
  DEFINE buffer gl-acct1 FOR gl-acct. 
  DEF VAR curr-zwkum AS CHARACTER INIT "".
  DEF VAR create-sub-group AS LOGICAL INITIAL YES.

  status default "Processing...". 
  
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  do-it = YES. 

  /* calculate the outgoing stocks within the given periods */ 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK:

      curr-artnr = 0. 
      t-anz = 0.

      /* Oscar (18/12/2024) - 989732 - fix some article seperated */
      CREATE str-list. 
      str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
      
      CREATE str-list.
      
      curr-zwkum = "".

      FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.anzahl NE 0 AND l-op.op-art = 3 
        AND l-op.loeschflag LE 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum EQ from-grp NO-LOCK, 
        FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
        AND l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK, 
        FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
        AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
        /*BY l-op.datum BY l-artikel.bezeich*/
        BY l-untergrup.bezeich BY l-op.datum /*BY l-artikel.bezeich*/ BY l-op.artnr:
  
          IF show-price THEN 
          DO: 
            preis = l-op.einzelpreis. 
            wert = l-op.warenwert. 
          END. 
    
          it-exist = YES. 
          other-fibu = NO. 
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
    
          IF other-fibu THEN 
          DO: 
            fibukonto = gl-acct1.fibukonto. 
            cost-bezeich = gl-acct1.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
          ELSE 
          DO: 
            fibukonto = gl-acct.fibukonto. 
            cost-bezeich = gl-acct.bezeich. 
            IF cost-acct = "" THEN create-it = YES. 
            ELSE create-it = (cost-acct = fibukonto). 
          END. 
    
          IF create-it AND deptNo NE 0 THEN
          DO:
            FIND FIRST parameters NO-LOCK WHERE 
              parameters.progname = "CostCenter"  AND
              parameters.section = "alloc"        AND
              parameters.varname = STRING(deptNo) AND
              parameters.vstring = fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.

          /* Oscar (18/12/2024) - 989732 - fix some article seperated */
          /* IF datum = ? THEN datum = l-op.datum. 
          IF datum NE l-op.datum AND t-anz NE 0 THEN 
          DO: 
            create str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 41: /*ragung*/ 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 14: 
              str-list.s = str-list.s + " ". 
            END. 
            /*EKO*IF NOT long-digit THEN */
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            /*EKO*ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). */
            t-anz = 0. 
            t-val = 0. 
            create str-list. 
            lschein = l-op.lscheinnr. 
            datum = l-op.datum. 
            curr-artnr = l-op.artnr. 
          END. */ 
    
          /* IF do-it THEN 
          DO:  
            create str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
            create str-list. 
            do-it = NO. 
          END. */ 
    
          /* IF curr-zwkum NE l-untergrup.zwkum THEN
          DO:
            curr-zwkum = l-untergrup.zwkum.
            create str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-untergrup.bezeich, "x(24)"). 
          END. */

          IF create-it THEN 
          DO: 
            /* Oscar (18/12/2024) - 989732 - fix some article seperated */
            IF curr-zwkum = "" THEN curr-zwkum = l-untergrup.bezeich. 
            IF (curr-zwkum NE l-untergrup.bezeich) AND t-anz NE 0 THEN 
            DO: 
              CREATE str-list. 
              DO i = 1 TO 45: 
                str-list.s = str-list.s + " ". 
              END. 

              str-list.s = str-list.s + "Subtotal ". 
              DO i = 1 TO 41: /*ragung*/   
                str-list.s = str-list.s + " ". 
              END.

              str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
              DO i = 1 TO 14: 
                str-list.s = str-list.s + " ". 
              END. 

              /*MTIF NOT long-digit THEN */
              /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
              str-list.amount = t-val.
              str-list.avrg-price = 0. 
              /*MTELSE 
              str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
              t-anz = 0. 
              t-val = 0. 
 
              CREATE str-list. 
              lschein = l-op.lscheinnr. 
              datum = l-op.datum. 
              curr-artnr = l-op.artnr.
              curr-zwkum = l-untergrup.bezeich.
              
              create-sub-group = YES.
            END.

            IF create-sub-group THEN
            DO:
              CREATE str-list. 
              str-list.s = STRING("", "x(8)") + "SUB: " + STRING(l-untergrup.bezeich, "x(24)").
              CREATE str-list.
              create-sub-group = NO.
            END.

            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich.

              IF cc-code NE 0 THEN 
                s-list.bezeich = STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 

            s-list.cost = s-list.cost + wert.
            s-list.anzahl = s-list.anzahl + l-op.anzahl.
            t-anz = t-anz + l-op.anzahl. 
            t-val = t-val + wert. 
            tot-anz = tot-anz + l-op.anzahl. 
            tot-amount = tot-amount + wert. 

            CREATE str-list. 
            RUN add-id.

            str-list.lscheinnr = l-op.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            str-list.masseinheit = l-artikel.masseinheit.
            str-list.gldept = STRING(gl-department.nr) + " - " + gl-department.bezeich.

            /* Oscar (12/02/25) - DDB12D - show remark in outgoing report */
            FIND FIRST queasy WHERE queasy.KEY EQ 340 
              AND queasy.char1 EQ l-op.lscheinnr
              AND queasy.number1 EQ l-op.artnr
              AND queasy.deci1 EQ l-op.einzelpreis NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
              str-list.remark-artikel = queasy.char2.
            END.
            ELSE
            DO:
              str-list.remark-artikel = "".
            END.

            /*MTIF NOT long-digit THEN*/
            str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(50)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    /* + STRING(preis, ">>>,>>>,>>9.99") 
                    + STRING(wert, "->,>>>,>>>,>>9.99")  */
                    + STRING(l-op.lscheinnr, "x(12)"). 
            /*MTELSE str-list.s = STRING(l-op.datum) 
                    + STRING(s-list.bezeich, "x(30)") 
                    + STRING(l-artikel.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(32)") 
                    + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                    + STRING(preis, ">>>>,>>>,>>9") 
                    + STRING(wert, "->,>>>,>>>,>>9") 
                    + STRING(l-op.lscheinnr, "x(12)").*/
            str-list.billdate = l-op.datum.
            str-list.avrg-price = preis.
            str-list.amount = wert.
          END. 
      END. 

      IF t-anz NE 0 THEN 
      DO: 
        CREATE str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 

        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 41: /*ragung*/   
          str-list.s = str-list.s + " ". 
        END.

        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 

        /*MTIF NOT long-digit THEN */
        /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */
        str-list.amount = t-val.
        str-list.avrg-price = 0. 
        /*MTELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
        t-anz = 0. 
        t-val = 0. 

        CREATE str-list.
        create-sub-group = YES.
      END.
  END. 
  
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 41: /*ragung*/
      str-list.s = str-list.s + " ". 
    END. 

    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    
    /*MTIF NOT long-digit THEN*/
    /* str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). */ 
    str-list.amount = t-val.
    str-list.avrg-price = 0.
    /*MTELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9").*/
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 14: 
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */ 
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  str-list.s = STRING("","x(8)") + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  tot-anz = 0.

  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    /*MTIF NOT long-digit THEN*/
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(50)") 
      + STRING(s-list.anzahl, "->>>>>>>>>>>>>").
      /* + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). */ 
    /*MTELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9").*/
    str-list.amount = s-list.cost.
    str-list.avrg-price = 0.

    tot-amount = tot-amount + s-list.cost. 
    tot-anz = tot-anz + s-list.anzahl.
  END. 

  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 41: /*ragung*/
    str-list.s = str-list.s + " ". 
  END. 

  str-list.s = str-list.s + STRING(tot-anz, "->>>>>>>>>>>>>").
  DO i = 1 TO 12:
    str-list.s = str-list.s + " ". 
  END. 

  /*MTIF NOT long-digit THEN*/
  /* str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9.99"). */
  str-list.amount = tot-amount.
  str-list.avrg-price = 0.
  /*MTELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9").*/
END. 

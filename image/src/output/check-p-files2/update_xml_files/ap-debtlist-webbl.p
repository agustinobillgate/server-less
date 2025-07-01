DEFINE TEMP-TABLE output-list 
  FIELD paid        AS CHAR FORMAT "x(3)" 
  FIELD ap-recid    AS INTEGER INITIAL 0 
  FIELD STR         AS CHAR
  FIELD lscheinnr   AS CHAR
    /*gst for penang*/
  FIELD gstid       AS CHAR
  FIELD tax-code    AS CHAR
  FIELD tax-amount  AS CHAR
  FIELD tot-amt     AS CHAR
  /*ragung ganti field from str*/
  FIELD lief        AS CHAR
  FIELD datum       AS CHAR
  FIELD docu-nr     AS CHAR
  FIELD NAME        AS CHAR 
  FIELD amount      AS CHAR
  FIELD id          AS CHAR 
  FIELD due-date    AS CHAR
  FIELD remark      AS CHAR 
  . 


DEFINE TEMP-TABLE taxcode-list
    FIELD taxcode   AS CHAR
    FIELD taxamount AS DECIMAL.

DEF INPUT  PARAMETER duedate-flag  AS LOGICAL.
DEF INPUT  PARAMETER from-lief     AS INT.
DEF INPUT  PARAMETER to-lief       AS INT.
DEF INPUT  PARAMETER paid-flag     AS LOGICAL.
DEF INPUT  PARAMETER excl-apmanual AS LOGICAL.
DEF INPUT  PARAMETER from-date     AS DATE.
DEF INPUT  PARAMETER to-date       AS DATE.
DEF INPUT  PARAMETER from-supp     AS CHAR.
DEF INPUT  PARAMETER to-supp       AS CHAR.
DEF INPUT  PARAMETER only-apmanual AS LOGICAL.
DEF INPUT  PARAMETER TABLE FOR taxcode-list.
DEF OUTPUT PARAMETER TABLE FOR output-list.

IF NOT duedate-flag THEN
DO:
    IF from-lief NE 0 AND to-lief = from-lief THEN 
    DO: 
      IF paid-flag THEN RUN create-list0A. 
      ELSE RUN create-list0B. 
    END. 
    ELSE 
    DO: 
      IF paid-flag THEN RUN create-listA. 
      ELSE RUN create-listB. 
    END.
END.
ELSE IF duedate-flag THEN
DO:
    IF from-lief NE 0 AND to-lief = from-lief THEN 
    DO: 
      IF paid-flag THEN RUN create-Dlist0A. 
      ELSE RUN create-Dlist0B. 
    END. 
    ELSE 
    DO: 
      IF paid-flag THEN RUN create-DlistA. 
      ELSE RUN create-DlistB. 
    END.
END.


/****************************************************/
PROCEDURE create-list0A: 
DEFINE VARIABLE t-debit     AS DECIMAL. 
DEFINE VARIABLE tot-debit   AS DECIMAL. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE due-date    AS DATE. 
DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)" INITIAL "". 
DEFINE VARIABLE code1       AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE code2       AS INTEGER INITIAL 1 NO-UNDO.
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
DEFINE VARIABLE loopi       AS INTEGER NO-UNDO.
DEFINE VARIABLE amt         AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-tax       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv       AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-tax     AS DECIMAL. 
DEFINE VARIABLE tot-amt     AS DECIMAL.
DEFINE VARIABLE t-amt       AS DECIMAL.
DEFINE VARIABLE tamt        AS DECIMAL.

  
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  
  ASSIGN
    t-debit   = 0 
    tot-debit = 0
    amt       = 0 
    t-tax     = 0 
    t-inv     = 0
    tot-tax   = 0
    tot-amt   = 0
    t-amt     = 0
    tamt      = 0.

  IF excl-apmanual THEN ASSIGN code2 = 0.

  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto = 0 
    AND l-kredit.lief-nr = from-lief 
    AND l-kredit.steuercode GE code1 AND l-kredit.steuercode LE code2 
    NO-LOCK USE-INDEX liefnr_ix, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
    BY l-lieferant.firma BY l-kredit.rgdatum BY l-kredit.name: 

    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.

    IF only-apmanual AND l-kredit.steuercode = 1 THEN do-it = YES.
    ELSE IF only-apmanual AND l-kredit.steuercode = 0 THEN do-it = NO.

    IF do-it THEN
    DO:
      IF receiver NE l-lieferant.firma THEN 
      DO: 
        IF receiver NE "" THEN 
        DO: 
/*      CREATE output-list. */ 
          CREATE output-list. 
          ASSIGN
              output-list.lscheinnr = "T O T A L" 
              output-list.amount    = STRING(t-debit, "->>>,>>>,>>>,>>9.99"). 
          CREATE output-list. 
          t-debit = 0. 
        END. 
      END. 
      receiver = l-lieferant.firma. 
      due-date = l-kredit.rgdatum + l-kredit.ziel. 
      CREATE output-list. 
      ASSIGN
          output-list.ap-recid  = RECID(l-kredit)
          output-list.datum     = STRING(l-kredit.rgdatum) 
          output-list.lief      = receiver
          output-list.NAME      = l-kredit.name
          output-list.amount    = STRING(l-kredit.netto, "->>>,>>>,>>>,>>9.99")
          output-list.docu-nr   = l-kredit.lscheinnr
          output-list.lscheinnr = l-kredit.lscheinnr.

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.id = STRING(bediener.userinit,"x(2)"). 
      ELSE output-list.id = "  ". 
      output-list.due-date = STRING(due-date). 

      /*ITA 260916*/
      IF NUM-ENTRIES(l-kredit.bemerk, ";") GT 1 THEN 
          ASSIGN output-list.remark = ENTRY(1, l-kredit.bemerk, ";" )
                 output-list.tax-code = STRING(ENTRY(2, l-kredit.bemerk, ";" ), "x(10)").
      ELSE output-list.remark = l-kredit.bemerk.
      
      IF l-lieferant.plz NE " " THEN DO:
          IF l-lieferant.plz MATCHES "*#*" THEN DO:
              DO loopi = 1 TO NUM-ENTRIES(l-lieferant.plz,"#"):
                  IF ENTRY(loopi + 1, l-lieferant.plz, "#") NE " "  THEN DO:
                        ASSIGN output-list.gstid = ENTRY(loopi + 1, l-lieferant.plz, "#").
                        LEAVE.
                  END.                   
              END.
          END.
      END.

      IF NUM-ENTRIES(l-kredit.bemerk, ";") = 3 THEN DO:
              ASSIGN 
                  t-amt                  = DECIMAL(ENTRY(3, l-kredit.bemerk, ";" ))
                  output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                  t-tax                  = t-tax   + t-amt
                  tot-tax                = tot-tax + t-amt
                     
                  tamt                = l-kredit.netto - t-amt
                  output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                  t-inv               = t-inv + tamt
                  tot-amt             = tot-amt + tamt.

      END.
      ELSE DO:
          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = output-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                    = l-kredit.netto * taxcode-list.taxamount
                     t-amt                  = l-kredit.netto * taxcode-list.taxamount
                     output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                     t-tax                  = t-tax   + (l-kredit.netto * taxcode-list.taxamount)
                     tot-tax                = tot-tax + (l-kredit.netto * taxcode-list.taxamount) 
                     
                     tamt                = l-kredit.netto - t-amt
                     output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                     t-inv               = t-inv + (l-kredit.netto - t-amt)
                     tot-amt             = tot-amt + (l-kredit.netto - t-amt).
          END.
      END.
      /*end*/

      IF l-kredit.opart = 2 THEN output-list.paid = "Yes". 
      ELSE output-list.paid = "No". 
      t-debit = t-debit + l-kredit.netto. 
      tot-debit = tot-debit + l-kredit.netto. 
    END. 
  END.

/* CREATE output-list. */ 
  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = "T O T A L"
      output-list.amount     = STRING(t-debit, "->>>,>>>,>>>,>>9.99").
      output-list.tax-amount = STRING(t-tax, "->>>,>>>,>>>,>>9.99" ).
      output-list.tot-amt    = STRING(t-inv, "->>>,>>>,>>>,>>9.99" ).
 
  CREATE output-list. 

  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = output-list.str + "Grand TOTAL" 
      output-list.amount     = STRING(tot-debit, "->>>,>>>,>>>,>>9.99")
      output-list.tax-amount = STRING(tot-tax, "->>>,>>>,>>>,>>9.99" )
      output-list.tot-amt    = STRING(tot-amt, "->>>,>>>,>>>,>>9.99" ).
END. 
 
PROCEDURE create-Dlist0A: 
DEFINE VARIABLE t-debit     AS DECIMAL. 
DEFINE VARIABLE tot-debit   AS DECIMAL. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE due-date    AS DATE. 
DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)" INITIAL "". 
DEFINE VARIABLE code1       AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE code2       AS INTEGER INITIAL 1 NO-UNDO.
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
DEFINE VARIABLE loopi       AS INTEGER NO-UNDO.
DEFINE VARIABLE amt         AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-tax       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv       AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-tax     AS DECIMAL. 
DEFINE VARIABLE tot-amt     AS DECIMAL.
DEFINE VARIABLE t-amt       AS DECIMAL.
DEFINE VARIABLE tamt        AS DECIMAL.
  
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  
  ASSIGN
    t-debit   = 0 
    tot-debit = 0
    amt       = 0 
    t-tax     = 0 
    t-inv     = 0
    tot-tax   = 0
    tot-amt   = 0
    t-amt     = 0
    tamt      = 0.

  IF excl-apmanual THEN ASSIGN code2 = 0.

  FOR EACH l-kredit WHERE (l-kredit.rgdatum + l-kredit.ziel) GE from-date 
    AND (l-kredit.rgdatum + l-kredit.ziel) LE to-date 
    AND l-kredit.zahlkonto = 0 
    AND l-kredit.lief-nr = from-lief 
    AND l-kredit.steuercode GE code1 AND l-kredit.steuercode LE code2 
    NO-LOCK USE-INDEX liefnr_ix, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
    BY l-lieferant.firma BY (l-kredit.rgdatum + l-kredit.ziel) BY l-kredit.name: 
    
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    IF only-apmanual AND l-kredit.steuercode = 1 THEN do-it = YES.
    ELSE IF only-apmanual AND l-kredit.steuercode = 0 THEN do-it = NO.

    IF do-it THEN
    DO:
      IF receiver NE l-lieferant.firma THEN 
      DO: 
        IF receiver NE "" THEN 
        DO: 
/*      CREATE output-list. */ 
          CREATE output-list. 
          ASSIGN
              output-list.lscheinnr = "T O T A L" 
              output-list.amount    = STRING(t-debit, "->>>,>>>,>>>,>>9.99"). 
          CREATE output-list. 
          t-debit = 0. 
        END. 
      END. 
    
      receiver = l-lieferant.firma. 
      due-date = l-kredit.rgdatum + l-kredit.ziel. 
      CREATE output-list. 
      ASSIGN
          output-list.ap-recid  = RECID(l-kredit)
          output-list.datum     = STRING(l-kredit.rgdatum) 
          output-list.lief      = receiver
          output-list.NAME      = l-kredit.name
          output-list.amount    = STRING(l-kredit.netto, "->>>,>>>,>>>,>>9.99")
          output-list.docu-nr   = l-kredit.lscheinnr
          output-list.lscheinnr = l-kredit.lscheinnr.

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.id = STRING(bediener.userinit,"x(2)"). 
      ELSE output-list.id = "  ". 
      output-list.due-date = STRING(due-date). 

      /*ITA 260916*/
      IF NUM-ENTRIES(l-kredit.bemerk, ";") GT 1 THEN 
          ASSIGN output-list.remark = ENTRY(1, l-kredit.bemerk, ";" )
                 output-list.tax-code = STRING(ENTRY(2, l-kredit.bemerk, ";" ), "x(10)").
      ELSE output-list.remark = l-kredit.bemerk.
      
      IF l-lieferant.plz NE " " THEN DO:
          IF l-lieferant.plz MATCHES "*#*" THEN DO:
              DO loopi = 1 TO NUM-ENTRIES(l-lieferant.plz,"#"):
                  IF ENTRY(loopi + 1, l-lieferant.plz, "#") NE " "  THEN DO:
                        ASSIGN output-list.gstid = ENTRY(loopi + 1, l-lieferant.plz, "#").
                        LEAVE.
                  END.                   
              END.
          END.
      END.

      IF NUM-ENTRIES(l-kredit.bemerk, ";") = 3 THEN DO:
              ASSIGN 
                  t-amt                  = DECIMAL(ENTRY(3, l-kredit.bemerk, ";" ))
                  output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                  t-tax                  = t-tax   + t-amt
                  tot-tax                = tot-tax + t-amt
                     
                  tamt                = l-kredit.netto - t-amt
                  output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                  t-inv               = t-inv + tamt
                  tot-amt             = tot-amt + tamt.

      END.
      ELSE DO:
          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = output-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                    = l-kredit.netto * taxcode-list.taxamount
                     t-amt                  = l-kredit.netto * taxcode-list.taxamount
                     output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                     t-tax                  = t-tax   + (l-kredit.netto * taxcode-list.taxamount)
                     tot-tax                = tot-tax + (l-kredit.netto * taxcode-list.taxamount) 
                     
                     tamt                = l-kredit.netto - t-amt
                     output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                     t-inv               = t-inv + (l-kredit.netto - t-amt)
                     tot-amt             = tot-amt + (l-kredit.netto - t-amt).
          END.
      END.
      /*end*/
      IF l-kredit.opart = 2 THEN output-list.paid = "Yes". 
      ELSE output-list.paid = "No". 
      t-debit = t-debit + l-kredit.netto. 
      tot-debit = tot-debit + l-kredit.netto. 
    END.
  END.
 
/* CREATE output-list. */ 
  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = "T O T A L"
      output-list.amount     = STRING(t-debit, "->>>,>>>,>>>,>>9.99").
      output-list.tax-amount = STRING(t-tax, "->>>,>>>,>>>,>>9.99" ).
      output-list.tot-amt    = STRING(t-inv, "->>>,>>>,>>>,>>9.99" ).
 
  CREATE output-list. 

  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = output-list.str + "Grand TOTAL" 
      output-list.amount     = STRING(tot-debit, "->>>,>>>,>>>,>>9.99")
      output-list.tax-amount = STRING(tot-tax, "->>>,>>>,>>>,>>9.99" )
      output-list.tot-amt    = STRING(tot-amt, "->>>,>>>,>>>,>>9.99" ).
END. 
 
PROCEDURE create-list0B: 
DEFINE VARIABLE t-debit     AS DECIMAL. 
DEFINE VARIABLE tot-debit   AS DECIMAL. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE due-date    AS DATE. 
DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)" INITIAL "". 
DEFINE VARIABLE code1       AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE code2       AS INTEGER INITIAL 1 NO-UNDO.
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
DEFINE VARIABLE loopi       AS INTEGER NO-UNDO.
DEFINE VARIABLE amt         AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-tax       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv       AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-tax     AS DECIMAL. 
DEFINE VARIABLE tot-amt     AS DECIMAL.
DEFINE VARIABLE t-amt       AS DECIMAL.
DEFINE VARIABLE tamt        AS DECIMAL.
  
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  
  ASSIGN
    t-debit   = 0 
    tot-debit = 0
    amt       = 0 
    t-tax     = 0 
    t-inv     = 0
    tot-tax   = 0
    tot-amt   = 0
    t-amt     = 0
    tamt      = 0.

  IF excl-apmanual THEN ASSIGN code2 = 0.

  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto = 0 
    AND l-kredit.lief-nr = from-lief AND l-kredit.opart = 0 
    AND l-kredit.steuercode GE code1 AND l-kredit.steuercode LE code2 
    NO-LOCK USE-INDEX liefnr_ix, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
    BY l-lieferant.firma BY l-kredit.rgdatum BY l-kredit.name: 
    
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    IF only-apmanual AND l-kredit.steuercode = 1 THEN do-it = YES.
    ELSE IF only-apmanual AND l-kredit.steuercode = 0 THEN do-it = NO.

    IF do-it THEN
    DO:
      IF receiver NE l-lieferant.firma THEN 
      DO: 
        IF receiver NE "" THEN 
        DO: 
/*      CREATE output-list. */ 
          CREATE output-list. 
          ASSIGN
              output-list.lscheinnr = "T O T A L" 
              output-list.amount    = STRING(t-debit, "->>>,>>>,>>>,>>9.99").
          CREATE output-list. 
          t-debit = 0. 
        END. 
      END. 
      receiver = l-lieferant.firma. 
      due-date = l-kredit.rgdatum + l-kredit.ziel. 
      CREATE output-list. 
      ASSIGN
          output-list.ap-recid  = RECID(l-kredit)
          output-list.datum     = STRING(l-kredit.rgdatum) 
          output-list.lief      = receiver
          output-list.NAME      = l-kredit.name
          output-list.amount    = STRING(l-kredit.netto, "->>>,>>>,>>>,>>9.99")
          output-list.docu-nr   = l-kredit.lscheinnr
          output-list.lscheinnr = l-kredit.lscheinnr.

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
          ASSIGN output-list.remark = ENTRY(1, l-kredit.bemerk, ";" )
                 output-list.tax-code = STRING(ENTRY(2, l-kredit.bemerk, ";" ), "x(10)").
      ELSE output-list.remark = l-kredit.bemerk.
      
      /*ITA 260916*/
      IF NUM-ENTRIES(l-kredit.bemerk, ";") GT 1 THEN 
          ASSIGN output-list.str = output-list.str + STRING(ENTRY(1, l-kredit.bemerk, ";" ), "x(30)")
                 output-list.tax-code = STRING(ENTRY(2, l-kredit.bemerk, ";" ), "x(10)").
      ELSE output-list.str = output-list.str + STRING(l-kredit.bemerk, "x(30)").
      
      IF l-lieferant.plz NE " " THEN DO:
          IF l-lieferant.plz MATCHES "*#*" THEN DO:
              DO loopi = 1 TO NUM-ENTRIES(l-lieferant.plz,"#"):
                  IF ENTRY(loopi + 1, l-lieferant.plz, "#") NE " "  THEN DO:
                        ASSIGN output-list.gstid = ENTRY(loopi + 1, l-lieferant.plz, "#").
                        LEAVE.
                  END.                   
              END.
          END.
      END.

      IF NUM-ENTRIES(l-kredit.bemerk, ";") = 3 THEN DO:
              ASSIGN 
                  t-amt                  = DECIMAL(ENTRY(3, l-kredit.bemerk, ";" ))
                  output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                  t-tax                  = t-tax   + t-amt
                  tot-tax                = tot-tax + t-amt
                     
                  tamt                = l-kredit.netto - t-amt
                  output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                  t-inv               = t-inv + tamt
                  tot-amt             = tot-amt + tamt.

      END.
      ELSE DO:
          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = output-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                    = l-kredit.netto * taxcode-list.taxamount
                     t-amt                  = l-kredit.netto * taxcode-list.taxamount
                     output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                     t-tax                  = t-tax   + (l-kredit.netto * taxcode-list.taxamount)
                     tot-tax                = tot-tax + (l-kredit.netto * taxcode-list.taxamount) 
                     
                     tamt                = l-kredit.netto - t-amt
                     output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                     t-inv               = t-inv + (l-kredit.netto - t-amt)
                     tot-amt             = tot-amt + (l-kredit.netto - t-amt).
          END.
      END.
      /*end*/

      IF l-kredit.opart = 2 THEN output-list.paid = "Yes". 
      ELSE output-list.paid = "No". 
      t-debit = t-debit + l-kredit.netto. 
      tot-debit = tot-debit + l-kredit.netto. 
    END.
  END.
 
/* CREATE output-list. */ 
  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = "T O T A L"
      output-list.amount     = STRING(t-debit, "->>>,>>>,>>>,>>9.99").
      output-list.tax-amount = STRING(t-tax, "->>>,>>>,>>>,>>9.99" ).
      output-list.tot-amt    = STRING(t-inv, "->>>,>>>,>>>,>>9.99" ).
 
  CREATE output-list. 

  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = output-list.str + "Grand TOTAL" 
      output-list.amount     = STRING(tot-debit, "->>>,>>>,>>>,>>9.99")
      output-list.tax-amount = STRING(tot-tax, "->>>,>>>,>>>,>>9.99" )
      output-list.tot-amt    = STRING(tot-amt, "->>>,>>>,>>>,>>9.99" ).
END. 
 
PROCEDURE create-Dlist0B: 
DEFINE VARIABLE t-debit     AS DECIMAL. 
DEFINE VARIABLE tot-debit   AS DECIMAL. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE due-date    AS DATE. 
DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)" INITIAL "". 
DEFINE VARIABLE code1       AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE code2       AS INTEGER INITIAL 1 NO-UNDO.
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
DEFINE VARIABLE loopi       AS INTEGER NO-UNDO.
DEFINE VARIABLE amt         AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-tax       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv       AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-tax     AS DECIMAL. 
DEFINE VARIABLE tot-amt     AS DECIMAL.
DEFINE VARIABLE t-amt       AS DECIMAL.
DEFINE VARIABLE tamt        AS DECIMAL.
  
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  
  ASSIGN
    t-debit   = 0 
    tot-debit = 0
    amt       = 0 
    t-tax     = 0 
    t-inv     = 0
    tot-tax   = 0
    tot-amt   = 0
    t-amt     = 0
    tamt      = 0.

  IF excl-apmanual THEN ASSIGN code2 = 0.

  FOR EACH l-kredit WHERE (l-kredit.rgdatum + l-kredit.ziel) GE from-date 
    AND (l-kredit.rgdatum + l-kredit.ziel) LE to-date 
    AND l-kredit.zahlkonto = 0 
    AND l-kredit.lief-nr = from-lief AND l-kredit.opart = 0 
    AND l-kredit.steuercode GE code1 AND l-kredit.steuercode LE code2 
    NO-LOCK USE-INDEX liefnr_ix, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
    BY l-lieferant.firma BY (l-kredit.rgdatum + l-kredit.ziel) BY l-kredit.name: 
    
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    IF only-apmanual AND l-kredit.steuercode = 1 THEN do-it = YES.
    ELSE IF only-apmanual AND l-kredit.steuercode = 0 THEN do-it = NO.

    IF do-it THEN
    DO:
      IF receiver NE l-lieferant.firma THEN 
      DO: 
        IF receiver NE "" THEN 
        DO: 
/*      CREATE output-list. */ 
          CREATE output-list. 
          ASSIGN
              output-list.lscheinnr = "T O T A L" 
              output-list.amount    = STRING(t-debit, "->>>,>>>,>>>,>>9.99"). 
          CREATE output-list.
          t-debit = 0. 
        END. 
      END. 
      receiver = l-lieferant.firma. 
      due-date = l-kredit.rgdatum + l-kredit.ziel. 
      CREATE output-list. 
      ASSIGN
          output-list.ap-recid  = RECID(l-kredit)
          output-list.datum     = STRING(l-kredit.rgdatum) 
          output-list.lief      = receiver
          output-list.NAME      = l-kredit.name
          output-list.amount    = STRING(l-kredit.netto, "->>>,>>>,>>>,>>9.99")
          output-list.docu-nr   = l-kredit.lscheinnr
          output-list.lscheinnr = l-kredit.lscheinnr.

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.id = STRING(bediener.userinit,"x(2)"). 
      ELSE output-list.id = "  ". 
      output-list.due-date = STRING(due-date).

      /*ITA 260916*/
      IF NUM-ENTRIES(l-kredit.bemerk, ";") GT 1 THEN 
          ASSIGN output-list.remark = ENTRY(1, l-kredit.bemerk, ";" )
                 output-list.tax-code = STRING(ENTRY(2, l-kredit.bemerk, ";" ), "x(10)").
      ELSE output-list.remark = l-kredit.bemerk.
      
      IF l-lieferant.plz NE " " THEN DO:
          IF l-lieferant.plz MATCHES "*#*" THEN DO:
              DO loopi = 1 TO NUM-ENTRIES(l-lieferant.plz,"#"):
                  IF ENTRY(loopi + 1, l-lieferant.plz, "#") NE " "  THEN DO:
                        ASSIGN output-list.gstid = ENTRY(loopi + 1, l-lieferant.plz, "#").
                        LEAVE.
                  END.                   
              END.
          END.
      END.

      IF NUM-ENTRIES(l-kredit.bemerk, ";") = 3 THEN DO:
              ASSIGN 
                  t-amt                  = DECIMAL(ENTRY(3, l-kredit.bemerk, ";" ))
                  output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                  t-tax                  = t-tax   + t-amt
                  tot-tax                = tot-tax + t-amt
                     
                  tamt                = l-kredit.netto - t-amt
                  output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                  t-inv               = t-inv + tamt
                  tot-amt             = tot-amt + tamt.

      END.
      ELSE DO:
          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = output-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                    = l-kredit.netto * taxcode-list.taxamount
                     t-amt                  = l-kredit.netto * taxcode-list.taxamount
                     output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                     t-tax                  = t-tax   + (l-kredit.netto * taxcode-list.taxamount)
                     tot-tax                = tot-tax + (l-kredit.netto * taxcode-list.taxamount) 
                     
                     tamt                = l-kredit.netto - t-amt
                     output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                     t-inv               = t-inv + (l-kredit.netto - t-amt)
                     tot-amt             = tot-amt + (l-kredit.netto - t-amt).
          END.
      END.
      /*end*/

      IF l-kredit.opart = 2 THEN output-list.paid = "Yes". 
      ELSE output-list.paid = "No". 
      t-debit = t-debit + l-kredit.netto. 
      tot-debit = tot-debit + l-kredit.netto. 
    END.
  END.
 
/* CREATE output-list. */ 
  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = "T O T A L"
      output-list.amount     = STRING(t-debit, "->>>,>>>,>>>,>>9.99").
      output-list.tax-amount = STRING(t-tax, "->>>,>>>,>>>,>>9.99" ).
      output-list.tot-amt    = STRING(t-inv, "->>>,>>>,>>>,>>9.99" ).
 
  CREATE output-list. 

  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = output-list.str + "Grand TOTAL" 
      output-list.amount     = STRING(tot-debit, "->>>,>>>,>>>,>>9.99")
      output-list.tax-amount = STRING(tot-tax, "->>>,>>>,>>>,>>9.99" )
      output-list.tot-amt    = STRING(tot-amt, "->>>,>>>,>>>,>>9.99" ).
END. 

PROCEDURE create-listA: 
DEFINE VARIABLE t-debit     AS DECIMAL. 
DEFINE VARIABLE tot-debit   AS DECIMAL. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE due-date    AS DATE. 
DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)" INITIAL "". 
DEFINE VARIABLE code1       AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE code2       AS INTEGER INITIAL 1 NO-UNDO.
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
DEFINE VARIABLE loopi       AS INTEGER NO-UNDO.
DEFINE VARIABLE amt         AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-tax       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv       AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-tax     AS DECIMAL. 
DEFINE VARIABLE tot-amt     AS DECIMAL.
DEFINE VARIABLE t-amt       AS DECIMAL.
DEFINE VARIABLE tamt        AS DECIMAL.
  
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  
  ASSIGN
    t-debit   = 0 
    tot-debit = 0
    amt       = 0 
    t-tax     = 0 
    t-inv     = 0
    t-amt     = 0
    tamt      = 0.

  IF excl-apmanual THEN ASSIGN code2 = 0.

  FOR EACH l-lieferant WHERE l-lieferant.firma GE from-supp 
    AND l-lieferant.firma LE to-supp NO-LOCK, 
    EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto = 0 
    AND l-kredit.lief-nr = l-lieferant.lief-nr 
    AND l-kredit.steuercode GE code1 AND l-kredit.steuercode LE code2 
    NO-LOCK USE-INDEX liefnr_ix 
    BY l-lieferant.firma: 

    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    IF only-apmanual AND l-kredit.steuercode = 1 THEN do-it = YES.
    ELSE IF only-apmanual AND l-kredit.steuercode = 0 THEN do-it = NO.

    IF do-it THEN
    DO:
      IF receiver NE l-lieferant.firma THEN 
      DO: 
        IF receiver NE "" THEN 
        DO: 
/*      CREATE output-list. */ 
          CREATE output-list. 
          ASSIGN
              output-list.lscheinnr = "T O T A L" 
              output-list.amount    = STRING(t-debit, "->>>,>>>,>>>,>>9.99"). 
          CREATE output-list. 
          t-debit = 0. 
        END. 
      END. 
      receiver = l-lieferant.firma. 
      due-date = l-kredit.rgdatum + l-kredit.ziel. 
      CREATE output-list. 
      ASSIGN
          output-list.ap-recid  = RECID(l-kredit)
          output-list.datum     = STRING(l-kredit.rgdatum) 
          output-list.lief      = receiver
          output-list.NAME      = l-kredit.name
          output-list.amount    = STRING(l-kredit.netto, "->>>,>>>,>>>,>>9.99")
          output-list.docu-nr   = l-kredit.lscheinnr
          output-list.lscheinnr = l-kredit.lscheinnr.

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN
          output-list.id = STRING(bediener.userinit,"x(2)"). 
      ELSE output-list.id = "  ". 
      output-list.due-date = STRING(due-date).  
      

 /*ITA 260916*/
      IF NUM-ENTRIES(l-kredit.bemerk, ";") GT 1 THEN 
          ASSIGN output-list.str = output-list.str + STRING(ENTRY(1, l-kredit.bemerk, ";" ), "x(30)")
                 output-list.tax-code = STRING(ENTRY(2, l-kredit.bemerk, ";" ), "x(10)").
      ELSE output-list.str = output-list.str + STRING(l-kredit.bemerk, "x(30)").
      
      IF l-lieferant.plz NE " " THEN DO:
          IF l-lieferant.plz MATCHES "*#*" THEN DO:
              DO loopi = 1 TO NUM-ENTRIES(l-lieferant.plz,"#"):
                  IF ENTRY(loopi + 1, l-lieferant.plz, "#") NE " "  THEN DO:
                        ASSIGN output-list.gstid = ENTRY(loopi + 1, l-lieferant.plz, "#").
                        LEAVE.
                  END.                   
              END.
          END.
      END.

      IF NUM-ENTRIES(l-kredit.bemerk, ";") = 3 THEN DO:
              ASSIGN 
                  t-amt                  = DECIMAL(ENTRY(3, l-kredit.bemerk, ";" ))
                  output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                  t-tax                  = t-tax   + t-amt
                  tot-tax                = tot-tax + t-amt
                     
                  tamt                = l-kredit.netto - t-amt
                  output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                  t-inv               = t-inv + tamt
                  tot-amt             = tot-amt + tamt.

      END.
      ELSE DO:
          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = output-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                    = l-kredit.netto * taxcode-list.taxamount
                     t-amt                  = l-kredit.netto * taxcode-list.taxamount
                     output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                     t-tax                  = t-tax   + (l-kredit.netto * taxcode-list.taxamount)
                     tot-tax                = tot-tax + (l-kredit.netto * taxcode-list.taxamount) 
                     
                     tamt                = l-kredit.netto - t-amt
                     output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                     t-inv               = t-inv + (l-kredit.netto - t-amt)
                     tot-amt             = tot-amt + (l-kredit.netto - t-amt).
          END.
      END.
     /*end*/

      IF l-kredit.opart = 2 THEN output-list.paid = "Yes". 
      ELSE output-list.paid = "No". 
      t-debit = t-debit + l-kredit.netto. 
      tot-debit = tot-debit + l-kredit.netto. 
    END.
  END.
 
/* CREATE output-list. */ 
  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = "T O T A L"
      output-list.amount     = STRING(t-debit, "->>>,>>>,>>>,>>9.99").
      output-list.tax-amount = STRING(t-tax, "->>>,>>>,>>>,>>9.99" ).
      output-list.tot-amt    = STRING(t-inv, "->>>,>>>,>>>,>>9.99" ).
 
  CREATE output-list. 

  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = output-list.str + "Grand TOTAL" 
      output-list.amount     = STRING(tot-debit, "->>>,>>>,>>>,>>9.99")
      output-list.tax-amount = STRING(tot-tax, "->>>,>>>,>>>,>>9.99" )
      output-list.tot-amt    = STRING(tot-amt, "->>>,>>>,>>>,>>9.99" ).
END. 
 
PROCEDURE create-DlistA: 
DEFINE VARIABLE t-debit     AS DECIMAL. 
DEFINE VARIABLE tot-debit   AS DECIMAL. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE due-date    AS DATE. 
DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)" INITIAL "". 
DEFINE VARIABLE code1       AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE code2       AS INTEGER INITIAL 1 NO-UNDO.
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
DEFINE VARIABLE loopi       AS INTEGER NO-UNDO.
DEFINE VARIABLE amt         AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-tax       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv       AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-tax     AS DECIMAL. 
DEFINE VARIABLE tot-amt     AS DECIMAL.
DEFINE VARIABLE t-amt       AS DECIMAL.
DEFINE VARIABLE tamt        AS DECIMAL.
  
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  
  ASSIGN
    t-debit   = 0 
    tot-debit = 0
    amt       = 0 
    t-tax     = 0 
    t-inv     = 0
    tot-tax   = 0
    tot-amt   = 0
    t-amt     = 0
    tamt      = 0.

  IF excl-apmanual THEN ASSIGN code2 = 0.

  FOR EACH l-lieferant WHERE l-lieferant.firma GE from-supp 
    AND l-lieferant.firma LE to-supp NO-LOCK, 
    EACH l-kredit WHERE (l-kredit.rgdatum + l-kredit.ziel) GE from-date 
    AND (l-kredit.rgdatum + l-kredit.ziel) LE to-date 
    AND l-kredit.zahlkonto = 0 
    AND l-kredit.lief-nr = l-lieferant.lief-nr 
    AND l-kredit.steuercode GE code1 AND l-kredit.steuercode LE code2 
    NO-LOCK USE-INDEX liefnr_ix 
    BY l-lieferant.firma BY (l-kredit.rgdatum + l-kredit.ziel): 
    
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    IF only-apmanual AND l-kredit.steuercode = 1 THEN do-it = YES.
    ELSE IF only-apmanual AND l-kredit.steuercode = 0 THEN do-it = NO.

    IF do-it THEN
    DO:
      IF receiver NE l-lieferant.firma THEN 
      DO: 
        IF receiver NE "" THEN 
        DO: 
/*      CREATE output-list. */ 
          CREATE output-list. 
          ASSIGN
              output-list.lscheinnr = "T O T A L" 
              output-list.amount    = STRING(t-debit, "->>>,>>>,>>>,>>9.99"). 
          CREATE output-list.  
          t-debit = 0. 
        END. 
      END. 
      receiver = l-lieferant.firma. 
      due-date = l-kredit.rgdatum + l-kredit.ziel. 
      CREATE output-list. 
      ASSIGN
          output-list.ap-recid  = RECID(l-kredit)
          output-list.datum     = STRING(l-kredit.rgdatum) 
          output-list.lief      = receiver
          output-list.NAME      = l-kredit.name
          output-list.amount    = STRING(l-kredit.netto, "->>>,>>>,>>>,>>9.99")
          output-list.docu-nr   = l-kredit.lscheinnr
          output-list.lscheinnr = l-kredit.lscheinnr.

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.id = STRING(bediener.userinit,"x(2)"). 
      ELSE output-list.id = "  ". 
      output-list.due-date = STRING(due-date).

      /*ITA 260916*/
      IF NUM-ENTRIES(l-kredit.bemerk, ";") GT 1 THEN 
          ASSIGN output-list.remark = ENTRY(1, l-kredit.bemerk, ";" )
                 output-list.tax-code = STRING(ENTRY(2, l-kredit.bemerk, ";" ), "x(10)").
      ELSE output-list.remark = l-kredit.bemerk.
      
      IF l-lieferant.plz NE " " THEN DO:
          IF l-lieferant.plz MATCHES "*#*" THEN DO:
              DO loopi = 1 TO NUM-ENTRIES(l-lieferant.plz,"#"):
                  IF ENTRY(loopi + 1, l-lieferant.plz, "#") NE " "  THEN DO:
                        ASSIGN output-list.gstid = ENTRY(loopi + 1, l-lieferant.plz, "#").
                        LEAVE.
                  END.                   
              END.
          END.
      END.

      IF NUM-ENTRIES(l-kredit.bemerk, ";") = 3 THEN DO:
              ASSIGN 
                  t-amt                  = DECIMAL(ENTRY(3, l-kredit.bemerk, ";" ))
                  output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                  t-tax                  = t-tax   + t-amt
                  tot-tax                = tot-tax + t-amt
                     
                  tamt                = l-kredit.netto - t-amt
                  output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                  t-inv               = t-inv + tamt
                  tot-amt             = tot-amt + tamt.

      END.
      ELSE DO:
          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = output-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                    = l-kredit.netto * taxcode-list.taxamount
                     t-amt                  = l-kredit.netto * taxcode-list.taxamount
                     output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                     t-tax                  = t-tax   + (l-kredit.netto * taxcode-list.taxamount)
                     tot-tax                = tot-tax + (l-kredit.netto * taxcode-list.taxamount) 
                     
                     tamt                = l-kredit.netto - t-amt
                     output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                     t-inv               = t-inv + (l-kredit.netto - t-amt)
                     tot-amt             = tot-amt + (l-kredit.netto - t-amt).
          END.
      END.
      /*end*/

      IF l-kredit.opart = 2 THEN output-list.paid = "Yes". 
      ELSE output-list.paid = "No". 
      t-debit = t-debit + l-kredit.netto. 
      tot-debit = tot-debit + l-kredit.netto. 
    END.
  END.
 
/* CREATE output-list. */ 
 CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = "T O T A L"
      output-list.amount     = STRING(t-debit, "->>>,>>>,>>>,>>9.99").
      output-list.tax-amount = STRING(t-tax, "->>>,>>>,>>>,>>9.99" ).
      output-list.tot-amt    = STRING(t-inv, "->>>,>>>,>>>,>>9.99" ).
 
  CREATE output-list. 

  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = output-list.str + "Grand TOTAL" 
      output-list.amount     = STRING(tot-debit, "->>>,>>>,>>>,>>9.99")
      output-list.tax-amount = STRING(tot-tax, "->>>,>>>,>>>,>>9.99" )
      output-list.tot-amt    = STRING(tot-amt, "->>>,>>>,>>>,>>9.99" ).
END. 
 
PROCEDURE create-listB: 
DEFINE VARIABLE t-debit     AS DECIMAL. 
DEFINE VARIABLE tot-debit   AS DECIMAL. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE due-date    AS DATE. 
DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)" INITIAL "". 
DEFINE VARIABLE code1       AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE code2       AS INTEGER INITIAL 1 NO-UNDO.
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
DEFINE VARIABLE loopi       AS INTEGER NO-UNDO.
DEFINE VARIABLE amt         AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-tax       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv       AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-tax     AS DECIMAL. 
DEFINE VARIABLE tot-amt     AS DECIMAL.
DEFINE VARIABLE t-amt       AS DECIMAL.
DEFINE VARIABLE tamt        AS DECIMAL.
  
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  
  ASSIGN
    t-debit   = 0 
    tot-debit = 0
    amt       = 0 
    t-tax     = 0 
    t-inv     = 0
    tot-tax   = 0
    tot-amt   = 0
    t-amt     = 0
    tamt      = 0.

  IF excl-apmanual THEN ASSIGN code2 = 0.

  FOR EACH l-lieferant WHERE l-lieferant.firma GE from-supp 
    AND l-lieferant.firma LE to-supp NO-LOCK, 
    EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto = 0 
    AND l-kredit.lief-nr = l-lieferant.lief-nr AND l-kredit.opart = 0 
    AND l-kredit.steuercode GE code1 AND l-kredit.steuercode LE code2 
    NO-LOCK USE-INDEX liefnr_ix 
    BY l-lieferant.firma: 
    
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    IF only-apmanual AND l-kredit.steuercode = 1 THEN do-it = YES.
    ELSE IF only-apmanual AND l-kredit.steuercode = 0 THEN do-it = NO.

    IF do-it THEN
    DO:
      IF receiver NE l-lieferant.firma THEN 
      DO: 
        IF receiver NE "" THEN 
        DO: 
/*      CREATE output-list. */ 
          CREATE output-list. 
          ASSIGN
              output-list.lscheinnr = "T O T A L" 
              output-list.amount    = STRING(t-debit, "->>>,>>>,>>>,>>9.99"). 
          CREATE output-list. 
          t-debit = 0. 
        END. 
      END. 
      receiver = l-lieferant.firma. 
      due-date = l-kredit.rgdatum + l-kredit.ziel. 
      CREATE output-list. 
      ASSIGN
          output-list.ap-recid  = RECID(l-kredit)
          output-list.datum     = STRING(l-kredit.rgdatum) 
          output-list.lief      = receiver
          output-list.NAME      = l-kredit.name
          output-list.amount    = STRING(l-kredit.netto, "->>>,>>>,>>>,>>9.99")
          output-list.docu-nr   = l-kredit.lscheinnr
          output-list.lscheinnr = l-kredit.lscheinnr.

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.id = STRING(bediener.userinit,"x(2)"). 
      ELSE output-list.id = "  ". 
      output-list.due-date = STRING(due-date). 

      /*ITA 260916*/
      IF NUM-ENTRIES(l-kredit.bemerk, ";") GT 1 THEN 
          ASSIGN output-list.remark = ENTRY(1, l-kredit.bemerk, ";" )
                 output-list.tax-code = STRING(ENTRY(2, l-kredit.bemerk, ";" ), "x(10)").
      ELSE output-list.remark = l-kredit.bemerk.
      
      IF l-lieferant.plz NE " " THEN DO:
          IF l-lieferant.plz MATCHES "*#*" THEN DO:
              DO loopi = 1 TO NUM-ENTRIES(l-lieferant.plz,"#"):
                  IF ENTRY(loopi + 1, l-lieferant.plz, "#") NE " "  THEN DO:
                        ASSIGN output-list.gstid = ENTRY(loopi + 1, l-lieferant.plz, "#").
                        LEAVE.
                  END.                   
              END.
          END.
      END.

     IF NUM-ENTRIES(l-kredit.bemerk, ";") = 3 THEN DO:
              ASSIGN 
                  t-amt                  = DECIMAL(ENTRY(3, l-kredit.bemerk, ";" ))
                  output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                  t-tax                  = t-tax   + t-amt
                  tot-tax                = tot-tax + t-amt
                     
                  tamt                = l-kredit.netto - t-amt
                  output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                  t-inv               = t-inv + tamt
                  tot-amt             = tot-amt + tamt.

      END.
      ELSE DO:
          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = output-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                    = l-kredit.netto * taxcode-list.taxamount
                     t-amt                  = l-kredit.netto * taxcode-list.taxamount
                     output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                     t-tax                  = t-tax   + (l-kredit.netto * taxcode-list.taxamount)
                     tot-tax                = tot-tax + (l-kredit.netto * taxcode-list.taxamount) 
                     
                     tamt                = l-kredit.netto - t-amt
                     output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                     t-inv               = t-inv + (l-kredit.netto - t-amt)
                     tot-amt             = tot-amt + (l-kredit.netto - t-amt).
          END.
      END.
      /*end*/

      IF l-kredit.opart = 2 THEN output-list.paid = "Yes". 
      ELSE output-list.paid = "No". 
      t-debit = t-debit + l-kredit.netto. 
      tot-debit = tot-debit + l-kredit.netto. 
    END. 
  END.

/* CREATE output-list. */ 
  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = "T O T A L"
      output-list.amount     = STRING(t-debit, "->>>,>>>,>>>,>>9.99").
      output-list.tax-amount = STRING(t-tax, "->>>,>>>,>>>,>>9.99" ).
      output-list.tot-amt    = STRING(t-inv, "->>>,>>>,>>>,>>9.99" ).
 
  CREATE output-list. 

  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = output-list.str + "Grand TOTAL" 
      output-list.amount     = STRING(tot-debit, "->>>,>>>,>>>,>>9.99")
      output-list.tax-amount = STRING(tot-tax, "->>>,>>>,>>>,>>9.99" )
      output-list.tot-amt    = STRING(tot-amt, "->>>,>>>,>>>,>>9.99" ).
END. 
 
PROCEDURE create-DlistB:
DEFINE VARIABLE t-debit     AS DECIMAL. 
DEFINE VARIABLE tot-debit   AS DECIMAL. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE due-date    AS DATE. 
DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)" INITIAL "". 
DEFINE VARIABLE code1       AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE code2       AS INTEGER INITIAL 1 NO-UNDO.
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
DEFINE VARIABLE loopi       AS INTEGER NO-UNDO.
DEFINE VARIABLE amt         AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-tax       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv       AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-tax     AS DECIMAL. 
DEFINE VARIABLE tot-amt     AS DECIMAL.
DEFINE VARIABLE t-amt       AS DECIMAL.
DEFINE VARIABLE tamt        AS DECIMAL.
  
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  
  ASSIGN
    t-debit   = 0 
    tot-debit = 0
    amt       = 0 
    t-tax     = 0 
    t-inv     = 0
    tot-tax   = 0
    tot-amt   = 0
    t-amt     = 0
    tamt      = 0.

  IF excl-apmanual THEN ASSIGN code2 = 0.

  FOR EACH l-lieferant WHERE l-lieferant.firma GE from-supp 
    AND l-lieferant.firma LE to-supp NO-LOCK, 
    EACH l-kredit WHERE (l-kredit.rgdatum + l-kredit.ziel) GE from-date 
    AND (l-kredit.rgdatum + l-kredit.ziel) LE to-date 
    AND l-kredit.zahlkonto = 0 
    AND l-kredit.lief-nr = l-lieferant.lief-nr AND l-kredit.opart = 0 
    AND l-kredit.steuercode GE code1 AND l-kredit.steuercode LE code2 
    NO-LOCK USE-INDEX liefnr_ix 
    BY l-lieferant.firma BY (l-kredit.rgdatum + l-kredit.ziel): 
    
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    IF only-apmanual AND l-kredit.steuercode = 1 THEN do-it = YES.
    ELSE IF only-apmanual AND l-kredit.steuercode = 0 THEN do-it = NO.

    IF do-it THEN
    DO:
      IF receiver NE l-lieferant.firma THEN 
      DO: 
        IF receiver NE "" THEN 
        DO: 
/*      CREATE output-list. */ 
          CREATE output-list. 
          ASSIGN
              output-list.lscheinnr = "T O T A L" 
              output-list.amount    = STRING(t-debit, "->>>,>>>,>>>,>>9.99").  
          CREATE output-list. 
          t-debit = 0. 
        END. 
      END. 
      receiver = l-lieferant.firma. 
      due-date = l-kredit.rgdatum + l-kredit.ziel. 
      CREATE output-list. 
      ASSIGN
          output-list.ap-recid  = RECID(l-kredit)
          output-list.datum     = STRING(l-kredit.rgdatum) 
          output-list.lief      = receiver
          output-list.NAME      = l-kredit.name
          output-list.amount    = STRING(l-kredit.netto, "->>>,>>>,>>>,>>9.99")
          output-list.docu-nr   = l-kredit.lscheinnr
          output-list.lscheinnr = l-kredit.lscheinnr.
      
      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.id = STRING(bediener.userinit,"x(2)"). 
      ELSE output-list.id = "  ". 
      output-list.due-date = STRING(due-date).

      /*ITA 260916*/
      IF NUM-ENTRIES(l-kredit.bemerk, ";") GT 1 THEN 
          ASSIGN output-list.remark = ENTRY(1, l-kredit.bemerk, ";" )
                 output-list.tax-code = STRING(ENTRY(2, l-kredit.bemerk, ";" ), "x(10)").
      ELSE output-list.remark = l-kredit.bemerk.
      
      IF l-lieferant.plz NE " " THEN DO:
          IF l-lieferant.plz MATCHES "*#*" THEN DO:
              DO loopi = 1 TO NUM-ENTRIES(l-lieferant.plz,"#"):
                  IF ENTRY(loopi + 1, l-lieferant.plz, "#") NE " "  THEN DO:
                        ASSIGN output-list.gstid = ENTRY(loopi + 1, l-lieferant.plz, "#").
                        LEAVE.
                  END.                   
              END.
          END.
      END.

      IF NUM-ENTRIES(l-kredit.bemerk, ";") = 3 THEN DO:
              ASSIGN 
                  t-amt                  = DECIMAL(ENTRY(3, l-kredit.bemerk, ";" ))
                  output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                  t-tax                  = t-tax   + t-amt
                  tot-tax                = tot-tax + t-amt
                     
                  tamt                = l-kredit.netto - t-amt
                  output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                  t-inv               = t-inv + tamt
                  tot-amt             = tot-amt + tamt.

      END.
      ELSE DO:
          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = output-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                    = l-kredit.netto * taxcode-list.taxamount
                     t-amt                  = l-kredit.netto * taxcode-list.taxamount
                     output-list.tax-amount = STRING(t-amt, "->>>,>>>,>>>,>>9.99" )
                     t-tax                  = t-tax   + (l-kredit.netto * taxcode-list.taxamount)
                     tot-tax                = tot-tax + (l-kredit.netto * taxcode-list.taxamount) 
                     
                     tamt                = l-kredit.netto - t-amt
                     output-list.tot-amt = STRING(tamt, "->>>,>>>,>>>,>>9.99" ) 
                     t-inv               = t-inv + (l-kredit.netto - t-amt)
                     tot-amt             = tot-amt + (l-kredit.netto - t-amt).
          END.
      END.
      /*end*/

      IF l-kredit.opart = 2 THEN output-list.paid = "Yes". 
      ELSE output-list.paid = "No". 
      t-debit = t-debit + l-kredit.netto. 
      tot-debit = tot-debit + l-kredit.netto. 
    END.
  END.
 
/* CREATE output-list. */ 
  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = "T O T A L"
      output-list.amount     = STRING(t-debit, "->>>,>>>,>>>,>>9.99").
      output-list.tax-amount = STRING(t-tax, "->>>,>>>,>>>,>>9.99" ).
      output-list.tot-amt    = STRING(t-inv, "->>>,>>>,>>>,>>9.99" ).
 
  CREATE output-list. 

  CREATE output-list. 
  ASSIGN
      output-list.lscheinnr  = output-list.str + "Grand TOTAL" 
      output-list.amount     = STRING(tot-debit, "->>>,>>>,>>>,>>9.99")
      output-list.tax-amount = STRING(tot-tax, "->>>,>>>,>>>,>>9.99" )
      output-list.tot-amt    = STRING(tot-amt, "->>>,>>>,>>>,>>9.99" ).
END. 

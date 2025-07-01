/*ITA 160215 --> detail for sorting by COA*/

DEFINE TEMP-TABLE lagerBuff LIKE fa-lager.
DEFINE TEMP-TABLE str-list
  FIELD flag        AS INTEGER 
  FIELD refno       AS CHAR FORMAT "x(14)" LABEL "Reference-No" 
  FIELD location    AS CHAR FORMAT "x(16)" LABEL "Location" 
  FIELD s           AS CHAR FORMAT "x(200)". 

DEFINE INPUT PARAMETER pvILanguage          AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR lagerBuff.
DEFINE INPUT PARAMETER mi-lager-chk         AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER mi-subgrp-chk        AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER mi-acct-chk          AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER mi-bookvalue-chk     AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER from-grp             AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER from-date            AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER to-lager             AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER from-lager           AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER maxNr                AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER to-date              AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER zero-value-only      AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER last-acctdate        AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER yy                   AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER mm                   AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER from-subgr           AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER to-subgr             AS INTEGER  NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR str-list.

DEFINE VARIABLE do-it       AS LOGICAL INITIAL NO.
DEFINE VARIABLE sub-depn    AS INTEGER NO-UNDO.
DEFINE VARIABLE val-dep     AS DECIMAL NO-UNDO.
DEFINE VARIABLE datum       AS DATE    NO-UNDO.
DEFINE VARIABLE flag        AS LOGICAL NO-UNDO.

DEFINE VARIABLE p-depn-wert AS DECIMAL NO-UNDO.
DEFINE VARIABLE p-book-wert AS DECIMAL NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fa-valuate".

IF mi-lager-chk = YES THEN 
DO: 
    IF from-grp = 0 THEN 
    DO: 
      IF from-date = ? THEN RUN create-list. 
      ELSE RUN create-list0. 
    END. 
    ELSE 
    DO: 
      IF from-date = ? THEN RUN create-list1. 
      ELSE RUN create-list11. 
    END. 
END. 
ELSE IF mi-subgrp-chk = YES THEN 
DO: 
    RUN create-listsgrp. 
END. 
ELSE IF mi-acct-chk = YES THEN 
DO: 
    RUN create-listacct.  
END. 

PROCEDURE create-list:  /* all FA-Group */ 
    
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE t-anz      AS DECIMAL. 
DEFINE VARIABLE t-val      AS DECIMAL. 
DEFINE VARIABLE t-val1     AS DECIMAL. 
DEFINE VARIABLE t-val2     AS DECIMAL. 
DEFINE VARIABLE tt-anz     AS DECIMAL. 
DEFINE VARIABLE tt-val     AS DECIMAL. 
DEFINE VARIABLE tt-val1    AS DECIMAL. 
DEFINE VARIABLE tt-val2    AS DECIMAL. 
DEFINE VARIABLE tot-anz    AS DECIMAL. 
DEFINE VARIABLE tot-val    AS DECIMAL. 
DEFINE VARIABLE tot-val1   AS DECIMAL. 
DEFINE VARIABLE tot-val2   AS DECIMAL. 
DEFINE VARIABLE zwkum AS INTEGER. 
DEFINE VARIABLE bezeich AS CHAR. 
 
DEFINE BUFFER l-oh   FOR mathis. 
DEFINE VARIABLE qty  AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 

DEFINE VARIABLE max-lager AS INTEGER NO-UNDO.

  STATUS DEFAULT "Processing...". 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
 
  ASSIGN
    tot-anz  = 0 
    tot-val  = 0 
    tot-val1 = 0 
    tot-val2 = 0
  .
  max-lager = to-lager.
  IF from-lager NE to-lager AND (maxNr - 1) = to-lager THEN max-lager = maxNr.
  FOR EACH lagerBuff WHERE lagerBuff.lager-nr GE from-lager 
    AND lagerBuff.lager-nr LE maxNr: 
    i = 0. 
    zwkum = 0. 
    t-anz = 0. 
    t-val = 0. 
    t-val1 = 0. 
    t-val2 = 0. 
    tt-anz = 0. 
    tt-val = 0. 
    tt-val1 = 0. 
    tt-val2 = 0. 
    create str-list. 
    create str-list. 
    str-list.s = STRING(lagerBuff.lager-nr, ">>99") 
      + "-" + STRING(lagerBuff.bezeich, "x(56)"). /*naufal afthar - 1C4A52*/
    
     /*ITA 110315*/
    IF mi-bookvalue-chk = YES THEN DO:
        FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich
          AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
          FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr NO-LOCK, 
          FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.gnr 
            AND fa-grup.flag = 0 NO-LOCK BY fa-grup.gnr BY mathis.name: 
    
            do-it = NO.
            IF NOT zero-value-only THEN do-it = YES.
            ELSE do-it = fa-artikel.book-wert = 0.
    
          IF do-it THEN
          DO:
              IF zwkum NE fa-artikel.gnr THEN 
              DO: 
                IF zwkum NE 0 THEN 
                DO: 
                  create str-list. 
                  DO j = 1 TO 60: 
                    str-list.s = str-list.s + " ". 
                  END. 
    
                  ASSIGN
                    str-list.refno  = "SUB TOTAL" 
                /*    str-list.flag   = 1   */
                    str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
                  IF t-anz GT 99999 THEN
                    str-list.s = str-list.s + STRING(t-anz,">>>>>9").
                  ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
                  IF t-val GT 99999999999 OR t-val1 GT 99999999999
                      OR t-val2 GT 99999999999 THEN
                  str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
                  ELSE
                  str-list.s = str-list.s + STRING(t-val, ">>>,>>>,>>>,>>9.99") 
                    + STRING(t-val1, ">>>,>>>,>>>,>>9.99") 
                    + STRING(t-val2, ">>>,>>>,>>>,>>9.99"). 
                END. 
                
                CREATE str-list. 
                str-list.s = STRING(fa-grup.bezeich, "x(28)"). 
                ASSIGN
                  t-anz  = 0 
                  t-val  = 0 
                  t-val1 = 0 
                  t-val2 = 0 
                  zwkum  = fa-artikel.gnr
                . 
              END. 
              
              create str-list. 
              str-list.refno = mathis.asset. 
              str-list.s = STRING(mathis.name, "x(60)") /*naufal afthar - 1C4A52*/
                           + STRING(mathis.asset, "x(14)") 
                           + STRING(mathis.datum) 
                           + STRING(fa-artikel.anzahl,">>,>>9"). 

             
              ASSIGN val-dep     = fa-artikel.depn-wert / fa-artikel.anz-depn
                     sub-depn    = 0
                     flag        = NO.

              IF val-dep = ? THEN val-dep = 0.
              DO datum = from-date TO to-date:
                  IF flag AND datum = DATE(MONTH(datum) + 1, 1, YEAR(datum)) - 1 THEN 
                        ASSIGN sub-depn = sub-depn + 1.
                
                  IF datum = fa-artikel.first-depn THEN 
                      ASSIGN sub-depn    = sub-depn + 1
                             flag        = YES.

                  IF datum = fa-artikel.last-depn THEN LEAVE.
              END.


              ASSIGN p-depn-wert = val-dep * sub-depn
                     p-book-wert = fa-artikel.warenwert - p-depn-wert.

              i = i + 1. 

              /*SUB TOTAl*/
              t-anz = t-anz + fa-artikel.anzahl. 
              t-val = t-val + fa-artikel.warenwert. 
              t-val1 = t-val1 + p-depn-wert. 
              t-val2 = t-val2 + p-book-wert. 

              /*TOTAL*/
              tt-anz = tt-anz + fa-artikel.anzahl. 
              tt-val = tt-val + fa-artikel.warenwert. 
              tt-val1 = tt-val1 + p-depn-wert. 
              tt-val2 = tt-val2 + p-book-wert. 

              /*Grand TOTAL*/
              tot-anz = tot-anz + fa-artikel.anzahl. 
              tot-val = tot-val + fa-artikel.warenwert. 
              tot-val1 = tot-val1 + p-depn-wert. 
              tot-val2 = tot-val2 + p-book-wert. 


              str-list.s = str-list.s 
                     + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") 
                     + STRING(p-depn-wert, ">>>,>>>,>>>,>>9.99") 
                     + STRING(p-book-wert, ">>>,>>>,>>>,>>9.99"). 

              IF fa-artikel.first-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.first-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.next-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.next-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.last-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.last-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.anz-depn NE ? THEN 
                str-list.s = str-list.s + STRING(sub-depn). 
              ELSE str-list.s = str-list.s + "        ". 
          END.
        END.
    END. /*end ITA*/
    ELSE DO:
        FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich
          AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
          FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
          /*AND fa-artikel.loeschflag = 0*/ NO-LOCK, 
          FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.gnr 
            AND fa-grup.flag = 0 NO-LOCK BY fa-grup.gnr BY mathis.name: 
    
            do-it = NO.
            IF NOT zero-value-only THEN do-it = YES.
            ELSE do-it = fa-artikel.book-wert = 0.
    
          IF do-it THEN
          DO:
              IF zwkum NE fa-artikel.gnr THEN 
              DO: 
                IF zwkum NE 0 THEN 
                DO: 
                  create str-list. 
                  DO j = 1 TO 60: 
                    str-list.s = str-list.s + " ". 
                  END. 
    
                  ASSIGN
                    str-list.refno  = "SUB TOTAL" 
                /*    str-list.flag   = 1   */
                    str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
                  IF t-anz GT 99999 THEN
                    str-list.s = str-list.s + STRING(t-anz,">>>>>9").
                  ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
                  IF t-val GT 99999999999 OR t-val1 GT 99999999999
                      OR t-val2 GT 99999999999 THEN
                  str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
                  ELSE
                  str-list.s = str-list.s + STRING(t-val, ">>>,>>>,>>>,>>9.99") 
                    + STRING(t-val1, ">>>,>>>,>>>,>>9.99") 
                    + STRING(t-val2, ">>>,>>>,>>>,>>9.99"). 
                END. 
                
                CREATE str-list. 
                str-list.s = STRING(fa-grup.bezeich, "x(28)"). 
                ASSIGN
                  t-anz  = 0 
                  t-val  = 0 
                  t-val1 = 0 
                  t-val2 = 0 
                  zwkum  = fa-artikel.gnr
                . 
              END. 
              i = i + 1. 
              t-anz = t-anz + fa-artikel.anzahl. 
              t-val = t-val + fa-artikel.warenwert. 
              t-val1 = t-val1 + fa-artikel.depn-wert. 
              t-val2 = t-val2 + fa-artikel.book-wert. 
              tt-anz = tt-anz + fa-artikel.anzahl. 
              tt-val = tt-val + fa-artikel.warenwert. 
              tt-val1 = tt-val1 + fa-artikel.depn-wert. 
              tt-val2 = tt-val2 + fa-artikel.book-wert. 
              tot-anz = tot-anz + fa-artikel.anzahl. 
              tot-val = tot-val + fa-artikel.warenwert. 
              tot-val1 = tot-val1 + fa-artikel.depn-wert. 
              tot-val2 = tot-val2 + fa-artikel.book-wert. 
         
              create str-list. 
              str-list.refno = mathis.asset. 
              str-list.s = STRING(mathis.name, "x(60)") /*naufal afthar - 1C4A52*/
                     + STRING(mathis.asset, "x(14)") 
                     + STRING(mathis.datum) 
                     + STRING(fa-artikel.anzahl,">>,>>9"). 
              str-list.s = str-list.s 
                     + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") 
                     + STRING(fa-artikel.depn-wert, ">>>,>>>,>>>,>>9.99") 
                     + STRING(fa-artikel.book-wert, ">>>,>>>,>>>,>>9.99"). 
              IF fa-artikel.first-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.first-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.next-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.next-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.last-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.last-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.anz-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.anz-depn). 
              ELSE str-list.s = str-list.s + "        ". 
          END.
        END.
    END.
 
     
    IF t-anz NE 0 THEN 
    DO: 
      create str-list. 
      DO j = 1 TO 60: 
        str-list.s = str-list.s + " ". 
      END. 

      ASSIGN
        str-list.refno  = "SUB TOTAL" 
   /*   str-list.flag   = 1   */
        str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
      IF t-anz GT 99999 THEN
        str-list.s = str-list.s + STRING(t-anz,">>>>>9").
      ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
      IF t-val GT 99999999999 OR t-val1 GT 99999999999
          OR t-val2 GT 99999999999 THEN
      str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
        + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
        + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
      ELSE
      str-list.s = str-list.s + STRING(t-val, ">>>,>>>,>>>,>>9.99") 
        + STRING(t-val1, ">>>,>>>,>>>,>>9.99") 
        + STRING(t-val2, ">>>,>>>,>>>,>>9.99"). 

    END. 
    IF i GT 0 THEN 
    DO: 
      create str-list. 
      DO j = 1 TO 60: 
        str-list.s = str-list.s + " ". 
      END. 
    END. 
    str-list.refno = "T O T A L". 
    str-list.flag = 1. 
    IF LENGTH(TRIM(STRING(str-list.s))) NE 0 THEN str-list.s = str-list.s + STRING("T O T A L", "x(21)"). 
    ELSE str-list.s = str-list.s + STRING("T O T A L", "x(22)").  
    IF LENGTH(TRIM(STRING(tt-anz))) GT 5 THEN
        str-list.s = str-list.s + STRING(tt-anz,">>>>>9"). 
    ELSE str-list.s = str-list.s + STRING(tt-anz,">>,>>9"). 

    IF LENGTH(TRIM(STRING(tt-val, ">>>,>>>,>>>,>>9.99"))) GT 17 THEN
        str-list.s = str-list.s + STRING(tt-val, ">,>>>,>>>,>>>,>>9") .
    ELSE str-list.s = str-list.s + STRING(tt-val, ">>>,>>>,>>>,>>9.99") .
    str-list.s = str-list.s 
      + STRING(tt-val1, ">>>,>>>,>>>,>>9.99") 
      + STRING(tt-val2, ">>>,>>>,>>>,>>9.99"). 
  END. 
 
  IF from-lager NE to-lager AND tot-anz NE 0 THEN 
  DO: 
    create str-list. 
    create str-list. 
    DO j = 1 TO 60: 
      str-list.s = str-list.s + " ". 
    END. 

    ASSIGN
      str-list.flag  = 2 
      str-list.refno = "GRAND TOTAL".

    IF LENGTH(TRIM(STRING(str-list.s))) NE 0 THEN str-list.s     = str-list.s + STRING(" ", "x(21)"). 
    ELSE str-list.s     = str-list.s + STRING(" ", "x(22)").  

    IF LENGTH(TRIM(STRING(tot-anz))) GT 6 THEN
        str-list.s = str-list.s + STRING(tot-anz,">>>>>9"). 
    ELSE str-list.s = str-list.s + STRING(tot-anz,">>,>>9"). 

    IF tot-val GT 99999999999 OR tot-val1 GT 99999999999
      OR tot-val2 GT 99999999999 THEN
    str-list.s = str-list.s + STRING(tot-val, ">,>>>,>>>,>>>,>>9") 
      + STRING(tot-val1, ">,>>>,>>>,>>>,>>9") 
      + STRING(tot-val2, ">,>>>,>>>,>>>,>>9"). 
    ELSE
    str-list.s = str-list.s + STRING(tot-val, ">>>,>>>,>>>,>>9.99") 
      + STRING(tot-val1, ">>>,>>>,>>>,>>9.99") 
      + STRING(tot-val2, ">>>,>>>,>>>,>>9.99"). 

  END. 
END. 

PROCEDURE create-list0:  /* all FA-Group, from-date */ 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE t-anz      AS DECIMAL. 
DEFINE VARIABLE t-val      AS DECIMAL. 
DEFINE VARIABLE t-val1     AS DECIMAL. 
DEFINE VARIABLE t-val2     AS DECIMAL. 
DEFINE VARIABLE tt-anz     AS DECIMAL. 
DEFINE VARIABLE tt-val     AS DECIMAL. 
DEFINE VARIABLE tt-val1    AS DECIMAL. 
DEFINE VARIABLE tt-val2    AS DECIMAL. 
DEFINE VARIABLE tot-anz    AS DECIMAL. 
DEFINE VARIABLE tot-val    AS DECIMAL. 
DEFINE VARIABLE tot-val1   AS DECIMAL. 
DEFINE VARIABLE tot-val2   AS DECIMAL. 
DEFINE VARIABLE zwkum AS INTEGER. 
DEFINE VARIABLE bezeich AS CHAR. 
 
DEFINE BUFFER l-oh  FOR mathis. 
DEFINE VARIABLE qty         AS DECIMAL. 
DEFINE VARIABLE wert        AS DECIMAL. 
DEFINE VARIABLE max-lager   AS INTEGER NO-UNDO.

  STATUS DEFAULT "Processing...". 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
 
  ASSIGN
    tot-anz     = 0
    tot-val     = 0 
    tot-val1    = 0 
    tot-val2    = 0 
    max-lager   = to-lager
  .
  IF from-lager NE to-lager AND (maxNr - 1) = to-lager THEN max-lager = maxNr.
  FOR EACH lagerBuff WHERE lagerBuff.lager-nr GE from-lager 
    AND lagerBuff.lager-nr LE maxNr: 
    i = 0. 
    zwkum = 0. 
    t-anz = 0. 
    t-val = 0. 
    t-val1 = 0. 
    t-val2 = 0. 
    tt-anz = 0. 
    tt-val = 0. 
    tt-val1 = 0. 
    tt-val2 = 0. 
    create str-list. 
    create str-list. 
    str-list.s = STRING(lagerBuff.lager-nr, ">>99") 
      + "-" + STRING(lagerBuff.bezeich, "x(56)"). /*naufal afthar - 1C4A52*/
        
    /*ITA 110315*/
    IF mi-bookvalue-chk = YES THEN DO:
        FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich 
          AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
          FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0  NO-LOCK, 
          FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.gnr 
            AND fa-grup.flag = 0 NO-LOCK BY fa-grup.gnr BY mathis.name: 
    
          do-it = NO.
    
          IF NOT zero-value-only THEN do-it = YES.
          ELSE do-it = fa-artikel.book-wert = 0.
        
          
          IF do-it THEN
          DO:
              IF zwkum NE fa-artikel.gnr THEN 
              DO: 
                IF zwkum NE 0 THEN 
                DO: 
                  create str-list. 
                  DO j = 1 TO 60: 
                    str-list.s = str-list.s + " ". 
                  END. 
    
                  ASSIGN
                    str-list.refno  = "SUB TOTAL" 
             /*     str-list.flag   = 1   */
                    str-list.s      = str-list.s + STRING("SUB TOTAL", "x(60)"). /*naufal afthar - 1C4A52*/
                  IF t-anz GT 99999 THEN
                    str-list.s = str-list.s + STRING(t-anz,">>>>>9").
                  ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
                  IF t-val GT 99999999999 OR t-val1 GT 99999999999
                      OR t-val2 GT 99999999999 THEN
                  str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
                  ELSE
                  str-list.s = str-list.s + STRING(t-val, ">>>,>>>,>>>,>>9.99") /*test*/
                    + STRING(t-val1, ">>>,>>>,>>>,>>9.99") 
                    + STRING(t-val2, ">>>,>>>,>>>,>>9.99"). 
                END. 
                
                CREATE str-list. 
                ASSIGN
                  str-list.s = STRING(fa-grup.bezeich, "x(28)")
                  t-anz      = 0
                  t-val      = 0 
                  t-val1     = 0 
                  t-val2     = 0 
                  zwkum      = fa-artikel.gnr. 
              END. 
              
              create str-list. 
              str-list.refno = mathis.asset. 
              str-list.s = STRING(mathis.name, "x(60)") /*naufal afthar - 1C4A52*/
                           + STRING(mathis.asset, "x(14)") 
                           + STRING(mathis.datum) 
                           + STRING(fa-artikel.anzahl,">>,>>9"). 

              ASSIGN val-dep     = fa-artikel.depn-wert / fa-artikel.anz-depn
                     sub-depn    = 0
                     flag        = NO.
               
              IF val-dep = ? THEN val-dep = 0.
              DO datum = from-date TO to-date:
                  IF flag AND datum = DATE(MONTH(datum) + 1, 1, YEAR(datum)) - 1 THEN 
                        ASSIGN sub-depn = sub-depn + 1.
                
                  IF datum = fa-artikel.first-depn THEN 
                      ASSIGN sub-depn    = sub-depn + 1
                             flag        = YES.

                  IF datum = fa-artikel.last-depn THEN LEAVE.
              END.
              

              ASSIGN p-depn-wert = val-dep * sub-depn
                     p-book-wert = fa-artikel.warenwert - p-depn-wert.
              
              i = i + 1. 
              t-anz = t-anz + fa-artikel.anzahl. 
              t-val = t-val + fa-artikel.warenwert. 
              t-val1 = t-val1 + p-depn-wert. 
              t-val2 = t-val2 + p-book-wert. 
              tt-anz = tt-anz + fa-artikel.anzahl. 
              tt-val = tt-val + fa-artikel.warenwert. 
              tt-val1 = tt-val1 + p-depn-wert. 
              tt-val2 = tt-val2 + p-book-wert. 
              tot-anz = tot-anz + fa-artikel.anzahl. 
              tot-val = tot-val + fa-artikel.warenwert. 
              tot-val1 = tot-val1 + p-depn-wert. 
              tot-val2 = tot-val2 + p-book-wert. 
               
              str-list.s = str-list.s 
                         + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") 
                         + STRING(p-depn-wert, ">>>,>>>,>>>,>>9.99") 
                         + STRING(p-book-wert, ">>>,>>>,>>>,>>9.99"). 

              IF fa-artikel.first-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.first-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.next-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.next-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.last-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.last-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.anz-depn NE ? THEN 
                str-list.s = str-list.s + STRING(sub-depn). 
              ELSE str-list.s = str-list.s + "        ". 
          END.
        END. 
    END. /*END*/
    ELSE DO:
        FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich 
          AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
          FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0  NO-LOCK, 
          FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.gnr 
            AND fa-grup.flag = 0 NO-LOCK BY fa-grup.gnr BY mathis.name: 
    
          do-it = NO.
    
          IF NOT zero-value-only THEN do-it = YES.
          ELSE do-it = fa-artikel.book-wert = 0.
        
          
          IF do-it THEN
          DO:
              IF zwkum NE fa-artikel.gnr THEN 
              DO: 
                IF zwkum NE 0 THEN 
                DO: 
                  create str-list. 
                  DO j = 1 TO 60: 
                    str-list.s = str-list.s + " ". 
                  END. 
    
                  ASSIGN
                    str-list.refno  = "SUB TOTAL" 
             /*     str-list.flag   = 1   */
                    str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
                  IF t-anz GT 99999 THEN
                    str-list.s = str-list.s + STRING(t-anz,">>>>>9").
                  ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
                  IF t-val GT 99999999999 OR t-val1 GT 99999999999
                      OR t-val2 GT 99999999999 THEN
                  str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
                  ELSE
                  str-list.s = str-list.s + STRING(t-val, ">>>,>>>,>>>,>>9.99") /*test*/
                    + STRING(t-val1, ">>>,>>>,>>>,>>9.99") 
                    + STRING(t-val2, ">>>,>>>,>>>,>>9.99"). 
                END. 
                
                CREATE str-list. 
                ASSIGN
                  str-list.s = STRING(fa-grup.bezeich, "x(28)")
                  t-anz      = 0
                  t-val      = 0 
                  t-val1     = 0 
                  t-val2     = 0 
                  zwkum      = fa-artikel.gnr. 
              END. 
              i = i + 1. 
              t-anz = t-anz + fa-artikel.anzahl. 
              t-val = t-val + fa-artikel.warenwert. 
              t-val1 = t-val1 + fa-artikel.depn-wert. 
              t-val2 = t-val2 + fa-artikel.book-wert. 
              tt-anz = tt-anz + fa-artikel.anzahl. 
              tt-val = tt-val + fa-artikel.warenwert. 
              tt-val1 = tt-val1 + fa-artikel.depn-wert. 
              tt-val2 = tt-val2 + fa-artikel.book-wert. 
              tot-anz = tot-anz + fa-artikel.anzahl. 
              tot-val = tot-val + fa-artikel.warenwert. 
              tot-val1 = tot-val1 + fa-artikel.depn-wert. 
              tot-val2 = tot-val2 + fa-artikel.book-wert. 
         
              create str-list. 
              str-list.refno = mathis.asset. 
              str-list.s = STRING(mathis.name, "x(60)") /*naufal afthar - 1C4A52*/
                     + STRING(mathis.asset, "x(14)") 
                     + STRING(mathis.datum) 
                     + STRING(fa-artikel.anzahl,">>,>>9"). 
              str-list.s = str-list.s 
                     + STRING(fa-artikel.warenwert, ">>>,>>>,>>>,>>9.99") 
                     + STRING(fa-artikel.depn-wert, ">>>,>>>,>>>,>>9.99") 
                     + STRING(fa-artikel.book-wert, ">>>,>>>,>>>,>>9.99"). 
              IF fa-artikel.first-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.first-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.next-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.next-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.last-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.last-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.anz-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.anz-depn). 
              ELSE str-list.s = str-list.s + "        ". 
          END.
        END. 
    END.
 
    
    IF t-anz NE 0 THEN 
    DO: 
      create str-list. 
      DO j = 1 TO 60: 
        str-list.s = str-list.s + " ". 
      END. 

      ASSIGN
        str-list.refno  = "SUB TOTAL" 
  /*    str-list.flag   = 1   */
        str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
      IF t-anz GT 99999 THEN
        str-list.s = str-list.s + STRING(t-anz,">>>>>9").
      ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
      IF t-val GT 99999999999 OR t-val1 GT 99999999999
          OR t-val2 GT 99999999999 THEN
      str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
        + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
        + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
      ELSE
      str-list.s = str-list.s + STRING(t-val, ">>>,>>>,>>>,>>9.99") 
        + STRING(t-val1, ">>>,>>>,>>>,>>9.99") 
        + STRING(t-val2, ">>>,>>>,>>>,>>9.99"). 

    END. 
    IF i GT 0 THEN 
    DO: 
      create str-list. 
      DO j = 1 TO 60: 
        str-list.s = str-list.s + " ". 
      END. 
    END. 

    str-list.refno = "T O T A L". 
    str-list.flag = 1.
    IF LENGTH(TRIM(STRING(str-list.s))) NE 0 THEN str-list.s = str-list.s + STRING("T O T A L", "x(21)"). 
    ELSE str-list.s = str-list.s + STRING("T O T A L", "x(22)"). 
    IF LENGTH(TRIM(STRING(tt-anz))) GT 6 THEN
        str-list.s = str-list.s + STRING(tt-anz,">>>>>9"). 
    ELSE
        str-list.s = str-list.s + STRING(tt-anz,">>,>>9"). 

    IF LENGTH(TRIM(STRING(tt-val,">>>,>>>,>>>,>>9.99"))) GT 18 THEN
        str-list.s = str-list.s + STRING(tt-val, ">,>>>,>>>,>>>,>>9") .
    ELSE str-list.s = str-list.s + STRING(tt-val, ">>>,>>>,>>>,>>9.99") .
    str-list.s = str-list.s 
      + STRING(tt-val1, ">>>,>>>,>>>,>>9.99") 
      + STRING(tt-val2, ">>>,>>>,>>>,>>9.99").  
  END.

  IF from-lager NE to-lager AND tot-anz NE 0 THEN 
  DO: 
    create str-list. 
    create str-list. 
    DO j = 1 TO 60: 
      str-list.s = str-list.s + " ". 
    END. 

    ASSIGN
      str-list.flag  = 2 
      str-list.refno = "GRAND TOTAL".
    
    IF LENGTH(TRIM(STRING(str-list.s))) NE 0 THEN str-list.s = str-list.s + STRING(" ", "x(21)"). 
    ELSE str-list.s     = str-list.s + STRING(" ", "x(22)").  
    
    IF LENGTH(TRIM(STRING(tot-anz))) GT 6 THEN
        str-list.s = str-list.s + STRING(tot-anz,">>>>>9"). 
    ELSE str-list.s = str-list.s + STRING(tot-anz,">>,>>9"). 

    IF tot-val GT 99999999999 OR tot-val1 GT 99999999999
      OR tot-val2 GT 99999999999 THEN
    str-list.s = str-list.s + STRING(tot-val, ">,>>>,>>>,>>>,>>9") 
      + STRING(tot-val1, ">,>>>,>>>,>>>,>>9") 
      + STRING(tot-val2, ">,>>>,>>>,>>>,>>9"). 
    ELSE
    str-list.s = str-list.s + STRING(tot-val, ">>>,>>>,>>>,>>9.99") 
      + STRING(tot-val1, ">>>,>>>,>>>,>>9.99") 
      + STRING(tot-val2, ">>>,>>>,>>>,>>9.99"). 
  END. 
END. 

PROCEDURE create-list1:  /*  FA-Group */ 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE t-anz      AS DECIMAL. 
DEFINE VARIABLE t-val      AS DECIMAL. 
DEFINE VARIABLE t-val1     AS DECIMAL. 
DEFINE VARIABLE t-val2     AS DECIMAL. 
DEFINE VARIABLE tt-anz     AS DECIMAL. 
DEFINE VARIABLE tt-val     AS DECIMAL. 
DEFINE VARIABLE tt-val1    AS DECIMAL. 
DEFINE VARIABLE tt-val2    AS DECIMAL. 
DEFINE VARIABLE tot-anz    AS DECIMAL. 
DEFINE VARIABLE tot-val    AS DECIMAL. 
DEFINE VARIABLE tot-val1   AS DECIMAL. 
DEFINE VARIABLE tot-val2   AS DECIMAL. 
DEFINE VARIABLE zwkum AS INTEGER. 
DEFINE VARIABLE bezeich AS CHAR. 
 
DEFINE buffer l-oh FOR mathis. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
 
  status default "Processing...". 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  tot-anz = 0. 
  tot-val = 0. 
  tot-val1 = 0. 
  tot-val2 = 0. 
 
  FIND FIRST fa-grup WHERE fa-grup.gnr = from-grp 
    AND fa-grup.flag = 0 NO-LOCK. 
  FOR EACH lagerBuff WHERE lagerBuff.lager-nr GE from-lager 
    AND lagerBuff.lager-nr LE to-lager: 
    i = 0. 
    zwkum = 0. 
    t-anz = 0. 
    t-val = 0. 
    t-val1 = 0. 
    t-val2 = 0. 
    tt-anz = 0. 
    tt-val = 0. 
    tt-val1 = 0. 
    tt-val2 = 0. 
    create str-list. 
    create str-list. 
    str-list.s = STRING(lagerBuff.lager-nr, ">>99") 
      + "-" + STRING(lagerBuff.bezeich, "x(24)"). 

    /*ITA 110315*/
    IF mi-bookvalue-chk = YES THEN DO:
        FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich
          AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
          FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
          AND fa-artikel.loeschflag = 0 AND fa-artikel.gnr = from-grp NO-LOCK 
          BY mathis.name: 
     
          do-it = NO.
          IF NOT zero-value-only THEN do-it = YES.
          ELSE do-it = fa-artikel.book-wert = 0.
    
          IF do-it THEN
          DO:
              IF zwkum NE fa-artikel.gnr THEN 
              DO: 
                IF zwkum NE 0 THEN 
                DO: 
                  create str-list. 
                  DO j = 1 TO 28: 
                    str-list.s = str-list.s + " ". 
                  END. 
    
                  ASSIGN
                    str-list.refno  = "SUB TOTAL" 
             /*       str-list.flag   = 1  */
                    str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
                  IF t-anz GT 99999 THEN
                    str-list.s = str-list.s + STRING(t-anz,">>>>>9").
                  ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
                  IF t-val GT 99999999999 OR t-val1 GT 99999999999
                      OR t-val2 GT 99999999999 THEN
                  str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
                  ELSE
                  str-list.s = str-list.s + STRING(t-val, ">>,>>>,>>>,>>9.99") 
                    + STRING(t-val1, ">>,>>>,>>>,>>9.99") 
                    + STRING(t-val2, ">>,>>>,>>>,>>9.99"). 
    
                END. 
                CREATE str-list. 
                ASSIGN
                  str-list.s = STRING(fa-grup.bezeich, "x(28)")
                  t-anz      = 0
                  t-val      = 0 
                  t-val1     = 0 
                  t-val2     = 0 
                  zwkum = fa-artikel.gnr
                . 
              END. 
              
              create str-list. 
              str-list.refno = mathis.asset. 
              str-list.s = STRING(mathis.name, "x(28)") 
                     + STRING(mathis.asset, "x(14)") 
                     + STRING(mathis.datum) 
                     + STRING(fa-artikel.anzahl,">>,>>9"). 

              ASSIGN val-dep     = fa-artikel.depn-wert / fa-artikel.anz-depn
                     sub-depn    = 0
                     flag        = NO.

              IF val-dep = ? THEN val-dep = 0.
              DO datum = from-date TO to-date:
                  IF flag AND datum = DATE(MONTH(datum) + 1, 1, YEAR(datum)) - 1 THEN 
                        ASSIGN sub-depn = sub-depn + 1.
                
                  IF datum = fa-artikel.first-depn THEN 
                      ASSIGN sub-depn    = sub-depn + 1
                             flag        = YES.

                  IF datum = fa-artikel.last-depn THEN LEAVE.
              END.


              ASSIGN p-depn-wert = val-dep * sub-depn
                     p-book-wert = fa-artikel.warenwert - p-depn-wert.

              i = i + 1. 
              t-anz = t-anz + fa-artikel.anzahl. 
              t-val = t-val + fa-artikel.warenwert. 
              t-val1 = t-val1 + p-depn-wert. 
              t-val2 = t-val2 + p-book-wert. 
              tt-anz = tt-anz + fa-artikel.anzahl. 
              tt-val = tt-val + fa-artikel.warenwert. 
              tt-val1 = tt-val1 + p-depn-wert. 
              tt-val2 = tt-val2 + p-book-wert. 
              tot-anz = tot-anz + fa-artikel.anzahl. 
              tot-val = tot-val + fa-artikel.warenwert. 
              tot-val1 = tot-val1 + p-depn-wert. 
              tot-val2 = tot-val2 + p-book-wert. 

              str-list.s = str-list.s 
                     + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") 
                     + STRING(p-depn-wert, ">>>,>>>,>>>,>>9.99") 
                     + STRING(p-book-wert, ">>>,>>>,>>>,>>9.99"). 

              IF fa-artikel.first-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.first-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.next-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.next-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.last-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.last-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.anz-depn NE ? THEN 
                str-list.s = str-list.s + STRING(sub-depn). 
              ELSE str-list.s = str-list.s + "        ". 
            END. 
            IF t-anz NE 0 THEN 
            DO: 
              create str-list. 
              DO j = 1 TO 28: 
                str-list.s = str-list.s + " ". 
              END. 
    
              ASSIGN
                str-list.refno  = "SUB TOTAL" 
         /*     str-list.flag   = 1   */
                str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
              IF t-anz GT 99999 THEN
                str-list.s = str-list.s + STRING(t-anz,">>>>>9").
              ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
              IF t-val GT 99999999999 OR t-val1 GT 99999999999
                  OR t-val2 GT 99999999999 THEN
              str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
              ELSE
              str-list.s = str-list.s + STRING(t-val, ">>,>>>,>>>,>>9.99") 
                + STRING(t-val1, ">>,>>>,>>>,>>9.99") 
                + STRING(t-val2, ">>,>>>,>>>,>>9.99"). 
    
            END. 
            IF i GT 0 THEN 
            DO: 
              create str-list. 
              DO j = 1 TO 28: 
                str-list.s = str-list.s + " ". 
              END. 
            END. 
            str-list.refno = "T O T A L". 
            str-list.flag = 1. 
            str-list.s = str-list.s + STRING("T O T A L", "x(22)"). 
            str-list.s = str-list.s + STRING(tt-anz,">>,>>9"). 
            str-list.s = str-list.s + STRING(tt-val, ">>,>>>,>>>,>>9.99") 
              + STRING(tt-val1, ">>,>>>,>>>,>>9.99") 
              + STRING(tt-val2, ">>,>>>,>>>,>>9.99"). 
        END.
    END. /*END*/
    ELSE DO:
        FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich
          AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
          FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
          AND fa-artikel.loeschflag = 0 AND fa-artikel.gnr = from-grp NO-LOCK 
          BY mathis.name: 
     
          do-it = NO.
          IF NOT zero-value-only THEN do-it = YES.
          ELSE do-it = fa-artikel.book-wert = 0.
    
          IF do-it THEN
          DO:
              IF zwkum NE fa-artikel.gnr THEN 
              DO: 
                IF zwkum NE 0 THEN 
                DO: 
                  create str-list. 
                  DO j = 1 TO 28: 
                    str-list.s = str-list.s + " ". 
                  END. 
    
                  ASSIGN
                    str-list.refno  = "SUB TOTAL" 
             /*       str-list.flag   = 1  */
                    str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
                  IF t-anz GT 99999 THEN
                    str-list.s = str-list.s + STRING(t-anz,">>>>>9").
                  ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
                  IF t-val GT 99999999999 OR t-val1 GT 99999999999
                      OR t-val2 GT 99999999999 THEN
                  str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
                  ELSE
                  str-list.s = str-list.s + STRING(t-val, ">>,>>>,>>>,>>9.99") 
                    + STRING(t-val1, ">>,>>>,>>>,>>9.99") 
                    + STRING(t-val2, ">>,>>>,>>>,>>9.99"). 
    
                END. 
                CREATE str-list. 
                ASSIGN
                  str-list.s = STRING(fa-grup.bezeich, "x(28)")
                  t-anz      = 0
                  t-val      = 0 
                  t-val1     = 0 
                  t-val2     = 0 
                  zwkum = fa-artikel.gnr
                . 
              END. 
              i = i + 1. 
              t-anz = t-anz + fa-artikel.anzahl. 
              t-val = t-val + fa-artikel.warenwert. 
              t-val1 = t-val1 + fa-artikel.depn-wert. 
              t-val2 = t-val2 + fa-artikel.book-wert. 
              tt-anz = tt-anz + fa-artikel.anzahl. 
              tt-val = tt-val + fa-artikel.warenwert. 
              tt-val1 = tt-val1 + fa-artikel.depn-wert. 
              tt-val2 = tt-val2 + fa-artikel.book-wert. 
              tot-anz = tot-anz + fa-artikel.anzahl. 
              tot-val = tot-val + fa-artikel.warenwert. 
              tot-val1 = tot-val1 + fa-artikel.depn-wert. 
              tot-val2 = tot-val2 + fa-artikel.book-wert. 
         
              create str-list. 
              str-list.refno = mathis.asset. 
              str-list.s = STRING(mathis.name, "x(28)") 
                     + STRING(mathis.asset, "x(14)") 
                     + STRING(mathis.datum) 
                     + STRING(fa-artikel.anzahl,">>,>>9"). 
              str-list.s = str-list.s 
                     + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") 
                     + STRING(fa-artikel.depn-wert, ">>,>>>,>>>,>>9.99") 
                     + STRING(fa-artikel.book-wert, ">>,>>>,>>>,>>9.99"). 
              IF fa-artikel.first-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.first-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.next-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.next-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.last-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.last-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.anz-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.anz-depn). 
              ELSE str-list.s = str-list.s + "        ". 
            END. 
            IF t-anz NE 0 THEN 
            DO: 
              create str-list. 
              DO j = 1 TO 28: 
                str-list.s = str-list.s + " ". 
              END. 
    
              ASSIGN
                str-list.refno  = "SUB TOTAL" 
         /*     str-list.flag   = 1   */
                str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
              IF t-anz GT 99999 THEN
                str-list.s = str-list.s + STRING(t-anz,">>>>>9").
              ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
              IF t-val GT 99999999999 OR t-val1 GT 99999999999
                  OR t-val2 GT 99999999999 THEN
              str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
              ELSE
              str-list.s = str-list.s + STRING(t-val, ">>,>>>,>>>,>>9.99") 
                + STRING(t-val1, ">>,>>>,>>>,>>9.99") 
                + STRING(t-val2, ">>,>>>,>>>,>>9.99"). 
    
            END. 
            IF i GT 0 THEN 
            DO: 
              create str-list. 
              DO j = 1 TO 28: 
                str-list.s = str-list.s + " ". 
              END. 
            END. 
            str-list.refno = "T O T A L". 
            str-list.flag = 1. 
            str-list.s = str-list.s + STRING("T O T A L", "x(22)"). 
            str-list.s = str-list.s + STRING(tt-anz,">>,>>9"). 
            str-list.s = str-list.s + STRING(tt-val, ">>,>>>,>>>,>>9.99") 
              + STRING(tt-val1, ">>,>>>,>>>,>>9.99") 
              + STRING(tt-val2, ">>,>>>,>>>,>>9.99"). 
        END.
    END.
  END. 
 
  IF from-lager NE to-lager AND tot-anz NE 0 THEN 
  DO: 
    create str-list. 
    create str-list. 
    DO j = 1 TO 28: 
      str-list.s = str-list.s + " ". 
    END. 

    ASSIGN
      str-list.flag  = 2 
      str-list.refno = "GRAND TOTAL".

    IF LENGTH(TRIM(STRING(str-list.s))) NE 0 THEN str-list.s     = str-list.s + STRING(" ", "x(21)"). 
    ELSE str-list.s     = str-list.s + STRING(" ", "x(22)").  
      
    IF LENGTH(TRIM(STRING(tot-anz))) GT 6 THEN
        str-list.s = str-list.s + STRING(tot-anz,">>>>>9"). 
    ELSE str-list.s = str-list.s + STRING(tot-anz,">>,>>9"). 

    IF tot-val GT 99999999999 OR tot-val1 GT 99999999999
      OR tot-val2 GT 99999999999 THEN
    str-list.s = str-list.s + STRING(tot-val, ">,>>>,>>>,>>>,>>9") 
      + STRING(tot-val1, ">,>>>,>>>,>>>,>>9") 
      + STRING(tot-val2, ">,>>>,>>>,>>>,>>9"). 
    ELSE
    str-list.s = str-list.s + STRING(tot-val, ">>,>>>,>>>,>>9.99") 
      + STRING(tot-val1, ">>,>>>,>>>,>>9.99") 
      + STRING(tot-val2, ">>,>>>,>>>,>>9.99"). 

  END. 
END. 
 
PROCEDURE create-list11:  /*  FA-Group, from-date */ 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE t-anz      AS DECIMAL. 
DEFINE VARIABLE t-val      AS DECIMAL. 
DEFINE VARIABLE t-val1     AS DECIMAL. 
DEFINE VARIABLE t-val2     AS DECIMAL. 
DEFINE VARIABLE tt-anz     AS DECIMAL. 
DEFINE VARIABLE tt-val     AS DECIMAL. 
DEFINE VARIABLE tt-val1    AS DECIMAL. 
DEFINE VARIABLE tt-val2    AS DECIMAL. 
DEFINE VARIABLE tot-anz    AS DECIMAL. 
DEFINE VARIABLE tot-val    AS DECIMAL. 
DEFINE VARIABLE tot-val1   AS DECIMAL. 
DEFINE VARIABLE tot-val2   AS DECIMAL. 
DEFINE VARIABLE zwkum AS INTEGER. 
DEFINE VARIABLE bezeich AS CHAR. 
 
DEFINE buffer l-oh FOR mathis. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
 
  status default "Processing...". 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  tot-anz = 0. 
  tot-val = 0. 
  tot-val1 = 0. 
  tot-val2 = 0. 
 
  FIND FIRST fa-grup WHERE fa-grup.gnr = from-grp 
    AND fa-grup.flag = 0 NO-LOCK. 
  FOR EACH lagerBuff WHERE lagerBuff.lager-nr GE from-lager 
    AND lagerBuff.lager-nr LE to-lager: 
    i = 0. 
    zwkum = 0. 
    t-anz = 0. 
    t-val = 0. 
    t-val1 = 0. 
    t-val2 = 0. 
    tt-anz = 0. 
    tt-val = 0. 
    tt-val1 = 0. 
    tt-val2 = 0. 
    create str-list. 
    create str-list. 
    str-list.s = STRING(lagerBuff.lager-nr, ">>99") 
      + "-" + STRING(lagerBuff.bezeich, "x(24)"). 

    /*ITA 110315*/
    IF mi-bookvalue-chk = YES THEN DO:
        FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich 
          AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
          FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
          AND fa-artikel.loeschflag = 0 AND fa-artikel.gnr = from-grp NO-LOCK 
          BY mathis.name: 
          do-it = NO.
          IF NOT zero-value-only THEN do-it = YES.
          ELSE do-it = fa-artikel.book-wert = 0.
     
          IF do-it THEN
          DO:
              IF zwkum NE fa-artikel.gnr THEN 
              DO: 
                IF zwkum NE 0 THEN 
                DO: 
                  create str-list. 
                  DO j = 1 TO 28: 
                    str-list.s = str-list.s + " ". 
                  END. 
    
                  ASSIGN
                    str-list.refno  = "SUB TOTAL" 
             /*     str-list.flag   = 1   */
                    str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
                  IF t-anz GT 99999 THEN
                    str-list.s = str-list.s + STRING(t-anz,">>>>>9").
                  ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
                  IF t-val GT 99999999999 OR t-val1 GT 99999999999
                      OR t-val2 GT 99999999999 THEN
                  str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
                  ELSE
                  str-list.s = str-list.s + STRING(t-val, ">>>,>>>,>>>,>>9.99") 
                    + STRING(t-val1, ">>>,>>>,>>>,>>9.99") 
                    + STRING(t-val2, ">>>,>>>,>>>,>>9.99"). 
    
                END. 
                CREATE str-list. 
                ASSIGN
                  str-list.s = STRING(fa-grup.bezeich, "x(28)")
                  t-anz    = 0
                  t-val    = 0 
                  t-val1   = 0 
                  t-val2   = 0 
                  zwkum    = fa-artikel.gnr
                . 
              END. 
              
              create str-list. 
              str-list.refno = mathis.asset. 
              str-list.s = STRING(mathis.name, "x(28)") 
                     + STRING(mathis.asset, "x(14)") 
                     + STRING(mathis.datum) 
                     + STRING(fa-artikel.anzahl,">>,>>9"). 

              ASSIGN val-dep     = fa-artikel.depn-wert / fa-artikel.anz-depn
                     sub-depn    = 0
                     flag        = NO.
              IF val-dep = ? THEN val-dep = 0.
              DO datum = from-date TO to-date:
                  IF flag AND datum = DATE(MONTH(datum) + 1, 1, YEAR(datum)) - 1 THEN 
                        ASSIGN sub-depn = sub-depn + 1.
                
                  IF datum = fa-artikel.first-depn THEN 
                      ASSIGN sub-depn    = sub-depn + 1
                             flag        = YES.

                  IF datum = fa-artikel.last-depn THEN LEAVE.
              END.

              ASSIGN p-depn-wert = val-dep * sub-depn
                     p-book-wert = fa-artikel.warenwert - p-depn-wert.

              i = i + 1. 
              t-anz = t-anz + fa-artikel.anzahl. 
              t-val = t-val + fa-artikel.warenwert. 
              t-val1 = t-val1 + p-depn-wert. 
              t-val2 = t-val2 + p-book-wert. 
              tt-anz = tt-anz + fa-artikel.anzahl. 
              tt-val = tt-val + fa-artikel.warenwert. 
              tt-val1 = tt-val1 + p-depn-wert. 
              tt-val2 = tt-val2 + p-book-wert. 
              tot-anz = tot-anz + fa-artikel.anzahl. 
              tot-val = tot-val + fa-artikel.warenwert. 
              tot-val1 = tot-val1 + p-depn-wert. 
              tot-val2 = tot-val2 + p-book-wert. 

              str-list.s = str-list.s 
                     + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") 
                     + STRING(p-depn-wert, ">>>,>>>,>>>,>>9.99") 
                     + STRING(p-book-wert, ">>>,>>>,>>>,>>9.99"). 

              IF fa-artikel.first-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.first-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.next-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.next-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.last-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.last-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.anz-depn NE ? THEN 
                str-list.s = str-list.s + STRING(sub-depn). 
              ELSE str-list.s = str-list.s + "        ". 
            END. 

            IF t-anz NE 0 THEN 
            DO: 
              create str-list. 
              DO j = 1 TO 28: 
                str-list.s = str-list.s + " ". 
              END. 
    
              ASSIGN
                str-list.refno  = "SUB TOTAL" 
         /*     str-list.flag   = 1   */
                str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
              IF t-anz GT 99999 THEN
                str-list.s = str-list.s + STRING(t-anz,">>>>>9").
              ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
              IF t-val GT 99999999999 OR t-val1 GT 99999999999
                  OR t-val2 GT 99999999999 THEN
              str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
              ELSE
              str-list.s = str-list.s + STRING(t-val, ">>>,>>>,>>>,>>9.99") 
                + STRING(t-val1, ">>>,>>>,>>>,>>9.99") 
                + STRING(t-val2, ">>>,>>>,>>>,>>9.99"). 
    
            END. 
            IF i GT 0 THEN 
            DO: 
              create str-list. 
              DO j = 1 TO 28: 
                str-list.s = str-list.s + " ". 
              END. 
            END. 
            str-list.refno = "T O T A L". 
            str-list.flag = 1. 
            str-list.s = str-list.s + STRING("T O T A L", "x(22)"). 
            str-list.s = str-list.s + STRING(tt-anz,">>,>>9"). 
            str-list.s = str-list.s + STRING(tt-val, ">>>,>>>,>>>,>>9.99") 
              + STRING(tt-val1, ">>>,>>>,>>>,>>9.99") 
              + STRING(tt-val2, ">>>,>>>,>>>,>>9.99"). 
        END.
    END. /*END*/
    ELSE DO:
        FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich 
          AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
          FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
          AND fa-artikel.loeschflag = 0 AND fa-artikel.gnr = from-grp NO-LOCK 
          BY mathis.name: 
          do-it = NO.
          IF NOT zero-value-only THEN do-it = YES.
          ELSE do-it = fa-artikel.book-wert = 0.
     
          IF do-it THEN
          DO:
              IF zwkum NE fa-artikel.gnr THEN 
              DO: 
                IF zwkum NE 0 THEN 
                DO: 
                  create str-list. 
                  DO j = 1 TO 28: 
                    str-list.s = str-list.s + " ". 
                  END. 
    
                  ASSIGN
                    str-list.refno  = "SUB TOTAL" 
             /*     str-list.flag   = 1   */
                    str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
                  IF t-anz GT 99999 THEN
                    str-list.s = str-list.s + STRING(t-anz,">>>>>9").
                  ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
                  IF t-val GT 99999999999 OR t-val1 GT 99999999999
                      OR t-val2 GT 99999999999 THEN
                  str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
                  ELSE
                  str-list.s = str-list.s + STRING(t-val, ">>>,>>>,>>>,>>9.99") 
                    + STRING(t-val1, ">>>,>>>,>>>,>>9.99") 
                    + STRING(t-val2, ">>>,>>>,>>>,>>9.99"). 
    
                END. 
                CREATE str-list. 
                ASSIGN
                  str-list.s = STRING(fa-grup.bezeich, "x(28)")
                  t-anz    = 0
                  t-val    = 0 
                  t-val1   = 0 
                  t-val2   = 0 
                  zwkum    = fa-artikel.gnr
                . 
              END. 
              i = i + 1. 
              t-anz = t-anz + fa-artikel.anzahl. 
              t-val = t-val + fa-artikel.warenwert. 
              t-val1 = t-val1 + fa-artikel.depn-wert. 
              t-val2 = t-val2 + fa-artikel.book-wert. 
              tt-anz = tt-anz + fa-artikel.anzahl. 
              tt-val = tt-val + fa-artikel.warenwert. 
              tt-val1 = tt-val1 + fa-artikel.depn-wert. 
              tt-val2 = tt-val2 + fa-artikel.book-wert. 
              tot-anz = tot-anz + fa-artikel.anzahl. 
              tot-val = tot-val + fa-artikel.warenwert. 
              tot-val1 = tot-val1 + fa-artikel.depn-wert. 
              tot-val2 = tot-val2 + fa-artikel.book-wert. 
         
              create str-list. 
              str-list.refno = mathis.asset. 
              str-list.s = STRING(mathis.name, "x(28)") 
                     + STRING(mathis.asset, "x(14)") 
                     + STRING(mathis.datum) 
                     + STRING(fa-artikel.anzahl,">>,>>9"). 
              str-list.s = str-list.s 
                     + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") 
                     + STRING(fa-artikel.depn-wert, ">>>,>>>,>>>,>>9.99") 
                     + STRING(fa-artikel.book-wert, ">>>,>>>,>>>,>>9.99"). 
              IF fa-artikel.first-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.first-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.next-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.next-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.last-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.last-depn). 
              ELSE str-list.s = str-list.s + "        ". 
              IF fa-artikel.anz-depn NE ? THEN 
                str-list.s = str-list.s + STRING(fa-artikel.anz-depn). 
              ELSE str-list.s = str-list.s + "        ". 
            END. 
            IF t-anz NE 0 THEN 
            DO: 
              create str-list. 
              DO j = 1 TO 28: 
                str-list.s = str-list.s + " ". 
              END. 
    
              ASSIGN
                str-list.refno  = "SUB TOTAL" 
         /*     str-list.flag   = 1   */
                str-list.s      = str-list.s + STRING("SUB TOTAL", "x(22)").
              IF t-anz GT 99999 THEN
                str-list.s = str-list.s + STRING(t-anz,">>>>>9").
              ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
              IF t-val GT 99999999999 OR t-val1 GT 99999999999
                  OR t-val2 GT 99999999999 THEN
              str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
              ELSE
              str-list.s = str-list.s + STRING(t-val, ">>>,>>>,>>>,>>9.99") 
                + STRING(t-val1, ">>>,>>>,>>>,>>9.99") 
                + STRING(t-val2, ">>>,>>>,>>>,>>9.99"). 
    
            END. 
            IF i GT 0 THEN 
            DO: 
              create str-list. 
              DO j = 1 TO 28: 
                str-list.s = str-list.s + " ". 
              END. 
            END. 
            str-list.refno = "T O T A L". 
            str-list.flag = 1. 
            str-list.s = str-list.s + STRING("T O T A L", "x(22)"). 
            str-list.s = str-list.s + STRING(tt-anz,">>,>>9"). 
            str-list.s = str-list.s + STRING(tt-val, ">>>,>>>,>>>,>>9.99") 
              + STRING(tt-val1, ">>>,>>>,>>>,>>9.99") 
              + STRING(tt-val2, ">>>,>>>,>>>,>>9.99"). 
        END.
    END.
  END. 
 
  IF from-lager NE to-lager AND tot-anz NE 0 THEN 
  DO: 
    create str-list. 
    create str-list. 
    DO j = 1 TO 28: 
      str-list.s = str-list.s + " ". 
    END. 

    ASSIGN
      str-list.flag  = 2 
      str-list.refno = "GRAND TOTAL".
    
    IF LENGTH(TRIM(STRING(str-list.s))) NE 0 THEN str-list.s     = str-list.s + STRING(" ", "x(21)"). 
    ELSE str-list.s     = str-list.s + STRING(" ", "x(22)").  
    
    IF LENGTH(TRIM(STRING(tot-anz))) GT 6 THEN
        str-list.s = str-list.s + STRING(tot-anz,">>>>>9"). 
    ELSE str-list.s = str-list.s + STRING(tot-anz,">>,>>9"). 

    IF tot-val GT 99999999999 OR tot-val1 GT 99999999999
      OR tot-val2 GT 99999999999 THEN
    str-list.s = str-list.s + STRING(tot-val, ">,>>>,>>>,>>>,>>9") 
      + STRING(tot-val1, ">,>>>,>>>,>>>,>>9") 
      + STRING(tot-val2, ">,>>>,>>>,>>>,>>9"). 
    ELSE
    str-list.s = str-list.s + STRING(tot-val, ">>>,>>>,>>>,>>9.99") 
      + STRING(tot-val1, ">>>,>>>,>>>,>>9.99") 
      + STRING(tot-val2, ">>>,>>>,>>>,>>9.99"). 
  END. 
END. 

PROCEDURE create-listsgrp:  /* all FA-Group */ 
    
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE t-anz      AS DECIMAL. 
DEFINE VARIABLE t-val      AS DECIMAL. 
DEFINE VARIABLE t-val1     AS DECIMAL. 
DEFINE VARIABLE t-val2     AS DECIMAL. 
DEFINE VARIABLE tot-anz    AS DECIMAL. 
DEFINE VARIABLE tot-val    AS DECIMAL. 
DEFINE VARIABLE tot-val1   AS DECIMAL. 
DEFINE VARIABLE tot-val2   AS DECIMAL. 
DEFINE VARIABLE zwkum AS INTEGER. 
DEFINE VARIABLE bezeich AS CHAR. 
 
DEFINE buffer l-oh FOR mathis. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
 
DEF VAR diff-n AS INTEGER. 
DEF VAR diff-wert AS DECIMAL. 
 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
 
  diff-n = (YEAR(last-acctdate) - yy) * 12 +  MONTH(last-acctdate) - mm. 
 
  tot-anz = 0. 
  tot-val = 0. 
  tot-val1 = 0. 
  tot-val2 = 0. 
 
  DO: 
    i = 0. 
    zwkum = 0. 
    t-anz = 0. 
    t-val = 0. 
    t-val1 = 0. 
    t-val2 = 0. 
    
    /*ITA 110315*/
    IF mi-bookvalue-chk = YES THEN DO:
        FOR EACH mathis WHERE mathis.datum GE from-date
          AND mathis.datum LE to-date NO-LOCK, 
          FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0
          /*AND fa-artikel.loeschflag = 0 AND (fa-artikel.anz-depn - diff-n) GE 0 */
          NO-LOCK, 
          FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp 
            AND fa-grup.flag = 1 
            AND fa-grup.gnr GE from-subgr
            AND fa-grup.gnr LE to-subgr NO-LOCK BY fa-artikel.subgrp BY mathis.name: 
     
         /*IF mathis.datum GT 08/31/10 THEN DISP mathis.datum.*/
    
          IF zwkum NE fa-artikel.subgrp THEN 
          DO: 
                IF zwkum NE 0 THEN 
                DO: 
                  create str-list. 
                  DO j = 1 TO 38: 
                    str-list.s = str-list.s + " ". 
                  END. 
        
                  ASSIGN
                    str-list.refno  = "SUB TOTAL" 
                    str-list.flag   = 1
                    str-list.s      = str-list.s + STRING("SUB TOTAL", "x(55)") + "                                        " .
                  IF t-anz GT 99999 THEN
                    str-list.s = str-list.s + STRING(t-anz,">>>>>9").
                  ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
                  IF t-val GT 99999999999 OR t-val1 GT 99999999999
                      OR t-val2 GT 99999999999 THEN
                  str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
                    + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
                  ELSE
                  str-list.s = str-list.s + STRING(t-val, ">>,>>>,>>>,>>9.99") 
                    + STRING(t-val1, ">>,>>>,>>>,>>9.99") 
                    + STRING(t-val2, ">>,>>>,>>>,>>9.99"). 
        
                END. 
                CREATE str-list. 
                ASSIGN
                  str-list.s = STRING(fa-grup.bezeich, "x(28)")
                  t-anz      = 0
                  t-val      = 0 
                  t-val1     = 0 
                  t-val2     = 0 
                  zwkum      = fa-artikel.subgrp. 
          END. 


          CREATE str-list. 
          ASSIGN 
            str-list.refno = mathis.asset 
            str-list.location = trim(mathis.location )
            str-list.s = STRING(mathis.name, "x(38)") 
                 + STRING(mathis.asset, "x(14)") 
                 + STRING(mathis.datum) 
                 + STRING(fa-artikel.anzahl,">>,>>9"). 

          ASSIGN val-dep     = fa-artikel.depn-wert / fa-artikel.anz-depn
                 sub-depn    = 0
                 flag        = NO.
          IF val-dep = ? THEN val-dep = 0.
          DO datum = from-date TO to-date:
              IF flag AND datum = DATE(MONTH(datum) + 1, 1, YEAR(datum)) - 1 THEN 
                    ASSIGN sub-depn = sub-depn + 1.
            
              IF datum = fa-artikel.first-depn THEN 
                  ASSIGN sub-depn    = sub-depn + 1
                         flag        = YES.

              IF datum = fa-artikel.last-depn THEN LEAVE.
          END.


          ASSIGN p-depn-wert = val-dep * sub-depn
                 p-book-wert = fa-artikel.warenwert - p-depn-wert.
            
          i = i + 1. 
          t-anz = t-anz + fa-artikel.anzahl. 
          t-val = t-val + fa-artikel.warenwert. 
          tot-anz = tot-anz + fa-artikel.anzahl. 
          tot-val = tot-val + fa-artikel.warenwert. 
            
          IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
          DO: 
            t-val2 = t-val2 + fa-artikel.warenwert. 
            tot-val2 = tot-val2 + fa-artikel.warenwert. 
          END. 
          ELSE 
          DO: 
            diff-wert = (p-depn-wert / sub-depn) * diff-n. 
            IF diff-wert = ? THEN diff-wert = 0.
            t-val1 = t-val1 + p-depn-wert - diff-wert. 
            t-val2 = t-val2 + p-book-wert + diff-wert. 
            tot-val1 = tot-val1 + p-depn-wert - diff-wert. 
            tot-val2 = tot-val2 + p-book-wert + diff-wert. 
          END. 

     
          IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
          DO: 
            str-list.s = str-list.s 
                 + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>>,>>9.99") 
                 + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99"). 
          END. 
          ELSE 
          DO: 
            str-list.s = str-list.s 
                 + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") 
                 + STRING(p-depn-wert - diff-wert, ">>>,>>>,>>>,>>9.99") 
                 + STRING(p-book-wert + diff-wert, ">>>,>>>,>>>,>>9.99"). 
          END. 

          
          IF fa-artikel.first-depn NE ? THEN 
            str-list.s = str-list.s + STRING(fa-artikel.first-depn). 
          ELSE str-list.s = str-list.s + "        ". 
          IF fa-artikel.next-depn NE ? THEN 
            str-list.s = str-list.s + STRING(fa-artikel.next-depn). 
          ELSE str-list.s = str-list.s + "        ". 
          IF fa-artikel.last-depn NE ? THEN 
            str-list.s = str-list.s + STRING(fa-artikel.last-depn). 
          ELSE str-list.s = str-list.s + "        ". 
          IF fa-artikel.anz-depn NE ? THEN 
             str-list.s = str-list.s + STRING(sub-depn). 
          ELSE str-list.s = str-list.s + "        ". 
        END. 

        IF t-anz NE 0 THEN 
        DO: 
          create str-list. 
          DO j = 1 TO 38: 
            str-list.s = str-list.s + " ". 
          END.       
    
          ASSIGN
            str-list.refno  = "SUB TOTAL" 
            str-list.flag   = 1
            str-list.s      = str-list.s + STRING("SUB TOTAL", "x(24)").
          IF t-anz GT 99999 THEN
            str-list.s = str-list.s + STRING(t-anz,">>>>>9").
          ELSE str-list.s = str-list.s + STRING(t-anz,">>,>>9"). 
          IF t-val GT 99999999999 OR t-val1 GT 99999999999
              OR t-val2 GT 99999999999 THEN
          str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") 
            + STRING(t-val1, ">,>>>,>>>,>>>,>>9") 
            + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
          ELSE
          str-list.s = str-list.s + STRING(t-val, ">>,>>>,>>>,>>9.99") 
            + STRING(t-val1, ">>,>>>,>>>,>>9.99") 
            + STRING(t-val2, ">>,>>>,>>>,>>9.99"). 
    
        END.
    END. /*end*/
    ELSE DO:
        FOR EACH mathis WHERE mathis.datum GE from-date
          AND mathis.datum LE to-date NO-LOCK, 
          FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0
          /*AND fa-artikel.loeschflag = 0 AND (fa-artikel.anz-depn - diff-n) GE 0 */
          NO-LOCK, 
          FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp 
            AND fa-grup.flag = 1 
            AND fa-grup.gnr GE from-subgr
            AND fa-grup.gnr LE to-subgr NO-LOCK BY fa-artikel.subgrp BY mathis.name: 
     
         /*IF mathis.datum GT 08/31/10 THEN DISP mathis.datum.*/
        
          IF zwkum NE fa-artikel.subgrp THEN 
          DO: 
            IF zwkum NE 0 THEN 
            DO: 
              create str-list. 
              DO j = 1 TO 38: 
                str-list.s = str-list.s + " ". 
              END. 
                
              ASSIGN
                str-list.refno  = "SUB TOTAL" 
                str-list.flag   = 1
                str-list.s      = str-list.s + STRING("SUB TOTAL", "x(23)").
              IF t-anz GT 99999 THEN
                str-list.s = str-list.s + STRING(t-anz,">>>9") + "   ".
              ELSE str-list.s = str-list.s + STRING(t-anz,">,>>9") + "   ". 

              IF t-val GT 99999999999 OR t-val1 GT 99999999999
                  OR t-val2 GT 99999999999 THEN
              str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") + " "
                + STRING(t-val1, ">,>>>,>>>,>>>,>>9") + " "
                + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
              ELSE
              str-list.s = str-list.s + STRING(t-val, ">>,>>>,>>>,>>9.99") + " " 
                + STRING(t-val1, ">>,>>>,>>>,>>9.99") + " "
                + STRING(t-val2, ">>,>>>,>>>,>>9.99"). 
    
            END. 

            CREATE str-list. 
            ASSIGN
              str-list.s = STRING(fa-grup.bezeich, "x(28)")
              t-anz      = 0
              t-val      = 0 
              t-val1     = 0 
              t-val2     = 0 
              zwkum      = fa-artikel.subgrp
            . 
          END. 
          i = i + 1. 
          t-anz = t-anz + fa-artikel.anzahl. 
          t-val = t-val + fa-artikel.warenwert. 
          tot-anz = tot-anz + fa-artikel.anzahl. 
          tot-val = tot-val + fa-artikel.warenwert. 
            
          IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
          DO: 
            t-val2 = t-val2 + fa-artikel.warenwert. 
            tot-val2 = tot-val2 + fa-artikel.warenwert. 
          END. 
          ELSE 
          DO: 
            diff-wert = (fa-artikel.depn-wert / fa-artikel.anz-depn) * diff-n.
            IF diff-wert = ? THEN diff-wert = 0.
            t-val1 = t-val1 + fa-artikel.depn-wert - diff-wert. 
            t-val2 = t-val2 + fa-artikel.book-wert + diff-wert. 
            tot-val1 = tot-val1 + fa-artikel.depn-wert - diff-wert. 
            tot-val2 = tot-val2 + fa-artikel.book-wert + diff-wert. 
          END. 
     
          CREATE str-list. 
          ASSIGN 
            str-list.refno = mathis.asset 
            str-list.location = trim(mathis.location)
            str-list.s = STRING(mathis.name, "x(38)") 
                 + STRING(mathis.asset, "x(14)") 
                 + STRING(mathis.datum) 
                 + STRING(fa-artikel.anzahl,">>,>>9"). 
     
          IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
          DO: 
            str-list.s = str-list.s 
                 + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>>,>>9.99") 
                 + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99"). 
          END. 
          ELSE 
          DO: 
            str-list.s = str-list.s 
                 + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") 
                 + STRING(fa-artikel.depn-wert - diff-wert, ">>>,>>>,>>>,>>9.99") 
                 + STRING(fa-artikel.book-wert + diff-wert, ">>>,>>>,>>>,>>9.99"). 
          END. 
     
          IF fa-artikel.first-depn NE ? THEN 
            str-list.s = str-list.s + STRING(fa-artikel.first-depn). 
          ELSE str-list.s = str-list.s + "        ". 
          IF fa-artikel.next-depn NE ? THEN 
            str-list.s = str-list.s + STRING(fa-artikel.next-depn). 
          ELSE str-list.s = str-list.s + "        ". 
          IF fa-artikel.last-depn NE ? THEN 
            str-list.s = str-list.s + STRING(fa-artikel.last-depn). 
          ELSE str-list.s = str-list.s + "        ". 
          IF fa-artikel.anz-depn NE ? THEN 
             str-list.s = str-list.s + STRING(fa-artikel.anz-depn). 
          ELSE str-list.s = str-list.s + "        ". 
        END. 
        IF t-anz NE 0 THEN 
        DO: 
          create str-list. 
          DO j = 1 TO 38: 
            str-list.s = str-list.s + " ". 
          END.       
    
          ASSIGN
            str-list.refno  = "SUB TOTAL" 
            str-list.flag   = 1
            str-list.s      = str-list.s + STRING("SUB TOTAL", "x(23)").
          IF t-anz GT 99999 THEN
            str-list.s = str-list.s + STRING(t-anz,">>>9") + "   ".
          ELSE str-list.s = str-list.s + STRING(t-anz,">,>>9") + "   ". 
          IF t-val GT 99999999999 OR t-val1 GT 99999999999
              OR t-val2 GT 99999999999 THEN
          str-list.s = str-list.s + STRING(t-val, ">,>>>,>>>,>>>,>>9") + " "
            + STRING(t-val1, ">,>>>,>>>,>>>,>>9") + " "
            + STRING(t-val2, ">,>>>,>>>,>>>,>>9"). 
          ELSE
          str-list.s = str-list.s + STRING(t-val, ">>,>>>,>>>,>>9.99") + " "
            + STRING(t-val1, ">>,>>>,>>>,>>9.99") + " "
            + STRING(t-val2, ">>,>>>,>>>,>>9.99"). 
    
        END.
    END.
  END. 
 
  IF tot-anz NE 0 THEN 
  DO: 
    create str-list. 
    create str-list. 
    DO j = 1 TO 38: 
      str-list.s = str-list.s + " ". 
    END. 
    
    ASSIGN
      str-list.flag  = 2 
      str-list.refno = "GRAND TOTAL". 

    IF LENGTH(TRIM(STRING(str-list.s))) NE 0 THEN str-list.s     = str-list.s + STRING(" ", "x(21)"). 
    ELSE str-list.s     = str-list.s + STRING(" ", "x(22)").  
      
    IF LENGTH(TRIM(STRING(tot-anz))) GT 6 THEN
        str-list.s = str-list.s + STRING(tot-anz,">>>>>9"). 
    ELSE str-list.s = str-list.s + STRING(tot-anz,">>,>>9") + "   ". 

    IF tot-val GT 99999999999 OR tot-val1 GT 99999999999
      OR tot-val2 GT 99999999999 THEN
    str-list.s = str-list.s + STRING(tot-val, ">,>>>,>>>,>>>,>>9") + " "
      + STRING(tot-val1, ">,>>>,>>>,>>>,>>9") + " "
      + STRING(tot-val2, ">,>>>,>>>,>>>,>>9"). 
    ELSE
    str-list.s = str-list.s + STRING(tot-val, ">>,>>>,>>>,>>9.99")
      + STRING(tot-val1, ">>,>>>,>>>,>>9.99") 
      + STRING(tot-val2, ">>,>>>,>>>,>>9.99"). 

  END. 
END. 


PROCEDURE create-listACCT:  /* all FA-Group BY acctno */ 
DEF VAR curr-acct   AS CHAR INITIAL "". 
DEF VAR fibu        AS CHAR. 
DEF VAR diff-n      AS INTEGER. 
DEF VAR diff-wert   AS DECIMAL. 
DEF VAR t-oh        AS DECIMAL INITIAL 0. 
DEF VAR t-depn      AS DECIMAL INITIAL 0. 
DEF VAR tot-oh      AS DECIMAL INITIAL 0. 
DEF VAR tot-depn    AS DECIMAL INITIAL 0.
DEF VAR t-book      AS DECIMAL INITIAL 0.
DEF VAR tot-book    AS DECIMAL INITIAL 0.
DEF VAR t-anz       AS DECIMAL INITIAL 0.
DEF VAR tot-anz     AS DECIMAL INITIAL 0.
 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
  
  diff-n = (YEAR(last-acctdate) - yy) * 12 +  MONTH(last-acctdate) - mm. 

  /*ITA 110315*/
  IF mi-bookvalue-chk = YES THEN DO:
      FOR EACH mathis WHERE mathis.datum GE from-date
        AND mathis.datum LE to-date NO-LOCK, 
       FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
         AND fa-artikel.loeschflag = 0
        /*AND fa-artikel.loeschflag = 0 AND (fa-artikel.anz-depn - diff-n) GE 0 */
        NO-LOCK BY fa-artikel.fibukonto: 
            
        /*IF curr-acct = "" THEN curr-acct = fa-artikel.fibukonto.*/
        IF curr-acct NE fa-artikel.fibukonto THEN 
        DO: 
          ASSIGN 
              tot-anz  = tot-anz + t-anz
              tot-oh   = tot-oh + t-oh
              tot-depn = tot-depn + t-depn
              tot-book = tot-book + t-book.
            
          FIND FIRST gl-acct WHERE gl-acct.fibukonto = curr-acct NO-LOCK NO-ERROR. 
          IF AVAILABLE gl-acct THEN RUN convert-fibu(curr-acct, OUTPUT fibu). 
    
          IF curr-acct NE "" THEN DO:
              
              CREATE str-list. 
              ASSIGN
               str-list.location  = ""
               str-list.s = STRING("SUBTOTAL ", "x(13)") 
                /*+ STRING(gl-acct.bezeich, "x(48)") */
                + STRING(" ", "x(48)") 
                + "        "
                + STRING(t-anz,">>,>>9")
                + STRING(t-oh, ">>>,>>>,>>>,>>9.99") 
                + STRING(t-depn, ">>>,>>>,>>>,>>9.99")
                + STRING(t-book, "  >>>,>>>,>>>,>>9.99"). 
    
              CREATE str-list.
    
          END.
    
          /*CREATE str-list. 
          ASSIGN str-list.s = STRING(fibu, "x(13)") 
            + STRING(" ", "x(48)") 
            + STRING(" ","x(10)")
            + STRING(" ","x(6)")
            + STRING(0, ">>>,>>>,>>>,>>9.99") 
            + STRING(0, ">>>,>>>,>>>,>>9.99"). */
    
           ASSIGN
              curr-acct = fa-artikel.fibukonto
              t-anz     = 0
              t-oh      = 0 
              t-depn    = 0
              t-book    = 0. 
          
        END.
        
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-artikel.fibukonto NO-LOCK NO-ERROR. 
        RUN convert-fibu(fa-artikel.fibukonto, OUTPUT fibu). 
        
        FIND FIRST str-list WHERE SUBSTRING(str-list.s,1,13) = fibu NO-ERROR.
        IF AVAILABLE str-list THEN DO:
            CREATE str-list. 
            ASSIGN 
                
                str-list.refno    = mathis.asset 
                str-list.location = trim(mathis.location) 
                str-list.s = STRING(" ", "x(13)") 
                             + STRING(mathis.name, "x(48)") 
                             + STRING(mathis.datum) 
                             + STRING(fa-artikel.anzahl,">>,>>9"). 
    
        END.
        ELSE DO:
            CREATE str-list. 
            ASSIGN 
                
                str-list.refno    = mathis.asset 
                str-list.location = trim(mathis.location) 
                str-list.s = STRING(fibu, "x(13)") 
                             + STRING(mathis.name, "x(48)") 
                             + STRING(mathis.datum) 
                             + STRING(fa-artikel.anzahl,">>,>>9"). 
        END.

        ASSIGN val-dep     = fa-artikel.depn-wert / fa-artikel.anz-depn
               sub-depn    = 0
               flag        = NO.

        IF val-dep = ? THEN val-dep = 0.
        DO datum = from-date TO to-date:

          IF flag AND datum = DATE(MONTH(datum) + 1, 1, YEAR(datum)) - 1 THEN 
                ASSIGN sub-depn = sub-depn + 1.
        
          IF datum = fa-artikel.first-depn THEN 
              ASSIGN sub-depn    = sub-depn + 1
                     flag        = YES.

          IF datum = fa-artikel.last-depn THEN LEAVE.
        END.
            
        ASSIGN p-depn-wert = val-dep * sub-depn
               p-book-wert = fa-artikel.warenwert - p-depn-wert.
    
        /*ITA 160214*/    
        IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
        DO: 
            str-list.s = str-list.s 
                 + STRING(fa-artikel.warenwert, ">>>,>>>,>>>,>>9.99") 
                 + STRING(0, ">>>,>>>,>>>,>>9.99") 
                 + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99"). 
        END. 
        ELSE 
        DO: 
            str-list.s = str-list.s 
                 + STRING(fa-artikel.warenwert, ">>>,>>>,>>>,>>9.99") 
                 + STRING(p-depn-wert - diff-wert, ">>>,>>>,>>>,>>9.99") 
                 + STRING(p-book-wert + diff-wert, "  >>>,>>>,>>>,>>9.99"). 
        END. 
     
        IF fa-artikel.first-depn NE ? THEN 
           str-list.s = str-list.s + STRING(fa-artikel.first-depn). 
        ELSE str-list.s = str-list.s + "        ". 
        IF fa-artikel.next-depn NE ? THEN 
           str-list.s = str-list.s + STRING(fa-artikel.next-depn). 
        ELSE str-list.s = str-list.s + "        ". 
        IF fa-artikel.last-depn NE ? THEN 
           str-list.s = str-list.s + STRING(fa-artikel.last-depn). 
        ELSE str-list.s = str-list.s + "        ". 
        IF fa-artikel.anz-depn NE ? THEN 
            str-list.s = str-list.s + STRING(sub-depn). 
        ELSE str-list.s = str-list.s + "   ". /*end*/
        /*
        IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
        DO: 
          t-oh = t-oh + fa-artikel.warenwert.
          t-book = t-book + fa-artikel.book-wert.
        END. 
        ELSE IF fa-artikel.anz-depn - diff-n > 0 THEN 
        DO: 
          FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK. 
          IF (fa-kateg.methode = 0) THEN 
          DO: 
            diff-wert = (fa-artikel.depn-wert / fa-artikel.anz-depn) * diff-n. 
            /*t-oh = t-oh + fa-artikel.book-wert + diff-wert. */
            t-oh   = t-oh + fa-artikel.warenwert.
            t-depn = t-depn + fa-artikel.depn-wert - diff-wert. 
            t-book = t-book + fa-artikel.book-wert + diff-wert.
          END. 
        END. */

        IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
        DO: 
          t-anz     = t-anz + fa-artikel.anzahl.
          t-oh      = t-oh + fa-artikel.warenwert.
          t-book    = t-book + fa-artikel.book-wert.
        END. 
        ELSE IF fa-artikel.anz-depn - diff-n > 0 THEN 
        DO: 
          FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK. 
          IF (fa-kateg.methode = 0) THEN 
          DO: 
            diff-wert = (p-book-wert / sub-depn) * diff-n. 
            IF diff-wert = ? THEN diff-wert = 0.
            t-anz  = t-anz + fa-artikel.anzahl.
            t-oh   = t-oh + fa-artikel.warenwert.
            t-depn = t-depn + p-depn-wert - diff-wert. 
            t-book = t-book + p-book-wert + diff-wert.
          END. 
        END.
      END.
  END. /*end*/
  ELSE DO:
      FOR EACH mathis WHERE mathis.datum GE from-date
        AND mathis.datum LE to-date NO-LOCK, 
       FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
         AND fa-artikel.loeschflag = 0
        /*AND fa-artikel.loeschflag = 0 AND (fa-artikel.anz-depn - diff-n) GE 0 */
        NO-LOCK BY fa-artikel.fibukonto: 
            
        /*IF curr-acct = "" THEN curr-acct = fa-artikel.fibukonto.*/
        IF curr-acct NE fa-artikel.fibukonto THEN 
        DO: 
          ASSIGN
              tot-anz  = tot-anz + t-anz
              tot-oh   = tot-oh + t-oh
              tot-depn = tot-depn + t-depn
              tot-book = tot-book + t-book.
            
         
          FIND FIRST gl-acct WHERE gl-acct.fibukonto = curr-acct NO-LOCK NO-ERROR. 
          IF AVAILABLE gl-acct THEN RUN convert-fibu(curr-acct, OUTPUT fibu). 
    
          IF curr-acct NE "" THEN DO:              
              
              CREATE str-list.
              ASSIGN
                   str-list.location  = ""
                   str-list.s = STRING("SUBTOTAL ", "x(13)") 
                    /*+ STRING(gl-acct.bezeich, "x(48)") */
                    + STRING(" ", "x(48)") 
                    + "        "
                    + STRING(t-anz,">>,>>9")
                    + STRING(t-oh, ">>>,>>>,>>>,>>9.99") 
                    + STRING(t-depn, ">>>,>>>,>>>,>>9.99")
                    + STRING(t-book, "  >>>,>>>,>>>,>>9.99"). 
    
              CREATE str-list.
    
          END.
    
          /*CREATE str-list. 
          ASSIGN str-list.s = STRING(fibu, "x(13)") 
            + STRING(" ", "x(48)") 
            + STRING(" ","x(10)")
            + STRING(" ","x(6)")
            + STRING(0, ">>>,>>>,>>>,>>9.99") 
            + STRING(0, ">>>,>>>,>>>,>>9.99"). */
    
           ASSIGN
              curr-acct = fa-artikel.fibukonto
              t-anz     = 0
              t-oh      = 0 
              t-depn    = 0
              t-book    = 0. 
          
        END.

        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-artikel.fibukonto NO-LOCK NO-ERROR. 
        RUN convert-fibu(fa-artikel.fibukonto, OUTPUT fibu). 
        
        FIND FIRST str-list WHERE SUBSTRING(str-list.s,1,13) = fibu NO-ERROR.
        IF AVAILABLE str-list THEN DO:
            CREATE str-list. 
            ASSIGN 
                
                str-list.refno    = mathis.asset 
                str-list.location = trim(mathis.location)
                str-list.s = STRING(" ", "x(13)") 
                             + STRING(mathis.name, "x(48)") 
                             + STRING(mathis.datum) 
                             + STRING(fa-artikel.anzahl,">>,>>9"). 
    
        END.
        ELSE DO:
            CREATE str-list. 
            ASSIGN 
                
                str-list.refno    = mathis.asset 
                str-list.location = trim(mathis.location) 
                str-list.s = STRING(fibu, "x(13)") 
                             + STRING(mathis.name, "x(48)") 
                             + STRING(mathis.datum) 
                             + STRING(fa-artikel.anzahl,">>,>>9"). 
    
    
        END.
    
        /*ITA 160214*/    
        IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
        DO: 
            str-list.s = str-list.s 
                 + STRING(fa-artikel.warenwert, ">>>,>>>,>>>,>>9.99") 
                 + STRING(0, ">>>,>>>,>>>,>>9.99") 
                 + STRING(fa-artikel.warenwert, ">,>>>,>>>,>>>,>>9.99"). 
        END. 
        ELSE 
        DO: 
            str-list.s = str-list.s 
                 + STRING(fa-artikel.warenwert, ">>>,>>>,>>>,>>9.99") 
                 + STRING(fa-artikel.depn-wert - diff-wert, ">>>,>>>,>>>,>>9.99") 
                 + STRING(fa-artikel.book-wert + diff-wert, "  >>>,>>>,>>>,>>9.99"). 
        END. 
     
        IF fa-artikel.first-depn NE ? THEN 
           str-list.s = str-list.s + STRING(fa-artikel.first-depn). 
        ELSE str-list.s = str-list.s + "        ". 
        IF fa-artikel.next-depn NE ? THEN 
           str-list.s = str-list.s + STRING(fa-artikel.next-depn). 
        ELSE str-list.s = str-list.s + "        ". 
        IF fa-artikel.last-depn NE ? THEN 
           str-list.s = str-list.s + STRING(fa-artikel.last-depn). 
        ELSE str-list.s = str-list.s + "        ". 
        IF fa-artikel.anz-depn NE ? THEN 
            str-list.s = str-list.s + STRING(fa-artikel.anz-depn). 
        ELSE str-list.s = str-list.s + "   ". /*end*/
        
        /*ragung 34E4EB*/
        t-anz  = t-anz + fa-artikel.anzahl.
        t-oh   = t-oh + fa-artikel.warenwert.
        /*end*/

        IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
        DO: 
          /*t-anz  = t-anz + fa-artikel.anzahl.
          t-oh   = t-oh + fa-artikel.warenwert.*/
          t-book = t-book + fa-artikel.book-wert.
          
        END. 
        ELSE IF fa-artikel.anz-depn - diff-n > 0 THEN 
        DO: 
          FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK. 
          IF (fa-kateg.methode = 0) THEN 
          DO: 
            diff-wert = (fa-artikel.depn-wert / fa-artikel.anz-depn) * diff-n. 
            /*t-oh = t-oh + fa-artikel.book-wert + diff-wert. */
            IF diff-wert = ? THEN diff-wert = 0.
            /*t-anz   = t-anz + fa-artikel.anzahl.
            t-oh    = t-oh + fa-artikel.warenwert.*/
            t-depn  = t-depn + fa-artikel.depn-wert - diff-wert. 
            t-book  = t-book + fa-artikel.book-wert + diff-wert.            
          END. 
        END. 
      END.
  END.
 
  tot-anz   = tot-anz + t-anz.
  tot-oh    = tot-oh + t-oh. 
  tot-depn  = tot-depn + t-depn.
  tot-book  = tot-book + t-book.

  FIND FIRST gl-acct WHERE gl-acct.fibukonto = curr-acct NO-LOCK NO-ERROR. 
  RUN convert-fibu(curr-acct, OUTPUT fibu). 
  /*CREATE str-list. 
  ASSIGN str-list.s = STRING(fibu, "x(13)") 
    + STRING(gl-acct.bezeich, "x(48)")
    + STRING(" ","x(10)")
    + STRING(" ","x(6)")
    + STRING(t-oh, ">>>,>>>,>>>,>>9.99") 
    + STRING(t-depn, ">>>,>>>,>>>,>>9.99"). */

  CREATE str-list. 
  ASSIGN str-list.s = STRING("SUBTOTAL ", "x(13)") 
    + STRING(gl-acct.bezeich, "x(48)") 
    + "        "
    + STRING(t-anz,">>,>>9")
    + STRING(t-oh, ">>>,>>>,>>>,>>9.99") 
    + STRING(t-depn, ">>>,>>>,>>>,>>9.99")
    + STRING(t-book, "  >>>,>>>,>>>,>>9.99"). 


  CREATE str-list. 
  ASSIGN str-list.s = STRING("", "x(13)") 
    + STRING(translateExtended("T O T A L", lvCAREA, ""), "x(48)") 
    + "        "
    + STRING(tot-anz,">>,>>9").
/*
  IF LENGTH(TRIM(STRING(tot-oh, ">>>,>>>,>>>,>>9.99"))) GT 17 THEN
  str-list.s = str-list.s + STRING(tot-oh, ">,>>>,>>>,>>>,>>9.99") .
  ELSE str-list.s = str-list.s 
    + STRING(tot-depn, ">>,>>>,>>>,>>9.99"). 
*/

 IF LENGTH(TRIM(STRING(tot-oh, ">>>,>>>,>>>,>>9.99"))) GT 18 THEN
    str-list.s = str-list.s + STRING(tot-oh, ">>>,>>>,>>>,>>9.99") .
  ELSE str-list.s = str-list.s + STRING(tot-oh, ">>>,>>>,>>>,>>9.99") .
 IF LENGTH(TRIM(STRING(tot-depn, ">>>,>>>,>>>,>>9.99"))) GT 18 THEN
    str-list.s = str-list.s + STRING(tot-depn, ">>>,>>>,>>>,>>9.99") .
 ELSE str-list.s = str-list.s + STRING(tot-depn, ">>>,>>>,>>>,>>9.99") .
 IF LENGTH(TRIM(STRING(tot-book, ">>>,>>>,>>>,>>9.99"))) GT 18 THEN
    str-list.s = str-list.s + STRING(tot-book, "  >>>,>>>,>>>,>>9.99") .
 ELSE str-list.s = str-list.s + STRING(tot-book, "  >>>,>>>,>>>,>>9.99") .
END. 

PROCEDURE convert-fibu: 
DEFINE INPUT PARAMETER konto AS CHAR. 
DEFINE OUTPUT PARAMETER s AS CHAR INITIAL "". 
DEFINE VARIABLE ch AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 977 NO-LOCK.
  ch = htparam.fchar.
  j = 0. 
  DO i = 1 TO length(ch): 
    IF SUBSTR(ch, i, 1) GE "0" AND SUBSTR(ch, i, 1) LE  "9" THEN 
    DO: 
      j = j + 1. 
      s = s + SUBSTR(konto, j, 1). 
    END. 
    ELSE s = s + SUBSTR(ch, i, 1). 
  END. 
END. 


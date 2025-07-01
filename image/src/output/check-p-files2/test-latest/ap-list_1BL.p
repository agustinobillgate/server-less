DEFINE TEMP-TABLE output-list 
  FIELD betriebsnr  AS INTEGER INITIAL 0 
  FIELD ap-recid    AS INTEGER INITIAL 0 
  FIELD curr-pay    AS DECIMAL 
  FIELD lscheinnr   AS CHAR
  FIELD STR         AS CHAR
  FIELD steuercode  AS INTEGER /*FD*/ 
  FIELD recv-date   AS DATE /*gerald*/
  .

DEF INPUT  PARAMETER from-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF INPUT  PARAMETER lastname       AS CHAR.
DEF INPUT  PARAMETER sorttype       AS INT.
DEF INPUT  PARAMETER price-decimal  AS INT.
DEF INPUT  PARAMETER check-disp     AS INTEGER. /* Gerald 130220 */
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE t-ap    AS DECIMAL. 
DEFINE VARIABLE t-pay   AS DECIMAL. 
DEFINE VARIABLE t-bal   AS DECIMAL. 
DEFINE VARIABLE tot-ap  AS DECIMAL. 
DEFINE VARIABLE tot-pay AS DECIMAL. 
DEFINE VARIABLE tot-bal AS DECIMAL. 
DEFINE VARIABLE i       AS INTEGER. 

IF from-date = ? AND to-date = ? THEN RUN disp-it.
ELSE IF from-date = ? AND to-date NE ? THEN RUN disp-it0.
ELSE RUN disp-it1.

PROCEDURE disp-it: 
DEFINE VARIABLE curr-firma  AS CHAR INITIAL "". 
DEFINE VARIABLE s2          AS CHAR. 
DEFINE VARIABLE d2          AS CHAR. 
DEFINE VARIABLE curr-pay    AS DECIMAL. 
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
DEFINE BUFFER l-ap FOR l-kredit.
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  t-ap = 0. 
  t-pay = 0. 
  t-bal = 0. 
  tot-ap = 0. 
  tot-pay = 0. 
  tot-bal = 0. 
  IF lastname = "" THEN 
  DO: 
    IF check-disp = 0 THEN
    DO:
      FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.zahlkonto = 0 
        AND l-kredit.opart = sorttype 
        AND l-kredit.counter GE 0 AND l-kredit.netto NE 0 
        NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 

        do-it = YES.
        IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
  
        IF do-it THEN
        DO:
          IF curr-firma = "" THEN curr-firma = l-lieferant.firma. 
          IF curr-firma NE l-lieferant.firma THEN 
          DO: 
            create output-list. 
            DO i = 1 TO 53: 
              output-list.str = output-list.str + " ". 
            END. 
            output-list.str = output-list.str + "T O T A L     ". 
            IF price-decimal = 0 THEN output-list.str = output-list.str 
              + STRING(t-ap,  "->,>>>,>>>,>>>,>>9") 
              + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
              + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
            ELSE output-list.str = output-list.str 
              + STRING(t-ap,  "->>,>>>,>>>,>>9.99") 
              + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
              + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
            t-ap = 0. 
            t-pay = 0. 
            t-bal = 0. 
            curr-firma = l-lieferant.firma. 
          END. 
          curr-pay = 0. 
          IF l-kredit.counter GT 0 THEN 
          DO: 
            FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
              AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
              BY l-ap.rgdatum: 
              curr-pay = curr-pay - l-ap.saldo. 
              d2 = STRING(l-ap.rgdatum). 
            END. 
          END. 
          IF curr-pay = 0 THEN d2 = "". 
          create output-list. 
          output-list.betriebsnr = l-kredit.betriebsnr. 
          output-list.ap-recid = RECID(l-kredit). 
          output-list.curr-pay = curr-pay. 
          output-list.steuercode = l-kredit.steuercode.
          output-list.str = output-list.str
              /*here*/
            + STRING(l-lieferant.firma, "x(26)") /*supplier Name */
            + STRING(l-kredit.rgdatum) /*Bill Date*/
            + STRING(l-kredit.name, "x(14)") /*docu number*/
            + STRING(l-kredit.lscheinnr, "x(19)"). /*deliver note*/
          output-list.lscheinnr = l-kredit.lscheinnr. 
          IF price-decimal = 0 THEN output-list.str = output-list.str 
            + STRING(l-kredit.netto, "->,>>>,>>>,>>>,>>9") /*amount*/ 
            + STRING(curr-pay, "->,>>>,>>>,>>>,>>9")       /*paid amount*/
            + STRING(d2,"x(8)") /*paid date*/
            + STRING(l-kredit.netto - curr-pay, "->,>>>,>>>,>>>,>>9") /*balance*/
            + STRING(l-kredit.rgdatum + l-kredit.ziel) /*due date*/ 
            + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
          ELSE output-list.str = output-list.str 
            + STRING(l-kredit.netto, "->>,>>>,>>>,>>9.99") 
            + STRING(curr-pay, "->>,>>>,>>>,>>9.99") 
            + STRING(d2,"x(8)") 
            + STRING(l-kredit.netto - curr-pay, "->>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.rgdatum + l-kredit.ziel)
            + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
          t-ap = t-ap + l-kredit.netto. 
          t-pay = t-pay + curr-pay. 
          t-bal = t-bal + l-kredit.netto - curr-pay. 
          tot-ap = tot-ap + l-kredit.netto. 
          tot-pay = tot-pay + curr-pay. 
          tot-bal = tot-bal + l-kredit.netto - curr-pay. 

          FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
              AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
              ASSIGN
                  output-list.recv-date = queasy.date1.
          END.
        END.
      END.
    END.
    ELSE IF check-disp = 1 THEN
    DO:
      FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.zahlkonto = 0 
        AND l-kredit.opart = sorttype 
        AND l-kredit.counter GE 0 AND l-kredit.netto NE 0 
        AND l-kredit.rechnr NE 0000000
        NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
  
        do-it = YES.
        IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
  
        IF do-it THEN
        DO:
          IF curr-firma = "" THEN curr-firma = l-lieferant.firma. 
          IF curr-firma NE l-lieferant.firma THEN 
          DO: 
            create output-list. 
            DO i = 1 TO 53: 
              output-list.str = output-list.str + " ". 
            END. 
            output-list.str = output-list.str + "T O T A L     ". 
            IF price-decimal = 0 THEN output-list.str = output-list.str 
              + STRING(t-ap,  "->,>>>,>>>,>>>,>>9") 
              + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
              + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
            ELSE output-list.str = output-list.str 
              + STRING(t-ap,  "->>,>>>,>>>,>>9.99") 
              + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
              + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
            t-ap = 0. 
            t-pay = 0. 
            t-bal = 0. 
            curr-firma = l-lieferant.firma. 
          END. 
          curr-pay = 0. 
          IF l-kredit.counter GT 0 THEN 
          DO: 
            FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
              AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
              BY l-ap.rgdatum: 
              curr-pay = curr-pay - l-ap.saldo. 
              d2 = STRING(l-ap.rgdatum). 
            END. 
          END. 
          IF curr-pay = 0 THEN d2 = "". 
          create output-list. 
          output-list.betriebsnr = l-kredit.betriebsnr. 
          output-list.ap-recid = RECID(l-kredit). 
          output-list.curr-pay = curr-pay.
          output-list.steuercode = l-kredit.steuercode.
          output-list.str = output-list.str
              /*here*/
            + STRING(l-lieferant.firma, "x(26)") /*supplier Name */
            + STRING(l-kredit.rgdatum) /*Bill Date*/
            + STRING(l-kredit.name, "x(14)") /*docu number*/
            + STRING(l-kredit.lscheinnr, "x(19)"). /*deliver note*/
          output-list.lscheinnr = l-kredit.lscheinnr. 
          IF price-decimal = 0 THEN output-list.str = output-list.str 
            + STRING(l-kredit.netto, "->,>>>,>>>,>>>,>>9") /*amount*/ 
            + STRING(curr-pay, "->,>>>,>>>,>>>,>>9")       /*paid amount*/
            + STRING(d2,"x(8)") /*paid date*/
            + STRING(l-kredit.netto - curr-pay, "->,>>>,>>>,>>>,>>9") /*balance*/
            + STRING(l-kredit.rgdatum + l-kredit.ziel) /*due date*/ 
            + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
          ELSE output-list.str = output-list.str 
            + STRING(l-kredit.netto, "->>,>>>,>>>,>>9.99") 
            + STRING(curr-pay, "->>,>>>,>>>,>>9.99") 
            + STRING(d2,"x(8)") 
            + STRING(l-kredit.netto - curr-pay, "->>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.rgdatum + l-kredit.ziel)
            + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
          t-ap = t-ap + l-kredit.netto. 
          t-pay = t-pay + curr-pay. 
          t-bal = t-bal + l-kredit.netto - curr-pay. 
          tot-ap = tot-ap + l-kredit.netto. 
          tot-pay = tot-pay + curr-pay. 
          tot-bal = tot-bal + l-kredit.netto - curr-pay. 

          FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
              AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
              ASSIGN
                  output-list.recv-date = queasy.date1.
          END.
        END.
      END.
    END.
    ELSE
    DO:
      FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.zahlkonto = 0 
        AND l-kredit.opart = sorttype 
        AND l-kredit.counter GE 0 AND l-kredit.netto NE 0 
        NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 

        FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
              AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
          do-it = YES.
          IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    
          IF do-it THEN
          DO:
            IF curr-firma = "" THEN curr-firma = l-lieferant.firma. 
            IF curr-firma NE l-lieferant.firma THEN 
            DO: 
              create output-list. 
              DO i = 1 TO 53: 
                output-list.str = output-list.str + " ". 
              END. 
              output-list.str = output-list.str + "T O T A L     ". 
              IF price-decimal = 0 THEN output-list.str = output-list.str 
                + STRING(t-ap,  "->,>>>,>>>,>>>,>>9") 
                + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
                + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
              ELSE output-list.str = output-list.str 
                + STRING(t-ap,  "->>,>>>,>>>,>>9.99") 
                + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
                + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
              t-ap = 0. 
              t-pay = 0. 
              t-bal = 0. 
              curr-firma = l-lieferant.firma. 
            END. 
            curr-pay = 0. 
            IF l-kredit.counter GT 0 THEN 
            DO: 
              FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
                AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
                BY l-ap.rgdatum: 
                curr-pay = curr-pay - l-ap.saldo. 
                d2 = STRING(l-ap.rgdatum). 
              END. 
            END. 
            IF curr-pay = 0 THEN d2 = "". 
            create output-list. 
            output-list.betriebsnr = l-kredit.betriebsnr. 
            output-list.ap-recid = RECID(l-kredit). 
            output-list.curr-pay = curr-pay.
            output-list.steuercode = l-kredit.steuercode.
            output-list.recv-date = queasy.date1.
            output-list.str = output-list.str
                /*here*/
              + STRING(l-lieferant.firma, "x(26)") /*supplier Name */
              + STRING(l-kredit.rgdatum) /*Bill Date*/
              + STRING(l-kredit.name, "x(14)") /*docu number*/
              + STRING(l-kredit.lscheinnr, "x(19)"). /*deliver note*/
            output-list.lscheinnr = l-kredit.lscheinnr. 
            IF price-decimal = 0 THEN output-list.str = output-list.str 
              + STRING(l-kredit.netto, "->,>>>,>>>,>>>,>>9") /*amount*/ 
              + STRING(curr-pay, "->,>>>,>>>,>>>,>>9")       /*paid amount*/
              + STRING(d2,"x(8)") /*paid date*/
              + STRING(l-kredit.netto - curr-pay, "->,>>>,>>>,>>>,>>9") /*balance*/
              + STRING(l-kredit.rgdatum + l-kredit.ziel) /*due date*/ 
              + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
            ELSE output-list.str = output-list.str 
              + STRING(l-kredit.netto, "->>,>>>,>>>,>>9.99") 
              + STRING(curr-pay, "->>,>>>,>>>,>>9.99") 
              + STRING(d2,"x(8)") 
              + STRING(l-kredit.netto - curr-pay, "->>,>>>,>>>,>>9.99") 
              + STRING(l-kredit.rgdatum + l-kredit.ziel)
              + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
            t-ap = t-ap + l-kredit.netto. 
            t-pay = t-pay + curr-pay. 
            t-bal = t-bal + l-kredit.netto - curr-pay. 
            tot-ap = tot-ap + l-kredit.netto. 
            tot-pay = tot-pay + curr-pay. 
            tot-bal = tot-bal + l-kredit.netto - curr-pay.
          END.
        END.
      END.
    END.
    
    create output-list. 
    DO i = 1 TO 53: 
      output-list.str = output-list.str + " ". 
    END. 
    output-list.str = output-list.str + "T O T A L     ". 
    IF price-decimal = 0 THEN output-list.str = output-list.str 
      + STRING(t-ap, "->,>>>,>>>,>>>,>>9") 
      + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
      + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
    ELSE output-list.str = output-list.str 
      + STRING(t-ap, "->>,>>>,>>>,>>9.99") 
      + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
      + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
    create output-list. 
    create output-list. 
    DO i = 1 TO 53: 
      output-list.str = output-list.str + " ". 
    END. 
    output-list.str = output-list.str + "GRAND TOTAL   ". 
    IF price-decimal = 0 THEN output-list.str = output-list.str 
      + STRING(tot-ap, "->,>>>,>>>,>>>,>>9") 
      + STRING(tot-pay, "->,>>>,>>>,>>>,>>9") + "        " 
      + STRING(tot-bal, "->,>>>,>>>,>>>,>>9"). 
    ELSE output-list.str = output-list.str 
      + STRING(tot-ap, "->>,>>>,>>>,>>9.99") 
      + STRING(tot-pay, "->>,>>>,>>>,>>9.99") + "        " 
      + STRING(tot-bal, "->>,>>>,>>>,>>9.99") + "        ". 
  END. 
  ELSE 
  DO: 
    do-it = NO.
    FIND FIRST l-lieferant WHERE l-lieferant.firma = lastname NO-LOCK NO-ERROR. 
    IF AVAILABLE l-lieferant THEN 
    DO:
        IF segm = 0 THEN do-it = YES.
        ELSE do-it = l-lieferant.segment1 = segm.
    END.
    IF do-it THEN
    DO: 
      FOR EACH l-kredit WHERE l-kredit.lief-nr = l-lieferant.lief-nr 
        AND l-kredit.zahlkonto = 0 AND l-kredit.opart = sorttype 
        AND l-kredit.counter GE 0 AND l-kredit.netto NE 0 
        NO-LOCK USE-INDEX counter_ix BY l-kredit.rgdatum: 
        curr-pay = 0. 
        IF l-kredit.counter GT 0 THEN 
        DO: 
          FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
            BY l-ap.rgdatum: 
            curr-pay = curr-pay - l-ap.saldo. 
            d2 = STRING(l-ap.rgdatum). 
          END. 
        END. 
        IF curr-pay = 0 THEN d2 = "". 
        create output-list. 
        output-list.betriebsnr = l-kredit.betriebsnr. 
        output-list.ap-recid = RECID(l-kredit). 
        output-list.curr-pay = curr-pay. 
        output-list.steuercode = l-kredit.steuercode.
        output-list.str = output-list.str 
          + STRING(l-lieferant.firma, "x(26)") 
          + STRING(l-kredit.rgdatum) 
          + STRING(l-kredit.name, "x(14)") 
          + STRING(l-kredit.lscheinnr, "x(19)"). 
        output-list.lscheinnr = l-kredit.lscheinnr. 
        IF price-decimal = 0 THEN output-list.str = output-list.str 
          + STRING(l-kredit.netto, "->,>>>,>>>,>>>,>>9") 
          + STRING(curr-pay, "->,>>>,>>>,>>>,>>9") 
          + STRING(d2, "x(8)") 
          + STRING(l-kredit.netto - curr-pay, "->,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.rgdatum + l-kredit.ziel)
          + STRING(l-kredit.rechnr, "9999999").     /* voucher no */ /* Gerald 130220 */
        ELSE output-list.str = output-list.str 
          + STRING(l-kredit.netto, "->>,>>>,>>>,>>9.99") 
          + STRING(curr-pay, "->>,>>>,>>>,>>9.99") 
          + STRING(d2, "x(8)") 
          + STRING(l-kredit.netto - curr-pay, "->>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.rgdatum + l-kredit.ziel)
          + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
        t-ap = t-ap + l-kredit.netto. 
        t-pay = t-pay + curr-pay. 
        t-bal = t-bal + l-kredit.netto - curr-pay. 

        FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
            AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN
                output-list.recv-date = queasy.date1.
        END.
      END. 
      create output-list. 
      DO i = 1 TO 53: 
        output-list.str = output-list.str + " ". 
      END. 
      output-list.str = output-list.str + "T O T A L     ". 
      IF price-decimal = 0 THEN output-list.str = output-list.str 
        + STRING(t-ap, "->,>>>,>>>,>>>,>>9") 
        + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
        + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
      ELSE output-list.str = output-list.str 
        + STRING(t-ap, "->>,>>>,>>>,>>9.99") 
        + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
        + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
    END. 
  END.
END. 


PROCEDURE disp-it0: 
DEFINE VARIABLE curr-firma  AS CHAR INITIAL "". 
DEFINE VARIABLE s2          AS CHAR. 
DEFINE VARIABLE d2          AS CHAR. 
DEFINE VARIABLE curr-pay    AS DECIMAL. 
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
DEFINE BUFFER l-ap FOR l-kredit. 

  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  t-ap = 0. 
  t-pay = 0. 
  t-bal = 0. 
  tot-ap = 0. 
  tot-pay = 0. 
  tot-bal = 0. 
 
  IF lastname = "" THEN 
  DO: 
    IF check-disp = 0 THEN
    DO:
      FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.zahlkonto = 0 
        AND l-kredit.opart = sorttype AND l-kredit.rgdatum LE to-date 
        AND l-kredit.counter GE 0 AND l-kredit.netto NE 0 
        NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
  
        do-it = YES.
        IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
  
        IF do-it THEN
        DO:
          IF curr-firma = "" THEN curr-firma = l-lieferant.firma. 
          IF curr-firma NE l-lieferant.firma THEN 
          DO: 
            create output-list. 
            DO i = 1 TO 53: 
              output-list.str = output-list.str + " ". 
            END. 
            output-list.str = output-list.str + "T O T A L     ". 
           IF price-decimal = 0 THEN output-list.str = output-list.str 
              + STRING(t-ap, "->,>>>,>>>,>>>,>>9") 
              + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
              + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
            ELSE output-list.str = output-list.str 
              + STRING(t-ap, "->>,>>>,>>>,>>9.99") 
              + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
              + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
            t-ap = 0. 
            t-pay = 0. 
            t-bal = 0. 
            curr-firma = l-lieferant.firma. 
          END. 
          curr-pay = 0. 
          IF l-kredit.counter GT 0 THEN 
          DO: 
            FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
              AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
              BY l-ap.rgdatum: 
              curr-pay = curr-pay - l-ap.saldo. 
              d2 = STRING(l-ap.rgdatum). 
            END. 
          END. 
          IF curr-pay = 0 THEN d2 = "". 
          create output-list. 
          output-list.betriebsnr = l-kredit.betriebsnr. 
          output-list.ap-recid = RECID(l-kredit). 
          output-list.curr-pay = curr-pay. 
          output-list.steuercode = l-kredit.steuercode.
          output-list.str = output-list.str 
            + STRING(l-lieferant.firma, "x(26)") 
            + STRING(l-kredit.rgdatum) 
            + STRING(l-kredit.name, "x(14)") 
            + STRING(l-kredit.lscheinnr, "x(19)"). 
          output-list.lscheinnr = l-kredit.lscheinnr. 
          IF price-decimal = 0 THEN output-list.str = output-list.str 
            + STRING(l-kredit.netto, "->,>>>,>>>,>>>,>>9") 
            + STRING(curr-pay, "->,>>>,>>>,>>>,>>9") 
            + STRING(d2,"x(8)") 
            + STRING(l-kredit.netto - curr-pay, "->,>>>,>>>,>>>,>>9") 
            + STRING(l-kredit.rgdatum + l-kredit.ziel)
            + STRING(l-kredit.rechnr, "9999999").     /* voucher no */ /* Gerald 130220 */
          ELSE output-list.str = output-list.str 
            + STRING(l-kredit.netto, "->>,>>>,>>>,>>9.99") 
            + STRING(curr-pay, "->>,>>>,>>>,>>9.99") 
            + STRING(d2,"x(8)") 
            + STRING(l-kredit.netto - curr-pay, "->>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.rgdatum + l-kredit.ziel)
            + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
          t-ap = t-ap + l-kredit.netto. 
          t-pay = t-pay + curr-pay. 
          t-bal = t-bal + l-kredit.netto - curr-pay. 
          tot-ap = tot-ap + l-kredit.netto. 
          tot-pay = tot-pay + curr-pay. 
          tot-bal = tot-bal + l-kredit.netto - curr-pay. 

          FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
              AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
              ASSIGN
                  output-list.recv-date = queasy.date1.
          END.
        END.
      END.
    END.
    ELSE IF check-disp = 1 THEN
    DO:
      FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.zahlkonto = 0 
        AND l-kredit.opart = sorttype AND l-kredit.rgdatum LE to-date 
        AND l-kredit.counter GE 0 AND l-kredit.netto NE 0 
        AND l-kredit.rechnr NE 0000000
        NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
  
        do-it = YES.
        IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
  
        IF do-it THEN
        DO:
          IF curr-firma = "" THEN curr-firma = l-lieferant.firma. 
          IF curr-firma NE l-lieferant.firma THEN 
          DO: 
            create output-list. 
            DO i = 1 TO 53: 
              output-list.str = output-list.str + " ". 
            END. 
            output-list.str = output-list.str + "T O T A L     ". 
           IF price-decimal = 0 THEN output-list.str = output-list.str 
              + STRING(t-ap, "->,>>>,>>>,>>>,>>9") 
              + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
              + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
            ELSE output-list.str = output-list.str 
              + STRING(t-ap, "->>,>>>,>>>,>>9.99") 
              + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
              + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
            t-ap = 0. 
            t-pay = 0. 
            t-bal = 0. 
            curr-firma = l-lieferant.firma. 
          END. 
          curr-pay = 0. 
          IF l-kredit.counter GT 0 THEN 
          DO: 
            FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
              AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
              BY l-ap.rgdatum: 
              curr-pay = curr-pay - l-ap.saldo. 
              d2 = STRING(l-ap.rgdatum). 
            END. 
          END. 
          IF curr-pay = 0 THEN d2 = "". 
          create output-list. 
          output-list.betriebsnr = l-kredit.betriebsnr. 
          output-list.ap-recid = RECID(l-kredit). 
          output-list.curr-pay = curr-pay. 
          output-list.steuercode = l-kredit.steuercode.
          output-list.str = output-list.str 
            + STRING(l-lieferant.firma, "x(26)") 
            + STRING(l-kredit.rgdatum) 
            + STRING(l-kredit.name, "x(14)") 
            + STRING(l-kredit.lscheinnr, "x(19)"). 
          output-list.lscheinnr = l-kredit.lscheinnr. 
          IF price-decimal = 0 THEN output-list.str = output-list.str 
            + STRING(l-kredit.netto, "->,>>>,>>>,>>>,>>9") 
            + STRING(curr-pay, "->,>>>,>>>,>>>,>>9") 
            + STRING(d2,"x(8)") 
            + STRING(l-kredit.netto - curr-pay, "->,>>>,>>>,>>>,>>9") 
            + STRING(l-kredit.rgdatum + l-kredit.ziel)
            + STRING(l-kredit.rechnr, "9999999").     /* voucher no */ /* Gerald 130220 */
          ELSE output-list.str = output-list.str 
            + STRING(l-kredit.netto, "->>,>>>,>>>,>>9.99") 
            + STRING(curr-pay, "->>,>>>,>>>,>>9.99") 
            + STRING(d2,"x(8)") 
            + STRING(l-kredit.netto - curr-pay, "->>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.rgdatum + l-kredit.ziel)
            + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
          t-ap = t-ap + l-kredit.netto. 
          t-pay = t-pay + curr-pay. 
          t-bal = t-bal + l-kredit.netto - curr-pay. 
          tot-ap = tot-ap + l-kredit.netto. 
          tot-pay = tot-pay + curr-pay. 
          tot-bal = tot-bal + l-kredit.netto - curr-pay. 

          FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
              AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
              ASSIGN
                  output-list.recv-date = queasy.date1.
          END.
        END.
      END.
    END.
    ELSE
    DO:
      FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.zahlkonto = 0 
        AND l-kredit.opart = sorttype AND l-kredit.rgdatum LE to-date 
        AND l-kredit.counter GE 0 AND l-kredit.netto NE 0 
        NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 

        FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
              AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
          do-it = YES.
          IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    
          IF do-it THEN
          DO:
            IF curr-firma = "" THEN curr-firma = l-lieferant.firma. 
            IF curr-firma NE l-lieferant.firma THEN 
            DO: 
              create output-list. 
              DO i = 1 TO 53: 
                output-list.str = output-list.str + " ". 
              END. 
              output-list.str = output-list.str + "T O T A L     ". 
             IF price-decimal = 0 THEN output-list.str = output-list.str 
                + STRING(t-ap, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
                + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
              ELSE output-list.str = output-list.str 
                + STRING(t-ap, "->>,>>>,>>>,>>9.99") 
                + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
                + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
              t-ap = 0. 
              t-pay = 0. 
              t-bal = 0. 
              curr-firma = l-lieferant.firma. 
            END. 
            curr-pay = 0. 
            IF l-kredit.counter GT 0 THEN 
            DO: 
              FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
                AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
                BY l-ap.rgdatum: 
                curr-pay = curr-pay - l-ap.saldo. 
                d2 = STRING(l-ap.rgdatum). 
              END. 
            END. 
            IF curr-pay = 0 THEN d2 = "". 
            create output-list. 
            output-list.betriebsnr = l-kredit.betriebsnr. 
            output-list.ap-recid = RECID(l-kredit). 
            output-list.curr-pay = curr-pay. 
            output-list.steuercode = l-kredit.steuercode.
            output-list.recv-date  = queasy.date1.
            output-list.str = output-list.str 
              + STRING(l-lieferant.firma, "x(26)") 
              + STRING(l-kredit.rgdatum) 
              + STRING(l-kredit.name, "x(14)") 
              + STRING(l-kredit.lscheinnr, "x(19)"). 
            output-list.lscheinnr = l-kredit.lscheinnr. 
            IF price-decimal = 0 THEN output-list.str = output-list.str 
              + STRING(l-kredit.netto, "->,>>>,>>>,>>>,>>9") 
              + STRING(curr-pay, "->,>>>,>>>,>>>,>>9") 
              + STRING(d2,"x(8)") 
              + STRING(l-kredit.netto - curr-pay, "->,>>>,>>>,>>>,>>9") 
              + STRING(l-kredit.rgdatum + l-kredit.ziel)
              + STRING(l-kredit.rechnr, "9999999").     /* voucher no */ /* Gerald 130220 */
            ELSE output-list.str = output-list.str 
              + STRING(l-kredit.netto, "->>,>>>,>>>,>>9.99") 
              + STRING(curr-pay, "->>,>>>,>>>,>>9.99") 
              + STRING(d2,"x(8)") 
              + STRING(l-kredit.netto - curr-pay, "->>,>>>,>>>,>>9.99") 
              + STRING(l-kredit.rgdatum + l-kredit.ziel)
              + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
            t-ap = t-ap + l-kredit.netto. 
            t-pay = t-pay + curr-pay. 
            t-bal = t-bal + l-kredit.netto - curr-pay. 
            tot-ap = tot-ap + l-kredit.netto. 
            tot-pay = tot-pay + curr-pay. 
            tot-bal = tot-bal + l-kredit.netto - curr-pay. 
          END.
        END.
      END.
    END.

    create output-list. 
    DO i = 1 TO 53: 
      output-list.str = output-list.str + " ". 
    END. 
    output-list.str = output-list.str + "T O T A L     ". 
    IF price-decimal = 0 THEN output-list.str = output-list.str 
      + STRING(t-ap, "->,>>>,>>>,>>>,>>9") 
      + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
      + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
    ELSE output-list.str = output-list.str 
      + STRING(t-ap, "->>,>>>,>>>,>>9.99") 
      + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
      + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
    create output-list. 
    create output-list. 
    DO i = 1 TO 53: 
      output-list.str = output-list.str + " ". 
    END. 
    output-list.str = output-list.str + "GRAND TOTAL   ". 
    IF price-decimal = 0 THEN output-list.str = output-list.str 
      + STRING(tot-ap, "->,>>>,>>>,>>>,>>9") 
      + STRING(tot-pay, "->,>>>,>>>,>>>,>>9") + "        " 
      + STRING(tot-bal, "->,>>>,>>>,>>>,>>9"). 
    ELSE output-list.str = output-list.str 
      + STRING(tot-ap, "->>,>>>,>>>,>>9.99") 
      + STRING(tot-pay, "->>,>>>,>>>,>>9.99") + "        " 
      + STRING(tot-bal, "->>,>>>,>>>,>>9.99") + "        ". 
  END. 
  ELSE 
  DO: 
    do-it = NO.
    FIND FIRST l-lieferant WHERE l-lieferant.firma = lastname NO-LOCK NO-ERROR. 
    IF AVAILABLE l-lieferant THEN 
    DO:
        IF segm = 0 THEN do-it = YES.
        ELSE do-it = l-lieferant.segment1 = segm.
    END.
    IF do-it THEN
    DO: 
      FOR EACH l-kredit WHERE l-kredit.lief-nr = l-lieferant.lief-nr 
        AND l-kredit.zahlkonto = 0 AND l-kredit.opart = sorttype 
        AND l-kredit.counter GE 0 AND l-kredit.netto NE 0 
        AND l-kredit.rgdatum LE to-date 
        NO-LOCK USE-INDEX counter_ix BY l-kredit.rgdatum: 
        curr-pay = 0. 
        IF l-kredit.counter GT 0 THEN 
        DO: 
          FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
            BY l-ap.rgdatum: 
            curr-pay = curr-pay - l-ap.saldo. 
            d2 = STRING(l-ap.rgdatum). 
          END. 
        END. 
        IF curr-pay = 0 THEN d2 = "". 
        create output-list. 
        output-list.betriebsnr = l-kredit.betriebsnr. 
        output-list.ap-recid = RECID(l-kredit). 
        output-list.curr-pay = curr-pay. 
        output-list.steuercode = l-kredit.steuercode.
        output-list.str = output-list.str 
          + STRING(l-lieferant.firma, "x(26)") 
          + STRING(l-kredit.rgdatum) 
          + STRING(l-kredit.name, "x(14)") 
          + STRING(l-kredit.lscheinnr, "x(19)"). 
        output-list.lscheinnr = l-kredit.lscheinnr. 
        IF price-decimal = 0 THEN output-list.str = output-list.str 
          + STRING(l-kredit.netto, "->,>>>,>>>,>>>,>>9") 
          + STRING(curr-pay, "->,>>>,>>>,>>>,>>9") 
          + STRING(d2, "x(8)") 
          + STRING(l-kredit.netto - curr-pay, "->,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.rgdatum + l-kredit.ziel)
          + STRING(l-kredit.rechnr, "9999999").     /* voucher no */ /* Gerald 130220 */
        ELSE output-list.str = output-list.str 
          + STRING(l-kredit.netto, "->>,>>>,>>>,>>9.99") 
          + STRING(curr-pay, "->>,>>>,>>>,>>9.99") 
          + STRING(d2, "x(8)") 
          + STRING(l-kredit.netto - curr-pay, "->>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.rgdatum + l-kredit.ziel)
          + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
        t-ap = t-ap + l-kredit.netto. 
        t-pay = t-pay + curr-pay. 
        t-bal = t-bal + l-kredit.netto - curr-pay. 

        FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
            AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN
                output-list.recv-date = queasy.date1.
        END.
      END. 
      create output-list. 
      DO i = 1 TO 53: 
        output-list.str = output-list.str + " ". 
      END. 
      output-list.str = output-list.str + "T O T A L     ". 
      IF price-decimal = 0 THEN output-list.str = output-list.str 
        + STRING(t-ap, "->,>>>,>>>,>>>,>>9") 
        + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
        + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
      ELSE output-list.str = output-list.str 
        + STRING(t-ap, "->>,>>>,>>>,>>9.99") 
        + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
        + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
    END. 
  END.
END. 
 
PROCEDURE disp-it1: 
DEFINE VARIABLE curr-firma  AS CHAR INITIAL "". 
DEFINE VARIABLE s2          AS CHAR. 
DEFINE VARIABLE d2          AS CHAR. 
DEFINE VARIABLE curr-pay    AS DECIMAL. 
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
DEFINE BUFFER l-ap FOR l-kredit.

  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  t-ap = 0. 
  t-pay = 0. 
  t-bal = 0. 
  tot-ap = 0. 
  tot-pay = 0. 
  tot-bal = 0. 
 
  IF lastname = "" THEN 
  DO: 
    IF check-disp = 0 THEN
    DO:
      FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.zahlkonto = 0 
        AND l-kredit.opart = sorttype AND l-kredit.rgdatum GE from-date 
        AND l-kredit.rgdatum LE to-date 
        AND l-kredit.counter GE 0 AND l-kredit.netto NE 0 
        NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
  
        do-it = YES.
        IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
  
        IF do-it THEN
        DO:
          IF curr-firma = "" THEN curr-firma = l-lieferant.firma. 
          IF curr-firma NE l-lieferant.firma THEN 
          DO: 
            create output-list. 
            DO i = 1 TO 53: 
              output-list.str = output-list.str + " ". 
            END. 
            output-list.str = output-list.str + "T O T A L     ". 
            IF price-decimal = 0 THEN output-list.str = output-list.str 
              + STRING(t-ap, "->,>>>,>>>,>>>,>>9") 
              + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
              + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
            ELSE output-list.str = output-list.str 
              + STRING(t-ap, "->>,>>>,>>>,>>9.99") 
              + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
              + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
            t-ap = 0. 
            t-pay = 0. 
            t-bal = 0. 
            curr-firma = l-lieferant.firma. 
          END. 
          curr-pay = 0. 
          IF l-kredit.counter GT 0 THEN 
          DO: 
            FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
              AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
              BY l-ap.rgdatum: 
              curr-pay = curr-pay - l-ap.saldo. 
              d2 = STRING(l-ap.rgdatum). 
            END. 
          END. 
          IF curr-pay = 0 THEN d2 = "". 
          create output-list. 
          output-list.betriebsnr = l-kredit.betriebsnr. 
          output-list.ap-recid = RECID(l-kredit). 
          output-list.curr-pay = curr-pay. 
          output-list.steuercode = l-kredit.steuercode.
          output-list.str = output-list.str 
            + STRING(l-lieferant.firma, "x(26)") 
            + STRING(l-kredit.rgdatum) 
            + STRING(l-kredit.name, "x(14)") 
            + STRING(l-kredit.lscheinnr, "x(19)"). 
          output-list.lscheinnr = l-kredit.lscheinnr. 
          IF price-decimal = 0 THEN output-list.str = output-list.str 
            + STRING(l-kredit.netto, "->,>>>,>>>,>>>,>>9") 
            + STRING(curr-pay, "->,>>>,>>>,>>>,>>9") 
            + STRING(d2,"x(8)") 
            + STRING(l-kredit.netto - curr-pay, "->,>>>,>>>,>>>,>>9") 
            + STRING(l-kredit.rgdatum + l-kredit.ziel)
            + STRING(l-kredit.rechnr, "9999999").     /* voucher no */ /* Gerald 130220 */
          ELSE output-list.str = output-list.str 
            + STRING(l-kredit.netto, "->>,>>>,>>>,>>9.99") 
            + STRING(curr-pay, "->>,>>>,>>>,>>9.99") 
            + STRING(d2,"x(8)") 
            + STRING(l-kredit.netto - curr-pay, "->>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.rgdatum + l-kredit.ziel)
            + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
          t-ap = t-ap + l-kredit.netto. 
          t-pay = t-pay + curr-pay. 
          t-bal = t-bal + l-kredit.netto - curr-pay. 
          tot-ap = tot-ap + l-kredit.netto. 
          tot-pay = tot-pay + curr-pay. 
          tot-bal = tot-bal + l-kredit.netto - curr-pay. 

          FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
              AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
              ASSIGN
                  output-list.recv-date = queasy.date1.
          END.
        END. 
      END.
    END.
    ELSE IF check-disp = 1 THEN
    DO:
      FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.zahlkonto = 0 
        AND l-kredit.opart = sorttype AND l-kredit.rgdatum GE from-date 
        AND l-kredit.rgdatum LE to-date 
        AND l-kredit.counter GE 0 AND l-kredit.netto NE 0 
        AND l-kredit.rechnr NE 0000000
        NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
  
        do-it = YES.
        IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
  
        IF do-it THEN
        DO:
          IF curr-firma = "" THEN curr-firma = l-lieferant.firma. 
          IF curr-firma NE l-lieferant.firma THEN 
          DO: 
            create output-list. 
            DO i = 1 TO 53: 
              output-list.str = output-list.str + " ". 
            END. 
            output-list.str = output-list.str + "T O T A L     ". 
            IF price-decimal = 0 THEN output-list.str = output-list.str 
              + STRING(t-ap, "->,>>>,>>>,>>>,>>9") 
              + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
              + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
            ELSE output-list.str = output-list.str 
              + STRING(t-ap, "->>,>>>,>>>,>>9.99") 
              + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
              + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
            t-ap = 0. 
            t-pay = 0. 
            t-bal = 0. 
            curr-firma = l-lieferant.firma. 
          END. 
          curr-pay = 0. 
          IF l-kredit.counter GT 0 THEN 
          DO: 
            FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
              AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
              BY l-ap.rgdatum: 
              curr-pay = curr-pay - l-ap.saldo. 
              d2 = STRING(l-ap.rgdatum). 
            END. 
          END. 
          IF curr-pay = 0 THEN d2 = "". 
          create output-list. 
          output-list.betriebsnr = l-kredit.betriebsnr. 
          output-list.ap-recid = RECID(l-kredit). 
          output-list.curr-pay = curr-pay. 
          output-list.steuercode = l-kredit.steuercode.
          output-list.str = output-list.str 
            + STRING(l-lieferant.firma, "x(26)") 
            + STRING(l-kredit.rgdatum) 
            + STRING(l-kredit.name, "x(14)") 
            + STRING(l-kredit.lscheinnr, "x(19)"). 
          output-list.lscheinnr = l-kredit.lscheinnr. 
          IF price-decimal = 0 THEN output-list.str = output-list.str 
            + STRING(l-kredit.netto, "->,>>>,>>>,>>>,>>9") 
            + STRING(curr-pay, "->,>>>,>>>,>>>,>>9") 
            + STRING(d2,"x(8)") 
            + STRING(l-kredit.netto - curr-pay, "->,>>>,>>>,>>>,>>9") 
            + STRING(l-kredit.rgdatum + l-kredit.ziel)
            + STRING(l-kredit.rechnr, "9999999").     /* voucher no */ /* Gerald 130220 */
          ELSE output-list.str = output-list.str 
            + STRING(l-kredit.netto, "->>,>>>,>>>,>>9.99") 
            + STRING(curr-pay, "->>,>>>,>>>,>>9.99") 
            + STRING(d2,"x(8)") 
            + STRING(l-kredit.netto - curr-pay, "->>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.rgdatum + l-kredit.ziel)
            + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
          t-ap = t-ap + l-kredit.netto. 
          t-pay = t-pay + curr-pay. 
          t-bal = t-bal + l-kredit.netto - curr-pay. 
          tot-ap = tot-ap + l-kredit.netto. 
          tot-pay = tot-pay + curr-pay. 
          tot-bal = tot-bal + l-kredit.netto - curr-pay. 

          FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
              AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
              ASSIGN
                  output-list.recv-date = queasy.date1.
          END.
        END. 
      END.
    END.
    ELSE 
    DO:
      FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.zahlkonto = 0 
        AND l-kredit.opart = sorttype AND l-kredit.rgdatum GE from-date 
        AND l-kredit.rgdatum LE to-date 
        AND l-kredit.counter GE 0 AND l-kredit.netto NE 0 
        NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 

        FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
              AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
          do-it = YES.
          IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    
          IF do-it THEN
          DO:
            IF curr-firma = "" THEN curr-firma = l-lieferant.firma. 
            IF curr-firma NE l-lieferant.firma THEN 
            DO: 
              create output-list. 
              DO i = 1 TO 53: 
                output-list.str = output-list.str + " ". 
              END. 
              output-list.str = output-list.str + "T O T A L     ". 
              IF price-decimal = 0 THEN output-list.str = output-list.str 
                + STRING(t-ap, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
                + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
              ELSE output-list.str = output-list.str 
                + STRING(t-ap, "->>,>>>,>>>,>>9.99") 
                + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
                + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
              t-ap = 0. 
              t-pay = 0. 
              t-bal = 0. 
              curr-firma = l-lieferant.firma. 
            END. 
            curr-pay = 0. 
            IF l-kredit.counter GT 0 THEN 
            DO: 
              FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
                AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
                BY l-ap.rgdatum: 
                curr-pay = curr-pay - l-ap.saldo. 
                d2 = STRING(l-ap.rgdatum). 
              END. 
            END. 
            IF curr-pay = 0 THEN d2 = "". 
            create output-list. 
            output-list.betriebsnr = l-kredit.betriebsnr. 
            output-list.ap-recid = RECID(l-kredit). 
            output-list.curr-pay = curr-pay. 
            output-list.steuercode = l-kredit.steuercode.
            output-list.str = output-list.str 
              + STRING(l-lieferant.firma, "x(26)") 
              + STRING(l-kredit.rgdatum) 
              + STRING(l-kredit.name, "x(14)") 
              + STRING(l-kredit.lscheinnr, "x(19)"). 
            output-list.lscheinnr = l-kredit.lscheinnr. 
            IF price-decimal = 0 THEN output-list.str = output-list.str 
              + STRING(l-kredit.netto, "->,>>>,>>>,>>>,>>9") 
              + STRING(curr-pay, "->,>>>,>>>,>>>,>>9") 
              + STRING(d2,"x(8)") 
              + STRING(l-kredit.netto - curr-pay, "->,>>>,>>>,>>>,>>9") 
              + STRING(l-kredit.rgdatum + l-kredit.ziel)
              + STRING(l-kredit.rechnr, "9999999").     /* voucher no */ /* Gerald 130220 */
            ELSE output-list.str = output-list.str 
              + STRING(l-kredit.netto, "->>,>>>,>>>,>>9.99") 
              + STRING(curr-pay, "->>,>>>,>>>,>>9.99") 
              + STRING(d2,"x(8)") 
              + STRING(l-kredit.netto - curr-pay, "->>,>>>,>>>,>>9.99") 
              + STRING(l-kredit.rgdatum + l-kredit.ziel)
              + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
            t-ap = t-ap + l-kredit.netto. 
            t-pay = t-pay + curr-pay. 
            t-bal = t-bal + l-kredit.netto - curr-pay. 
            tot-ap = tot-ap + l-kredit.netto. 
            tot-pay = tot-pay + curr-pay. 
            tot-bal = tot-bal + l-kredit.netto - curr-pay. 
          END. 
        END.
      END.
    END.

    create output-list. 
    DO i = 1 TO 53: 
      output-list.str = output-list.str + " ". 
    END. 
    output-list.str = output-list.str + "T O T A L     ". 
    IF price-decimal = 0 THEN output-list.str = output-list.str 
      + STRING(t-ap, "->,>>>,>>>,>>>,>>9") 
      + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
      + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
    ELSE output-list.str = output-list.str 
      + STRING(t-ap, "->>,>>>,>>>,>>9.99") 
      + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
      + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
    create output-list. 
    create output-list. 
    DO i = 1 TO 53: 
      output-list.str = output-list.str + " ". 
    END. 
    output-list.str = output-list.str + "GRAND TOTAL   ". 
    IF price-decimal = 0 THEN output-list.str = output-list.str 
      + STRING(tot-ap, "->,>>>,>>>,>>>,>>9") 
      + STRING(tot-pay, "->,>>>,>>>,>>>,>>9") + "        " 
      + STRING(tot-bal, "->,>>>,>>>,>>>,>>9"). 
    ELSE output-list.str = output-list.str 
      + STRING(tot-ap, "->>,>>>,>>>,>>9.99") 
      + STRING(tot-pay, "->>,>>>,>>>,>>9.99") + "        " 
      + STRING(tot-bal, "->>,>>>,>>>,>>9.99") + "        ". 
  END. 
  ELSE 
  DO: 
    do-it = NO.
    FIND FIRST l-lieferant WHERE l-lieferant.firma = lastname NO-LOCK NO-ERROR. 
    IF AVAILABLE l-lieferant THEN 
    DO:
        IF segm = 0 THEN do-it = YES.
        ELSE do-it = l-lieferant.segment1 = segm.
    END.
    IF do-it THEN
    DO: 
      FOR EACH l-kredit WHERE l-kredit.lief-nr = l-lieferant.lief-nr 
        AND l-kredit.zahlkonto = 0 AND l-kredit.opart = sorttype 
        AND l-kredit.counter GE 0 AND l-kredit.netto NE 0 
         AND l-kredit.rgdatum GE from-date AND l-kredit.rgdatum LE to-date 
        NO-LOCK USE-INDEX counter_ix BY l-kredit.rgdatum: 
        curr-pay = 0. 
        IF l-kredit.counter GT 0 THEN 
        DO: 
          FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
            BY l-ap.rgdatum: 
            curr-pay = curr-pay - l-ap.saldo. 
            d2 = STRING(l-ap.rgdatum). 
          END. 
        END. 
        IF curr-pay = 0 THEN d2 = "". 
        create output-list. 
        output-list.betriebsnr = l-kredit.betriebsnr. 
        output-list.ap-recid = RECID(l-kredit). 
        output-list.curr-pay = curr-pay. 
        output-list.steuercode = l-kredit.steuercode.
        output-list.str = output-list.str 
          + STRING(l-lieferant.firma, "x(26)") 
          + STRING(l-kredit.rgdatum) 
          + STRING(l-kredit.name, "x(14)") 
          + STRING(l-kredit.lscheinnr, "x(19)"). 
        output-list.lscheinnr = l-kredit.lscheinnr. 
        IF price-decimal = 0 THEN output-list.str = output-list.str 
          + STRING(l-kredit.netto, "->,>>>,>>>,>>>,>>9") 
          + STRING(curr-pay, "->,>>>,>>>,>>>,>>9") 
          + STRING(d2, "x(8)") 
          + STRING(l-kredit.netto - curr-pay, "->,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.rgdatum + l-kredit.ziel)
          + STRING(l-kredit.rechnr, "9999999").     /* voucher no */ /* Gerald 130220 */
        ELSE output-list.str = output-list.str 
          + STRING(l-kredit.netto, "->>,>>>,>>>,>>9.99") 
          + STRING(curr-pay, "->>,>>>,>>>,>>9.99") 
          + STRING(d2, "x(8)") 
          + STRING(l-kredit.netto - curr-pay, "->>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.rgdatum + l-kredit.ziel)
          + STRING(l-kredit.rechnr, "9999999").   /* voucher no */ /* Gerald 130220 */
        t-ap = t-ap + l-kredit.netto. 
        t-pay = t-pay + curr-pay. 
        t-bal = t-bal + l-kredit.netto - curr-pay. 

        FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
            AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN
                output-list.recv-date = queasy.date1.
        END.
      END. 
      create output-list. 
      DO i = 1 TO 53: 
        output-list.str = output-list.str + " ". 
      END. 
      output-list.str = output-list.str + "T O T A L     ". 
      IF price-decimal = 0 THEN output-list.str = output-list.str 
        + STRING(t-ap, "->,>>>,>>>,>>>,>>9") 
        + STRING(t-pay, "->,>>>,>>>,>>>,>>9") + "        " 
        + STRING(t-bal, "->,>>>,>>>,>>>,>>9") + "        ". 
      ELSE output-list.str = output-list.str 
        + STRING(t-ap, "->>,>>>,>>>,>>9.99") 
        + STRING(t-pay, "->>,>>>,>>>,>>9.99") + "        " 
        + STRING(t-bal, "->>,>>>,>>>,>>9.99") + "        ". 
    END. 
  END.
END.


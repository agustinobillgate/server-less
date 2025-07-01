DEF TEMP-TABLE s-list 
  FIELD fibu            AS CHAR 
  FIELD cost-center     AS CHAR FORMAT "x(24)" 
  FIELD bezeich         AS CHAR 
  FIELD cost            AS DECIMAL.

DEF TEMP-TABLE str-list 
  FIELD fibu            AS CHAR 
  FIELD other-fibu      AS LOGICAL 
  FIELD op-recid        AS INTEGER 
  FIELD lscheinnr       AS CHAR 
  FIELD s               AS CHAR FORMAT "x(160)"
  FIELD mark            AS CHAR.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER trans-code     AS CHAR.
DEF INPUT  PARAMETER from-grp       AS INT.
DEF INPUT  PARAMETER mi-alloc-chk   AS LOGICAL.
DEF INPUT  PARAMETER mi-article-chk AS LOGICAL.
DEF INPUT  PARAMETER mi-docu-chk    AS LOGICAL.
DEF INPUT  PARAMETER mi-date-chk    AS LOGICAL.

DEF INPUT  PARAMETER from-lager     AS INT.
DEF INPUT  PARAMETER to-lager       AS INT.
DEF INPUT  PARAMETER from-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF INPUT  PARAMETER from-art       AS INT.
DEF INPUT  PARAMETER to-art         AS INT.
DEF INPUT  PARAMETER deptNo         AS INT.
DEF INPUT  PARAMETER long-digit     AS LOGICAL.
DEF INPUT  PARAMETER cost-acct      AS CHAR.
DEF INPUT  PARAMETER mattype        AS INT.

DEF OUTPUT PARAMETER it-exist       AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR str-list.

DEFINE VARIABLE tot-anz    AS DECIMAL. 
DEFINE VARIABLE tot-amount AS DECIMAL INITIAL 0. 
DEFINE VARIABLE i          AS INTEGER.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "stock-houtlist".
IF from-grp = 0 THEN 
DO: 
    IF mi-alloc-chk = YES THEN RUN create-list. 
    ELSE IF mi-article-chk = YES 
      THEN RUN create-listA. 
    ELSE IF mi-docu-chk = YES 
      THEN RUN create-listB. 
    ELSE IF mi-date-chk = YES 
      THEN RUN create-listC. 
END. 
ELSE 
DO: 
    IF mi-alloc-chk = YES THEN RUN create-list1. 
    ELSE IF mi-article-chk = YES 
      THEN RUN create-list1A. 
    ELSE IF mi-docu-chk = YES 
      THEN RUN create-list1B. 
    ELSE IF mi-date-chk = YES 
      THEN RUN create-list1C. 
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
 
it-exist = NO. 
FOR EACH str-list: 
  DELETE str-list. 
END. 
FOR EACH s-list: 
  DELETE s-list. 
END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    curr-artnr = 0. 

    IF CONNECTED ("vhparch") THEN 
    DO:
        RUN stockHoutli-arch.p('listA', l-lager.lager-nr, from-date, to-date, 
            from-art, to-art, deptNo, long-digit, do-it, l-lager.bezeich,
            from-grp, "", "", OUTPUT it-exist, OUTPUT t-anz, OUTPUT t-val, 
            OUTPUT tot-anz, OUTPUT tot-amount).
    END.
    ELSE
    DO:
        FOR EACH vhp.l-ophis WHERE vhp.l-ophis.lager-nr = l-lager.lager-nr 
          AND vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
          AND vhp.l-ophis.artnr GE from-art AND vhp.l-ophis.artnr LE to-art 
          AND vhp.l-ophis.anzahl NE 0 AND vhp.l-ophis.op-art = 3 NO-LOCK, 
          FIRST vhp.l-ophhis WHERE vhp.l-ophhis.op-typ = "STT" 
          AND vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
          AND vhp.l-ophhis.fibukonto NE "" NO-LOCK, 
          FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophis.fibukonto NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK 
          /*BY l-artikel.bezeich*/ BY vhp.l-ophis.datum 
          BY vhp.l-ophis.lscheinnr BY l-ophis.artnr: 
     
          it-exist = YES. 
          other-fibu = NO. 
          IF vhp.l-ophis.fibukonto NE "" THEN 
          DO: 
            IF deptno NE 0 THEN /*MT 31-08-12 */
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto AND gl-acct1.deptnr = deptno
              NO-LOCK NO-ERROR. 
            ELSE
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
     
          IF lschein = "" THEN lschein = vhp.l-ophis.lscheinnr. 
     
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
              parameters.vstring = gl-acct.fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.
    
          IF curr-artnr = 0 THEN curr-artnr = vhp.l-ophis.artnr. 
          IF (curr-artnr NE vhp.l-ophis.artnr) AND t-anz NE 0 THEN 
          DO: 
            CREATE str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 46: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 12: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            ELSE 
            str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
            t-anz = 0. 
            t-val = 0. 
            CREATE str-list. 
            lschein = vhp.l-ophis.lscheinnr. 
            curr-artnr = vhp.l-ophis.artnr. 
          END. 
     
          IF do-it THEN 
          DO: 
            CREATE str-list. 
            CREATE str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
            CREATE str-list. 
            do-it = NO. 
          END. 
     
          IF create-it THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
             CREATE s-list. 
             s-list.fibu = fibukonto. 
             s-list.bezeich = cost-bezeich. 
             IF cc-code NE 0 THEN s-list.bezeich = 
               STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 
            s-list.cost = s-list.cost + vhp.l-ophis.warenwert. 
            t-anz = t-anz + vhp.l-ophis.anzahl. 
            t-val = t-val + vhp.l-ophis.warenwert. 
            tot-anz = tot-anz + vhp.l-ophis.anzahl. 
            tot-amount = tot-amount + vhp.l-ophis.warenwert. 
            CREATE str-list. 
            str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 

            IF NOT long-digit THEN 
            DO:
              IF vhp.l-ophis.einzelpreis GT 9999999 THEN
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(45)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
              ELSE
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(45)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, ">,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
            END.
            ELSE str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(45)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->>>>,>>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
          END. 
        END. 
    END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 46: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 12: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val,      "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 46: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  
  ASSIGN
    str-list.s = STRING("","x(8)") 
      + STRING(translateExtended ("SUMMARY OF EXPENSES",lvCAREA,""), "x(30)")
    str-list.mark = "Summary".

  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(45)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(45)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>>>,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 72: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-listB: /*Ragung*/
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
 
it-exist = NO. 
FOR EACH str-list: 
  DELETE str-list. 
END. 
FOR EACH s-list: 
  DELETE s-list. 
END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    curr-artnr = 0. 

    IF CONNECTED ("vhparch") THEN 
    DO:
        RUN stockHoutli-arch.p('listB', l-lager.lager-nr, from-date, to-date, 
            from-art, to-art, deptNo, long-digit, do-it, l-lager.bezeich,
            from-grp, "", "", OUTPUT it-exist, OUTPUT t-anz, OUTPUT t-val, 
            OUTPUT tot-anz, OUTPUT tot-amount).
    END.
    ELSE
    DO:
        FOR EACH vhp.l-ophis WHERE vhp.l-ophis.lager-nr = l-lager.lager-nr 
          AND vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
          AND vhp.l-ophis.artnr GE from-art AND vhp.l-ophis.artnr LE to-art 
          AND vhp.l-ophis.anzahl NE 0 AND vhp.l-ophis.op-art = 3 NO-LOCK, 
          FIRST vhp.l-ophhis WHERE vhp.l-ophhis.op-typ = "STT" 
          AND vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
          AND vhp.l-ophhis.fibukonto NE "" NO-LOCK, 
          FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophis.fibukonto 
            /*MT 19-04-12 AND gl-acct.deptnr = deptno*/ NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK 
          BY vhp.l-ophis.lscheinnr /*BY l-artikel.bezeich*/  BY l-ophis.artnr: 
     
          it-exist = YES. 
          other-fibu = NO. 
          IF vhp.l-ophis.fibukonto NE "" THEN 
          DO: 
            IF deptno NE 0 THEN /*MT 31-08-12 */
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto AND gl-acct1.deptnr = deptno
              NO-LOCK NO-ERROR. 
            ELSE
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto
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
              parameters.vstring = gl-acct.fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.
    
          IF lschein = "" THEN lschein = vhp.l-ophis.lscheinnr. 
          IF (lschein NE vhp.l-ophis.lscheinnr) AND t-anz NE 0 THEN 
          DO: 
            CREATE str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 46: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 12: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            ELSE 
            str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
            t-anz = 0. 
            t-val = 0. 
            CREATE str-list. 
            lschein = vhp.l-ophis.lscheinnr. 
            curr-artnr = vhp.l-ophis.artnr. 
          END. 
     
          IF do-it THEN 
          DO: 
            CREATE str-list. 
            CREATE str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
            CREATE str-list. 
            do-it = NO. 
          END. 
     
          IF create-it THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
             CREATE s-list. 
             s-list.fibu = fibukonto. 
             s-list.bezeich = cost-bezeich. 
             IF cc-code NE 0 THEN s-list.bezeich = 
               STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 
            s-list.cost = s-list.cost + vhp.l-ophis.warenwert. 
            t-anz = t-anz + vhp.l-ophis.anzahl. 
            t-val = t-val + vhp.l-ophis.warenwert. 
            tot-anz = tot-anz + vhp.l-ophis.anzahl. 
            tot-amount = tot-amount + vhp.l-ophis.warenwert. 
            CREATE str-list. 
            str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            IF NOT long-digit THEN 
            DO:
              IF vhp.l-ophis.einzelpreis GT 9999999 THEN
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
              ELSE
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, ">,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
            END.
            ELSE str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->>>>,>>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
          END. 
        END. 
    END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO:                                                                                                     
    CREATE str-list.                                                                                      
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 46: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 12: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val,      "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 46: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  
  ASSIGN
    str-list.s = STRING("","x(8)") 
      + STRING(translateExtended ("SUMMARY OF EXPENSES",lvCAREA,""), "x(30)")
    str-list.mark = "Summary".

  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>>>,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 72: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 

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
 
it-exist = NO. 
FOR EACH str-list: 
  DELETE str-list. 
END. 
FOR EACH s-list: 
  DELETE s-list. 
END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
    do-it = YES. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    curr-artnr = 0. 

    IF CONNECTED ("vhparch") THEN 
    DO:
        RUN stockHoutli-arch.p('listC', l-lager.lager-nr, from-date, to-date, 
            from-art, to-art, deptNo, long-digit, do-it, l-lager.bezeich,
            from-grp, "", "", OUTPUT it-exist, OUTPUT t-anz, OUTPUT t-val, 
            OUTPUT tot-anz, OUTPUT tot-amount).
    END.
    ELSE
    DO:
        FOR EACH vhp.l-ophis WHERE vhp.l-ophis.lager-nr = l-lager.lager-nr 
          AND vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
          AND vhp.l-ophis.artnr GE from-art AND vhp.l-ophis.artnr LE to-art 
          AND vhp.l-ophis.anzahl NE 0 AND vhp.l-ophis.op-art = 3 NO-LOCK, 
          FIRST vhp.l-ophhis WHERE vhp.l-ophhis.op-typ = "STT" 
          AND vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
          AND vhp.l-ophhis.fibukonto NE "" NO-LOCK, 
          FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophis.fibukonto NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK 
          BY vhp.l-ophis.datum /*BY l-artikel.bezeich*/ BY l-ophis.artnr: 
     
          it-exist = YES. 
          other-fibu = NO. 
          IF vhp.l-ophis.fibukonto NE "" THEN 
          DO: 
            IF deptno NE 0 THEN /*MT 31-08-12 */
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto AND gl-acct1.deptnr = deptno
              NO-LOCK NO-ERROR. 
            ELSE
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto
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
              parameters.vstring = gl-acct.fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.
    
          IF datum = ? THEN datum = vhp.l-ophis.datum. 
          IF (datum NE vhp.l-ophis.datum) AND t-anz NE 0 THEN 
          DO: 
            CREATE str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 46: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 12: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            ELSE 
            str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
            t-anz = 0. 
            t-val = 0. 
            CREATE str-list. 
            lschein = vhp.l-ophis.lscheinnr. 
            datum = vhp.l-ophis.datum. 
            curr-artnr = vhp.l-ophis.artnr. 
          END. 
     
          IF do-it THEN 
          DO: 
            CREATE str-list. 
            CREATE str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
            CREATE str-list. 
            do-it = NO. 
          END. 
     
          IF create-it THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
             CREATE s-list. 
             s-list.fibu = fibukonto. 
             s-list.bezeich = cost-bezeich. 
             IF cc-code NE 0 THEN s-list.bezeich = 
               STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 
            s-list.cost = s-list.cost + vhp.l-ophis.warenwert. 
            t-anz = t-anz + vhp.l-ophis.anzahl. 
            t-val = t-val + vhp.l-ophis.warenwert. 
            tot-anz = tot-anz + vhp.l-ophis.anzahl. 
            tot-amount = tot-amount + vhp.l-ophis.warenwert. 
            CREATE str-list. 
            str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            IF NOT long-digit THEN 
            DO:
              IF vhp.l-ophis.einzelpreis GT 9999999 THEN
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
              ELSE
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, ">,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
            END.
            ELSE str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->>>>,>>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
          END. 
        END. 
    END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 46: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 12: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val,      "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 46: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  
  ASSIGN
    str-list.s = STRING("","x(8)") 
      + STRING(translateExtended ("SUMMARY OF EXPENSES",lvCAREA,""), "x(30)")
    str-list.mark = "Summary".

  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>>>,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 72: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list: 
DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE t-val AS DECIMAL. 
DEFINE VARIABLE lschein AS CHAR INITIAL "". 
DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(24)". 
DEFINE VARIABLE fibukonto AS CHAR INITIAL "". 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
DEFINE VARIABLE other-fibu AS LOGICAL. 
DEFINE buffer gl-acct1 FOR gl-acct. 
DEFINE VARIABLE create-it AS LOGICAL. 
DEFINE VARIABLE curr-fibu AS CHAR INITIAL "". 

it-exist = NO. 
FOR EACH str-list: 
  DELETE str-list. 
END. 
FOR EACH s-list: 
  DELETE s-list. 
END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
/*  calculate the outgoing stocks within the given periods */ 

    IF CONNECTED ("vhparch") THEN 
    DO:
        RUN stockHoutli-arch.p('list', l-lager.lager-nr, from-date, to-date, 
            from-art, to-art, deptNo, long-digit, do-it, l-lager.bezeich,
            from-grp, "", "", OUTPUT it-exist, OUTPUT t-anz, OUTPUT t-val, 
            OUTPUT tot-anz, OUTPUT tot-amount).
    END.
    ELSE
    DO:
        FOR EACH vhp.l-ophis WHERE vhp.l-ophis.lager-nr = l-lager.lager-nr 
          AND vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
          AND vhp.l-ophis.artnr GE from-art AND vhp.l-ophis.artnr LE to-art 
          AND vhp.l-ophis.anzahl NE 0 AND vhp.l-ophis.op-art = 3 NO-LOCK, 
          FIRST vhp.l-ophhis WHERE vhp.l-ophhis.op-typ = "STT" 
          AND vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
          AND vhp.l-ophhis.fibukonto NE "" NO-LOCK, 
          FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophis.fibukonto NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK 
          BY vhp.l-ophis.fibukonto /*BY l-artikel.bezeich*/ 
          BY vhp.l-ophis.datum  BY l-ophis.artnr: 
          /* 
          BY SUBSTR(vhp.l-ophis.lscheinnr,4,12) BY vhp.l-ophis.zeit: 
          */ 
          it-exist = YES. 
          other-fibu = NO. 
          IF vhp.l-ophis.fibukonto NE "" THEN 
          DO: 
            IF deptno NE 0 THEN /*MT 31-08-12 */
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto AND gl-acct1.deptnr = deptno
              NO-LOCK NO-ERROR. 
            ELSE
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES.
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
     
          IF lschein = "" THEN lschein = vhp.l-ophis.lscheinnr. 
     
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
              parameters.vstring = /*gl-acct.fibukonto*/ fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.
    
          /* Naufal Afthar - F82EA5*/
          IF create-it AND curr-fibu = "" THEN curr-fibu = fibukonto. 
          IF create-it AND curr-fibu NE fibukonto AND t-anz NE 0 THEN 
          /* end Naufal Afthar*/
    /*    IF (lschein NE vhp.l-ophis.lscheinnr) AND t-anz NE 0 THEN */ 
          DO: 
            CREATE str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 46: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 12: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
            str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9.99"). 
            ELSE 
            str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
            t-anz = 0. 
            t-val = 0. 
            CREATE str-list. 
            lschein = vhp.l-ophis.lscheinnr. 
            curr-fibu = fibukonto. 
          END. 
     
          IF do-it THEN 
          DO: 
            CREATE str-list. 
            CREATE str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
            CREATE str-list. 
            do-it = NO. 
          END. 
     
          IF create-it THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
             CREATE s-list. 
             s-list.fibu = fibukonto. 
             s-list.bezeich = cost-bezeich. 
             IF cc-code NE 0 THEN s-list.bezeich = 
               STRING(cc-code,"9999 ") + s-list.bezeich.
            END. 
            s-list.cost = s-list.cost + vhp.l-ophis.warenwert. 
            t-anz = t-anz + vhp.l-ophis.anzahl. 
            t-val = t-val + vhp.l-ophis.warenwert. 
            tot-anz = tot-anz + vhp.l-ophis.anzahl. 
            tot-amount = tot-amount + vhp.l-ophis.warenwert. 
            CREATE str-list. 
            str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
            str-list.fibu = fibukonto. 
            str-list.other-fibu = other-fibu. 
            str-list.op-recid = RECID(l-op). 
            IF NOT long-digit THEN 
            DO:
              IF vhp.l-ophis.einzelpreis GT 9999999 THEN
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
              ELSE
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, ">,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
            END.
            ELSE str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->>>>,>>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
          END. 
        END. 
    END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 46: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 12: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val,      "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 46: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>>>,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 72: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
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
 
  it-exist = NO. 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
  FOR EACH s-list: 
    DELETE s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
/*  calculate the outgoing stocks within the given periods */ 
    do-it = YES. 

    IF CONNECTED ("vhparch") THEN 
    DO:
        RUN stockHoutli-arch.p('list1', l-lager.lager-nr, from-date, to-date, 
            from-art, to-art, deptNo, long-digit, do-it, l-lager.bezeich,
            from-grp, grp1, grp2, OUTPUT it-exist, OUTPUT t-anz, OUTPUT t-val, 
            OUTPUT tot-anz, OUTPUT tot-amount).
    END.
    ELSE
    DO:
        FOR EACH vhp.l-ophis WHERE vhp.l-ophis.lager-nr = l-lager.lager-nr 
          AND vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
          AND vhp.l-ophis.artnr GE from-art AND vhp.l-ophis.artnr LE to-art 
          AND vhp.l-ophis.anzahl NE 0 AND vhp.l-ophis.op-art = 3 NO-LOCK, 
          FIRST vhp.l-ophhis WHERE vhp.l-ophhis.op-typ = "STT" 
          AND vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
          AND vhp.l-ophhis.fibukonto NE "" NO-LOCK, 
          FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophis.fibukonto NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum EQ from-grp NO-LOCK, 
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
          AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
          NO-LOCK BY vhp.l-ophis.fibukonto BY vhp.l-ophhis.fibukonto 
          /*BY l-artikel.bezeich*/ BY vhp.l-ophis.datum BY l-ophis.artnr: 
          /* 
          BY vhp.l-ophis.datum BY SUBSTR(vhp.l-ophis.lscheinnr,4,12) BY vhp.l-ophis.zeit: 
          */ 
          it-exist = YES. 
          other-fibu = NO. 
          IF vhp.l-ophis.fibukonto NE "" THEN 
          DO: 
            IF deptno NE 0 THEN /*MT 31-08-12 */
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto AND gl-acct1.deptnr = deptno
              NO-LOCK NO-ERROR. 
            ELSE
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
     
          IF lschein = "" THEN lschein = vhp.l-ophis.lscheinnr. 
     
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
              parameters.vstring = gl-acct.fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.
    
          /* Naufal Afthar - F82EA5*/
          IF create-it AND curr-fibu = "" THEN curr-fibu = fibukonto. 
          IF create-it AND curr-fibu NE fibukonto AND t-anz NE 0 THEN 
          /* end Naufal Afthar*/
    /*    IF (lschein NE vhp.l-ophis.lscheinnr) AND t-anz NE 0 THEN */ 
          DO: 
            CREATE str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 46: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 12: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
            str-list.s = str-list.s + STRING(t-val,      "->,>>>,>>>,>>9.99"). 
            ELSE str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
            t-anz = 0. 
            t-val = 0. 
            CREATE str-list. 
            lschein = vhp.l-ophis.lscheinnr. 
            curr-fibu = fibukonto. 
          END. 
     
          IF do-it THEN 
          DO: 
            CREATE str-list. 
            CREATE str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
            CREATE str-list. 
            do-it = NO. 
          END. 
     
          IF create-it THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich. 
              IF cc-code NE 0 THEN s-list.bezeich = 
                STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 
            s-list.cost = s-list.cost + vhp.l-ophis.warenwert. 
            t-anz = t-anz + vhp.l-ophis.anzahl. 
            t-val = t-val + vhp.l-ophis.warenwert. 
            tot-anz = tot-anz + vhp.l-ophis.anzahl. 
            tot-amount = tot-amount + vhp.l-ophis.warenwert. 
            CREATE str-list. 
            str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
            str-list.other-fibu = other-fibu. 
            str-list.fibu = fibukonto. 
            str-list.op-recid = RECID(l-op). 
            IF NOT long-digit THEN 
            DO:
              IF vhp.l-ophis.einzelpreis GT 9999999 THEN
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
              ELSE
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, ">,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
            END.
            ELSE 
            str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->>>>,>>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
          END. 
        END. 
    END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 46: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 12: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val,      "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 46: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  
  ASSIGN
    str-list.s = STRING("","x(8)") 
      + STRING(translateExtended ("SUMMARY OF EXPENSES",lvCAREA,""), "x(30)")
    str-list.mark = "Summary".

  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>>>,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 72: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
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

  it-exist = NO. 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
  FOR EACH s-list: 
    DELETE s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
/*  calculate the outgoing stocks within the given periods */ 
    do-it = YES. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    curr-artnr = 0. 

    IF CONNECTED ("vhparch") THEN 
    DO:
        RUN stockHoutli-arch.p('list1A', l-lager.lager-nr, from-date, to-date, 
            from-art, to-art, deptNo, long-digit, do-it, l-lager.bezeich,
            from-grp, grp1, grp2, OUTPUT it-exist, OUTPUT t-anz, OUTPUT t-val, 
            OUTPUT tot-anz, OUTPUT tot-amount).
    END.
    ELSE
    DO:
        FOR EACH vhp.l-ophis WHERE vhp.l-ophis.lager-nr = l-lager.lager-nr 
          AND vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
          AND vhp.l-ophis.artnr GE from-art AND vhp.l-ophis.artnr LE to-art 
          AND vhp.l-ophis.anzahl NE 0 AND vhp.l-ophis.op-art = 3 NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum EQ from-grp NO-LOCK, 
          FIRST vhp.l-ophhis WHERE vhp.l-ophhis.op-typ = "STT" 
          AND vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
          AND vhp.l-ophhis.fibukonto NE "" NO-LOCK, 
          FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophis.fibukonto NO-LOCK, 
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
          AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
          NO-LOCK /*BY l-artikel.bezeich*/ 
          BY vhp.l-ophis.datum BY vhp.l-ophis.lscheinnr BY l-ophis.artnr: 

          it-exist = YES. 
          other-fibu = NO. 
          IF vhp.l-ophis.fibukonto NE "" THEN 
          DO: 
            IF deptno NE 0 THEN /*MT 31-08-12 */
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto AND gl-acct1.deptnr = deptno
              NO-LOCK NO-ERROR. 
            ELSE
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
          END. 
          IF other-fibu THEN 
            RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
          ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
     
          IF lschein = "" THEN lschein = vhp.l-ophis.lscheinnr. 
     
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
              parameters.vstring = gl-acct.fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.
    
          IF curr-artnr = 0 THEN curr-artnr = vhp.l-ophis.artnr. 
          IF curr-artnr NE vhp.l-ophis.artnr AND t-anz NE 0 THEN 
          DO: 
            CREATE str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 46: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 12: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
            str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
            ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
            t-anz = 0. 
            t-val = 0. 
            CREATE str-list. 
            lschein = vhp.l-ophis.lscheinnr. 
            curr-artnr = vhp.l-ophis.artnr. 
          END. 
     
          IF do-it THEN 
          DO: 
            CREATE str-list. 
            CREATE str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
            CREATE str-list. 
            do-it = NO. 
          END. 
     
          IF create-it THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich. 
              IF cc-code NE 0 THEN s-list.bezeich = 
                STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 
            s-list.cost = s-list.cost + vhp.l-ophis.warenwert. 
            t-anz = t-anz + vhp.l-ophis.anzahl. 
            t-val = t-val + vhp.l-ophis.warenwert. 
            tot-anz = tot-anz + vhp.l-ophis.anzahl. 
            tot-amount = tot-amount + vhp.l-ophis.warenwert. 
            CREATE str-list. 
            str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
            str-list.other-fibu = other-fibu. 
            str-list.fibu = fibukonto. 
            str-list.op-recid = RECID(l-op). 
            IF NOT long-digit THEN 
            DO:
              IF vhp.l-ophis.einzelpreis GT 9999999 THEN
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
              ELSE
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, ">,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
            END.
            ELSE 
            str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->>>>,>>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
          END. 
        END. 
    END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 46: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 12: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val,      "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 46: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  
  ASSIGN
    str-list.s = STRING("","x(8)") 
      + STRING(translateExtended ("SUMMARY OF EXPENSES",lvCAREA,""), "x(30)")
    str-list.mark = "Summary".

  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>>>,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 72: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
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

  it-exist = NO. 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
  FOR EACH s-list: 
    DELETE s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
/*  calculate the outgoing stocks within the given periods */ 
    do-it = YES. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    curr-artnr = 0. 

    IF CONNECTED ("vhparch") THEN 
    DO:
        RUN stockHoutli-arch.p('list1B', l-lager.lager-nr, from-date, to-date, 
            from-art, to-art, deptNo, long-digit, do-it, l-lager.bezeich,
            from-grp, grp1, grp2, OUTPUT it-exist, OUTPUT t-anz, OUTPUT t-val, 
            OUTPUT tot-anz, OUTPUT tot-amount).
    END.
    ELSE
    DO:
        FOR EACH vhp.l-ophis WHERE vhp.l-ophis.lager-nr = l-lager.lager-nr 
          AND vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
          AND vhp.l-ophis.artnr GE from-art AND vhp.l-ophis.artnr LE to-art 
          AND vhp.l-ophis.anzahl NE 0 AND vhp.l-ophis.op-art = 3 NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum EQ from-grp NO-LOCK, 
          FIRST vhp.l-ophhis WHERE vhp.l-ophhis.op-typ = "STT" 
          AND vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
          AND vhp.l-ophhis.fibukonto NE "" NO-LOCK, 
          FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophis.fibukonto NO-LOCK, 
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
          AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
          BY vhp.l-ophis.lscheinnr /*BY l-artikel.bezeich*/ BY l-ophis.artnr: 

          it-exist = YES. 
          other-fibu = NO. 
          IF vhp.l-ophis.fibukonto NE "" THEN 
          DO: 
            IF deptno NE 0 THEN /*MT 31-08-12 */
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto AND gl-acct1.deptnr = deptno
              NO-LOCK NO-ERROR. 
            ELSE
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto
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
              parameters.vstring = gl-acct.fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.
    
          IF lschein = "" THEN lschein = vhp.l-ophis.lscheinnr. 
          IF lschein NE vhp.l-ophis.lscheinnr AND t-anz NE 0 THEN 
          DO: 
            CREATE str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 46: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 12: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
            str-list.s = str-list.s + STRING(t-val,      "->,>>>,>>>,>>9.99"). 
            ELSE str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
            t-anz = 0. 
            t-val = 0. 
            CREATE str-list. 
            lschein = vhp.l-ophis.lscheinnr. 
            curr-artnr = vhp.l-ophis.artnr. 
          END. 
     
          IF do-it THEN 
          DO: 
            CREATE str-list. 
            CREATE str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
            CREATE str-list. 
            do-it = NO. 
          END. 
     
          IF create-it THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich. 
              IF cc-code NE 0 THEN s-list.bezeich = 
                STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 
            s-list.cost = s-list.cost + vhp.l-ophis.warenwert. 
            t-anz = t-anz + vhp.l-ophis.anzahl. 
            t-val = t-val + vhp.l-ophis.warenwert. 
            tot-anz = tot-anz + vhp.l-ophis.anzahl. 
            tot-amount = tot-amount + vhp.l-ophis.warenwert. 
            CREATE str-list. 
            str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
            str-list.other-fibu = other-fibu. 
            str-list.fibu = fibukonto. 
            str-list.op-recid = RECID(l-op). 
            IF NOT long-digit THEN 
            DO:
              IF vhp.l-ophis.einzelpreis GT 9999999 THEN
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
              ELSE
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, ">,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
            END.
            ELSE 
            str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->>>>,>>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
          END. 
        END. 
    END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 46: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 12: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val,      "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 46: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  
  ASSIGN
    str-list.s = STRING("","x(8)") 
      + STRING(translateExtended ("SUMMARY OF EXPENSES",lvCAREA,""), "x(30)")
    str-list.mark = "Summary".

  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>>>,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 72: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
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
 
  it-exist = NO. 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
  FOR EACH s-list: 
    DELETE s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
/*  calculate the outgoing stocks within the given periods */ 
    do-it = YES. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    curr-artnr = 0. 

    IF CONNECTED ("vhparch") THEN 
    DO:
        RUN stockHoutli-arch.p('list1C', l-lager.lager-nr, from-date, to-date, 
            from-art, to-art, deptNo, long-digit, do-it, l-lager.bezeich,
            from-grp, grp1, grp2, OUTPUT it-exist, OUTPUT t-anz, OUTPUT t-val, 
            OUTPUT tot-anz, OUTPUT tot-amount).
    END.
    ELSE
    DO:
        FOR EACH vhp.l-ophis WHERE vhp.l-ophis.lager-nr = l-lager.lager-nr 
          AND vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
          AND vhp.l-ophis.artnr GE from-art AND vhp.l-ophis.artnr LE to-art 
          AND vhp.l-ophis.anzahl NE 0 AND vhp.l-ophis.op-art = 3 NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum EQ from-grp NO-LOCK, 
          FIRST vhp.l-ophhis WHERE vhp.l-ophhis.op-typ = "STT" 
          AND vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
          AND vhp.l-ophhis.fibukonto NE "" NO-LOCK, 
          FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophis.fibukonto NO-LOCK, 
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
          AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
          BY vhp.l-ophis.datum /*BY l-artikel.bezeich*/ BY l-ophis.artnr: 

          it-exist = YES. 
          other-fibu = NO. 
          IF vhp.l-ophis.fibukonto NE "" THEN 
          DO: 
            IF deptno NE 0 THEN /*MT 31-08-12 */
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto AND gl-acct1.deptnr = deptno
              NO-LOCK NO-ERROR. 
            ELSE
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto
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
              parameters.vstring = gl-acct.fibukonto NO-ERROR.
            create-it = AVAILABLE parameters.
          END.
    
          IF datum = ? THEN datum = vhp.l-ophis.datum. 
          IF datum NE vhp.l-ophis.datum AND t-anz NE 0 THEN 
          DO: 
            CREATE str-list. 
            DO i = 1 TO 45: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + "Subtotal ". 
            DO i = 1 TO 46: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
            DO i = 1 TO 12: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
            str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
            ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
            t-anz = 0. 
            t-val = 0. 
            CREATE str-list. 
            lschein = vhp.l-ophis.lscheinnr. 
            datum = vhp.l-ophis.datum. 
            curr-artnr = vhp.l-ophis.artnr. 
          END. 
     
          IF do-it THEN 
          DO: 
            CREATE str-list. 
            CREATE str-list. 
            str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
            CREATE str-list. 
            do-it = NO. 
          END. 
     
          IF create-it THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.fibu = fibukonto. 
              s-list.bezeich = cost-bezeich. 
              IF cc-code NE 0 THEN s-list.bezeich = 
                STRING(cc-code,"9999 ") + s-list.bezeich. 
            END. 
            s-list.cost = s-list.cost + vhp.l-ophis.warenwert. 
            t-anz = t-anz + vhp.l-ophis.anzahl. 
            t-val = t-val + vhp.l-ophis.warenwert. 
            tot-anz = tot-anz + vhp.l-ophis.anzahl. 
            tot-amount = tot-amount + vhp.l-ophis.warenwert. 
            CREATE str-list. 
            str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
            str-list.other-fibu = other-fibu. 
            str-list.fibu = fibukonto. 
            str-list.op-recid = RECID(l-op). 
            IF NOT long-digit THEN 
            DO:
              IF vhp.l-ophis.einzelpreis GT 9999999 THEN
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
              ELSE
              str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, ">,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.warenwert, "->,>>>,>>>,>>9.99") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
            END.
            ELSE 
            str-list.s = STRING(vhp.l-ophis.datum) 
                     + STRING(s-list.bezeich, "x(30)") 
                     + STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(55)") 
                     + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.999") 
                     + STRING(vhp.l-ophis.einzelpreis, " >>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.warenwert, "->>>>,>>>,>>>,>>9") 
                     + STRING(vhp.l-ophis.lscheinnr, "x(12)"). 
          END. 
        END. 
    END.
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    CREATE str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 46: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 12: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val,      "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->>>>,>>>,>>>,>>9"). 
    CREATE str-list. 
  END. 
 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 46: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
 
  CREATE str-list. 
  CREATE str-list. 
  CREATE str-list. 
  
  ASSIGN
    str-list.s = STRING("","x(8)") 
      + STRING(translateExtended ("SUMMARY OF EXPENSES",lvCAREA,""), "x(30)")
    str-list.mark = "Summary".

  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    CREATE str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(55)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>>>,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  CREATE str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 72: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount,      "->,>>>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->>>>,>>>,>>>,>>9"). 
END. 

PROCEDURE get-costcenter-code: 
DEFINE INPUT PARAMETER fibukonto AS CHAR. 
DEFINE OUTPUT PARAMETER cc-code AS INTEGER INITIAL 0. 
  FIND FIRST parameters WHERE progname = "CostCenter" 
    AND section = "Alloc" AND varname GT "" 
    AND parameters.vstring = fibukonto NO-LOCK NO-ERROR. 
  IF AVAILABLE parameters THEN cc-code = INTEGER(parameters.varname). 
END. 

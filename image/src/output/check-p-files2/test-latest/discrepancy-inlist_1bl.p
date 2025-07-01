DEFINE TEMP-TABLE str-list 
    FIELD s AS CHAR FORMAT "x(135)". 

DEFINE TEMP-TABLE output-list
    FIELD datum     AS CHARACTER /* DATE FORMAT "99/99/9999" */
    FIELD lager     AS CHARACTER 
    FIELD docunr    AS CHARACTER
    FIELD art       AS CHARACTER
    FIELD bezeich   AS CHARACTER
    FIELD in-qty    AS CHARACTER /* DECIMAL FORMAT "->>>,>>9.99" */     
    FIELD amount    AS CHARACTER /* DECIMAL FORMAT ">,>>>,>>>,>>9.99" */
    FIELD epreis1   AS CHARACTER /* DECIMAL FORMAT ">,>>>,>>>,>>9.99" */
    FIELD epreis2   AS CHARACTER /* DECIMAL FORMAT ">,>>>,>>>,>>9.99" */
    FIELD lief      AS CHARACTER
    FIELD dlvnote   AS CHARACTER
    .  

DEFINE TEMP-TABLE discrepancy-inlist
    FIELD datum     AS DATE FORMAT "99/99/9999"
    FIELD lager     AS CHARACTER
    FIELD docunr    AS CHARACTER
    FIELD art       AS CHARACTER
    FIELD bezeich   AS CHARACTER
    FIELD in-qty    AS DECIMAL FORMAT "->>>,>>9.99"     
    FIELD amount    AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"
    FIELD epreis1   AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"
    FIELD epreis2   AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"
    FIELD lief      AS CHARACTER
    FIELD dlvnote   AS CHARACTER
    .  

DEF INPUT  PARAMETER sorttype   AS INT      NO-UNDO.
DEF INPUT  PARAMETER from-lager AS INT      NO-UNDO.
DEF INPUT  PARAMETER to-lager   AS INT      NO-UNDO.
DEF INPUT  PARAMETER from-date  AS DATE     NO-UNDO.
DEF INPUT  PARAMETER to-date    AS DATE     NO-UNDO.
DEF INPUT  PARAMETER from-art   AS INT      NO-UNDO.
DEF INPUT  PARAMETER to-art     AS INT      NO-UNDO.
DEF INPUT  PARAMETER mi-rec-chk AS LOGICAL  NO-UNDO.
DEF INPUT  PARAMETER mi-ord-chk AS LOGICAL  NO-UNDO.
DEF INPUT  PARAMETER mi-all-chk AS LOGICAL  NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR discrepancy-inlist.

/*DEF VAR sorttype   AS INT INIT 1.
DEF VAR from-lager AS INT INIT 1.
DEF VAR to-lager   AS INT INIT 18.
DEF VAR from-date  AS DATE INIT 1/1/19.
DEF VAR to-date    AS DATE INIT 12/17/19.
DEF VAR from-art   AS INT INIT 1.
DEF VAR to-art     AS INT INIT 9999999.
DEF VAR mi-rec-chk AS LOGICAL INIT YES.
DEF VAR mi-ord-chk AS LOGICAL INIT NO.
DEF VAR mi-all-chk AS LOGICAL INIT NO.*/

DEF VAR lager-bezeich AS CHARACTER.
DEFINE VARIABLE i               AS INTEGER. 
DEFINE VARIABLE tot-anz         AS DECIMAL. 
DEFINE VARIABLE tot-amount      AS DECIMAL.
DEFINE VARIABLE price-decimal   AS INTEGER.
DEFINE VARIABLE long-digit      AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.
DEFINE VARIABLE note-str   AS CHAR EXTENT 2 INITIAL ["        ", "Transfer"]. 
DEFINE VARIABLE deliver-no AS CHAR. 

RUN htpint.p (491, OUTPUT price-decimal).
IF sorttype = 1 THEN RUN create-list1. 
ELSE IF sorttype = 2 THEN RUN create-list2. 
ELSE RUN create-list3. 

/* Malik Serverless 670 comment and move to one file 
RUN discrepancy-inlistbl.p (sorttype, from-lager, to-lager, from-date, to-date, from-art, to-art, mi-rec-chk, mi-ord-chk, mi-all-chk, OUTPUT TABLE str-list).*/


FOR EACH discrepancy-inlist:
    DELETE discrepancy-inlist.
END.

/* 
FOR EACH str-list:
    CREATE discrepancy-inlist.

    FIND FIRST l-lager WHERE lager-nr EQ INTEGER(SUBSTR(str-list.s, 9,  2)) NO-LOCK NO-ERROR.
    IF AVAILABLE l-lager THEN ASSIGN lager-bezeich = l-lager.bezeich.

    ASSIGN
        discrepancy-inlist.datum    =   DATE(SUBSTR(str-list.s, 1,  8)) /* STRING(l-op.datum) */
        discrepancy-inlist.lager    =   lager-bezeich /* STRING(l-op.lager-nr, "99") */
        discrepancy-inlist.docunr   =   SUBSTR(str-list.s, 107, 12) /* STRING(l-op.docu-nr, "x(12)") */
        discrepancy-inlist.art      =   SUBSTR(str-list.s, 11,  7) /* STRING(l-artikel.artnr, "9999999") */
        discrepancy-inlist.bezeich  =   SUBSTR(str-list.s, 18, 36) /* STRING(l-artikel.bezeich, "x(36)") */
        discrepancy-inlist.in-qty   =   DECIMAL(SUBSTR(str-list.s, 54, 11)) /* STRING(l-op.anzahl, "->>>,>>9.99") */
        discrepancy-inlist.amount   =   DECIMAL(SUBSTR(str-list.s, 65, 14)) /* STRING(l-op.warenwert, "->>,>>>,>>9.99") */
        discrepancy-inlist.epreis1  =   DECIMAL(SUBSTR(str-list.s, 135, 14)) /* STRING(l-op.einzelpreis, "->,>>>,>>>,>>9") */
        discrepancy-inlist.epreis2  =   DECIMAL(SUBSTR(str-list.s, 149, 14)) /* STRING(epreis,"->,>>>,>>>,>>9") */
        discrepancy-inlist.lief     =   SUBSTR(str-list.s, 87, 20) /* note-str[l-op.op-art] (8) + STRING(l-lieferant.firma, "x(20)") */
        discrepancy-inlist.dlvnote  =   SUBSTR(str-list.s, 119, 16) /* STRING(deliver-no, "x(16)") */
        .
END.*/

FOR EACH output-list:
    CREATE discrepancy-inlist.

    FIND FIRST l-lager WHERE lager-nr EQ INTEGER(output-list.lager) NO-LOCK NO-ERROR.
    IF AVAILABLE l-lager THEN ASSIGN lager-bezeich = l-lager.bezeich.

    ASSIGN
        discrepancy-inlist.datum    =   DATE(output-list.datum) 
        discrepancy-inlist.lager    =   lager-bezeich 
        discrepancy-inlist.docunr   =   output-list.docunr 
        discrepancy-inlist.art      =   output-list.art 
        discrepancy-inlist.bezeich  =   output-list.bezeich 
        discrepancy-inlist.in-qty   =   DECIMAL(output-list.in-qty) 
        discrepancy-inlist.amount   =   DECIMAL(output-list.amount) 
        discrepancy-inlist.epreis1  =   DECIMAL(output-list.epreis1) 
        discrepancy-inlist.epreis2  =   DECIMAL(output-list.epreis2) 
        discrepancy-inlist.lief     =   output-list.lief /* note-str[l-op.op-art] (8) + STRING(l-lieferant.firma, "x(20)") */
        discrepancy-inlist.dlvnote  =   output-list.dlvnote. 
END.

/*FOR EACH discrepancy-inlist:
    DISP discrepancy-inlist.
END.*/


PROCEDURE create-list1: 
    DEFINE VARIABLE epreis AS DECIMAL. 
    DEFINE VARIABLE diff-flag AS LOGICAL. 
    /*MTstatus default "Processing...". */ 
    FOR EACH str-list: 
    delete str-list. 
    END. 
 
    tot-anz = 0. 
    tot-amount = 0. 
    FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
        AND l-lager.lager-nr LE to-lager: 
        /*  calculate the incoming stocks within the given periods */ 
        FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
            AND l-op.datum GE from-date AND l-op.datum LE to-date 
            AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
            AND l-op.anzahl NE 0 AND l-op.loeschflag LT 2 
            AND l-op.op-art = 1 AND l-op.docu-nr NE l-op.lscheinnr 
            NO-LOCK USE-INDEX artopart_ix, 
            FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
                NO-LOCK BY l-op.artnr BY l-op.datum: 
            FIND FIRST l-order WHERE l-order.docu-nr = l-op.docu-nr 
                AND l-order.artnr = l-op.artnr NO-LOCK NO-ERROR. 
            diff-flag = NO. 
            IF AVAILABLE l-order THEN 
            DO: 
                IF l-order.flag THEN epreis = l-order.einzelpreis / l-order.txtnr. 
                ELSE epreis = l-order.einzelpreis. 
                IF price-decimal = 0 THEN 
                DO: 
                IF (epreis - l-op.einzelpreis) GT 1 OR 
                    (l-op.einzelpreis - epreis) GT 1 THEN diff-flag = YES. 
                END. 
                ELSE 
                DO: 
                IF (epreis - l-op.einzelpreis) GT 0.01 OR 
                    (l-op.einzelpreis - epreis) GT 0.01 THEN diff-flag = YES. 
                END. 
            END. 
            IF diff-flag THEN 
            DO: 
                tot-anz = tot-anz + l-op.anzahl. 
                tot-amount = tot-amount + l-op.warenwert. 
                /* create str-list. */ 
                IF NOT long-digit THEN 
                DO:
                    CREATE output-list.
                    output-list.datum   = STRING(l-op.datum).
                    output-list.lager   = STRING(l-op.lager-nr, "99").
                    /* output-list.docunr   = */
                    output-list.art     = STRING(l-artikel.artnr, "9999999").
                    output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                    output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                    output-list.amount  = STRING(l-op.warenwert, "->>,>>>,>>9.99").

                    /* Malik Serverless 670 comment 
                    str-list.s = STRING(l-op.datum) /* 8 */
                            + STRING(l-op.lager-nr, "99") /* 10 */
                            + STRING(l-artikel.artnr, "9999999") /* 17 */ 
                            + STRING(l-artikel.bezeich, "x(36)") /* 53 */
                            + STRING(l-op.anzahl, "->>>,>>9.99") /* 64 */
                            + STRING(l-op.warenwert, "->>,>>>,>>9.99") /* 88 */
                            + note-str[l-op.op-art]. /* 96 */*/
                END.        
                ELSE 
                DO:
                    CREATE output-list.
                    output-list.datum   = STRING(l-op.datum).
                    output-list.lager   = STRING(l-op.lager-nr, "99").
                    /* output-list.docunr   = */
                    output-list.art     = STRING(l-artikel.artnr, "9999999").
                    output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                    output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                    output-list.amount  = STRING(l-op.warenwert, "->,>>>,>>>,>>9").
                    /* Malik Serverless 670 comment
                    str-list.s = STRING(l-op.datum) 
                            + STRING(l-op.lager-nr, "99") 
                            + STRING(l-artikel.artnr, "9999999") 
                            + STRING(l-artikel.bezeich, "x(36)") 
                            + STRING(l-op.anzahl, "->>>,>>9.99") 
                            + STRING(l-op.warenwert, "->,>>>,>>>,>>9") 
                            + note-str[l-op.op-art]. */
                END.
                IF l-op.lief-nr NE 0 THEN 
                DO: 
                    FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr 
                        NO-LOCK NO-ERROR. 
                    IF AVAILABLE l-lieferant THEN 
                    DO:
                        /* Malik Serverless 670 comment 
                        str-list.s = str-list.s + STRING(l-lieferant.firma, "x(20)"). /* 116 */*/
                        output-list.lief = STRING(l-lieferant.firma, "x(20)").
                    END.
                    ELSE
                    DO:
                        /* 
                        str-list.s = str-list.s + "                    ".*/
                        output-list.lief = STRING(" ", "x(20)").
                    END. 
                END. 
                ELSE 
                DO:
                    /* 
                    str-list.s = str-list.s + "                    ". */
                    output-list.lief = STRING(" ", "x(20)").
                END.

                IF length(l-op.lscheinnr) GT 16 THEN 
                    deliver-no = SUBSTR(l-op.lscheinnr,length(l-op.lscheinnr) - 15, 16). 
                ELSE deliver-no = l-op.lscheinnr. 

                /* Malik Serverless 670 comment 
                str-list.s = str-list.s 
                + STRING(l-op.docu-nr, "x(12)") /* 128 */
                + STRING(deliver-no, "x(16)"). /* 144 */*/
                output-list.docunr  = STRING(l-op.docu-nr, "x(12)").
                output-list.dlvnote = STRING(deliver-no, "x(16)").

                IF long-digit THEN 
                DO: 
                    output-list.epreis1 = STRING(l-op.einzelpreis, "->,>>>,>>>,>>9").
                    output-list.epreis2 = STRING(epreis,"->,>>>,>>>,>>9").
                    /* Malik Serverless 670 comment 
                    str-list.s = str-list.s 
                        + STRING(l-op.einzelpreis, "->,>>>,>>>,>>9") 
                        + STRING(epreis,"->,>>>,>>>,>>9"). */
                END. 
                ELSE 
                DO: 
                    output-list.epreis1 = STRING(l-op.einzelpreis, "->>,>>>,>>9.99").
                    output-list.epreis2 = STRING(epreis,"->>,>>>,>>9.99").
                    /* Malik Serverless 670 comment
                    str-list.s = str-list.s 
                        + STRING(l-op.einzelpreis, "->>,>>>,>>9.99") 
                        + STRING(epreis,"->>,>>>,>>9.99"). */
                END. 
            END. 
        END. 
    END. 
    /* Malik Serverless 670 comment
    create str-list. 
    DO i = 1 TO 17: 
        str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "T O T A L". 
    DO i = 1 TO 25: 
        str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                + STRING(tot-amount, "->>,>>>,>>9.99"). 
    ELSE 
    str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                + STRING(tot-amount, "->,>>>,>>>,>>9"). */
    CREATE output-list.
    output-list.datum   = STRING(" ", "x(8)").
    output-list.lager   = STRING(" ", "x(2)").
    output-list.art     = STRING(" ", "x(7)").
    output-list.bezeich = STRING("T O T A L", "x(36)").
    IF NOT long-digit THEN 
    DO:
        output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
        output-list.amount  = STRING(tot-amount, "->>,>>>,>>9.99").
    END.
    ELSE
    DO: 
        output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
        output-list.amount  = STRING(tot-amount, "->,>>>,>>>,>>9").
    END.
END. 
 
/*PROCEDURE create-list2: 
    /*MTstatus default "Processing...". */ 
    FOR EACH str-list: 
    delete str-list. 
    END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager: 
    /*  calculate the incoming stocks within the given periods */ 
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.anzahl NE 0 AND l-op.loeschflag LT 2 
      AND l-op.op-art = 1 
    /*    AND l-op.herkunftflag NE 2  /** this is  direct issue **/  */ 
      NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        NO-LOCK BY l-artikel.bezeich BY l-op.datum: 
      tot-anz = tot-anz + l-op.anzahl. 
      tot-amount = tot-amount + l-op.warenwert. 
      create str-list. 
      IF NOT long-digit THEN 
      str-list.s = STRING(l-op.datum) 
                 + STRING(l-op.lager-nr, "99") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(36)") 
                 + STRING(l-op.anzahl, "->>>,>>9.99") 
                 + STRING(l-op.warenwert, "->>,>>>,>>9.99") 
                 + note-str[l-op.op-art]. 
      ELSE 
      str-list.s = STRING(l-op.datum) 
                 + STRING(l-op.lager-nr, "99") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(36)") 
                 + STRING(l-op.anzahl, "->>>,>>9.99") 
                 + STRING(l-op.warenwert, "->,>>>,>>>,>>9") 
                 + note-str[l-op.op-art]. 
      IF l-op.lief-nr NE 0 THEN 
      DO: 
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE l-lieferant THEN 
          str-list.s = str-list.s + STRING(l-lieferant.firma, "x(20)"). 
        ELSE str-list.s = str-list.s + "                    ". 
      END. 
      ELSE str-list.s = str-list.s + "                    ". 
      IF length(l-op.lscheinnr) GT 16 THEN 
        deliver-no = SUBSTR(l-op.lscheinnr,length(l-op.lscheinnr) - 15, 16). 
      ELSE deliver-no = l-op.lscheinnr. 
      str-list.s = str-list.s 
        + STRING(l-op.docu-nr, "x(12)") 
        + STRING(deliver-no, "x(16)"). 
    END. 
  END. 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 25: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->,>>>,>>>,>>9"). 
END.*/
 
PROCEDURE create-list2: 
    DEFINE VARIABLE epreis AS DECIMAL. 
    DEFINE VARIABLE diff-flag AS LOGICAL. 
    /*MTstatus default "Processing...". */ 
    FOR EACH str-list: 
    delete str-list. 
    END. 

    tot-anz = 0. 
    tot-amount = 0. 
    FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
        AND l-lager.lager-nr LE to-lager: 
        /*  calculate the incoming stocks within the given periods */ 
        FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.anzahl NE 0 AND l-op.loeschflag LT 2 
        AND l-op.op-art = 1 AND l-op.docu-nr NE l-op.lscheinnr 
        NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
            NO-LOCK BY l-artikel.bezeich BY l-op.datum: 
        FIND FIRST l-order WHERE l-order.docu-nr = l-op.docu-nr 
            AND l-order.artnr = l-op.artnr NO-LOCK NO-ERROR. 
        diff-flag = NO. 
        IF AVAILABLE l-order THEN 
        DO: 
            IF l-order.flag THEN epreis = l-order.einzelpreis / l-order.txtnr. 
            ELSE epreis = l-order.einzelpreis. 
            IF price-decimal = 0 THEN 
            DO: 
            IF (epreis - l-op.einzelpreis) GT 1 OR 
                (l-op.einzelpreis - epreis) GT 1 THEN diff-flag = YES. 
            END. 
            ELSE 
            DO: 
            IF (epreis - l-op.einzelpreis) GT 0.01 OR 
                (l-op.einzelpreis - epreis) GT 0.01 THEN diff-flag = YES. 
            END. 
        END. 
        IF diff-flag THEN 
        DO: 
            IF mi-rec-chk = YES THEN
            DO:
                IF l-op.einzelpreis GE epreis THEN
                DO:
                    tot-anz = tot-anz + l-op.anzahl. 
                    tot-amount = tot-amount + l-op.warenwert. 
                    /* create str-list. */ 
                    IF NOT long-digit THEN 
                    DO:
                        /* Malik Serverless 670 comment 
                        str-list.s = STRING(l-op.datum) 
                                + STRING(l-op.lager-nr, "99") 
                                + STRING(l-artikel.artnr, "9999999") 
                                + STRING(l-artikel.bezeich, "x(36)") 
                                + STRING(l-op.anzahl, "->>>,>>9.99") 
                                + STRING(l-op.warenwert, "->>,>>>,>>9.99")
                                + note-str[l-op.op-art].*/
                        CREATE output-list.
                        output-list.datum   = STRING(l-op.datum).
                        output-list.lager   = STRING(l-op.lager-nr, "99").
                        /* output-list.docunr   = */
                        output-list.art     = STRING(l-artikel.artnr, "9999999").
                        output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                        output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                        output-list.amount  = STRING(l-op.warenwert, "->>,>>>,>>9.99").        
                    END.
                    ELSE 
                    DO:
                        /* Malik Serverless 670 comment 
                        str-list.s = STRING(l-op.datum) 
                                + STRING(l-op.lager-nr, "99") 
                                + STRING(l-artikel.artnr, "9999999") 
                                + STRING(l-artikel.bezeich, "x(36)") 
                                + STRING(l-op.anzahl, "->>>,>>9.99") 
                                + STRING(l-op.warenwert, "->,>>>,>>>,>>9") 
                                + note-str[l-op.op-art]. */
                        CREATE output-list.
                        output-list.datum   = STRING(l-op.datum).
                        output-list.lager   = STRING(l-op.lager-nr, "99").
                        /* output-list.docunr   = */
                        output-list.art     = STRING(l-artikel.artnr, "9999999").
                        output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                        output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                        output-list.amount  = STRING(l-op.warenwert, "->,>>>,>>>,>>9").
                        
                    END.
                    IF l-op.lief-nr NE 0 THEN 
                    DO: 
                        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr 
                            NO-LOCK NO-ERROR. 
                        IF AVAILABLE l-lieferant THEN 
                        DO:
                            /* Malik Serverless 670 comment
                            str-list.s = str-list.s + STRING(l-lieferant.firma, "x(20)").*/
                            output-list.lief    = STRING(l-lieferant.firma, "x(20)").
                        END. 
                        ELSE 
                        DO:
                            /* 
                            str-list.s = str-list.s + "                    ".*/
                            output-list.lief = STRING(" ", "x(20)"). 
                        END.
                    END. 
                    ELSE
                    DO:
                        /* 
                        str-list.s = str-list.s + "                    ". */
                        output-list.lief = STRING(" ", "x(20)").
                    END.
                    IF length(l-op.lscheinnr) GT 16 THEN 
                    DO:
                        deliver-no = SUBSTR(l-op.lscheinnr,length(l-op.lscheinnr) - 15, 16). 
                    END.
                    ELSE
                    DO:
                        deliver-no = l-op.lscheinnr. 
                    END. 
                    /* 
                    str-list.s = str-list.s 
                    + STRING(l-op.docu-nr, "x(12)") 
                    + STRING(deliver-no, "x(16)"). 
        
                    IF long-digit THEN 
                    DO: 
                    str-list.s = str-list.s 
                        + STRING(l-op.einzelpreis, "->,>>>,>>>,>>9")    /*received-price*/
                        + STRING(epreis,"->,>>>,>>>,>>9").                /*ordered-price*/
                    END. 
                    ELSE 
                    DO: 
                    str-list.s = str-list.s 
                        + STRING(l-op.einzelpreis, "->>,>>>,>>9.99")    /*received-price*/
                        + STRING(epreis,"->>,>>>,>>9.99").                 /*ordered-price*/
                    END.*/
                    output-list.docunr  = STRING(l-op.docu-nr, "x(12)").
                    output-list.dlvnote = STRING(deliver-no, "x(16)").
                    IF long-digit THEN 
                    DO: 
                        /* 
                        str-list.s = str-list.s 
                            + STRING(l-op.einzelpreis, "->,>>>,>>>,>>9")    /*received-price*/
                            + STRING(epreis,"->,>>>,>>>,>>9").                /*ordered-price*/*/
                        output-list.epreis1 = STRING(l-op.einzelpreis, "->,>>>,>>>,>>9").
                        output-list.epreis2 = STRING(epreis,"->,>>>,>>>,>>9").
                        
                    END. 
                    ELSE 
                    DO: 
                        /* 
                        str-list.s = str-list.s 
                            + STRING(l-op.einzelpreis, "->>,>>>,>>9.99")    /*received-price*/
                            + STRING(epreis,"->>,>>>,>>9.99").                 /*ordered-price*/*/
                        output-list.epreis1 = STRING(l-op.einzelpreis, "->>,>>>,>>9.99").
                        output-list.epreis2 = STRING(epreis,"->>,>>>,>>9.99").
                    END.   
                END.
            END.
            ELSE IF mi-ord-chk = YES THEN
            DO:
                IF epreis GE l-op.einzelpreis THEN
                DO:            
                    tot-anz = tot-anz + l-op.anzahl. 
                    tot-amount = tot-amount + l-op.warenwert. 
                    /* create str-list. */ 
                    IF NOT long-digit THEN 
                    DO:
                        /* Malik Serverless 670 comment
                        str-list.s = STRING(l-op.datum) 
                                + STRING(l-op.lager-nr, "99") 
                                + STRING(l-artikel.artnr, "9999999") 
                                + STRING(l-artikel.bezeich, "x(36)") 
                                + STRING(l-op.anzahl, "->>>,>>9.99") 
                                + STRING(l-op.warenwert, "->>,>>>,>>9.99")
                                + note-str[l-op.op-art]. */
                        CREATE output-list.
                        output-list.datum   = STRING(l-op.datum).
                        output-list.lager   = STRING(l-op.lager-nr, "99").
                        /* output-list.docunr   = */
                        output-list.art     = STRING(l-artikel.artnr, "9999999").
                        output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                        output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                        output-list.amount  = STRING(l-op.warenwert, "->>,>>>,>>9.99").
                    END.
                    ELSE 
                    DO: 
                        /*    
                        str-list.s = STRING(l-op.datum) 
                                + STRING(l-op.lager-nr, "99") 
                                + STRING(l-artikel.artnr, "9999999") 
                                + STRING(l-artikel.bezeich, "x(36)") 
                                + STRING(l-op.anzahl, "->>>,>>9.99") 
                                + STRING(l-op.warenwert, "->,>>>,>>>,>>9") 
                                + note-str[l-op.op-art]. */
                        CREATE output-list.
                        output-list.datum   = STRING(l-op.datum).
                        output-list.lager   = STRING(l-op.lager-nr, "99").
                        /* output-list.docunr   = */
                        output-list.art     = STRING(l-artikel.artnr, "9999999").
                        output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                        output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                        output-list.amount  = STRING(l-op.warenwert, "->,>>>,>>>,>>9").
                    END.
                    IF l-op.lief-nr NE 0 THEN 
                    DO: 
                        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr 
                            NO-LOCK NO-ERROR. 
                        IF AVAILABLE l-lieferant THEN 
                        DO:
                            /* 
                            str-list.s = str-list.s + STRING(l-lieferant.firma, "x(20)"). */
                            output-list.lief = STRING(l-lieferant.firma, "x(20)").
                        END.
                        ELSE 
                        DO:
                            /* 
                            str-list.s = str-list.s + "                    ".*/
                            output-list.lief = STRING(" ", "x(20)"). 
                        END.
                    END. 
                    ELSE
                    DO:
                        /* 
                        str-list.s = str-list.s + "                    ". */
                        output-list.lief = STRING(" ", "x(20)").
                    END. 
                    IF length(l-op.lscheinnr) GT 16 THEN 
                    DO:
                        deliver-no = SUBSTR(l-op.lscheinnr,length(l-op.lscheinnr) - 15, 16).
                    END. 
                    ELSE 
                    DO:
                        deliver-no = l-op.lscheinnr. 
                    END.
                    /* 
                    str-list.s = str-list.s 
                    + STRING(l-op.docu-nr, "x(12)") 
                    + STRING(deliver-no, "x(16)"). 
        
                    IF long-digit THEN 
                    DO: 
                    str-list.s = str-list.s 
                        + STRING(l-op.einzelpreis, "->,>>>,>>>,>>9")    /*received-price*/
                        + STRING(epreis,"->,>>>,>>>,>>9").                /*ordered-price*/
                    END. 
                    ELSE 
                    DO: 
                    str-list.s = str-list.s 
                        + STRING(l-op.einzelpreis, "->>,>>>,>>9.99")    /*received-price*/
                        + STRING(epreis,"->>,>>>,>>9.99").                 /*ordered-price*/
                    END. */
                    output-list.docunr  = STRING(l-op.docu-nr, "x(12)").
                    output-list.dlvnote = STRING(deliver-no, "x(16)").
                    IF long-digit THEN 
                    DO:
                        /*  
                        str-list.s = str-list.s 
                            + STRING(l-op.einzelpreis, "->,>>>,>>>,>>9")    /*received-price*/
                            + STRING(epreis,"->,>>>,>>>,>>9").                /*ordered-price*/*/
                        output-list.epreis1 = STRING(l-op.einzelpreis, "->,>>>,>>>,>>9").
                        output-list.epreis2 = STRING(epreis,"->,>>>,>>>,>>9").
                    END. 
                    ELSE 
                    DO: 
                        /* 
                        str-list.s = str-list.s 
                            + STRING(l-op.einzelpreis, "->>,>>>,>>9.99")    /*received-price*/
                            + STRING(epreis,"->>,>>>,>>9.99").                 /*ordered-price*/*/
                        output-list.epreis1 = STRING(l-op.einzelpreis, "->>,>>>,>>9.99").
                        output-list.epreis2 = STRING(epreis,"->>,>>>,>>9.99").
                    END.
                END.
            END.
            ELSE IF mi-all-chk = YES THEN
            DO:
                tot-anz = tot-anz + l-op.anzahl. 
                tot-amount = tot-amount + l-op.warenwert. 
                /* create str-list. */ 
                IF NOT long-digit THEN 
                DO:
                    /* 
                    str-list.s = STRING(l-op.datum) 
                            + STRING(l-op.lager-nr, "99") 
                            + STRING(l-artikel.artnr, "9999999") 
                            + STRING(l-artikel.bezeich, "x(36)") 
                            + STRING(l-op.anzahl, "->>>,>>9.99") 
                            + STRING(l-op.warenwert, "->>,>>>,>>9.99")
                            + note-str[l-op.op-art].*/
                    CREATE output-list.
                    output-list.datum   = STRING(l-op.datum).
                    output-list.lager   = STRING(l-op.lager-nr, "99").
                    /* output-list.docunr   = */
                    output-list.art     = STRING(l-artikel.artnr, "9999999").
                    output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                    output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                    output-list.amount  = STRING(l-op.warenwert, "->>,>>>,>>9.99").
                END.         
                ELSE 
                DO:
                    /* 
                    str-list.s = STRING(l-op.datum) 
                            + STRING(l-op.lager-nr, "99") 
                            + STRING(l-artikel.artnr, "9999999") 
                            + STRING(l-artikel.bezeich, "x(36)") 
                            + STRING(l-op.anzahl, "->>>,>>9.99") 
                            + STRING(l-op.warenwert, "->,>>>,>>>,>>9") 
                            + note-str[l-op.op-art]. */
                    CREATE output-list.
                    output-list.datum   = STRING(l-op.datum).
                    output-list.lager   = STRING(l-op.lager-nr, "99").
                    /* output-list.docunr   = */
                    output-list.art     = STRING(l-artikel.artnr, "9999999").
                    output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                    output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                    output-list.amount  = STRING(l-op.warenwert, "->,>>>,>>>,>>9").
                END.
                IF l-op.lief-nr NE 0 THEN 
                DO: 
                    FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr 
                    NO-LOCK NO-ERROR. 
                    IF AVAILABLE l-lieferant THEN 
                    DO:
                        /* 
                        str-list.s = str-list.s + STRING(l-lieferant.firma, "x(20)").*/
                        output-list.lief = STRING(l-lieferant.firma, "x(20)").
                    END.     
                    ELSE
                    DO:
                        /* 
                        str-list.s = str-list.s + "                    ".*/
                        output-list.lief = STRING(" ", "x(20)").
                    END.  
                END. 
                ELSE
                DO:
                    /* 
                    str-list.s = str-list.s + "                    ". */
                    output-list.lief = STRING(" ", "x(20)").
                END. 
                IF length(l-op.lscheinnr) GT 16 THEN
                DO: 
                    deliver-no = SUBSTR(l-op.lscheinnr,length(l-op.lscheinnr) - 15, 16). 
                END.
                ELSE
                DO:
                    deliver-no = l-op.lscheinnr. 
                END.
                /* Malik Serverless 670 comment  
                str-list.s = str-list.s 
                + STRING(l-op.docu-nr, "x(12)") 
                + STRING(deliver-no, "x(16)"). 
    
                IF long-digit THEN 
                DO: 
                    str-list.s = str-list.s 
                        + STRING(l-op.einzelpreis, "->,>>>,>>>,>>9")    /*received-price*/
                        + STRING(epreis,"->,>>>,>>>,>>9").                /*ordered-price*/
                END. 
                ELSE 
                DO: 
                    str-list.s = str-list.s 
                        + STRING(l-op.einzelpreis, "->>,>>>,>>9.99")    /*received-price*/
                        + STRING(epreis,"->>,>>>,>>9.99").                 /*ordered-price*/
                END.*/
                output-list.docunr  = STRING(l-op.docu-nr, "x(12)").
                output-list.dlvnote = STRING(deliver-no, "x(16)"). 
                IF long-digit THEN 
                DO:
                    /*  
                    str-list.s = str-list.s 
                        + STRING(l-op.einzelpreis, "->,>>>,>>>,>>9")    /*received-price*/
                        + STRING(epreis,"->,>>>,>>>,>>9").                /*ordered-price*/*/
                    output-list.epreis1 = STRING(l-op.einzelpreis, "->,>>>,>>>,>>9").
                    output-list.epreis2 = STRING(epreis,"->,>>>,>>>,>>9").
                END. 
                ELSE 
                DO: 
                    /* 
                    str-list.s = str-list.s 
                        + STRING(l-op.einzelpreis, "->>,>>>,>>9.99")    /*received-price*/
                        + STRING(epreis,"->>,>>>,>>9.99").                 /*ordered-price*/*/
                    output-list.epreis1 = STRING(l-op.einzelpreis, "->>,>>>,>>9.99").
                    output-list.epreis2 = STRING(epreis,"->>,>>>,>>9.99").
                END.
            END.        
        END. 
        END. 
    END. 


    IF mi-rec-chk = YES AND tot-anz NE 0 AND tot-amount NE 0 THEN
    DO:
        /*    
        create str-list. 
        DO i = 1 TO 17: 
            str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 25: 
            str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                    + STRING(tot-amount, "->>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                    + STRING(tot-amount, "->,>>>,>>>,>>9"). */
        CREATE output-list.
        output-list.datum   = STRING(" ", "x(8)").
        output-list.lager   = STRING(" ", "x(2)").
        output-list.art     = STRING(" ", "x(7)").
        output-list.bezeich = STRING("T O T A L", "x(36)").
        IF NOT long-digit THEN 
        DO:
            output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
            output-list.amount  = STRING(tot-amount, "->>,>>>,>>9.99").
        END.
        ELSE
        DO: 
            output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
            output-list.amount  = STRING(tot-amount, "->,>>>,>>>,>>9").
        END.
    END.
    ELSE IF mi-ord-chk = YES AND tot-anz NE 0 AND tot-amount NE 0 THEN
    DO:
        /* 
        create str-list. 
        DO i = 1 TO 17: 
            str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 25: 
            str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                    + STRING(tot-amount, "->>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                    + STRING(tot-amount, "->,>>>,>>>,>>9"). */
        CREATE output-list.
        output-list.datum   = STRING(" ", "x(8)").
        output-list.lager   = STRING(" ", "x(2)").
        output-list.art     = STRING(" ", "x(7)").
        output-list.bezeich = STRING("T O T A L", "x(36)").
        IF NOT long-digit THEN 
        DO:
            output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
            output-list.amount  = STRING(tot-amount, "->>,>>>,>>9.99").
        END.
        ELSE
        DO: 
            output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
            output-list.amount  = STRING(tot-amount, "->,>>>,>>>,>>9").
        END.
    END.
    ELSE IF mi-all-chk = YES THEN
    DO:
        /* 
        create str-list. 
        DO i = 1 TO 17: 
            str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 25: 
            str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                    + STRING(tot-amount, "->>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                    + STRING(tot-amount, "->,>>>,>>>,>>9").*/
        CREATE output-list.
        output-list.datum   = STRING(" ", "x(8)").
        output-list.lager   = STRING(" ", "x(2)").
        output-list.art     = STRING(" ", "x(7)").
        output-list.bezeich = STRING("T O T A L", "x(36)").
        IF NOT long-digit THEN 
        DO:
            output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
            output-list.amount  = STRING(tot-amount, "->>,>>>,>>9.99").
        END.
        ELSE
        DO: 
            output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
            output-list.amount  = STRING(tot-amount, "->,>>>,>>>,>>9").
        END. 
    END.
END.

PROCEDURE create-list3: 
    DEFINE VARIABLE epreis AS DECIMAL. 
    DEFINE VARIABLE diff-flag AS LOGICAL. 
    /*MTstatus default "Processing...". */ 
    FOR EACH str-list: 
    delete str-list. 
    END. 

    tot-anz = 0. 
    tot-amount = 0. 
    FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
        AND l-lager.lager-nr LE to-lager: 
        /*  calculate the incoming stocks within the given periods */ 
        FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
            AND l-op.datum GE from-date AND l-op.datum LE to-date 
            AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
            AND l-op.anzahl NE 0 AND l-op.loeschflag LT 2 
            AND l-op.op-art = 1 AND l-op.docu-nr NE l-op.lscheinnr 
            NO-LOCK USE-INDEX artopart_ix, 
            FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
                NO-LOCK BY l-op.datum BY l-op.lscheinnr BY l-artikel.bezeich: 
            FIND FIRST l-order WHERE l-order.docu-nr = l-op.docu-nr 
                AND l-order.artnr = l-op.artnr NO-LOCK NO-ERROR. 
            diff-flag = NO. 
            IF AVAILABLE l-order THEN 
            DO: 
                IF l-order.flag THEN epreis = l-order.einzelpreis / l-order.txtnr. 
                ELSE epreis = l-order.einzelpreis. 
                IF price-decimal = 0 THEN 
                DO: 
                IF (epreis - l-op.einzelpreis) GT 1 OR 
                    (l-op.einzelpreis - epreis) GT 1 THEN diff-flag = YES. 
                END. 
                ELSE 
                DO: 
                IF (epreis - l-op.einzelpreis) GT 0.01 OR 
                    (l-op.einzelpreis - epreis) GT 0.01 THEN diff-flag = YES. 
                END. 
            END. 
            IF diff-flag THEN 
            DO: 
                IF mi-rec-chk = YES THEN
                DO:
                    IF l-op.einzelpreis GE epreis THEN
                    DO:
                        tot-anz = tot-anz + l-op.anzahl. 
                        tot-amount = tot-amount + l-op.warenwert. 
                        /* create str-list. */ 
                        IF NOT long-digit THEN 
                        DO:
                            /* 
                            str-list.s = STRING(l-op.datum) 
                                    + STRING(l-op.lager-nr, "99") 
                                    + STRING(l-artikel.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(36)") 
                                    + STRING(l-op.anzahl, "->>>,>>9.99") 
                                    + STRING(l-op.warenwert, "->>,>>>,>>9.99")
                                    + note-str[l-op.op-art]. */
                            CREATE output-list.
                            output-list.datum   = STRING(l-op.datum).
                            output-list.lager   = STRING(l-op.lager-nr, "99").
                            /* output-list.docunr   = */
                            output-list.art     = STRING(l-artikel.artnr, "9999999").
                            output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                            output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                            output-list.amount  = STRING(l-op.warenwert, "->>,>>>,>>9.99").
                        END.
                        ELSE 
                        DO:
                            /* 
                            str-list.s = STRING(l-op.datum) 
                                    + STRING(l-op.lager-nr, "99") 
                                    + STRING(l-artikel.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(36)") 
                                    + STRING(l-op.anzahl, "->>>,>>9.99") 
                                    + STRING(l-op.warenwert, "->,>>>,>>>,>>9") 
                                    + note-str[l-op.op-art].*/
                            CREATE output-list.
                            output-list.datum   = STRING(l-op.datum).
                            output-list.lager   = STRING(l-op.lager-nr, "99").
                            /* output-list.docunr   = */
                            output-list.art     = STRING(l-artikel.artnr, "9999999").
                            output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                            output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                            output-list.amount  = STRING(l-op.warenwert, "->,>>>,>>>,>>9").         
                        END.        
                        IF l-op.lief-nr NE 0 THEN 
                        DO: 
                            FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr 
                                NO-LOCK NO-ERROR. 
                            IF AVAILABLE l-lieferant THEN 
                            DO:
                                /* 
                                str-list.s = str-list.s + STRING(l-lieferant.firma, "x(20)"). */
                                output-list.lief    = STRING(l-lieferant.firma, "x(20)").
                            END.
                            ELSE
                            DO:
                                /* 
                                str-list.s = str-list.s + "                    ". */
                                output-list.lief = STRING(" ", "x(20)"). 
                            END.
                        END. 
                        ELSE 
                        DO:
                            /* 
                            str-list.s = str-list.s + "                    ".*/
                            output-list.lief = STRING(" ", "x(20)"). 
                        END.

                        IF length(l-op.lscheinnr) GT 16 THEN 
                        DO:
                            deliver-no = SUBSTR(l-op.lscheinnr,length(l-op.lscheinnr) - 15, 16). 
                        END.
                        ELSE
                        DO:
                            deliver-no = l-op.lscheinnr. 
                        END.
                        /* 
                        str-list.s = str-list.s 
                        + STRING(l-op.docu-nr, "x(12)") 
                        + STRING(deliver-no, "x(16)"). 
                        
                        IF long-digit THEN 
                        DO: 
                        str-list.s = str-list.s 
                            + STRING(l-op.einzelpreis, "->,>>>,>>>,>>9")    /*received-price*/
                            + STRING(epreis,"->,>>>,>>>,>>9").                /*ordered-price*/
                        END. 
                        ELSE 
                        DO: 
                        str-list.s = str-list.s 
                            + STRING(l-op.einzelpreis, "->>,>>>,>>9.99")    /*received-price*/
                            + STRING(epreis,"->>,>>>,>>9.99").                 /*ordered-price*/
                        END.  */
                        output-list.docunr  = STRING(l-op.docu-nr, "x(12)").
                        output-list.dlvnote = STRING(deliver-no, "x(16)").  
                        IF long-digit THEN 
                        DO: 
                            output-list.epreis1 = STRING(l-op.einzelpreis, "->,>>>,>>>,>>9").
                            output-list.epreis2 = STRING(epreis,"->,>>>,>>>,>>9").
                        END. 
                        ELSE 
                        DO: 
                            output-list.epreis1 = STRING(l-op.einzelpreis, "->>,>>>,>>9.99").
                            output-list.epreis2 = STRING(epreis,"->>,>>>,>>9.99").
                        END. 

                    END.
                END.
                ELSE IF mi-ord-chk = YES THEN
                DO:
                    IF epreis GE l-op.einzelpreis THEN
                    DO:            
                        tot-anz = tot-anz + l-op.anzahl. 
                        tot-amount = tot-amount + l-op.warenwert. 
                        /*create str-list.*/ 
                        IF NOT long-digit THEN 
                        DO:
                            /* 
                            str-list.s = STRING(l-op.datum) 
                                    + STRING(l-op.lager-nr, "99") 
                                    + STRING(l-artikel.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(36)") 
                                    + STRING(l-op.anzahl, "->>>,>>9.99") 
                                    + STRING(l-op.warenwert, "->>,>>>,>>9.99")
                                    + note-str[l-op.op-art]. */
                            CREATE output-list.
                            output-list.datum   = STRING(l-op.datum).
                            output-list.lager   = STRING(l-op.lager-nr, "99").
                            /* output-list.docunr   = */
                            output-list.art     = STRING(l-artikel.artnr, "9999999").
                            output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                            output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                            output-list.amount  = STRING(l-op.warenwert, "->>,>>>,>>9.99").
                        END.       
                        ELSE 
                        DO:
                            /* 
                            str-list.s = STRING(l-op.datum) 
                                    + STRING(l-op.lager-nr, "99") 
                                    + STRING(l-artikel.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(36)") 
                                    + STRING(l-op.anzahl, "->>>,>>9.99") 
                                    + STRING(l-op.warenwert, "->,>>>,>>>,>>9") 
                                    + note-str[l-op.op-art]. */
                            CREATE output-list.
                            output-list.datum   = STRING(l-op.datum).
                            output-list.lager   = STRING(l-op.lager-nr, "99").
                            /* output-list.docunr   = */
                            output-list.art     = STRING(l-artikel.artnr, "9999999").
                            output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                            output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                            output-list.amount  = STRING(l-op.warenwert, "->,>>>,>>>,>>9").
                        END.
                        IF l-op.lief-nr NE 0 THEN 
                        DO: 
                            FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr 
                                NO-LOCK NO-ERROR. 
                            IF AVAILABLE l-lieferant THEN
                            DO: 
                                /* 
                                str-list.s = str-list.s + STRING(l-lieferant.firma, "x(20)"). */
                                output-list.lief    = STRING(l-lieferant.firma, "x(20)").
                            END.
                            ELSE
                            DO:
                                /* 
                                str-list.s = str-list.s + "                    ".*/
                                output-list.lief = STRING(" ", "x(20)").

                            END.
                        END. 
                        ELSE
                        DO:
                            /* 
                            str-list.s = str-list.s + "                    ".*/
                            output-list.lief = STRING(" ", "x(20)"). 
                        END.
                        IF length(l-op.lscheinnr) GT 16 THEN 
                        DO:
                            deliver-no = SUBSTR(l-op.lscheinnr,length(l-op.lscheinnr) - 15, 16). 
                        END.
                        ELSE 
                        DO:
                            deliver-no = l-op.lscheinnr. 
                        END.
                        /* 
                        str-list.s = str-list.s 
                        + STRING(l-op.docu-nr, "x(12)") 
                        + STRING(deliver-no, "x(16)"). 
                        
                        IF long-digit THEN 
                        DO: 
                        str-list.s = str-list.s 
                            + STRING(l-op.einzelpreis, "->,>>>,>>>,>>9")    /*received-price*/
                            + STRING(epreis,"->,>>>,>>>,>>9").                /*ordered-price*/
                        END. 
                        ELSE 
                        DO: 
                        str-list.s = str-list.s 
                            + STRING(l-op.einzelpreis, "->>,>>>,>>9.99")    /*received-price*/
                            + STRING(epreis,"->>,>>>,>>9.99").                 /*ordered-price*/
                        END. */
                        output-list.docunr  = STRING(l-op.docu-nr, "x(12)").
                        output-list.dlvnote = STRING(deliver-no, "x(16)").  
                        IF long-digit THEN 
                        DO: 
                            output-list.epreis1 = STRING(l-op.einzelpreis, "->,>>>,>>>,>>9").
                            output-list.epreis2 = STRING(epreis,"->,>>>,>>>,>>9").
                        END. 
                        ELSE 
                        DO: 
                            output-list.epreis1 = STRING(l-op.einzelpreis, "->>,>>>,>>9.99").
                            output-list.epreis2 = STRING(epreis,"->>,>>>,>>9.99").
                        END. 
                    END.
                END.
                ELSE IF mi-all-chk = YES THEN
                DO:
                    tot-anz = tot-anz + l-op.anzahl. 
                    tot-amount = tot-amount + l-op.warenwert. 
                    /* create str-list. */ 
                    IF NOT long-digit THEN 
                    DO:
                        /* 
                        str-list.s = STRING(l-op.datum) 
                                + STRING(l-op.lager-nr, "99") 
                                + STRING(l-artikel.artnr, "9999999") 
                                + STRING(l-artikel.bezeich, "x(36)") 
                                + STRING(l-op.anzahl, "->>>,>>9.99") 
                                + STRING(l-op.warenwert, "->>,>>>,>>9.99")
                                + note-str[l-op.op-art].*/
                        CREATE output-list.
                        output-list.datum   = STRING(l-op.datum).
                        output-list.lager   = STRING(l-op.lager-nr, "99").
                        /* output-list.docunr   = */
                        output-list.art     = STRING(l-artikel.artnr, "9999999").
                        output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                        output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                        output-list.amount  = STRING(l-op.warenwert, "->>,>>>,>>9.99"). 
                    END.
                    ELSE 
                    DO:
                        /* 
                        str-list.s = STRING(l-op.datum) 
                                + STRING(l-op.lager-nr, "99") 
                                + STRING(l-artikel.artnr, "9999999") 
                                + STRING(l-artikel.bezeich, "x(36)") 
                                + STRING(l-op.anzahl, "->>>,>>9.99") 
                                + STRING(l-op.warenwert, "->,>>>,>>>,>>9") 
                                + note-str[l-op.op-art].*/
                        CREATE output-list.
                        output-list.datum   = STRING(l-op.datum).
                        output-list.lager   = STRING(l-op.lager-nr, "99").
                        /* output-list.docunr   = */
                        output-list.art     = STRING(l-artikel.artnr, "9999999").
                        output-list.bezeich = STRING(l-artikel.bezeich, "x(36)").
                        output-list.in-qty  = STRING(l-op.anzahl, "->>>,>>9.99").
                        output-list.amount  = STRING(l-op.warenwert, "->,>>>,>>>,>>9").
                    END.
                    IF l-op.lief-nr NE 0 THEN 
                    DO: 
                        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr 
                            NO-LOCK NO-ERROR. 
                        IF AVAILABLE l-lieferant THEN 
                        DO:
                            /* 
                            str-list.s = str-list.s + STRING(l-lieferant.firma, "x(20)").*/
                            output-list.lief    = STRING(l-lieferant.firma, "x(20)").
                        END.
                        ELSE
                        DO:
                            /* 
                            str-list.s = str-list.s + "                    ".*/
                            output-list.lief = STRING(" ", "x(20)").
                        END. 
                    END. 
                    ELSE
                    DO:
                        /* 
                        str-list.s = str-list.s + "                    ". */
                        output-list.lief = STRING(" ", "x(20)"). 
                    END.
                    IF length(l-op.lscheinnr) GT 16 THEN 
                    DO:
                        deliver-no = SUBSTR(l-op.lscheinnr,length(l-op.lscheinnr) - 15, 16). 
                    END.
                    ELSE
                    DO:
                        deliver-no = l-op.lscheinnr.
                    END. 
                    /* 
                    str-list.s = str-list.s 
                    + STRING(l-op.docu-nr, "x(12)") 
                    + STRING(deliver-no, "x(16)"). 
                    
                    IF long-digit THEN 
                    DO: 
                    str-list.s = str-list.s 
                        + STRING(l-op.einzelpreis, "->,>>>,>>>,>>9")    /*received-price*/
                        + STRING(epreis,"->,>>>,>>>,>>9").                /*ordered-price*/
                    END. 
                    ELSE 
                    DO: 
                    str-list.s = str-list.s 
                        + STRING(l-op.einzelpreis, "->>,>>>,>>9.99")    /*received-price*/
                        + STRING(epreis,"->>,>>>,>>9.99").                 /*ordered-price*/
                    END. */
                    output-list.docunr  = STRING(l-op.docu-nr, "x(12)").
                    output-list.dlvnote = STRING(deliver-no, "x(16)").  
                    IF long-digit THEN 
                    DO: 
                        output-list.epreis1 = STRING(l-op.einzelpreis, "->,>>>,>>>,>>9").
                        output-list.epreis2 = STRING(epreis,"->,>>>,>>>,>>9").
                    END. 
                    ELSE 
                    DO: 
                        output-list.epreis1 = STRING(l-op.einzelpreis, "->>,>>>,>>9.99").
                        output-list.epreis2 = STRING(epreis,"->>,>>>,>>9.99").
                    END.    
                END.        
            END. 
        END. 
    END. 


    IF mi-rec-chk = YES AND tot-anz NE 0 AND tot-amount NE 0 THEN
    DO:
        /*    
        create str-list. 
        DO i = 1 TO 17: 
            str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 25: 
            str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                    + STRING(tot-amount, "->>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                    + STRING(tot-amount, "->,>>>,>>>,>>9").*/
        CREATE output-list.
        output-list.datum   = STRING(" ", "x(8)").
        output-list.lager   = STRING(" ", "x(2)").
        output-list.art     = STRING(" ", "x(7)").
        output-list.bezeich = STRING("T O T A L", "x(36)").
        IF NOT long-digit THEN 
        DO:
            output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
            output-list.amount  = STRING(tot-amount, "->>,>>>,>>9.99").
        END.
        ELSE
        DO: 
            output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
            output-list.amount  = STRING(tot-amount, "->,>>>,>>>,>>9").
        END.
         
    END.
    ELSE IF mi-ord-chk = YES AND tot-anz NE 0 AND tot-amount NE 0 THEN
    DO:
        /* 
        create str-list. 
        DO i = 1 TO 17: 
            str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 25: 
            str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                    + STRING(tot-amount, "->>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                    + STRING(tot-amount, "->,>>>,>>>,>>9"). */

        CREATE output-list.
        output-list.datum   = STRING(" ", "x(8)").
        output-list.lager   = STRING(" ", "x(2)").
        output-list.art     = STRING(" ", "x(7)").
        output-list.bezeich = STRING("T O T A L", "x(36)").
        IF NOT long-digit THEN 
        DO:
            output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
            output-list.amount  = STRING(tot-amount, "->>,>>>,>>9.99").
        END.
        ELSE
        DO: 
            output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
            output-list.amount  = STRING(tot-amount, "->,>>>,>>>,>>9").
        END. 
    END.
    ELSE IF mi-all-chk = YES THEN
    DO:
        /* 
        create str-list. 
        DO i = 1 TO 17: 
            str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 25: 
            str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                    + STRING(tot-amount, "->>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
                    + STRING(tot-amount, "->,>>>,>>>,>>9"). */
        CREATE output-list.
        output-list.datum   = STRING(" ", "x(8)").
        output-list.lager   = STRING(" ", "x(2)").
        output-list.art     = STRING(" ", "x(7)").
        output-list.bezeich = STRING("T O T A L", "x(36)").
        IF NOT long-digit THEN 
        DO:
            output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
            output-list.amount  = STRING(tot-amount, "->>,>>>,>>9.99").
        END.
        ELSE
        DO: 
            output-list.in-qty  = STRING(tot-anz, "->,>>>,>>9.99").
            output-list.amount  = STRING(tot-amount, "->,>>>,>>>,>>9").
        END.
    END.
END.

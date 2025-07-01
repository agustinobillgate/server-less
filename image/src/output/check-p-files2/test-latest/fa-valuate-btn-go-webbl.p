/*ITA 160215 --> detail for sorting by COA*/

DEFINE TEMP-TABLE lagerBuff LIKE fa-lager.

DEFINE TEMP-TABLE out-list
    FIELD flag AS INT
    FIELD fibu AS CHAR
    FIELD bezeich AS CHAR
    FIELD refno AS CHAR
    FIELD location AS CHAR
    FIELD received AS DATE
    FIELD qty AS DECIMAL
    FIELD init-val AS DECIMAL
    FIELD depn-val AS DECIMAL
    FIELD book-val AS DECIMAL
    FIELD depn-no AS INT
    FIELD first-depn AS DATE
    FIELD next-depn AS DATE
    FIELD last-depn AS DATE
    FIELD kateg AS CHAR.


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
DEFINE OUTPUT PARAMETER TABLE FOR out-list.
/*
DEFINE VAR pvILanguage          AS INTEGER  INIT 1.
DEFINE VAR mi-lager-chk         AS LOGICAL  INIT NO.
DEFINE VAR mi-subgrp-chk        AS LOGICAL  INIT NO.
DEFINE VAR mi-acct-chk          AS LOGICAL  INIT YES.
DEFINE VAR mi-bookvalue-chk     AS LOGICAL  INIT NO.
DEFINE VAR from-grp             AS INTEGER  INIT 0.
DEFINE VAR from-date            AS DATE     INIT 12/01/21.
DEFINE VAR to-lager             AS INTEGER  INIT 12.
DEFINE VAR from-lager           AS INTEGER  INIT 1.
DEFINE VAR maxNr                AS INTEGER.
DEFINE VAR to-date              AS DATE     INIT 12/31/21.
DEFINE VAR zero-value-only      AS LOGICAL  INIT NO.
DEFINE VAR last-acctdate        AS DATE.
DEFINE VAR yy                   AS INTEGER.
DEFINE VAR mm                   AS INTEGER.
DEFINE VAR from-subgr           AS INTEGER.
DEFINE VAR to-subgr             AS INTEGER.

FOR EACH fa-lager NO-LOCK BY fa-lager.lager-nr:
  CREATE lagerBuff.
  BUFFER-COPY fa-lager TO lagerBuff.
  maxNr = fa-lager.lager-nr.
END.
maxNr = maxNr + 1.
CREATE lagerBuff.
ASSIGN lagerBuff.lager-nr = maxNr
      lagerBuff.bezeich = "".

FIND FIRST htparam WHERE paramnr = 881 no-lock.    /* LAST Dep'n DATE */ 
last-acctdate = htparam.fdate.

mm = MONTH(last-acctdate). 
yy = YEAR(last-acctdate). 
*/
DEFINE VARIABLE do-it       AS LOGICAL INITIAL NO.
DEFINE VARIABLE sub-depn    AS INTEGER NO-UNDO.
DEFINE VARIABLE val-dep     AS DECIMAL NO-UNDO.
DEFINE VARIABLE datum       AS DATE    NO-UNDO.
DEFINE VARIABLE flag        AS LOGICAL NO-UNDO.

DEFINE VARIABLE p-depn-wert AS DECIMAL NO-UNDO.
DEFINE VARIABLE p-book-wert AS DECIMAL NO-UNDO.

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
    /* adding new procedure and condition so filter by Main Group can work by Oscar (B3BA7B) */
    IF from-grp = 0 THEN
        RUN create-listsgrp. 
    ELSE RUN create-listsgrp1.
END. 
ELSE IF mi-acct-chk = YES THEN 
DO: 
    /* adding new procedure and condition so filter by Main Group can work by Oscar (B3BA7B) */
    IF from-grp = 0 THEN
        RUN create-listacct. 
    ELSE RUN create-listacct1.
END. 

/*
for each out-list:
disp out-list.fibu out-list.bezeich out-list.received out-list.qty out-list.init-val.
end.*/

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

    ASSIGN
        tot-anz  = 0 
        tot-val  = 0 
        tot-val1 = 0 
        tot-val2 = 0.

    /* max-lager = to-lager.
    IF from-lager NE to-lager AND (maxNr - 1) = to-lager THEN max-lager = maxNr. */
    FOR EACH lagerBuff WHERE lagerBuff.lager-nr GE from-lager 
    AND lagerBuff.lager-nr LE to-lager: 
    
        CREATE out-list.
        ASSIGN
            out-list.bezeich = STRING(lagerBuff.lager-nr, ">>99") + "-" + lagerBuff.bezeich
            i = 0
            zwkum = 0
            t-anz = 0 
            t-val = 0 
            t-val1 = 0 
            t-val2 = 0 
            tt-anz = 0 
            tt-val = 0 
            tt-val1 = 0 
            tt-val2 = 0. 
    
        /*ITA 110315*/
        IF mi-bookvalue-chk = YES THEN 
        DO:
            FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich
            AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
            FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr NO-LOCK, 
            /* FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.nr NO-LOCK,  */
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
                            CREATE out-list.
                            ASSIGN 
                                out-list.flag = 1
                                out-list.refno = "SUB TOTAL"
                                out-list.qty = t-anz
                                out-list.init-val = t-val
                                out-list.depn-val = t-val1
                                out-list.book-val = t-val2.
                        END. 
                    
                        CREATE out-list.     
                        ASSIGN
                            out-list.bezeich = fa-grup.bezeich
                            t-anz  = 0 
                            t-val  = 0 
                            t-val1 = 0 
                            t-val2 = 0 
                            zwkum  = fa-artikel.gnr. 
                    END. 
                
                    CREATE out-list.
                    ASSIGN
                        out-list.flag = 1
                        out-list.refno = mathis.asset
                        out-list.bezeich = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty = fa-artikel.anzahl.

                
                    ASSIGN val-dep      = fa-artikel.depn-wert / fa-artikel.anz-depn
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


                    ASSIGN 
                        p-depn-wert = val-dep * sub-depn
                        p-book-wert = fa-artikel.warenwert - p-depn-wert
                        i = i + 1

                        /*SUB TOTAl*/
                        t-anz = t-anz + fa-artikel.anzahl
                        t-val = t-val + fa-artikel.warenwert
                        t-val1 = t-val1 + p-depn-wert 
                        t-val2 = t-val2 + p-book-wert 

                        /*TOTAL*/
                        tt-anz = tt-anz + fa-artikel.anzahl
                        tt-val = tt-val + fa-artikel.warenwert
                        tt-val1 = tt-val1 + p-depn-wert
                        tt-val2 = tt-val2 + p-book-wert 

                        /*Grand TOTAL*/
                        tot-anz = tot-anz + fa-artikel.anzahl
                        tot-val = tot-val + fa-artikel.warenwert
                        tot-val1 = tot-val1 + p-depn-wert 
                        tot-val2 = tot-val2 + p-book-wert 
                        
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = p-depn-wert
                        out-list.book-val = p-book-wert.

                    /* added FIND FIRST because fa-kateg not found by Oscar (26 Agustus 2024) - B3BA7B */
                    FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-kateg THEN
                    DO:
                        ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                    END.

                    IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                    IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                    IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                    IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = sub-depn. 
                END.
            END.
        END. /*end ITA*/
        ELSE 
        DO:
            FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich
            AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
            FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            /*AND fa-artikel.loeschflag = 0*/ NO-LOCK, 
            /* FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.nr NO-LOCK,  */
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
                            CREATE out-list.
                            ASSIGN
                                out-list.flag = 1
                                out-list.refno = "SUB TOTAL"
                                out-list.qty = t-anz
                                out-list.init-val = t-val
                                out-list.depn-val = t-val1
                                out-list.book-val = t-val2.
                        END. 
                
                        CREATE out-list.
                        ASSIGN
                            out-list.bezeich = fa-grup.bezeich
                            t-anz  = 0 
                            t-val  = 0 
                            t-val1 = 0 
                            t-val2 = 0 
                            zwkum  = fa-artikel.gnr. 
                    END. 

                    ASSIGN
                        i = i + 1
                        t-anz = t-anz + fa-artikel.anzahl
                        t-val = t-val + fa-artikel.warenwert 
                        t-val1 = t-val1 + fa-artikel.depn-wert 
                        t-val2 = t-val2 + fa-artikel.book-wert 
                        tt-anz = tt-anz + fa-artikel.anzahl 
                        tt-val = tt-val + fa-artikel.warenwert
                        tt-val1 = tt-val1 + fa-artikel.depn-wert
                        tt-val2 = tt-val2 + fa-artikel.book-wert 
                        tot-anz = tot-anz + fa-artikel.anzahl 
                        tot-val = tot-val + fa-artikel.warenwert
                        tot-val1 = tot-val1 + fa-artikel.depn-wert
                        tot-val2 = tot-val2 + fa-artikel.book-wert. 
         
                    CREATE out-list.
                    ASSIGN
                        out-list.flag = 1
                        out-list.bezeich = mathis.NAME
                        out-list.refno = mathis.asset
                        out-list.received = mathis.datum
                        out-list.qty = fa-artikel.anzahl
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = depn-wert
                        out-list.book-val = book-wert.

                    /* added FIND FIRST because fa-kateg not found by Oscar (26 Agustus 2024) - B3BA7B */
                    FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-kateg THEN
                    DO:
                        ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                    END.
                        
                    IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                    IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                    IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                    IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = fa-artikel.anz-depn. 
                END.
            END.
        END.
 
        CREATE out-list.
        ASSIGN
            out-list.flag = 1
            out-list.refno = "SUB TOTAL"
            out-list.qty = t-anz
            out-list.init-val = t-val
            out-list.depn-val = t-val1
            out-list.book-val = t-val2.

        CREATE out-list.
        ASSIGN
            out-list.refno = "T O T A L"
            out-list.flag = 1
            out-list.qty = tt-anz
            out-list.init-val = tt-val
            out-list.depn-val = tt-val1
            out-list.book-val = tt-val2.
    END. 
 
    IF from-lager NE to-lager THEN 
    DO: 
        CREATE out-list.
        CREATE out-list.
        ASSIGN
            out-list.flag = 2
            out-list.refno = "GRAND TOTAL"
            out-list.qty = tot-anz
            out-list.init-val = tot-val
            out-list.depn-val = tot-val1
            out-list.book-val = tot-val2.
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

    ASSIGN
        tot-anz     = 0
        tot-val     = 0 
        tot-val1    = 0 
        tot-val2    = 0 
        max-lager   = to-lager.

    /* Change this logic because make range filter not woking correctly by Oscar (26 Agustus 2024) - B3BA7B */
    /* IF from-lager NE to-lager AND (maxNr - 1) = to-lager THEN max-lager = maxNr. */
    FOR EACH lagerBuff WHERE lagerBuff.lager-nr GE from-lager 
    AND lagerBuff.lager-nr LE to-lager: 

        CREATE out-list.
        ASSIGN
            out-list.bezeich = STRING(lagerBuff.lager-nr, ">>99") + "-" + lagerBuff.bezeich
            i = 0
            zwkum = 0 
            t-anz = 0 
            t-val = 0 
            t-val1 = 0 
            t-val2 = 0 
            tt-anz = 0 
            tt-val = 0 
            tt-val1 = 0 
            tt-val2 = 0.

        /*ITA 110315*/
        IF mi-bookvalue-chk = YES THEN DO:
            FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich 
            AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
            FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0  NO-LOCK, 
            /* FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.nr NO-LOCK, */ 
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
                            CREATE out-list.
                            ASSIGN
                                out-list.flag = 1
                                out-list.refno = "SUB TOTAL"
                                out-list.qty = t-anz
                                out-list.init-val = t-val
                                out-list.depn-val = t-val1
                                out-list.book-val = t-val2.
                        END. 
                
                        CREATE out-list. 
                        ASSIGN
                        out-list.bezeich = fa-grup.bezeich
                        t-anz      = 0
                        t-val      = 0 
                        t-val1     = 0 
                        t-val2     = 0 
                        zwkum      = fa-artikel.gnr. 
                    END. 
              
                    CREATE out-list.
                    ASSIGN 
                        out-list.flag = 1
                        out-list.refno = mathis.asset
                        out-list.bezeich = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty = fa-artikel.anzahl.

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
              

                    ASSIGN
                        p-depn-wert = val-dep * sub-depn
                        p-book-wert = fa-artikel.warenwert - p-depn-wert
                        i = i + 1
                        t-anz = t-anz + fa-artikel.anzahl
                        t-val = t-val + fa-artikel.warenwert
                        t-val1 = t-val1 + p-depn-wert 
                        t-val2 = t-val2 + p-book-wert 
                        tt-anz = tt-anz + fa-artikel.anzahl 
                        tt-val = tt-val + fa-artikel.warenwert
                        tt-val1 = tt-val1 + p-depn-wert
                        tt-val2 = tt-val2 + p-book-wert 
                        tot-anz = tot-anz + fa-artikel.anzahl
                        tot-val = tot-val + fa-artikel.warenwert
                        tot-val1 = tot-val1 + p-depn-wert 
                        tot-val2 = tot-val2 + p-book-wert
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = p-depn-wert
                        out-list.book-val = p-book-wert. 

                    /* added FIND FIRST because fa-kateg not found by Oscar (26 Agustus 2024) - B3BA7B */
                    FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-kateg THEN
                    DO:
                        ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                    END.
                
                    IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn. 
                    IF fa-artikel.next-depn NE ? THEN  out-list.next-depn = fa-artikel.next-depn.
                    IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                    IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = sub-depn. 
                END.
            END. 
        END. /*END*/
        ELSE DO:
            FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich 
            AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
            FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0  NO-LOCK, 
            /* FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.nr NO-LOCK, */ 
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
                            CREATE out-list.
                            ASSIGN
                                out-list.refno = "SUB TOTAL"
                                out-list.flag = 1
                                out-list.qty = t-anz
                                out-list.init-val = t-val
                                out-list.depn-val = t-val1
                                out-list.book-val = t-val2.
                        END. 
                
                        CREATE out-list. 
                        ASSIGN
                            out-list.bezeich = fa-grup.bezeich
                            t-anz      = 0
                            t-val      = 0 
                            t-val1     = 0 
                            t-val2     = 0 
                            zwkum      = fa-artikel.gnr. 
                    END. 

                    ASSIGN
                        i = i + 1
                        t-anz = t-anz + fa-artikel.anzahl
                        t-val = t-val + fa-artikel.warenwert
                        t-val1 = t-val1 + fa-artikel.depn-wert
                        t-val2 = t-val2 + fa-artikel.book-wert 
                        tt-anz = tt-anz + fa-artikel.anzahl
                        tt-val = tt-val + fa-artikel.warenwert
                        tt-val1 = tt-val1 + fa-artikel.depn-wert
                        tt-val2 = tt-val2 + fa-artikel.book-wert 
                        tot-anz = tot-anz + fa-artikel.anzahl
                        tot-val = tot-val + fa-artikel.warenwert
                        tot-val1 = tot-val1 + fa-artikel.depn-wert
                        tot-val2 = tot-val2 + fa-artikel.book-wert. 
         
                    CREATE out-list.
                    ASSIGN
                        out-list.flag = 1
                        out-list.bezeich = mathis.NAME
                        out-list.refno = mathis.asset
                        out-list.received = mathis.datu
                        out-list.qty = fa-artikel.anzahl
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = fa-artikel.depn-wert
                        out-list.book-val = fa-artikel.book-wert.

                    /* added FIND FIRST because fa-kateg not found by Oscar (26 Agustus 2024) - B3BA7B */
                    FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-kateg THEN
                    DO:
                        ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                    END.

                    IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                    IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                    IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                    IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = fa-artikel.anz-depn.
                END.
            END. 
        END.
 
        CREATE out-list.
        ASSIGN
            out-list.refno  = "SUB TOTAL" 
            out-list.flag   = 1   
            out-list.qty = t-anz
            out-list.init-val = t-val
            out-list.depn-val = t-val1
            out-list.book-val = t-val2.

        CREATE out-list. 
        ASSIGN
            out-list.refno = "T O T A L"
            out-list.flag = 1
            out-list.qty = tt-anz
            out-list.init-val = tt-val
            out-list.depn-val = tt-val1
            out-list.book-val = tt-val2.
    END.

    IF from-lager NE to-lager THEN 
    DO: 
        CREATE out-list. 
        CREATE out-list.
        ASSIGN
            out-list.flag  = 2 
            out-list.refno = "GRAND TOTAL"
            out-list.qty = tot-anz
            out-list.init-val = tot-val
            out-list.depn-val = tot-val1
            out-list.book-val = tot-val2.
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
 
    ASSIGN
        tot-anz = 0
        tot-val = 0 
        tot-val1 = 0 
        tot-val2 = 0. 
 
    FIND FIRST fa-grup WHERE fa-grup.gnr = from-grp AND fa-grup.flag = 0 NO-LOCK. 
    FOR EACH lagerBuff WHERE lagerBuff.lager-nr GE from-lager 
    AND lagerBuff.lager-nr LE to-lager: 
    
        CREATE out-list.
        ASSIGN
            out-list.bezeich = STRING(lagerBuff.lager-nr, ">>99") + "-" + lagerBuff.bezeich. 
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
    
        /*ITA 110315*/
        IF mi-bookvalue-chk = YES THEN DO:
            FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich
            AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
            FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0 AND fa-artikel.gnr = from-grp NO-LOCK
            /* FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.nr NO-LOCK */
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
                            CREATE out-list.
                            ASSIGN
                                out-list.refno  = "SUB TOTAL" 
                                out-list.flag   = 1   
                                out-list.qty = t-anz
                                out-list.init-val = t-val
                                out-list.depn-val = t-val1
                                out-list.book-val = t-val2.
                        END. 

                        CREATE out-list. 
                        ASSIGN
                        out-list.bezeich = fa-grup.bezeich
                        t-anz      = 0
                        t-val      = 0 
                        t-val1     = 0 
                        t-val2     = 0 
                        zwkum = fa-artikel.gnr. 
                    END. 
              
                    CREATE out-list. 
                    ASSIGN
                        out-list.refno = mathis.asset
                        out-list.flag = 1
                        out-list.bezeich = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty = fa-artikel.anzahl
                        val-dep     = fa-artikel.depn-wert / fa-artikel.anz-depn
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
              
                    ASSIGN 
                        p-depn-wert = val-dep * sub-depn
                        p-book-wert = fa-artikel.warenwert - p-depn-wert
                        i = i + 1
                        t-anz = t-anz + fa-artikel.anzahl
                        t-val = t-val + fa-artikel.warenwert 
                        t-val1 = t-val1 + p-depn-wert 
                        t-val2 = t-val2 + p-book-wert 
                        tt-anz = tt-anz + fa-artikel.anzahl 
                        tt-val = tt-val + fa-artikel.warenwert 
                        tt-val1 = tt-val1 + p-depn-wert 
                        tt-val2 = tt-val2 + p-book-wert 
                        tot-anz = tot-anz + fa-artikel.anzahl
                        tot-val = tot-val + fa-artikel.warenwert
                        tot-val1 = tot-val1 + p-depn-wert 
                        tot-val2 = tot-val2 + p-book-wert
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = p-depn-wert
                        out-list.book-val = p-book-wert.

                    /* added FIND FIRST because fa-kateg not found by Oscar (26 Agustus 2024) - B3BA7B */
                    FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-kateg THEN
                    DO:
                        ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                    END.

                    IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                    IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                    IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                    IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = sub-depn. 
                END. 

                /* CREATE out-list.
                ASSIGN
                    out-list.refno  = "SUB TOTAL" 
                    out-list.flag   = 1  
                    out-list.qty = t-anz
                    out-list.init-val = t-val
                    out-list.depn-val = t-val1
                    out-list.book-val = t-val2.

                CREATE out-list.
                ASSIGN
                    out-list.refno = "T O T A L"
                    out-list.flag = 1
                    out-list.qty = tt-anz
                    out-list.init-val = tt-val
                    out-list.depn-val = tt-val1
                    out-list.book-val = tt-val2. */
            END.
        END. /*END*/
        ELSE DO:
            FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich
            AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
            FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0 AND fa-artikel.gnr = from-grp NO-LOCK
            /* FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.nr NO-LOCK */ 
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
                            CREATE out-list.
                            ASSIGN
                                out-list.refno  = "SUB TOTAL" 
                                out-list.flag   = 1  
                                out-list.qty = t-anz
                                out-list.init-val = t-val
                                out-list.depn-val = t-val1
                                out-list.book-val = t-val2.
                        END. 
                
                        CREATE out-list. 
                        ASSIGN
                        out-list.bezeich = fa-grup.bezeich
                        t-anz      = 0
                        t-val      = 0 
                        t-val1     = 0 
                        t-val2     = 0 
                        zwkum = fa-artikel.gnr. 
                    END.

                    ASSIGN
                        i = i + 1
                        t-anz = t-anz + fa-artikel.anzahl
                        t-val = t-val + fa-artikel.warenwert
                        t-val1 = t-val1 + fa-artikel.depn-wert 
                        t-val2 = t-val2 + fa-artikel.book-wert 
                        tt-anz = tt-anz + fa-artikel.anzahl 
                        tt-val = tt-val + fa-artikel.warenwert 
                        tt-val1 = tt-val1 + fa-artikel.depn-wert 
                        tt-val2 = tt-val2 + fa-artikel.book-wert 
                        tot-anz = tot-anz + fa-artikel.anzahl 
                        tot-val = tot-val + fa-artikel.warenwert 
                        tot-val1 = tot-val1 + fa-artikel.depn-wert 
                        tot-val2 = tot-val2 + fa-artikel.book-wert. 
         
                    CREATE out-list. 
                    ASSIGN
                        out-list.flag = 1
                        out-list.refno = mathis.asset
                        out-list.bezeich = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty = fa-artikel.anzahl
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = fa-artikel.depn-wert
                        out-list.book-val = fa-artikel.book-wert.

                    /* added FIND FIRST because fa-kateg not found by Oscar (26 Agustus 2024) - B3BA7B */
                    FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-kateg THEN
                    DO:
                        ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                    END.

                    IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                    IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                    IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                    IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = anz-depn.
                END. 
            
                /* CREATE out-list. 
                ASSIGN
                    out-list.refno  = "SUB TOTAL" 
                    out-list.flag   = 1  
                    out-list.qty = t-anz
                    out-list.init-val = t-val
                    out-list.depn-val = t-val1
                    out-list.book-val = t-val2.

                IF i GT 0 THEN 
                DO: 
                    CREATE out-list. 
                    ASSIGN
                        out-list.refno = "T O T A L"
                        out-list.flag = 1
                        out-list.qty = tt-anz
                        out-list.init-val = tt-val
                        out-list.depn-val = tt-val1
                        out-list.book-val = tt-val2.
                END. */
            END.
        END.

        CREATE out-list. 
                ASSIGN
                    out-list.refno  = "SUB TOTAL" 
                    out-list.flag   = 1  
                    out-list.qty = t-anz
                    out-list.init-val = t-val
                    out-list.depn-val = t-val1
                    out-list.book-val = t-val2.

        CREATE out-list. 
        ASSIGN
            out-list.refno = "T O T A L"
            out-list.flag = 1
            out-list.qty = tt-anz
            out-list.init-val = tt-val
            out-list.depn-val = tt-val1
            out-list.book-val = tt-val2.
    END. 
 
    IF from-lager NE to-lager AND tot-anz NE 0 THEN 
    DO: 
        CREATE out-list. 
        CREATE out-list. 
        ASSIGN
            out-list.flag  = 2 
            out-list.refno = "GRAND TOTAL"
            out-list.qty = tot-anz
            out-list.init-val = tot-val
            out-list.depn-val = tot-val1
            out-list.book-val = tot-val2.
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
 
    ASSIGN
        tot-anz = 0
        tot-val = 0
        tot-val1 = 0
        tot-val2 = 0. 
 
    FIND FIRST fa-grup WHERE fa-grup.gnr = from-grp AND fa-grup.flag = 0 NO-LOCK. 
    FOR EACH lagerBuff WHERE lagerBuff.lager-nr GE from-lager 
    AND lagerBuff.lager-nr LE to-lager: 
    
        ASSIGN 
            i = 0
            zwkum = 0 
            t-anz = 0 
            t-val = 0 
            t-val1 = 0 
            t-val2 = 0 
            tt-anz = 0 
            tt-val = 0 
            tt-val1 = 0 
            tt-val2 = 0. 
    
        CREATE out-list. 
        ASSIGN
            out-list.bezeich = STRING(lagerBuff.lager-nr, ">>99") + "-" + lagerBuff.bezeich.

        /*ITA 110315*/
        IF mi-bookvalue-chk = YES THEN DO:
            FOR EACH mathis WHERE mathis.location = lagerBuff.bezeich 
            AND mathis.datum GE from-date AND mathis.datum LE to-date NO-LOCK, 
            FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0 AND fa-artikel.gnr = from-grp NO-LOCK
            /* FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.nr NO-LOCK */ 
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
                            CREATE out-list. 
                            ASSIGN
                                out-list.refno  = "SUB TOTAL" 
                                out-list.flag   = 1  
                                out-list.qty = t-anz
                                out-list.init-val = t-val
                                out-list.depn-val = t-val1
                                out-list.book-val = t-val2.
                        END. 

                        CREATE out-list. 
                        ASSIGN
                            out-list.bezeich = fa-grup.bezeich
                            t-anz    = 0
                            t-val    = 0 
                            t-val1   = 0 
                            t-val2   = 0 
                            zwkum    = fa-artikel.gnr. 
                    END. 
              
                    CREATE out-list. 
                    ASSIGN
                        out-list.flag = 1
                        out-list.refno = mathis.asset
                        out-list.bezeich = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty = fa-artikel.anzahl
                        val-dep     = fa-artikel.depn-wert / fa-artikel.anz-depn
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

                    ASSIGN 
                        p-depn-wert = val-dep * sub-depn
                        p-book-wert = fa-artikel.warenwert - p-depn-wert
                        i = i + 1
                        t-anz = t-anz + fa-artikel.anzahl
                        t-val = t-val + fa-artikel.warenwert 
                        t-val1 = t-val1 + p-depn-wert 
                        t-val2 = t-val2 + p-book-wert 
                        tt-anz = tt-anz + fa-artikel.anzahl 
                        tt-val = tt-val + fa-artikel.warenwert 
                        tt-val1 = tt-val1 + p-depn-wert 
                        tt-val2 = tt-val2 + p-book-wert 
                        tot-anz = tot-anz + fa-artikel.anzahl 
                        tot-val = tot-val + fa-artikel.warenwert 
                        tot-val1 = tot-val1 + p-depn-wert
                        tot-val2 = tot-val2 + p-book-wert
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = p-depn-wert
                        out-list.book-val = p-book-wert.

                    /* added FIND FIRST because fa-kateg not found by Oscar (26 Agustus 2024) - B3BA7B */
                    FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-kateg THEN
                    DO:
                        ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                    END.

                    IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                    IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn. 
                    IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                    IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = sub-depn.
                END. 

                /* CREATE out-list. 
                ASSIGN
                    out-list.refno  = "SUB TOTAL" 
                    out-list.flag   = 1   
                    out-list.qty = t-anz
                    out-list.init-val = t-val
                    out-list.depn-val = t-val1
                    out-list.book-val = t-val2.

                CREATE out-list. 
                ASSIGN
                    out-list.refno = "T O T A L"
                    out-list.flag = 1
                    out-list.qty = tt-anz
                    out-list.init-val = tt-val
                    out-list.depn-val = tt-val1
                    out-list.book-val = tt-val2. */
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
                        CREATE out-list. 
                        ASSIGN
                            out-list.refno  = "SUB TOTAL" 
                            out-list.flag   = 1  
                            out-list.qty = t-anz
                            out-list.init-val = t-val
                            out-list.depn-val = t-val1
                            out-list.book-val = t-val2.
                        END. 

                        CREATE out-list. 
                        ASSIGN
                        out-list.bezeich = fa-grup.bezeich
                        t-anz    = 0
                        t-val    = 0 
                        t-val1   = 0 
                        t-val2   = 0 
                        zwkum    = fa-artikel.gnr. 
                    END.
                    ASSIGN
                        i = i + 1
                        t-anz = t-anz + fa-artikel.anzahl
                        t-val = t-val + fa-artikel.warenwert
                        t-val1 = t-val1 + fa-artikel.depn-wert
                        t-val2 = t-val2 + fa-artikel.book-wert 
                        tt-anz = tt-anz + fa-artikel.anzahl 
                        tt-val = tt-val + fa-artikel.warenwert
                        tt-val1 = tt-val1 + fa-artikel.depn-wert 
                        tt-val2 = tt-val2 + fa-artikel.book-wert 
                        tot-anz = tot-anz + fa-artikel.anzahl 
                        tot-val = tot-val + fa-artikel.warenwert
                        tot-val1 = tot-val1 + fa-artikel.depn-wert
                        tot-val2 = tot-val2 + fa-artikel.book-wert. 
         
                        CREATE out-list. 
                        ASSIGN
                            out-list.flag = 1
                            out-list.refno = mathis.asset
                            out-list.bezeich = mathis.NAME
                            out-list.received = mathis.datum
                            out-list.qty = fa-artikel.anzahl
                            out-list.init-val = fa-artikel.warenwert
                            out-list.depn-val = fa-artikel.depn-wert
                            out-list.book-val = fa-artikel.book-wert.

                        /* added FIND FIRST because fa-kateg not found by Oscar (26 Agustus 2024) - B3BA7B */
                        FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                        IF AVAILABLE fa-kateg THEN
                        DO:
                            ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                        END.

                        IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                        IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                        IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                        IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = fa-artikel.anz-depn.
                END.
                
                /* CREATE out-list. 
                ASSIGN
                    out-list.refno  = "SUB TOTAL" 
                    out-list.flag   = 1  
                    out-list.qty = t-anz
                    out-list.init-val = t-val
                    out-list.depn-val = t-val1
                    out-list.book-val = t-val2.
                    
                CREATE out-list. 
                ASSIGN
                    out-list.refno = "T O T A L"
                    out-list.flag = 1
                    out-list.qty = tt-anz
                    out-list.init-val = tt-val
                    out-list.depn-val = tt-val1
                    out-list.book-val = tt-val2. */
            END.
        END.

        CREATE out-list. 
        ASSIGN
            out-list.refno  = "SUB TOTAL" 
            out-list.flag   = 1  
            out-list.qty = t-anz
            out-list.init-val = t-val
            out-list.depn-val = t-val1
            out-list.book-val = t-val2.
                    
        CREATE out-list. 
        ASSIGN
            out-list.refno = "T O T A L"
            out-list.flag = 1
            out-list.qty = tt-anz
            out-list.init-val = tt-val
            out-list.depn-val = tt-val1
            out-list.book-val = tt-val2.
    END. 
 
    IF from-lager NE to-lager THEN 
    DO: 
        CREATE out-list. 
        CREATE out-list. 
        ASSIGN
            out-list.flag  = 2 
            out-list.refno = "GRAND TOTAL"
            out-list.qty = tot-anz
            out-list.init-val = tot-val
            out-list.depn-val = tot-val1
            out-list.book-val = tot-val2.
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
 
    ASSIGN
        diff-n = (YEAR(last-acctdate) - yy) * 12 +  MONTH(last-acctdate) - mm
        tot-anz = 0
        tot-val = 0 
        tot-val1 = 0 
        tot-val2 = 0. 
 
    DO:
        ASSIGN
            i = 0
            zwkum = 0
            t-anz = 0 
            t-val = 0 
            t-val1 = 0 
            t-val2 = 0. 
    
        /*ITA 110315*/
        IF mi-bookvalue-chk = YES THEN DO:
            FOR EACH mathis WHERE mathis.datum GE from-date
            AND mathis.datum LE to-date NO-LOCK, 
            FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0
            /*AND fa-artikel.loeschflag = 0 AND (fa-artikel.anz-depn - diff-n) GE 0 */
            NO-LOCK, 
            /* FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.nr NO-LOCK,  */ 
            FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp 
            AND fa-grup.flag = 1 
            AND fa-grup.gnr GE from-subgr
            AND fa-grup.gnr LE to-subgr NO-LOCK BY fa-artikel.subgrp BY mathis.name:

                /*IF mathis.datum GT 08/31/10 THEN DISP mathis.datum.*/

                /* adding this code so filter "Full Depreciation Only" work by Oscar (27 Agustus 2024) - B3BA7B */
                do-it = NO.
                IF NOT zero-value-only THEN do-it = YES.
                ELSE do-it = fa-artikel.book-wert EQ 0.
                
                IF do-it THEN 
                DO:
                    IF zwkum NE fa-artikel.subgrp THEN 
                    DO: 
                        IF zwkum NE 0 THEN 
                        DO: 
                            CREATE out-list. 
                            ASSIGN
                                out-list.refno  = "SUB TOTAL" 
                                out-list.flag   = 1
                                out-list.qty = t-anz
                                out-list.init-val = t-val
                                out-list.depn-val = t-val1
                                out-list.book-val = t-val2.
                        END. 
                        CREATE out-list. 
                        ASSIGN
                            out-list.bezeich = fa-grup.bezeich
                            t-anz      = 0
                            t-val      = 0 
                            t-val1     = 0 
                            t-val2     = 0 
                            zwkum      = fa-artikel.subgrp. 
                    END. 

                    CREATE out-list. 
                    ASSIGN
                        out-list.flag = 1
                        out-list.refno = mathis.asset 
                        out-list.location = trim(mathis.location )
                        out-list.bezeich = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty = fa-artikel.anzahl
                        out-list.init-val = fa-artikel.warenwert
                        val-dep     = fa-artikel.depn-wert / fa-artikel.anz-depn
                        sub-depn    = 0
                        flag        = NO.
                    IF val-dep = ? THEN val-dep = 0.

                    DO datum = from-date TO to-date:
                        IF flag AND datum = DATE(MONTH(datum) + 1, 1, YEAR(datum)) - 1 THEN 
                            ASSIGN sub-depn = sub-depn + 1.
                        
                        IF datum = fa-artikel.first-depn THEN 
                            ASSIGN sub-depn    = sub-depn + 1
                                    flag       = YES.

                        IF datum = fa-artikel.last-depn THEN LEAVE.
                    END.


                    ASSIGN 
                        p-depn-wert = val-dep * sub-depn
                        p-book-wert = fa-artikel.warenwert - p-depn-wert
                        i = i + 1
                        t-anz = t-anz + fa-artikel.anzahl
                        t-val = t-val + fa-artikel.warenwert
                        tot-anz = tot-anz + fa-artikel.anzahl 
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
                        ASSIGN
                        out-list.depn-val = 0
                        out-list.book-val = fa-artikel.warenwert.
                    END. 
                    ELSE 
                    DO: 
                        ASSIGN
                        out-list.depn-val = p-depn-wert - diff-wert
                        out-list.book-val = p-book-wert + diff-wert.
                    END. 
                
                    /* added FIND FIRST because fa-kateg not found by Oscar (26 Agustus 2024) - B3BA7B */
                    FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-kateg THEN
                    DO:
                        ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                    END.
                
                    IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                    IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                    IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                    IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = sub-depn.
                END.
            END. 

            CREATE out-list. 
            ASSIGN
                out-list.refno  = "SUB TOTAL" 
                out-list.flag   = 1
                out-list.qty = t-anz
                out-list.init-val = t-val
                out-list.depn-val = t-val1
                out-list.book-val = t-val2.
                
        END. /*end*/
        ELSE DO:
            FOR EACH mathis WHERE mathis.datum GE from-date
            AND mathis.datum LE to-date NO-LOCK, 
            FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0
            /*AND fa-artikel.loeschflag = 0 AND (fa-artikel.anz-depn - diff-n) GE 0 */
            NO-LOCK, 
            /* FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.nr NO-LOCK, */
            FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp 
            AND fa-grup.flag = 1 
            AND fa-grup.gnr GE from-subgr
            AND fa-grup.gnr LE to-subgr NO-LOCK BY fa-artikel.subgrp BY mathis.name: 

                /*IF mathis.datum GT 08/31/10 THEN DISP mathis.datum.*/
            
                /* adding this code so filter "Full Depreciation Only" work by Oscar (27 Agustus 2024) - B3BA7B */
                do-it = NO.
                IF NOT zero-value-only THEN do-it = YES.
                ELSE do-it = fa-artikel.book-wert EQ 0.
                
                IF do-it THEN 
                DO:
                    IF zwkum NE fa-artikel.subgrp THEN 
                    DO: 
                        IF zwkum NE 0 THEN 
                        DO: 
                            CREATE out-list. 
                            ASSIGN
                                out-list.refno  = "SUB TOTAL" 
                                out-list.flag   = 1
                                out-list.qty = t-anz
                                out-list.init-val = t-val
                                out-list.depn-val = t-val1
                                out-list.book-val = t-val2.
                        END. 
                        CREATE out-list. 
                        ASSIGN
                            out-list.bezeich = fa-grup.bezeich
                            t-anz      = 0
                            t-val      = 0 
                            t-val1     = 0 
                            t-val2     = 0 
                            zwkum      = fa-artikel.subgrp. 
                    END.
                    ASSIGN
                        i = i + 1
                        t-anz = t-anz + fa-artikel.anzahl
                        t-val = t-val + fa-artikel.warenwert
                        tot-anz = tot-anz + fa-artikel.anzahl 
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
                
                    CREATE out-list. 
                    ASSIGN
                        out-list.flag = 1
                        out-list.refno = mathis.asset 
                        out-list.location = trim(mathis.location)
                        out-list.bezeich = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty = fa-artikel.anzahl
                        out-list.init-val = fa-artikel.warenwert.
            
                    IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
                    DO:
                        ASSIGN
                        out-list.depn-val = 0
                        out-list.book-val = fa-artikel.warenwert.
                    END. 
                    ELSE 
                    DO:
                        ASSIGN
                        out-list.depn-val = fa-artikel.depn-wert - diff-wert
                        out-list.book-val = fa-artikel.book-wert + diff-wert.
                    END. 
                    
                    /* added FIND FIRST because fa-kateg not found by Oscar (26 Agustus 2024) - B3BA7B */
                    FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-kateg THEN
                    DO:
                        ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                    END.

                    IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                    IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                    IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                    IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = fa-artikel.anz-depn.
                END.
            END.

            CREATE out-list. 
            ASSIGN
                out-list.refno  = "SUB TOTAL" 
                out-list.flag   = 1
                out-list.qty = t-anz
                out-list.init-val = t-val
                out-list.depn-val = t-val1
                out-list.book-val = t-val2.
        END.
    END. 
 
    IF tot-anz NE 0 THEN 
    DO: 
        CREATE out-list. 
        CREATE out-list. 
        ASSIGN
        out-list.flag  = 2 
        out-list.refno = "TOTAL"
        out-list.qty = tot-anz
        out-list.init-val = tot-val
        out-list.depn-val = tot-val1
        out-list.book-val = tot-val2.
    END. 
END. 

PROCEDURE create-listsgrp1:  /* all FA-Group */ 
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
 
    ASSIGN
        diff-n = (YEAR(last-acctdate) - yy) * 12 +  MONTH(last-acctdate) - mm
        tot-anz = 0
        tot-val = 0 
        tot-val1 = 0 
        tot-val2 = 0. 
 
    DO:
        ASSIGN
            i = 0
            zwkum = 0
            t-anz = 0 
            t-val = 0 
            t-val1 = 0 
            t-val2 = 0. 
    
        /*ITA 110315*/
        IF mi-bookvalue-chk = YES THEN DO:
            FOR EACH mathis WHERE mathis.datum GE from-date
            AND mathis.datum LE to-date NO-LOCK, 
            FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0 AND fa-artikel.gnr = from-grp
            /*AND fa-artikel.loeschflag = 0 AND (fa-artikel.anz-depn - diff-n) GE 0 */
            NO-LOCK, 
            /* FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.nr NO-LOCK,  */ 
            FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp 
            AND fa-grup.flag = 1 
            AND fa-grup.gnr GE from-subgr
            AND fa-grup.gnr LE to-subgr NO-LOCK BY fa-artikel.subgrp BY mathis.name: 

                /*IF mathis.datum GT 08/31/10 THEN DISP mathis.datum.*/

                /* adding this code so filter "Full Depreciation Only" work by Oscar (27 Agustus 2024) - B3BA7B */
                do-it = NO.
                IF NOT zero-value-only THEN do-it = YES.
                ELSE do-it = fa-artikel.book-wert EQ 0.
                
                IF do-it THEN 
                DO:
                    IF zwkum NE fa-artikel.subgrp THEN 
                    DO: 
                        IF zwkum NE 0 THEN 
                        DO: 
                            CREATE out-list. 
                            ASSIGN
                                out-list.refno  = "SUB TOTAL" 
                                out-list.flag   = 1
                                out-list.qty = t-anz
                                out-list.init-val = t-val
                                out-list.depn-val = t-val1
                                out-list.book-val = t-val2.
                        END. 
                        CREATE out-list. 
                        ASSIGN
                            out-list.bezeich = fa-grup.bezeich
                            t-anz      = 0
                            t-val      = 0 
                            t-val1     = 0 
                            t-val2     = 0 
                            zwkum      = fa-artikel.subgrp. 
                    END. 

                    CREATE out-list. 
                    ASSIGN
                        out-list.flag = 1
                        out-list.refno = mathis.asset 
                        out-list.location = trim(mathis.location )
                        out-list.bezeich = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty = fa-artikel.anzahl
                        out-list.init-val = fa-artikel.warenwert
                        val-dep     = fa-artikel.depn-wert / fa-artikel.anz-depn
                        sub-depn    = 0
                        flag        = NO.
                    IF val-dep = ? THEN val-dep = 0.

                    DO datum = from-date TO to-date:
                        IF flag AND datum = DATE(MONTH(datum) + 1, 1, YEAR(datum)) - 1 THEN 
                            ASSIGN sub-depn = sub-depn + 1.
                        
                        IF datum = fa-artikel.first-depn THEN 
                            ASSIGN sub-depn    = sub-depn + 1
                                    flag       = YES.

                        IF datum = fa-artikel.last-depn THEN LEAVE.
                    END.


                    ASSIGN 
                        p-depn-wert = val-dep * sub-depn
                        p-book-wert = fa-artikel.warenwert - p-depn-wert
                        i = i + 1
                        t-anz = t-anz + fa-artikel.anzahl
                        t-val = t-val + fa-artikel.warenwert
                        tot-anz = tot-anz + fa-artikel.anzahl 
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
                        ASSIGN
                        out-list.depn-val = 0
                        out-list.book-val = fa-artikel.warenwert.
                    END. 
                    ELSE 
                    DO: 
                        ASSIGN
                        out-list.depn-val = p-depn-wert - diff-wert
                        out-list.book-val = p-book-wert + diff-wert.
                    END. 
                
                    /* added FIND FIRST because fa-kateg not found by Oscar (26 Agustus 2024) - B3BA7B */
                    FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-kateg THEN
                    DO:
                        ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                    END.
                
                    IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                    IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                    IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                    IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = sub-depn.
                END.
            END. 

            CREATE out-list. 
            ASSIGN
                out-list.refno  = "SUB TOTAL" 
                out-list.flag   = 1
                out-list.qty = t-anz
                out-list.init-val = t-val
                out-list.depn-val = t-val1
                out-list.book-val = t-val2.
                
        END. /*end*/
        ELSE DO:
            FOR EACH mathis WHERE mathis.datum GE from-date
            AND mathis.datum LE to-date NO-LOCK, 
            FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
            AND fa-artikel.loeschflag = 0 AND fa-artikel.gnr = from-grp
            /*AND fa-artikel.loeschflag = 0 AND (fa-artikel.anz-depn - diff-n) GE 0 */
            NO-LOCK, 
            /* FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.nr NO-LOCK, */
            FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp 
            AND fa-grup.flag = 1 
            AND fa-grup.gnr GE from-subgr
            AND fa-grup.gnr LE to-subgr NO-LOCK BY fa-artikel.subgrp BY mathis.name:
        
                /*IF mathis.datum GT 08/31/10 THEN DISP mathis.datum.*/

                /* adding this code so filter "Full Depreciation Only" work by Oscar (27 Agustus 2024) - B3BA7B */
                do-it = NO.
                IF NOT zero-value-only THEN do-it = YES.
                ELSE do-it = fa-artikel.book-wert EQ 0.
                
                IF do-it THEN 
                DO:
                    IF zwkum NE fa-artikel.subgrp THEN 
                    DO: 
                        IF zwkum NE 0 THEN 
                        DO: 
                            CREATE out-list. 
                            ASSIGN
                                out-list.refno  = "SUB TOTAL" 
                                out-list.flag   = 1
                                out-list.qty = t-anz
                                out-list.init-val = t-val
                                out-list.depn-val = t-val1
                                out-list.book-val = t-val2.
                        END. 
                        CREATE out-list. 
                        ASSIGN
                            out-list.bezeich = fa-grup.bezeich
                            t-anz      = 0
                            t-val      = 0 
                            t-val1     = 0 
                            t-val2     = 0 
                            zwkum      = fa-artikel.subgrp. 
                    END.
                    ASSIGN
                        i = i + 1
                        t-anz = t-anz + fa-artikel.anzahl
                        t-val = t-val + fa-artikel.warenwert
                        tot-anz = tot-anz + fa-artikel.anzahl 
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
                
                    CREATE out-list. 
                    ASSIGN
                        out-list.flag = 1
                        out-list.refno = mathis.asset 
                        out-list.location = trim(mathis.location)
                        out-list.bezeich = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty = fa-artikel.anzahl
                        out-list.init-val = fa-artikel.warenwert.
            
                    IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
                    DO:
                        ASSIGN
                        out-list.depn-val = 0
                        out-list.book-val = fa-artikel.warenwert.
                    END. 
                    ELSE 
                    DO:
                        ASSIGN
                        out-list.depn-val = fa-artikel.depn-wert - diff-wert
                        out-list.book-val = fa-artikel.book-wert + diff-wert.
                    END. 
                    
                    /* added FIND FIRST because fa-kateg not found by Oscar (26 Agustus 2024) - B3BA7B */
                    FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-kateg THEN
                    DO:
                        ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                    END.

                    IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                    IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                    IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                    IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = fa-artikel.anz-depn.
                END.
            END.

            CREATE out-list. 
            ASSIGN
                out-list.refno  = "SUB TOTAL" 
                out-list.flag   = 1
                out-list.qty = t-anz
                out-list.init-val = t-val
                out-list.depn-val = t-val1
                out-list.book-val = t-val2.
        END.
    END. 
 
    IF tot-anz NE 0 THEN 
    DO: 
        CREATE out-list. 
        CREATE out-list. 
        ASSIGN
        out-list.flag  = 2 
        out-list.refno = "TOTAL"
        out-list.qty = tot-anz
        out-list.init-val = tot-val
        out-list.depn-val = tot-val1
        out-list.book-val = tot-val2.
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
 
  	diff-n = (YEAR(last-acctdate) - yy) * 12 +  MONTH(last-acctdate) - mm. 

	/*ITA 110315*/
	IF mi-bookvalue-chk = YES THEN DO:
		FOR EACH mathis WHERE mathis.datum GE from-date
		AND mathis.datum LE to-date NO-LOCK, 
		FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
		AND fa-artikel.loeschflag = 0
		/*AND fa-artikel.loeschflag = 0 AND (fa-artikel.anz-depn - diff-n) GE 0 */
		NO-LOCK BY fa-artikel.fibukonto: 

            /* adding this code so filter "Full Depreciation Only" work by Oscar (27 Agustus 2024) - B3BA7B */
            do-it = NO.
            IF NOT zero-value-only THEN do-it = YES.
            ELSE do-it = fa-artikel.book-wert EQ 0.
            
            IF do-it THEN 
            DO:
                /*IF curr-acct = "" THEN curr-acct = fa-artikel.fibukonto.*/
                IF curr-acct NE fa-artikel.fibukonto /* AND curr-acct NE "" disable this by Oscar (27 Agustus 2024) - B3BA7B */ THEN 
                DO: 
                    ASSIGN 
                        tot-anz  = tot-anz + t-anz
                        tot-oh   = tot-oh + t-oh
                        tot-depn = tot-depn + t-depn
                        tot-book = tot-book + t-book.
                
                    FIND FIRST gl-acct WHERE gl-acct.fibukonto = curr-acct NO-LOCK NO-ERROR. 
                    IF AVAILABLE gl-acct THEN RUN convert-fibu(curr-acct, OUTPUT fibu). 
            
                    IF curr-acct NE "" THEN DO:
                        CREATE out-list. 
                        ASSIGN
                            out-list.location  = ""
                            out-list.bezeich   = "SUBTOTAL"
                            out-list.qty 	   = t-anz
                            out-list.init-val  = t-oh
                            out-list.depn-val  = t-depn
                            out-list.book-val  = t-book.
                        CREATE out-list.
                    END.
        
                    ASSIGN
                        curr-acct = fa-artikel.fibukonto
                        t-anz     = 0
                        t-oh      = 0 
                        t-depn    = 0
                        t-book    = 0. 
                END.
            
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-artikel.fibukonto NO-LOCK NO-ERROR. 
                RUN convert-fibu(fa-artikel.fibukonto, OUTPUT fibu). 

                FIND FIRST out-list WHERE out-list.fibu = fibu NO-ERROR.
                IF AVAILABLE out-list THEN DO:
                    CREATE out-list. 
                    ASSIGN
                        out-list.flag 		= 1
                        out-list.refno    	= mathis.asset 
                        out-list.location 	= mathis.location
                        out-list.bezeich 	= mathis.NAME
                        out-list.received 	= mathis.datum
                        out-list.qty 		= fa-artikel.anzahl.
                END.
                ELSE DO:
                    CREATE out-list. 
                    ASSIGN 
                        out-list.flag 		= 1
                        out-list.refno    	= mathis.asset 
                        out-list.location 	= trim(mathis.location)
                        out-list.fibu 		= fibu
                        out-list.bezeich	= mathis.NAME
                        out-list.received 	= mathis.datum
                        out-list.qty 		= fa-artikel.anzahl.
                END.

                ASSIGN 
                    val-dep     = fa-artikel.depn-wert / fa-artikel.anz-depn
                    sub-depn    = 0
                    flag        = NO.

                IF val-dep = ? THEN val-dep = 0.
                DO datum = from-date TO to-date:
                    IF flag AND datum = DATE(MONTH(datum) + 1, 1, YEAR(datum)) - 1 THEN 
                            ASSIGN sub-depn = sub-depn + 1.
            
                    IF datum = fa-artikel.first-depn THEN 
                        ASSIGN 
                            sub-depn    = sub-depn + 1
                            flag        = YES.

                    IF datum = fa-artikel.last-depn THEN LEAVE.
                END.

                ASSIGN 
                    p-depn-wert = val-dep * sub-depn
                    p-book-wert = fa-artikel.warenwert - p-depn-wert.
        
                /*ITA 160214*/    
                IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
                DO: 
                    ASSIGN
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = 0
                        out-list.book-val = fa-artikel.warenwert.
                END. 
                ELSE 
                DO:
                    ASSIGN
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = p-depn-wert - diff-wert
                        out-list.book-val = p-book-wert + diff-wert.
                END. 
            
                /* added FIND FIRST because fa-kateg not found by Oscar (22 Agustus 2024) - 0D6718 */
                FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                IF AVAILABLE fa-kateg THEN
                DO:
                    ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                END.

                IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = sub-depn.
                
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
      	END.
  	END. /*end*/

  	ELSE DO:
      	FOR EACH mathis WHERE mathis.datum GE from-date
        AND mathis.datum LE to-date NO-LOCK, 
       	FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
		AND fa-artikel.loeschflag = 0
        /*AND fa-artikel.loeschflag = 0 AND (fa-artikel.anz-depn - diff-n) GE 0 */
        NO-LOCK BY fa-artikel.fibukonto: 

            /* adding this code so filter "Full Depreciation Only" work by Oscar (27 Agustus 2024) - B3BA7B */
            do-it = NO.
            IF NOT zero-value-only THEN do-it = YES.
            ELSE do-it = fa-artikel.book-wert EQ 0.
            
            IF do-it THEN 
            DO:
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
                    
                        CREATE out-list.
                        ASSIGN
                            out-list.location  = ""
                            out-list.bezeich = "SUBTOTAL"
                            out-list.qty = t-anz
                            out-list.init-val = t-oh
                            out-list.depn-val = t-depn
                            out-list.book-val = t-book.
            
                        CREATE out-list.
                    END.
            
                    ASSIGN
                        curr-acct = fa-artikel.fibukonto
                        t-anz     = 0
                        t-oh      = 0 
                        t-depn    = 0
                        t-book    = 0. 
                END.
        
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-artikel.fibukonto NO-LOCK NO-ERROR. 
                RUN convert-fibu(fa-artikel.fibukonto, OUTPUT fibu). 
            
                FIND FIRST out-list WHERE out-list.fibu = fibu NO-ERROR.
                IF AVAILABLE out-list THEN 
                DO:
                    CREATE out-list. 
                    ASSIGN 
                        out-list.refno    = mathis.asset 
                        out-list.location = trim(mathis.location)
                        out-list.bezeich  = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty 	  = fa-artikel.anzahl.
        
                END.
                ELSE 
                DO:
                    CREATE out-list. 
                    ASSIGN 
                        out-list.refno    = mathis.asset 
                        out-list.location = trim(mathis.location) 
                        out-list.bezeich  = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty 	  = fa-artikel.anzahl
                        out-list.fibu     = fibu.
                END.
        
                /*ITA 160214*/    
                IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
                DO: 
                    ASSIGN
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = 0 
                        out-list.book-val = fa-artikel.warenwert.
                END. 
                ELSE 
                DO: 
                    ASSIGN
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = fa-artikel.depn-wert - diff-wert
                        out-list.book-val = fa-artikel.book-wert + diff-wert.
                END.

                /* added FIND FIRST because fa-kateg not found by Oscar (22 Agustus 2024) - 0D6718 */
                FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                IF AVAILABLE fa-kateg THEN
                DO:
                    ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                END.
                
                IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = fa-artikel.anz-depn.        
                IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
                DO: 
                    t-anz  = t-anz + fa-artikel.anzahl.
                    t-oh   = t-oh + fa-artikel.warenwert.
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
                        t-anz   = t-anz + fa-artikel.anzahl.
                        t-oh    = t-oh + fa-artikel.warenwert.
                        t-depn  = t-depn + fa-artikel.depn-wert - diff-wert. 
                        t-book  = t-book + fa-artikel.book-wert + diff-wert.
                    END. 
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
  	CREATE out-list. 
  	ASSIGN 
		out-list.bezeich = "SUBTOTAL"
		out-list.flag = 1
		/*out-list.bezeich = gl-acct.bezeich*/
		out-list.qty = t-anz
		out-list.init-val = t-oh
		out-list.depn-val = t-depn
		out-list.book-val = t-book.

  	CREATE out-list. 
  	CREATE out-list. 
  	ASSIGN 
		out-list.bezeich = "T O T A L"
		out-list.qty = tot-anz
		out-list.init-val = tot-oh
		out-list.depn-val = tot-depn
		out-list.book-val = tot-book.
END. 

PROCEDURE create-listACCT1:  /* all FA-Group BY acctno */ 
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
 
  	diff-n = (YEAR(last-acctdate) - yy) * 12 +  MONTH(last-acctdate) - mm. 

	/*ITA 110315*/
	IF mi-bookvalue-chk = YES THEN DO:
		FOR EACH mathis WHERE mathis.datum GE from-date
		AND mathis.datum LE to-date NO-LOCK, 
		FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
		AND fa-artikel.loeschflag = 0 AND fa-artikel.gnr = from-grp
		/*AND fa-artikel.loeschflag = 0 AND (fa-artikel.anz-depn - diff-n) GE 0 */
		NO-LOCK BY fa-artikel.fibukonto: 

            /* adding this code so filter "Full Depreciation Only" work by Oscar (27 Agustus 2024) - B3BA7B */
            do-it = NO.
            IF NOT zero-value-only THEN do-it = YES.
            ELSE do-it = fa-artikel.book-wert EQ 0.
            
            IF do-it THEN 
            DO:
                /*IF curr-acct = "" THEN curr-acct = fa-artikel.fibukonto.*/
                IF curr-acct NE fa-artikel.fibukonto /* AND curr-acct NE ""  disable this by Oscar (27 Agustus 2024) - B3BA7B */ THEN 
                DO: 
                    ASSIGN 
                        tot-anz  = tot-anz + t-anz
                        tot-oh   = tot-oh + t-oh
                        tot-depn = tot-depn + t-depn
                        tot-book = tot-book + t-book.
                
                    FIND FIRST gl-acct WHERE gl-acct.fibukonto = curr-acct NO-LOCK NO-ERROR. 
                    IF AVAILABLE gl-acct THEN RUN convert-fibu(curr-acct, OUTPUT fibu). 
            
                    IF curr-acct NE "" THEN DO:
                        CREATE out-list. 
                        ASSIGN
                            out-list.location  = ""
                            out-list.bezeich   = "SUBTOTAL"
                            out-list.qty 	   = t-anz
                            out-list.init-val  = t-oh
                            out-list.depn-val  = t-depn
                            out-list.book-val  = t-book.
                        CREATE out-list.
                    END.
        
                    ASSIGN
                        curr-acct = fa-artikel.fibukonto
                        t-anz     = 0
                        t-oh      = 0 
                        t-depn    = 0
                        t-book    = 0. 
                END.
            
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-artikel.fibukonto NO-LOCK NO-ERROR. 
                RUN convert-fibu(fa-artikel.fibukonto, OUTPUT fibu). 

                FIND FIRST out-list WHERE out-list.fibu = fibu NO-ERROR.
                IF AVAILABLE out-list THEN DO:
                    CREATE out-list. 
                    ASSIGN
                        out-list.flag 		= 1
                        out-list.refno    	= mathis.asset 
                        out-list.location 	= mathis.location
                        out-list.bezeich 	= mathis.NAME
                        out-list.received 	= mathis.datum
                        out-list.qty 		= fa-artikel.anzahl.
                END.
                ELSE DO:
                    CREATE out-list. 
                    ASSIGN 
                        out-list.flag 		= 1
                        out-list.refno    	= mathis.asset 
                        out-list.location 	= trim(mathis.location)
                        out-list.fibu 		= fibu
                        out-list.bezeich	= mathis.NAME
                        out-list.received 	= mathis.datum
                        out-list.qty 		= fa-artikel.anzahl.
                END.

                ASSIGN 
                    val-dep     = fa-artikel.depn-wert / fa-artikel.anz-depn
                    sub-depn    = 0
                    flag        = NO.

                IF val-dep = ? THEN val-dep = 0.
                DO datum = from-date TO to-date:
                    IF flag AND datum = DATE(MONTH(datum) + 1, 1, YEAR(datum)) - 1 THEN 
                            ASSIGN sub-depn = sub-depn + 1.
            
                    IF datum = fa-artikel.first-depn THEN 
                        ASSIGN 
                            sub-depn    = sub-depn + 1
                            flag        = YES.

                    IF datum = fa-artikel.last-depn THEN LEAVE.
                END.

                ASSIGN 
                    p-depn-wert = val-dep * sub-depn
                    p-book-wert = fa-artikel.warenwert - p-depn-wert.
        
                /*ITA 160214*/    
                IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
                DO: 
                    ASSIGN
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = 0
                        out-list.book-val = fa-artikel.warenwert.
                END. 
                ELSE 
                DO:
                    ASSIGN
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = p-depn-wert - diff-wert
                        out-list.book-val = p-book-wert + diff-wert.
                END. 
            
                /* added FIND FIRST because fa-kateg not found by Oscar (22 Agustus 2024) - 0D6718 */
                FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                IF AVAILABLE fa-kateg THEN
                DO:
                    ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                END.

                IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = sub-depn.
                
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
      	END.
  	END. /*end*/

  	ELSE DO:
      	FOR EACH mathis WHERE mathis.datum GE from-date
        AND mathis.datum LE to-date NO-LOCK, 
       	FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
		AND fa-artikel.loeschflag = 0 AND fa-artikel.gnr = from-grp
        /*AND fa-artikel.loeschflag = 0 AND (fa-artikel.anz-depn - diff-n) GE 0 */
        NO-LOCK BY fa-artikel.fibukonto: 
            
            /* adding this code so filter "Full Depreciation Only" work by Oscar (27 Agustus 2024) - B3BA7B */
            do-it = NO.
            IF NOT zero-value-only THEN do-it = YES.
            ELSE do-it = fa-artikel.book-wert EQ 0.
            
            IF do-it THEN 
            DO:
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
                    
                        CREATE out-list.
                        ASSIGN
                            out-list.location  = ""
                            out-list.bezeich = "SUBTOTAL"
                            out-list.qty = t-anz
                            out-list.init-val = t-oh
                            out-list.depn-val = t-depn
                            out-list.book-val = t-book.
                        CREATE out-list.
                    END.
            
                    ASSIGN
                        curr-acct = fa-artikel.fibukonto
                        t-anz     = 0
                        t-oh      = 0 
                        t-depn    = 0
                        t-book    = 0. 
                END.
        
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-artikel.fibukonto NO-LOCK NO-ERROR. 
                RUN convert-fibu(fa-artikel.fibukonto, OUTPUT fibu). 
            
                FIND FIRST out-list WHERE out-list.fibu = fibu NO-ERROR.
                IF AVAILABLE out-list THEN 
                DO:
                    CREATE out-list. 
                    ASSIGN 
                        out-list.refno    = mathis.asset 
                        out-list.location = trim(mathis.location)
                        out-list.bezeich  = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty 	  = fa-artikel.anzahl.
        
                END.
                ELSE 
                DO:
                    CREATE out-list. 
                    ASSIGN 
                        out-list.refno    = mathis.asset 
                        out-list.location = trim(mathis.location) 
                        out-list.bezeich  = mathis.NAME
                        out-list.received = mathis.datum
                        out-list.qty 	  = fa-artikel.anzahl
                        out-list.fibu     = fibu.
                END.
        
                /*ITA 160214*/    
                IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
                DO: 
                    ASSIGN
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = 0 
                        out-list.book-val = fa-artikel.warenwert.
                END. 
                ELSE 
                DO: 
                    ASSIGN
                        out-list.init-val = fa-artikel.warenwert
                        out-list.depn-val = fa-artikel.depn-wert - diff-wert
                        out-list.book-val = fa-artikel.book-wert + diff-wert.
                END.

                /* added FIND FIRST because fa-kateg not found by Oscar (22 Agustus 2024) - 0D6718 */
                FIND FIRST fa-kateg WHERE fa-kateg.katnr EQ fa-artikel.katnr NO-LOCK NO-ERROR.
                IF AVAILABLE fa-kateg THEN
                DO:
                    ASSIGN out-list.kateg = fa-kateg.bezeich + " - " + STRING(fa-kateg.rate) + "%".
                END.
                
                IF fa-artikel.first-depn NE ? THEN out-list.first-depn = fa-artikel.first-depn.
                IF fa-artikel.next-depn NE ? THEN out-list.next-depn = fa-artikel.next-depn.
                IF fa-artikel.last-depn NE ? THEN out-list.last-depn = fa-artikel.last-depn.
                IF fa-artikel.anz-depn NE ? THEN out-list.depn-no = fa-artikel.anz-depn.        
                IF (fa-artikel.anz-depn - diff-n) EQ 0 THEN 
                DO: 
                    t-anz  = t-anz + fa-artikel.anzahl.
                    t-oh   = t-oh + fa-artikel.warenwert.
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
                        t-anz   = t-anz + fa-artikel.anzahl.
                        t-oh    = t-oh + fa-artikel.warenwert.
                        t-depn  = t-depn + fa-artikel.depn-wert - diff-wert. 
                        t-book  = t-book + fa-artikel.book-wert + diff-wert.
                    END. 
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
  	CREATE out-list. 
  	ASSIGN 
		out-list.bezeich = "SUBTOTAL"
		out-list.flag = 1
		/*out-list.bezeich = gl-acct.bezeich*/
		out-list.qty = t-anz
		out-list.init-val = t-oh
		out-list.depn-val = t-depn
		out-list.book-val = t-book.

  	CREATE out-list. 
  	CREATE out-list. 
  	ASSIGN 
		out-list.bezeich = "T O T A L"
		out-list.qty = tot-anz
		out-list.init-val = tot-oh
		out-list.depn-val = tot-depn
		out-list.book-val = tot-book.
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


DEF TEMP-TABLE q2-list
    FIELD bestelldatum AS DATE                                  COLUMN-LABEL "OrderDate"                       
    FIELD bezeich AS CHAR                                       COLUMN-LABEL "Department"                   FORMAT "x(24)"       
    FIELD firma LIKE l-lieferant.firma                          COLUMN-LABEL "Supplier"                        
    FIELD docu-nr LIKE l-orderhdr.docu-nr                       COLUMN-LABEL "Document No"                  FORMAT "x(10)"      
    FIELD l-orderhdr-lieferdatum LIKE l-orderhdr.lieferdatum    COLUMN-LABEL "Deliver Date"                    
    FIELD wabkurz AS CHAR 
    FIELD bestellart LIKE l-orderhdr.bestellart                 COLUMN-LABEL "Type of Order"           
    FIELD gedruckt LIKE l-orderhdr.gedruckt                     COLUMN-LABEL "Released"                
    FIELD l-orderhdr-besteller LIKE l-orderhdr.besteller        COLUMN-LABEL "Created by"              
    FIELD l-order-gedruckt LIKE l-order.gedruckt                COLUMN-LABEL "Printed"                 
    FIELD zeit LIKE l-order.zeit                                COLUMN-LABEL "Time"                    
    FIELD lief-fax-2 AS CHARACTER                               COLUMN-LABEL "Changed by"              
    FIELD l-order-lieferdatum LIKE l-order.lieferdatum          COLUMN-LABEL "ChgDate"                 
    FIELD lief-fax-3 AS CHARACTER                                  COLUMN-LABEL "Closed by/Order Instruction"               
    FIELD lieferdatum-eff LIKE l-order.lieferdatum-eff          COLUMN-LABEL "CloseDate"               
    FIELD lief-fax-1 AS CHARACTER                                  COLUMN-LABEL "PR Number"       
    FIELD lief-nr LIKE l-order.lief-nr                          COLUMN-LABEL "Supplier Number"
    FIELD username          AS CHAR
    FIELD del-reason        AS CHAR FORMAT "x(32)" /*gerald 080520 Reason on delete*/
    FIELD tot-amount        AS DECIMAL
    FIELD art-number        AS INTEGER
    FIELD art-desc          AS CHARACTER
    FIELD content           AS DECIMAL
    FIELD order-qty         AS DECIMAL
    FIELD unit-price        AS DECIMAL
    FIELD gross-amount      AS DECIMAL
    FIELD deliv-unit        AS CHARACTER
    FIELD nett-price        AS DECIMAL
    FIELD nett-amount       AS DECIMAL
    FIELD arrival-date      AS CHARACTER
    FIELD s-unit            AS INTEGER
    FIELD d-unit            AS DECIMAL
    FIELD art-unit          AS CHARACTER
    FIELD last-user         AS CHARACTER
    FIELD account-number    AS CHARACTER
    FIELD account-name      AS CHARACTER
    FIELD remark            AS CHARACTER
    FIELD flag-line         AS LOGICAL
    .

DEF TEMP-TABLE t-list
    FIELD bestelldatum LIKE l-orderhdr.bestelldatum             COLUMN-LABEL "OrderDate"                       
    FIELD bezeich AS CHAR                                       COLUMN-LABEL "Department"                   FORMAT "x(24)"       
    FIELD firma LIKE l-lieferant.firma                          COLUMN-LABEL "Supplier"                        
    FIELD docu-nr LIKE l-orderhdr.docu-nr                       COLUMN-LABEL "Document No"                  FORMAT "x(10)"      
    FIELD l-orderhdr-lieferdatum LIKE l-orderhdr.lieferdatum    COLUMN-LABEL "Deliver Date"                    
    FIELD wabkurz AS CHAR 
    FIELD bestellart LIKE l-orderhdr.bestellart                 COLUMN-LABEL "Type of Order"           
    FIELD gedruckt LIKE l-orderhdr.gedruckt                     COLUMN-LABEL "Released"                
    FIELD l-orderhdr-besteller LIKE l-orderhdr.besteller        COLUMN-LABEL "Created by"              
    FIELD l-order-gedruckt LIKE l-order.gedruckt                COLUMN-LABEL "Printed"                 
    FIELD zeit LIKE l-order.zeit                                COLUMN-LABEL "Time"                    
    FIELD lief-fax-2 AS CHARACTER                               COLUMN-LABEL "Changed by"              
    FIELD l-order-lieferdatum LIKE l-order.lieferdatum          COLUMN-LABEL "ChgDate"                 
    FIELD lief-fax-3 AS CHARACTER                                  COLUMN-LABEL "Closed by/Order Instruction"               
    FIELD lieferdatum-eff LIKE l-order.lieferdatum-eff          COLUMN-LABEL "CloseDate"               
    FIELD lief-fax-1 AS CHARACTER                                  COLUMN-LABEL "PR Number"       
    FIELD lief-nr LIKE l-order.lief-nr                          COLUMN-LABEL "Supplier Number"
    FIELD username              AS CHAR
    FIELD del-reason            AS CHAR FORMAT "x(32)" /*gerald 080520 Reason on delete*/
    FIELD tot-amount            AS DECIMAL
    .

DEFINE INPUT PARAMETER usrname      AS CHAR.
DEFINE INPUT PARAMETER po-number    AS CHAR. 
DEFINE INPUT PARAMETER last-doc-nr AS CHAR. 
DEFINE INPUT PARAMETER app-sort     AS CHARACTER.
DEFINE INPUT PARAMETER dml-only     AS LOGICAL.     
DEFINE INPUT PARAMETER t-liefNo     AS INTEGER.               
DEFINE INPUT PARAMETER deptnr       AS INTEGER.
DEFINE INPUT PARAMETER all-supp     AS LOGICAL.    
DEFINE INPUT PARAMETER stattype     AS INTEGER.
DEFINE INPUT PARAMETER sorttype     AS INTEGER.
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER billdate     AS DATE.
DEFINE INPUT PARAMETER pr-only      AS LOGICAL. /*FDL August 01, 2024 => Ticket 8300F1 */
DEFINE INPUT PARAMETER excl-dml-pr  AS LOGICAL. /*FDL August 01, 2024 => Ticket 8300F1 */

DEFINE OUTPUT PARAMETER p-267 AS INTEGER.
DEFINE OUTPUT PARAMETER first-docu-nr AS CHAR.
DEFINE OUTPUT PARAMETER curr-docu-nr AS CHAR.
DEFINE OUTPUT PARAMETER last-docu-nr AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR q2-list.

DEFINE VARIABLE param267 AS LOGICAL.

IF usrName    eq ? then usrName   = "".
IF po-number  eq ? then po-number = "".
IF dml-only   eq ? then dml-only  = NO.
IF t-liefNo   eq ? then t-liefNo  = 0.
IF sorttype   eq ? then sorttype  = 1.
IF deptnr     eq ? then deptnr    = -1.
IF all-supp   eq ? then all-supp  = YES.
IF stattype   eq ? then stattype  = 0.
IF usrName    eq ? then usrName   = "".

IF po-number NE "" THEN
DO:
    /*FDL August 01, 2024 => Ticket 8300F1 - Add _1*/
    RUN po-list-btn-go_1cldbl.p(usrName, po-number, dml-only, pr-only, excl-dml-pr, OUTPUT param267, OUTPUT TABLE t-list).
END.
ELSE 
DO:
    /*FDL August 01, 2024 => Ticket 8300F1 - Add _1*/
    RUN po-list-btn-go2_1cldbl.p(t-liefNo, last-doc-nr, sorttype, deptnr, all-supp, stattype, usrName,
                from-date, to-date, billdate, dml-only, app-sort, pr-only, excl-dml-pr,
                OUTPUT first-docu-nr, OUTPUT curr-docu-nr, OUTPUT param267, OUTPUT last-docu-nr,
                OUTPUT TABLE t-list).
END.
p-267 = INT(param267).

FOR EACH t-list NO-LOCK BY t-list.docu-nr:
    CREATE q2-list.
    BUFFER-COPY t-list TO q2-list.

    FIND FIRST l-order WHERE l-order.docu-nr EQ t-list.docu-nr
        AND l-order.loeschflag EQ 0
        AND l-order.pos GT 0 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-order:

        CREATE q2-list.
        ASSIGN
            q2-list.flag-line   = YES
            q2-list.docu-nr     = l-order.docu-nr
            q2-list.art-number  = l-order.artnr
            q2-list.order-qty   = l-order.anzahl
            q2-list.nett-price  = l-order.einzelpreis
            q2-list.nett-amount = l-order.warenwert
            q2-list.account-number = l-order.stornogrund
            q2-list.remark      = l-order.besteller
            q2-list.deliv-unit  = l-order.lief-fax[3]
            q2-list.d-unit      = l-order.geliefert            
            q2-list.s-unit      = l-order.angebot-lief[1]
            q2-list.last-user   = l-order.lief-fax[2]
            .

        IF l-order.lieferdatum-eff NE ? THEN q2-list.arrival-date = STRING(l-order.lieferdatum-eff).
        ELSE q2-list.arrival-date = "".

        FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ l-order.stornogrund NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN q2-list.account-name = gl-acct.bezeich.

        FIND FIRST l-artikel WHERE l-artikel.artnr EQ l-order.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE l-artikel THEN
        DO:
            ASSIGN
                q2-list.art-desc    = l-artikel.bezeich
                q2-list.content     = l-artikel.lief-einheit
                q2-list.art-unit    = l-artikel.masseinheit
                .
        END.

        FIND NEXT l-order WHERE l-order.docu-nr EQ t-list.docu-nr
            AND l-order.loeschflag EQ 0
            AND l-order.pos GT 0 NO-LOCK NO-ERROR.
    END.
END.

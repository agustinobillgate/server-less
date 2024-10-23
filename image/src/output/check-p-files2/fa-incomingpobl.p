
DEFINE TEMP-TABLE op-list
    FIELD lscheinnr     LIKE fa-op.lscheinnr
    FIELD name          LIKE mathis.name
    FIELD location      LIKE mathis.location
    FIELD einzelpreis   LIKE fa-op.einzelpreis
    FIELD anzahl        LIKE fa-op.anzahl
    FIELD warenwert     LIKE fa-op.warenwert
    FIELD firma         LIKE l-lieferant.firma
    FIELD datum         LIKE fa-op.datum
    FIELD docu-nr       LIKE fa-op.docu-nr
    FIELD lief-nr       LIKE fa-op.lief-nr
    FIELD rec-id        AS INT.

DEFINE TEMP-TABLE fa-ordheaderlist LIKE fa-ordheader
    FIELD create-name    AS CHAR  FORMAT "x(30)"
    FIELD modify-name    AS CHAR  FORMAT "x(30)"
    FIELD total-amount1  AS DECIMAL  FORMAT "->,>>>,>>>,>>>,>>9.99" .


DEFINE INPUT PARAMETER fromdate   AS DATE.
DEFINE INPUT PARAMETER todate     AS DATE.
DEFINE INPUT PARAMETER searchby   AS INTEGER.
DEFINE INPUT PARAMETER devnote-no AS CHARACTER.
DEFINE INPUT PARAMETER po-no      AS CHARACTER.
DEFINE INPUT PARAMETER supp-no    AS INTEGER.

/*
DEFINE VARIABLE fromdate AS DATE INIT 08/01/19.
DEFINE VARIABLE todate AS DATE INIT 09/30/19.
DEFINE VARIABLE searchby AS CHARACTER INIT "PO".
DEFINE VARIABLE devnote-no AS CHARACTER INIT "if190822004".
DEFINE VARIABLE po-no AS CHARACTER.
DEFINE VARIABLE supp-no AS INTEGER.
*/

RUN create-faOrdHeaderlist.
RUN Distinct-op.


PROCEDURE Distinct-OP :
    DEFINE VARIABLE temp-Number         AS CHAR.

    FOR EACH op-list :
        DELETE op-list.
    END.

    IF (devnote-no = "" AND po-no = "" AND supp-no = 0) OR searchby = 0 OR 
       (searchby = 1 AND devnote-no = "") OR
       (searchby = 2 AND po-no = "") OR 
       (searchby = 3 AND supp-no = 0) THEN
    DO:
        FOR EACH fa-op WHERE fa-op.loeschflag <= 1 AND 
            fa-op.warenwert > 0 AND fa-op.datum GE fromdate AND fa-op.datum LE todate NO-LOCK,
            FIRST fa-ordheaderlist WHERE fa-ordheaderlist.order-nr = fa-op.docu-nr  NO-LOCK,
            FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-op.lief-nr NO-LOCK,
            FIRST mathis WHERE mathis.nr = fa-op.nr NO-LOCK
            BY fa-op.docu-nr BY fa-op.lscheinnr BY fa-op.zeit :
            IF temp-Number = "" THEN
            DO:
                temp-number = fa-op.lscheinnr.
                RUN create-op-list.
            END.
            ELSE
            DO:
                IF temp-number NE fa-op.lscheinnr THEN
                DO:
                    temp-number = fa-op.lscheinnr.
                    RUN create-op-list.
                END.
            END.
        END.
    END.    
    ELSE IF searchby = 1 AND devnote-no NE "" THEN
        FOR EACH fa-op WHERE fa-op.loeschflag <= 1 AND 
            fa-op.warenwert > 0 AND fa-op.datum GE fromdate AND fa-op.datum LE todate AND
            fa-op.lscheinnr = devnote-no NO-LOCK,
            FIRST fa-ordheaderlist WHERE fa-ordheaderlist.order-nr = fa-op.docu-nr  NO-LOCK,
            FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-op.lief-nr NO-LOCK,
            FIRST mathis WHERE mathis.nr = fa-op.nr NO-LOCK
            BY fa-op.docu-nr BY fa-op.lscheinnr BY fa-op.zeit :
            IF temp-Number = "" THEN
            DO:
                temp-number = fa-op.lscheinnr.
                RUN create-op-list.
            END.
            ELSE
            DO:
                IF temp-number NE fa-op.lscheinnr THEN
                DO:
                    temp-number = fa-op.lscheinnr.
                    RUN create-op-list.
                END.
            END.
        END.
    ELSE IF searchby = 2 AND po-no NE "" THEN
        FOR EACH fa-op WHERE fa-op.loeschflag <= 1 AND 
            fa-op.warenwert > 0 AND fa-op.datum GE fromdate AND fa-op.datum LE todate AND
            fa-op.lscheinnr NE "" NO-LOCK,
            FIRST fa-ordheaderlist WHERE fa-ordheaderlist.order-nr = fa-op.docu-nr  
            AND fa-ordheaderlist.order-nr = po-no NO-LOCK,
            FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-op.lief-nr NO-LOCK,
            FIRST mathis WHERE mathis.nr = fa-op.nr NO-LOCK
            BY fa-op.docu-nr BY fa-op.lscheinnr BY fa-op.zeit :
            IF temp-Number = "" THEN
            DO:
                temp-number = fa-op.lscheinnr.
                RUN create-op-list.
            END.
            ELSE
            DO:
                IF temp-number NE fa-op.lscheinnr THEN
                DO:
                    temp-number = fa-op.lscheinnr.
                    RUN create-op-list.
                END.
            END.
        END.
    ELSE IF searchby = 3 AND supp-no NE 0 THEN
        FOR EACH fa-op WHERE fa-op.loeschflag <= 1 AND 
            fa-op.warenwert > 0 AND fa-op.datum GE fromdate AND fa-op.datum LE todate AND
            fa-op.lscheinnr NE "" NO-LOCK,
            FIRST fa-ordheaderlist WHERE fa-ordheaderlist.order-nr = fa-op.docu-nr  
            AND fa-ordheaderlist.supplier-nr = supp-no NO-LOCK,
            FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-op.lief-nr NO-LOCK,
            FIRST mathis WHERE mathis.nr = fa-op.nr NO-LOCK
            BY fa-op.docu-nr BY fa-op.lscheinnr BY fa-op.zeit :
            IF temp-Number = "" THEN
            DO:
                temp-number = fa-op.lscheinnr.
    
                RUN create-op-list.
                BUFFER-COPY fa-op TO op-list.
            END.
            ELSE
            DO:
                IF temp-number NE fa-op.lscheinnr THEN
                DO:
                    temp-number = fa-op.lscheinnr.
                    RUN create-op-list.
                END.
            END.
        END.
END PROCEDURE.

PROCEDURE create-op-list:
    CREATE op-list.
    ASSIGN
        op-list.lscheinnr     = fa-op.lscheinnr
        op-list.name          = mathis.name
        op-list.location      = mathis.location
        op-list.einzelpreis   = fa-op.einzelpreis
        op-list.anzahl        = fa-op.anzahl
        op-list.warenwert     = fa-op.warenwert
        op-list.firma         = l-lieferant.firma
        op-list.datum         = fa-op.datum
        op-list.docu-nr       = fa-op.docu-nr
        op-list.lief-nr       = fa-op.lief-nr
        op-list.rec-id        = RECID(fa-op).
END.

PROCEDURE create-faOrdHeaderlist :
    DEF VAR temp-create AS CHAR FORMAT "x(30)".
    DEF VAR temp-modify AS CHAR FORMAT "x(30)".
    DEF VAR total-amount  AS DECIMAL INITIAL 0.

    FOR EACH fa-ordheaderlist :
        DELETE fa-ordheaderlist.
    END.

    FOR EACH fa-ordheader NO-LOCK USE-INDEX datumactive :

        IF fa-ordheader.created-by NE "" THEN
        DO:
            FIND FIRST bediener WHERE bediener.userinit = fa-ordheader.created-by NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN temp-create = bediener.username.
            ELSE temp-create = "".
        END.
        ELSE
        DO:
            temp-create = "".
        END.

        IF fa-ordheader.modified-by NE "" THEN
        DO:
            FIND FIRST bediener WHERE bediener.userinit = fa-ordheader.modified-by NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN temp-modify = bediener.username.
            ELSE temp-modify = "".
        END.
        ELSE
        DO:
            temp-modify = "".
        END.
        
        FOR EACH fa-order WHERE fa-order.order-nr  = fa-ordheader.order-nr NO-LOCK:
            total-amount = total-amount + fa-order.order-amount.    
        END.

        CREATE fa-ordheaderlist.
        BUFFER-COPY fa-ordheader TO fa-ordheaderlist.
        ASSIGN fa-ordheaderlist.create-name = temp-create
               fa-ordheaderlist.modify-name = temp-modify
               fa-ordheaderlist.total-amount1 = total-amount.

        temp-create     = "".
        temp-modify     = "".
        total-amount    = 0.
    END.


END PROCEDURE.


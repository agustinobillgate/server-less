DEFINE TEMP-TABLE ttStock 
    FIELD dDate     AS DATE FORMAT "99/99/99"           COLUMN-LABEL "Date" 
    FIELD iSt       AS INTEGER FORMAT "99"              COLUMN-LABEL "St" 
    FIELD sDocument AS CHARACTER FORMAT "X(12)"         COLUMN-LABEL "Document No" 
    FIELD delivnote AS CHARACTER FORMAT "x(12)"         column-label "Delivery Note"
    FIELD iArticle  AS INTEGER FORMAT "9999999"         COLUMN-LABEL "Article No" 
    FIELD sDesc     AS CHARACTER FORMAT "X(36)"         COLUMN-LABEL "Description" 
    FIELD dQuantity AS INTEGER FORMAT "->>>,>>9.99"     COLUMN-LABEL "Quantity" 
    FIELD sAmount   AS CHARACTER FORMAT "X(19)"         COLUMN-LABEL "Amount" 
    FIELD price     AS DECIMAL FORMAT "->,>>>,>>9.999"  COLUMN-LABEL "Unit Price"
    FIELD itime     AS CHARACTER FORMAT "x(8)"          COLUMN-LABEL "Time"
    FIELD sSupplier AS CHARACTER FORMAT "X(30)"         COLUMN-LABEL "Supplier" 
    FIELD sNote     AS CHARACTER FORMAT "X(8)" 
    FIELD iMark      AS INTEGER.

DEFINE INPUT PARAMETER sname        AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER fdate        AS DATE.
DEFINE INPUT PARAMETER tdate        AS DATE.
DEFINE INPUT PARAMETER show-price   AS LOGICAL.
DEFINE INPUT PARAMETER long-digit   AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR ttStock.

DEFINE VARIABLE tot-anz     AS DECIMAL.
DEFINE VARIABLE tot-amount  AS DECIMAL.
DEFINE VARIABLE note-str    AS CHARACTER EXTENT 2 
    INITIAL ["        ", "Transfer"]                    NO-UNDO. 


RUN create-list.

PROCEDURE create-list :
DEFINE VARIABLE del-note2 AS CHAR.
DEFINE VARIABLE curr-note AS CHAR.
DEFINE VARIABLE sub-anz AS INTEGER.
DEFINE VARIABLE sub-amount AS DECIMAL.

FOR EACH ttStock: 
    DELETE ttStock. 
END. 

ASSIGN 
    tot-anz     = 0 
    tot-amount  = 0
    sub-anz     = 0
    sub-amount  = 0. 

FIND FIRST l-lieferant WHERE l-lieferant.firma = sname NO-LOCK NO-ERROR.
IF AVAILABLE l-lieferant THEN DO:
    FOR EACH l-op NO-LOCK WHERE /*l-op.lscheinnr = del-note AND*/ l-op.loeschflag LT 2 AND 
        l-op.op-art = 1 AND l-op.lief-nr = l-lieferant.lief-nr AND l-op.datum GE
        fdate AND l-op.datum LE tdate,
        FIRST l-artikel NO-LOCK WHERE l-artikel.artnr = l-op.artnr BY 
        l-op.lscheinnr BY l-op.artnr:

        IF curr-note NE "" AND curr-note NE l-op.lscheinnr THEN
        DO:
            CREATE ttstock.
            ASSIGN 
                ttStock.sDesc       = "SubTotal" 
                ttStock.dQuantity   = sub-anz 
                ttStock.iMark       = 1. 
            
            /*
              IF show-price THEN ASSIGN 
                ttStock.sAmount     = IF long-digit THEN STRING(sub-amount, "   ->>>,>>>,>>>,>>9") ELSE 
                    STRING(sub-amount, "->>>,>>>,>>>,>>9.99"). 
               ASSIGN
                   sub-anz = 0
                   sub-amount = 0.
            */
            /*dody change format IF*/
            IF show-price THEN
            DO:
                IF long-digit THEN ttStock.sAmount = STRING(sub-amount, "   ->>>,>>>,>>>,>>9").
                ELSE ttStock.sAmount = STRING(sub-amount, "->>>,>>>,>>>,>>9.99").
            END.
            ASSIGN
                sub-anz = 0
                sub-amount = 0. 
        END.

        curr-note = l-op.lscheinnr.
        CREATE ttstock.
        ASSIGN 
            sub-anz             = sub-anz + l-op.anzahl
            sub-amount          = sub-amount + l-op.warenwert
            tot-anz             = tot-anz + l-op.anzahl 
            tot-amount          = tot-amount + l-op.warenwert
            ttStock.dDate       = l-op.datum 
            ttStock.iSt         = l-op.lager-nr 
            ttStock.iArticle    = l-artikel.artnr 
            ttStock.sDocument   = l-op.docu-nr 
            ttStock.sDesc       = l-artikel.bezeich 
            ttStock.dQuantity   = l-op.anzahl 
            ttstock.price       = l-op.einzelpreis
            ttstock.itime       = STRING(l-op.zeit,"HH:MM:SS")
            ttStock.sNote       = note-str[l-op.op-art] 
            ttStock.iMark       = 0
            ttStock.sSupplier   = l-lieferant.firma
            ttStock.delivnote   = l-op.lscheinnr. 
        
        /*
        IF show-price THEN ASSIGN 
            ttStock.sAmount     = IF long-digit THEN STRING(l-op.warenwert, "   ->>>,>>>,>>>,>>9") ELSE 
                STRING(l-op.warenwert, "->>>,>>>,>>>,>>9.99"). */
        /*dody change format IF*/
        IF show-price THEN
        DO:
            IF long-digit THEN ttStock.sAmount = STRING(l-op.warenwert, "   ->>>,>>>,>>>,>>9").
            ELSE ttStock.sAmount = STRING(l-op.warenwert, "->>>,>>>,>>>,>>9.99").
        END.
    END.
    FOR EACH l-ophis WHERE l-ophis.lief-nr = l-lieferant.lief-nr AND 
        l-ophis.datum GE fdate AND l-ophis.datum LE tdate AND 
        l-ophis.op-art = 1 AND NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*" NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK BY 
        l-ophis.lscheinnr BY l-ophis.artnr:
        IF curr-note NE "" AND curr-note NE l-ophis.lscheinnr THEN
        DO:
            CREATE ttstock.
            ASSIGN 
                ttStock.sDesc       = "SubTotal" 
                ttStock.dQuantity   = sub-anz 
                ttStock.iMark       = 1. 
            
              /*
              IF show-price THEN ASSIGN 
                ttStock.sAmount     = IF long-digit THEN STRING(sub-amount, "   ->>>,>>>,>>>,>>9") ELSE 
                    STRING(sub-amount, "->>>,>>>,>>>,>>9.99"). 
               ASSIGN
                   sub-anz = 0
                   sub-amount = 0.
            */
            /*dody change format IF*/
            IF show-price THEN
            DO:
                IF long-digit THEN ttStock.sAmount = STRING(sub-amount, "   ->>>,>>>,>>>,>>9").
                ELSE ttStock.sAmount = STRING(sub-amount, "->>>,>>>,>>>,>>9.99").
            END.
            ASSIGN
                sub-anz = 0
                sub-amount = 0. 

        END.
        curr-note = l-ophis.lscheinnr.
        CREATE ttstock.
        ASSIGN 
            sub-anz             = sub-anz + l-ophis.anzahl 
            sub-amount          = sub-amount + l-ophis.warenwert
            tot-anz             = tot-anz + l-ophis.anzahl 
            tot-amount          = tot-amount + l-ophis.warenwert
            ttStock.dDate       = l-ophis.datum 
            ttStock.iSt         = l-ophis.lager-nr 
            ttStock.iArticle    = l-artikel.artnr 
            ttStock.sDocument   = l-ophis.docu-nr 
            ttStock.sDesc       = l-artikel.bezeich 
            ttStock.dQuantity   = l-ophis.anzahl 
            ttstock.price       = l-ophis.einzelpreis
            /*ttstock.itime       = STRING(l-ophis.zeit,"HH:MM:SS")*/
            ttStock.sNote       = note-str[l-ophis.op-art] 
            ttStock.iMark       = 0
            ttStock.sSupplier   = l-lieferant.firma
            ttStock.delivnote   = l-ophis.lscheinnr. 
        
        /*
        IF show-price THEN ASSIGN 
            ttStock.sAmount     = IF long-digit THEN STRING(l-op.warenwert, "   ->>>,>>>,>>>,>>9") ELSE 
                STRING(l-op.warenwert, "->>>,>>>,>>>,>>9.99"). */
        /*dody change format IF*/
        IF show-price THEN
        DO:
            IF long-digit THEN ttStock.sAmount = STRING(l-op.warenwert, "   ->>>,>>>,>>>,>>9").
            ELSE ttStock.sAmount = STRING(l-op.warenwert, "->>>,>>>,>>>,>>9.99").
        END.
    END.

    CREATE ttstock.
    ASSIGN 
        ttStock.sDesc       = "SubTotal" 
        ttStock.dQuantity   = sub-anz 
        ttStock.iMark       = 1. 
    
    /*
      IF show-price THEN ASSIGN 
        ttStock.sAmount     = IF long-digit THEN STRING(sub-amount, "   ->>>,>>>,>>>,>>9") ELSE 
            STRING(sub-amount, "->>>,>>>,>>>,>>9.99"). */
    /*dody change format IF*/
    IF show-price THEN
    DO:
        IF long-digit THEN ttStock.sAmount = STRING(sub-amount, "   ->>>,>>>,>>>,>>9").
        ELSE ttStock.sAmount = STRING(sub-amount, "->>>,>>>,>>>,>>9.99").
    END.

  CREATE ttStock. 
  ASSIGN 
    ttStock.sDesc       = "T O T A L" 
    ttStock.dQuantity   = tot-anz 
    ttStock.iMark       = 2. 

  /*
    IF show-price THEN ASSIGN 
    ttStock.sAmount     = IF long-digit THEN STRING(tot-amount, "   ->>>,>>>,>>>,>>9") ELSE 
        STRING(tot-amount, "->>>,>>>,>>>,>>9.99"). */
    /*dody change format IF*/
    IF show-price THEN
    DO:
        IF long-digit THEN ttStock.sAmount = STRING(tot-amount, "   ->>>,>>>,>>>,>>9").
        ELSE ttStock.sAmount = STRING(tot-amount, "->>>,>>>,>>>,>>9.99").
    END.
END.



END PROCEDURE.

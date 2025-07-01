
DEF TEMP-TABLE t-rcv-trx
    FIELD rcvtrx-suppName       AS CHAR
    FIELD rcvtrx-suppBRN        AS INT
    FIELD rcvtrx-invoiceDate    AS DATE
    FIELD rcvtrx-invoiceNumber  AS CHAR
    FIELD rcvtrx-importDecNo    AS INT
    FIELD rcvtrx-LineNumber     AS INT
    FIELD rcvtrx-ProductDesc    AS CHAR
    FIELD rcvtrx-PchaseValMYR   AS DEC
    FIELD rcvtrx-GSTValMYR      AS DEC
    FIELD rcvtrx-TaxCode        AS CHAR
    FIELD rcvtrx-FCYCode        AS CHAR
    FIELD rcvtrx-PchaseFCY      AS INT
    FIELD rcvtrx-GSTFCY         AS INT
    FIELD rcvtrx-Artnr          AS INT.


DEF TEMP-TABLE t-supplier
    FIELD suppID                AS INT
    FIELD suppName              AS CHAR
    FIELD suppBRN               AS INT
    FIELD suppDateGST           AS DATE
    FIELD suppGSTno             AS INT
    FIELD suppAddr1             AS CHAR
    FIELD suppAddr2             AS CHAR
    FIELD suppTlp               AS CHAR
    FIELD suppFax               AS CHAR
    FIELD suppEmail             AS CHAR
    FIELD suppWebsite           AS CHAR.

DEF TEMP-TABLE t-customer
    FIELD custID                AS INT
    FIELD custName              AS CHAR
    FIELD custBRN               AS INT
    FIELD custInvDate           AS DATE
    FIELD custInvNo             AS INT
    FIELD custLineNo            AS INT
    FIELD custDesc              AS CHAR
    FIELD custSuppValMYR        AS DEC
    FIELD custGSTValMYR         AS DEC
    FIELD custTaxCode           AS CHAR
    FIELD custCountry           AS CHAR
    FIELD custFCYCode           AS CHAR
    FIELD custSuppFCY           AS DEC
    FIELD custGSTFCY            AS DEC.
    

DEF TEMP-TABLE t-gl-trx
    FIELD gltrx-TrxDate         AS DATE
    FIELD gltrx-AccountID       AS CHAR
    FIELD gltrx-AccountName     AS CHAR
    FIELD gltrx-TrxDesc         AS CHAR
    FIELD gltrx-Name            AS CHAR
    FIELD gltrx-TrxID           AS INT
    FIELD gltrx-SrcDocumentID   AS CHAR
    FIELD gltrx-SrcType         AS CHAR
    FIELD gltrx-Debit           AS DEC
    FIELD gltrx-Credit          AS DEC
    FIELD gltrx-Balance         AS DEC.
DEF TEMP-TABLE t-gl
    FIELD glID          AS CHAR
    FIELD glAccName     AS CHAR
    FIELD glAccType     AS INT
    FIELD glDebit       AS DECIMAL
    FIELD glCredit      AS DECIMAL.

DEF INPUT  PARAMETER fdate      AS DATE.
DEF INPUT  PARAMETER tdate      AS DATE.
DEF INPUT  PARAMETER sorttype   AS INT.
DEF OUTPUT PARAMETER done       AS LOGICAL INIT YES.
DEF OUTPUT PARAMETER TABLE FOR t-supplier.
DEF OUTPUT PARAMETER TABLE FOR t-customer.
DEF OUTPUT PARAMETER TABLE FOR t-gl.
DEF OUTPUT PARAMETER TABLE FOR t-rcv-trx.
DEF OUTPUT PARAMETER TABLE FOR t-gl-trx.

DEF VAR a AS INT.
DEF VAR b AS CHAR.
/*supplier files*/
FOR EACH l-op WHERE l-op.datum GE fdate AND l-op.datum LE tdate
    AND l-op.lief-nr GT 0
    AND l-op.loeschflag LE 1
    AND l-op.op-art = 1
    NO-LOCK USE-INDEX lief_ix,
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr
    /*AND l-artikel.endkum GE from-grp
    AND l-artikel.endkum LE to-grp*/
    NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK
    BY l-lieferant.firma BY l-op.datum BY l-artikel.bezeich:
    IF l-artikel.lief-artnr[3] EQ "" THEN
    DO:
        done = NO.
        RETURN.
    END.
    CREATE t-supplier.
    ASSIGN
        t-supplier.suppID        = l-lieferant.lief-nr
        t-supplier.suppName      = l-lieferant.firma
        t-supplier.suppDateGST   = 01/01/99
        t-supplier.suppGSTno     = 9999999
        t-supplier.suppAddr1     = l-lieferant.adresse1
        t-supplier.suppAddr2     = l-lieferant.adresse2
        t-supplier.suppTlp       = telefon
        t-supplier.suppFax       = fax
        t-supplier.suppEmail     = "aaa@aa.com"
        t-supplier.suppWebsite   = "www.aaa.com"
        .
    IF l-lieferant.notizen[1] MATCHES ("*" + "#BRN*" + "*") THEN
    DO:
        a = LENGTH(TRIM(ENTRY(2, l-lieferant.notizen[1], "#BRN"))).
        b = TRIM(ENTRY(2, l-lieferant.notizen[1], "#BRN")).
        t-supplier.suppBRN = INT(SUBSTR(b, 4, a - 3)).
    END.
    ELSE t-supplier.suppBRN      = 9999.

    CREATE t-rcv-trx.
    ASSIGN
        t-rcv-trx.rcvtrx-suppName       = l-lieferant.firma
        t-rcv-trx.rcvtrx-suppBRN        = t-supplier.suppBRN
        t-rcv-trx.rcvtrx-invoiceDate    = l-op.datum
        t-rcv-trx.rcvtrx-invoiceNumber  = l-op.docu-nr
        t-rcv-trx.rcvtrx-importDecNo    = 999
        t-rcv-trx.rcvtrx-LineNumber     = l-op.pos
        t-rcv-trx.rcvtrx-ProductDesc    = l-artikel.bezeich
        t-rcv-trx.rcvtrx-PchaseValMYR   = 999
        t-rcv-trx.rcvtrx-GSTValMYR      = 999
        t-rcv-trx.rcvtrx-TaxCode        = l-artikel.lief-artnr[3]
        t-rcv-trx.rcvtrx-FCYCode        = ""
        t-rcv-trx.rcvtrx-PchaseFCY      = 0
        t-rcv-trx.rcvtrx-GSTFCY         = 0
        t-rcv-trx.rcvtrx-PchaseValMYR   = l-op.warenwert
        t-rcv-trx.rcvtrx-Artnr          = l-artikel.artnr.
END.
/*
FOR EACH l-lieferant NO-LOCK:
    CREATE t-supplier.
    ASSIGN
        t-supplier.suppID        = l-lieferant.lief-nr
        t-supplier.suppName      = l-lieferant.firma
        t-supplier.suppBRN       = 999
        t-supplier.suppDateGST   = 01/01/99
        t-supplier.suppGSTno     = 9999999
        t-supplier.suppAddr1     = l-lieferant.adresse1
        t-supplier.suppAddr2     = l-lieferant.adresse2
        t-supplier.suppTlp       = telefon
        t-supplier.suppFax       = fax
        t-supplier.suppEmail     = "aaa@aa.com"
        t-supplier.suppWebsite   = "www.aaa.com".
END.
*/

/*customer files*/
RUN generate-gst-fobillbl.p(fdate,tdate, OUTPUT TABLE t-customer).
FIND FIRST t-customer.
/*FOR EACH guest NO-LOCK:
    CREATE t-customer.
    ASSIGN
        t-customer.custID        = guest.gastnr
        t-customer.custName      = guest.NAME
        t-customer.custBRN       = 999
        t-customer.custDateGST   = 01/01/99
        t-customer.custGSTno     = 9999999
        t-customer.custAddr1     = guest.adresse1
        t-customer.custAddr2     = guest.adresse2
        t-customer.custTlp       = guest.telex
        t-customer.custFax       = guest.fax
        t-customer.custEmail     = guest.email-adr
        t-customer.custWebsite   = "xxx.xxx.com".
END.*/

/*G/L files*/
FOR EACH gl-acct NO-LOCK:
    CREATE t-gl.
    ASSIGN
        t-gl.glID          = gl-acct.fibukonto
        t-gl.glAccName     = gl-acct.bezeich
        t-gl.glAccType     = gl-acct.acc-type
        t-gl.glDebit       = gl-acct.debit[1]
        t-gl.glCredit      = gl-acct.credit[1].
END.
FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE fdate
    AND gl-jouhdr.datum LE tdate NO-LOCK BY gl-jouhdr.datum:
    FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr,
        FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto,
        FIRST gl-fstype WHERE gl-fstype.nr = gl-acct.fs-type
        NO-LOCK BY gl-journal.fibukonto:
        CREATE t-gl-trx.
        ASSIGN
            t-gl-trx.gltrx-TrxDate         = gl-jouhdr.datum
            t-gl-trx.gltrx-AccountID       = gl-journal.fibukonto
            t-gl-trx.gltrx-AccountName     = gl-acct.bezeich
            t-gl-trx.gltrx-TrxDesc         = gl-jouhdr.bezeich
            t-gl-trx.gltrx-Name            = gl-jouhdr.bezeich
            t-gl-trx.gltrx-TrxID           = gl-journal.jnr
            t-gl-trx.gltrx-SrcDocumentID   = gl-jouhdr.refno
            t-gl-trx.gltrx-SrcType         = gl-fstype.bezeich
            t-gl-trx.gltrx-Debit           = gl-journal.debit
            t-gl-trx.gltrx-Credit          = gl-journal.credit
            t-gl-trx.gltrx-Balance         = gl-journal.debit - gl-journal.credit.
    END.
END.

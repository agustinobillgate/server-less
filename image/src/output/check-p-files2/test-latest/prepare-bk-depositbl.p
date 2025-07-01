DEFINE TEMP-TABLE t-artikel LIKE artikel.

DEFINE TEMP-TABLE t-bk-deposit
    FIELD blockId       AS CHARACTER
    FIELD deposit       AS DECIMAL
    FIELD limitDate     AS DATE
    FIELD totalPaid     AS DECIMAL
    FIELD totalRefund   AS DECIMAL
    FIELD gastNr        AS INTEGER.

DEFINE TEMP-TABLE t-bk-deposit-line
    FIELD blockId           AS CHARACTER
    FIELD nr                AS INTEGER
    FIELD paymentAmount     AS DECIMAL
    FIELD paymentArtnr      AS INTEGER
    FIELD paymentUserInit   AS CHARACTER
    FIELD paymentDate       AS DATE
    FIELD paymentType       AS INTEGER /* 0 = Deposit | 1 = Payment | 2 = Refund */
    FIELD voucherNo         AS CHARACTER.

/**/
DEFINE INPUT PARAMETER blockId      AS CHARACTER.
/*DEFINE OUTPUT PARAMETER guestName   AS CHARACTER.*/
DEFINE OUTPUT PARAMETER TABLE FOR t-bk-deposit.
DEFINE OUTPUT PARAMETER TABLE FOR t-bk-deposit-line.
DEFINE OUTPUT PARAMETER TABLE FOR t-artikel.
/**/

/*
DEFINE VARIABLE depositAmount       AS DECIMAL      NO-UNDO.
DEFINE VARIABLE refund              AS DECIMAL      NO-UNDO.
*/
/*
FIND FIRST bk-master WHERE bk-master.block-id EQ blockID NO-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN
DO:
    guestName   = bk-master.name.
END.
*/
FIND FIRST bk-deposit WHERE bk-deposit.blockId EQ blockId NO-LOCK NO-ERROR.
IF AVAILABLE bk-deposit THEN
DO:
    CREATE t-bk-deposit.
    BUFFER-COPY bk-deposit TO t-bk-deposit.
END.

FOR EACH bk-deposit-line WHERE bk-deposit-line.blockId EQ blockId NO-LOCK:
    CREATE t-bk-deposit-line.
    BUFFER-COPY bk-deposit-line TO t-bk-deposit-line.
END.

FOR EACH artikel WHERE (artikel.artart EQ 6 OR artikel.artart EQ 7) NO-LOCK:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
END.

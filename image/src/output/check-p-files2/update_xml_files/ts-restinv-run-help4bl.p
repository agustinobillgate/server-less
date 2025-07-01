DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-h-artikel1 LIKE h-artikel
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-h-bill-tmp LIKE t-h-bill.

DEFINE INPUT-OUTPUT PARAMETER kpr-time  AS INTEGER NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER kpr-recid AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER bill-date        AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER tischnr          AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER curr-dept        AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER amount LIKE vhp.bill-line.betrag.

DEFINE OUTPUT PARAMETER fl-code AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-h-bill-tmp.
DEFINE OUTPUT PARAMETER TABLE FOR t-h-artikel1.
DEFINE OUTPUT PARAMETER TABLE FOR t-h-bill.

RUN ts-restinv-run-helpbl.p (INPUT-OUTPUT kpr-time,
    INPUT-OUTPUT kpr-recid, bill-date, tischnr, curr-dept,
    amount, OUTPUT fl-code, OUTPUT TABLE t-h-artikel1,
    OUTPUT TABLE t-h-bill).

/*Eko 07 Jun 2016, Checking Table already opened with active bill or not*/ 
EMPTY TEMP-TABLE t-h-bill-tmp NO-ERROR.
RUN ts-restinv-run-help-check-billbl.p (3, tischnr, curr-dept, OUTPUT TABLE t-h-bill-tmp).


DEFINE TEMP-TABLE b1-list
    FIELD resnr         LIKE bill.resnr
    FIELD rechnr        LIKE bill.rechnr
    FIELD name          LIKE guest.name
    FIELD vorname1      LIKE guest.vorname1
    FIELD anrede1       LIKE guest.anrede1
    FIELD saldo         LIKE bill.saldo
    FIELD printnr       LIKE bill.printnr
    FIELD datum         LIKE bill.datum
    FIELD b-recid       AS INTEGER
    FIELD adresse1      LIKE guest.adresse1
    FIELD wohnort       LIKE guest.wohnort
    FIELD bemerk        LIKE guest.bemerkung
    FIELD plz           LIKE guest.plz
    FIELD bill-datum    AS DATE
    FIELD qr-code       AS CHARACTER
    .
DEFINE TEMP-TABLE temp-list LIKE b1-list.

DEFINE INPUT PARAMETER dept AS INTEGER.
DEFINE INPUT PARAMETER qr-code AS CHARACTER.
DEFINE INPUT PARAMETER bill-recid AS INTEGER.
DEFINE OUTPUT PARAMETER ok-flag AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER msg-int AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR temp-list.

DEFINE VARIABLE found-sameqr AS LOGICAL.
DEFINE VARIABLE invalid-code AS LOGICAL.
DEFINE VARIABLE transaction-exist AS LOGICAL.

DEFINE BUFFER buf-bill FOR bill.

IF qr-code EQ ? THEN qr-code = "".

FOR EACH buf-bill WHERE buf-bill.flag EQ 0 
    AND buf-bill.resnr EQ 0 AND buf-bill.reslinnr EQ 1 
    AND buf-bill.rechnr GT 0 /*AND buf-bill.billtyp EQ dept*/ NO-LOCK:

    IF buf-bill.vesrdepot2 NE "" AND buf-bill.vesrdepot2 EQ qr-code THEN
    DO:
        found-sameqr = YES.
        LEAVE.
    END.
END.
IF found-sameqr THEN
DO:
    msg-int = 1.
    RETURN.
END.    

IF qr-code NE "" THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 248 AND queasy.char2 EQ qr-code NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        invalid-code = YES.
    END.
    IF invalid-code THEN
    DO:
        msg-int = 2.
        RETURN.
    END.
END.

IF qr-code EQ "" OR qr-code EQ ? THEN
DO:
    FIND FIRST buf-bill WHERE RECID(buf-bill) EQ bill-recid AND buf-bill.flag EQ 0 
        AND buf-bill.resnr EQ 0 AND buf-bill.reslinnr EQ 1 
        AND buf-bill.rechnr GT 0 AND buf-bill.vesrdepot2 NE "" NO-LOCK NO-ERROR.
    IF AVAILABLE buf-bill THEN
    DO:
        FIND FIRST bill-line WHERE bill-line.rechnr EQ buf-bill.rechnr NO-LOCK NO-ERROR.
        IF AVAILABLE bill-line THEN
        DO:
            msg-int = 3.
            RETURN.
        END.
    END.
END.
/*
FIND FIRST buf-bill WHERE RECID(buf-bill) EQ bill-recid AND buf-bill.flag EQ 0 
    AND buf-bill.resnr EQ 0 AND buf-bill.reslinnr EQ 1 
    AND buf-bill.rechnr GT 0 AND buf-bill.vesrdepot2 NE "" NO-LOCK NO-ERROR.
IF AVAILABLE buf-bill THEN
DO:
    FIND FIRST bill-line WHERE bill-line.rechnr EQ buf-bill.rechnr NO-LOCK NO-ERROR.
    IF AVAILABLE bill-line THEN
    DO:
        msg-int = 3.
        RETURN.
    END.
END.
*/
FIND FIRST bill WHERE RECID(bill) EQ bill-recid NO-LOCK NO-ERROR.
IF AVAILABLE bill THEN
DO:
    FIND CURRENT bill EXCLUSIVE-LOCK.
    bill.vesrdepot2 = qr-code.
    
    CREATE temp-list.
    ASSIGN
        temp-list.resnr     = bill.resnr
        temp-list.rechnr    = bill.rechnr
        temp-list.saldo     = bill.saldo
        temp-list.printnr   = bill.printnr
        temp-list.datum     = bill.datum
        temp-list.b-recid   = RECID(bill)
        temp-list.qr-code   = bill.vesrdepot2
        .

    FIND FIRST guest WHERE guest.gastnr EQ bill.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
        ASSIGN
            temp-list.name      = guest.NAME
            temp-list.vorname1  = guest.vorname1
            temp-list.anrede1   = guest.anrede1
            temp-list.adresse1  = guest.adresse1
            temp-list.wohnort   = guest.wohnort
            temp-list.bemerk    = guest.bemerkung
            temp-list.plz       = guest.plz
            .
    END.

    FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr NO-LOCK NO-ERROR.
    IF AVAILABLE bill-line THEN
    DO:
        temp-list.bill-datum = bill-line.bill-datum.
    END.

    FIND CURRENT bill NO-LOCK.
    RELEASE bill.

    ok-flag = YES.
END.



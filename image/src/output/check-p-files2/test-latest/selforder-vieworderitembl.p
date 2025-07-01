
DEFINE TEMP-TABLE selected-menu
  FIELD rec-id          AS INTEGER
  FIELD article-name    AS CHARACTER
  FIELD quantity        AS INTEGER
  FIELD price           AS DECIMAL
  FIELD post-date       AS DATE
  FIELD post-time       AS CHARACTER
  FIELD tax             AS DECIMAL
  FIELD service         AS DECIMAL
  FIELD subtotal        AS DECIMAL
  FIELD special-req     AS CHARACTER
.

DEFINE INPUT PARAMETER inp-outlet-num   AS INTEGER.
DEFINE INPUT PARAMETER inp-table-num    AS INTEGER.
DEFINE OUTPUT PARAMETER record-id       AS INTEGER.
DEFINE OUTPUT PARAMETER user-init       AS CHARACTER.
DEFINE OUTPUT PARAMETER language-code   AS INTEGER.
DEFINE OUTPUT PARAMETER outlet-number   AS INTEGER.
DEFINE OUTPUT PARAMETER order-number    AS INTEGER.
DEFINE OUTPUT PARAMETER table-number    AS INTEGER.
DEFINE OUTPUT PARAMETER post-datetime   AS CHARACTER.
DEFINE OUTPUT PARAMETER guest-number    AS INTEGER.
DEFINE OUTPUT PARAMETER guest-name      AS CHARACTER.
DEFINE OUTPUT PARAMETER pax             AS INTEGER.
DEFINE OUTPUT PARAMETER room-number     AS CHARACTER.
DEFINE OUTPUT PARAMETER res-number      AS INTEGER.
DEFINE OUTPUT PARAMETER reslin-numnber  AS INTEGER.
DEFINE OUTPUT PARAMETER subtotal        AS DECIMAL.
DEFINE OUTPUT PARAMETER mess-result     AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR selected-menu.
/*
DEFINE VARIABLE inp-outlet-num   AS INTEGER INIT 1.
DEFINE VARIABLE inp-table-num    AS INTEGER INIT 50.
DEFINE VARIABLE  record-id       AS INTEGER.
DEFINE VARIABLE  user-init       AS CHARACTER.
DEFINE VARIABLE  language-code   AS INTEGER.
DEFINE VARIABLE  outlet-number   AS INTEGER.
DEFINE VARIABLE  order-number    AS INTEGER.
DEFINE VARIABLE  table-number    AS INTEGER.
DEFINE VARIABLE  post-datetime   AS CHARACTER.
DEFINE VARIABLE  guest-number    AS INTEGER.
DEFINE VARIABLE  guest-name      AS CHARACTER.
DEFINE VARIABLE  pax             AS INTEGER.
DEFINE VARIABLE  room-number     AS CHARACTER.
DEFINE VARIABLE  res-number      AS INTEGER.
DEFINE VARIABLE  reslin-numnber  AS INTEGER.
DEFINE VARIABLE  mess-result     AS CHARACTER.
DEFINE VARIABLE  subtotal        AS DECIMAL.
*/
/*********************************************************************************************/
FOR EACH selected-menu:
    DELETE selected-menu.
END.

FIND FIRST h-bill WHERE h-bill.departement EQ inp-outlet-num 
    AND h-bill.flag EQ 0 
    AND h-bill.saldo NE 0 
    AND h-bill.tischnr EQ inp-table-num NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    ASSIGN
    record-id       = RECID(h-bill)
    order-number    = h-bill.rechnr
    outlet-number   = inp-outlet-num
    table-number    = inp-table-num
    pax             = h-bill.belegung
    res-number      = h-bill.resnr
    reslin-numnber  = h-bill.reslinnr
    /*language-code*/
    .    
    
    FIND FIRST bediener WHERE bediener.userinit EQ "SO" NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN user-init = bediener.userinit.
    
    FIND FIRST h-bill-line WHERE h-bill-line.rechnr EQ h-bill.rechnr 
        AND h-bill-line.departement EQ h-bill.departement
        AND h-bill-line.tischnr EQ h-bill.tischnr NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill-line THEN post-datetime = STRING(h-bill-line.bill-datum) + " - " + STRING(h-bill-line.zeit, "HH:MM:SS").
    
    IF h-bill.resnr GT 0 THEN
    DO:
        FIND FIRST res-line WHERE res-line.resnr EQ h-bill.resnr
        AND res-line.reslinnr EQ h-bill.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN
        DO:    
            ASSIGN
            guest-number  = res-line.gastnrmember  
            guest-name    = res-line.NAME
            room-number   = res-line.zinr
            .    
        END.
    END.  
    ELSE
    DO:
        ASSIGN
        guest-name    = h-bill.bilname
        room-number   = ""
        .   
    END.
    
    FOR EACH h-bill-line WHERE h-bill-line.rechnr EQ h-bill.rechnr 
        AND h-bill-line.departement EQ h-bill.departement
        AND h-bill-line.tischnr EQ h-bill.tischnr NO-LOCK 
        BY h-bill-line.bill-datum DESC BY h-bill-line.zeit DESC:
        
        CREATE selected-menu.
        ASSIGN
        selected-menu.rec-id        = RECID(h-bill-line) 
        selected-menu.article-name  = h-bill-line.bezeich
        selected-menu.quantity      = h-bill-line.anzahl
        selected-menu.price         = h-bill-line.betrag
        selected-menu.post-date     = h-bill-line.bill-datum
        selected-menu.post-time     = STRING(h-bill-line.zeit, "HH:MM:SS")
        subtotal                    = subtotal + h-bill-line.betrag
        . 
        
        FIND FIRST htparam WHERE htparam.paramnr = 557 NO-LOCK.
        FIND FIRST h-journal WHERE h-journal.artnr = h-bill-line.artnr 
            AND h-journal.departement = h-bill-line.departement
            AND h-journal.rechnr = h-bill-line.rechnr 
            AND h-journal.bill-datum = h-bill-line.bill-datum NO-LOCK NO-ERROR. 
        IF AVAILABLE h-journal AND h-journal.artnr NE htparam.finteger THEN 
        selected-menu.special-req = h-journal.aendertext.
        ELSE selected-menu.special-req = "".
    END.
    mess-result = "Success load data".
END.
ELSE mess-result = "Bill status is closed!".



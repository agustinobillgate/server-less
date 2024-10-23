
DEF INPUT  PARAMETER recid-resline  AS INT.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER t-ankunft      AS DATE.
DEF OUTPUT PARAMETER fl-ok          AS LOGICAL INIT YES.
DEF OUTPUT PARAMETER fl-error       AS INT INIT 0.

DEF VAR p-87 AS DATE.
DEFINE BUFFER resline FOR res-line.
DEFINE VARIABLE orig-status AS INTEGER INITIAL 1    NO-UNDO.
DEFINE VARIABLE room-nr AS CHARACTER INITIAL "" NO-UNDO.
DEFINE VARIABLE priscilla-active AS LOGICAL INITIAL YES NO-UNDO.
DEFINE VARIABLE billnumber AS CHARACTER.
DEFINE VARIABLE res-number AS INTEGER.
DEFINE VARIABLE count-i    AS INTEGER.

DEFINE BUFFER buff-resline FOR res-line.
DEFINE BUFFER mbill FOR bill.

RUN htpdate.p (87, OUTPUT p-87).
IF t-ankunft LT p-87 THEN fl-ok = NO.
IF NOT fl-ok THEN RETURN.

FIND FIRST res-line WHERE RECID(res-line) = recid-resline.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
  
res-number = res-line.resnr.
room-nr = res-line.zinr.
/* SY 01 Sept 2015: FOR EACH instead of FIRST BILL */
FOR EACH bill WHERE bill.resnr = res-line.resnr
    AND bill.parent-nr = res-line.reslinnr NO-LOCK:
    IF (bill.gesamtumsatz NE 0 OR bill.saldo NE 0) THEN 
    DO: 
        fl-error = 1.
        RETURN. 
    END. 
    FIND FIRST bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK NO-ERROR.
    IF AVAILABLE bill-line THEN
    DO:
        fl-error = 2.
        RETURN. 
    END. 
END.


billnumber = "".
FOR EACH bill WHERE bill.resnr EQ res-line.resnr AND bill.parent-nr EQ res-line.reslinnr EXCLUSIVE-LOCK: 
    IF bill.rechnr EQ 0 THEN 
    DO:
        DELETE bill.
        RELEASE bill.
    END.
    ELSE
    DO:
        ASSIGN 
            bill.flag  = 1
            fl-error   = 3 /*Message to UI if Bill Moved To CLose BIll \ MASDOD181120*/
            billnumber = billnumber + ";" + STRING(bill.rechnr)
            .
    END.
END.

/*FDL Feb 09, 2023 => Ticket 883576*/
FOR EACH buff-resline WHERE buff-resline.resnr EQ res-number
    AND buff-resline.resstatus EQ 6 NO-LOCK:
    count-i = count-i + 1.
END.

IF count-i EQ 1 THEN
DO:
    FIND FIRST mbill WHERE mbill.resnr EQ res-number 
        AND mbill.reslinnr EQ 0 AND mbill.saldo NE 0
        AND mbill.zinr EQ "" AND mbill.flag EQ 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE mbill THEN
    DO:
        fl-error = 1.
    END.
END.
/*End FDL*/

CREATE reslin-queasy. 
ASSIGN 
reslin-queasy.key       = "ResChanges" 
reslin-queasy.resnr     = res-line.resnr 
reslin-queasy.reslinnr  = res-line.reslinnr 
reslin-queasy.date2     = TODAY 
reslin-queasy.number2   = TIME 
reslin-queasy.char3 = STRING(res-line.ankunft) + ";" 
                    + STRING(res-line.ankunft) + ";" 
                    + STRING(res-line.abreise) + ";" 
                    + STRING(res-line.abreise) + ";" 
                    + STRING(res-line.zimmeranz) + ";" 
                    + STRING(res-line.zimmeranz) + ";" 
                    + STRING(res-line.erwachs) + ";" 
                    + STRING(res-line.erwachs) + ";" 
                    + STRING(res-line.kind1) + ";" 
                    + STRING(res-line.kind1) + ";" 
                    + STRING(res-line.gratis) + ";" 
                    + STRING(res-line.gratis) + ";" 
                    + STRING(res-line.zikatnr) + ";" 
                    + STRING(res-line.zikatnr) + ";" 
                    + STRING(res-line.zinr) + ";" 
                    + STRING(res-line.zinr) + ";" 
                    + STRING(res-line.arrangement) + ";" 
                    + STRING(res-line.arrangement) + ";"  
                    + STRING(res-line.zipreis) + ";" 
                    + STRING(res-line.zipreis) + ";" 
                    + STRING(user-init) + ";" 
                    + STRING(user-init) + ";" 
                    + STRING(TODAY) + ";" 
                    + STRING(TODAY) + ";" 
                    + STRING(res-line.name) + ";" 
                    + STRING("CANCEL CHECK-IN") + ";" 
                    + STRING(" ") + ";" 
                    + STRING(" ") + ";". 
RELEASE reslin-queasy. 

CREATE res-history. 
ASSIGN 
    res-history.nr          = bediener.nr 
    res-history.resnr       = res-line.resnr
    res-history.reslinnr    = res-line.reslinnr
    res-history.datum       = TODAY 
    res-history.zeit        = TIME 
    res-history.aenderung   = "Cancel C/I Room " + res-line.zinr 
                            + " ResNo " + STRING(res-line.resnr) + " BillNumber " + billnumber 
    /*res-history.action      = "Checkin"*/
    res-history.action      = "Cancel C/I". /*Gerald Key LogFile #660691*/
FIND CURRENT res-history NO-LOCK. 
RELEASE res-history. 

RUN intevent-1.p( 2, res-line.zinr, "Deactivate!;PABX", res-line.resnr, res-line.reslinnr). 

FOR EACH resplan WHERE resplan.zikatnr = res-line.zikatnr AND 
    resplan.datum >= res-line.ankunft AND 
    resplan.datum < res-line.abreise EXCLUSIVE-LOCK: 
    resplan.anzzim[res-line.resstatus] = resplan.anzzim[res-line.resstatus] - 1. 
    resplan.anzzim[1] = resplan.anzzim[1] + 1. 
    RELEASE resplan.
END. /* FOR EACH resplan */ 

FIND FIRST resline WHERE resline.active-flag = 1 
  AND resline.zinr = res-line.zinr
  AND resline.reslinnr NE res-line.reslinnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE resline THEN
DO:
    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
    IF AVAILABLE zimmer THEN
    DO:
      FIND CURRENT zimmer EXCLUSIVE-LOCK.
      zimmer.zistatus = 2. 
      FIND CURRENT zimmer NO-LOCK. 
    END.
    FOR EACH zimplan WHERE zimplan.zinr = res-line.zinr AND 
      zimplan.gastnrmember = res-line.gastnrmember
      AND zimplan.datum GE res-line.ankunft 
      AND zimplan.datum LE (res-line.abreise - 1) EXCLUSIVE-LOCK: 
      DELETE zimplan. 
      RELEASE zimplan.
    END. 
END.

FIND FIRST resline WHERE RECID(resline) = RECID(res-line) EXCLUSIVE-LOCK. 
IF resline.resstatus = 13 THEN orig-status = 11.
ASSIGN 
    resline.zinr = "" 
    resline.resstatus = orig-status
    resline.ankzeit = 0 
    resline.active-flag = 0. 
FIND CURRENT resline NO-LOCK. 

FOR EACH resline WHERE resline.resnr = res-line.resnr
    AND resline.active-flag = 1
    AND resline.l-zuordnung[3] = 1
    AND resline.kontakt-nr = res-line.reslinnr:
    ASSIGN 
      resline.zinr = "" 
      resline.resstatus = 11
      resline.ankzeit = 0 
      resline.active-flag = 0. 
END.


FIND FIRST htparam WHERE htparam.paramnr = 341 NO-LOCK. 
IF htparam.fchar NE "" THEN
DO:
    RUN intevent-1.p( 2, room-nr, "My Checkout!", res-line.resnr, res-line.reslinnr). 
END.

IF priscilla-active THEN
DO:
    RUN intevent-1.p( 9, room-nr, "Priscilla", res-line.resnr, res-line.reslinnr). 
END.


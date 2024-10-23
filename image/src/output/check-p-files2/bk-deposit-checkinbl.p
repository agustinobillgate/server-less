/**/
DEFINE INPUT PARAMETER blockID  AS CHARACTER.
DEFINE INPUT PARAMETER user-init AS CHARACTER.
DEFINE OUTPUT PARAMETER errCode AS INTEGER.
/*
errCode Legend:
1 = Banquet Art Not Setup Yet in paramnr 117
2 = Banquet Department Not Setup Yet in Paramnr 900
*/
/**/

/*
DEFINE VARIABLE blockID         AS CHARACTER    NO-UNDO INITIAL "BQ0000008". /*I*/
DEFINE VARIABLE user-init        AS CHARACTER    NO-UNDO INITIAL "01". /*I*/
DEFINE VARIABLE errCode         AS INTEGER      NO-UNDO. /*O*/
*/

DEFINE VARIABLE billNo          AS INTEGER      NO-UNDO.
DEFINE VARIABLE guestNo         AS INTEGER      NO-UNDO.
DEFINE VARIABLE guestName       AS CHARACTER    NO-UNDO.
DEFINE VARIABLE billDate        AS DATE         NO-UNDO.
DEFINE VARIABLE depositAmount   AS DECIMAL      NO-UNDO.
DEFINE VARIABLE artDeposit      AS INTEGER      NO-UNDO.
DEFINE VARIABLE artDescription  AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bqtDepartment   AS INTEGER      NO-UNDO.

/*GET BILL DATE FROM PARAM 110*/
run htpdate.p(110, OUTPUT billDate).
/******************************************************/  

MESSAGE user-init VIEW-AS ALERT-BOX.

/*GET LAST BILL NO + 1*/
FIND FIRST counters WHERE counters.counter-no EQ 3 EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE counters THEN
DO:
    billNo = counters.counter + 1.
END.
ELSE 
DO:
    billNo = 1.
END.
/******************************************************/  

/*GET BANQUET DEPOSIT ARTICLE*/
FIND FIRST htparam WHERE htparam.paramnr EQ 117 USE-INDEX paramnr_ix NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    artDeposit  = htparam.finteger.
END.
ELSE
DO:
    errCode = 1.
    
    RETURN.
END.
/******************************************************/  

/*GET BANQUET DEPARTMENT*/
FIND FIRST htparam WHERE htparam.paramnr EQ 900 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    bqtDepartment   = htparam.paramnr.
END.
ELSE
DO:
    errCode = 2.
    
    RETURN.
END.
/******************************************************/  

/*GET DEPOSIT AMOUNT*/
FIND FIRST bk-deposit WHERE bk-deposit.blockId EQ blockID NO-LOCK NO-ERROR.
IF AVAILABLE bk-deposit THEN
DO:
    depositAmount   = bk-deposit.deposit.
END.
/******************************************************/  

/*GET GUEST NO AND GUEST NAME FROM BK-MASTER*/
FIND FIRST bk-master WHERE bk-master.block-id EQ blockID NO-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN
DO:
    ASSIGN
        guestNo     = bk-master.gastnr
        guestName   = bk-master.name.
END.
/***********************/

/****************UPDATE RESSTATUS**********************/
DEFINE VARIABLE ciStatus    AS INTEGER      NO-UNDO.

FIND FIRST bk-queasy WHERE bk-queasy.key EQ 1
    AND bk-queasy.number2 EQ 5 NO-LOCK NO-ERROR.
IF AVAILABLE bk-queasy THEN
DO:
    ciStatus = bk-queasy.number1.
END.

FIND FIRST bk-master WHERE bk-master.block-id EQ blockID EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN
DO:
    ASSIGN
        bk-master.resstatus = ciStatus.
    RELEASE bk-master.    
    
    errCode = 0.
END.
/******************************************************/

FIND FIRST bk-deposit WHERE bk-deposit.blockId EQ blockId NO-LOCK NO-ERROR.
IF NOT AVAILABLE bk-deposit THEN
DO:
    errCode = 99.
    
    RETURN.
END.

/*UPDATE LAST BILLNO TO CURRENT BILLNO*/
ASSIGN
    counters.counter = billNo.
/******************************************************/  

/*********************CREATE NS BILL******************/
CREATE bill.
ASSIGN
  bill.resnr        = 0
  bill.zinr         = ""
  bill.reslinnr     = 1
  bill.rgdruck      = 1 
  bill.billtyp      = 0
  bill.rechnr       = billNo
  bill.gastnr       = guestNo
  bill.datum        = billDate
  bill.name         = guestName
  bill.vesrdepot    = blockID
  bill.saldo        = - depositAmount
  bill.gesamtumsatz = - depositAmount
  bill.logisumsatz  = - depositAmount
  bill.bilname      = guestName.
/******************************************************/  

/**************CREATE BILL-LINE***********************/
FIND FIRST artikel WHERE artikel.artnr EQ artDeposit NO-LOCK NO-ERROR.
IF AVAILABLE artikel THEN
DO:
    artDescription = artikel.bezeich. 
END.

CREATE bill-line. 
ASSIGN
  bill-line.rechnr      = billNo
  bill-line.artnr       = artDeposit
  bill-line.bezeich     = artDescription
  bill-line.anzahl      = 1
  bill-line.betrag      = - depositAmount 
  bill-line.zeit        = TIME
  bill-line.userinit    = user-init
  bill-line.zinr        = ""
  bill-line.massnr      = 0
  bill-line.billin-nr   = 0
  bill-line.bill-datum  = billDate. 
/******************************************************/   

/***************CREATE BILLJOURNAL*********************/
FIND FIRST artikel WHERE artikel.artnr EQ artDeposit NO-LOCK NO-ERROR.
IF AVAILABLE artikel THEN
DO:              
    CREATE billjournal.
    ASSIGN
        billjournal.artnr           = artDeposit
        billjournal.rechnr          = billNo
        billjournal.departement     = artikel.departement
        billjournal.billjou-ref     = artikel.artnr
        billjournal.anzahl          = 1
        billjournal.betrag          = - depositAmount
        billjournal.bezeich         = artDescription + " [CheckIn#" + blockId + "]" + "/" + ""
        billjournal.epreis          = 0
        billjournal.zeit            = TIME
        billjournal.userinit        = user-init
        billjournal.bill-datum      = billDate.
          
END.
/******************************************************/

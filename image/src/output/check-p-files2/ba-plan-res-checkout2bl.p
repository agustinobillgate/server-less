
DEF INPUT  PARAMETER mainres-recid  AS INT.
DEF INPUT  PARAMETER t-resnr        AS INT.
DEF INPUT  PARAMETER t-reslinnr     AS INT.
DEF INPUT  PARAMETER user-init      AS CHAR.

DEFINE BUFFER resline    FOR bk-reser.
DEFINE BUFFER bk-resline FOR bk-reser. 
DEFINE BUFFER mainres    FOR bk-veran.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 

FIND FIRST resline WHERE resline.veran-nr = t-resnr 
  AND resline.veran-resnr = t-reslinnr NO-LOCK NO-ERROR. 
FIND FIRST mainres WHERE RECID(mainres) = mainres-recid NO-LOCK.
FIND FIRST bill WHERE bill.rechnr = mainres.rechnr NO-LOCK NO-ERROR. 

DO TRANSACTION: 
    FIND CURRENT mainres EXCLUSIVE-LOCK. 
    mainres.activeflag = 1. 
    FIND CURRENT mainres NO-LOCK. 

    FIND FIRST bk-resline WHERE bk-resline.veran-nr = resline.veran-nr 
      AND bk-resline.resstatus = 1 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE bk-resline: 
        FIND CURRENT bk-resline EXCLUSIVE-LOCK. 
        bk-resline.resstatus = 8. 
        FIND CURRENT bk-resline NO-LOCK. 
        FIND NEXT bk-resline WHERE bk-resline.veran-nr = resline.veran-nr 
          AND bk-resline.resstatus = 1 NO-LOCK NO-ERROR. 
    END. 

    FIND FIRST bk-func WHERE bk-func.veran-nr = resline.veran-nr 
      AND bk-func.resstatus = 1 NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE bk-func: 
        RUN create-bahistory. 
        FIND CURRENT bk-func EXCLUSIVE-LOCK. 
        ASSIGN 
          bk-func.resstatus = 8 
          bk-func.c-resstatus[1] = "I" 
          bk-func.r-resstatus[1] = 8 
        . 
        FIND CURRENT bk-func NO-LOCK. 

        FIND NEXT bk-func WHERE bk-func.veran-nr = resline.veran-nr 
          AND bk-func.resstatus = 1 NO-LOCK NO-ERROR. 
    END. 

    IF mainres.rechnr > 0 THEN 
    DO: 
        FIND CURRENT bill EXCLUSIVE-LOCK. 
        ASSIGN 
          bill.flag = 1 
          bill.datum = ci-date 
          bill.vesrcod = user-init 
        . 
        FIND CURRENT bill NO-LOCK. 
    END. 
END. 

/*ITA 270614*/
PROCEDURE create-bahistory: 
  CREATE b-history. 
  BUFFER-COPY bk-func TO b-history. 
  ASSIGN 
    b-history.deposit = mainres.deposit 
    b-history.limit-date          = mainres.limit-date 
    b-history.segmentcode         = mainres.segmentcode  
    b-history.deposit-payment[1]  = mainres.deposit-payment[1] 
    b-history.deposit-payment[2]  = mainres.deposit-payment[2] 
    b-history.deposit-payment[3]  = mainres.deposit-payment[3] 
    b-history.deposit-payment[4]  = mainres.deposit-payment[4] 
    b-history.deposit-payment[5]  = mainres.deposit-payment[5] 
    b-history.deposit-payment[6]  = mainres.deposit-payment[6] 
    b-history.deposit-payment[7]  = mainres.deposit-payment[7] 
    b-history.deposit-payment[8]  = mainres.deposit-payment[8] 
    b-history.deposit-payment[9]  = mainres.deposit-payment[9] 
    b-history.payment-date[1]     = mainres.payment-date[1] 
    b-history.payment-date[2]     = mainres.payment-date[2] 
    b-history.payment-date[3]     = mainres.payment-date[3] 
    b-history.payment-date[4]     = mainres.payment-date[4] 
    b-history.payment-date[5]     = mainres.payment-date[5] 
    b-history.payment-date[6]     = mainres.payment-date[6] 
    b-history.payment-date[7]     = mainres.payment-date[7] 
    b-history.payment-date[8]     = mainres.payment-date[8] 
    b-history.payment-date[9]     = mainres.payment-date[9] 
    b-history.payment-userinit[1] = mainres.payment-userinit[1] 
    b-history.payment-userinit[2] = mainres.payment-userinit[2] 
    b-history.payment-userinit[3] = mainres.payment-userinit[3] 
    b-history.payment-userinit[4] = mainres.payment-userinit[4] 
    b-history.payment-userinit[5] = mainres.payment-userinit[5] 
    b-history.payment-userinit[6] = mainres.payment-userinit[6] 
    b-history.payment-userinit[7] = mainres.payment-userinit[7] 
    b-history.payment-userinit[8] = mainres.payment-userinit[8] 
    b-history.payment-userinit[9] = mainres.payment-userinit[9] 
    b-history.total-paid          = mainres.total-paid 
  . 
  FIND CURRENT b-history NO-LOCK. 
  RELEASE b-history. 
END. 

DEF TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INT.

DEF INPUT PARAMETER multi-cash AS LOGICAL.
DEF INPUT PARAMETER cash-artno AS INT.
DEF INPUT PARAMETER cash-foreign AS LOGICAL.
DEF INPUT PARAMETER pay-voucher AS LOGICAL.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER voucher-nr AS CHAR.
DEF INPUT PARAMETER amount AS DECIMAL.

DEF OUTPUT PARAMETER billart AS INT.
DEF OUTPUT PARAMETER qty AS DECIMAL.
DEF OUTPUT PARAMETER description AS CHAR.
DEF OUTPUT PARAMETER p-88 AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.

DEFINE VARIABLE local-curr-code AS CHARACTER.

FIND FIRST htparam WHERE htparam.paramnr EQ 152 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN local-curr-code = htparam.fchar.

  IF multi-cash AND cash-artno NE 0 THEN billart = cash-artno. 
  ELSE 
  DO: 
    IF cash-foreign THEN 
      FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 854 NO-LOCK. 
    ELSE 
    DO: 
      IF NOT pay-voucher THEN 
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 855 NO-LOCK. 
      ELSE FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 1001 NO-LOCK. 
    END. 
    billart = vhp.htparam.finteger. 
  END. 

  FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = curr-dept 
    AND vhp.h-artikel.artnr = billart NO-LOCK. 

  qty = 1. 
  description = vhp.h-artikel.bezeich. 
  IF voucher-nr NE "" AND voucher-nr NE "0" THEN DESCRIPTION = DESCRIPTION + " " + voucher-nr.  

  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 88 NO-LOCK.
  p-88 = vhp.htparam.flogical.

  CREATE t-h-artikel.
  BUFFER-COPY h-artikel TO t-h-artikel.
  ASSIGN t-h-artikel.rec-id = RECID(h-artikel).

  IF local-curr-code NE "Rp" THEN
  DO:
    description = "Cash" + " " + local-curr-code. 
    IF voucher-nr NE "" AND voucher-nr NE "0" THEN DESCRIPTION = DESCRIPTION + " " + voucher-nr.

    t-h-artikel.bezeich = "Cash" + " " + local-curr-code.
  END.
  /*MT
  IF amount NE 0 THEN 
  DO: 
    RUN update-bill(h-artikel.artart, vhp.h-artikel.artnrfront). 
  END. 

  answer = NO. 
  IF full-paid THEN 
  DO: 
    answer = NO. 
    IF must-print THEN 
    DO: 
      HIDE MESSAGE NO-PAUSE. 
      answer = YES. 
      MESSAGE translateExtended ("Print the bill?",lvCAREA,"") VIEW-AS ALERT-BOX QUESTION 
      BUTTONS YES-NO UPDATE answer. 
    END. 
    IF answer THEN 
    DO: 
      IF double-currency THEN 
        RUN print-hbill2c.p(NO, curr-printer, RECID(vhp.h-bill), 
          changed-foreign, changed). 
      ELSE
      DO curr-num = 1 TO copy-num:     
        IF copy-num = 1 THEN 
          RUN print-hbill1.p(NO, curr-printer, RECID(vhp.h-bill)). 
        ELSE RUN print-hbill1.p(YES, curr-printer, RECID(vhp.h-bill)). 
      END.
      RUN del-queasy. 
    END.

    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 88 NO-LOCK.
    IF vhp.htparam.flogical THEN
    DO:
      HIDE MESSAGE NO-PAUSE. 
      answer = YES. 
      MESSAGE translateExtended ("Print the OFFICIAL INVOICE?",lvCAREA,"") VIEW-AS ALERT-BOX QUESTION 
      BUTTONS YES-NO UPDATE answer. 
      IF answer THEN 
      RUN print-hbill88.p(0, curr-printer, RECID(vhp.h-bill)). 
    END.
  END. 

  IF full-paid AND amt NE 0 THEN 
  DO: 
    add-zeit = 1. 
    IF double-currency THEN 
    DO: 
      IF NOT cash-foreign THEN 
      DO: 
        amount = - amt. /* change */ 
        amount-foreign = - amt-foreign. 
        change-str = translateExtended ("(Change)",lvCAREA,""). 
        RUN update-bill(h-artikel.artart, vhp.h-artikel.artnrfront). 
      END. 
      ELSE 
      DO: 
        IF changed-foreign NE 0 THEN 
        DO: 
          change-str = translateExtended ("(Change)",lvCAREA,""). 
          amount-foreign = changed-foreign. 
          amount = ROUND(amount-foreign * exrate, 0). 
          RUN update-bill(h-artikel.artart, vhp.h-artikel.artnrfront). 
        END. 
        IF changed NE 0 THEN 
        DO: 
          change-str = translateExtended ("(Change)",lvCAREA,""). 
          cash-foreign = NO. 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 855 NO-LOCK. 
          /* cash local currency */ 
          FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement 
            = curr-dept 
          AND vhp.h-artikel.artnr = vhp.htparam.finteger NO-LOCK. 
          billart = vhp.h-artikel.artnr. 
          qty = 1. 
          description = vhp.h-artikel.bezeich. 
          amount = changed. 
          amount-foreign = ROUND(amount / exchg-rate, 2). 
          RUN update-bill(h-artikel.artart, vhp.h-artikel.artnrfront). 
        END. 
      END. 
    END. /* IF doucble currency */ 

    ELSE DO: 
      IF multi-cash THEN 
      DO: 
        IF changed NE 0 THEN 
        DO: 
          amount = changed. 
          amount-foreign = changed-foreign. 
          change-str = translateExtended ("(Change)",lvCAREA,""). 
          RUN update-bill(h-artikel.artart, vhp.h-artikel.artnrfront). 
        END. 
        IF lchange NE 0 THEN 
        DO: 
          add-zeit = add-zeit + 1. 
          amount = lchange. 
          amount-foreign = lchange. 
          change-str = translateExtended ("(Change)",lvCAREA,""). 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 855 NO-LOCK. 
          billart = vhp.htparam.finteger. 
          FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = curr-dept 
            AND vhp.h-artikel.artnr = billart NO-LOCK. 
          description = vhp.h-artikel.bezeich. 
          change-str = translateExtended ("(Change)",lvCAREA,""). 
          RUN update-bill(h-artikel.artart, vhp.h-artikel.artnrfront). 
        END. 
      END. 
      ELSE 
      DO: 
        amount = - amt. /* change */ 
        amount-foreign = - amt-foreign. 
        change-str = translateExtended ("(Change)",lvCAREA,""). 
       RUN update-bill(h-artikel.artart, vhp.h-artikel.artnrfront). 
      END. 
    END. 
  END. 

  add-zeit = 0. 

  IF full-paid THEN 
  DO: 
    RUN fill-cover. 
    DO TRANSACTION: 
      FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
      vhp.h-bill.flag = 1. 
      FIND CURRENT vhp.h-bill NO-LOCK. 
    END. 
    RUN clear-bill-display. 
    APPLY "entry" TO  tischnr IN FRAME frame1. 
    RETURN NO-APPLY. 
  END. 
  ELSE 
  DO: 
    printed = "". 
    DISP balance /*printed*/ WITH FRAME frame1. 
    IF double-currency THEN DISP balance-foreign WITH FRAME frame1. 
  END. 
  
  */

DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF INPUT PARAMETER h-bill-recid    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER balance-foreign AS DECIMAL NO-UNDO.
DEF INPUT PARAMETER balance         AS DECIMAL NO-UNDO.
DEF INPUT PARAMETER transf-str      AS CHAR    NO-UNDO.

DEF OUTPUT PARAMETER billart        AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER qty            AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER price          AS DECIMAL NO-UNDO.
DEF OUTPUT PARAMETER amount-foreign AS DECIMAL NO-UNDO.
DEF OUTPUT PARAMETER amount         AS DECIMAL NO-UNDO.
DEF OUTPUT PARAMETER gname          AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER desc-str       AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER transfer-zinr  AS CHAR    NO-UNDO INIT "".
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

  FIND FIRST h-bill WHERE RECID(h-bill) = h-bill-recid.
  ASSIGN
      billart        = 0 
      qty            = 1 
      price          = 0 
      amount-foreign = - balance-foreign 
      amount         = - balance 
      gname          = ""
      desc-str       = transf-str 
      gname          = transf-str
      transfer-zinr  = ENTRY(2, ENTRY(1, transf-str, "*"), " ") 
  .
  FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
  ASSIGN 
      vhp.h-bill.bilname = gname
      vhp.h-bill.flag    = 1
  . 
  FIND CURRENT vhp.h-bill NO-LOCK. 
    
  CREATE t-h-bill.
  BUFFER-COPY h-bill TO t-h-bill.
  ASSIGN t-h-bill.rec-id = RECID(h-bill).

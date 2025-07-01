DEFINE TEMP-TABLE inv-list
    FIELD s-recid       AS INTEGER
    FIELD reihenfolge   AS INTEGER FORMAT ">9" LABEL "No"
    FIELD amount        AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Amount"
    FIELD remark        AS CHAR FORMAT "x(28)" LABEL "Remark"
    FIELD inv-AcctNo    LIKE gl-acct.fibukonto
    FIELD inv-bezeich   AS CHAR FORMAT "x(28)" LABEL "Description" 
    FIELD supplier      AS CHAR FORMAT "x(28)" LABEL "Supplier"
    FIELD invNo         AS CHAR FORMAT "x(12)" LABEL "Invoice"
    FIELD created       AS DATE
    FIELD zeit          AS INTEGER
.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER inv-acctNo     AS CHAR.
DEF INPUT  PARAMETER invoice-amt    AS DECIMAL.
DEF INPUT  PARAMETER pbuff-docu-nr  AS CHAR.
DEF INPUT  PARAMETER PI-liefnr      AS INT.
DEF INPUT  PARAMETER invoice-nr     AS CHAR.
DEF INPUT  PARAMETER inv-bezeich    AS CHAR.
DEF INPUT  PARAMETER inv-bemerk     AS CHAR.
DEF INPUT  PARAMETER supplier       AS CHAR.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR inv-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-gcPI".

FIND FIRST gl-acct WHERE gl-acct.fibukonto = inv-acctNo NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-acct THEN
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("GL Account Number not found.", lvCAREA,"").
END.
ELSE IF invoice-amt = 0 THEN
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("Enter the amount.", lvCAREA,"").
END.
ELSE
DO:
  CREATE gc-PIbline.
  ASSIGN
    gc-PIbline.docu-nr     = pbuff-docu-nr
    gc-PIbline.supplier    = supplier
    gc-PIbline.lief-nr     = PI-liefnr
    gc-PIbline.invoice-nr  = invoice-nr
    gc-PIbline.inv-acctNo  = inv-acctNo
    gc-PIbline.inv-bezeich = inv-bezeich
    gc-PIbline.inv-amount  = invoice-amt
    gc-PIbline.inv-bemerk  = inv-bemerk
    gc-PIbline.created     = TODAY
    gc-PIbline.zeit        = TIME
  .
  CREATE inv-list.
  ASSIGN
      inv-list.supplier    = gc-PIbline.supplier
      inv-list.inv-acctNo  = gc-PIbline.inv-acctNo
      inv-list.inv-bezeich = gc-PIbline.inv-bezeich
      inv-list.amount      = gc-PIbline.inv-amount
      inv-list.remark      = gc-PIbline.inv-bemerk
      inv-list.invNo       = gc-PIbline.invoice-nr
      inv-list.created     = gc-PIbline.created
      inv-list.zeit        = gc-PIbline.zeit
      inv-list.s-recid     = RECID(gc-PIbline)
  .
END.

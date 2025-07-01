DEF TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEF INPUT PARAMETER TABLE FOR t-l-orderhdr.
DEF INPUT PARAMETER lief-nr     AS INT.
DEF INPUT PARAMETER docu-nr     AS CHAR.
DEF INPUT PARAMETER pr          AS CHAR.
DEF INPUT PARAMETER curr-liefnr AS INT.

DEF VARIABLE globaldisc AS DECIMAL NO-UNDO INIT 0.

FIND FIRST t-l-orderhdr.
FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = t-l-orderhdr.rec-id
    EXCLUSIVE-LOCK.

IF NUM-ENTRIES(t-l-orderhdr.lief-fax[3],CHR(2)) GT 1 THEN
ASSIGN 
  globaldisc = DECIMAL(ENTRY(2, t-l-orderhdr.lief-fax[3], CHR(2))) / 100
  t-l-orderhdr.lief-fax[3] = ENTRY(1, t-l-orderhdr.lief-fax[3], CHR(2))
.

BUFFER-COPY t-l-orderhdr TO l-orderhdr.
RUN assign-lorder.

PROCEDURE assign-lorder: 
  FIND FIRST l-order WHERE l-order.docu-nr = docu-nr AND 
    l-order.pos = 0 AND l-order.loeschflag = 0 
    AND l-order.lief-nr = curr-liefnr NO-ERROR. 
  IF AVAILABLE l-order THEN
      ASSIGN
        l-order.lief-nr     = lief-nr 
        l-order.lief-fax[1] = pr
        l-order.warenwert   = globaldisc
      . 
  FOR EACH l-order WHERE l-order.docu-nr = docu-nr AND 
    l-order.loeschflag = 0 AND l-order.lief-nr = curr-liefnr: 
    l-order.lief-nr = lief-nr. 
    l-order.betriebsnr = 0. 
  END. 
  IF curr-liefnr NE lief-nr THEN l-orderhdr.lief-nr = lief-nr. 
  FIND CURRENT l-orderhdr NO-LOCK. 
END.  

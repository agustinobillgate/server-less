
DEF INPUT  PARAMETER mat-buff-nr AS INT.
DEF INPUT  PARAMETER recid-fa-artikel AS INT.
DEF INPUT  PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER err-no AS INT INIT 0.

DEFINE BUFFER fa-buff FOR fa-artikel.
DEF VAR last-depn AS DATE NO-UNDO.

FIND FIRST htparam WHERE paramnr = 881 NO-LOCK.
last-depn = htparam.fdate.

FIND FIRST fa-artikel WHERE RECID(fa-artikel) = recid-fa-artikel NO-LOCK.
FIND FIRST fa-op WHERE fa-op.opart = 4 AND fa-op.nr = mat-buff-nr
    AND fa-op.datum = fa-artikel.deleted NO-LOCK .
IF fa-op.datum LT last-depn THEN
DO:
    err-no = 1.
    /*MT
    HIDE MESSAGE NO-PAUSE.
    MESSAGE translateExtended("Cancel upgrade NOT POSSIBLE.", lvCAREA, "")
        VIEW-AS ALERT-BOX INFORMATION.
    APPLY "Entry" TO fdate IN FRAME frame1.
    */
    RETURN NO-APPLY.
END.

RUN cancel-upgrade.


PROCEDURE cancel-upgrade :
  DO TRANSACTION:
    FIND CURRENT fa-op EXCLUSIVE-LOCK.
    ASSIGN fa-op.loeschflag = 1.
    FIND CURRENT fa-op NO-LOCK.

    FIND FIRST fa-buff WHERE fa-buff.nr = fa-artikel.p-nr EXCLUSIVE-LOCK .
    ASSIGN 
        fa-buff.warenwert = fa-buff.warenwert - fa-artikel.warenwert
        fa-buff.book-wert = fa-buff.book-wert - fa-artikel.warenwert
        .
    FIND CURRENT fa-buff NO-LOCK.
    
    FIND CURRENT fa-artikel EXCLUSIVE-LOCK.
    ASSIGN
        fa-artikel.loeschflag = 0
        fa-artikel.deleted = ? 
        fa-artikel.DID = user-init
        fa-art.p-nr    = 0.
    FIND CURRENT fa-artikel NO-LOCK.

    err-no = 2.
    /*MT
    */
  END.
END.

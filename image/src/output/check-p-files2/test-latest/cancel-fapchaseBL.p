 
 
DEFINE INPUT PARAMETER lief-nr      AS INTEGER NO-UNDO. 
DEFINE INPUT PARAMETER docu-nr      AS CHAR    NO-UNDO. 
DEFINE INPUT PARAMETER user-init    AS CHAR. 

/* 
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 2. 
DEFINE VARIABLE docu-nr LIKE l-orderhdr.docu-nr INITIAL "I990912001". 
DEFINE VARIABLE user-init AS CHAR INITIAL "SY". 
*/ 

DEFINE VARIABLE lscheinnr AS CHAR. 
DEFINE VARIABLE billdate AS DATE. 
DEFINE VARIABLE t-amount AS DECIMAL. 
DEFINE buffer fa-art FOR fa-artikel. 
 
lscheinnr = docu-nr. 
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
billdate = htparam.fdate. 
 
FOR EACH fa-op WHERE fa-op.lief-nr = lief-nr 
    /*AND fa-op.docu-nr = docu-nr
    AND fa-op.lscheinnr = docu-nr */  /*FD Comment*/
    AND fa-op.lscheinnr = lscheinnr /*FD Nov 21, 2022 => Ticket A80699*/
    AND fa-op.loeschflag LE 1: 
    FIND FIRST fa-artikel WHERE fa-artikel.nr = fa-op.nr EXCLUSIVE-LOCK. 
    IF fa-artikel.p-nr NE 0 THEN 
    DO: 
        FIND FIRST fa-art WHERE fa-art.nr = fa-artikel.p-nr EXCLUSIVE-LOCK NO-ERROR. 
        IF AVAILABLE fa-art THEN 
        DO: 
            fa-art.warenwert = fa-art.warenwert - fa-artikel.warenwert. 
            fa-art.book-wert = fa-art.book-wert - fa-artikel.warenwert. 
            FIND CURRENT fa-art NO-LOCK. 
        END. 
    END. 
    fa-artikel.posted = NO. 
    fa-artikel.next-depn = ?. 
    fa-artikel.anzahl = 0. 
    fa-artikel.warenwert = 0. 
    fa-artikel.book-wert = 0. 
    FIND CURRENT fa-artikel NO-LOCK. 
    fa-op.loeschflag = 2. 
    t-amount = t-amount - fa-op.warenwert. 
END. 
/*
FIND FIRST fa-op WHERE fa-op.opart EQ 1 
  AND fa-op.lscheinnr EQ docu-nr 
  AND fa-op.datum EQ billdate 
  AND fa-op.loeschflag LE 1 NO-LOCK NO-ERROR.
IF AVAILABLE fa-op THEN
DO:
  FIND CURRENT fa-op EXCLUSIVE-LOCK. 
  DELETE fa-op. 
END.
*/

RUN update-ap. 
 
/********************************* PROCEDURE *********************************/ 
PROCEDURE update-ap: 
    FIND FIRST htparam WHERE paramnr = 1016 no-lock. /* ap license */ 
    IF NOT flogical THEN RETURN. 
        
    FIND FIRST l-kredit WHERE l-kredit.name = docu-nr 
        AND l-kredit.saldo = - t-amount 
        AND l-kredit.lief-nr = lief-nr 
        AND l-kredit.rgdatum = billdate NO-LOCK NO-ERROR. 
    IF AVAILABLE l-kredit THEN 
    DO: 
        FIND CURRENT l-kredit EXCLUSIVE-LOCK. 
        DELETE l-kredit. 
    END. 
    ELSE 
    DO: 
      create l-kredit. 
      ASSIGN  l-kredit.name        = docu-nr 
              l-kredit.lief-nr     = lief-nr 
              l-kredit.lscheinnr   = lscheinnr 
              l-kredit.rgdatum     = billdate 
              l-kredit.datum       = ? 
              l-kredit.saldo       = t-amount 
              l-kredit.ziel        = 0 
              l-kredit.netto       = t-amount 
              l-kredit.bediener-nr = bediener.nr. 
    END. 
    
    create ap-journal. 
    ASSIGN  ap-journal.lief-nr    = lief-nr 
            ap-journal.docu-nr    = docu-nr 
            ap-journal.lscheinnr  = docu-nr 
            ap-journal.rgdatum    = billdate 
            ap-journal.saldo      = t-amount 
            ap-journal.netto      = t-amount 
            ap-journal.userinit   = bediener.userinit 
            ap-journal.zeit       = TIME 
            ap-journal.bemerk     = "Cancel Fixed Asset Receiving". 
END. 
 

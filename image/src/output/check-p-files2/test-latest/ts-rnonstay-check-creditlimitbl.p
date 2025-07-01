
DEF INPUT  PARAMETER rechnr         AS INT.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER rec-id         AS INT.
DEF INPUT  PARAMETER balance        AS DECIMAL.
DEF INPUT  PARAMETER overCL-flag    AS LOGICAL.
DEF OUTPUT PARAMETER err-flag       AS INT INIT 0.
DEF OUTPUT PARAMETER msg-str        AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-rnonstay".

FIND FIRST bill WHERE RECID(bill) = rec-id.
RUN check-creditlimit.

PROCEDURE check-creditlimit: 
DEFINE VARIABLE klimit AS DECIMAL. 
DEFINE VARIABLE answer AS LOGICAL INITIAL YES. 
  FIND FIRST vhp.htparam WHERE paramnr = 68 no-lock.  /* credit limit */ 
  FIND FIRST vhp.guest WHERE vhp.guest.gastnr = vhp.bill.gastnr NO-LOCK. 
  IF vhp.guest.kreditlimit NE 0 THEN klimit = vhp.guest.kreditlimit. 
  ELSE 
  DO: 
    IF vhp.htparam.fdecimal NE 0 THEN klimit = vhp.htparam.fdecimal. 
    ELSE klimit = vhp.htparam.finteger. 
  END. 
  IF (vhp.bill.saldo + balance) GT klimit THEN 
  DO: 
    IF overCL-flag THEN 
    DO:
      err-flag = 1.
      msg-str = msg-str + CHR(2)
              + translateExtended ("OVER Credit Limit found !!!",lvCAREA,"")
              + CHR(10)
              + translateExtended ("Given Limit  =",lvCAREA,"") + " "
              + TRIM(STRING(klimit,">>>,>>>,>>>,>>9"))
              + CHR(10)
              + translateExtended ("Bill Balance will be",lvCAREA,"") + " "
              + TRIM(STRING((vhp.bill.saldo + balance),">>>,>>>,>>>,>>9.99"))
              + CHR(10)
              + translateExtended ("Bill Transfer no longer possible.",lvCAREA,"").
      /*MTrechnr = 0.*/
      RETURN. 
    END. 
    msg-str = msg-str + CHR(2) + "&Q"
            + translateExtended ("OVER Credit Limit found !!!",lvCAREA,"")
            + CHR(10)
            + translateExtended ("Given Limit  =",lvCAREA,"") + " "
            + TRIM(STRING(klimit,">>>,>>>,>>>,>>9"))
            + CHR(10)
            + translateExtended ("Bill Balance will be",lvCAREA,"") + " "
            + TRIM(STRING((vhp.bill.saldo + balance),">>>,>>>,>>>,>>9.99"))
            + CHR(10)
            + translateExtended ("CANCEL the Bill Transfer?",lvCAREA,"").
    /*MTVIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer. 
    IF answer THEN rechnr = 0. */
  END. 
END. 


DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER fl-code        AS INT.
DEF INPUT  PARAMETER code           AS CHAR.
DEF INPUT  PARAMETER resnr          AS INT.
DEF INPUT  PARAMETER reslinnr       AS INT.
DEF INPUT  PARAMETER balance        AS DECIMAL.
DEF OUTPUT PARAMETER bilrecid       AS INT.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER msg-str1       AS CHAR.
DEF OUTPUT PARAMETER msg-str2       AS CHAR.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-rzinr".

IF fl-code = 1 THEN 
DO: 
  FIND FIRST vhp.queasy WHERE vhp.queasy.key = 9 AND vhp.queasy.number1 = 
    INTEGER(code) NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.queasy AND vhp.queasy.logi1 THEN 
  DO:
    msg-str = msg-str + CHR(2) + "&Q"
            + translateExtended ("CASH BASIS Billing Instruction :",lvCAREA,"")
            + vhp.queasy.char1
            + CHR(10)
            + translateExtended ("Proceed with the Room Transfer?",lvCAREA,"").
    /*MTIF NOT answer THEN 
    DO:
      APPLY "entry" TO zinr. 
      RETURN NO-APPLY. 
    END.*/
  END.
END.
ELSE IF fl-code = 2 THEN
DO: 
  FIND FIRST vhp.queasy WHERE vhp.queasy.key = 9 AND vhp.queasy.number1 = 
    INTEGER(code) NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.queasy AND vhp.queasy.logi1 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("CASH BASIS Billing Instruction :",lvCAREA,"") + vhp.queasy.char1
            + CHR(10)
            + translateExtended ("Room Transfer not possible",lvCAREA,"").
    /*MTAPPLY "entry" TO zinr. */
    RETURN NO-APPLY. 
  END. 
END.
FIND FIRST vhp.bill WHERE vhp.bill.resnr = resnr 
  AND vhp.bill.reslinnr = reslinnr 
  AND vhp.bill.flag = 0 NO-LOCK. 
bilrecid = RECID(vhp.bill). 
RUN check-creditlimit.

/*ITA 140318*/
RUN check-discrepancy.


PROCEDURE check-creditlimit: 
DEFINE VARIABLE klimit AS DECIMAL. 
DEFINE VARIABLE answer AS LOGICAL INITIAL YES. 
  FIND FIRST  vhp.htparam WHERE paramnr = 68 no-lock.  /* credit limit */ 
  FIND FIRST vhp.guest WHERE vhp.guest.gastnr = vhp.bill.gastnr NO-LOCK. 
  IF vhp.guest.kreditlimit NE 0 THEN klimit = vhp.guest.kreditlimit. 
  ELSE 
  DO: 
    IF vhp.htparam.fdecimal NE 0 THEN klimit = vhp.htparam.fdecimal. 
    ELSE klimit = vhp.htparam.finteger. 
  END. 
  IF (vhp.bill.saldo + balance) GT klimit THEN 
  DO: 
    msg-str1 = msg-str1 + CHR(2) + "&Q"
             + translateExtended ("OVER Credit Limit found: ",lvCAREA,"")
             + translateExtended ("Given Limit  =",lvCAREA,"") + " "
             + TRIM(STRING(klimit,">>>,>>>,>>>,>>9")) + " / "
             + translateExtended ("Bill Balance =",lvCAREA,"") + " "
             + TRIM(STRING(bill.saldo, "->>>,>>>,>>>,>>9.99"))
             + CHR(10)
             + translateExtended ("Restaurant Balance =",lvCAREA,"") + " "
             + TRIM(STRING(balance,"->>>,>>>,>>>,>>9.99"))
             + CHR(10)
             + translateExtended ("Do you wish to CANCEL the room transfer?",lvCAREA,"").
    /*MTIF answer THEN bilrecid = 0. */
  END. 
END. 


PROCEDURE check-discrepancy:
    FIND FIRST res-line WHERE res-line.resnr = resnr AND res-line.reslinnr = reslinnr
        NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN DO:
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr 
            AND zimmer.house-status NE 0 NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer THEN DO:
            msg-str2 = translateExtended ("Room discrepancy is found. Transaction not possible.",lvCAREA,"")
                      + CHR(10) + translateExtended ("Please contact Front Office.",lvCAREA,"").
        END.
    END.
END.


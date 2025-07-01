
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER curr-waiter AS INT.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER p-852 AS INT.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-restinv".

RUN not-balance-bill.
FIND FIRST vhp.htparam WHERE paramnr = 852 NO-LOCK.
ASSIGN p-852 = vhp.htparam.finteger.

PROCEDURE not-balance-bill: 
DEFINE buffer hbill FOR vhp.h-bill. 
DEFINE VARIABLE found AS LOGICAL INITIAL NO. 
  FIND FIRST hbill WHERE hbill.departement = curr-dept 
    AND hbill.kellner-nr = curr-waiter AND hbill.flag = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE hbill THEN 
  DO: 
    msg-str = msg-str + CHR(2) + "&W"
            + translateExtended ("Not balanced open bill(s) found:",lvCAREA,"")
            + CHR(10)
            + translateExtended ("BillNo:",lvCAREA,"") + " " + STRING(hbill.rechnr) + "  "
            + translateExtended ("TableNo:",lvCAREA,"")
            + " " + STRING(hbill.tischnr)
            + CHR(10)
            + translateExtended ("Balance",lvCAREA,"")
            + " " + TRIM(STRING(hbill.saldo,"->>,>>>,>>9.99")).
    found = TRUE. 
  END. 
END. 

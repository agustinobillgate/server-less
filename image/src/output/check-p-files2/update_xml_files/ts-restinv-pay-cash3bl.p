DEF TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INT.


DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER curr-dept AS INT.
DEF INPUT  PARAMETER do-it AS LOGICAL.
DEF INPUT  PARAMETER rec-id AS INT.
DEF INPUT  PARAMETER balance-foreign AS DECIMAL.
DEF INPUT  PARAMETER balance AS DECIMAL.
DEF INPUT  PARAMETER double-currency AS LOGICAL.

DEF OUTPUT PARAMETER exrate  AS DECIMAL. 
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-restinv".

DEFINE BUFFER h-bline               FOR vhp.h-bill-line. 
DEFINE BUFFER h-art                 FOR vhp.h-artikel.

FIND FIRST vhp.h-bill WHERE RECID(vhp.h-bill) = rec-id.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 855 NO-LOCK. 
FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = curr-dept 
  AND vhp.h-artikel.artnr = vhp.htparam.finteger NO-LOCK NO-ERROR. 
IF NOT AVAILABLE h-artikel OR h-artikel.artart NE 6 THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Cash Payment Article not defined. (Param 855 / Grp 19).",lvCAREA,"").
  /*MTAPPLY "entry" TO billart IN FRAME frame1. */
  RETURN NO-APPLY. 
END. 

IF do-it THEN 
DO:
  FIND FIRST h-bline WHERE h-bline.rechnr = vhp.h-bill.rechnr 
    AND h-bline.departement = vhp.h-bill.departement 
    AND h-bline.waehrungsnr GT 0 NO-LOCK NO-ERROR.
  IF AVAILABLE h-bline THEN
  DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("Bill has been splitted, use Split Bill's Cash Payment",lvCAREA,"").
    /*MTAPPLY "entry" TO billart IN FRAME frame1.*/
    RETURN NO-APPLY. 
  END.
  
  IF balance-foreign NE 0 THEN exrate = balance / balance-foreign.
END. 

CREATE t-h-artikel.
BUFFER-COPY h-artikel TO t-h-artikel.
ASSIGN t-h-artikel.rec-id = RECID(h-artikel).

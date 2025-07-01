

DEF INPUT  PARAMETER pvILanguage        AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER str-list-billdate  AS DATE.
DEF INPUT  PARAMETER str-list-lief-nr   AS INT.
DEF INPUT  PARAMETER str-list-docu-nr   AS CHAR.
DEF INPUT  PARAMETER str-list-lscheinnr AS CHAR.
DEF OUTPUT PARAMETER msg-str            AS CHAR.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "supply-inlist".

FIND FIRST htparam WHERE paramnr = 269 NO-LOCK. 
IF htparam.fdate NE ? AND htparam.fdate GT str-list-billdate THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("The receiving record(s) have been transfered to the G/L.",lvCAREA,"")
          + CHR(10)
          + translateExtended ("Inserting is no longer possible.",lvCAREA,"").
  /*MTAPPLY "entry" TO from-date. */
  RETURN NO-APPLY. 
END. 


FIND FIRST l-kredit WHERE l-kredit.lief-nr = str-list-lief-nr 
  AND l-kredit.name = str-list-docu-nr 
  AND l-kredit.lscheinnr = str-list-lscheinnr 
  AND l-kredit.opart GE 1 AND l-kredit.zahlkonto GT 0 NO-LOCK NO-ERROR. 
IF AVAILABLE l-kredit THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("The A/P Payment record found.",lvCAREA,"")
          + CHR(10)
          + translateExtended ("Inserting is no longer possible.",lvCAREA,"").
  /*MTAPPLY "entry" TO from-date. */
  RETURN NO-APPLY. 
END. 

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER datum            AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER acct-date        AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER last-acctdate    AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER to-date          AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER close-year       AS DATE    NO-UNDO.

DEFINE OUTPUT PARAMETER msg-str         AS CHAR    NO-UNDO.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-linkar-check-date". 

IF acct-date = ? OR last-acctdate = ? OR to-date = ? OR close-year = ? THEN 
DO: 
    ASSIGN 
        msg-str = translateExtended ("Accounting Date(s) not defined",lvCAREA,"") + CHR(13)
                  + CHR(10) + translateExtended ("(ParamNo 372, 558, 597, 1014)",lvCAREA,"").
END. 
ELSE 
DO: 
    IF datum LE last-acctdate THEN 
    DO: 
      ASSIGN
          msg-str = translateExtended ("Wrong Posting Date",lvCAREA,"") + CHR(13)
                    + CHR(10) + translateExtended ("Last A/R Journal Transfer Date :",lvCAREA,"") + " " + STRING(last-acctdate)
                    + CHR(13) + CHR(10) + translateExtended ("Current G/L Closing Date :",lvCAREA,"") + " " + STRING(acct-date).      
    END. 
END. 


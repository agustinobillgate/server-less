DEFINE INPUT PARAMETER pvILanguage  AS INT  NO-UNDO.
DEFINE INPUT PARAMETER fibukonto    AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER str-msg     AS CHAR NO-UNDO.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "mk-sarticle". 

FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibukonto NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct AND INTEGER(fibukonto) NE 0 THEN 
    str-msg = translateExtended ("No such account number",lvCAREA,"").

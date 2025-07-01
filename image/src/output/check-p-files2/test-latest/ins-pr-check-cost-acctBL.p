DEFINE INPUT PARAMETER pvILanguage      AS INT  NO-UNDO.
DEFINE INPUT PARAMETER cost-acct        AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str         AS CHAR NO-UNDO.

{ Supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "ins-pr". 


FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-acct NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct THEN 
    msg-str = translateExtended ("Account Number incorrect.",lvCAREA,""). 
IF AVAILABLE gl-acct AND gl-acct.acc-type EQ 1 THEN 
    msg-str = translateExtended ("Wrong Type of Account Number.",lvCAREA,""). 
     

DEFINE INPUT PARAMETER pvILanguage      AS INT  NO-UNDO.
DEFINE INPUT PARAMETER curr-select      AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER acct             AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER s-artnr          AS INT  NO-UNDO.
DEFINE OUTPUT PARAMETER outputChar      AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER l-traubensort   AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER l-lief-einheit  LIKE l-artikel.lief-einheit NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str         AS CHAR NO-UNDO.

{ Supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "ins-pr". 
    
IF curr-select = "cost-acct" THEN 
DO: 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = acct NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acct THEN outputChar = acct. 
END. 
ELSE IF curr-select = "artnr" THEN 
DO: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK. 
    IF l-artikel.betriebsnr NE 0 THEN 
        msg-str = translateExtended ("This is a special article not for purchasing.",lvCAREA,"").
          
    FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK. 
    ASSIGN l-traubensort = l-artikel.traubensort 
           l-lief-einheit = l-artikel.lief-einheit 
           outputChar = TRIM(l-artikel.bezeich) + " - " 
                        + STRING(l-artikel.inhalt) + " " 
                        + STRING(l-artikel.masseinheit,"x(3)"). 
END. 


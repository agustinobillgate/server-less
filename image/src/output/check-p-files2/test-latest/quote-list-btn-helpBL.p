DEFINE INPUT PARAMETER pvILanguage  AS INT  NO-UNDO.
DEFINE INPUT PARAMETER curr-select  AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER art-No       AS INT  NO-UNDO.
DEFINE OUTPUT PARAMETER art-Name    AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER dev-Unit     AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER cont        AS INT  NO-UNDO INIT 0.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR NO-UNDO INIT "".

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "quote-list". 

FIND FIRST l-artikel WHERE l-artikel.artnr = art-No NO-LOCK NO-ERROR. 
IF AVAILABLE l-artikel AND l-artikel.betriebsnr NE 0 THEN 
    ASSIGN art-No   = 0 
           art-Name = ""
           dev-Unit = ""
           cont = 0
           msg-str = translateExtended ("This is a special article not for purchasing.",
                                        lvCAREA,""). 
ELSE IF AVAILABLE l-artikel THEN
    ASSIGN art-Name = TRIM(l-artikel.bezeich) + " - " + 
                           STRING(l-artikel.inhalt) + " " + 
                           STRING(l-artikel.masseinheit,"x(3)")
           dev-Unit = l-artikel.traubensort
           cont = l-artikel.lief-einheit.

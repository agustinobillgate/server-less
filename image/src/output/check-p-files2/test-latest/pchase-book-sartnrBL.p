DEFINE INPUT PARAMETER pvILanguage  AS INT  NO-UNDO.
DEFINE INPUT PARAMETER s-artnr      AS INT  NO-UNDO.
DEFINE OUTPUT PARAMETER s-bezeich   AS CHAR NO-UNDO.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "pchase-book". 

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK NO-ERROR. 
IF AVAILABLE l-artikel THEN s-bezeich = l-artikel.bezeich. 
ELSE s-bezeich = translateExtended ("Article Description",lvCAREA,""). 
       

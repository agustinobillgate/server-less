DEFINE INPUT PARAMETER pvILanguage      AS INT  NO-UNDO.
DEFINE INPUT PARAMETER l-bezeich        AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER str-msg         AS CHAR NO-UNDO INIT "".

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "mk-sarticle". 

DEFINE BUFFER l-art1 FOR l-artikel.

FIND FIRST l-art1 WHERE l-art1.bezeich = l-bezeich NO-LOCK NO-ERROR. 
IF AVAILABLE l-art1 THEN 
    str-msg = "&W" 
              + translateExtended ("Same Description found with article number: ",
                                   lvCAREA,"")
              + STRING(l-art1.artnr). 

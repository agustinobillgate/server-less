DEFINE INPUT PARAMETER pvILanguage  AS INT  NO-UNDO.
DEFINE INPUT PARAMETER case-type    AS INT  NO-UNDO.
DEFINE INPUT PARAMETER inpInt       AS INT  NO-UNDO.
DEFINE INPUT PARAMETER inpInt2      AS INT  NO-UNDO.
DEFINE INPUT PARAMETER inpChar      AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER outChar     AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER outInt      AS INT  NO-UNDO.
DEFINE OUTPUT PARAMETER str-msg     AS CHAR NO-UNDO.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "mk-sarticle". 

DEFINE buffer l-art1 FOR l-artikel. 

CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST l-art1 WHERE l-art1.artnr = inpInt NO-LOCK. 
        IF l-art1.betriebsnr NE 0 THEN 
            str-msg = translateExtended ("This is a special article not for purchasing.",
                                         lvCAREA,""). 

        outChar = l-art1.bezeich. 
        outInt = inpInt. 
    END.
    WHEN 2 THEN
        RUN find-new-artnr(OUTPUT outInt). 
    WHEN 3 THEN
    DO:
        FIND FIRST nation WHERE nation.kurzbez = inpChar NO-LOCK. 
        outChar = nation.bezeich. 
    END.
    WHEN 4 THEN
    DO:
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = inpInt NO-LOCK. 
        outChar = l-lieferant.firma. 
    END.
END CASE.


PROCEDURE find-new-artnr: 
DEFINE OUTPUT PARAMETER new-artnr AS INTEGER INITIAL 0. 
DEFINE buffer l-artikel1 FOR l-artikel. 
DEFINE buffer l-art1 FOR l-artikel. 
   FOR EACH l-art1 WHERE l-art1.zwkum = inpInt
      AND l-art1.endkum = inpInt2 NO-LOCK BY l-art1.artnr DESCENDING: 
      IF l-art1.zwkum LE 99 
          AND SUBSTR(STRING(l-art1.artnr),2,2) EQ STRING(l-art1.zwkum,"99") 
          AND SUBSTR(STRING(l-art1.artnr),1,1) EQ STRING(l-art1.endkum,"9") THEN 
       DO: 
          new-artnr = l-art1.artnr + 1. 
          RETURN. 
       END. 
       ELSE IF l-art1.zwkum GE 100 
           AND SUBSTR(STRING(l-art1.artnr),2,3) EQ STRING(l-art1.zwkum,"999") 
           AND SUBSTR(STRING(l-art1.artnr),1,1) EQ STRING(l-art1.endkum,"9") THEN 
       DO: 
           new-artnr = l-art1.artnr + 1. 
           RETURN. 
       END. 
   END. 
   IF inpInt LE 99 THEN 
       new-artnr = inpInt2 * 1000000 + inpInt * 10000 + 1. 
   ELSE IF inpInt GE 100 THEN 
       new-artnr = inpInt2 * 1000000 + inpInt * 1000 + 1. 
   FIND FIRST l-artikel1 WHERE l-artikel1.artnr = new-artnr NO-LOCK NO-ERROR. 
   IF AVAILABLE l-artikel1 THEN new-artnr = 0. 
END. 

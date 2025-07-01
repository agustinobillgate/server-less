
DEFINE INPUT PARAMETER p-artnr      AS INTEGER.   
DEFINE INPUT PARAMETER menge        AS DECIMAL.   
DEFINE INPUT PARAMETER price-type   AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER cost  AS DECIMAL.   

RUN cal-cost.

PROCEDURE cal-cost:
DEFINE VARIABLE inh AS DECIMAL.   
DEFINE VARIABLE vk-preis AS DECIMAL.   
DEFINE buffer h-rezlin1 FOR h-rezlin.   
  FOR EACH h-rezlin1 WHERE h-rezlin1.artnrrezept = p-artnr NO-LOCK:   
    inh = menge * h-rezlin1.menge.   
    IF h-rezlin1.recipe-flag = YES THEN RUN cal-cost2(h-rezlin1.artnrlager,   
      inh, INPUT-OUTPUT cost).   
    ELSE   
    DO:   
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin1.artnrlager NO-LOCK.   
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN   
        vk-preis = l-artikel.vk-preis.   
      ELSE vk-preis = l-artikel.ek-aktuell.   
      cost = cost + inh / l-artikel.inhalt * vk-preis / (1 - h-rezlin1.lostfact / 100).   
    END.   
  END.   
END.   

PROCEDURE cal-cost2:
DEFINE VARIABLE inh AS DECIMAL.   
DEFINE VARIABLE vk-preis AS DECIMAL.   
DEFINE buffer h-rezlin1 FOR h-rezlin.   
  FOR EACH h-rezlin1 WHERE h-rezlin1.artnrrezept = p-artnr NO-LOCK:   
    inh = menge * h-rezlin1.menge.   
    IF h-rezlin1.recipe-flag = YES THEN RUN cal-cost2(h-rezlin1.artnrlager,   
      inh, INPUT-OUTPUT cost).   
    ELSE   
    DO:   
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin1.artnrlager NO-LOCK.   
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN   
        vk-preis = l-artikel.vk-preis.   
      ELSE vk-preis = l-artikel.ek-aktuell.   
      cost = cost + inh / l-artikel.inhalt * vk-preis / (1 - h-rezlin1.lostfact / 100).   
    END.   
  END.   
END.   

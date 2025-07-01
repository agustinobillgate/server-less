DEFINE TEMP-TABLE lart-list
    FIELD artnr        LIKE l-artikel.artnr
    FIELD bezeich      LIKE l-artikel.bezeich
    FIELD traubensorte AS CHAR COLUMN-LABEL "DelivUnit" FORMAT "x(9)"
    FIELD lief-einheit AS DECIMAL COLUMN-LABEL "Content"   FORMAT ">,>>9" 
.
DEFINE TEMP-TABLE payload-list
  FIELD pr  AS CHAR
  FIELD mode AS INTEGER
  FIELD s-artnr AS INTEGER
  .

DEFINE TEMP-TABLE output-list
  FIELD long-digit AS LOGICAL
  .

DEF TEMP-TABLE q1-list LIKE l-pprice
  FIELD a-firma       LIKE l-lieferant.firma
  FIELD traubensorte  LIKE l-artikel.traubensorte
  FIELD lief-einheit  LIKE l-artikel.lief-einheit
  .
DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.
DEFINE OUTPUT PARAMETER TABLE FOR q1-list.
/* 
DEFINE INPUT  PARAMETER pr         AS CHAR.
DEFINE OUTPUT PARAMETER long-digit AS LOGICAL.
*/
DEFINE OUTPUT PARAMETER TABLE FOR lart-list.
FIND FIRST payload-list NO-ERROR.
CREATE output-list.

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
output-list.long-digit = htparam.flogical. 

IF payload-list.mode EQ 1 THEN /* Prepare list article */
DO:
  RUN create-lart-list.
END.
ELSE /* Handle show data when double click left table */
DO:
  IF payload-list.s-artnr NE ? THEN
  DO:
    RUN create-query.
  END.
END.


PROCEDURE create-lart-list:
  DEFINE BUFFER usr   FOR bediener.
  DEFINE BUFFER l-art FOR l-artikel.
  FOR EACH l-order WHERE l-order.docu-nr = payload-list.pr 
    AND l-order.loeschflag LE 1 AND l-order.pos GT 0 
    AND l-order.lief-nr = 0 NO-LOCK, 
    FIRST l-art WHERE l-art.artnr = l-order.artnr NO-LOCK 
    BY l-art.bezeich: 
    CREATE lart-list.
    BUFFER-COPY l-art TO lart-list.
  END.
END.

PROCEDURE create-query:
  FOR EACH l-pprice WHERE l-pprice.artnr = payload-list.s-artnr NO-LOCK, 
      FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK, 
      FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK:
      CREATE q1-list. 
      BUFFER-COPY l-pprice TO q1-list.
      ASSIGN 
          q1-list.a-firma         = l-lieferant.firma
          q1-list.traubensorte    = l-artikel.traubensorte
          q1-list.lief-einheit    = l-artikel.lief-einheit.
  END.
END.


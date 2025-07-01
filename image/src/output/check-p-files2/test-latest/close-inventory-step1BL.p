
DEF INPUT PARAMETER pvILanguage AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER closedate   AS DATE     NO-UNDO.
DEF INPUT PARAMETER inv-type    AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER m-endkum    AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER its-ok     AS LOGICAL  NO-UNDO INIT YES.
DEF OUTPUT PARAMETER msg-str    AS CHAR     NO-UNDO INIT "".
DEF OUTPUT PARAMETER msg-str2   AS CHAR     NO-UNDO INIT "".

{ supertransbl.i }
DEF VAR lvCAREA AS CHAR INITIAL "close-inventory". 
DEFINE VARIABLE anzahl          AS DECIMAL  NO-UNDO.
DEFINE VARIABLE startDate          AS DATE     NO-UNDO.
DEFINE BUFFER l-onhand FOR l-bestand. 

ASSIGN startDate  = DATE(MONTH(closeDate), 1, YEAR(closeDate)).

FIND FIRST l-bestand WHERE (l-bestand.anf-best-dat LE closedate)
    OR (l-bestand.anf-best-dat GE closedate)
    OR (l-bestand.anf-best-dat = ?) NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE l-bestand: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK 
      NO-ERROR. 
    IF NOT AVAILABLE l-artikel THEN 
    DO:
      msg-str2 = msg-str2 + CHR(2) + "&W"
               + translateExtended ("Article not found for stock onhand",lvCAREA,"") + " " 
               + STRING(l-bestand.artnr,"9999999").
    END. 
    ELSE IF AVAILABLE l-artikel AND ((inv-type = 1 AND endkum LT m-endkum) OR 
      (inv-type = 2 AND endkum GE m-endkum) OR inv-type = 3) THEN 
    DO TRANSACTION: 
      FIND FIRST l-besthis WHERE l-besthis.artnr = l-bestand.artnr
          AND l-besthis.lager-nr = l-bestand.lager-nr
          AND l-besthis.anf-best-dat = l-bestand.anf-best-dat
          NO-ERROR.
      IF NOT AVAILABLE l-besthis THEN CREATE l-besthis.
      BUFFER-COPY l-bestand EXCEPT anz-eingang anz-ausgang
          wert-eingang wert-ausgang TO l-besthis.
      ASSIGN l-besthis.anf-best-dat = startDate.
      FIND FIRST l-onhand WHERE RECID(l-onhand) = RECID(l-bestand).
      DELETE l-onhand.
      RELEASE l-onhand.
    END. /* transaction */
    FIND NEXT l-bestand WHERE (l-bestand.anf-best-dat LE closedate) 
      OR (l-bestand.anf-best-dat GE closedate)
      OR (l-bestand.anf-best-dat = ?) NO-LOCK NO-ERROR. 
END. 

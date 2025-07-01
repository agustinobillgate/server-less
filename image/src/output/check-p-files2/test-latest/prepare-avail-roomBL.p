DEF OUTPUT PARAM ci-date      AS DATE NO-UNDO.
DEF OUTPUT PARAM setup-combo  AS CHAR INIT "" NO-UNDO.
DEF OUTPUT PARAM view-combo   AS CHAR INIT "" NO-UNDO.

RUN htpdate.p (87, OUTPUT ci-date).

FOR EACH paramtext WHERE paramtext.txtnr GE 9201 
  AND paramtext.txtnr LE 9299 NO-LOCK: 
  setup-combo = setup-combo + paramtext.ptexte + ";". 
END. 

FOR EACH paramtext WHERE paramtext.txtnr = 230 NO-LOCK: 
  view-combo = view-combo + paramtext.ptexte + ";".
END. 

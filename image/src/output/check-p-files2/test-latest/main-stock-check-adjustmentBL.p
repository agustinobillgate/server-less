
DEF INPUT-OUTPUT PARAMETER inv-type AS INTEGER.
DEF OUTPUT PARAMETER curr-type AS INTEGER NO-UNDO.  
RUN check-adjustment.

PROCEDURE check-adjustment:
  curr-type = inv-type.  
  IF inv-type = 1 THEN /*Food and Beverage */  
  DO:   
      FIND FIRST l-bestand WHERE l-bestand.artnr LE 2999999   
        AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.  
      IF AVAILABLE l-bestand THEN  
      DO:  
        FIND FIRST l-op WHERE l-op.op-art = 3 AND l-op.artnr LE 2999999   
          AND SUBSTR(l-op.lscheinnr, 1, 3) = "INV" NO-LOCK NO-ERROR.   
        IF NOT AVAILABLE l-op THEN curr-type = 0.   
      END.  
  END.   
  ELSE IF inv-type = 2 THEN /* Material */  
  DO:   
      FIND FIRST l-bestand WHERE l-bestand.artnr GE 3000000  
        AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.  
      IF AVAILABLE l-bestand THEN  
      DO:  
        FIND FIRST l-op WHERE l-op.op-art = 3 AND l-op.artnr GE 3000000   
          AND SUBSTR(l-op.lscheinnr, 1, 3) = "INV" NO-LOCK NO-ERROR.   
        IF NOT AVAILABLE l-op THEN curr-type = 0.   
      END.  
  END.   
  IF inv-type = 3 THEN /* ALL */  
  DO:   
    FIND FIRST l-op WHERE l-op.op-art = 3  
      AND SUBSTR(l-op.lscheinnr, 1, 3) = "INV" NO-LOCK NO-ERROR.   
    IF NOT AVAILABLE l-op THEN curr-type = 0.   
  END.
END.   



DEF TEMP-TABLE t-history LIKE history.
DEF TEMP-TABLE hist1     LIKE history.

DEF INPUT  PARAMETER resnr AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER TABLE FOR hist1.
DEF OUTPUT PARAMETER TABLE FOR t-history.

  FIND FIRST hist1.
  FOR EACH history WHERE history.resnr = resnr 
      AND ((history.ankunft - hist1.ankunft) LE 30 
      OR   (hist1.ankunft - history.ankunft) LE 30) 
      NO-LOCK BY history.ankunft DESCENDING BY history.zinr: 
    CREATE t-history.
    BUFFER-COPY history TO t-history.
  END.

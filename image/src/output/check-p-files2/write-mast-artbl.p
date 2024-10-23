
DEF TEMP-TABLE artikel-list
    FIELD artnr       LIKE artikel.artnr
    FIELD departement LIKE artikel.departement
    FIELD bezeich     LIKE artikel.bezeich
    FIELD artart      LIKE artikel.artart.

DEF INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT PARAMETER resNo     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER TABLE FOR artikel-list.

CASE case-type:
  WHEN 1 THEN
  DO:
    FOR EACH mast-art WHERE mast-art.resnr = resNo:
      DELETE mast-art. 
    END.     
    FIND FIRST artikel-list NO-ERROR.
    DO WHILE AVAILABLE artikel-list.
      CREATE mast-art. 
      ASSIGN
        mast-art.resnr        = resNo
        mast-art.artnr        = artikel-list.artnr
        mast-art.departement  = artikel-list.departement 
        mast-art.reslinnr     = 1
      . 
      FIND NEXT artikel-list NO-ERROR.
    END.
  END.
  WHEN 2 THEN .
END CASE.

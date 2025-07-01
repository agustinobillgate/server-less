DEFINE TEMP-TABLE text-p2-list
    FIELD nr AS INTEGER
    FIELD bezeich AS CHARACTER
    FIELD bg-col AS INTEGER
    FIELD fg-col AS INTEGER.

DEF OUTPUT PARAMETER TABLE FOR text-p2-list.

DEFINE VARIABLE lvCVal      AS CHARACTER                    NO-UNDO. 
DEFINE VARIABLE lvI         AS INTEGER                      NO-UNDO. 
DEFINE VARIABLE lvICnt      AS INTEGER                      NO-UNDO. 
DEFINE VARIABLE dept        AS INTEGER                      NO-UNDO. 
DEFINE VARIABLE cdelimiter  AS CHAR         INITIAL ";"     NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 900 NO-LOCK. 
dept = htparam.finteger. 
IF dept = 0 THEN RETURN. 

FIND FIRST htparam WHERE htparam.paramnr = 902 NO-LOCK. 
IF htparam.fchar = "" THEN RETURN. 
IF htparam.fchar MATCHES ("*,*") THEN cdelimiter = ",".


lvICnt = NUM-ENTRIES(htparam.fchar, cdelimiter). 
DO lvI = 1 TO lvICnt: 
  ASSIGN lvCVal  = "". 
  lvCVal = TRIM(ENTRY(lvI, htparam.fchar, cdelimiter)). 
  
  IF lvCVal NE "" THEN 
  DO: 
    FIND FIRST zwkum WHERE zwkum.zknr = INTEGER(lvCVal) 
        AND zwkum.departement = dept NO-LOCK NO-ERROR.
    IF AVAILABLE zwkum AND (lvI LE 6) THEN 
    DO:
      CREATE text-p2-list.
      ASSIGN 
          text-p2-list.nr = lvI
          text-p2-list.bezeich = zwkum.bezeich
          text-p2-list.bg-col = 9
          text-p2-list.fg-col = 15.
    END. 
  END. 
END.





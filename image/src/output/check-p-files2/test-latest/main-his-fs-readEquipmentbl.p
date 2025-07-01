DEFINE OUTPUT PARAMETER text-p2 AS CHARACTER FORMAT "x(46)" EXTENT 6.


PROCEDURE readEquipment: 
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
        FIND FIRST zwkum WHERE zwkum.departement = dept AND 
          zwkum.zknr = INTEGER(lvCVal) NO-LOCK NO-ERROR. 
        IF AVAILABLE zwkum AND (lvI LE 6) THEN 
        DO: 
          IF lvI = 1 THEN 
          ASSIGN 
            text-p2[1] = zwkum.bezeich 
          . 
          ELSE IF lvI = 2 THEN 
          ASSIGN 
            text-p2[2] = zwkum.bezeich 
          . 
          ELSE IF lvI = 3 THEN 
          ASSIGN 
            text-p2[3] = zwkum.bezeich 
          . 
          ELSE IF lvI = 4 THEN 
          ASSIGN 
            text-p2[4] = zwkum.bezeich 
          . 
          ELSE IF lvI = 5 THEN 
          ASSIGN 
            text-p2[5] = zwkum.bezeich 
          . 
          ELSE IF lvI = 6 THEN 
          ASSIGN 
            text-p2[6] = zwkum.bezeich 
          . 
        END. 
      END. 
    END. 
END PROCEDURE.

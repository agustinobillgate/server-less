
DEFINE TEMP-TABLE z-list   LIKE zwkum. 

DEF OUTPUT PARAMETER system-date    AS DATE.
DEF OUTPUT PARAMETER curr-date      AS DATE.
DEF OUTPUT PARAMETER from-date      AS DATE.
DEF OUTPUT PARAMETER ba-dept        AS INT.
DEF OUTPUT PARAMETER TABLE FOR z-list.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK. 
system-date = htparam.fdate. 
curr-date = htparam.fdate. 
from-date = curr-date. 
 
FIND FIRST htparam WHERE htparam.paramnr = 900 USE-INDEX paramnr_ix NO-LOCK. 
ba-dept = htparam.finteger. 

RUN readEquipment.

PROCEDURE readEquipment: 
    DEFINE VARIABLE lvCVal AS CHARACTER             NO-UNDO. 
    DEFINE VARIABLE lvI    AS INTEGER               NO-UNDO. 
    DEFINE VARIABLE lvICnt AS INTEGER               NO-UNDO. 
    DEFINE VARIABLE dept   AS INTEGER               NO-UNDO. 
 
    FIND FIRST htparam WHERE htparam.paramnr = 900 NO-LOCK. 
    dept = htparam.finteger. 
    IF dept = 0 THEN RETURN. 
 
    FIND FIRST htparam WHERE htparam.paramnr = 902 NO-LOCK. 
    IF htparam.fchar = "" THEN RETURN. 
 
    FOR EACH z-list: 
        DELETE z-list. 
    END. 
 
    lvICnt = NUM-ENTRIES(htparam.fchar, ";"). 
    DO lvI = 1 TO lvICnt: 
      ASSIGN lvCVal  = "". 
      lvCVal = TRIM(ENTRY(lvI, htparam.fchar, ";")). 
      IF lvCVal NE "" THEN 
      DO: 
        FIND FIRST zwkum WHERE zwkum.departement = dept AND 
          zwkum.zknr = INTEGER(lvCVal) NO-LOCK NO-ERROR. 
        IF AVAILABLE zwkum THEN 
        DO: 
          CREATE z-list. 
          BUFFER-COPY zwkum TO z-list. 
        END. 
      END. 
    END. 
END PROCEDURE. 


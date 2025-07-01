DEF TEMP-TABLE t-tisch LIKE tisch.

DEF INPUT PARAMETER dept AS INT.
DEF OUTPUT PARAMETER h-depart AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-tisch.

FIND FIRST hoteldpt WHERE hoteldpt.num = dept NO-LOCK. 
h-depart = hoteldpt.depart.
FOR EACH tisch WHERE tisch.departement = dept
    NO-LOCK BY tisch.tischnr:
    CREATE t-tisch.
    BUFFER-COPY tisch TO t-tisch.
END.

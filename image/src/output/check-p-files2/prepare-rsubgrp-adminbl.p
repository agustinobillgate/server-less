
DEFINE TEMP-TABLE t-wgrpdep LIKE wgrpdep
    FIELD rec-id AS INT.

DEF INPUT PARAMETER dept AS INT.
DEF OUTPUT PARAMETER hoteldpt-depart AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-wgrpdep.

FIND FIRST hoteldpt WHERE hoteldpt.num = dept NO-LOCK. 
hoteldpt-depart = hoteldpt.depart.

FOR EACH wgrpdep WHERE wgrpdep.departement = dept 
    NO-LOCK BY wgrpdep.betriebsnr DESCENDING BY wgrpdep.zknr:
    CREATE t-wgrpdep.
    BUFFER-COPY wgrpdep TO t-wgrpdep.
    ASSIGN t-wgrpdep.rec-id = RECID(wgrpdep).
END.

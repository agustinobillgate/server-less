DEFINE TEMP-TABLE t-phone-list
    FIELD dept LIKE telephone.dept
    FIELD name LIKE telephone.name
    FIELD telephone LIKE telephone.telephone
    FIELD ext LIKE telephone.ext
    FIELD mobil-telefon LIKE telephone.mobil-telefon
    FIELD fax LIKE telephone.fax
    FIELD adresse1 LIKE telephone.adresse1
    FIELD wohnort LIKE telephone.wohnort
    FIELD prefix LIKE telephone.prefix
    FIELD land LIKE telephone.land
    FIELD vorname LIKE telephone.vorname
    FIELD telex LIKE telephone.telex
    FIELD adresse2 LIKE telephone.adresse2
    FIELD rec-id AS INTEGER.

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER name1 AS CHAR.
DEFINE INPUT PARAMETER dept1 AS CHAR.

DEFINE INPUT PARAMETER phone-nr AS CHAR.
DEFINE INPUT PARAMETER pn AS CHAR.

DEFINE INPUT PARAMETER mobil-nr AS CHAR.
DEFINE INPUT PARAMETER lvCOldMobilNR AS CHAR.

DEFINE OUTPUT PARAMETER TABLE FOR t-phone-list.
    
IF case-type = 1 THEN   /*btn-go*/
DO:
    IF dept1 = "" THEN 
    DO: 
        IF SUBSTR(name1,1,1) = "*" THEN 
        DO: 
            FOR EACH telephone WHERE 
                telephone.name MATCHES name1 USE-INDEX name
                NO-LOCK BY telephone.name:
                RUN assign-it.
            END.
        END. 
        ELSE
        DO:
            FOR EACH telephone WHERE 
                telephone.name GE name1 USE-INDEX name
                NO-LOCK BY telephone.name:
                RUN assign-it.
            END.
        END.
    END. 
    ELSE 
    DO: 
        IF SUBSTR(name1,1,1) = "*" THEN 
        DO: 
          FOR EACH telephone WHERE
              telephone.dept GE dept1 AND telephone.name MATCHES name1 
              USE-INDEX dep_ix
              NO-LOCK BY telephone.dept BY telephone.name:
              RUN assign-it.
          END.
        END. 
        ELSE
        DO:
           FOR EACH telephone WHERE 
               telephone.dept GE dept1 AND telephone.name GE name1 
               USE-INDEX dep_ix
               NO-LOCK BY telephone.dept BY telephone.name:
               RUN assign-it.
           END.
        END.
    END. 
END.
ELSE IF case-type = 2 THEN  /*phone-nr*/
DO:
  IF phone-nr = "" AND phone-nr NE pn THEN 
  DO: 
    FOR EACH telephone WHERE 
      telephone.dept GE dept1 AND telephone.name GE name1 
      USE-INDEX dep_ix
      NO-LOCK BY telephone.dept BY telephone.name:
        RUN assign-it.
    END.
  END. 
  ELSE 
  DO: 
    IF phone-nr NE "" AND phone-nr NE pn THEN 
    DO: 
      IF SUBSTR(phone-nr,1,1) = "*" THEN 
      FOR EACH telephone WHERE 
        telephone.telephone MATCHES(phone-nr) 
        AND telephone.dept GE dept1 AND telephone.name GE name1 
        USE-INDEX dep_ix
        NO-LOCK BY telephone.telephone:
          RUN assign-it.
      END.
      ELSE 
        FOR EACH telephone WHERE 
        telephone.telephone GE phone-nr 
        AND telephone.dept GE dept1 AND telephone.name GE name1 
        USE-INDEX dep_ix
        NO-LOCK BY telephone.telephone:
          RUN assign-it.
        END.
    END. 
  END. 
END.
ELSE IF case-type = 3 THEN  /*mobil-nr*/
DO:
    IF mobil-nr EQ "" AND mobil-nr NE lvCOldMobilNr THEN DO: 
        FOR EACH telephone NO-LOCK WHERE 
            telephone.dept      GE dept1        AND 
            telephone.name      GE name1 
            USE-INDEX dep_ix
            BY telephone.dept BY telephone.name:
            RUN assign-it.
        END.
    END. 
    ELSE DO: 
        IF mobil-nr NE "" AND mobil-nr NE lvCOldMobilNr THEN DO: 
            IF SUBSTRING(mobil-nr, 1, 1) EQ "*" THEN 
                FOR EACH telephone NO-LOCK WHERE
                    telephone.dept      GE dept1        AND 
                    telephone.name      GE name1        AND 
                    telephone.mobil-telefon MATCHES(mobil-nr + "*") 
                    USE-INDEX dep_ix
                    BY telephone.mobil-telefon BY telephone.dept:
                    RUN assign-it.
                END.
            ELSE 
                FOR EACH telephone NO-LOCK WHERE 
                    telephone.dept      GE dept1        AND 
                    telephone.name      GE name1        AND 
                    telephone.mobil-telefon GE mobil-nr 
                    USE-INDEX dep_ix
                    BY telephone.mobil-telefon BY telephone.dept:
                    RUN assign-it.
                END.
        END. 
    END. 
END.


PROCEDURE assign-it:
    CREATE t-phone-list.
    ASSIGN
        t-phone-list.dept = telephone.dept
        t-phone-list.name = telephone.name
        t-phone-list.telephone = telephone.telephone
        t-phone-list.ext = telephone.ext
        t-phone-list.mobil-telefon = telephone.mobil-telefon
        t-phone-list.fax = telephone.fax
        t-phone-list.adresse1 = telephone.adresse1
        t-phone-list.wohnort = telephone.wohnort
        t-phone-list.prefix = telephone.prefix
        t-phone-list.land = telephone.land
        t-phone-list.vorname = telephone.vorname
        t-phone-list.telex = telephone.telex
        t-phone-list.adresse2 = telephone.adresse2
        t-phone-list.rec-id = RECID(telephone).
END.

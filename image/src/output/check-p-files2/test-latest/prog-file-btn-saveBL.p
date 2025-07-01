DEFINE TEMP-TABLE prog-list
    FIELD counter       AS INTEGER
    FIELD prog-grup     AS INTEGER /*1=Pre Night Audit dan 2=Post Night Audit*/
    FIELD prog-title    AS CHAR
    FIELD prog-name     AS CHAR
    FIELD prog-desc     AS CHAR
    FIELD prog-active   AS LOGICAL
    FIELD rec-id        AS INTEGER
 .

/*1=add 2=modify 3=delete*/
DEFINE INPUT PARAMETER case-type   AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER main-nr     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER counter     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER grupno      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER titleno     AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER rname       AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER bezeich     AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER active-flag AS LOGICAL NO-UNDO.

DEFINE VARIABLE count-no AS INTEGER NO-UNDO INIT 0.

CASE case-type:
    WHEN 1 THEN DO:
        FOR EACH progfile WHERE progfile.catnr  = main-nr
            AND progfile.bezeich MATCHES "*;*"  NO-LOCK BY progfile.bezeich DESC:
            ASSIGN count-no = INTEGER(ENTRY(1,progfile.bezeich,";")).
            LEAVE.
        END.

        
        ASSIGN count-no = count-no + 1.
        CREATE progfile.
        ASSIGN progfile.catnr   = main-nr
               progfile.bezeich = STRING(count-no) + ";" 
                                  + STRING(grupno) + ";"
                                  + titleno + ";"
                                  + rname + ";"
                                  + bezeich + ";"
                                  + STRING(active-flag)
            .                    
    END.
    WHEN 2 THEN DO:
        FIND FIRST progfile WHERE progfile.catnr   = main-nr
            AND progfile.bezeich MATCHES "*;*" 
            AND INTEGER(ENTRY(1, progfile.bezeich, ";")) = counter NO-LOCK NO-ERROR.
        IF AVAILABLE progfile THEN DO:
            FIND CURRENT progfile EXCLUSIVE-LOCK.
            ASSIGN 
                progfile.bezeich = STRING(counter) + ";" 
                                  + STRING(grupno) + ";"
                                  + titleno + ";"
                                  + rname + ";"
                                  + bezeich + ";"
                                  + STRING(active-flag)
            .                                      
            FIND CURRENT progfile NO-LOCK.
            RELEASE progfile.
        END.
    END.
    WHEN 3 THEN DO:
        FIND FIRST progfile WHERE progfile.catnr   = main-nr
            AND progfile.bezeich MATCHES "*;*" 
            AND INTEGER(ENTRY(1, progfile.bezeich, ";")) = counter NO-LOCK NO-ERROR.
        IF AVAILABLE progfile THEN DO:
            FIND CURRENT progfile EXCLUSIVE-LOCK.
            DELETE progfile.
            RELEASE progfile.
        END.
    END.
END CASE.

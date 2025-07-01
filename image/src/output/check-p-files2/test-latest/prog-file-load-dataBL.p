
DEFINE TEMP-TABLE prog-list
    FIELD counter       AS INTEGER
    FIELD prog-grup     AS INTEGER /*1=Pre Night Audit dan 2=Post Night Audit*/
    FIELD prog-title    AS CHAR
    FIELD prog-name     AS CHAR
    FIELD prog-desc     AS CHAR
    FIELD prog-active   AS LOGICAL
    FIELD rec-id        AS INTEGER
 .


DEFINE INPUT PARAMETER main-nr      AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER time-server AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR prog-list.

ASSIGN time-server = STRING(TODAY, "99/99/9999") + " " + STRING(TIME, "HH:SS:MM").

FOR EACH progfile WHERE progfile.catnr = main-nr NO-LOCK:
    CREATE prog-list.
    ASSIGN prog-list.counter    = INTEGER(ENTRY(1, progfile.bezeich, ";"))
           prog-list.prog-grup  = INTEGER(ENTRY(2, progfile.bezeich, ";"))
           prog-list.prog-title = ENTRY(3, progfile.bezeich, ";")
           prog-list.prog-name  = ENTRY(4, progfile.bezeich, ";")
           prog-list.prog-desc  = ENTRY(5, progfile.bezeich, ";")
           prog-list.prog-active = LOGICAL(ENTRY(6, progfile.bezeich, ";"))
      .
END.

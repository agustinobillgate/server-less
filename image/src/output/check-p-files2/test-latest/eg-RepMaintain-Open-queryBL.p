
DEF TEMP-TABLE t-eg-maintain LIKE eg-maintain.

DEF INPUT PARAMETER fdate AS DATE.
DEF INPUT PARAMETER tdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-eg-maintain.

FOR EACH eg-maintain WHERE 
    eg-maintain.estworkdate >= fdate AND 
    eg-maintain.estworkdate <= tdate AND 
    /*eg-maintain.delete-flag NE YES FTserverless*/
    NOT eg-maintain.delete-flag NO-LOCK:
    CREATE t-eg-maintain.
    BUFFER-COPY eg-maintain TO t-eg-maintain.
END.

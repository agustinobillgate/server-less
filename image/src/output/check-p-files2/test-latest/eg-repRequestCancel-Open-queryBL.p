
DEF TEMP-TABLE t-eg-request LIKE eg-request.

DEF INPUT PARAMETER fdate AS DATE.
DEF INPUT PARAMETER tdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-eg-request.
    
FOR EACH eg-request WHERE 
    eg-request.cancel-date GE fdate AND 
    eg-request.cancel-date LE tdate AND 
    eg-request.delete-flag = YES NO-LOCK:
    CREATE t-eg-request.
    BUFFER-COPY eg-request TO t-eg-request.
END.


DEF TEMP-TABLE t-l-artikel LIKE l-artikel.
DEF TEMP-TABLE t-h-rezept LIKE h-rezept.

DEF OUTPUT PARAMETER price-type AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.
DEF OUTPUT PARAMETER TABLE FOR t-h-rezept.

FIND FIRST htparam WHERE paramnr = 1024 NO-LOCK. 
price-type = htparam.finteger. 

/* -START RS 19 feb 2010 add this code to prevent error message "Entry 2 is outside the range of list" */
FOR EACH l-artikel WHERE l-artikel.herkunft = "" EXCLUSIVE-LOCK :
    ASSIGN l-artikel.herkunft = ";;".
END.
RELEASE l-artikel.
/* -END RS 19 feb 2010 */

FOR EACH l-artikel:
    CREATE t-l-artikel.
    BUFFER-COPY l-artikel TO t-l-artikel.
END.

FOR EACH h-rezept:
    CREATE t-h-rezept.
    BUFFER-COPY h-rezept TO t-h-rezept.
END.

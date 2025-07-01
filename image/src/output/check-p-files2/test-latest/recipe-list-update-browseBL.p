
DEFINE TEMP-TABLE t-h-rezept LIKE h-rezept.

DEF OUTPUT PARAMETER TABLE FOR t-h-rezept.

FOR EACH h-rezept:
    CREATE t-h-rezept.
    BUFFER-COPY h-rezept TO t-h-rezept.
END.

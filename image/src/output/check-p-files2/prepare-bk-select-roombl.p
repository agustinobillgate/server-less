DEFINE TEMP-TABLE t-bkraum LIKE bk-raum.

DEFINE OUTPUT PARAMETER TABLE FOR t-bkraum.

FOR EACH bk-raum:
    CREATE t-bkraum.
    BUFFER-COPY bk-raum TO t-bkraum.
END.

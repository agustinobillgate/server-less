DEFINE TEMP-TABLE t-bk-raum LIKE bk-raum.


DEFINE OUTPUT PARAMETER TABLE FOR t-bk-raum.


FOR EACH bk-raum NO-LOCK:
    BUFFER-COPY bk-raum TO t-bk-raum.
END.

DEF TEMP-TABLE t-artikel LIKE artikel.


DEFINE INPUT PARAMETER TABLE FOR t-artikel.

FOR EACH t-artikel BY t-artikel.artnr BY t-artikel.departement:
    DISP t-artikel.artnr t-artikel.departement LABEL "Dept" t-artikel.bezeich.
    UPDATE t-artikel.bezeich2.
    IF t-artikel.bezeich2 NE "" THEN
    DO:
        RUN gst-init-update-foartikelbl.p
            (t-artikel.artnr, t-artikel.departement, t-artikel.bezeich2).
    END.
END.


DEF TEMP-TABLE t-uebertrag LIKE uebertrag.

DEF OUTPUT PARAMETER TABLE FOR t-uebertrag.

FOR EACH uebertrag NO-LOCK:
    CREATE t-uebertrag.
    BUFFER-COPY uebertrag TO t-uebertrag.
END.


/*

FOR EACH _file WHERE _file._hidden = NO NO-LOCK:
    disp _file._file-name.
END.
*/

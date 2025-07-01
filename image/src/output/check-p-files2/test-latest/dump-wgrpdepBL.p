
DEF TEMP-TABLE t-wgrpdep LIKE wgrpdep.

DEF OUTPUT PARAMETER TABLE FOR t-wgrpdep.

FOR EACH wgrpdep NO-LOCK:
    CREATE t-wgrpdep.
    BUFFER-COPY wgrpdep TO t-wgrpdep.
END.


/*

FOR EACH _file WHERE _file._hidden = NO NO-LOCK:
    disp _file._file-name.
END.
*/

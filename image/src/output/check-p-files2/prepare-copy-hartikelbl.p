
DEFINE TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEF OUTPUT PARAMETER p-852 AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.

FIND FIRST vhp.htparam WHERE paramnr = 852 NO-LOCK.
p-852 = htparam.finteger.

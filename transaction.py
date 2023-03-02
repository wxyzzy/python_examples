# Supporting the "with" statement
# from Henrik Tunedal


class Transaction:
    def __init__(self, conn, mode):
        self.conn = conn
        if mode in ["DEFERRED", "IMMEDIATE", "EXCLUSIVE"]:
            self.mode = mode
        else:
            raise Exception("Invalid mode: " + repr(mode))

    def __enter__(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute("BEGIN {} TRANSACTION".format(self.mode))
        return self.cursor

    def __exit__(self, errtype, errvalue, traceback):
        if errtype:
            self.conn.rollback()
        else:
            self.conn.commit()

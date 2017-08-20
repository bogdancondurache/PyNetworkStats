from config import config_db


def main():
    conn, c = config_db()

    query = 'CREATE  TABLE "main"."systems" ("id" INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL  UNIQUE , ' \
            '"ip" TEXT NOT NULL , "memory_usage" DOUBLE NOT NULL , "cpu_usage" DOUBLE NOT NULL , ' \
            '"uptime" DOUBLE NOT NULL , "events" TEXT)'

    c.execute(query)
    conn.commit()
    conn.close()

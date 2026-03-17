import mysql.connector
database = mysql.conncetor.conect(
    host ="localhost",
    user = "root",
    password = "",

)
cursorObject = database.cursor()
cursorObject.execute("CREATE DATABASE cliente")
print("Base de datos creada")


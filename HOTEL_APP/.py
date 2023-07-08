import sqlite3

connection=sqlite3.connect('db_royalpalm.db')
c= connection.cursor()

# c.execute("CREATE TABLE usuario (cedula varchar(50) primary key, nombre varchar(50), apellido varchar(50), correo varchar(50), clave varchar(50), rol varchar(50) )")



c.execute("INSERT INTO usuario VALUES('29831425','WILFRED','SILVA','wuilfred@gmail.com','123','usuario')")
connection.commit()
connection.close()
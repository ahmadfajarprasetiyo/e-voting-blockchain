import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="toor",
  database="evoting"
)

mycursor = db.cursor()

mycursor.execute("DROP TABLE IF EXISTS blockchains") 
mycursor.execute("DROP TABLE IF EXISTS pilihans")
mycursor.execute("DROP TABLE IF EXISTS alamat_blockchains")
mycursor.execute("DROP TABLE IF EXISTS map_blockchains")




mycursor.execute("CREATE TABLE blockchains (id INT(6), nama VARCHAR(255))")
mycursor.execute("CREATE TABLE pilihans (id_blockchain INT(6), id_pilihan INT(6), nilai_n INT(6), nilai_e INT(6))")
mycursor.execute("CREATE TABLE alamat_blockchains (id_blockchain INT(6), alamat VARCHAR(255))")
mycursor.execute("CREATE TABLE map_blockchains (id_blockchain INT(6), nilai_n INT(6), nilai_e INT(6))")

from DB_CONNECT import condb
mydb = condb(1)
c = mydb.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS vettable(
                        vetId SERIAL NOT NULL,
                        vetName VARCHAR(50) NOT NULL,
                        vetDes VARCHAR(500),
                        vetDate TIMESTAMP NOT NULL,
                        vetImg BYTEA,
                        PRIMARY KEY(vetId)
                        );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS addrprovince(
                        provinceId CHAR(2) NOT NULL,
                        provinceName VARCHAR(50) NOT NULL,
                        PRIMARY KEY(provinceId)
                        );   
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS addrdistrict(
                        districtId CHAR(4) NOT NULL,
                        districtName VARCHAR(50) NOT NULL,
                        provinceId CHAR(2) NOT NULL,
                        PRIMARY KEY(districtID),
                        FOREIGN KEY (provinceId) REFERENCES addrprovince(provinceID)
                        ON UPDATE RESTRICT ON DELETE CASCADE
                        );          
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS addrsubdistrict(
                        subdistrictId CHAR(6) NOT NULL,
                        subdistrictName VARCHAR(50) NOT NULL,
                        postcode CHAR(5) NOT NULL,
                        districtId CHAR(4) NOT NULL,
                        PRIMARY KEY (subdistrictId),
                        FOREIGN KEY (districtId) REFERENCES addrdistrict(districtId)
                        ON UPDATE RESTRICT ON DELETE CASCADE
                        );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS farmertable(
                        farmerId SERIAL NOT NULL, 
                        preName CHAR(6),
                        farmerFirstname VARCHAR(250) NOT NULL,
                        farmerLastname VARCHAR(250) NOT NULL,
                        farmerIdth CHAR(13),
                        idTh CHAR(13),
                        addrNo CHAR(7) NOT NULL,
                        addrVilno CHAR(2),
                        addrVil VARCHAR(150),
                        addrSubdistrictid CHAR(6) NOT NULL,
                        farmerTel CHAR(10),
												
						PRIMARY KEY (farmerId),
						FOREIGN KEY (addrSubdistrictid) REFERENCES addrsubdistrict(subdistrictId)
                        ON UPDATE RESTRICT ON DELETE CASCADE
                        ); 
    """)
    c.execute("""CREATE TABLE IF NOT EXISTS farmlocation(
                        farmId SERIAL NOT NULL,
                        landPrivileges VARCHAR(60),
                        farmvil VARCHAR(150),
						farmVilno VARCHAR(2) NOT NULL,
						farmSubdistrictid CHAR (6) NOT NULL,
						quantityFarm INT,
						quantityBuilding INT,
						soilAnalysed BOOLEAN,
						waterAnalysed BOOLEAN,
						gapAnalysed BOOLEAN,
						PRIMARY KEY (farmId),
						FOREIGN KEY (farmId) REFERENCES farmertable(farmerId)
                        ON UPDATE RESTRICT ON DELETE CASCADE
						);
    """)

    return False
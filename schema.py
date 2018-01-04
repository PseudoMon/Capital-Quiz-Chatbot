import peewee, codecs

db = peewee.SqliteDatabase("countries.db")

class BaseModel(peewee.Model):
    class Meta:
        database = db
        
class Country(BaseModel):
    name = peewee.TextField()
    capital = peewee.TextField()
    area = peewee.FloatField()
    population = peewee.IntegerField()
    continent = peewee.TextField()
    
class Game(BaseModel):
    isgroup = peewee.BooleanField()
    source_id = peewee.TextField()
    currentcountry = peewee.ForeignKeyField(Country, related_name='games', null=True)
    modifier = peewee.TextField(null=True)
    
def createCountriesDB():
    Country.create_table()

    cl = codecs.open("countriescapitalnew.txt", 'r', 'utf-8')
    for country in cl.readlines():
        country = country.replace('\n', '')
        
        if country != " ":
            country = country.split("\t")
            name = country[4]
            capital = country[5]
            area = float("".join(country[6].split(",")))
            population = int(float("".join(country[6].split(","))))
            cont = country[8]
            
            c = Country(name=name, capital=capital, population=population, area=area, continent=cont)
            c.save()
            
            print("Added: " + name + " : " + capital)
                
                
        
if __name__ == '__main__':
    Game.drop_table()
    Game.create_table()
    Country.drop_table()
    createCountriesDB()
    
    
    print("Testing!")
    print("The capital of Kuwait is:")
    c = Country.get(Country.name=="Kuwait")
    print(c.capital)
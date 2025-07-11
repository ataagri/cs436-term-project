""" database creation """
import sqlalchemy.exc
from db import Base, SessionLocal, engine
from models import Contact

print("Creating database tables...")
try:
    Base.metadata.create_all(engine)
    print("Tables created successfully")
except Exception as e:
    print(f"Error creating tables: {e}")
    exit(1)

print("Adding sample contacts...")
db = SessionLocal()

try:
    # Check if we already have contacts to avoid duplicates
    existing_contacts = db.query(Contact).count()
    if existing_contacts > 0:
        print(f"Database already has {existing_contacts} contacts. Skipping sample data creation.")
        db.close()
        exit(0)
        
    sample_contacts = [
        Contact(
            first_name="Bilbo",
            last_name="Baggins",
            company=None,
            telephone=None,
            email="bilbo@gmail.com",
            address="1 Middle Earth",
            notes="some note blah blah blah",
        ),
        Contact(
            first_name="Harry",
            last_name="Potter",
            company="Hogwarts",
            telephone="0723456789",
            email="hpotter@hogwarts.co.uk",
            address="Highlands, Scotland, UK",
            notes="some note blah blah blah",
        ),
        Contact(
            first_name="Mary",
            last_name="Poppins",
            company="Perfect Nanny Corp",
            telephone="02012349876",
            email="mary@poppins.co.uk",
            address="17 Cherry Tree Lane",
            notes="some note blah blah blah",
        ),
        Contact(
            first_name="Tony",
            last_name="Stark",
            company="Stark Industries",
            telephone="212-456-7890",
            email="tony@starkindustries.com",
            address="1 Stark Tower, New York, NY 12345",
            notes="some note blah blah blah",
        ),
        Contact(
            first_name="Daenerys",
            last_name="Targaryen",
            company="Mother of Dragons",
            telephone=None,
            email="dtargaryen@got.com",
            address="House Targaryen of King's Landing, Westeros",
            notes="some note blah blah blah",
        ),
        Contact(
            first_name="Frank",
            last_name="Flintstone",
            company="Slate Rock and Gravel Company",
            telephone="210-555-1212",
            email="frank.flintstone@srgc.com",
            address="1 Yabba-Dabba-Doo, Bedrock, TX 12345",
            notes="some note blah blah blah",
        ),
        Contact(
            first_name="Luke",
            last_name="Skywalker",
            company="Jedi Order",
            telephone="012-345-6789",
            email="lskywalker@jediorder.xyz",
            address="69 Padmé Amidala Way, Coruscant, Tatooine",
            notes="some note blah blah blah",
        ),
        Contact(
            first_name="Peter",
            last_name="Parker",
            company=None,
            telephone="212-987-6543",
            email="peterparker@gmail.com",
            address="20 Ingram Street, New York, NY 12345",
            notes="some note blah blah blah",
        ),
        Contact(
            first_name="Walter",
            last_name="White",
            company="Gray Matter Technologies",
            telephone="505-353-1234",
            email="walter@graymatter.com",
            address="308 Negra Arroyo Lane, Albuquerque, NM 87111",
            notes="some note blah blah blah",
        ),
        Contact(
            first_name="Harvey",
            last_name="Specter",
            company="Specter Litt",
            telephone="212-456-7890",
            email="harvey.specter@specterlitt.com",
            address="1 Specter Litt, New York, NY 12345",
            notes="some note blah blah blah",
        ),
    ]
    
    db.add_all(sample_contacts)
    db.commit()
    print(f"Added {len(sample_contacts)} sample contacts to the database")
except sqlalchemy.exc.SQLAlchemyError as e:
    db.rollback()
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error adding sample data: {e}")
finally:
    db.close()
    print("Database connection closed")
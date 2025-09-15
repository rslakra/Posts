#
# Author: Rohtash Lakra
#
from datetime import datetime

from sqlalchemy.orm import Session

from framework.db.connector import createEngine, createDatabase
from rest.role.schema import RoleSchema
from rest.user.schema import UserSchema, AddressSchema


class SqlAlchemyTableObject:

    def __init__(self):
        # The echo=True parameter indicates that SQL emitted by connections will be logged to standard out.
        self.engine = createEngine("sqlite:///testPosts.db", True)
        createDatabase(self.engine)

    def populate_database(self):
        print(f"populate_database\n")
        with Session(self.engine) as session:
            # create roles
            admin_role = RoleSchema(name="ADMIN")
            user_role = RoleSchema(name="USER")
            guest_role = RoleSchema(name="GUEST")
            # add all roles
            session.add_all([admin_role, user_role, guest_role])

            # create users
            roh = UserSchema(
                user_name="roh@lakra.com",
                password="Roh",
                email="roh@lakra.com",
                first_name="Rohtash",
                last_name="Lakra",
                admin=True,
                addresses=[AddressSchema(
                    street1="Tennison Rd",
                    city="Hayward",
                    state="California",
                    country="US",
                    zip="94544"
                )],
            )

            san = UserSchema(
                user_name="san@lakra.com",
                password="San",
                email="san@lakra.com",
                first_name="Sangita",
                last_name="Lakra",
                admin=True,
                addresses=[AddressSchema(
                    street1="Mission Blvd",
                    city="Hayward",
                    state="California",
                    country="US",
                    zip="94544"
                ),
                    AddressSchema(
                        street1="Mission Rd",
                        city="Fremont",
                        state="California",
                        country="US",
                        zip="94534"
                    )
                ]
            )

            # add users
            session.add_all([roh, san])
            session.commit()
        print()

    def fetch_roles(self):
        print(f"fetch_roles\n")
        # Simple SELECT
        from sqlalchemy import select
        session = Session(self.engine)
        stmt = select(RoleSchema)
        for role in session.scalars(stmt):
            print(role)
        print()

    def fetch_users(self):
        print(f"fetch_users\n")
        # Simple SELECT
        from sqlalchemy import select
        session = Session(self.engine)
        stmt = select(UserSchema)
        for user in session.scalars(stmt):
            print(user)
        print()

    def fetch_records(self):
        print(f"fetch_records\n")
        # Simple SELECT
        from sqlalchemy import select
        session = Session(self.engine)
        stmt = select(UserSchema).where(UserSchema.first_name.in_(["Rohtash", "Sangita"]))
        for user in session.scalars(stmt):
            print(user)
        print()

    def fetch_with_joins(self):
        print(f"fetch_with_joins\n")
        from sqlalchemy import select
        session = Session(self.engine)
        stmt = (
            select(AddressSchema)
            .join(AddressSchema.user)
            .where(AddressSchema.state == "California")
            .where(UserSchema.first_name == "Rohtash")
        )
        roh_address = session.scalars(stmt).one()
        print(roh_address)
        print()

    def update_records(self):
        print(f"update_records\n")
        from sqlalchemy import select
        session = Session(self.engine)
        stmt = (
            select(AddressSchema)
            .join(AddressSchema.user)
            .where(AddressSchema.state == "California")
            .where(UserSchema.first_name == "Rohtash")
        )
        roh_address = session.scalars(stmt).one()
        print(f"roh_address\n{roh_address}")
        roh_address.street2 = "roh@sqlalchemy.org"
        print(f"After update roh_address\n{roh_address}")

        # add new address
        stmt = select(UserSchema).where(UserSchema.first_name == "Sangita")
        san = session.scalars(stmt).one()
        print(f"san\n{san}")
        san.addresses.append(
            AddressSchema(
                street1="Mission Creek",
                city="Fremont",
                state="California",
                country="US",
                zip="94536"
            )
        )

        # stmt = select(User).where(User.first_name == "Sangita")
        print(f"san.addresses\n{san.addresses}")
        session.commit()
        print()

    def delete_record(self):
        print(f"delete_record\n")
        from sqlalchemy import select
        session = Session(self.engine)

        stmt = select(AddressSchema).where(AddressSchema.zip == "94536")
        san_address = session.scalars(stmt).one()
        print(f"san_address\n{san_address}")
        print()

        san = session.get(UserSchema, 2)
        print(f"san\n{san}")
        print()

        print(f"deleting address: {san_address.id}")
        san.addresses.remove(san_address)
        session.flush()

        print(f"Deleting User:\n{san}")
        session.delete(san)
        session.commit()
        print()


class SqlAlchemyClassicalObject:

    def create_role(self, roleName):
        now = datetime.now()
        return RoleSchema(name=roleName, created_at=now, updated_at=now)

    def create_address(self, street1, city, state, country, zip):
        return AddressSchema(
            street1=street1,
            city=city,
            state=state,
            country=country,
            zip=zip
        )

    def create_user(self, userName, password, email, firstName, lastName, isAdmin, addresses: [AddressSchema]):
        return UserSchema(
            user_name="roh@lakra.com",
            password="Roh",
            email="roh@lakra.com",
            first_name="Rohtash",
            last_name="Lakra",
            admin=True,
            addresses=addresses,
        )

    def print_classical_objects(self):
        print(f"print_classical_objects\n")
        # create roles
        roles = (self.create_role("ADMIN"), self.create_role("USER"), self.create_role("GUEST"))
        print(f"roles:\n{roles}")
        print()

        # create user
        roh_user = self.create_user(
            "roh@lakra.com",
            "Roh",
            "roh@lakra.com",
            "Rohtash",
            "Lakra",
            True,
            [
                self.create_address(
                    "Tennison Rd",
                    "Hayward",
                    "Washington",
                    "US",
                    "94532"
                )
            ]
        )

        print(f"roh_user:\n{roh_user}")
        print()

        # create user
        san_user = self.create_user(
            "san@lakra.com",
            "Sangita",
            "san@lakra.com",
            "Sangita",
            "Lakra",
            True,
            [
                self.create_address(
                    "Tennison Blvd",
                    "Hayward",
                    "New York",
                    "US",
                    "94534"
                ),
                self.create_address(
                    "Mission Blvd",
                    "Hayward",
                    "Utha",
                    "US",
                    "91534"
                )
            ]
        )

        print(f"san_user:\n{san_user}")
        print()


if __name__ == '__main__':
    # sqlalchemy.__version__
    sqlAlchemyTableObject = SqlAlchemyTableObject()
    sqlAlchemyTableObject.populate_database()
    sqlAlchemyTableObject.fetch_roles()
    sqlAlchemyTableObject.fetch_users()
    sqlAlchemyTableObject.fetch_records()
    sqlAlchemyTableObject.fetch_with_joins()
    sqlAlchemyTableObject.update_records()
    sqlAlchemyTableObject.delete_record()
    print()

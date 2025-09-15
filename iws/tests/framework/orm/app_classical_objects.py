#
# Author: Rohtash Lakra
#
from datetime import datetime

from rest.user.schema import UserSchema, AddressSchema
from rest.role.schema import RoleSchema


class SqlAlchemyClassicalModel:

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
        user = UserSchema(
            user_name="roh@lakra.com",
            password="Roh",
            email="roh@lakra.com",
            first_name="Rohtash",
            last_name="Lakra",
            admin=True,
        )

        if addresses and len(addresses) > 0:
            for address in addresses:
                user.add_address(address)

        return user

    def print_objects(self):
        print(f"print_objects\n")
        # create roles
        roles = (self.create_role("ADMIN"), self.create_role("USER"), self.create_role("GUEST"))
        print(f"roles:\n")
        for role in roles:
            print(f"{role}")
        print()
        # print(f"roles:\n{json.dumps(roles)}")
        # for role in roles:
        #     print(f"{role.to_json()}")
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

    def update_records(self):
        pass


if __name__ == '__main__':
    print()
    sqlAlchemyClassicalModel = SqlAlchemyClassicalModel()
    sqlAlchemyClassicalModel.print_objects()

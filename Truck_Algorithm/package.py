# package class
class Package:
    # constructor of package class
    # spacetime complexity -> O(1)
    def __init__(self, package_id, address, city, state, package_zip, deliveryDeadline, massKilo, note):
        self.delivered_time = None
        self.leave_hub_time = None
        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = package_zip
        self.deliveryDeadline = deliveryDeadline
        self.massKilo = massKilo
        self.note = note

    # method that gathers information for the console inputs.
    # time from console is passed in
    # spacetime complexity -> 0(1)
    def calculate_status(self, time):
        # if the time is less than the truck leave time, it will show the info of the package and the status as at hub
        if time < self.leave_hub_time:
            print(f"-PACKAGE {self.id}, ADDRESS: {self.address}, {self.city} {self.zip}, WEIGHT: {self.massKilo} , "
                  f"DEADLINE: {self.deliveryDeadline}, STATUS: is at Hub at {time}")

        # if the time is more than the delivery time, it will show the info of the package and the status as delivered
        elif time > self.delivered_time:
            print(f"-PACKAGE {self.id}, ADDRESS: {self.address}, {self.city} {self.zip}, WEIGHT: {self.massKilo} , "
                  f"DEADLINE: {self.deliveryDeadline}, STATUS: was delivered at {self.delivered_time}")

        # if none of the above, than the package info will show with status as en route
        else:
            print(f"-PACKAGE {self.id}, ADDRESS: {self.address}, {self.city} {self.zip}, WEIGHT: {self.massKilo} , "
                  f"DEADLINE: {self.deliveryDeadline}, STATUS: is en route at {time}")

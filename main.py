import re, base64, codecs

class UUID4:
    def __init__(self, id):
        """
        :param id: universally unique identifier in uuid version 4 format `39512f4d-fb31-4e08-bd35-69b79d6ae487`
        :type id: string
        """
        self.id = id
    def __str__(self):
        return self.id
    def convert(self):
        hex = re.sub("[{}-]", '', self.id)
        decoded = codecs.decode(bytearray(hex, 'utf-8'), 'hex_codec')
        return BinaryID(base64.b64encode(decoded))

class BinaryID:
    def __init__(self, id):
        """
        :param id: mongodb Binary representation of uuid when coverting using a Python, Golang, etc. driver
        :type id: bytes
        """
        self.id = id
    def __str__(self):
        return self.id.decode()
    def convert(self):
        hex = base64.b16encode(base64.b64decode(self.id)).decode().lower()
        uuid = "-".join([hex[0: 8], hex[8: 12], hex[12: 16], hex[16: 20], hex[20: 32]])
        return UUID4(uuid)

class IDFactory:
    @staticmethod
    def NewID(typeof, id):
        if typeof.lower() == "uuid4":
            return UUID4(id)
        elif typeof.lower() == "binary":
            return BinaryID(id)
        else:
            return None

if __name__ == "__main__":
    while True:
        id_type = input("enter id format (uuid4|binary):")
        id_val = input("enter id:")
        id = IDFactory.NewID(id_type, id_val)
        print("{} => {}".format(id, id.convert() if id else None))

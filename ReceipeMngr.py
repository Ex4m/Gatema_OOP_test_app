
responses = ["y", "yes", ","]


class ReceipeMngr:
    
    
    def Build(self):
        raise NotImplementedError("Build is not implemented")

    def Load(self):
        raise NotImplementedError("Load is not implemented")

    def Store(self):
        raise NotImplementedError("Store is not implemented")

    def OnBuildReceipeHandler(self):
        recipe = Receipe()
        while True:
            user_inp = input("Do you want to add new product? (y/n): ")
            if user_inp.lower() in responses:
                recipe.add_product()
            else:
                pass
        


class Receipe:
    def __init__(self):
        self.products = []

    def add_product(self):
        product = Product()
        self.products.append(product)
        return product


    def remove_product(self, product):
        del product
        self.products.remove(product)


    def rename_product(self, product):
        product.name = input("Enter new name: ")


    def get_product(self, id):
        for product in self.products:
            if product.id == id:
                return product
        return None







import string
import random

class Product:
    _instances = []  # list of all instances of the products
    _next_id = 1  # next avaiable id

    def __init__(self, ):
        self.id = self.generate_id()
        self.thickness = input("Enter thickness: ")
        self.material = input("Enter material: ")
        self.name = self.generate_name()

        
        Product._instances.append(self)
        print(f"id: {self.id}, thickness: {self.thickness}, material: {self.material}, name: {self.name}")
        
    
    @property
    def thickness(self):
        return self._thickness
    
    @thickness.setter
    def thickness(self, value):
        while True:
            try:
                value = int(value)
                if value <= 0:
                    raise ValueError("thickness must be a positive integer")
                break
            except ValueError:
                print("Invalid value for thickness. Please enter a positive integer.")
                value = input("Enter thickness: ")
        self._thickness = value
    
    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        while True:
            if len(value.split()) > 1:
                print("Invalid value for material. Material must be a single word.")
            elif not value.isalpha():
                print("Invalid value for material. Material must contain only letters.")
            else:
                self._material = value
                break

            value = input("Enter material: ")  
        
        
            
    def generate_name(self):
        alphabet = string.ascii_uppercase
        num_letters = len(alphabet)
        # projdeme všechny možné kombinace písmena a čísla v názvu produktu
        while True:
            name = f"Product {alphabet[Product._next_id % num_letters-1]}-{Product._next_id // num_letters + 1}"
            Product._next_id += 1
            # if product with same name not in list of all instances, return name
            if not any(product.name == name for product in Product._instances):
                return name

    def generate_id(self):
        letters = string.ascii_uppercase + string.digits
        return "".join(random.choice(letters) for i in range(8))

    def add_op_pressing(self, product1, product2):
        thickness = product1.thickness + product2.thickness
        material = product1.material + "-" + product2.material
        new_product = Product(thickness, material)
        self._instances.append(new_product)
        self._instances.remove(product1)
        self._instances.remove(product2)
        return new_product
            
    
    def add_op_laminate(self, product1, product2):
        if product1.thickness < product2.thickness:
            product2.thickness += product1.thickness
            product2.material = product1.material + "-" + product2.material
            del product1 #self._instances.remove(product1)
            return product2
        else:
            product1.thickness += product2.thickness
            product1.material = product1.material + "-" + product2.material
            del product2 #self._instances.remove(product2)
            return product1
        
        
    def add_op_custom(self):
        pass
    
            
    
"""product1 = Product(13, "copper")
product2 = Product(20, "laminate")
product3 = Product(30, "Kapton")
product4 = Product(40, "Tape")
product5 = Product(13, "Flex")
prod1 = Product.add_op_pressing(Product, product1, product2)
prod2 = Product.add_op_laminate(Product, prod1, product3 )
prod3 = Product.add_op_pressing(Product, prod1, product5 )"""



recipe_manager = ReceipeMngr()
recipe_manager.OnBuildReceipeHandler()









        
        
        
"""# Example user definition of products

        # Build product A (copper)
        prodcutA = receipe.AddProduct("A")
        prodcutA.AddOpCustom("test operation 1")
        prodcutA.AddOpCustom("test operation 2")
        prodcutA.AddOpCustom("test operation 3")

        # Build product B (laminate)
        prodcutB = receipe.AddProduct("B")
        prodcutB.AddOpCustom("test operation 1")
        prodcutB.AddOpLaminate(prodcutA)    # merge to receipe together by laminating operation
        prodcutB.AddOpCustom("test operation 3")

        # Build product C (Kapton)
        prodcutC = receipe.AddProduct("C")
        prodcutC.AddOpCustom("test operation 1")
        prodcutC.AddOpCustom("test operation 2")

        # Build product D (laminate)
        prodcutD = receipe.AddProduct("D")
        prodcutD.AddOpCustom("test operation 1")
        prodcutB.AddOpLaminate(prodcutC)    # merge to receipe together by laminating operation
        prodcutD.AddOpCustom("test operation 3")

        # Build product E (Kapton)
        prodcutE = receipe.AddProduct("E")
        prodcutE.AddOpCustom("test operation 1")
        prodcutE.AddOpCustom("test operation 2")

        # Build product F (Tape)
        prodcutF = receipe.AddProduct("F")
        prodcutF.AddOpCustom("test operation 1")
        prodcutF.AddOpCustom("test operation 2")

        # Build product G
        prodcutG = receipe.AddProduct("G")
        prodcutG.AddOpCustom("test operation 1")
        p        rodcutG.AddOpCustom("test operation 2")
        prodcutG.AddOpPressing(prodcutB, prodcutD)    # merge to receipe together by pressing operation
        prodcutG.AddOpCustom("test operation 4")
        prodcutB.AddOpLaminate(prodcutE)             # merge to receipe together by laminating operation
        prodcutG.AddOpCustom("test operation 5")
        prodcutB.AddOpLaminate(prodcutF)             # merge to receipe together by laminating operation
        prodcutG.AddOpCustom("test operation 6")"""




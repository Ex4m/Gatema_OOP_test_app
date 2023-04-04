
responses = ["y", "yes", ","]
n_responses = ["n", "no", "not"]
decorator = "*--*--*--*--*--*--*--*--*--*--*--*--*"
decorator2 = "--------------------------------------"
decorator3 = "**************************************"

import pickle

class ReceipeMngr:
    def __init__(self):
        self.receipe = Receipe()
    
    def Build(self):
        raise NotImplementedError("Build is not implemented")

    def save_operation_state(self, file_name):
        data = {
            "receipe": self.receipe.to_dict(),
            "products": [p.to_dict() for p in Product.products]    
            }
        print(data) 
        with open(file_name, 'wb') as file:
            pickle.dump(data, file)
            print("Operation progress saved.")
    
    def load_operation_state(self, file_name):
        with open(file_name, 'rb') as file:
            data = pickle.load(file)
            print("Operation progress loaded.")
        # load receipe
        Receipe.from_dict(data["receipe"], self.receipe)
        # load products
        Product.products = []
        for product_dict in data["products"]:
            product = Product.from_dict(product_dict)
            Product.products.append(product)
    
    def OnBuildReceipeHandler(self):
        print("""
Hello,
welcome to the receipe manager. You can create new receipe or load existing one.
First, you need to add products to the receipe. You can add as many products as you want.
Then you can add operations to the products. You can add as many operations as you want.
At first you will be asked to enter thickness and material of the product.
""")
        self.receipe.init_product_list()
        self.receipe.main_menu()

        
        
        
    
            
                
class Receipe:
    def __init__(self):
        self.step = 1
        self.num_pairs = None
        self.sub_product_list = []
        self.product_pairs = []
        self.unmodified_products = []
            
    def show_products(self):
        print(decorator2)
        for product in Product.products:
            product.get_info()
        print(decorator2)
    
    def show_sub_products(self, unmodified_products):
        if len(Product.products) == 0:
            print("No products available.")
            return
        print(decorator2)
        print("Available products:")
        for p in Product.products:
            if p in unmodified_products:
                p.get_info()
        print(decorator2)    

    
    def add_product(self):
        thickness = input("Enter thickness: ")
        material = input("Enter material: ")
        product = Product(thickness=thickness, material=material)
        Product.products.append(product)
        return product

    def remove_product(self, product):
        Product.products.remove(product)

    def rename_product(self, product):
        product.name = input("Enter new name: ")

    def get_product(self, identifier):
        for product in Product.products:
            if product._id == identifier or product._name == identifier:
                return product
        return None

    def init_product_list(self):
        while True:
            user_inp = input("Do you want to add a new product? (y/n): ")
            if user_inp.lower() in responses:
                self.add_product()
                for product in Product.products:
                    product.get_info()
            else:
                break
    
    def generate_pairs(self, unmodified_products):
        if len(unmodified_products) < 2:
            print("You don't have enough products. Please add more products.")
            return None, None
        self.show_sub_products(unmodified_products)
        product1 = None
        product2 = None
        print("Select products to be used in the operation.")
        for i in range(2):
            while True:
                product_id_name = input(f"Enter name or ID of the {i+1}. product: ")
                product = self.get_product(product_id_name)
                if product not in unmodified_products:
                    print("Product not found. Please try again.")
                elif product.was_used:
                    print("Product already used. Please choose another.")
                else:
                    product.was_used = True
                    if i == 0:
                        product1 = product
                    else:
                        product2 = product
                    break
        return product1, product2
    
    # function returning num_pairs based on user input, but not more than half of the products
    def inp_num_pairs(self):
        while True:
            try:
                self.num_pairs = int(input("How many initial product pairs do you want to create? "))
                if self.num_pairs > 0:
                    if self.num_pairs * 2 <= len(Product.products):
                        return self.num_pairs
                    else:
                        response = input("You don't have enough products. Do you want to add more? (y/n): ")
                        if response.lower() in responses:
                            self.init_product_list()
                            self.operation_step()
                        else:
                            print("Returning to main menu.")   
                else:
                    print("Please enter a positive integer.")
            except ValueError:
                print("Please enter a positive integer.")
                    
    def operation_step(self):
        while True:
            self.num_pairs = self.inp_num_pairs()
            self.sub_product_list = Product.products.copy()
            print(decorator3 + f"\nSTEP {self.step}\n" + decorator3)
            print(f"Creating {self.num_pairs} product pair..." if self.num_pairs == 1 else f"Creating {self.num_pairs} product pairs...")
            for i in range(self.num_pairs):
                print(decorator2)
                print(f"Work on pair {i+1}/{self.num_pairs}")
                self.unmodified_products = [p for p in self.sub_product_list if not p.was_used]
                if len(self.unmodified_products) < 2:
                    print("Not enough unmodified products to create a pair. Returning to main menu.")
                    break
                product1, product2 = self.generate_pairs(self.unmodified_products)
                if product1 is not None and product2 is not None:
                    print(decorator)
                    print("1. Add laminate operation")
                    print("2. Add pressing operation")
                    print("3. Add custom operation")
                    print(decorator) 
                    op_choice = input("Enter operation choice: ")
                    
                    if op_choice == "1":
                        Operations.add_op_laminate(product1, product2)
                    elif op_choice == "2":
                        Operations.add_op_pressing(product1, product2)
                    elif op_choice == "3":
                        op_name = input("Enter custom operation name: ")
                        Operations.add_op_custom(op_name)
                    else:
                        print("Invalid operation choice.") 
                    # Set was_used to True for both products
                    product1.was_used = True
                    product2.was_used = True
                else:
                    print("Invalid product pair.")
                    continue
            for product in Product.products:
                product.was_used = False                        
            self.step += 1   
            print(decorator3)
            print("Current products (after operation step)")
            self.show_products()
            #print(f"Number of pairs left: {num_pairs}")
            if self.num_pairs >= 0:
                print(decorator2)
                if len(Product.products) <= 1:
                    print("OPERATION FINISHED, Returning to main menu")
                    break
                next_step = input("Do you want to continue to the next step? (y/n) ")
                if next_step.lower() in n_responses:
                    print("Returning to main menu.")
                    break
                elif next_step.lower() not in n_responses and next_step.lower() not in responses:
                    print("Invalid input. Continuing to the next step.")
                else:
                    print("Continuing to the next step.")   
                                
        
    
            
    def main_menu(self):
        while True:
            print(decorator2)
            print("MAIN MENU")
            print("1. Rename a product")
            print("2. Remove a product")
            print("3. Add a product to product list")
            print("4. *Start building a receipe/PCB*")
            print("5. Show me a list of products")
            print("6. Save operation progress to file")
            print("7. Load operation progress from file")
            print("8. TEST step")
            print("10. Exit")
            print(decorator2)
            choice = input("Enter a number to choose an option: ")

            if choice == "1":
                id = input("Enter the id of the product you want to rename: ")
                product = self.get_product(id)
                if product is None:
                    print("Product not found")
                else:
                    self.rename_product(product)

            elif choice == "2":
                id = input("Enter the id of the product you want to remove: ")
                product = self.get_product(id)
                if product is None:
                    print("Product not found")
                else:
                    self.remove_product(product)
                    
            elif choice == "3":
                self.init_product_list()

            
            elif choice == "4":
                self.operation_step()
                input("Press enter key to continue...")     
                
            elif choice == "5":
                self.show_products()  
                print("\n")
                input("Press enter key to continue...")              

            elif choice == "6": 
                receipe_manager.save_operation_state("Products.pickle")
                input("Press enter key to continue...")
                
            elif choice == "7":
                receipe_manager.load_operation_state("Products.pickle")
                input("Press enter key to continue...")
                    
            elif choice == "8":
                print(self.step)
                print("\n")
                print(self.to_dict())
                
            elif choice == "10":
                print("Exiting...")
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and X.")

    def to_dict(self):
        print(self.step)
        return {
            "step": self.step,
            "num_pairs": self.num_pairs,
            "sub_product_list": self.sub_product_list,
            "product_pairs": self.product_pairs,
            "unmodified_products": self.unmodified_products
        }
        
    
    @staticmethod
    def from_dict(data, receipe):
        receipe.step = data["step"]
        receipe.num_pairs = data["num_pairs"]
        receipe.sub_product_list = data["sub_product_list"]
        receipe.product_pairs = data["product_pairs"]
        receipe.unmodified_products = data["unmodified_products"]
        print(receipe.step)
        
    
    def __getstate__(self):
        state = self.__dict__.copy()
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)



import string
import random
import re
    
    
    
    
class Product:
    
    _next_id = 1  # next avaiable id
    products = []
    
    def __init__(self, thickness, material):
            self.thickness = thickness
            self.material = material
            self._name = self.generate_name()
            self._id = self.generate_id()
            self.was_used = False
            #self.products.append(self)
        
    def get_info(self):
        print(f"id: {self._id}, thickness: {self.thickness}, material: {self.material}, name: {self._name}, used this step: {self.was_used}")
    
        
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
        pattern = r'^[a-zA-Z]+(-[a-zA-Z]+)*$'  # regular expression to match word-word-word format
        while True:
            if not re.match(pattern, value):
                print("Invalid value for material. Material must be in word-word-word format and contain only letters and hyphens.")
            else:
                self._material = value.title()
                break

            value = input("Enter material: ")

    def generate_name(self):
        alphabet = string.ascii_uppercase
        num_letters = len(alphabet)
        while True:
            name = f"{alphabet[Product._next_id % num_letters-1]}_{Product._next_id // num_letters + 1}"
            Product._next_id += 1
            if not any(product._name == name for product in self.products):
                return name


    def generate_id(self):
        letters = string.ascii_uppercase + string.digits
        while True:
            new_id = "".join(random.choice(letters) for i in range(8))
            if not any(product._id == new_id for product in Product.products):
                return new_id

    def to_dict(self):
        return {
            "thickness": self.thickness,
            "material": self.material,
            "_name": self._name,
            "_id": self._id,
            "was_used": self.was_used
        }

    @classmethod
    def from_dict(cls, product_dict):
        product = cls(thickness=product_dict["thickness"], material=product_dict["material"])
        product._name = product_dict["_name"]
        product._id = product_dict["_id"]
        product.was_used = product_dict["was_used"]
        return product


        
    
    
class Operations:
    modified_products = []
    
    @classmethod
    def add_op_pressing(cls, product1, product2):
        thickness = product1.thickness + product2.thickness
        material = product1.material + "-" + product2.material
        new_product = Product(thickness=thickness, material=material)
        new_product.was_used = True
        Product.products.append(new_product)
        Product.products.remove(product1)
        Product.products.remove(product2)
        print("Pressing operation done.")
        return new_product

    @classmethod
    def add_op_laminate(cls, product1, product2):
        if product1.thickness < product2.thickness:
            product2.thickness += product1.thickness
            product2.material = product1.material + "-" + product2.material
            product2.was_used = True
            Product.products.remove(product1)
            print("Laminate operation done.")
            return product2
        else:
            product1.thickness += product2.thickness
            product1.material = product1.material + "-" + product2.material
            product1.was_used = True
            Product.products.remove(product2)
            print("Laminate operation done.")
            return product1

        
    @classmethod        
    def add_op_custom(cls, op_name):
        cls.op_name = op_name
        print(op_name)
    
 

     
    
            
    
"""product1 = Product(13, "copper")
product2 = Product(20, "laminate")
product3 = Product(30, "Kapton")
product4 = Product(40, "Tape")
product5 = Product(13, "Flex")
prod1 = Product.add_op_pressing(Product, product1, product2)
prod2 = Product.add_op_laminate(Product, prod1, product3 )
prod3 = Product.add_op_pressing(Product, prod1, product5 )"""



receipe_manager = ReceipeMngr()
receipe_manager.OnBuildReceipeHandler()









        
        
        
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




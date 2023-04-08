
responses = ["y", "yes", ","]
n_responses = ["n", "no", "not"]
decorator = "*--*--*--*--*--*--*--*--*--*--*--*--*"
decorator2 = "--------------------------------------"
decorator3 = "**************************************"

import pickle
from anytree import Node, RenderTree, NodeMixin, iterators
import string
import random
import re



class ReceipeMngr:
    def __init__(self):
        self.receipe = Receipe()
        self.receipe_tester = ReceipeTester(self.receipe)
        
    def Build(self):
        raise NotImplementedError("Build is not implemented")

    def save_operation_state(self, file_name):
        self.receipe_tester.root_node = self.receipe_tester.create_tree()  # aktualizace root_node
        data = {
            "receipe": self.receipe.to_dict(),
            "products": [p.to_dict() for p in Product.products],
            "tree_root": pickle.dumps(self.receipe_tester.root_node)  # použití aktualizovaného root_node
        }
        with open(file_name, 'wb') as file:
            pickle.dump(data, file)
        print("Operation progress saved.")

    def load_operation_state(self, file_name):
        with open(file_name, 'rb') as file:
            data = pickle.load(file)
        # load receipe
        Receipe.from_dict(data["receipe"], self.receipe)
        # load products
        Product.products = []
        for product_dict in data["products"]:
            product = Product.from_dict(product_dict)
            Product.products.append(product)
        # load nodes
        root_node = pickle.loads(data["tree_root"])
        self.receipe_tester.root_node = root_node
        print("Operation progress loaded.")
    
    def OnBuildReceipeHandler(self):
        print("""
Hello,
welcome to the receipe manager. You can create new receipe or load existing one.
First, you need to add products to the receipe. You can add as many products as you want.
Then you can add operations to the products. You can add as many operations as you want.
At first you will be asked to enter thickness and material of the product.
""")
        self.receipe.init_product_list()
        self.main_menu()
        
        
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
            print("8. Print Tree (Work in Progress)")
            print("9. TEST nodes list")
            print("10. Print Pressing count")
            print("11. Print Product path(Work in Progress)")
            print("15. Exit")
            print(decorator2)
            choice = input("Enter a number to choose an option: ")

            if choice == "1":
                id = input("Enter the id of the product you want to rename: ")
                product = self.receipe.get_product(id)
                if product is None:
                    print("Product not found")
                else:
                    self.receipe.rename_product(product)

            elif choice == "2":
                id = input("Enter the id of the product you want to remove: ")
                product = self.receipe.get_product(id)
                if product is None:
                    print("Product not found")
                else:
                    self.receipe.remove_product(product)
                    
            elif choice == "3":
                self.receipe.init_product_list()

            
            elif choice == "4":
                self.receipe.operation_step()
                input("Press enter key to continue...")     
                
            elif choice == "5":
                self.receipe.show_products()  
                print("\n")
                input("Press enter key to continue...")              

            elif choice == "6": 
                receipe_manager.save_operation_state("Products.pickle")
                input("Press enter key to continue...")
                
            elif choice == "7":
                receipe_manager.load_operation_state("Products.pickle")
                input("Press enter key to continue...")
                    
            elif choice == "8":
                self.receipe_tester.print_product_tree()
                input("Press enter key to continue...")  
            
            elif choice == "9":
                print(self.receipe.nodes_list)
                input("Press enter key to continue...")  
            
            elif choice == "10":
                print(f"Pressing count: {self.receipe_tester.print_press_count()}")
                input("Press enter key to continue...") 
            
            elif choice == "11":
                print(f"Product path is: {self.receipe_tester.print_product_path()}")
                input("Press enter key to continue...") 
                
            elif choice == "15":
                print("Exiting...")
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and X.")    
        
    
            
                
class Receipe:
    def __init__(self):
        self.step = 1
        self.num_pairs = None
        self.sub_product_list = []
        self.product_pairs = []
        self.unmodified_products = []
        self.operations = []
        self.root_node = Node("PCB Production Process")
        self.nodes_list = []
        self.pressing_count = 0
            
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
        return product.name

    def get_product(self, identifier):
        for product in Product.products:
            if product._id == identifier or product.name == identifier:
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
                self.want_quit = False
                if self.num_pairs > 0:
                    if self.num_pairs * 2 <= len(Product.products):
                        return self.num_pairs, self.want_quit
                    else:
                        response = input("You don't have enough products. Do you want to add more? (y/n): ")
                        if response.lower() in responses:
                            self.init_product_list()
                            self.operation_step()
                        else:
                            print("Returning to main menu.")   
                            self.want_quit = True
                            self.num_pairs = 0
                            return self.num_pairs, self.want_quit
                else:
                    print("Please enter a positive integer.")
            except ValueError:
                print("Please enter a positive integer.")
                    
    def operation_step(self):
        """
        Creates nodes in the tree representing each step of the operation and appends them to the nodes_list.
        """
        root_node = self.root_node
        while True:
            self.num_pairs, self.want_quit = self.inp_num_pairs()
            if self.want_quit:
                break
            self.sub_product_list = Product.products.copy()
            #new_step_node = Node(f"Step {self.step}", parent=root_node)
            #self.nodes_list.append(new_step_node)
            for i in range(self.num_pairs):
                #new_work_node = Node(f"Work on pair {i+1}/{self.num_pairs}", parent=new_step_node)
                #self.nodes_list.append(new_work_node)
                self.unmodified_products = [p for p in self.sub_product_list if not p.was_used]
                if len(self.unmodified_products) < 2:
                    print("Not enough unmodified products to create a pair. Returning to main menu.")
                    break
                product1, product2 = self.generate_pairs(self.unmodified_products)
                if product1 is not None and product2 is not None:
                    print(decorator3)
                    op_choice = input("Choose operation: \n1. Laminating operation\n2. Pressing operation\n3. Custom operation\n")
                    print(decorator3)
                    if op_choice == "1":
                        Operations.add_op_laminate(product1, product2)
                        new_op_name = "Laminate"
                    elif op_choice == "2":
                        Operations.add_op_pressing(product1, product2)
                        new_op_name = "Pressing"
                        self.pressing_count += 1
                    elif op_choice == "3":
                        op_name = input("Enter custom operation name: ")
                        Operations.add_op_custom(op_name)
                        new_op_name = op_name
                    else:
                        print("Invalid operation choice.")
                        continue
                    #new_op_node = Node(f"{new_op_name} ({product1._name}-{product2._name})", parent=new_work_node)
                    #self.nodes_list.append(new_op_node)
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
            if len(Product.products) <= 1:
                final_node = Node(f"Final Product: {Product.products[0].name}")
                self.nodes_list.append(final_node)
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




    
    
    
class Product(NodeMixin):
    
    _next_id = 1  # next avaiable id
    products = []
    history = []
    
    def __init__(self, thickness, material):
            self.thickness = thickness
            self.material = material
            self.name = self.generate_name()
            self._id = self.generate_id()
            self.was_used = False
            self.child = None
            self.parent = None
            #self.products.append(self)
        
    def get_info(self):
        print(f"id: {self._id}, thickness: {self.thickness}, material: {self.material}, name: {self.name}")
    
    def set_child(self, child):
        self.child = child
        child.parent = self
        
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
            if not any(product.name == name for product in self.products):
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
            "name": self.name,
            "_id": self._id,
            "was_used": self.was_used
        }

    @classmethod
    def from_dict(cls, product_dict):
        product = cls(thickness=product_dict["thickness"], material=product_dict["material"])
        product.name = product_dict["name"]
        product._id = product_dict["_id"]
        product.was_used = product_dict["was_used"]
        return product


        
    
    
class Operations(NodeMixin):
        
    @classmethod
    def add_op_pressing(cls, product1, product2):
        thickness = product1.thickness + product2.thickness
        material = product1.material + "-" + product2.material
        new_product = Product(thickness=thickness, material=material)
        new_product.was_used = True
        Product.products.append(new_product)
        for i in (product1,product2):
            new_product.set_child(i)
            Product.history.append(i)
            Product.products.remove(i)
        print("Pressing operation done.")
        return new_product
    
    @classmethod
    def add_op_laminate(cls, product1, product2):
        if product1.thickness < product2.thickness:
            product2.thickness += product1.thickness
            product2.material = product1.material + "-" + product2.material
            product2.was_used = True
            product2.set_child(product1)
            Product.history.append(product1)
            Product.products.remove(product1)
            print("Laminate operation done.")
            return product2
        else:
            product1.thickness += product2.thickness
            product1.material = product1.material + "-" + product2.material
            product1.was_used = True
            product1.set_child(product2)
            Product.history.append(product2)
            Product.products.remove(product2)
            print("Laminate operation done.")
            return product1

        
    @classmethod        
    def add_op_custom(cls, op_name):
        cls.op_name = op_name
        print(op_name)
    
 

    



class ReceipeTester(NodeMixin):
    def __init__(self, receipe):
        self.receipe = receipe
        self.root_node = None
        self.preorderiter = iterators.PreOrderIter(self.root_node)
        
    def print_product_tree(self):
        if len(Product.products) > 1:
            print("Operation process not yet finished. Please finish the operation process before printing the tree.")
            return
            
        que = input("Do you want to print the full tree? (y/n): ")
        self.root_node = self.create_tree()
        if que in responses:
            for pre, _, node in RenderTree(self.root_node):
                print(f"{pre}{node.name}")
                print(f"{pre} parent: {node.parent.name if node.parent else None}")
                print(f"{pre} children: {[child.name for child in node.children]}\n")
        else:
            for pre, _, node in RenderTree(self.root_node):
                print(f"{pre}{node.name}")

    
    def create_tree(self):
        if self.root_node is None:
            # find the root node in the Product.products list
            root_product = next((p for p in Product.products if p.name == self.root_node), None)
            if not root_product:
                print(f"Root product '{self.root_node}' not found in Product.products")
                return None
            
            # create the root node and add it to the tree
            self.root_node = Node(root_product.name)
            
            # create the rest of the nodes and add them to the tree
            for node in Product.history:
                # skip the root node since we already added it
                if node.name == self.root_node:
                    continue
                
                parent_node = self.root_node
                for ancestor in node.ancestors:
                    for child in parent_node.children:
                        if child.name == ancestor.name:
                            parent_node = child
                            break
                    else:
                        parent_node = Node(ancestor.name, parent=parent_node)
                Node(node.name, parent=parent_node)
        return self.root_node



    
    
    def print_press_count(self):
        return self.receipe.pressing_count

        
    
    def print_max_depth():
        #Projde strukturu stromu a vytiskne „počet úrovní“ produktu/postupu (zohlednění operací lisování/laminování).
        #Tzn. na příkladu výše je nejhlouběji produkt A (a C) protože, produkt A je zanořen do Produktu B => Produkt B je zanořen do produktu G => tedy dvě zanoření, výsledek je 2
        pass
    
    def print_product_path(self):
        if self.root_node is None:
            print("Operation process not yet finished. Please finish the operation process before printing the tree path.")
            return
        inp = input("Enter product name: ")
        for node in self.preorderiter:
            if node.name == inp:
                path = [node.name]
                while node.parent is not None:
                    node = node.parent
                    path.append(node.name)
                path.reverse()
                print(" => ".join(path))
                break

        

    
    def remove_op_by_order(self, product_id, op_order):
        #Před vytisknutím postupu může být zavolána tato metoda, která modifikuje nadefinovaný postup tak, že odstraní jednu operaci z konkrétního postupu podle pořadí operace.
        #Metoda přijímá dva argumenty: Id produktu, Pořadí operace, která má být smazána. Změny se NEukládají na disk, operace probíhá pouze v paměti RAM
        product = Product.get_product_by_id(product_id)
        if product:
            if len(product.operations) > op_order-1:
                del product.operations[op_order-1]
                print(f"Operation {op_order} has been removed from product {product.name}.")
            else:
                print(f"Product {product.name} does not have {op_order} operations.")
        else:
            print(f"Product {product_id} not found.")


        
    def print_to_file():
        #Vytiskne postup do soborů typu txt do složky Output v kořenovém adresáři projektu. 
        #Důležité je, aby se postup načítal z disku. Ukázku výstupů najdete ve zdrojových kódech ve složce Output. Ukázky odpovídají našemu příkladu ze zadání.
        pass
    
    
    

receipe_manager = ReceipeMngr()
receipe_manager.OnBuildReceipeHandler()

   



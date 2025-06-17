# Capstone Project - Product Listing Application
# Rojwa Legiana Rachmiadi
# JCDSOH01-002-online

#------------ USER NAME ------------#
def name():
  while True:
    username = input("Please enter your name: ").strip().title()
    if username.isalpha():
      return username
    else:
      print("\n❗️Invalid input. Use alphabets only.\n")

#------------ MENU ------------#
def menu():
  username = name()
  while True:
    print(f"""
============================
🏠 The Home & Living Store 🪴
============================
Welcome to the store, {username}!

What would you like to do today?

1. Add Product Listing
2. Browse Data
3. Update Data
4. Remove Data
5. Restore Data

Enter 'q' to exit
""")
    options = input("Select menu by number (1-5): ")

    if options == "1":
      add(username)
    elif options == "2":
      browse()
    elif options == "3":
      update(username)
    elif options == "4":
      remove(username)
    elif options == "5":
      restore(username)
    elif options == "q":
      print("\nExiting program...")
      break
    else:
      print("❗️Invalid input. Please enter a number (1-5).")

#------------ 0. HELPER VARIABLES ------------#
# to recall in functions and avoid code repetition

# DICTIONARIES
listing = {}
trash = {}

# IMPORT
from datetime import datetime, timedelta
from tabulate import tabulate

## to export to csv
import csv
def export_to_csv(data, filename="product_catalog.csv"):
  if not data:
    print("❗️Database is empty. Please add a product listing.")
    return "q"
  first_prod = list(data.values())[0]
  headers = ["ID"] + list(first_prod.keys())
  with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    for prod_id, product in data.items():
      row = [prod_id] + [product.get(key, "") for key in first_prod.keys()]
      writer.writerow(row)

    print(f"✅ Product data exported to '{filename}' successfully.")


# OPTIONS
category = ["Furniture", "Storage & Organization", "Kitchen & Dining", "Home Décor & Lighting", "Bed & Bath"]
color = ["White", "Black", "Gray", "Brown", "Others"]
material = ["Wood", "Metal", "Glass & Acrylic", "Recycled", "Others"]

# DUMMY DATA
listing = {
    "PR0001": {
        "Product name": "LACK Coffee Table",
        "Price": 299000,
        "Category": "Furniture",
        "Material": "Wood",
        "Color": "White",
        "Size": "90 x 55 x 45 cm",
        "Weight": "5.50 kg",
        "Created by": "Ana at 10/06/2025, 10:00",
        "Last edited by": "Jane at 10/06/2025, 10:00"
    },
    "PR0002": {
        "Product name": "KALLAX Shelf Unit",
        "Price": 850000,
        "Category": "Storage & Organization",
        "Material": "Recycled",
        "Color": "Black",
        "Size": "77 x 147 x 39 cm",
        "Weight": "18.00 kg",
        "Created by": "John at 10/06/2025, 10:15",
        "Last edited by": "John at 10/06/2025, 10:15"
    },
    "PR0003": {
        "Product name": "GRUNKA Kitchen Utensil Set",
        "Price": 129000,
        "Category": "Kitchen & Dining",
        "Material": "Glass & Acrylic",
        "Color": "Gray",
        "Size": "30 x 10 x 5 cm",
        "Weight": "0.75 kg",
        "Created by": "John at 10/06/2025, 10:30",
        "Last edited by": "Ana at 10/06/2025, 11:00"
    },
    "PR0004": {
        "Product name": "FADO Table Lamp",
        "Price": 199000,
        "Category": "Home Décor & Lighting",
        "Material": "Metal",
        "Color": "White",
        "Size": "25 x 25 x 30 cm",
        "Weight": "1.10 kg",
        "Created by": "Jack at 10/06/2025, 11:10",
        "Last edited by": "Ana at 10/06/2025, 11:10"
    },
    "PR0005": {
        "Product name": "RÅGRUND Towel Rack",
        "Price": 449000,
        "Category": "Bed & Bath",
        "Material": "Glass & Acrylic",
        "Color": "Brown",
        "Size": "65 x 45 x 130 cm",
        "Weight": "3.20 kg",
        "Created by": "John at 10/06/2025, 11:25",
        "Last edited by": "John at 10/06/2025, 11:25"
    }
}

# PRODUCT NAME VALIDATION

def name_valid(prompt):
    while True:
        name_input = get_input(prompt)
        if name_input == "q":
            return "q"
        if name_input:
            return name_input.title()
        else:
            print("❗️Product name cannot be empty.")


# POSITIVE VALUES VALIDATION FOR PRODUCT MEASUREMENTS
def is_positive(value):
  try:
    return float(value)>0
  except ValueError:
    return False

# CATEGORY VALIDATION

def cat_select():
    while True:
        print("""
---------------------------
🪑 Select Product Category:\n""")
        for i, cat in enumerate(category, 1):
            print(f"{i}. {cat}")

        cat_input = get_input("\nEnter a number (1–5): ")
        if cat_input == "q":
          return "q"
        if cat_input.isnumeric():
            cat_int = int(cat_input)
            if 1 <= cat_int <= len(category):
                return category[cat_int - 1]
            else:
                print("❗️Invalid input. Please enter a number (1-5).")
        else:
            print("❗️Invalid input. Please enter a number (1-5).")

# MATERIAL VALIDATION

def mat_select():
  print("""
---------------------------------
🛠️ Select Product Material:\n""")
  for i, mat in enumerate(material, 1):
    print(f"{i}. {mat}")

  while True:
    mat_input = get_input("\nEnter a number (1–5): ")
    if mat_input == "q":
      return "q"
    if mat_input.isnumeric():
        mat_int = int(mat_input)
        if 1 <= mat_int <= len(material):
            return material[mat_int-1]
        else:
            print("❗️Invalid input. Please enter a number (1-5).")
    else:
        print("❗️Invalid input. Please enter a number (1-5).")


# PRICE VALIDATION

def price_valid(prompt):
    while True:
        price = get_input(prompt)
        if price == "q":
            return "q"
        if price.isnumeric():
            price = int(price)
            price_upd = f"Rp{price:,}".replace(",", ".")
            print(f"## Price (IDR): {price_upd}")
            return price
        else:
            print("❗️Invalid input. Please enter whole numbers only.")


# DIMENSIONS VALIDATION

def dimensions():
    print("""
-----------------------------
📐 Product Measurements\n""")
    while True:
        length = get_input("Length (cm): ")
        if length == "q":
            return "q"
        width = get_input("Width (cm): ")
        if width == "q":
            return "q"
        height = get_input("Height (cm): ")
        if height == "q":
            return "q"
        if all(is_positive(pos) for pos in [length, width, height]):
            return f"{length} x {width} x {height} cm"
        else:
            print("❗ Please enter numeric values for all dimensions.\n")

# WEIGHT VALIDATION

def weight():
  while True:
    w = get_input("Weight (kg): ")  # Use get_input here for consistency
    if w == "q":
      return "q"
    if is_positive(w):
      return f"{float(w):.2f} kg"
    else:
      print("❗ Please enter numeric values only.\n")

# COLOR VALIDATION

def col_select():
  print("""
---------------------------
🎨 Select Product Color:\n""")
  for i, col in enumerate(color,1):
    print(f"{i}. {col}")

  while True:
    col_input = get_input("\nEnter a number (1–5): ")
    if col_input == "q":
      return "q"
    if col_input.isnumeric():
      col_int = int(col_input)
      if 1 <= col_int <= len(color):
        return color[col_int-1]
    else:
      print("❗️Invalid input. Please enter a number (1-5).")

# DATA DISPLAY - per PROD ID

def display_prod(prod_id, product):
    print(f"\nProduct ID: {prod_id}")
    print("-" * 40)
    for key, value in product.items():
        print(f"{key:<20}: {value}")
    print("-" * 40)

# DATA DISPLAY - ALL
def display(data):
  if not data:
    print("❗️Database is empty. Please add a product listing.")
    return

  prod_table = []

  for prod_id, product in data.items():
      row = [
          prod_id,
          product.get("Product name", ""),
          product.get("Price", ""),
          product.get("Category", ""),
          product.get("Material", ""),
          product.get("Color", ""),
          product.get("Size", ""),
          product.get("Weight", ""),
          product.get("Created by", ""),
          product.get("Last edited by", "")
      ]

      prod_table.append(row)
  headers = ["ID", "Name", "Price", "Category", "Material", "Color", "Size", "Weight", "Created by", "Last edited by"]
  print(tabulate(prod_table, headers=headers, tablefmt="rounded_outline"))

# AUTO-GENERATE PRODUCT ID
def generate_prod_id():
  all_ids = listing.keys() | trash.keys()
  num = [int(pid[2:]) for pid in all_ids if pid.startswith("PR")]
  return "PR" + str(max(num, default=0) + 1).zfill(4)

# KEYWORD
def keyword_search():
    while True:
        if not listing:
            print("❗️Database is empty. Please add data.")
            return

        display(listing)
        keyword = get_input("\nEnter keyword (or q to return): ").lower()
        if keyword == "q":
            return

        results = {}
        for prod_id, product in listing.items():
            if (
                keyword in prod_id.lower() or
                keyword in product.get("Product name", "").lower() or
                keyword in product.get("Color", "").lower() or
                keyword in product.get("Material", "").lower() or
                keyword in product.get("Category", "").lower()
            ):
                results[prod_id] = product

        if results:
            display(results)
            result = export_prompt(results, "product_search_results.csv")
            if result == "menu":
              break
        else:
            print("\n❗ No matching products found.\n")

# EXPORT TO CSV

def export_prompt(data, filename):
    while True:
        print("""
Would you like to export this to .csv?

1. Yes
2. Return to browse data

Press q to return to menu
""")
        export = get_input("Enter 1, 2, or q: ")

        if export == "1":
            export_to_csv(data, filename)

        elif export == "2":
            return "browse"

        elif export == "q":
            return "menu"

        else:
            print("❗ Invalid input. Please enter 1, 2, or q.\n")

# RETURN TO MAIN MENU

def get_input(prompt):
    value = input(prompt).strip()
    if value.lower() == 'q':
        print("\n↩️ Returning to menu...\n")
        return "q"
    return value


#------------ 1. ADD PRODUCT LISTING ------------#

def add(username):
    while True:
        print("""
============================
🛒 Add New Product Listing 🛒
============================
Press 'q' to return to menu.
""")

        prod_nm = name_valid("Product name: ")
        if prod_nm == "q": break
        prod_pc = price_valid("Product price: ")
        if prod_pc == "q": break
        prod_size = dimensions()
        if prod_size == "q": break
        prod_weight = weight()
        if prod_weight == "q": break
        prod_cat = cat_select()
        if prod_cat == "q": break
        prod_mat = mat_select()
        if prod_mat == "q": break
        prod_color = col_select()
        if prod_color == "q": break

        new_product = {
            "Product name": prod_nm,
            "Price": prod_pc,
            "Category": prod_cat,
            "Material": prod_mat,
            "Color": prod_color,
            "Size": prod_size,
            "Weight": prod_weight
        }

        duplicate_found = False
        for existing in listing.values():
            if all(existing.get(k) == new_product[k] for k in new_product):
                duplicate_found = True
                break

        if duplicate_found:
            print("\n❗ Product already exists. Please re-check your input.\n")
            again = get_input("Try adding a different product? (1: Yes, Any key: No): ")
            if again != "1":
                print("\n↩️ Returning to menu...\n")
                break
            else:
                continue

        prod_id = generate_prod_id()
        now = (datetime.utcnow() + timedelta(hours=7)).strftime("%d/%m/%Y, %H:%M:%S")
        new_product["Created by"] = f"{username} at {now}"
        new_product["Last edited by"] = f"{username} at {now}"
        listing[prod_id] = new_product

        display_prod(prod_id, listing[prod_id])
        print("\n✅ Product added successfully.")

        again = get_input("\nAdd another product? (1: Yes, Any key: No): ")
        if again != "1":
            print("\n↩️ Returning to menu...\n")
            break

#------------ 2. BROWSE PRODUCT LISTING ------------#

def browse():
    while True:
        print("""
============================
🔎 Browse Product Listing 🔎
============================

1. View All Product Listings
2. Search by Keyword
3. View by Price: Low to High
4. View by Price: High to Low

Press q to return to menu
""")
        choice = get_input("Enter a number (1-4) or q: ")

        if choice == "1":
            display(listing)
            result = export_prompt(listing, "product_listing_all.csv")
            if result == "menu":
                break

        elif choice == "2":
            keyword_search()

        elif choice == "3":
            sorted_list = dict(sorted(listing.items(), key=lambda x: x[1]["Price"]))
            display(sorted_list)
            result = export_prompt(sorted_list, "product_listing_low_to_high.csv")
            if result == "menu":
                break

        elif choice == "4":
            sorted_list = dict(sorted(listing.items(), key=lambda x: x[1]["Price"], reverse=True))
            display(sorted_list)
            result = export_prompt(sorted_list, "product_listing_high_to_low.csv")
            if result == "menu":
                break

        else:
            print("❗ Invalid input. Please enter 1-4 or q.\n")

#------------ 3. UPDATE PRODUCT LISTING ------------#

def update(username):
    print("""
============================
📝 Update Product Listing 📝
============================
Press 'q' to return to menu.
""")

    if not listing:
        print("\n❗️Database is empty.")
        return

    display(listing)

    # Loop for valid product ID
    while True:
        prod_id = get_input("\nEnter Product ID to update: ").upper()
        if prod_id == "Q":
            print("\n↩️ Returning to menu...\n")
            return
        if prod_id in listing:
            break
        else:
            print("\n❗️Product ID not found. Please try again.")

    product = listing[prod_id]
    display_prod(prod_id, product)

    while True:
        options = ["Product name", "Price", "Category", "Color", "Size", "Weight"]
        for i, field in enumerate(options, 1):
            print(f"{i}. {field}")

        choice = get_input("""
Press q to return to menu

Select a field to update by number (1-6): """)
        if choice.lower() == "q":
            break
        if not choice.isdigit() or not 1 <= int(choice) <= len(options):
            print("\n❗️Invalid choice.\n")
            continue

        selected = options[int(choice) - 1]

        if selected == "Product name":
            new_val = name_valid("\nNew Product Name: ")
        elif selected == "Price":
            new_val = price_valid("\nNew Price: ")
        elif selected == "Category":
            new_val = cat_select()
        elif selected == "Color":
            new_val = col_select()
        elif selected == "Size":
            new_val = dimensions()
        elif selected == "Weight":
            new_val = weight()

        if new_val == "q":
            break

        updated_product = product.copy()
        updated_product[selected] = new_val

        duplicate_found = False
        for pid, existing in listing.items():
            if pid == prod_id:
                continue
            if all(existing.get(k) == updated_product[k] for k in updated_product):
                duplicate_found = True
                break

        if duplicate_found:
            print("\n❗ Another product with these details already exists.")
            again = get_input("Try updating a different field? (1: Yes, Any key: No): ")
            if again != "1":
                break
            else:
                continue
        else:
            product[selected] = new_val
            now = (datetime.utcnow() + timedelta(hours=7)).strftime("%d/%m/%Y, %H:%M:%S")
            product["Last edited by"] = f"{username} at {now}"
            display_prod(prod_id, product)
            print("\n✅ Product successfully updated.")

            again = get_input("\nUpdate another field for this product? (1: Yes, Any key: No): ")
            if again != "1":
                break

    again = get_input("\nUpdate another product? (1: Yes, Any key: No): ")
    if again == "1":
        update(username)
    else:
        print("\n↩️ Returning to main menu...\n")

#------------ 4. REMOVE PRODUCT LISTING ------------#

def remove(username):
    while True:
        print("""
============================
❌ Remove Product Listing ❌
============================
Press 'q' to return to menu.
""")

        if not listing:
            print("\n❗️Database is empty.")
            break

        display(listing)

        while True:
            prod_id = get_input("Enter Product ID to remove: ").upper()
            if prod_id.lower() == "q":
              print("\n↩️ Returning to menu...\n")
              return
            if prod_id in listing:
              break
            else:
                print("\n❗️Product ID not found. Please try again.")

        display_prod(prod_id, listing[prod_id])
        confirm = get_input("Are you sure you want to delete this product? (1: Yes, Any key: No): ")

        if confirm == "1":
            now = (datetime.utcnow() + timedelta(hours=7)).strftime("%d/%m/%Y, %H:%M:%S")
            removed = listing.pop(prod_id)
            removed["Last edited by"] = f"{username} at {now}"
            trash[prod_id] = removed
            print("\n✅ Product successfully removed.")
        else:
            print("\n❎ Product removal cancelled.")

        again = get_input("\nRemove another product? (1: Yes, Any key: No): ")
        if again != "1":
            print("\n↩️ Returning to menu...\n")
            break

#------------ 5. RESTORE DATA ------------#

def restore(username):
    print("""
============================
♻️ Restore Deleted Products ♻️
============================
Press 'q' to return to menu.

""")

    if not trash:
        print("🗑️ Trash bin is empty.")
        return

    trash_table = []
    for prod_id, product in trash.items():
        row = [
            prod_id,
            product.get("Product name", ""),
            product.get("Price", ""),
            product.get("Category", ""),
            product.get("Material", ""),
            product.get("Color", ""),
            product.get("Size", ""),
            product.get("Weight", ""),
            product.get("Last edited by", "")
        ]
        trash_table.append(row)

    headers = ["ID", "Name", "Price", "Category", "Material", "Color", "Size", "Weight", "Last edited by"]
    print(tabulate(trash_table, headers=headers, tablefmt="rounded_outline"))

    while True:
      prod_id = get_input("\nEnter Product ID to restore: ").upper()
      if prod_id == "Q":
        print("\n↩️ Returning to menu...\n")
        return
      if prod_id in trash:
        restore_prod = trash.pop(prod_id)
        now = (datetime.utcnow() + timedelta(hours=7)).strftime("%d/%m/%Y, %H:%M:%S")
        restore_prod["Last edited by"] = f"{username} at {now}"
        listing[prod_id] = restore_prod
        print(f"\n✅ {prod_id} has been restored to the product listing.")
      else:
        print("❗ Product ID not found. Please try again.")

      again = get_input("\nRestore another product? (1: Yes, Any key: No): ")
      if again != "1":
        print("\n↩️ Returning to menu...\n")
        break

menu()
# Product Inventory Dashboard

A dynamic **Product Inventory Dashboard** built using **HTML, CSS, and JavaScript**.
This project allows users to manage products with features like adding, editing, deleting, filtering, sorting, pagination, and analytics.

---
## Project Structure

```
frontend/
 ├── Mini_Project/
 │   ├── index.html
 │   ├── style.css
 │   ├── script.js
 │
 ├── screenshots/
 │   ├── Add_Product.png
 │   ├── Edit_product.png
 │   ├── Html_Structure.png
 │   ├── NoProductFound.png
 │   ├── Responsive.png
 │   ├── Search_Feature.png
 │   ├── delete_confir.png
 │   ├── full_UI.png
 │   ├── load_Spinner.png
 │   ├── sort_Feature.png
```

---

## Technologies Used

* HTML5
* CSS
* JavaScript 
* LocalStorage

---

## Features

## HTML Basic Structure

The project follows a well-structured HTML layout to organize different sections of the dashboard clearly and efficiently.

### Key Sections:

- **Header** – Displays the project title
- **Controls Section** – Includes search, filter, and sorting options
- **Analytics Section** – Shows summary data like total products, total value, and out-of-stock items
- **Product Section** – Displays dynamically rendered product cards
- **Form Section** – Allows users to add or edit products

This structured approach ensures better readability, maintainability, and scalability of the application.


*Figure: Basic HTML layout of the Product Inventory Dashboard*

![main structure](https://github.com/Manasvijain06/Assignments/blob/4c0c33f174c0860d01066ca57be72677c5b5a85c/frontend/Mini_Project/screenshots/Html_Structure.png)

---

### 1. Dynamic Product Rendering

* Products are rendered dynamically using JavaScript.
* No hardcoded HTML cards are used.
* Uses DOM manipulation for better performance.

![Full UI](https://github.com/Manasvijain06/Assignments/blob/4c0c33f174c0860d01066ca57be72677c5b5a85c/frontend/Mini_Project/screenshots/full_UI.png)

---

### 2. Add Product

* Users can add new products using a form.
* Includes validation for name, price, stock, and category.


![Add Product](https://github.com/Manasvijain06/Assignments/blob/4c0c33f174c0860d01066ca57be72677c5b5a85c/frontend/Mini_Project/screenshots/Add_Product.png)

---

### 3. Edit Product

* Edit button pre-fills the form with existing product data.
* Allows updating product details easily.


![Edit Product](https://github.com/Manasvijain06/Assignments/blob/4c0c33f174c0860d01066ca57be72677c5b5a85c/frontend/Mini_Project/screenshots/Edit_product.png)

---

### 4. Delete Product with Confirmation

* Users can delete products.
* A confirmation popup prevents accidental deletion.

![Delete Confirmation](https://github.com/Manasvijain06/Assignments/blob/4c0c33f174c0860d01066ca57be72677c5b5a85c/frontend/Mini_Project/screenshots/delete_confir.png)

---

### 5. Search Feature

* Real-time search by product name.
* Improves user experience for large datasets.

![Search Feature](https://github.com/Manasvijain06/Assignments/blob/4c0c33f174c0860d01066ca57be72677c5b5a85c/frontend/Mini_Project/screenshots/Search_Feature.png)

---

### 6. search by categories

* Filter products by category.
* Inculding all categories with individual too.

![category](https://github.com/Manasvijain06/Assignments/blob/90db3227f8cd2caa69388ecffd4d39b430a80289/frontend/Mini_Project/screenshots/category.png)



---

### 7. Sorting

* Sort products by:

  * Price (Low → High / High → Low)
  * Name (A → Z / Z → A)
    
![Filter](https://github.com/Manasvijain06/Assignments/blob/4c0c33f174c0860d01066ca57be72677c5b5a85c/frontend/Mini_Project/screenshots/sort_Feature.png)

---

### 8. Pagination

* Displays limited products per page.
* Improves UI performance and usability.

---

### 9. Stock Status Indicator

* Shows:

  * ✅ In Stock
  * ❌ Out of Stock

---

### 10. Analytics Dashboard

Displays:

* Total Products
* Total Inventory Value
* Out of Stock Products

---

### 11. Loading Spinner

* Shows loading animation during initialization.
* Disables inputs temporarily.

![Spinner](https://github.com/Manasvijain06/Assignments/blob/4c0c33f174c0860d01066ca57be72677c5b5a85c/frontend/Mini_Project/screenshots/load_Spinner.png)

---

### 12. Empty State Handling

* Displays message when no products are found.

![Not Found](https://github.com/Manasvijain06/Assignments/blob/4c0c33f174c0860d01066ca57be72677c5b5a85c/frontend/Mini_Project/screenshots/NoProductFound.png)

---

###  13. Responsive Design

* Fully responsive UI for mobile and desktop.

![Responsive](https://github.com/Manasvijain06/Assignments/blob/4c0c33f174c0860d01066ca57be72677c5b5a85c/frontend/Mini_Project/screenshots/Responsive.png)

---


## 💡 What I Learned

* Handling CRUD operations in JavaScript
* Implementing search, filter, and sorting logic
* Pagination and state management
* Using LocalStorage for data persistence
* Writing clean and structured code

---

## Conclusion

This project demonstrates a complete frontend application with real-world features like product management, analytics, and user-friendly UI.

---

## 📌 How to Run

1. Download or clone the repository
2. Open `index.html` in browser
3. Start managing products 🚀

---

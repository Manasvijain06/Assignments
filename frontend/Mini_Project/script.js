let products = [];
let filteredProducts = [];

let currentPage = 1;
const itemsPerPage = 4;
let editId = null;

// DEFAULT DATA
const defaultProducts = [
    { id: 1, name: "Laptop", price: 55000, stock: 5, category: "electronics" },
    { id: 2, name: "Shirt", price: 1200, stock: 10, category: "clothing" },
    { id: 3, name: "Book", price: 500, stock: 3, category: "books" },
    { id: 4, name: "Headphones", price: 2000, stock: 0, category: "electronics" },
    { id: 5, name: "Shoes", price: 3000, stock: 7, category: "clothing" },
    { id: 6, name: "Watch", price: 2500, stock: 2, category: "accessories" },
    { id: 7, name: "Bag", price: 1500, stock: 6, category: "accessories" },
    { id: 8, name: "Notebook", price: 100, stock: 20, category: "books" }
];

// LOAD DATA
function loadData() {
    const data = localStorage.getItem("products");
    products = data ? JSON.parse(data) : defaultProducts;
}

// SAVE DATA
function saveData() {
    localStorage.setItem("products", JSON.stringify(products));
}

// RENDER PRODUCTS 
function renderProducts(list) {
    const grid = document.getElementById("productGrid");
    const empty = document.getElementById("emptyMessage");

    grid.innerHTML = "";

    if (list.length === 0) {
        empty.style.display = "block";
        return;
    } else {
        empty.style.display = "none";
    }

    const start = (currentPage - 1) * itemsPerPage;
    const paginated = list.slice(start, start + itemsPerPage);

    paginated.forEach(p => {
        const card = document.createElement("div");
        card.className = "card";

        const name = document.createElement("h3");
        name.textContent = p.name;

        const price = document.createElement("p");
        price.textContent = "Price: ₹" + p.price;

        const category = document.createElement("p");
        category.textContent = "Category: " + p.category;

        const stock = document.createElement("p");
        if (p.stock === 0) {
            stock.textContent = "Out of Stock ❌";
            stock.style.color = "red";
        } else {
            stock.textContent = "In Stock ✅ (" + p.stock + ")";
            stock.style.color = "lightgreen";
        }

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.onclick = () => deleteProduct(p.id);

        const editBtn = document.createElement("button");
        editBtn.textContent = "Edit";
        editBtn.onclick = () => openEdit(p.id);

        card.append(name, price, category, stock, editBtn, deleteBtn);
        grid.appendChild(card);
        editBtn.style.marginRight = "10px";
    });

    setupPagination(list.length);
}
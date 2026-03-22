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

// PAGINATION
function setupPagination(totalItems) {
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    const totalPages = Math.ceil(totalItems / itemsPerPage);

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement("button");
        btn.textContent = i;

        if (i === currentPage) {
            btn.classList.add("active-page");
        }

        btn.onclick = () => changePage(i);
        pagination.appendChild(btn);
    }
}
function changePage(page) {
    currentPage = page;
    renderProducts(filteredProducts);
}

// FILTERS
function applyFilters() {
  currentPage = 1;

  let filtered = [...products];

  const search = document.getElementById("search").value.toLowerCase();
  const category = document.getElementById("categoryFilter").value;
  const stock = document.getElementById("stockFilter").value;
  const sort = document.getElementById("sort").value;

  if (search) {
    filtered = filtered.filter(p =>
      p.name.toLowerCase().includes(search)
    );
  }

  if (category !== "all") {
    filtered = filtered.filter(p => p.category === category);
  }

  if (stock === "low") {
    filtered = filtered.filter(p => p.stock < 5);
  }

  if (sort === "low-high") filtered.sort((a, b) => a.price - b.price);
  if (sort === "high-low") filtered.sort((a, b) => b.price - a.price);
  if (sort === "az") filtered.sort((a, b) => a.name.localeCompare(b.name));
  if (sort === "za") filtered.sort((a, b) => b.name.localeCompare(a.name));

  filteredProducts = filtered;

  renderProducts(filteredProducts);
  updateAnalytics();
}

// DELETE
function deleteProduct(id) {
  const confirmDelete = confirm("Are you sure you want to delete this product?");

  if (!confirmDelete) return;

  products = products.filter(p => p.id !== id);
  saveData();
  applyFilters();
}

//EDIT 
function openEdit(id) {
  const product = products.find(p => p.id === id);

  document.getElementById("name").value = product.name;
  document.getElementById("price").value = product.price;
  document.getElementById("stock").value = product.stock;
  document.getElementById("category").value = product.category;

  editId = id;
  //change button 
  const submitBtn = document.getElementById("submitBtn");
  submitBtn.innerText = "Update Product";
}

// ADD PRODUCT
document.getElementById("productForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const price = +document.getElementById("price").value;
  const stock = +document.getElementById("stock").value;
  const category = document.getElementById("category").value;

  if (!name || price <= 0 || stock < 0 || !category) {
    alert("Invalid Input");
    return;
  }

  if (editId !== null) {
  const index = products.findIndex(p => p.id === editId);

  products[index] = {
    id: editId,
    name,
    price,
    stock,
    category
  };

  editId = null;
  document.getElementById("submitBtn").innerText = "Add Product";
} else {
  const newProduct = {
    id: Date.now(),
    name,
    price,
    stock,
    category
  };
  products.push(newProduct);
}

  saveData();
  applyFilters();
  this.reset();
});

// EVENTS
document.getElementById("search").addEventListener("input", applyFilters);
document.getElementById("categoryFilter").addEventListener("change", applyFilters);
document.getElementById("stockFilter").addEventListener("change", applyFilters);
document.getElementById("sort").addEventListener("change", applyFilters);

// ANALYTICS
function updateAnalytics() {
  document.getElementById("totalProducts").innerText = products.length;

  const totalValue = products.reduce((sum, p) => sum + p.price * p.stock, 0);
  document.getElementById("totalValue").innerText = totalValue;

  const out = products.filter(p => p.stock === 0).length;
  document.getElementById("outOfStock").innerText = out;
}
// CATEGORY
function loadCategories() {
  const categories = [...new Set(products.map(p => p.category))];
  const dropdown = document.getElementById("categoryFilter");

  categories.forEach(cat => {
    const option = document.createElement("option");
    option.value = cat;
    option.textContent = cat;
    dropdown.appendChild(option);
  });
}
// SPINNER INIT
async function init() {
  const spinner = document.getElementById("spinner");

  spinner.style.display = "block";

  document.querySelectorAll("input, select, button").forEach(el => el.disabled = true);

  loadData();

  await new Promise(resolve => setTimeout(resolve, 1500));

  spinner.style.display = "none";

  document.querySelectorAll("input, select, button").forEach(el => el.disabled = false);

  loadCategories();
  filteredProducts = [...products];
  applyFilters();
}

init();
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

const API_URL = "http://127.0.0.1:8000";

const buyButton = document.getElementById("buyButton");
const sellButton = document.getElementById("sellButton");

const formContainer = document.getElementById("formContainer");
const result = document.getElementById("result");


buyButton.addEventListener("click", () => {
    showBuyForm();
});


sellButton.addEventListener("click", () => {
    showSellForm();
});

function senToRM(sen) {
    return `RM ${(sen / 100).toFixed(2)}`;
}

function rmToSen(rm) {
    return Math.round(Number(rm) * 100);
}

async function lookupProduct() {

    const productId = Number(
        document.getElementById("product_id").value
    );

    const productInfo = document.getElementById("productInfo");

    if (!productId || productId <= 0) {
        productInfo.textContent = "Please enter a valid Product ID.";
        return;
    }

    productInfo.textContent = "Loading product information...";

    try {

        const response = await fetch(
            `${API_URL}/products/${productId}`
        );

        const product = await response.json();

        if (!response.ok) {
            throw new Error(product.detail || "Product not found");
        }

        checkedProductId = product.id;

        productInfo.textContent = `
        Product Code: ${product.code}
        Product Name: ${product.name}
        Category ID: ${product.category_id}
        Current Price: RM ${(product.price_sen / 100).toFixed(2)}
        Available Quantity: ${product.quantity}
                `;

    } catch (error) {

        checkedProductId = null;
        productInfo.textContent = error.message;

    }
}

function showBuyForm() {

    formContainer.innerHTML = `
        <h2>Buy Product</h2>

        <form id="buyForm">

            <label>Product</label>

            <select id="product_id" required>
                <option value="">Loading products...</option>
            </select>

            <label>Supplier</label>

            <select id="supplier_id" required>
                <option value="">Loading suppliers...</option>
            </select>

            <input
                type="number"
                id="quantity"
                placeholder="Quantity"
                min="1"
                required
            >

            <label>Price (RM)</label>
            <input
                type="number"
                id="price_sen"
                min="0"
                step="0.01"
                placeholder="0.00"
                required
            >

            <button type="submit" class="submit-button">
                Confirm Buy
            </button>

        </form>
    `;

    document
        .getElementById("buyForm")
        .addEventListener("submit", buyProduct);

    loadProducts();
    loadSuppliers();
}

function showSellForm() {

    formContainer.innerHTML = `
        <h2>Sell Product</h2>

        <form id="sellForm">

            <label>Product</label>

            <select id="product_id" required>
                <option value="">Loading products...</option>
            </select>

            <label>Client</label>

            <select id="client_id" required>
                <option value="">Loading clients...</option>
            </select>

            <input
                type="number"
                id="quantity"
                placeholder="Quantity"
                min="1"
                required
            >

            <label>Price (RM)</label>
            <input
                type="number"
                id="unit_price_sen"
                min="0"
                step="0.01"
                placeholder="0.00"
                required
            >

            <button type="submit" class="submit-button">
                Confirm Sell
            </button>

        </form>
    `;

    document
        .getElementById("sellForm")
        .addEventListener("submit", sellProduct);

    loadProducts();
    loadClients();
}

async function loadClients() {

    const clients = await getData("/clients");

    const select = document.getElementById("client_id");

    select.innerHTML = `
        <option value="">Select Client</option>
    `;

    clients.forEach(client => {

        const option = document.createElement("option");

        option.value = client.id;

        option.textContent =
            `${client.code} - ${client.name}`;

        select.appendChild(option);
    });
}

async function buyProduct(event) {

    event.preventDefault();

    try {

        const data = {

            product_id:
                Number(document.getElementById("product_id").value),

            supplier_id:
                Number(document.getElementById("supplier_id").value),

            quantity:
                Number(document.getElementById("quantity").value),

            price_sen:
                rmToSen(document.getElementById("price_sen").value)
        };

        const result =
            await sendRequest("/inventory/buy", data);

        alert("Product purchased successfully.");

        // Reload product list so stock is updated
        loadProducts();

    } catch (error) {

        console.error(error);

        alert(`Purchase failed: ${error.message}`);
    }
}

async function sellProduct(event) {

    event.preventDefault();

    try {

        const data = {

            product_id:
                Number(document.getElementById("product_id").value),

            client_id:
                Number(document.getElementById("client_id").value),

            quantity:
                Number(document.getElementById("quantity").value),

            unit_price_sen:
                rmToSen(document.getElementById("unit_price_sen").value)
        };

        const result =
            await sendRequest("/inventory/sell", data);

        alert("Product sold successfully.");

        // Reload product list so stock is updated
        loadProducts();

    } catch (error) {

        console.error(error);

        alert(`Sell failed: ${error.message}`);
    }
}

async function getData(endpoint) {

    const response = await fetch(`${API_URL}${endpoint}`);

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Failed to load data");
    }

    return data;
}

async function loadProducts() {

    const products = await getData("/products");

    const select = document.getElementById("product_id");

    select.innerHTML = `
        <option value="">Select Product</option>
    `;

    products.forEach(product => {

        const option = document.createElement("option");

        option.value = product.id;

        option.textContent =
            `${product.code} - ${product.name} (Stock: ${product.quantity}, Price: ${senToRM(product.price_sen)})`;

        select.appendChild(option);
    });
}

async function loadSuppliers() {

    const suppliers = await getData("/suppliers");

    const select = document.getElementById("supplier_id");

    select.innerHTML = `
        <option value="">Select Supplier</option>
    `;

    suppliers.forEach(supplier => {

        const option = document.createElement("option");

        option.value = supplier.id;

        option.textContent =
            `${supplier.code} - ${supplier.name}`;

        select.appendChild(option);
    });
}

async function sendRequest(endpoint, data) {

    result.innerHTML = "Processing...";

    try {

        const response = await fetch(`${API_URL}${endpoint}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const responseData = await response.json();

        if (!response.ok) {
            throw new Error(
                responseData.detail || "Request failed"
            );
        }

        result.innerHTML = `
            <strong>Success</strong>

            <pre>${JSON.stringify(
            responseData,
            null,
            2
        )}</pre>
        `;

    } catch (error) {

        result.innerHTML = `
            <strong>Error</strong>
            <p>${error.message}</p>
        `;
    }
}

// // Add event listeners for each button
let tempdata;
let OptionsData;
let SubData;
document.querySelector(".FeaturePrducts").style.display = "none";
document.getElementById("pricing").addEventListener("click", async function () {
    document.getElementById("buttonContainer").style.display = "block";
    tempdata = await fetchAndData();
    document.querySelector(".FeaturePrducts").style.display = "block";
    await fetchAndDisplayData("Matrix ONE");
   
    OptionsData=await fetchData()

    SubData = await fetchSubData()
    console.log("subdata",SubData)

});

// Function to fetch and display data based on the category name
async function fetchAndData() {
    try {
        let response = await fetch("http://localhost:8000/product_categories/get/");
        let result = await response.json();
       
        // console.log("inner",result.data)
        
        return result.data

    } catch (error) {
        document.getElementById("output").innerText = "An error occurred: " + error;
    }
}

//  ---------------------api fatch ------------------------------
async function fetchData() {
    try {
        let response = await fetch("http://localhost:8000/product_options/get/");
        let result = await response.json();
       
        // console.log("inner",result.data)
        
        return result.data

    } catch (error) {
        document.getElementById("output").innerText = "An error occurred: " + error;
    }
}

// ------------- sub data api fetch------------------------------------------
async function fetchSubData() {
    try {
        let response = await fetch("http://localhost:8000/product_sub_options/get/");
        let result = await response.json();
        
        return result.data

    } catch (error) {
        document.getElementById("output").innerText = "An error occurred: " + error;
    }
}


// ----------------------------------------------------------------------
document.getElementById("One").addEventListener("click", async function () {
    await fetchAndDisplayData("Matrix ONE");
});

// Function to fetch and display data based on the category name
async function fetchAndDisplayData(category) {
    // console.log("Inside function:", tempdata);

    if (!tempdata) {
        console.log("Data not loaded yet. Fetching data first...");
        tempdata = await fetchAndData(); // Fetch data if not already fetched
    }

    try {
        // Filter data based on base_category_name
        let filteredData = tempdata.filter(item => item.base_category_name === category);

        // Remove unwanted fields
        let cleanedData = filteredData.map(({ updated_at, created_at, description, base_category_name, ...rest }) => rest);

        // console.log(`Filtered Data for ${category}:`, cleanedData);

        // Get the divs where you want to insert data
        let divs = document.querySelectorAll(".FeaturePrducts > div");

        // Clear previous content and apply "disabled" class initially
        divs.forEach(div => {
            div.innerHTML = "";
            div.classList.add("disabled"); // Add "disabled" class to all divs initially
        });

        // Loop through cleanedData and insert it into the divs (up to 4 items)
        cleanedData.forEach((item, index) => {
            if (index < divs.length) {
                let div = divs[index];
        
                div.innerHTML = `
                   <button class="feature-button" data-id="${item.id}">
                <div class="category_name">${item.category_name}</div>
                <div class="price">Starting From ₹${item.starting_price}</div>
            </button>
                `;
                div.classList.remove("disabled"); // Remove "disabled" class when data is inserted
                    // Add event listener to the button to call fetchAndDisplay function
                   
                let button = div.querySelector(".feature-button");

                button.addEventListener("click", function () {
                    let id = button.getAttribute("data-id"); // Now this will get the correct data-id
                    fetchAndDisplay(id); // Call the function with the id
        });
    }
});
        // If there is no data for the selected category, leave all divs disabled
        if (cleanedData.length === 0) {
            divs.forEach(div => div.classList.add("disabled"));
        }
    } catch (error) {
        console.error("An error occurred:", error);
    }
}


["One", "EDGE", "ALGO"].forEach(id => {
    document.getElementById(id).addEventListener("click", async function () {
        await fetchAndDisplayData(`Matrix ${id.toUpperCase()}`);
        document.querySelector(".FeaturePrducts").style.display = "block";
      
    });
});




// -------------------------Option data--------------------------


// Function to fetch and display data based on the category name
async function fetchAndDisplay(category_id) {
    console.log("OptionsData",OptionsData)
    category_id = Number(category_id)

    if (!OptionsData) {
        console.log("Data not loaded yet. Fetching data first...");
        OptionsData = await fetchAndData(); // Fetch data if not already fetched
    }

    try {
        // Filter data based on base_category_name
        let filteredData = OptionsData.filter(item => item.category_id === category_id);
        
        // Remove unwanted fields
        let cleanedData = filteredData.map(item => ({
            category_id: item.category_id,
            product_name: item.product_name,
            starting_price: item.starting_price,
            id: item.id
        
        }))

        console.log(`Filtered Data for ${category_id}:`, cleanedData);

        // Get the divs where you want to insert data
        let divs = document.querySelectorAll(".StandardizedPlans > div");

        // Clear previous content and apply "disabled" class initially
        divs.forEach(div => {
            div.innerHTML = "";
            div.classList.add("disabled"); // Add "disabled" class to all divs initially
        });

        // Loop through cleanedData and insert it into the divs (up to 4 items)
        cleanedData.forEach((item, index) => {
            if (index < divs.length) {
                let div = divs[index];
                console.log("item id",item.id)
                div.innerHTML = `
              
                   <button class="feature-sub-button"  data-id="${item.id}">
                    
                <div class="category_name">${item.product_name}</div>
                <div class="price">starts with ₹${item.starting_price}</div>
            </button>
                `;
                div.classList.remove("disabled"); // Remove "disabled" class when data is inserted
        // ------------------------------------------------------------------  
              
            }
        });
        
        // ----------------------------------------------------------------------------
        if (cleanedData.length === 0) {
            divs.forEach(div => div.classList.add("disabled"));
        }

        // Show the StandardizedPlans div once data is inserted
        document.querySelector(".StandardizedPlans").style.display = "block";
        // document.querySelector(".FeaturePrducts").style.display = "none"; // Hide FeaturePrducts div
        // document.querySelector(".FavouriteOne").style.display = "block";
        

        // Add event listener to each button to display data in FavouriteOne div
        document.querySelectorAll(".feature-sub-button").forEach(button => {
            button.addEventListener("click", function () {
                let id = button.getAttribute("data-id");
                fetchSubDataDisplay(id); // Call function to display the data in FavouriteOne div
            });
        });


    } catch (error) {
        console.error("An error occurred:", error);
    }
}





// ______________________sub data______________________________

async function fetchSubDataDisplay(product_id) {
    console.log("SubData",SubData)
    console.log("id",product_id)
    product_id = Number(product_id)

    if (!SubData) {
        console.log("Data not loaded yet. Fetching data first...");
        SubData = await fetchAndData(); // Fetch data if not already fetched
    }

    try {
        // Filter data based on base_category_name
        let filteredData =SubData.filter(item => item.product_option_id=== product_id);
        
        // Remove unwanted fields
        let cleanedData = filteredData.map(item => ({
            category_id: item.category_id,
            sub_product_name: item.sub_product_name,
            starting_price: item. starting_price,
            price: item.price
        
        }))

        console.log(`Filtered Data for ${ product_id}:`, cleanedData);

        // Get the divs where you want to insert data
        let divs = document.querySelectorAll(".FavouriteOne > div");

        // Clear previous content and apply "disabled" class initially
        divs.forEach(div => {
            div.innerHTML = "";
            div.classList.add("disabled"); // Add "disabled" class to all divs initially
        });

        // Loop through cleanedData and insert it into the divs (up to 4 items)
        cleanedData.forEach((item, index) => {
            if (index < divs.length) {
                let div = divs[index];
                div.innerHTML = `
              
                   <button class="feature-sub-button">
                    
                <div class="category_name">${item.sub_product_name}</div>
                <div class="price">₹${item.starting_price}</div>
                 <div class="actualprice"> ₹${item.price}</div>
            </button>
                `;
                div.classList.remove("disabled"); // Remove "disabled" class when data is inserted
            }
        });

        // If there is no data for the selected category, leave all divs disabled
        if (cleanedData.length === 0) {
            divs.forEach(div => div.classList.add("disabled"));
        }
        document.querySelector(".FavouriteOne").style.display = "block";
      
      
 
    } catch (error) {
        console.error("An error occurred:", error);
    }
}






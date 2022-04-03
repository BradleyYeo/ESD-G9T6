<?php
header("Access-Control-Allow-Origin: *");
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BLUEMART</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/items.css">
    <link rel="stylesheet" href="css/cart.css">

    <!-- Latest compiled and minified JavaScript -->
    <script
       src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
       <script 
       src='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js'
       integrity='sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM'
       crossorigin='anonymous'></script>

     <!-- Vue 3 -->
     <script src='https://cdn.jsdelivr.net/npm/vue@3.0.2/dist/vue.global.js'></script>
     <!-- Vue 3: production version, optimized for size and speed -->
     <!-- <script src='https://cdn.jsdelivr.net/npm/vue@3.0.2/dist/vue.global.prod.js'></script> -->

</head>

<body>
    <!-- CART -->
    <div id="cart">
        <!-- MAKE SURE TO MAKE THE REST OF THE PAGE UNSCROLLABLE WHEN CART IS OPEN -->
        
        <div class="top-row">
            <div class="close">close</div>
            <div id="title">CART</div>
        </div>

        <div id="cart-items">
            <div id="added-items"></div>
        </div>

        <div id="price">
            <div id="delivery-fee"></div>
            <div id="subtotal"></div>
        </div>

        <div id="checkout-button"></div>
    </div>
    <div id="app">
    <nav>
        <div class="nav-left">
            <a href="landing_page.html" class="nav-link">HOME</a>
            <a href="items.html" class="nav-link">ITEMS</a>
        </div>
        <div class="nav-brand">
            <a href="landing_page.html"><span style="color: var(--blue); font-style: italic;">BLUE</span>MART</a>
        </div>
        <div class="nav-right">
            <a href="" class="nav-link">LOGIN/SIGN UP</a>
            <div class="cart-button" id="cart-button">
                CART {{cartNum}}
                <div v-if="haveCart">
                    {{firstCartProductName}}
                </div>
            </div>
        </div>
    </nav>

    <div id="hero">
        <div id="all-items">
            <p class="title">All Items<p>
            <div class="items" v-if="noError">
                <div class="item" id="first-item">
                    <div>
                        <img src ="images/1.webp" width="150" height="100"/>
                    </div>
                        <h3> Item: {{firstProductName}} </h3> 
                        <p> Price: {{firstPrice}} cents</p>
                        <p> Product ID: {{firstProductId}}</p>
                        <p id="firstQuantity"> Quantity Available:{{firstQuantity}}</p> 
                        <button v-on:click="addedFirstItem" type="button" class="button" id="button1">Add to Cart!</button>
                </div>
                <div class="item" id="second-item">
                    <div>
                        <img src ="images/2.jpeg" width="150" height="100"/>
                    </div>
                        <h3> Item: {{secondProductName}} </h3> 
                        <p> Price: {{secondPrice}} cents</p>
                        <p> Product ID: {{secondProductId}}</p>
                        <p id="firstQuantity"> Quantity Available:{{secondQuantity}}</p> 
                        <button v-on:click="addedSecondItem" type="button" class="button" id="button2">Add to Cart!</button>
                </div>
                <div class="item" id="third-item">
                    <div>
                        <img src ="images/3.webp" width="150" height="100"/>
                    </div>
                        <h3> Item: {{thirdProductName}} </h3> 
                        <p> Price: {{thirdPrice}} cents</p>
                        <p> Product ID: {{thirdProductId}}</p>
                        <p id="firstQuantity"> Quantity Available:{{thirdQuantity}}</p> 
                        <button v-on:click="addedThirdItem" type="button" class="button" id="button3">Add to Cart!</button>
                </div>
            </div>
            <div v-else>There is something wrong, please try again later</div>
        </div>
    </div> <!--end of vue div container-->

    <div id="footer">

    </div>
    </div>

    <script>
        var get_all_URL = "http://192.168.1.3:5552/inventory";
        var cart_URL = 'http://192.168.1.3:5000/cart'

        const app = Vue.createApp({
            data(){
                return{
                    items : [],
                    cartItems : [],
                    firstItem : '',
                    firstProductName : '',
                    firstPrice : '',
                    firstProductId : '',
                    firstQuantity : '',
                    cartNum : 0,
                    noError : true,
                    haveCart : '',
                    newCustomerId : 1,
                    firstCartProductName : '',
                    secondItem : '',
                    secondPrice : '',
                    secondProductId : '',
                    secondProductName : '',
                    secondQuantity : '',
                    thirdItem : '',
                    thirdPrice : '',
                    thirdProductId : '',
                    thirdProductName : '',
                    thirdQuantity : '',
                }
            },
            methods : {
                addedFirstItem(){
                    this.cartNum ++;
                    let jsonData = JSON.stringify({
                        "cart": [
                            {
                            "price": 400,
                            "product_id": 1,
                            "product_name": "apple",
                            "quantity": 1,
                            "add": false
                            }
                        ]
                    });

                    let cartData = JSON.stringify({
                        "cart": [
                            {
                            "customer_id":1,
                            "product_id": 1,
                            "product_name": "apple",
                            "price": 400,
                            "quantity": 1
                            }
                        ]

                    })
                    //for inventory
                    fetch(`${get_all_URL}/update`,
                        {
                            method: "PUT",
                            headers: {
                                "Content-type": "application/json"
                            },
                            body: jsonData
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            result = data.data;
                            console.log(result);
                            // 3 cases
                            switch (data.code) {
                                case 201:
                                    this.noError = true;
                                    // refresh inventory
                                    this.getAllInventoryItems();

                                    // an alternate way is to add this one element into this.books
                                    break;
                                case 400:
                                case 500:
                                    this.noError = false;
                                    this.noError = data.message;
                                    break;
                                default:
                                    throw `${data.code}: ${data.message}`;
                            }
                        })

                        //for cart
                        fetch(`${cart_URL}/add`,
                        {
                            method: "POST",
                            headers: {
                                "Content-type": "application/json"
                            },
                            body: cartData
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            result = data.data;
                            console.log(result);
                            // 3 cases
                            switch (data.code) {
                                case 201:
                                    this.noError = true;
                                    // refresh inventory
                                    //this.getAllInventoryItems();

                                    // an alternate way is to add this one element into this.books
                                    break;
                                case 400:
                                case 500:
                                    this.noError = false;
                                    this.noError = data.message;
                                    break;
                                default:
                                    throw `${data.code}: ${data.message}`;
                            }
                        })
                },
                addedSecondItem(){
                    this.cartNum ++;
                    let jsonData = JSON.stringify({
                        "cart": [
                            {
                            "price": 300,
                            "product_id": 2,
                            "product_name": "banana",
                            "quantity": 1,
                            "add": false
                            }
                        ]
                    });

                    fetch(`${get_all_URL}/update`,
                        {
                            method: "PUT",
                            headers: {
                                "Content-type": "application/json"
                            },
                            body: jsonData
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            result = data.data;
                            console.log(result);
                            // 3 cases
                            switch (data.code) {
                                case 201:
                                    this.noError = true;
                                    // refresh inventory
                                    this.getAllInventoryItems();

                                    // an alternate way is to add this one element into this.books
                                    break;
                                case 400:
                                case 500:
                                    this.noError = false;
                                    this.noError = data.message;
                                    break;
                                default:
                                    throw `${data.code}: ${data.message}`;
                            }
                        })
                },addedThirdItem(){
                    this.cartNum ++;
                    let jsonData = JSON.stringify({
                        "cart": [
                            {
                            "price": 500,
                            "product_id": 3,
                            "product_name": "pineapple",
                            "quantity": 1,
                            "add": false
                            }
                        ]
                    });

                    fetch(`${get_all_URL}/update`,
                        {
                            method: "PUT",
                            headers: {
                                "Content-type": "application/json"
                            },
                            body: jsonData
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            result = data.data;
                            console.log(result);
                            // 3 cases
                            switch (data.code) {
                                case 201:
                                    this.noError = true;
                                    // refresh inventory
                                    this.getAllInventoryItems();

                                    // an alternate way is to add this one element into this.books
                                    break;
                                case 400:
                                case 500:
                                    this.noError = false;
                                    this.noError = data.message;
                                    break;
                                default:
                                    throw `${data.code}: ${data.message}`;
                            }
                        })
                },
                // getAllCart(){
                //     const response =
                //         fetch(cart_URL)
                //             .then(response => response.json())
                //             .then(data => {
                //                 console.log(response);
                //                 if (data.code === 404) {
                //                     // no book in db
                //                     this.message = data.message;
                //                 } else {
                //                     this.cartItems = data.data.carts;
                //                     // this.firstItem = this.items[0];
                //                     this.firstCartProductName = this.cartItems[0].product_name
                //                     // this.firstProductId = this.firstItem.product_id
                //                     // this.firstPrice = this.firstItem.price
                //                     // this.firstQuantity = this.firstItem.quantity
                //                     //console.log(this.firstProductName);

                //                     this.haveCart = true;
                //                 }
                //             })
                //             .catch(error => {
                //                 // Errors when calling the service; such as network error, 
                //                 // service offline, etc
                //                 console.log(this.message + error);

                //             });
                // },
                getAllInventoryItems(){
                    const response =
                        fetch(`${get_all_URL}/all`)
                            .then(response => response.json())
                            .then(data => {
                                console.log(response);
                                if (data.code === 404) {
                                    // no book in db
                                    this.message = data.message;
                                } else {
                                    this.items = data.data.items;

                                    this.firstItem = this.items[0];
                                    this.firstProductName = this.firstItem.product_name
                                    this.firstProductId = this.firstItem.product_id
                                    this.firstPrice = this.firstItem.price
                                    this.firstQuantity = this.firstItem.quantity
                                    //console.log(this.firstProductName);

                                    this.secondItem = this.items[1];
                                    this.secondPrice = this.secondItem.price
                                    this.secondProductId = this.secondItem.product_id
                                    this.secondProductName = this.secondItem.product_name
                                    this.secondQuantity = this.secondItem.quantity

                                    this.thirdItem = this.items[2];
                                    this.thirdPrice = this.thirdItem.price
                                    this.thirdProductId = this.thirdItem.product_id
                                    this.thirdProductName = this.thirdItem.product_name
                                    this.thirdQuantity = this.thirdItem.quantity
                                }
                            })
                            .catch(error => {
                                // Errors when calling the service; such as network error, 
                                // service offline, etc
                                console.log(this.message + error);

                            });
                }
            },
            created(){
                this.getAllInventoryItems();
            }
        })

        const vm = app.mount('#app');
    </script>

 <script>

        $("#login-sign-up").click(function(){
            $("#modal").show(500);
        });
        $("#modal-close").click(function(){
            $("#modal").hide(500);
        });
        


        $(".cart-button").click(function(){
            $("#cart").show(500);
        });
        $(".close").click(function(){
            $("#cart").hide(500);
        });
</script>

    <!-- // function addedFirstItem(){
    //     //testing if the button is working
    //     var info = 'added'
    //     $('#added-items').append(info)

    // }
    

    // // Helper function to display error message
    // function showError(message) {
    //     // Hide the table and button in the event of error
    //     $('.items').hide();
    //     // $('#addBookBtn').hide();
 
    //     // Display an error under the main container
    //     $('#hero')
    //         .append("<label>"+message+"</label>");
    // }

    // //anonymous async function 
    // //- using await requires the function that calls it to be async
    // $(async() => {           
    //     // Change serviceURL to your own
    //     var serviceURL = "http://192.168.1.2:5552/inventory/all";
 
    //     try {
    //         const response =
    //          await fetch(
    //            serviceURL, { method: 'GET' }
    //         );
    //         const result = await response.json();
    //          if (response.status === 200) {
    //             // success case
    //             var items = result.data.items; //the array is in items within data of 
    //                                            // the returned result
                   
    //             var firstItem = items[0]
    //             var firstPrice = firstItem['price']
    //             var firstProductId = firstItem['product_id']
    //             var firstProductName = firstItem['product_name']
    //             var firstQuantity = firstItem['quantity']
    //             var firstImage = 'images/1.webp'

    //                 var firstInfo = '<div><img src =" '+ firstImage +               '"width="150" height="100" /></div>' +
    //                             '<h3> Item: ' + firstProductName + '</h3>' + 
    //                             '<p> Price: ' + firstPrice + '</p>' + 
    //                             '<p> Product ID: ' + firstProductId + '</p>' + 
    //                             '<p id="firstQuantity"> Quantity Available: ' + firstQuantity + '</p>' + 
    //                             '<button onclick="addedFirstItem()" type="button" class="button" id="button1">Add to Cart!</button></a>'
    //             $('#first-item').append(firstInfo)
                
    //             var secondItem = items[1]
    //             var secondPrice = secondItem['price']
    //             var secondProductId = secondItem['product_id']
    //             var secondProductName = secondItem['product_name']
    //             var secondQuantity = secondItem['quantity']
    //             var secondImage = 'images/2.jpeg'

    //                 var secondInfo = '<div><img src =" '+ secondImage + '" width="150" height="100" /></div>' +
    //                             '<h3> Item: ' + secondProductName + '</h3>' + 
    //                             '<p> Price: ' + secondPrice + '</p>' + 
    //                             '<p> Product ID: ' + secondProductId + '</p>' + 
    //                             '<p> Quantity Available: ' + secondQuantity + '</p>' + 
    //                             '<button type="button" class="button" id="button2">Add to Cart!</button>'
    //             $('#second-item').append(secondInfo)

    //             var thirdItem = items[2]
    //             var thirdPrice = thirdItem['price']
    //             var thirdProductId = thirdItem['product_id']
    //             var thirdProductName = thirdItem['product_name']
    //             var thirdQuantity = thirdItem['quantity']
    //             var thirdImage = 'images/3.webp'

    //     var thirdInfo = '<div><img src =" '+ thirdImage + '" width="150" height="100" /></div>' +
    //                             '<h3> Item: ' + thirdProductName + '</h3>' + 
    //                             '<p> Price: ' + thirdPrice + '</p>' + 
    //                             '<p> Product ID: ' + thirdProductId + '</p>' + 
    //                             '<p> Quantity Available: ' + thirdQuantity + '</p>' + 
    //                             '<button type="button" class="button" id="button3">Add to Cart!</button>'
    //             $('#third-item').append(thirdInfo)


    //             } else if (response.status == 404) {
    //                 // No items
    //                 showError(result.message);
    //             } else {
    //                 // unexpected outcome, throw the error
    //                 throw response.status;
    //             }
    //         } catch (error) {
    //             // Errors when calling the service; such as network error, 
    //             // service offline, etc
    //             showError
    // ('There is a problem retrieving grocery items data, please try again later.<br />' + error);
    //         } // error
    // });

    // $('#button1').click(async (event) => {
    //     event.preventDefault();

    //     let serviceURL = 'http://192.168.1.2:5552/inventory/update';

    //     let firstQuantity = $('#firstQuantity').val();
    //     try {
    //             const response =
    //                 await fetch(
    //                     serviceURL, {
    //                     method: 'POST',
    //                     headers: { "Content-Type": "application/json" },
    //                     body: JSON.stringify({ title: title, price: price, quantity: firstQuantity })
    //                 });
    //             const data = await response.json();

    //             if (response.ok) {
    //                 // relocate to home page
    //                 window.location.replace("items.html");
    //                 return false;
    //             } else {
    //                 console.log(data);
    //                 showError(data.message);
    //             }
    //         } catch (error) {
    //             // Errors when calling the service; such as network error, 
    //             // service offline, etc
    //             showError
    //                 ("There is a problem adding this book, please try again later. " + error);

    //         } // error

    // }) -->


</script>
</body>
</html>

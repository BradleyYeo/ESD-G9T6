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
    <link rel="stylesheet" href="css/landing_page.css">
    <link rel="stylesheet" href="css/cart.css">
    <link rel="stylesheet" href="css/modal.css">
    <link rel="stylesheet" href="css/items.css">

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
    <!-- FOR FACEBOOK LOGIN -->
    <script>
        window.fbAsyncInit = function() {
            FB.init({
                appId            : '936734707042298',
                autoLogAppEvents : true,
                xfbml            : true,
                version          : 'v13.0'
            });
        };
    </script>
    <script async defer crossorigin="anonymous" src="https://connect.facebook.net/en_US/sdk.js"></script>
    
    
    <script>
    
        function statusChangeCallback(response) {  // Called with the results from FB.getLoginStatus().
            console.log('statusChangeCallback');
            console.log(response);                   // The current login status of the person.
            if (response.status === 'connected') {   // Logged into your webpage and Facebook.
                testAPI();
            } else {                                 // Not logged into your webpage or we are unable to tell.
                document.getElementById('status').innerHTML = 'Please log ' +
                    'into this webpage.';
            }
        }
    
    
        function checkLoginState() {               // Called when a person is finished with the Login Button.
            FB.getLoginStatus(function(response) {   // See the onlogin handler
                statusChangeCallback(response);
            });
        }
    
    
        window.fbAsyncInit = function() {
            FB.init({
                appId      : '936734707042298',
                cookie     : true,                     // Enable cookies to allow the server to access the session.
                xfbml      : true,                     // Parse social plugins on this webpage.
                version    : '13.0'           // Use this Graph API version for this call.
            });
    
    
            FB.getLoginStatus(function(response) {   // Called after the JS SDK has been initialized.
                statusChangeCallback(response);        // Returns the login status.
            });
        };
    
        function testAPI() {                      // Testing Graph API after login.  See statusChangeCallback() for when this call is made.
            console.log('Welcome!  Fetching your information.... ');
            FB.api('/me', function(response) {
                console.log('Successful login for: ' + response.name);
                document.getElementById('status').innerHTML =
                    'Thanks for logging in, ' + response.name + '!';
            });
        }
    
    </script>
    <!-- FOR FACEBOOK LOGIN END -->

    <!-- CART -->
    <div id="cart">
        <!-- MAKE SURE TO MAKE THE REST OF THE PAGE UNSCROLLABLE WHEN CART IS OPEN -->
        
        <div class="top-row">
            <img src="img/angle-left-solid.svg" alt="" class="close">
            <div id="title">CART</div>
        </div>

        <div id="cart-items">
            
        </div>


        <div id="price">
            <div id="delivery-fee">
                <div class="text">Delivery Fee</div>
                <div class="price-text">$3.50</div>
            </div>
            <div id="subtotal">
                <div class="subtotal-text">Subtotal</div>
                <!-- <div class="price-text">$3.50</div> -->
            </div>
        </div>

        <a id="checkout-button" onclick="checkout()">
            <img src="img/stripe-brands.svg" alt="">
            Proceed to Checkout
        </a>

        <a id="payment-button" onclick="payment()">
            <img src="img/stripe-brands.svg" alt="">
            Proceed to Payment
        </a>
    </div>

    <!-- LOGIN MODAL -->
    <div id="modal">
        <div id="modal-content">
            <div class="top"><img src="img/xmark-solid.svg" id="modal-close"></div>   
            <div class="title">Pardon the Interruption.</div>
            <p>
                We see that you're not logged in.<br>
                There's so many groceries waiting to be<br>
                added to your cart. Join us now!
            </p>
            <div class="facebook-login">
                <div id="fb-root"></div>

                <script async defer crossorigin="anonymous" src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v13.0&appId=936734707042298&autoLogAppEvents=1" nonce="K1O1L8gJ"></script>

                <div class="fb-login-button" data-width="250" data-size="large" data-button-type="continue_with" data-layout="default" data-auto-logout-link="true" data-use-continue-as="true"></div>

                <div id="status">
                </div>
            </div>
        </div>
    </div>

    <div id="app">
    <nav>
        <div class="nav-left">
            <a href="landing_page.php" class="nav-link">HOME</a>
            <a href="items.html" class="nav-link">ITEMS</a>
        </div>
        <div class="nav-brand">
            <a href="landing_page.php"><span style="color: var(--blue); font-style: italic;">BLUE</span>MART</a>
        </div>
        <div class="nav-right">
        <div class="nav-link" id="login-sign-up">LOGIN/SIGN UP</div>
            <div class="cart-button" id="cart-button">CART ( <span id="cart_num">0</span> )</div>
        </div>
    </nav>

    <div id="hero">
        <div id="all-items">
            <p class="title">All Items<p>
            <div class="items" v-if="noError">
                <!-- v-for to loop through the items  -->
                <!-- <div v-for='(item, index) in items'>
                    <div class="item">
                        <div class="item-img" v-bind:id='productId'>
                            <img v-bind:src='imgArr[index]'>
                        </div>
                            <h3 v-bind:value='item.product_name'> Item: {{item.product_name}} </h3> 
                            <p v-bind:value='item.price'> Price: {{item.price}} cents</p>
                            <p> Product ID: {{item.product_id}}</p>
                            <p id="productId"> Quantity Available:{{item.quantity}}</p> 
                            <button v-on:click="addedFirstItem" type="button" class="button" id="button1">Add to Cart!</button>
                    </div> -->

                    <div class="item" id="first-item">
                        <div class="item-img">
                            <img src ="img/1.webp"/>
                        </div>
                            <h3> Item: {{firstProductName}} </h3> 
                            <p> Price: {{firstPrice}} cents</p>
                            <p> Product ID: {{firstProductId}}</p>
                            <p id="firstQuantity"> Quantity Available:{{firstQuantity}}</p> 
                            <button v-on:click="addedFirstItem" type="button" class="button" id="button1">Add to Cart!</button>
                    </div>
                    <div class="item" id="second-item">
                        <div class="item-img">
                            <img src ="img/2.webp"/>
                        </div>
                            <h3> Item: {{secondProductName}} </h3> 
                            <p> Price: {{secondPrice}} cents</p>
                            <p> Product ID: {{secondProductId}}</p>
                            <p id="firstQuantity"> Quantity Available:{{secondQuantity}}</p> 
                            <button v-on:click="addedSecondItem" type="button" class="button" id="button2">Add to Cart!</button>
                    </div>
                    <div class="item" id="third-item">
                        <div class="item-img">
                            <img src ="img/3.webp"/>
                        </div>
                            <h3> Item: {{thirdProductName}} </h3> 
                            <p> Price: {{thirdPrice}} cents</p>
                            <p> Product ID: {{thirdProductId}}</p>
                            <p id="firstQuantity"> Quantity Available:{{thirdQuantity}}</p> 
                            <button v-on:click="addedThirdItem" type="button" class="button" id="button3">Add to Cart!</button>
                    </div>
                    <div class="item" id="forth-item">
                        <div class="item-img">
                            <img src ="img/4.jpeg"/>
                        </div>
                            <h3> Item: {{forthProductName}} </h3> 
                            <p> Price: {{forthPrice}} cents</p>
                            <p> Product ID: {{forthProductId}}</p>
                            <p id="forthQuantity"> Quantity Available:{{forthQuantity}}</p> 
                            <button v-on:click="addedForthItem" type="button" class="button" id="button4">Add to Cart!</button>
                    </div>
                    <div class="item" id="fifth-item">
                        <div class="item-img">
                            <img src ="img/5.jpeg"/>
                        </div>
                            <h3> Item: {{fifthProductName}} </h3> 
                            <p> Price: {{fifthPrice}} cents</p>
                            <p> Product ID: {{fifthProductId}}</p>
                            <p id="fifthQuantity"> Quantity Available:{{fifthQuantity}}</p> 
                            <button v-on:click="addedFifthItem" type="button" class="button" id="button5">Add to Cart!</button>
                    </div>
                    <div class="item" id="sixth-item">
                        <div class="item-img">
                            <img src ="img/6.webp"/>
                        </div>
                            <h3> Item: {{sixthProductName}} </h3> 
                            <p> Price: {{sixthPrice}} cents</p>
                            <p> Product ID: {{sixthProductId}}</p>
                            <p id="sixthQuantity"> Quantity Available:{{sixthQuantity}}</p> 
                            <button v-on:click="addedSixthItem" type="button" class="button" id="button6">Add to Cart!</button>
                    </div>
                <!-- </div> -->
                <!-- end of v-for  -->
            </div>
            <div v-else>There is something wrong, please try again later</div>
        </div>
    </div> <!--end of vue div container-->

    </div>

    <script>
        var get_all_URL = "http://192.168.1.3:5552/inventory";
        var cart_URL = 'http://192.168.1.3:5000/cart'

        const app = Vue.createApp({
            data(){
                return{
                    //items : [],
                    item : '',
                    items : [],

                    cartItems : [],
                    Item : '',
                    // productName : '',
                    // price : '',
                    // productId : '',
                    // quantity : '',
                    //imgArr : ['img/1.webp',"img/2.webp", "img/3.webp", "img/4.webp", "img/5.webp", "img/6.webp"],
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
                    forthItem : '',
                    forthPrice : '',
                    forthProductId : '',
                    forthProductName : '',
                    forthQuantity : '',
                    fifthItem : '',
                    fifthPrice : '',
                    fifthProductId : '',
                    fifthProductName : '',
                    fifthQuantity : '',
                    sixthItem : '',
                    sixthPrice : '',
                    sixthProductId : '',
                    sixthProductName : '',
                    sixthQuantity : '',
                }
            },
            methods : {
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
                                    // this.items =  [
                                    // {
                                    //     "price": 400, 
                                    //     "product_id": 1, 
                                    //     "product_name": "apple", 
                                    //     "quantity": 0
                                    // }, 
                                    // {
                                    //     "price": 300, 
                                    //     "product_id": 2, 
                                    //     "product_name": "banana", 
                                    //     "quantity": 0
                                    // }, 
                                    // {
                                    //     "price": 500, 
                                    //     "product_id": 3, 
                                    //     "product_name": "pineapple", 
                                    //     "quantity": 2
                                    // },
                                    // {
                                    //     "price": 400, 
                                    //     "product_id": 4, 
                                    //     "product_name": "orange", 
                                    //     "quantity": 0
                                    // }, 
                                    // {
                                    //     "price": 300, 
                                    //     "product_id": 5, 
                                    //     "product_name": "pear", 
                                    //     "quantity": 0
                                    // }, 
                                    // {
                                    //     "price": 500, 
                                    //     "product_id": 6, 
                                    //     "product_name": "grapes", 
                                    //     "quantity": 2
                                    // }
                                    // ];

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

                                    this.forthItem = this.items[3];
                                    this.forthPrice = this.forthItem.price
                                    this.forthProductId = this.forthItem.product_id
                                    this.forthProductName = this.forthItem.product_name
                                    this.forthQuantity = this.forthItem.quantity

                                    this.fifthItem = this.items[4];
                                    this.fifthPrice = this.fifthItem.price
                                    this.fifthProductId = this.fifthItem.product_id
                                    this.fifthProductName = this.fifthItem.product_name
                                    this.fifthQuantity = this.fifthItem.quantity

                                    this.sixthItem = this.items[5];
                                    this.sixthPrice = this.sixthItem.price
                                    this.sixthProductId = this.sixthItem.product_id
                                    this.sixthProductName = this.sixthItem.product_name
                                    this.sixthQuantity = this.sixthItem.quantity
                                }
                            })
                            .catch(error => {
                                // Errors when calling the service; such as network error, 
                                // service offline, etc
                                console.log(this.message + error);

                            });
                },
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
                addedForthItem(){
                    this.cartNum ++;
                    let jsonData = JSON.stringify({
                        "cart": [
                            {
                            "price": 100,
                            "product_id": 4,
                            "product_name": "orange",
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
                addedFifthItem(){
                    this.cartNum ++;
                    let jsonData = JSON.stringify({
                        "cart": [
                            {
                            "price": 110,
                            "product_id": 5,
                            "product_name": "pear",
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
                addedSixthItem(){
                    this.cartNum ++;
                    let jsonData = JSON.stringify({
                        "cart": [
                            {
                            "price": 500,
                            "product_id": 6,
                            "product_name": "grapes",
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
                // checkout(){
                //     let jsonData = JSON.stringify({
                //         "customer_id": 123456,
                //         "customer_email": "abc@abc"
                //     });

                //     //for cart
                //     fetch(`/checkout`,
                //     {
                //         method: "POST",
                //         headers: {
                //             "Content-type": "application/json"
                //         },
                //         body: jsonData
                //     })
                //     .then(response => response.json())
                //     .then(data => {
                //         console.log(data);
                //         result = data.data;
                //         console.log(result);
                //         // 3 cases
                //         switch (data.code) {
                //             case 201:
                //                 this.noError = true;
                //                 // refresh inventory
                //                 //this.getAllInventoryItems();

                //                 // an alternate way is to add this one element into this.books
                //                 break;
                //             case 400:
                //             case 500:
                //                 this.noError = false;
                //                 this.noError = data.message;
                //                 break;
                //             default:
                //                 throw `${data.code}: ${data.message}`;
                //         }
                //     })
                // }
               
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
            $('#login-sign-up').text('Victoria Lee');
        });
        


        $("#cart-button").click(function(){
            $("#cart").show(500);
            $('html, body').css({
                overflow: 'hidden',
                height: '100%'
            });
            
        });
        $(".close").click(function(){
            $("#cart").hide(500);
            $('html, body').css({
                overflow: 'auto',
                height: 'auto'
            });
        });
    </script>

<script>
        // anonymous async function 
        // - using await requires the function that calls it to be async
        $(async() => {           
            // Change serviceURL to your own
            var serviceURL = "http://127.0.0.1:5000/cart/2";

            try {
                const response =
                    await fetch(
                    serviceURL, { method: 'GET' }
                );
                const result = await response.json();
                    if (response.status === 200) {
                        // success case
                        var cart = result.data.cart; //the array is in books within data of 
                                                    // the returned result
                        // for loop to setup all table rows with obtained book data
                        var total_price = 0;
                        var cart_num = cart.length;
                        var rows = "";
                        for (const item of cart) {
                            // eachRow = "<div class='title'>"+ item.product_name + "</div>" +
                            //         "<div class='details'>" + 
                            //             "<div class='quantity'>" + item.quantity + "</div>" + 
                            //             "<div class='price'>" + item.price + "</div>" + 
                            //         "</div>"
                            item_price = (item.price)/100;
                            item_price = item_price * item.quantity;
                            item_price = item_price.toFixed(2);
                            total_price = Number(total_price) + Number(item_price);
                            each_row = `
                                <img class='cart-img' src='img/` + item.product_id + `.webp'>
                                <div class='cart-details'>
                                    <div class='cd-title'>` + item.product_name +`</div>
                                    <div class='cd-others'>
                                        <div class='quantity'>Qty: ` + item.quantity + `</div>
                                        <div class='price'>$` + item_price + `</div>
                                    </div>
                                </div>
                            `;
                            rows += "<div class='cart-item'>" + each_row + "</div>";
                        }
                        // add all the rows to the table
                        $('#cart-items').append(rows);
                        
                        total_price = Number(total_price) + Number(3.50);
                        var subtotal = `<div class="price-text">$`+ total_price.toFixed(2) +`</div>`;
                        $('#subtotal').append(subtotal);

                        $('#cart_num').text(cart_num);

                        $('#cart-items').css({
                            overflow: 'scroll'
                        })
                    } else if (response.status == 400) {
                        // No books
                        console.log(result.message);
                        noItemsMsg = `<div id="no-cart-items">
                            <div class="no-cart-items">Your Cart is Empty</div>
                            <a class="no-cart-items-btn" href="items.html">Shop for More</a>
                            </div>
                            `;
                        $('#cart-items').append(noItemsMsg);
                        $('#price').hide();
                        $('#checkout-button').hide();
                        $('#cart-items').css({
                            height: '40px'
                        })
                    } else {
                        // unexpected outcome, throw the error
                        throw response.status;
                    }
                } catch (error) {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    console.log
        ('There is a problem retrieving cart data, please try again later.<br />' + error);
                } // error
        });

        function checkout() {
            $(async() => {           
            // Change serviceURL to your own
            var serviceURL = "http://127.0.0.1:5550/checkout";
            var customerData = ({
                "customer_id": 1,
                "customer_email": "tianyu.chen.2020@smu.edu.sg"
            });

            try {
                const config = {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(customerData)
                }
                const response = await fetch(serviceURL, config)
                const result = await response.json();
                    if (response.status === 200) {
                        //success
                        $('checkout-button').hide();
                        $('payment-button').show();
                    } else {
                        //not success
                        alert(response.message);
                    } 
                } catch (error) {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    console.log
                        ('There is a problem checking out, please try again later.<br />' + error);
                                } // error
                        });
        }

        function payment() {
            $(async() => {           
            // Change serviceURL to your own
            var serviceURL = "http://127.0.0.1:5069/payment";
            var customerData = ({
                "customer_id": 1,
                "customer_email": "tianyu.chen.2020@smu.edu.sg"
            });

            try {
                const config = {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(customerData)
                }
                const response = await fetch(serviceURL, config)
                const result = await response.json();
                    if (response.status === 200) {
                        //success
                        $('checkout-button').hide();
                        $('payment-button').show();
                    } else {
                        // unexpected outcome, throw the error
                        alert(response.status);
                    }
                } catch (error) {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    console.log
                        ('There is a problem checking out, please try again later.<br />' + error);
                                } // error
                        });
        }
    </script>
    <script async defer crossorigin="anonymous" src="https://connect.facebook.net/en_US/sdk.js"></script>

   


</script>
</body>
</html>

var cart = document.getElementsByClassName("cart")
cart.style.maxWidth = '0px'
function toggleCart(){
    if (cart.style.maxWidth === '0px') {
        cart.style.maxWidth = '45%'
    } else {
        cart.style.maxWidth = '0px'
    }
}
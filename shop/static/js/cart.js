/* ==========================================
   MCART CART
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    initQuantityButtons();

    initRemoveButtons();

    updateCartSummary();

});


/* ==========================================
   QUANTITY
========================================== */

function initQuantityButtons(){

    document.querySelectorAll(".qty-minus").forEach(button=>{

        button.addEventListener("click",()=>{

            const input=button.parentElement.querySelector(".qty-input");

            let value=parseInt(input.value);

            if(value>1){

                input.value=value-1;

                updateCartSummary();

            }

        });

    });

    document.querySelectorAll(".qty-plus").forEach(button=>{

        button.addEventListener("click",()=>{

            const input=button.parentElement.querySelector(".qty-input");

            let value=parseInt(input.value);

            input.value=value+1;

            updateCartSummary();

        });

    });

}


/* ==========================================
   REMOVE ITEM
========================================== */

function initRemoveButtons(){

    document.querySelectorAll(".remove-cart-item").forEach(button=>{

        button.addEventListener("click",(e)=>{

            if(!confirm("Remove this item from cart?")){

                e.preventDefault();

            }

        });

    });

}


/* ==========================================
   UPDATE SUMMARY
========================================== */

function updateCartSummary(){

    let subtotal=0;

    document.querySelectorAll(".cart-item").forEach(item=>{

        const price=parseFloat(item.dataset.price);

        const qty=parseInt(item.querySelector(".qty-input").value);

        const total=price*qty;

        subtotal+=total;

        const itemTotal=item.querySelector(".item-total");

        if(itemTotal){

            itemTotal.textContent=`₹${total.toLocaleString("en-IN")}`;

        }

    });

    const subtotalElement=document.querySelector("#cartSubtotal");

    if(subtotalElement){

        subtotalElement.textContent=`₹${subtotal.toLocaleString("en-IN")}`;

    }

}


/* ==========================================
   AUTO UPDATE
========================================== */

document.querySelectorAll(".qty-input").forEach(input=>{

    input.addEventListener("change",()=>{

        if(input.value<1){

            input.value=1;

        }

        updateCartSummary();

    });

});
/* ==========================================
   MCART SEARCH
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    initSearch();

});


/* ==========================================
   SEARCH
========================================== */

function initSearch(){

    const searchInput = document.querySelector(".search-input");

    if(!searchInput) return;

    searchInput.addEventListener("focus",()=>{

        searchInput.parentElement.classList.add("search-active");

    });

    searchInput.addEventListener("blur",()=>{

        searchInput.parentElement.classList.remove("search-active");

    });

}


/* ==========================================
   CLEAR SEARCH
========================================== */

const clearBtn = document.querySelector(".search-clear");

if(clearBtn){

    clearBtn.addEventListener("click",()=>{

        const input=document.querySelector(".search-input");

        if(!input) return;

        input.value="";

        input.focus();

    });

}


/* ==========================================
   SEARCH SHORTCUT
========================================== */

document.addEventListener("keydown",(e)=>{

    if((e.ctrlKey || e.metaKey) && e.key==="k"){

        e.preventDefault();

        const input=document.querySelector(".search-input");

        if(input){

            input.focus();

        }

    }

});


/* ==========================================
   DEBOUNCE
========================================== */

function debounce(callback,delay=300){

    let timer;

    return (...args)=>{

        clearTimeout(timer);

        timer=setTimeout(()=>{

            callback(...args);

        },delay);

    };

}


/* ==========================================
   LIVE SEARCH PLACEHOLDER
========================================== */

const input=document.querySelector(".search-input");

if(input){

    input.addEventListener("input",

        debounce(function(){

            console.log("Searching :",this.value);

            /*
                Future AJAX Search

                fetch(...)
            */

        })

    );

}
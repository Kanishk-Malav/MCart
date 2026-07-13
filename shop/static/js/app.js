/* ==========================================
   MCART APP
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    initBackToTop();

    initNavbarShadow();

    initTooltips();

    initSmoothScroll();

});


/* ==========================================
   NAVBAR SHADOW
========================================== */

function initNavbarShadow(){

    const navbar = document.querySelector(".navbar");

    if(!navbar) return;

    window.addEventListener("scroll",()=>{

        if(window.scrollY > 30){

            navbar.classList.add("navbar-scrolled");

        }else{

            navbar.classList.remove("navbar-scrolled");

        }

    });

}


/* ==========================================
   BACK TO TOP
========================================== */

function initBackToTop(){

    const button = document.querySelector("#backToTop");

    if(!button) return;

    window.addEventListener("scroll",()=>{

        if(window.scrollY > 400){

            button.classList.add("show");

        }else{

            button.classList.remove("show");

        }

    });

    button.addEventListener("click",()=>{

        window.scrollTo({

            top:0,

            behavior:"smooth"

        });

    });

}


/* ==========================================
   BOOTSTRAP TOOLTIPS
========================================== */

function initTooltips(){

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');

    [...tooltipTriggerList].map(el=>new bootstrap.Tooltip(el));

}


/* ==========================================
   SMOOTH SCROLL
========================================== */

function initSmoothScroll(){

    document.querySelectorAll('a[href^="#"]').forEach(anchor=>{

        anchor.addEventListener("click",function(e){

            const target=document.querySelector(this.getAttribute("href"));

            if(!target) return;

            e.preventDefault();

            target.scrollIntoView({

                behavior:"smooth"

            });

        });

    });

}


/* ==========================================
   LOADER
========================================== */

window.addEventListener("load",()=>{

    const loader=document.querySelector(".page-loader");

    if(loader){

        loader.classList.add("d-none");

    }

});
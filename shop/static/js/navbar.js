/* ==========================================
   MCART NAVBAR
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    initStickyNavbar();

    initActiveNavLink();

    initSearchFocus();

    initMobileMenu();

});


/* ==========================================
   STICKY NAVBAR
========================================== */

function initStickyNavbar(){

    const navbar = document.querySelector(".navbar");

    if(!navbar) return;

    window.addEventListener("scroll",()=>{

        if(window.scrollY > 50){

            navbar.classList.add("navbar-scrolled");

        }else{

            navbar.classList.remove("navbar-scrolled");

        }

    });

}


/* ==========================================
   ACTIVE LINK
========================================== */

function initActiveNavLink(){

    const current = window.location.pathname;

    document.querySelectorAll(".navbar .nav-link").forEach(link=>{

        if(link.getAttribute("href") === current){

            link.classList.add("active");

        }

    });

}


/* ==========================================
   SEARCH FOCUS
========================================== */

function initSearchFocus(){

    const search = document.querySelector(".navbar-search");

    if(!search) return;

    search.addEventListener("focus",()=>{

        search.parentElement.classList.add("focused");

    });

    search.addEventListener("blur",()=>{

        search.parentElement.classList.remove("focused");

    });

}


/* ==========================================
   MOBILE MENU
========================================== */

function initMobileMenu(){

    const toggle = document.querySelector(".navbar-toggler");

    const menu = document.querySelector(".navbar-collapse");

    if(!toggle || !menu) return;

    toggle.addEventListener("click",()=>{

        menu.classList.toggle("show");

    });

}


/* ==========================================
   CLOSE MENU ON LINK CLICK
========================================== */

document.querySelectorAll(".navbar .nav-link").forEach(link=>{

    link.addEventListener("click",()=>{

        const menu = document.querySelector(".navbar-collapse");

        if(menu){

            menu.classList.remove("show");

        }

    });

});
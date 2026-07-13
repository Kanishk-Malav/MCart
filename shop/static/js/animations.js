/* ==========================================
   MCART ANIMATIONS
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    initRevealAnimation();

    initCounterAnimation();

    initHoverAnimation();

});


/* ==========================================
   SCROLL REVEAL
========================================== */

function initRevealAnimation(){

    const elements=document.querySelectorAll(".reveal");

    if(elements.length===0) return;

    const observer=new IntersectionObserver((entries)=>{

        entries.forEach(entry=>{

            if(entry.isIntersecting){

                entry.target.classList.add("active");

            }

        });

    },{

        threshold:0.15

    });

    elements.forEach(element=>{

        observer.observe(element);

    });

}


/* ==========================================
   COUNTER
========================================== */

function initCounterAnimation(){

    const counters=document.querySelectorAll(".counter");

    if(counters.length===0) return;

    counters.forEach(counter=>{

        const target=parseInt(counter.dataset.target);

        let current=0;

        const increment=Math.ceil(target/100);

        const update=()=>{

            current+=increment;

            if(current>=target){

                counter.innerText=target.toLocaleString();

                return;

            }

            counter.innerText=current.toLocaleString();

            requestAnimationFrame(update);

        };

        update();

    });

}


/* ==========================================
   IMAGE HOVER
========================================== */

function initHoverAnimation(){

    document.querySelectorAll(".product-card").forEach(card=>{

        card.addEventListener("mouseenter",()=>{

            card.classList.add("hovering");

        });

        card.addEventListener("mouseleave",()=>{

            card.classList.remove("hovering");

        });

    });

}


/* ==========================================
   PARALLAX
========================================== */

window.addEventListener("scroll",()=>{

    document.querySelectorAll(".parallax").forEach(element=>{

        const speed=element.dataset.speed || 0.3;

        element.style.transform=`translateY(${window.scrollY*speed}px)`;

    });

});


/* ==========================================
   FADE HERO
========================================== */

window.addEventListener("scroll",()=>{

    const hero=document.querySelector(".hero");

    if(!hero) return;

    hero.style.opacity=1-window.scrollY/700;

});


/* ==========================================
   LOADING ANIMATION
========================================== */

window.addEventListener("load",()=>{

    document.body.classList.add("loaded");

});
// SCROLL ANIMATION OBSERVER

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
        }
    });
}, observerOptions);

document.querySelectorAll('.scroll-animate').forEach((el, index) => {
    // Set stagger delay based on element position
    const delay = 0.1;
    el.style.setProperty('--delay', `${delay}s`);
    
    // Handle different element types
    if (el.tagName === 'LI') {
        const liIndex = Array.from(el.parentElement.children).indexOf(el);
        el.style.setProperty('--delay', `${liIndex * 0.15 + 0.2}s`);
    } else if (el.classList.contains('category-card')) {
        const cardIndex = Array.from(el.parentElement.children).indexOf(el);
        el.style.setProperty('--delay', `${cardIndex * 0.15}s`);
    }
    
    observer.observe(el);
});

// SIMPLE SCROLL EFFECT

window.addEventListener("scroll", () => {
    const navbar = document.querySelector(".navbar");
    if (window.scrollY > 50) {
        navbar.style.boxShadow = "0 18px 45px rgba(15,23,42,0.1)";
    } else {
        navbar.style.boxShadow = "0 14px 45px rgba(15,23,42,0.07)";
    }
});

// PRODUCT CARD ANIMATION

const cards = document.querySelectorAll(".card");

cards.forEach((card) => {
    card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.35), #ffffff 40%)`;
    });

    card.addEventListener("mouseleave", () => {
        card.style.background = "#ffffff";
    });
});


// PHILOSOPHY SCROLL ANIMATION

const philosophyBox = document.querySelector(".philosophy-box");

function revealPhilosophy() {

    if (!philosophyBox) return;

    const triggerBottom = window.innerHeight * 0.85;

    const boxTop = philosophyBox.getBoundingClientRect().top;

    if (boxTop < triggerBottom) {
        philosophyBox.classList.add("show");
    }
}

window.addEventListener("load", revealPhilosophy);
window.addEventListener("scroll", revealPhilosophy);

// // TOAST NOTIFICATION

const toastBox = document.getElementById("toastBox");

function showToast(message){

    toastBox.innerHTML = message;

    toastBox.classList.add("show");

    setTimeout(()=>{

        toastBox.classList.remove("show");

    },2500);

}





const counters = document.querySelectorAll('.counter');

const counterObserver = new IntersectionObserver(

(entries)=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            const counter = entry.target;

            const target =
            Number(counter.dataset.target);

            const suffix =
            counter.dataset.suffix || '';

            let current = 0;

            const increment =
            target / 80;

            const updateCounter = ()=>{

                if(current < target){

                    current += increment;

                    counter.innerText =
                    Math.floor(current) + suffix;

                    requestAnimationFrame(updateCounter);

                }else{

                    counter.innerText =
                    target + suffix;
                }
            };

            updateCounter();

            counterObserver.unobserve(counter);
        }

    });

},
{
    threshold:0.5
});

counters.forEach(counter=>{

    counterObserver.observe(counter);

});







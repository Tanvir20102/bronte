/* ============================================================= About Image Slider ============================================================== */
(function () {
    const track = document.querySelector('.about-slides-track');
    const slides = Array.from(document.querySelectorAll('.about-slide'));
    const dots = document.querySelectorAll('.about-dot');
    const prevBtn = document.getElementById('aboutSliderPrev');
    const nextBtn = document.getElementById('aboutSliderNext');
    const sliderEl = document.querySelector('.about-slider');

    if (!track || slides.length === 0) {
        return;
    }

    const total = slides.length;
    const transitionDuration = 600;
    const autoplayDelay = 4000;
    let current = 0;
    let autoplayTimer = null;
    let isAnimating = false;

    function updateTrack() {
        track.style.transition = `transform ${transitionDuration}ms cubic-bezier(0.77, 0, 0.175, 1)`;
        track.style.transform = `translateX(-${current * 100}%)`;

        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === current);
        });
    }

    function goTo(index) {
        if (isAnimating) {
            return;
        }

        current = (index + total) % total;
        isAnimating = true;
        updateTrack();
    }

    function moveBy(delta) {
        goTo(current + delta);
    }

    function startAutoplay() {
        stopAutoplay();
        autoplayTimer = setInterval(() => {
            if (!isAnimating) {
                moveBy(1);
            }
        }, autoplayDelay);
    }

    function stopAutoplay() {
        if (autoplayTimer) {
            clearInterval(autoplayTimer);
            autoplayTimer = null;
        }
    }

    track.addEventListener('transitionend', () => {
        isAnimating = false;
    });

    prevBtn.addEventListener('click', () => {
        stopAutoplay();
        moveBy(-1);
        startAutoplay();
    });

    nextBtn.addEventListener('click', () => {
        stopAutoplay();
        moveBy(1);
        startAutoplay();
    });

    dots.forEach((dot) => {
        dot.addEventListener('click', () => {
            stopAutoplay();
            goTo(parseInt(dot.dataset.index, 10));
            startAutoplay();
        });
    });

    sliderEl.addEventListener('mouseenter', stopAutoplay);
    sliderEl.addEventListener('mouseleave', startAutoplay);

    updateTrack();
    startAutoplay();
})();

// ***************************************************** responsive navbar toggle ****************************************************************
const menuOpen = document.getElementById('menu-icon');
const menuClose = document.getElementById('menu-close-icon');
const responsiveNav = document.querySelector('.responsive-nav-links');
const heroSection = document.querySelector('.hero-container');
let menuIsOpen = false;

gsap.set(responsiveNav, {
    scale: 0,
    opacity: 0,
    pointerEvents: 'none'
});

function updateResponsiveNavMode() {
    if (!heroSection) {
        responsiveNav.classList.remove('dark-bg');
        return;
    }

    const heroBottom = heroSection.offsetTop + heroSection.offsetHeight;
    const menuTop = window.scrollY;

    if (menuIsOpen && menuTop < heroBottom) {
        responsiveNav.classList.add('dark-bg');
    } else {
        responsiveNav.classList.remove('dark-bg');
    }
}

document.addEventListener('click', (e) => {
    if (e.target === menuOpen) {
        menuIsOpen = true;
        updateResponsiveNavMode();
        gsap.to(responsiveNav, {
            duration: 0.5,
            scale: 1,
            opacity: 1,
            pointerEvents: 'auto',
            ease: 'power2.out'
        });
    }
    if (e.target === menuClose) {
        menuIsOpen = false;
        updateResponsiveNavMode();
        gsap.to(responsiveNav, {
            duration: 0.5,
            scale: 0,
            opacity: 0,
            pointerEvents: 'none',
            ease: 'power2.out'
        });
    }
});

window.addEventListener('scroll', () => {
    if (menuIsOpen) {
        updateResponsiveNavMode();
    }
});

// ******************************* Send email ********************************
function sendMail () {
    let params = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        city: document.getElementById("city").value,
        message: document.getElementById("message").value,
    }

    emailjs.send("service_qg7tyvs", "template_2y57cbn", params).then(alert("Email Sent!"))
}
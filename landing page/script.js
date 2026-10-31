"use strict";

/* =================================
   CONFIGURATION
================================= */

// Replace this with your actual deployed Streamlit analyzer URL.
// Example: https://your-project-name.streamlit.app

const ANALYZER_URL = "https://youtube-video-analyzer-ashish-kumar.streamlit.app/";


/* =================================
   DOM ELEMENTS
================================= */

const navbar = document.getElementById("navbar");
const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

const analyzerButton = document.getElementById("analyzerButton");
const toast = document.getElementById("toast");

const currentYear = document.getElementById("currentYear");

let toastTimeout;


/* =================================
   MOBILE NAVIGATION
================================= */

function closeMenu() {
    navLinks.classList.remove("open");
    menuToggle.classList.remove("open");

    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Open navigation menu");
}

menuToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("open");

    menuToggle.classList.toggle("open", isOpen);

    menuToggle.setAttribute("aria-expanded", String(isOpen));

    menuToggle.setAttribute(
        "aria-label",
        isOpen ? "Close navigation menu" : "Open navigation menu"
    );
});


// Close the menu after clicking a navigation link.

document.querySelectorAll(".nav-link, .nav-cta").forEach((link) => {
    link.addEventListener("click", closeMenu);
});


// Close the mobile menu when clicking outside it.

document.addEventListener("click", (event) => {
    if (
        !navLinks.contains(event.target) &&
        !menuToggle.contains(event.target)
    ) {
        closeMenu();
    }
});


// Close the menu when switching back to desktop size.

window.addEventListener("resize", () => {
    if (window.innerWidth > 760) {
        closeMenu();
    }
});


/* =================================
   NAVBAR SCROLL EFFECT
================================= */

function updateNavbar() {
    navbar.classList.toggle("scrolled", window.scrollY > 20);
}

window.addEventListener("scroll", updateNavbar, {
    passive: true
});

updateNavbar();


/* =================================
   SCROLL REVEAL ANIMATIONS
================================= */

const revealElements = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {

    const revealObserver = new IntersectionObserver(
        (entries, observer) => {

            entries.forEach((entry) => {

                if (entry.isIntersecting) {

                    entry.target.classList.add("visible");

                    observer.unobserve(entry.target);
                }

            });

        },
        {
            threshold: 0.12,
            rootMargin: "0px 0px -30px 0px"
        }
    );

    revealElements.forEach((element) => {
        revealObserver.observe(element);
    });

} else {

    // Fallback for browsers without IntersectionObserver.

    revealElements.forEach((element) => {
        element.classList.add("visible");
    });

}


/* =================================
   ACTIVE NAVIGATION ON SCROLL
================================= */

const observedSections = document.querySelectorAll(
    "#home, #features, #how-it-works, #about"
);

if ("IntersectionObserver" in window) {

    const sectionObserver = new IntersectionObserver(
        (entries) => {

            entries.forEach((entry) => {

                if (entry.isIntersecting) {

                    const sectionId = entry.target.id;

                    document.querySelectorAll(".nav-link").forEach((link) => {

                        const isActive =
                            link.getAttribute("href") === `#${sectionId}`;

                        link.classList.toggle("active", isActive);

                    });

                }

            });

        },
        {
            rootMargin: "-25% 0px -60% 0px"
        }
    );

    observedSections.forEach((section) => {
        sectionObserver.observe(section);
    });

}


/* =================================
   TOAST MESSAGE
================================= */

function showToast(message) {

    toast.textContent = message;

    toast.classList.add("show");

    clearTimeout(toastTimeout);

    toastTimeout = setTimeout(() => {
        toast.classList.remove("show");
    }, 3500);

}


/* =================================
   OPEN THE ACTUAL ANALYZER
================================= */

function openAnalyzer(event) {

    event.preventDefault();

    const configuredUrl = ANALYZER_URL.trim();

    // Do not pretend that the analyzer is connected
    // if its real deployment URL has not been configured.

    if (
        !configuredUrl ||
        configuredUrl === "YOUR_STREAMLIT_ANALYZER_URL"
    ) {

        showToast(
            "Add your deployed Streamlit analyzer URL in script.js first."
        );

        return;
    }

    let parsedUrl;

    try {

        parsedUrl = new URL(configuredUrl);

    } catch (error) {

        showToast("The analyzer URL is invalid. Please check script.js.");

        return;
    }

    // Only allow secure HTTPS links.

    if (parsedUrl.protocol !== "https:") {

        showToast("Please configure your deployed analyzer with an HTTPS URL.");

        return;
    }

    // Open the real analyzer in a new tab.

    window.open(parsedUrl.href, "_blank", "noopener,noreferrer");

}


// Main CTA button.

analyzerButton.addEventListener("click", openAnalyzer);


// Header CTA button.

document.querySelector(".nav-cta").addEventListener("click", (event) => {

    // The header CTA scrolls to the analyzer section.
    // The main CTA opens the actual deployed application.

    closeMenu();

});


// Hero CTA scrolls to the analyzer section.

document.querySelectorAll('a[href="#analyzer"]').forEach((link) => {

    link.addEventListener("click", () => {
        closeMenu();
    });

});


/* =================================
   DYNAMIC COPYRIGHT YEAR
================================= */

currentYear.textContent = new Date().getFullYear();
document.addEventListener('DOMContentLoaded', () => {

    // Smooth Scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Intersection Observer for Fade-up Animation
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card, .contact-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });

    // Navbar Scroll Effect (Optimized with IntersectionObserver - Zero Reflow)
    const navbar = document.querySelector('.navbar');
    const sentinel = document.getElementById('navbar-sentinel');

    if (sentinel) {
        const navObserver = new IntersectionObserver((entries) => {
            if (!entries[0].isIntersecting) {
                // Scrolled down past sentinel
                navbar.style.boxShadow = '0 4px 10px rgba(0,0,0,0.1)';
                navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            } else {
                // Back at top
                navbar.style.boxShadow = 'none';
                navbar.style.background = 'rgba(255, 255, 255, 0.8)';
            }
        }, { threshold: 0 });

        navObserver.observe(sentinel);
    }

    // Showcase Tabs
    window.showTab = function (tabId) {
        // Hide all contents
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        // Remove active class from all buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // Show selected content
        document.getElementById(tabId).classList.add('active');

        // Add active class to clicked button (this is a bit tricky with inline onclick, easier to just find by text or use event delegation, but for now specific targeting)
        // A better way is to pass 'this'
        const buttons = document.querySelectorAll('.tab-btn');
        const indexMap = {
            'students': 0, 'finance': 1, 'teachers': 2, 'courses': 3, 'settings': 4
        };
        if (buttons[indexMap[tabId]]) {
            buttons[indexMap[tabId]].classList.add('active');
        }
    };

    // FAQ Accordion
    window.toggleFaq = function (element) {
        const item = element.parentElement;
        const isActive = item.classList.contains('active');

        // Close all
        document.querySelectorAll('.faq-item').forEach(faq => {
            faq.classList.remove('active');
        });

        // Open clicked if it wasn't active
        if (!isActive) {
            item.classList.add('active');
        }
    };
});

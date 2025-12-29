document.addEventListener('DOMContentLoaded', () => {
    const carousel = document.getElementById('setores-carousel');
    const prev = document.getElementById('setores-prev');
    const next = document.getElementById('setores-next');

    if (!carousel || !prev || !next) return;

    function getStep() {
        const firstCard = carousel.querySelector('.setor-card');
        if (!firstCard) return 300;
        const styles = window.getComputedStyle(carousel);
        const gap = parseInt(styles.columnGap || styles.gap || '16', 10);
        return firstCard.getBoundingClientRect().width + gap;
    }

    prev.addEventListener('click', () => {
        carousel.scrollBy({ left: -getStep(), behavior: 'smooth' });
    });

    next.addEventListener('click', () => {
        carousel.scrollBy({ left: getStep(), behavior: 'smooth' });
    });
});

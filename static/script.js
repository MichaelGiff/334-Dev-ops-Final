document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".recipe-card");
    cards.forEach((card, index) => {
        card.animate(
            [
                { opacity: 0, transform: "translateY(12px)" },
                { opacity: 1, transform: "translateY(0)" },
            ],
            {
                duration: 320,
                delay: index * 80,
                fill: "both",
                easing: "ease-out",
            }
        );
    });
});

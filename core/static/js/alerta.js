// Espera a página carregar
document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('mensagens-container');
    if (!container) {
        return; // nenhuma mensagem pra esconder
    }

    // Aplica uma leve transição visual
    container.style.transition = "opacity 0.5s ease";

    // Espera 1 segundo e começa a sumir
    setTimeout(function () {
        container.style.opacity = "0";

        // Depois de 0.5s (tempo da transição), remove do DOM
        setTimeout(function () {
            if (container && container.parentNode) {
                container.parentNode.removeChild(container);
            }
        }, 500);
    }, 1000); // 1000 ms = 1 segundo
});
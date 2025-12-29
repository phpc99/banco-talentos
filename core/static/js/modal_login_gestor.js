function abrirLoginModal() {
    const modal = document.getElementById('login-modal');
    if (modal) {
        modal.hidden = false;
        document.body.style.overflow = 'hidden';
    }
}

function fecharLoginModal() {
    const modal = document.getElementById('login-modal');
    if (modal) {
        modal.hidden = true;
        document.body.style.overflow = '';
    }
}

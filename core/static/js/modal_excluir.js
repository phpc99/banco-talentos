function abrirModalExcluir(id, nome) {
    const modal = document.getElementById('modal-excluir');
    const texto = document.getElementById('modal-texto');
    const form = document.getElementById('form-excluir');

    texto.innerHTML = `
        Tem certeza de que deseja excluir a candidatura de
        <strong>${nome}</strong> (ID ${id})?
        <br><br>
        <span style="color:#b91c1c;font-weight:600">
            Esta ação é irreversível.
        </span>
    `;

    form.action = `/gestor/excluir/${id}/`;  // URL Django de exclusão
    modal.classList.remove('hidden');
}

function fecharModalExcluir() {
    document.getElementById('modal-excluir').classList.add('hidden');
}

// fechar clicando fora
document.addEventListener("click", (e) => {
  const modal = document.getElementById("modal-excluir");
  if (!modal || modal.classList.contains("hidden")) return;

  if (e.target === modal) {
    fecharModalExcluir();
  }
});
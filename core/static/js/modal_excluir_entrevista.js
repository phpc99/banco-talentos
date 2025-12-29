function abrirModalExcluirEntrevista(candidatoId, nome) {
  const modal = document.getElementById("modal-excluir-entrevista");
  const texto = document.getElementById("modal-texto-entrevista");
  const form = document.getElementById("form-excluir-entrevista");

  if (!modal || !texto || !form) return;

  texto.innerHTML = `
    Tem certeza que deseja excluir a entrevista 
    de <strong>${nome}</strong> (ID ${candidatoId})?
    <br><br>
    <span style="color:#b91c1c;font-weight:600">
      Esta ação é irreversível.
    </span>
  `;

  // define action da rota de exclusão
  form.action = `/gestor/entrevistas/excluir/${candidatoId}/`;

  modal.classList.remove("hidden");
}

function fecharModalExcluirEntrevista() {
  const modal = document.getElementById("modal-excluir-entrevista");
  if (!modal) return;

  modal.classList.add("hidden");
}

// fechar clicando fora
document.addEventListener("click", (e) => {
  const modal = document.getElementById("modal-excluir-entrevista");
  if (!modal || modal.classList.contains("hidden")) return;

  if (e.target === modal) {
    fecharModalExcluirEntrevista();
  }
});

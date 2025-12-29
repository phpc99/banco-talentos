// cada item tem formato { nome: "cidade", uf: "sigla estado" }

document.addEventListener('DOMContentLoaded', function () {
    const selectEstado = document.getElementById('id_estado');
    const selectCidade = document.getElementById('id_cidade');

    if (!selectEstado || !selectCidade || typeof cidades === 'undefined') {
        return;
    }

    function carregarEstados() {
        // pega apenas as siglas únicas dos estados
        const ufs = [...new Set(cidades.map(c => c.uf))].sort();

        // limpa e coloca a opção padrão
        selectEstado.innerHTML = '<option value="">Selecione um estado</option>';

        ufs.forEach(uf => {
            const option = document.createElement('option');
            option.value = uf;          // valor que será enviado pro backend
            option.textContent = uf;    // texto exibido
            selectEstado.appendChild(option);
        });
    }

    function carregarCidades(uf) {
        // limpa e coloca opção padrão
        selectCidade.innerHTML = '<option value="">Selecione uma cidade</option>';

        // filtra cidades pelo estado escolhido
        const cidadesFiltradas = cidades.filter(c => c.uf === uf);

        cidadesFiltradas.forEach(cidade => {
            const option = document.createElement('option');
            option.value = cidade.nome;         // valor enviado pro backend
            option.textContent = cidade.nome;   // texto exibido
            selectCidade.appendChild(option);
        });
    }

    // quando o usuário muda o estado
    selectEstado.addEventListener('change', function () {
        const ufSelecionada = this.value;

        if (ufSelecionada) {
            carregarCidades(ufSelecionada);
            selectCidade.disabled = false;
        } else {
            selectCidade.innerHTML = '<option value="">Selecione um estado primeiro</option>';
            selectCidade.disabled = true;
        }
    });

    // inicialização
    carregarEstados();
    selectCidade.disabled = true;
});

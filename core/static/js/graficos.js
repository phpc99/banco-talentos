document.addEventListener('DOMContentLoaded', function () {
  const areaEl = document.getElementById('chart-area-data');
  const formacaoEl = document.getElementById('chart-formacao-data');
  const estadoEl = document.getElementById('chart-estado-data');

  if (!areaEl || !formacaoEl || !estadoEl) return;

  const chartArea = JSON.parse(areaEl.textContent);
  const chartFormacao = JSON.parse(formacaoEl.textContent);
  const chartEstado = JSON.parse(estadoEl.textContent);

  // Gerar cores dinamicamente (HSL)
  function gerarCores(qtd) {
    const cores = [];
    for (let i = 0; i < qtd; i++) {
      const hue = Math.round((360 / Math.max(qtd, 1)) * i);
      cores.push(`hsl(${hue}, 65%, 55%)`);
    }
    return cores;
  }

  function prepararCanvasPizza(canvas) {
    // deixa o canvas quadrado baseado no menor lado do container
    const wrap = canvas.closest('.chart-body') || canvas.parentElement;
    if (!wrap) return;

    const rect = wrap.getBoundingClientRect();
    const size = Math.floor(Math.min(rect.width, rect.height));
    if (size > 0) {
      canvas.style.width = `${size}px`;
      canvas.style.height = `${size}px`;
      canvas.width = size;
      canvas.height = size;
    }
  }

  function criarGrafico(idCanvas, dados, tipo, label) {
    const canvas = document.getElementById(idCanvas);
    if (!canvas) return null;

    // se for pizza, ajusta o canvas para quadrado antes de criar
    if (tipo === 'pie') prepararCanvasPizza(canvas);

    const ctx = canvas.getContext('2d');

    const config = {
      type: tipo,
      data: {
        labels: dados.labels,
        datasets: [
          {
            label: label,
            data: dados.values
          }
        ]
      },
      options: {}
    };

    if (tipo === 'bar') {

        const baseColor = 'rgba(0, 76, 108, 0.75)';
        const hoverColor = 'rgba(0, 76, 108, 1)';

        config.data.datasets[0].backgroundColor = baseColor;
        config.data.datasets[0].hoverBackgroundColor = hoverColor;
        config.data.datasets[0].hoverBorderWidth = 2;
        config.data.datasets[0].hoverBorderColor = '#00384f';

        config.options = {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
            y: {
                beginAtZero: true,
                ticks: {
                stepSize: 1,
                precision: 0
                }
            }
            },
            plugins: {
            legend: { display: false }
            },
            hover: {
                mode: 'nearest',
                intersect: true
            }
        };
    } else {
      const cores = gerarCores(dados.labels.length);

      config.data.datasets[0].backgroundColor = cores;
      config.data.datasets[0].borderColor = '#ffffff';
      config.data.datasets[0].borderWidth = 1;

      config.options = {
        responsive: true,
        maintainAspectRatio: true, // deixa o canvas mandar no tamanho
        plugins: {
          legend: {
            position: 'right',
            align: 'center'
          }
        },
        hover: {
          mode: 'nearest',
          intersect: true
        }
      };
    }

    return new Chart(ctx, config);
  }

  let chartAreaObj = criarGrafico(
    'graficoArea',
    chartArea,
    'bar',
    'Quantidade de candidatos por área'
  );

  let chartFormacaoObj = criarGrafico(
    'graficoFormacao',
    chartFormacao,
    'bar',
    'Quantidade de candidatos por formação'
  );

  let chartEstadoObj = criarGrafico(
    'graficoEstado',
    chartEstado,
    'bar',
    'Distribuição de candidatos por estado'
  );

  window.mudarTipo = function (grafico, tipo) {
    if (grafico === 'area' && chartAreaObj) {
      chartAreaObj.destroy();
      chartAreaObj = criarGrafico(
        'graficoArea',
        chartArea,
        tipo,
        'Quantidade de candidatos por área'
      );
    }

    if (grafico === 'formacao' && chartFormacaoObj) {
      chartFormacaoObj.destroy();
      chartFormacaoObj = criarGrafico(
        'graficoFormacao',
        chartFormacao,
        tipo,
        'Quantidade de candidatos por formação'
      );
    }

    if (grafico === 'estado' && chartEstadoObj) {
      chartEstadoObj.destroy();
      chartEstadoObj = criarGrafico(
        'graficoEstado',
        chartEstado,
        tipo,
        'Distribuição de candidatos por estado'
      );
    }
  };

  // alterar para responsividade no mobile
  window.addEventListener('resize', () => {
  });
});

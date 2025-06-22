function atualizarImagemForca(tentativasErradas) {
    // Array com as imagens em SVG da forca (em estágios)
    const forcaImagens = [
        `<svg width="110" height="174" viewBox="0 0 110 174" fill="none" xmlns="http://www.w3.org/2000/svg">
        <line x1="28.5" y1="172.991" x2="29.5" y2="2.99117" stroke="black" stroke-width="3" />
        <line y1="171.5" x2="110" y2="171.5" stroke="black" stroke-width="5" />
        <line x1="28" y1="1.5" x2="65" y2="1.5" stroke="black" stroke-width="3" />
        <line x1="63.5" y1="3" x2="63.5" y2="14" stroke="black" stroke-width="3" />
      </svg>`,
        `<svg width="110" height="174" viewBox="0 0 110 174" fill="none" xmlns="http://www.w3.org/2000/svg">
        <line x1="28.5" y1="172.991" x2="29.5" y2="2.99117" stroke="black" stroke-width="3" />
        <line y1="171.5" x2="110" y2="171.5" stroke="black" stroke-width="5" />
        <line x1="28" y1="1.5" x2="65" y2="1.5" stroke="black" stroke-width="3" />
        <line x1="63.5" y1="3" x2="63.5" y2="14" stroke="black" stroke-width="3" />
        <ellipse cx="62.5" cy="28" rx="13.5" ry="14" fill="#D9D9D9" />
      </svg>`,
        `<svg width="110" height="174" viewBox="0 0 110 174" fill="none" xmlns="http://www.w3.org/2000/svg">
        <line x1="28.5" y1="172.991" x2="29.5" y2="2.99117" stroke="black" stroke-width="3" />
        <line y1="171.5" x2="110" y2="171.5" stroke="black" stroke-width="5" />
        <line x1="28" y1="1.5" x2="65" y2="1.5" stroke="black" stroke-width="3" />
        <line x1="63.5" y1="3" x2="63.5" y2="14" stroke="black" stroke-width="3" />
        <ellipse cx="62.5" cy="28" rx="13.5" ry="14" fill="#D9D9D9" />
        <line x1="63" y1="42" x2="63" y2="116" stroke="#D9D9D9" stroke-width="2" />
      </svg>`,
        `<svg width="110" height="174" viewBox="0 0 110 174" fill="none" xmlns="http://www.w3.org/2000/svg">
        <line x1="28.5" y1="172.991" x2="29.5" y2="2.99117" stroke="black" stroke-width="3" />
        <line y1="171.5" x2="110" y2="171.5" stroke="black" stroke-width="5" />
        <line x1="28" y1="1.50001" x2="65" y2="1.50001" stroke="black" stroke-width="3" />
        <line x1="63.5" y1="3.00001" x2="63.5" y2="14" stroke="black" stroke-width="3" />
        <ellipse cx="62.5" cy="28" rx="13.5" ry="14" fill="#D9D9D9" />
        <line x1="63" y1="42" x2="63" y2="116" stroke="#D9D9D9" stroke-width="2" />
        <line x1="62.5547" y1="57.1679" x2="89.5547" y2="75.168" stroke="#D9D9D9" stroke-width="2" />
      </svg>`,
        `<svg width="110" height="174" viewBox="0 0 110 174" fill="none" xmlns="http://www.w3.org/2000/svg">
        <line x1="28.5" y1="172.991" x2="29.5" y2="2.99117" stroke="black" stroke-width="3" />
        <line y1="171.5" x2="110" y2="171.5" stroke="black" stroke-width="5" />
        <line x1="28" y1="1.50001" x2="65" y2="1.50001" stroke="black" stroke-width="3" />
        <line x1="63.5" y1="3.00001" x2="63.5" y2="14" stroke="black" stroke-width="3" />
        <ellipse cx="62.5" cy="28" rx="13.5" ry="14" fill="#D9D9D9" />
        <line x1="63" y1="42" x2="63" y2="116" stroke="#D9D9D9" stroke-width="2" />
        <line x1="62.5547" y1="57.1679" x2="89.5547" y2="75.168" stroke="#D9D9D9" stroke-width="2" />
        <line x1="38.4157" y1="75.1885" x2="63.4157" y2="57.1885" stroke="#D9D9D9" stroke-width="2" />
      </svg>`,
        `<svg width="110" height="174" viewBox="0 0 110 174" fill="none" xmlns="http://www.w3.org/2000/svg">
        <line x1="62.5087" y1="115.139" x2="84.5087" y2="128.139" stroke="#D9D9D9" stroke-width="2" />
        <line x1="28.5" y1="172.991" x2="29.5" y2="2.99117" stroke="black" stroke-width="3" />
        <line y1="171.5" x2="110" y2="171.5" stroke="black" stroke-width="5" />
        <line x1="28" y1="1.50001" x2="65" y2="1.50001" stroke="black" stroke-width="3" />
        <line x1="63.5" y1="3.00001" x2="63.5" y2="14" stroke="black" stroke-width="3" />
        <ellipse cx="62.5" cy="28" rx="13.5" ry="14" fill="#D9D9D9" />
        <line x1="63" y1="42" x2="63" y2="116" stroke="#D9D9D9" stroke-width="2" />
        <line x1="62.5547" y1="57.1679" x2="89.5547" y2="75.168" stroke="#D9D9D9" stroke-width="2" />
        <line x1="38.4157" y1="75.1885" x2="63.4157" y2="57.1885" stroke="#D9D9D9" stroke-width="2" />
      </svg>`,
        `<svg width="110" height="174" viewBox="0 0 110 174" fill="none" xmlns="http://www.w3.org/2000/svg">
        <line x1="47.3706" y1="128.223" x2="63.4225" y2="115.223" stroke="#D9D9D9" stroke-width="2" />
        <line x1="62.5087" y1="115.139" x2="84.5087" y2="128.139" stroke="#D9D9D9" stroke-width="2" />
        <line x1="28.5" y1="172.991" x2="29.5" y2="2.99117" stroke="black" stroke-width="3" />
        <line y1="171.5" x2="110" y2="171.5" stroke="black" stroke-width="5" />
        <line x1="28" y1="1.50001" x2="65" y2="1.50001" stroke="black" stroke-width="3" />
        <line x1="63.5" y1="3.00001" x2="63.5" y2="14" stroke="black" stroke-width="3" />
        <ellipse cx="62.5" cy="28" rx="13.5" ry="14" fill="#D9D9D9" />
        <line x1="63" y1="42" x2="63" y2="116" stroke="#D9D9D9" stroke-width="2" />
        <line x1="62.5547" y1="57.1679" x2="89.5547" y2="75.168" stroke="#D9D9D9" stroke-width="2" />
        <line x1="38.4157" y1="75.1885" x2="63.4157" y2="57.1885" stroke="#D9D9D9" stroke-width="2" />
      </svg>`
    ];

    // Seleciona a imagem correspondente à quantidade de erros
    const imagem = forcaImagens[Math.min(tentativasErradas, forcaImagens.length - 1)];

    // Exibe a imagem atual da forca
    document.getElementById("forca_imagem").innerHTML = imagem;
}

function resetarTela() {
    document.getElementById("letras_certas").textContent = "____";
    document.getElementById("letras_erradas").textContent = "";
    document.getElementById("tentativas").textContent = "Tentativas: 6";
    document.getElementById("letra").value = "";
    document.getElementById("jogo").style.display = "none";
    document.getElementById("forca_imagem").innerHTML = "";
}

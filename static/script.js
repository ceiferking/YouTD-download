// script.js

function toggleOptions() {
    /*
    Função para alternar a exibição das opções disponíveis quando o botão
    dropbtn é clicado. Adiciona ou remove a classe 'show' do elemento
    dropdown-content para mostrar ou ocultar as opções.
    */
    var dropdownContent = document.getElementById("dropdown-content");
    dropdownContent.classList.toggle("show");

    // Mostra ou oculta a lista de opções dentro do dropdown-content
    var optionsList = document.getElementById("options-list");
    if (optionsList.style.display === "none") {
        optionsList.style.display = "block";
    } else {
        optionsList.style.display = "none";
    }
}

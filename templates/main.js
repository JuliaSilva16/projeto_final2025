const botaoMais = document.getElementById("botao_mais");
const painelCadastro = document.getElementById("painel-cadastro");

botaoMais.addEventListener("click", (e) => {
  e.stopPropagation(); // impede que o clique feche o painel
  painelCadastro.style.display = painelCadastro.style.display === "flex" ? "none" : "flex";
});

document.addEventListener("click", () => {
  painelCadastro.style.display = "none";
});


// Fecha o painel se clicar fora
document.addEventListener("click", () => {
  painelCadastro.style.display = "none";
});





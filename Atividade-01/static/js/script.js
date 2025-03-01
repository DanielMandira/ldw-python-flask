// Dados dos fundadores
const founders = {
  miyazaki: {
    title: "Hayao Miyazaki",
    description:
      "Hayao Miyazaki é um diretor, animador e roteirista japonês. Ele é cofundador do Studio Ghibli e dirigiu filmes icônicos como 'A Viagem de Chihiro' e 'Meu Amigo Totoro'.",
  },
  takahata: {
    title: "Isao Takahata",
    description:
      "Isao Takahata foi um diretor e produtor japonês. Ele cofundou o Studio Ghibli e dirigiu filmes aclamados como 'O Túmulo dos Vagalumes' e 'Pom Poko'.",
  },
  suzuki: {
    title: "Toshio Suzuki",
    description:
      "Toshio Suzuki é um produtor japonês e cofundador do Studio Ghibli. Ele desempenhou um papel crucial na produção e promoção dos filmes do estúdio.",
  },
};

// Selecionar elementos
const founderNames = document.querySelectorAll(".founder-name");
const modal = document.getElementById("founder-modal");
const modalTitle = document.getElementById("modal-title");
const modalDescription = document.getElementById("modal-description");

// Adicionar eventos de mouse
founderNames.forEach((founder) => {
  founder.addEventListener("mouseenter", (e) => {
    const founderKey = e.target.getAttribute("data-founder");
    const founderData = founders[founderKey];

    // Atualizar o conteúdo do modal
    modalTitle.textContent = founderData.title;
    modalDescription.textContent = founderData.description;

    // Posicionar o modal próximo ao nome
    const rect = e.target.getBoundingClientRect();
    modal.style.top = `${rect.bottom + window.scrollY}px`;
    modal.style.left = `${rect.left + window.scrollX}px`;

    // Exibir o modal
    modal.classList.add("active");
  });

  founder.addEventListener("mouseleave", () => {
    // Esconder o modal
    modal.classList.remove("active");
  });
});

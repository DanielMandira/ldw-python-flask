document.addEventListener('DOMContentLoaded', function() {
    // Filtros de tarefa
    const priorityFilter = document.getElementById('priority-filter');
    const statusFilter = document.getElementById('status-filter');
    const taskCards = document.querySelectorAll('.task-card');
    const noTasksMessage = document.querySelector('.no-tasks');
  
    function applyFilters() {
        const selectedPriority = priorityFilter.value;
        const selectedStatus = statusFilter.value;
        let visibleTasks = 0;
  
        taskCards.forEach(card => {
            const cardPriority = card.querySelector('.task-priority').classList.contains(`priority-${selectedPriority}`);
            const cardStatus = card.querySelector('.task-status').classList.contains(`status-${selectedStatus}`);
  
            const showPriority = selectedPriority === 'all' || cardPriority;
            const showStatus = selectedStatus === 'all' || cardStatus;
            
            if (showPriority && showStatus) {
                card.style.display = 'block';
                visibleTasks++;
                // Adiciona animação de fade in
                card.style.opacity = '0';
                setTimeout(() => {
                    card.style.opacity = '1';
                }, 50);
            } else {
                card.style.display = 'none';
            }
        });

        // Mostra ou esconde a mensagem de "nenhuma tarefa"
        if (noTasksMessage) {
            if (visibleTasks === 0) {
                noTasksMessage.style.display = 'block';
                noTasksMessage.style.opacity = '0';
                setTimeout(() => {
                    noTasksMessage.style.opacity = '1';
                }, 50);
            } else {
                noTasksMessage.style.display = 'none';
            }
        }
    }
  
    if (priorityFilter && statusFilter) {
        priorityFilter.addEventListener('change', applyFilters);
        statusFilter.addEventListener('change', applyFilters);
    }

    // Fechar alertas com animação
    document.querySelectorAll('.alert-close').forEach(button => {
        button.addEventListener('click', () => {
            const alert = button.closest('.alert');
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        });
    });

    // Adiciona animação de fade in para os cards ao carregar a página
    taskCards.forEach((card, index) => {
        card.style.opacity = '0';
        setTimeout(() => {
            card.style.opacity = '1';
        }, index * 100);
    });
  
    // Inicializar filtros ao carregar
    applyFilters();
});
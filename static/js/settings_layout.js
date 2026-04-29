document.addEventListener("DOMContentLoaded", () => {
    loadLayout();

    const resetButton = document.getElementById("reset-layout-btn");

    if (resetButton) {
        resetButton.addEventListener("click", resetLayout);
    }
});

async function loadLayout() {
    const res = await fetch("/api/layout");
    const data = await res.json();

    const widgets = data.widgets;

    for (let i = 1; i <= 9; i++) {
        const select = document.getElementById("box" + i);
        if (!select) continue;

        select.innerHTML = "";

        widgets.forEach(w => {
            const option = document.createElement("option");
            option.value = w.id;
            option.textContent = w.name;
            select.appendChild(option);
        });
    }

    widgets.forEach(w => {
        const boxNumber = (w.row - 1) * 3 + w.col;
        const select = document.getElementById("box" + boxNumber);

        if (select) {
            select.value = w.id;
        }
    });
}

async function resetLayout() {
    await fetch("/api/layout/default", {
        method: "POST"
    });

    await loadLayout();
}
export async function updatePackages() {
    try {
        const response = await fetch('/widget/packages');
        const html = await response.text();
        const container = document.getElementById('packages');
        if (container) container.innerHTML = html;
    } catch (error) {
        console.error('Packages update failed:', error);
    }
}

// Update every 30 seconds
setInterval(updatePackages, 30000);
// Run once immediately
updatePackages();
// // static/frontend.js
// document.addEventListener('DOMContentLoaded', () => {
//   document.querySelectorAll('.toggle-btn').forEach(btn => {
//     btn.addEventListener('click', async () => {
//       const id = btn.dataset.id;
//       try {
//         const res = await fetch(`/toggle/${id}`, { method: 'POST' });
//         if (res.ok) {
//           // reload quickly to reflect change
//           window.location.reload();
//         } else {
//           alert('Toggle failed');
//         }
//       } catch (err) {
//         console.error(err);
//         alert('Error toggling device.');
//       }
//     });
//   });
// });


// static/frontend.js
document.addEventListener("DOMContentLoaded", () => {
  // Handle device toggle
  document.querySelectorAll(".toggle-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const id = btn.dataset.id;
      const res = await fetch(`/toggle/${id}`, { method: "POST" });
      const data = await res.json();

      // Update the status badge instantly
      const card = btn.closest("div.p-4");
      const badge = card.querySelector("span");
      if (data.status) {
        badge.textContent = "ON";
        badge.className = "px-2 py-1 rounded bg-green-100 text-green-800";
      } else {
        badge.textContent = "OFF";
        badge.className = "px-2 py-1 rounded bg-red-100 text-red-800";
      }

      // Optional: subtle animation
      card.classList.add("ring-2", "ring-pink-400");
      setTimeout(() => card.classList.remove("ring-2", "ring-pink-400"), 300);

      // Refresh dashboard stats
      updateStats();
    });
  });
});

// Refresh top stats dynamically
async function updateStats() {
  const res = await fetch("/stats");
  const data = await res.json();
  document.querySelector("strong:nth-of-type(1)").textContent = data.active_count;
  document.querySelector("strong:nth-of-type(2)").textContent = data.total_energy + " W";
}

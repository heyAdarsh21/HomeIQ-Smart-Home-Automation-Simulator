// const toggle = document.getElementById("theme-toggle")
// if (toggle) {
//   toggle.addEventListener("click", () => {
//     document.documentElement.classList.toggle("dark")
//     localStorage.setItem("theme", document.documentElement.classList.contains("dark") ? "dark" : "light");
//   })
// }

// if (localStorage.getItem("theme") === "dark") {
//   document.documentElement.classList.add("dark")
// }


const toggle = document.getElementById("theme-toggle");
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "dark") {
  document.documentElement.classList.add("dark");
} else if (savedTheme === "light") {
  document.documentElement.classList.remove("dark");
}

if (toggle) {
  toggle.addEventListener("click", () => {
    document.documentElement.classList.toggle("dark");
    if (document.documentElement.classList.contains("dark")) {
      localStorage.setItem("theme", "dark");
    } else {
      localStorage.setItem("theme", "light");
    }
  });
}

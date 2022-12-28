;(function () {
  const toastElement = document.getElementById("toast")
  const toastBody = document.getElementById("toast-body")
  const toast = new bootstrap.Toast(toastElement, { delay: 2500 })

  htmx.on("showMessage", (e) => {
    toastBody.innerText = e.detail.value
    toast.show()
  })

  htmx.on("showSuccess", (e) => {
    toastBody.innerText = e.detail.value
    toastElement.classList.add("bg-light");
    toastBody.classList.add("text-primary");
    toast.show()
  })

  htmx.on("showError", (e) => {
    toastBody.innerText = e.detail.value
    toastElement.classList.add("bg-light");
    toastBody.classList.add("text-danger");
    toast.show()
  })

})()

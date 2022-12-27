
;(function () {

  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #confirmation_modal_wrapper => show the modal
    if (e.detail.target.id == "confirmation_modal_wrapper") {
      const confirmation_modal = new bootstrap.Modal(document.getElementById("confirmation_modal"))
      confirmation_modal.show()
    }
  })

  htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #confirmation_modal_wrapper => hide the modal
    if (e.detail.target.id == "confirmation_modal_wrapper" && !e.detail.xhr.response) {
      const confirmation_modal = new bootstrap.Modal(document.getElementById("confirmation_modal"))
      confirmation_modal.hide()
      e.detail.shouldSwap = false
    }
  })

  // Remove dialog content after hiding
  htmx.on("hidden.bs.modal", () => {
    document.getElementById("confirmation_modal_wrapper").innerHTML = ""
  })
})()

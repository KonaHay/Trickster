
const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

const url = window.location.href

modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=>{
  const pk = modalBtn.getAttribute('data-pk')
  const quiz = modalBtn.getAttribute('data-quiz')
  const sections = modalBtn.getAttribute('data-sections')
  const imgURL = modalBtn.getAttribute('data-imgURL')

  modalBody.innerHTML = `
    <div class="h5 mb-3">Ready To Start? "<b>${quiz}</b>"?</div>

  `

  startBtn.addEventListener('click', ()=>{
    window.location.href = "/quiz/quiz_underway/" + pk
  })

}))



const url = window.location.href

const trickSection = document.getElementById('trick-section')
const trickBox = document.getElementById('trick-box')
const trickForm = document.getElementById('trick-form')

const quizSection = document.getElementById('quiz-section')
const quizBox = document.getElementById('quiz-box')
const quizForm = document.getElementById('quiz-form')

const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')


// ----- Trick Questions -----

$.ajax({
  type: 'GET',
  url: `${url}/tricks`,
  success: function(response){
    //console.log(response)

    const data = response.data

    data.forEach(el => {
      for (const [trick, scoreValue] of Object.entries(el)){
        trickBox.innerHTML += `
        <div class="col-sm">
          <div class="card text-bg-dark mb-3" style="width: 18rem; height: 15rem;">
            <div class="card-body">
              <h5 class="card-title text-center">
                <p name="${trick}" value="${scoreValue}">${trick}</p>
              </h5>
              <h6 class="text-center">
                ${scoreValue}
              </h6>
            </div>
            <div class="card-body-dark text-center gap-3" style="height: 3rem">
              <div class="form-check form-check-inline">
                <input type="checkbox" class="btn-check" id="${trick}" value="${scoreValue}" autocomplete="off">
                <label class="btn btn-outline-info" for="${trick}">Mark Trick As Learned</label><br>
              </div>      
            </div>
          </div>
        </div>
        `
      }
    })
  },
  error: function(error){
    console.log(error)
  }
})

const sendTrickData = () => {
  const elements = [...document.getElementsByClassName('btn-check')]
  const data = {}
  data['csrfmiddlewaretoken'] = csrf[0].value
  elements.forEach(el=>{
    if(el.checked) {
      data[el.id] = el.value
    }
  })

  $.ajax({
    type: 'POST',
    url: `${url}/next/`,
    data: data,
    success: function(response){
      console.log(response)
      const results = response.results
      trickSection.classList.add('d-none')
      quizSection.classList.remove('d-none')

    },
    error: function(error){
      //console.log(error)
    },
  })
}

trickForm.addEventListener('submit', e=>{
  e.preventDefault()

  sendTrickData()
}) 


// ----- Bonus Questions -----

$.ajax({
  type: 'GET',
  url: `${url}/data`,
  success: function(response){
    quizSection.classList.add('d-none')

    const data = response.data

    data.forEach(el => {
      for (const [question, answers] of Object.entries(el)){
        quizBox.innerHTML += `
          <hr>
          <div class="mb-2">
            <b>${question}</b>
          </div
        `
        answers.forEach(answer=>{
          quizBox.innerHTML += `
            <div>
              <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
              <label for="${question}">${answer}</label>
            </div>
          `
        })
      }
    }) 
  },
   error: function(error){
     console.log(error)
   }
})

const sendBonusData = () => {
  const elements = [...document.getElementsByClassName('ans')]
  const data = {}
  data['csrfmiddlewaretoken'] = csrf[0].value
  elements.forEach(el=>{
    if(el.checked) {
      data[el.name] = el.value
    } else {
      if (!data[el.name]){
        data[el.name] = null
      }
    }
  })

  $.ajax({
    type: 'POST',
    url: `${url}/save/`,
    data: data,
    success: function(response){
      const results = response.results
      quizForm.classList.add('d-none')

      results.forEach(res=>{
        const resDiv = document.createElement("div")
        for (const [question, resp] of Object.entries(res)){
          resDiv.innerHTML += question
          const cls = ['container', 'p-3', 'text-light', 'h3']
          resDiv.classList.add(...cls)

          if (resp=='not answered') {
            resDiv.innerHTML += '- not answered'
            resDiv.classList.add('bg-danger')
          } else {
            const answer = resp['answered']
            const correct = resp['correct_answer']
            if (answer == correct) {
              resDiv.classList.add('bg-success')
              resDiv.innerHTML += ` answered: ${answer}`
            } else {
              resDiv.classList.add('bg-danger')
              resDiv.innerHTML += ` correct answer: ${correct}`
              resDiv.innerHTML += ` answered: ${answer}`
            }
          }
        }
        resultBox.append(resDiv)
      })
    },
    error: function(error){
      console.log(error)
    },
  })
}

quizForm.addEventListener('submit', e=>{
  e.preventDefault()

  sendBonusData()
}) 
const url = window.location.href

const trickSection = document.getElementById('trick-section')
const trickBox = document.getElementById('trick-box')
const trickForm = document.getElementById('trick-form')

const quizSection = document.getElementById('quiz-section')
const quizBox = document.getElementById('quiz-box')
const quizForm = document.getElementById('quiz-form')

const trickScore = document.getElementById('trick-score')

const sectionComplete = document.getElementById('section-complete')
const quizComplete = document.getElementById('quiz-complete')

const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')


// ----- Trick Questions -----

$.ajax({
  type: 'GET',
  url: `${url}/tricks`,
  success: function(response){
    const data = response.data

    data.forEach(el => {
      for (const [trick, trickImg] of Object.entries(el)){
        if (trickImg != "null"){
          trickBox.innerHTML += `
          <div class="col-sm">
          <div class="card text-bg-dark mb-3" style="width: 18rem; height: 17rem;">
            <div class="card-body">
              <h5 class="card-title text-center">
                <img src="${trickImg}" class="img-fluid rounded" alt="trick cover image">
              </h5>
              <h5 class="text-center">
                <p name="${trick}" value="${trickImg}">${trick}</p>
              </h5>
            </div>
            <div class="card-body-dark text-center gap-3" style="height: 3rem">
              <div class="form-check form-check-inline">
                <input type="checkbox" class="btn-check" id="${trick}"  autocomplete="off">
                <label class="btn btn-outline-info" for="${trick}">Mark Trick As Learned</label><br>
              </div>      
            </div>
          </div>
        </div>`
        }else{
          trickBox.innerHTML += `
          <div class="col-sm">
          <div class="card text-bg-dark mb-3" style="width: 18rem; height: 17rem;">
            <div class="card-body">
              <h5 class="card-title text-center">
                <img src="/static/trickster/images/TrickListDefault.png" class="img-fluid rounded" alt="default trick cover image">
              </h5>
              <h5 class="text-center">
              <p name="${trick}" value="${trickImg}">${trick}</p>
              </h5>
            </div>
            <div class="card-body-dark text-center gap-3" style="height: 3rem">
              <div class="form-check form-check-inline">
                <input type="checkbox" class="btn-check" id="${trick}"  autocomplete="off">
                <label class="btn btn-outline-info" for="${trick}">Mark Trick As Learned</label><br>
              </div>      
            </div>
          </div>
        </div>`
        }
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
      const score = response.score

      trickScore.innerHTML = `${score}`

      trickSection.classList.add('d-none')
      quizSection.classList.remove('d-none')

    },
    error: function(error){
      console.log(error)
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
    //quizSection.classList.add('d-none')

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
  score = trickScore.innerHTML
  data["score"] = score

  $.ajax({
    type: 'POST',
    url: `${url}/save/`,
    data: data,
    success: function(response){
      quizSection.classList.add('d-none')
      console.log(response)

      const sectDiv = document.createElement("div")

      const score = response.score
      const nextSection = response.nextSection
      
      if(nextSection>=5) {
        quizComplete.classList.remove('d-none') 
      }else{
        sectDiv.innerHTML += ` 
        <h1> Section Complete! </h1>
        <h4> To move on to the next section click the "Next Section" button below. </h4>
        <hr>
        <br>
        <a href="/quiz/quiz_underway/${nextSection}" class="btn btn-success">Next Section</a>
        `
      }

      sectionComplete.append(sectDiv)
      sectionComplete.classList.remove('d-none')
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
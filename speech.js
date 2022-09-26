const span = document.querySelector("#results")
const btnGravar = document.querySelector("#btnGravar")
const btnParar = document.querySelector("#btnParar")

var isOn = false // variável para evitar o desligamento automático do microfone

class speechApi {

    constructor() {

        const SpeechToText = window.SpeechRecognition || window.webkitSpeechRecognition || null
        console.log(SpeechToText)
        this.speechApi = new SpeechToText()
        this.output = span.output
        this.speechApi.continuous = true
        this.speechApi.lang = "pt-BR"

        if (SpeechToText === null) {
            let p = document.createElement("p")
            p.innerText = "Não estamos oferecendo suporte para o seu navegador agora, tente usa o Google Chrome ou o Edge."

            span.appendChild(p)
        }

        this.speechApi.onresult = (e) => {
            var resultIndex = e.resultIndex
            var transcript = e.results[resultIndex][0].transcript

            console.log(transcript)
            let p = document.createElement("p")
            p.innerText = transcript

            span.appendChild(p)

            span.scrollTop = span.scrollHeight
        }
        this.speechApi.onend = (e) => {
            console.log("Desligou")
            if (isOn) {
                this.speechApi.start()
            }
        }
    }

    start() {
        isOn = true
        this.speechApi.start()
    }

    stop() {
        isOn = false
        this.speechApi.stop()
    }
}

var speech = new speechApi()

btnGravar.addEventListener("click", e => {
    btnGravar.disabled = true
    btnParar.disabled = false
    speech.start()
})

btnParar.addEventListener("click", () => {
    btnGravar.disabled = false
    btnParar.disabled = true
    speech.stop()
})
const span = document.querySelector("#results")
const btnMic = document.querySelector("#btnMic")
const btnLang = document.querySelector("#lang")
const btnReduceFont = document.querySelector("#btnReduce")
const btnIncreaseFont = document.querySelector("#btnIncrease")
const bottom = document.querySelector("#bottom")
const topPage = document.querySelector("#top")
const theme = document.querySelector("#theme");
const screen = document.querySelector("#screen")

var isOn = false // variável para evitar o desligamento automático do microfone
var themeSunny = false // variável para controlar o tema do site 
var isHover = $(bottom).is(":hover") || $(topPage).is(":hover") // impedir que os botões desapareçam quando o mouse estiver em cima deles
var isHoverLast = false // impedir que os botões apareção quando o texto é atualizado (algo chama o evendo de "mouse out" e o botões aparecem com visibilidade 0.5)

class speechApi {

    constructor() {

        const SpeechToText = window.SpeechRecognition || window.webkitSpeechRecognition || null

        if (SpeechToText === null) {
            let p = document.createElement("p")
            p.innerText = "Não estamos oferecendo suporte para o seu navegador agora, tente usa o Google Chrome ou o Edge."

            span.appendChild(p)
        }

        console.log(SpeechToText)
        this.speechApi = new SpeechToText()
        this.output = span.output
        this.speechApi.continuous = true

        // verificar se o idioma já foi selecionado
        if (localStorage.getItem("lang") !== null) {
            this.speechApi.lang = localStorage.getItem("lang")
            btnLang.selectedIndex = localStorage.getItem("langIndex")
        }
        else {
            this.speechApi.lang = "pt-BR"
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

btnMic.addEventListener("click", e => {
    if (isOn) {
        speech.stop()
        // mudar imagem do botão
        btnMic.style.backgroundImage = "url('../icons/mic-off.png')"
    }
    else {
        speech.start()
        // mudar imagem do botão
        btnMic.style.backgroundImage = "url('../icons/mic.png')"
    }
})

btnLang.addEventListener("click", e => {
    console.log("Clicou")

    let isRunning = isOn
    speech.stop()
    // mudar para idioma selecionado
    const index = btnLang.selectedIndex
    speech.speechApi.lang = btnLang.options[index].value

    console.log(speech.speechApi.lang)
    if (isRunning) {
        speech.start()
    }

    // salvar no local storage
    localStorage.setItem("lang", btnLang.options[index].value)
    localStorage.setItem("langIndex", index)

})

theme.addEventListener("click", e => {
    if (themeSunny) {
        themeSunny = false
        theme.style.backgroundImage = "url('../icons/sunny.png')"
        document.body.style.backgroundColor = "#396575"
        span.style.color = "#fff"
        span.style.fontWeight = "400"
    }
    else {
        themeSunny = true
        theme.style.backgroundImage = "url('../icons/moon.png')"
        document.body.style.backgroundColor = "#FEFEFE"
        span.style.color = "#000"
        span.style.fontWeight = "700"
    }
})

btnReduceFont.addEventListener("click", e => {
    let fontSize = parseInt(window.getComputedStyle(span).fontSize)
    console.log(fontSize)
    if (fontSize > 25) {
        span.style.fontSize = (fontSize - 2) + "px"
    }
})

btnIncreaseFont.addEventListener("click", e => {
    let fontSize = parseInt(window.getComputedStyle(span).fontSize)
    console.log(fontSize)
    if (fontSize < 65) {
        span.style.fontSize = (fontSize + 2) + "px"
    }
})

//fullscreen and exit fullscreen
screen.addEventListener("click", e => {
    if (document.fullscreenElement) {
        document.exitFullscreen()
        screen.style.backgroundImage = "url('../icons/fullscreen.png')"
    }
    else {
        document.documentElement.requestFullscreen()
        screen.style.backgroundImage = "url('../icons/fullscreen-exit.png')"
    }
})

document.addEventListener("fullscreenchange", e => {
    if (document.fullscreenElement) {
        screen.style.backgroundImage = "url('../icons/fullscreen-exit.png')"
    }
    else {
        screen.style.backgroundImage = "url('../icons/fullscreen.png')"
    }
})

//visibility
let visibility = function () {
    bottom.style.opacity = "1"
    topPage.style.opacity = "1"
    isHoverLast = true
}

let invisibility = function () {
    //verificar se o mouse está em cima
    isHover = $(bottom).is(":hover") || $(topPage).is(":hover")
    if (!isHover && isHoverLast) {
        setTimeout(() => {
            if (!isHover && isHoverLast) {
                bottom.style.opacity = "0.5"
                topPage.style.opacity = "0.5"
            }

            setTimeout(() => {
                if (!isHover && isHoverLast) {
                    bottom.style.opacity = "0"
                    topPage.style.opacity = "0"
                    isHoverLast = false
                }

            }, 5000)
        }, 5000)
    }

}

// Element visibility events
bottom.addEventListener("mouseover", e => { visibility() })
bottom.addEventListener("mouseout", e => { invisibility() })

topPage.addEventListener("mouseover", e => { visibility() })
top.addEventListener("mouseout", e => { invisibility() })

/* bottom.addEventListener("mouseover", e => {
    bottom.style.opacity = "1"
    // Esperar 3 segundos e esconder o botão

}) */

// quando o mouse sair da área do botão, esconder o botão
/* bottom.addEventListener("mouseout", e => {
    console.log("Saiu")
    setTimeout(() => {
        bottom.style.opacity = "0.5"
        console.log('passou 5 segundos')
        setTimeout(() => {
            bottom.style.opacity = "0"
            console.log('escondeu 5 segundos')
        }, 5000)
    }, 5000)

})
 */
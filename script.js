document.addEventListener('DOMContentLoaded', () => {
    var myLandbot = new Landbot.Livechat({ configUrl: 'https://landbot.online/v3/H-2714588-IFOFHWR8BIKXD7FA/index.html', }); });

// Função para o formulário de login
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
});
// Função para o formulário de registro
document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();
});

function cliente() {
    var nome = document.getElementById('nome').value;
    var erroMsg = '';
    if ( nome === '') {
        erroMsg.innerText = 'Todos os campos são obrigatórios!';
    }
    else{
    window.location.href = 'logincliente.html';
    }
}

function funcionario() {
    var nome = document.getElementById('nome').value;
    var erroMsg = '';
    if ( nome === '') {
        erroMsg.innerText = 'Todos os campos são obrigatórios!';
    }
    else{
        window.location.href = 'loginfunc.html';
        }
    }
function entrada() {
            window.location.href = 'entrada.html';
    }

    function p1() {
        window.location.href = 'produto1.html';
}

function p2() {
    window.location.href = 'produto2.html';
}

function p3() {
    window.location.href = 'produto3.html';
}

function logincliente() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var erroMsg = '';
    if ( email === '' || password === '' ) {
        erroMsg.innerText = 'Todos os campos são obrigatórios!';
    }
    else{
    window.location.href = 'areacliente.html';
    }
}

function loginfunc() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var erroMsg = '';
    if ( email === '' || password === '' ) {
        erroMsg.innerText = 'Todos os campos são obrigatórios!';
    }
    else{
    window.location.href = 'entrada.html';
    }
}






















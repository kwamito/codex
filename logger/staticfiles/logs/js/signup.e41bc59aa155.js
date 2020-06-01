const button = document.querySelector('#buut')
const parent = document.querySelector('.parent')
button.addEventListener('click',(e) => {
    parent.innerHTML = '<div class="spinner-grow" style="width: 3rem; height: 3rem;" role="status"><span class="sr-only">Loading...</span></div>';
    setTimeout(() => {
        parent.innerHTML = '';
    },3000)
})
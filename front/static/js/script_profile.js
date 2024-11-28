document.addEventListener('DOMContentLoaded', () => {
    const mainSection = document.querySelector('.main');

    mainSection.addEventListener('wheel', (event) => {
        event.preventDefault();
        mainSection.scrollTop += event.deltaY * 0.5;
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const mainSection = document.querySelector('#comments');

    mainSection.addEventListener('wheel', (event) => {
        event.preventDefault();
        mainSection.scrollTop += event.deltaY * 0.5;
    });
});

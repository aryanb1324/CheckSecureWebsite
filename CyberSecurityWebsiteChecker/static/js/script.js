document.addEventListener('DOMContentLoaded', function () {
   // Example of animation on button hover
    const button = document.querySelector('button');

    button.addEventListener('mouseover', () => {
        button.style.transform = 'scale(1.1)';
    });

    button.addEventListener('mouseout', () => {
        button.style.transform = 'scale(1)';
    });
});
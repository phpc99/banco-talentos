// JS: troca thumbnail por iframe do YouTube
// LIXO, usei INCORPORAR do yt

document.addEventListener('DOMContentLoaded', function () {
    const embed = document.querySelector('.video-embed');
    if (!embed) return;

    const btn = embed.querySelector('.video-thumb');
    if (!btn) return;

    btn.addEventListener('click', function () {
        const videoId = embed.getAttribute('data-video-id');
        if (!videoId || videoId === "YOUTUBE_ID") return;

        const iframe = document.createElement('iframe');
        iframe.setAttribute('width', '100%');
        iframe.setAttribute('height', '360');
        iframe.setAttribute('frameborder', '0');
        iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
        iframe.setAttribute('allowfullscreen', 'true');

        // autoplay = 1 para começar ao clicar
        iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;

        embed.innerHTML = '';
        embed.appendChild(iframe);
    });
});
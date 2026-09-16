// Native controls; no autoplay, loop, external host, or required narration.
export default {
  render({el,model}) {
    const host=el.closest('.lecture-film') || el.getRootNode().host?.closest('.lecture-film');
    const image=host?.querySelector('img');
    const link=host?.querySelector('a[href]');
    if(!image || !link) return;
    const video=document.createElement('video');
    video.src=link.href;
    video.poster=image.currentSrc || image.src;
    video.controls=true;
    video.preload='none';
    video.playsInline=true;
    video.setAttribute('aria-label',model.get('description'));
    video.append(document.createTextNode('Use the download link or static frame if playback is unavailable.'));
    host.append(video);
    host.classList.add('player-ready');
    const visibility=()=>{if(document.hidden)video.pause();};
    document.addEventListener('visibilitychange',visibility);
    return ()=>{video.pause();video.remove();video.removeAttribute('src');video.load();document.removeEventListener('visibilitychange',visibility);};
  },
};

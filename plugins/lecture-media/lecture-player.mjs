// Native controls; no autoplay, loop, external host, or required narration.
export default {
  render({el,model}) {
    const host=el.closest('.lecture-film') || el.getRootNode().host?.closest('.lecture-film');
    const image=host?.querySelector('img');
    const link=host?.querySelector('a[href]');
    if(!image || !link) return;
    const video=document.createElement('video');
    // Static copies keep URLs stable when MyST rebuilds its hashed assets.
    const mediaUrl=model.get('mediaUrl');
    if(mediaUrl) link.href=mediaUrl;
    video.src=link.href;
    video.poster=image.currentSrc || image.src;
    video.controls=true;
    video.preload='none';
    video.playsInline=true;
    video.setAttribute('aria-label',model.get('description'));
    video.append(document.createTextNode('Use the download link or static frame if playback is unavailable.'));
    host.append(video);
    host.classList.add('player-ready');
    const failure=document.createElement('p');
    failure.className='lecture-film-error';
    failure.setAttribute('role','status');
    failure.hidden=true;
    failure.textContent='The video could not load. Reload this page, or try the open/download link. The static frame and explanation remain available.';
    host.append(failure);
    const failed=()=>{failure.hidden=false;host.classList.remove('player-ready');};
    video.addEventListener('error',failed);
    const visibility=()=>{if(document.hidden)video.pause();};
    document.addEventListener('visibilitychange',visibility);
    return ()=>{failure.remove();video.removeEventListener('error',failed);video.pause();video.remove();video.removeAttribute('src');video.load();document.removeEventListener('visibilitychange',visibility);};
  },
};
